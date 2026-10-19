"""Turn an NCERT chapter PDF into Markdown using PyMuPDF block geometry.

The books (Our Pasts II and III, 2007 to 2025) share one design: a wide body column
set in Bookman 13 pt, a narrow side column with notes and figure captions, chapter
and section headings in Lucida Sans bold, quoted sources in Monotype Corsiva, and a
running footer with the page number and book or chapter name. Older files carry a
rotated "©NCERT not to be republished" watermark in the text layer.

Every text block is given a role. Body paragraphs are written as plain Markdown
paragraphs. Everything else is kept but tagged, so later diffs can choose what to
compare. Page boundaries are kept as HTML comments.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from . import clean

HORIZONTAL = (1.0, 0.0)
CHAPTER_NUMBER = re.compile(r"^(\d{1,2})\b|\b(\d{1,2})$")
SESSION_LABEL = re.compile(r"(Reprint|Rationalised)?\s*20\d\d-\d\d")  # "2018-19" print-run footers
# Running titles set at body size: "32 Social and Political Life", "Chapter 3: How the State Government Works 31".
RUNNING_TITLE = re.compile(r"^(?:\d{1,3}\s+[A-Z][^.?!]{3,55}|[A-Z][^.?!]{3,55}\s\d{1,3}|Chapter \d{1,2}: [A-Z][^.?!]{3,55})$")
UNREADABLE = "[unreadable]"  # text set in a font without a Unicode map comes out as blanks
# Headings that label a unit or chapter rather than name it. Not titles, not evidence of a chapter opener.
LABEL_HEADING = re.compile(r"^(unit\s+\w+|chapter\s*\d*|contents|notes|teacher[’']s note)[\s:.-]*$", re.IGNORECASE)
DROPCAP_LINE = re.compile(r"^[A-Z] [a-z]")  # a drop cap glued to its line ("Y crafts and production") is not a heading
TEACHERS_NOTE = re.compile(r"^teacher[’']s note", re.IGNORECASE)
UNIT_OPENER = re.compile(r"^(unit(\s+\w+)?|one|two|three|four|five|six|seven|eight|nine|ten)$", re.IGNORECASE)
UNIT_WORD = re.compile(r"^(unit|one|two|three|four|five|six|seven|eight|nine|ten)$", re.IGNORECASE)  # unit openers set one word per line
ICON_FONT = re.compile(r"webdings|wingdings|dingbat|zapfdingbats", re.IGNORECASE)
CHAPTER_LABEL = re.compile(r"^chapter\s+(\d{1,2})$", re.IGNORECASE)
ACTIVITY_HEADING = re.compile(r"Let[’']s (recall|discuss|do|understand|imagine|find out|write)", re.IGNORECASE)
FOOTER_BAND = 0.86  # fraction of page height below which small text is a footer
HEADER_BAND = 0.06
TITLE_BAND = 0.40  # chapter numbers live in the top part of the opening page
# Everything else is relative to the body size measured per document (13 pt in Our Pasts II,
# 11 pt in Our Pasts III), see font_profile().
DEFAULT_BODY_SIZE = 13.0


@dataclass
class Block:
    x0: float
    y0: float
    x1: float
    y1: float
    font: str
    size: float
    bold: bool
    italic: bool
    text: str
    max_size: float = 0.0
    role: str = "unknown"

    @property
    def centre_x(self) -> float:
        return (self.x0 + self.x1) / 2


@dataclass
class Page:
    index: int  # zero-based pdf page
    printed_number: int | None
    blocks: list[Block] = field(default_factory=list)
    source: str | None = None  # file name when the page was carried over from another chapter PDF


def _span_flags(span: dict) -> tuple[bool, bool]:
    font = span["font"]
    bold = bool(span["flags"] & 16) or "Bold" in font or "Demi" in font
    italic = bool(span["flags"] & 2) or "Italic" in font or "Corsiva" in font
    return bold, italic


def _overlap_ratio(a: tuple, b: tuple) -> float:
    """Intersection area over the smaller of the two boxes."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    smaller = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return ix * iy / smaller if smaller > 0 else 0.0


def _dedupe_shadow_spans_keep_blank(lines: list[dict]) -> list[list[dict]]:
    return _dedupe_shadow_spans(lines)


def _dedupe_shadow_spans(lines: list[dict]) -> list[list[dict]]:
    """Drop spans drawn on top of an identical earlier span (shadow and fake-bold effects).

    NCERT's PDFs draw some headings up to five times with sub-point offsets. Each copy
    becomes its own line, sometimes sharing a line with the next word. Keeping the first
    copy of every (text, position) pair reconstructs the heading once.
    """
    kept: list[tuple[str, tuple]] = []
    out: list[list[dict]] = []
    for ln in lines:
        spans = []
        for s in ln["spans"]:
            text = s["text"].strip()
            if text and any(text == t and _overlap_ratio(s["bbox"], bb) >= 0.7 for t, bb in kept):
                continue
            if text:
                kept.append((text, s["bbox"]))
            spans.append(s)
        if any(s["text"].strip() for s in spans) or any(len(s["text"]) >= 3 and s["bbox"][2] - s["bbox"][0] > 20 for s in spans):
            out.append(spans)
    return out


OutlinedReader = Callable[[pymupdf.Page, pymupdf.Rect], str | None]


def outlined_word_rects(page: pymupdf.Page) -> list[pymupdf.Rect]:
    """Runs of filled glyph outlines on one baseline: text the typesetter converted to curves.

    NCERT's 2024-25 Our Pasts II files draw transliterated terms with diacritics
    ("dehlīwāl", "tawārīkh") this way, and sometimes whole lines, so the words are absent
    from the text layer. Glyph drawings sharing a baseline are merged, across word spaces,
    into one run per line fragment so that tesseract reads whole words.
    """
    glyphs = []
    for d in page.get_drawings():
        r = d["rect"]
        if d["type"] == "f" and len(d["items"]) >= 12 and 4 <= r.height <= 30 and 1.5 <= r.width <= 250:
            glyphs.append(pymupdf.Rect(r))
    # Baseline groups: glyphs whose bottoms are within 4 pt of the group's bottom.
    groups: list[list[pymupdf.Rect]] = []
    for g in sorted(glyphs, key=lambda r: r.y1):
        if groups and abs(groups[-1][-1].y1 - g.y1) <= 4:
            groups[-1].append(g)
        else:
            groups.append([g])
    runs: list[pymupdf.Rect] = []
    for group in groups:
        group.sort(key=lambda r: r.x0)
        current = pymupdf.Rect(group[0])
        for g in group[1:]:
            if -2 <= g.x0 - current.x1 <= max(9.0, 0.8 * current.height):
                current |= g
            else:
                runs.append(current)
                current = pymupdf.Rect(g)
        runs.append(current)
    return [r for r in runs if r.width >= 12 and 6 <= r.height <= 30]


def read_blocks(page: pymupdf.Page, read_outlined: OutlinedReader | None = None) -> list[Block]:
    """Text blocks with rotated (watermark) lines removed and lines joined."""
    textpage = page.get_text("dict")
    if read_outlined is not None:
        _fill_outlined_words(page, textpage, outlined_word_rects(page), read_outlined)
    return blocks_from_dict(textpage)


def _fill_outlined_words(page: pymupdf.Page, textpage: dict, rects: list[pymupdf.Rect], read_outlined: OutlinedReader) -> None:
    """Insert OCR'd pseudo-spans for outlined runs: into a gap of a text line, or as a new line."""
    if not rects:
        return
    text_blocks = [b for b in textpage["blocks"] if b["type"] == 0]
    all_lines = [
        (raw, ln) for raw in text_blocks for ln in raw["lines"]
        if tuple(round(v, 1) for v in ln["dir"]) == HORIZONTAL and any(sp["text"].strip() for sp in ln["spans"])
    ]
    for r in rects:
        cy = (r.y0 + r.y1) / 2
        # The text line this run belongs to: nearest vertical centre among lines it touches horizontally.
        best = None
        for raw, ln in all_lines:
            lx0, ly0, lx1, ly1 = ln["bbox"]
            if r.x1 < lx0 - 3 or r.x0 > lx1 + 3 or r.height > 1.4 * (ly1 - ly0):
                continue
            dist = abs((ly0 + ly1) / 2 - cy)
            if dist <= 0.4 * (ly1 - ly0) and (best is None or dist < best[0]):
                best = (dist, ln)
        if best is not None:
            ln = best[1]
            spans = [sp for sp in ln["spans"] if sp["text"].strip()]
            if any(sp["bbox"][0] < r.x1 - 2 and sp["bbox"][2] > r.x0 + 2 for sp in spans):
                continue  # overlaps real text: decoration behind it, or invisible text already there
            word = read_outlined(page, r)
            if not word:
                continue
            nxt = next((sp for sp in spans if sp["bbox"][0] >= r.x1 - 2), None)
            if nxt and word[-1] in ",.;:" and nxt["text"].lstrip().startswith(word[-1]):
                word = word[:-1]
            ln["spans"].append({"text": f" {word} ", "bbox": tuple(r), "size": spans[0]["size"], "font": "OUTLINED", "flags": 2})
            ln["spans"].sort(key=lambda sp: sp["bbox"][0])
            continue
        # No text line there: a whole outlined line. Attach it to the block it sits in or next to.
        word = read_outlined(page, r)
        if not word:
            continue
        host = None
        for raw in text_blocks:
            bx0, by0, bx1, by1 = raw["bbox"]
            if r.x0 < bx1 + 4 and r.x1 > bx0 - 4 and by0 - r.height * 1.6 <= cy <= by1 + r.height * 1.6:
                host = raw
                break
        size = max((sp["size"] for ln in host["lines"] for sp in ln["spans"]), default=r.height * 0.9) if host else r.height * 0.9
        line = {"dir": (1.0, 0.0), "bbox": tuple(r), "spans": [{"text": word, "bbox": tuple(r), "size": size, "font": "OUTLINED", "flags": 2}]}
        if host:
            host["lines"].append(line)
            host["lines"].sort(key=lambda ln: ln["bbox"][1])
            host["bbox"] = tuple(pymupdf.Rect(host["bbox"]) | r)
        else:
            textpage["blocks"].append({"type": 0, "bbox": tuple(r), "lines": [line]})
            text_blocks.append(textpage["blocks"][-1])


def blocks_from_dict(textpage: dict) -> list[Block]:
    out: list[Block] = []
    for raw in textpage["blocks"]:
        if raw["type"] != 0:
            continue
        lines = [ln for ln in raw["lines"] if tuple(round(v, 1) for v in ln["dir"]) == HORIZONTAL]
        if not lines:
            continue
        sizes: Counter = Counter()
        fonts: Counter = Counter()
        flags: Counter = Counter()
        texts: list[str] = []
        max_size = 0.0
        for ln in lines:
            # Icon fonts carry activity glyphs ("Q" in Webdings is a question-mark bubble), not words.
            ln["spans"] = [sp for sp in ln["spans"] if not ICON_FONT.search(sp["font"])]
            for sp in ln["spans"]:
                sp["text"] = decode_symbol_font(sp["text"])
        for spans in _dedupe_shadow_spans(lines):
            joined = _join_spans(spans)
            if not joined.strip() and any(len(sp["text"]) >= 3 and sp["bbox"][2] - sp["bbox"][0] > 20 for sp in spans):
                joined = UNREADABLE  # glyphs are drawn but the font maps them to nothing
                for sp in spans:
                    sizes[round(sp["size"], 1)] += 10
                    fonts[sp["font"]] += 10
                    flags[_span_flags(sp)] += 10
            texts.append(joined)
            for s in spans:
                max_size = max(max_size, s["size"])
                n = len(s["text"].strip())
                if n:
                    sizes[round(s["size"], 1)] += n
                    fonts[s["font"]] += n
                    flags[_span_flags(s)] += n
        text = clean.join_lines(texts)
        if not text or not sizes or not clean.has_content(text):
            continue
        size = sizes.most_common(1)[0][0]
        font = fonts.most_common(1)[0][0]
        bold, italic = flags.most_common(1)[0][0]
        x0, y0, x1, y1 = raw["bbox"]
        out.append(Block(x0, y0, x1, y1, font, size, bold, italic, text, max_size))
    return out


def decode_symbol_font(text: str) -> str:
    """Some files (the 2022-23 Social and Political Life III) map body text to the private-use
    range U+F020 to U+F0FF, one code per Windows-1252 byte. Translate it back."""
    if not any("\uf020" <= ch <= "\uf0ff" for ch in text):
        return text
    out = []
    for ch in text:
        if "\uf020" <= ch <= "\uf0ff":
            out.append(bytes([ord(ch) - 0xF000]).decode("cp1252", "replace"))
        else:
            out.append(ch)
    return "".join(out)


def _join_spans(spans: list[dict]) -> str:
    """Concatenate span texts, adding a space where a huge glyph abuts normal text ("2" + "NEW")."""
    out = ""
    prev_size = None
    for s in spans:
        t = s["text"]
        if out and t and prev_size and not out[-1].isspace() and not t[0].isspace():
            big, small = max(prev_size, s["size"]), min(prev_size, s["size"])
            if small and big / small > 1.8:
                out += " "
        out += t
        prev_size = s["size"]
    return out


def font_profile(pages_blocks: list[list[Block]]) -> float:
    """The body text size of a document.

    Among plain prose blocks, the largest size that carries at least a quarter of the
    characters. "Largest" rather than "commonest" because a long teacher's note or glossary
    set a point or two smaller can outweigh the body text in a short chapter, and the body
    text is never the smaller of two prose sizes."""
    sizes: Counter = Counter()
    for blocks in pages_blocks:
        for b in blocks:
            if not b.bold and 9.0 <= b.size <= 14.5 and len(b.text) > 60:
                sizes[b.size] += len(b.text)
    if not sizes:
        return DEFAULT_BODY_SIZE
    total = sum(sizes.values())
    big = [size for size, n in sizes.items() if n >= 0.25 * total]
    return max(big) if big else sizes.most_common(1)[0][0]


SIDE_FONTS = ("Lucida", "Courier")  # fonts the books reserve for side notes and activity boxes


def classify(blocks: list[Block], width: float, height: float, body_size: float = DEFAULT_BODY_SIZE) -> int | None:
    """Assign a role to each block in place. Returns the printed page number if found."""
    printed: int | None = None
    near = lambda s, target, tol=0.6: abs(s - target) <= tol  # noqa: E731
    body = [b for b in blocks if near(b.size, body_size) and not b.bold and len(b.text) > 40]
    if body:
        col_left = min(b.x0 for b in body) - 6
        col_right = max(b.x1 for b in body) + 6
    else:
        col_left, col_right = 0.0, width

    for b in blocks:
        in_column = col_left <= b.centre_x <= col_right
        side_font = any(f in b.font for f in SIDE_FONTS)
        delta = body_size - b.size  # positive when smaller than body text
        # Footers are short and set small. An exercise question that happens to end the
        # page is neither, even though it sits in the same band.
        # "2022-23" is a print-run label, not page 23. Some files glue it to the running title.
        bare = SESSION_LABEL.sub("", b.text).strip()
        running = RUNNING_TITLE.fullmatch(bare) and len(bare.split()) >= 3
        short = len(b.text) <= 60 or (running and len(b.text) <= 80)  # a glued "Rationalised 2023-24" makes a running title longer
        if b.y0 > FOOTER_BAND * height and short and (delta >= 1.4 or len(b.text) <= 4 or SESSION_LABEL.fullmatch(b.text) or running):
            b.role = "footer"
            m = re.match(r"^(\d{1,3})\b", bare) or re.search(r"\b(\d{1,3})$", bare)
            if m and printed is None:
                printed = int(m.group(1))
            continue
        if b.y1 < HEADER_BAND * height and len(b.text) <= 60 and delta >= 1.4:
            b.role = "footer"
            continue
        if b.size >= 2 * body_size and len(b.text) <= 2 and not b.text.isdigit():
            b.role = "dropcap"
            continue
        if (b.max_size >= 2 * body_size and CHAPTER_NUMBER.search(b.text) and b.y0 < TITLE_BAND * height) or (
            CHAPTER_LABEL.match(b.text) and b.size >= body_size + 2 and b.y0 < TITLE_BAND * height
        ):
            b.role = "chapter-number"
            continue
        if b.size >= body_size + 2.5 and len(b.text) <= 160:
            letters = sum(ch.isalpha() for ch in b.text)
            if letters >= 2:
                b.role = "h2"
            elif letters == 1 and len(b.text) == 1:
                b.role = "dropcap"  # OCR sees the drop cap as an oversized one-letter paragraph
            else:
                b.role = "decoration"
            continue
        if b.bold and b.size >= body_size + 0.8 and len(b.text) <= 120:
            b.role = "h3"  # headings are short; some fonts report every weight as bold
            continue
        if "Corsiva" in b.font:
            b.role = "source"
            continue
        if ACTIVITY_HEADING.fullmatch(b.text):
            b.role = "h3"
            continue
        if delta > 2.4 or (b.italic and delta >= 1.4):
            b.role = "caption"
            continue
        if not in_column:
            b.role = "caption" if delta > 1.4 else "note"
            continue
        if side_font and delta > -0.6:
            b.role = "note"
            continue
        if delta <= 1.4 or len(b.text) > 200:
            b.role = "body"  # body text, smaller exercise questions, or a long note set smaller
            continue
        b.role = "table"
    return printed


def _read_all_pages(pdf_path: Path) -> tuple[list[Page], float]:
    from .ocr import outlined_reader  # lazy: tesseract is optional

    reader = outlined_reader(pdf_path)
    pages: list[Page] = []
    width = 600.0
    with pymupdf.open(pdf_path) as doc:
        raw = []
        for i, page in enumerate(doc):
            if i == 0:
                width = page.rect.width
            raw.append((i, read_blocks(page, reader), page.rect.width, page.rect.height))
    body_size = font_profile([blocks for _, blocks, _, _ in raw])
    for i, blocks, w, h in raw:
        printed = classify(blocks, w, h, body_size)
        pages.append(Page(i, printed, blocks))
    fix_page_numbers(pages)
    return pages, width


def has_text_layer(pdf_path: Path, min_chars_per_page: int = 200) -> bool:
    """False for scanned or rasterised PDFs that carry no usable text (they need OCR)."""
    with pymupdf.open(pdf_path) as doc:
        if doc.page_count == 0:
            return False
        sample = list(doc.pages(0, min(doc.page_count, 4)))
        chars = sum(len(p.get_text()) for p in sample)
    return chars >= min_chars_per_page * len(sample)


def read_pages(pdf_path: Path) -> list[Page]:
    pages, _ = _read_all_pages(pdf_path)
    return pages[first_kept_page(pages):]


def split_into_chapters(pages: list[Page]) -> list[list[Page]]:
    """Cut a whole-book page list at every page that opens a chapter. Pages before the first are dropped."""
    starts = [pos for pos, p in enumerate(pages) if any(b.role == "chapter-number" for b in p.blocks)]
    # A chapter opener is followed by at least a few pages. Anything closer is a stray big digit.
    starts = [s for i, s in enumerate(starts) if i == 0 or s - starts[i - 1] >= 4]
    return [pages[a:b] for a, b in zip(starts, starts[1:] + [len(pages)])]


def _columns(body: list[Block], width: float) -> list[tuple[float, float]]:
    """Left-to-right x ranges of the text columns the body blocks form (usually one)."""
    if not body:
        return [(0.0, width)]
    xs = sorted(set(round(b.x0) for b in body))
    groups: list[list[int]] = [[xs[0]]]
    for x in xs[1:]:
        if x - groups[-1][-1] > 0.12 * width:
            groups.append([x])
        else:
            groups[-1].append(x)
    cols = []
    for g in groups:
        members = [b for b in body if round(b.x0) in g]
        if len(members) >= 2 or len(groups) == 1:
            cols.append((min(b.x0 for b in members) - 6, max(b.x1 for b in members) + 6))
    cols.sort()
    # Columns that overlap are one column (an indented paragraph is not a new column).
    merged: list[tuple[float, float]] = []
    for left, right in cols:
        if merged and left < merged[-1][1] - 20:
            merged[-1] = (merged[-1][0], max(merged[-1][1], right))
        else:
            merged.append((left, right))
    return merged or [(0.0, width)]


def _reading_order(blocks: list[Block], width: float) -> list[Block]:
    """Each text column top to bottom, left column first, then the side notes."""
    body = [b for b in blocks if b.role in ("body", "table", "h2", "h3", "dropcap", "chapter-number")]
    cols = _columns(body, width)
    ordered: list[Block] = []
    side: list[Block] = []
    buckets: list[list[Block]] = [[] for _ in cols]
    for b in blocks:
        for k, (left, right) in enumerate(cols):
            if left <= b.centre_x <= right:
                buckets[k].append(b)
                break
        else:
            side.append(b)
    for bucket in buckets:
        ordered.extend(sorted(bucket, key=lambda b: (b.y0, b.x0)))
    ordered.extend(sorted(side, key=lambda b: (b.y0, b.x0)))
    return ordered


def title_page_position(pages: list[Page]) -> int:
    """Position in `pages` of the page that opens the chapter.

    Some 2007 files start with the previous chapter's last page, so this is not always 0.
    """
    for pos, p in enumerate(pages):
        if any(b.role == "chapter-number" for b in p.blocks):
            return pos
    return 0


def first_kept_page(pages: list[Page]) -> int:
    """Leading pages to skip: a stray last page of the previous chapter (only body text and
    activity headings), or a contents page bound into the first chapter file. A unit opener
    or a teacher's note before the chapter title is part of the chapter and is kept."""
    opener = title_page_position(pages)
    keep_from = opener
    for pos in range(opener - 1, -1, -1):
        p = pages[pos]
        heads = [b for b in p.blocks if b.role == "h2"]
        if heads and re.match(r"^contents$", heads[0].text.strip(), re.IGNORECASE):
            break  # a contents page: it and anything before it belong to the prelims
        if not heads:
            break  # body text only: the previous chapter's tail
        keep_from = pos
    return keep_from


def split_number_and_title(text: str) -> tuple[str | None, str | None]:
    """'4' -> ('4', None). '2 NEW KINGS' -> ('2', 'NEW KINGS'). 'TOWNS 6' -> ('6', 'TOWNS'). 'Chapter 4' -> ('4', None)."""
    m = CHAPTER_LABEL.match(text.strip())
    if m:
        return m.group(1), None
    m = re.match(r"^(\d{1,2})\s*(.*)$", text)
    if m:
        return m.group(1), (m.group(2).strip() or None)
    m = re.match(r"^(.*?)\s*(\d{1,2})$", text)
    if m:
        return m.group(2), (m.group(1).strip() or None)
    return None, None


def chapter_title(pages: list[Page]) -> tuple[str | None, str | None]:
    """(chapter number, title) from the oversized number and the heading beside it."""
    if not pages:
        return None, None
    pos = title_page_position(pages)
    number: str | None = None
    title: str | None = None
    for b in pages[pos].blocks:
        if b.role == "chapter-number":
            number, title = split_number_and_title(b.text)
            break
    if title is None:
        # Without a chapter number the title is the biggest heading on the first page that
        # has one, skipping a unit opener ("UNIT" / "ONE") bound in before the chapter.
        for page in pages[pos:pos + 4]:
            if any(TEACHERS_NOTE.match(b.text) for b in page.blocks):
                continue  # the unit's teacher's-note page carries the unit title, not the chapter's
            heads = sorted(
                (b for b in page.blocks if b.role == "h2" and not LABEL_HEADING.match(b.text.strip()) and not UNIT_WORD.match(b.text.strip()) and not DROPCAP_LINE.match(b.text)),
                key=lambda b: (-round(b.size), b.y0),
            )
            if heads:
                title = heads[0].text
                m = re.match(r"^(\d{1,2})\s+(.*)$", title)
                if m:
                    number = number or m.group(1)
                    title = m.group(2)
                break
    if title:
        title = re.sub(r"\s*\(\s*", " (", title)
        title = re.sub(r"\s*\)", ")", title)
        title = re.sub(r"(\d+)\s*(st|nd|rd|th)\b", r"\1\2", title)
    return number, title


def fix_page_numbers(pages: list[Page]) -> None:
    """Printed numbers must advance one per page. Use the commonest offset and fill the gaps."""
    offsets = Counter(p.printed_number - p.index for p in pages if p.printed_number is not None)
    if not offsets:
        return
    offset, votes = offsets.most_common(1)[0]
    if votes < 2 and len(pages) > 2:
        return
    for p in pages:
        p.printed_number = p.index + offset


def to_markdown(pages: list[Page], width: float = 600.0) -> str:
    lines: list[str] = []
    pending_body: str | None = None  # body paragraph that may continue past side blocks or a page break
    deferred: list[str] = []  # side blocks and page markers met while a paragraph was pending
    pending_dropcap: str | None = None
    first_heading_done = False  # the chapter title gets "#", wherever in the file it falls

    def emit(*items: str) -> None:
        target = deferred if pending_body is not None else lines
        target.extend(items)

    def flush() -> None:
        nonlocal pending_body
        if pending_body is not None:
            lines.append(pending_body)
            lines.append("")
            pending_body = None
        lines.extend(deferred)
        deferred.clear()

    for page in pages:
        where = f"{page.index + 1} of {page.source}" if page.source else f"{page.index + 1}"
        marker = f"<!-- page {page.printed_number} (pdf {where}) -->" if page.printed_number else f"<!-- pdf page {where} -->"
        emit(marker, "")
        for b in _reading_order(page.blocks, width):
            if b.role in ("footer", "decoration"):
                continue
            if b.role == "chapter-number":
                _, embedded_title = split_number_and_title(b.text)
                if embedded_title and not first_heading_done:
                    flush()
                    lines.extend((f"# {embedded_title}", ""))
                    first_heading_done = True
                continue
            if b.role == "dropcap":
                pending_dropcap = b.text
                continue
            if b.role == "body":
                text = b.text
                if pending_dropcap:
                    text = pending_dropcap + text
                    pending_dropcap = None
                if pending_body is not None and clean.continues(pending_body, text):
                    pending_body = clean.merge_paragraphs(pending_body, text)
                else:
                    flush()
                    pending_body = text
                continue
            if b.role == "h2":
                flush()
                if first_heading_done or LABEL_HEADING.match(b.text.strip()):
                    level = "##"
                else:
                    level = "#"
                    first_heading_done = True
                lines.extend((f"{level} {b.text}", ""))
                continue
            if b.role == "h3":
                # Box and activity headings often sit between a paragraph and its continuation
                # on the next page. They are written after the paragraph they interrupt.
                emit(f"### {b.text}", "")
                continue
            # Captions, notes, sources, tables: kept in place, without ending the paragraph.
            if clean.has_content(b.text):
                emit(f"> [{b.role}] {b.text}", "")
    flush()
    lines = _merge_split_asides(lines)
    lines = [ln for i, ln in enumerate(lines) if ln != "" or (i > 0 and lines[i - 1] != "")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


_ASIDE = re.compile(r"^> \[(\w+)\] (.*)$")


def _merge_split_asides(lines: list[str]) -> list[str]:
    """Join consecutive tagged blocks of the same role when one plainly continues the other.

    PyMuPDF often splits a table cell or a margin note into one block per line.
    """
    out: list[str] = []
    for line in lines:
        m = _ASIDE.match(line)
        if m and out:
            # Look back past the blank separator to the previous aside of the same role.
            k = len(out) - 1
            while k >= 0 and out[k] == "":
                k -= 1
            pm = _ASIDE.match(out[k]) if k >= 0 else None
            if pm and pm.group(1) == m.group(1) and clean.continues(pm.group(2), m.group(2)):
                out[k] = f"> [{m.group(1)}] {clean.merge_paragraphs(pm.group(2), m.group(2))}"
                continue
        out.append(line)
    return out


def extract_chapter(pdf_path: Path) -> tuple[str, dict]:
    """Markdown body and metadata for one chapter PDF."""
    pages, width = _read_all_pages(pdf_path)
    return _render(pages[first_kept_page(pages):], width)


def _is_unit_opener_page(page: Page) -> bool:
    """A page that carries nothing but "UNIT" and "THREE" in display type."""
    shown = [b for b in page.blocks if b.role != "footer"]
    return bool(shown) and all(b.role == "h2" and UNIT_OPENER.match(b.text.strip()) for b in shown)


def trailing_unit_opener(pages: list[Page]) -> int:
    """Position where a unit opener bound in at the END of a chapter file begins (the 2024-25
    Class 7 civics files end chapter 3 with Unit Three's opener and teacher's note, which the
    2023-24 files put at the start of chapter 4). len(pages) when there is none."""
    for pos in range(len(pages) - 1, 0, -1):
        rest = pages[pos + 1:]
        if _is_unit_opener_page(pages[pos]) and rest and all(any(TEACHERS_NOTE.match(b.text) for b in p.blocks) for p in rest):
            return pos
        if not any(TEACHERS_NOTE.match(b.text) for b in pages[pos].blocks):
            break
    return len(pages)


def extract_chapter_file(pdf_path: Path, carry: list[Page] | None = None) -> tuple[list[tuple[str, dict]], list[Page]]:
    """Every chapter in a per-chapter PDF, plus any trailing unit opener that belongs to the
    next file. Usually one chapter, but NCERT sometimes packs two chapters into one file (the
    2023-24 Class 7 civics ch08 holds chapters 7 and 8), so a file is cut at its chapter
    openers when they carry distinct chapter numbers. `carry` is the previous file's trailing
    opener, placed in front of this chapter."""
    pages, width = _read_all_pages(pdf_path)
    pages = pages[first_kept_page(pages):]
    cut = trailing_unit_opener(pages)
    trailing = pages[cut:]
    for p in trailing:
        p.source = pdf_path.name
    pages = list(carry or []) + pages[:cut]
    groups = split_into_chapters(pages)
    if len(groups) > 1:
        rendered = [_render(group, width) for group in groups]
        numbers = [meta["chapter_number"] for _, meta in rendered]
        if all(numbers) and len(set(numbers)) == len(numbers):
            return rendered, trailing
    return [_render(pages, width)], trailing


def extract_whole_book(pdf_path: Path) -> list[tuple[str, dict]]:
    """Markdown and metadata for every chapter found in a whole-book PDF."""
    pages, width = _read_all_pages(pdf_path)
    return [_render(group, width) for group in split_into_chapters(pages)]


def _render(pages: list[Page], width: float) -> tuple[str, dict]:
    number, title = chapter_title(pages)
    printed = [p.printed_number for p in pages if p.printed_number]
    meta = {
        "chapter_number": number,
        "title": title,
        "pdf_pages": len(pages),
        "printed_pages": f"{min(printed)}-{max(printed)}" if printed else None,
        "role_counts": dict(Counter(b.role for p in pages for b in p.blocks)),
    }
    return to_markdown(pages, width), meta


def body_text(markdown: str) -> str:
    """Only body paragraphs and headings, markers and tagged blocks removed. Used for fingerprints."""
    out = []
    for line in markdown.splitlines():
        if line.startswith("<!--") or line.startswith("> [") or line.startswith("---"):
            continue
        if line.strip():
            out.append(line.strip())
    return "\n".join(out)
