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
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from . import clean

HORIZONTAL = (1.0, 0.0)
CHAPTER_NUMBER = re.compile(r"^(\d{1,2})\b|\b(\d{1,2})$")
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
        if any(s["text"].strip() for s in spans):
            out.append(spans)
    return out


def read_blocks(page: pymupdf.Page) -> list[Block]:
    """Text blocks with rotated (watermark) lines removed and lines joined."""
    return blocks_from_dict(page.get_text("dict"))


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
        for spans in _dedupe_shadow_spans(lines):
            texts.append(_join_spans(spans))
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
    """The body text size of a document: the commonest size (by characters) among plain blocks."""
    sizes: Counter = Counter()
    for blocks in pages_blocks:
        for b in blocks:
            if not b.bold and 9.0 <= b.size <= 14.5 and len(b.text) > 60:
                sizes[b.size] += len(b.text)
    return sizes.most_common(1)[0][0] if sizes else DEFAULT_BODY_SIZE


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
        if b.y0 > FOOTER_BAND * height and len(b.text) <= 60 and (delta >= 1.4 or len(b.text) <= 4):
            b.role = "footer"
            m = re.match(r"^(\d{1,3})\b", b.text) or re.search(r"\b(\d{1,3})$", b.text)
            if m and printed is None:
                printed = int(m.group(1))
            continue
        if b.y1 < HEADER_BAND * height and len(b.text) <= 60 and delta >= 1.4:
            b.role = "footer"
            continue
        if b.size >= 2 * body_size and len(b.text) <= 2 and not b.text.isdigit():
            b.role = "dropcap"
            continue
        if b.max_size >= 2 * body_size and CHAPTER_NUMBER.search(b.text) and b.y0 < TITLE_BAND * height:
            b.role = "chapter-number"
            continue
        if b.size >= body_size + 2.5:
            b.role = "h2" if sum(ch.isalpha() for ch in b.text) >= 2 else "decoration"
            continue
        if b.bold and b.size >= body_size + 0.8:
            b.role = "h3"
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
        if delta <= 1.4:
            b.role = "body"  # body text, or the slightly smaller exercise questions
            continue
        b.role = "table"
    return printed


def _read_all_pages(pdf_path: Path) -> tuple[list[Page], float]:
    pages: list[Page] = []
    width = 600.0
    with pymupdf.open(pdf_path) as doc:
        raw = []
        for i, page in enumerate(doc):
            if i == 0:
                width = page.rect.width
            raw.append((i, read_blocks(page), page.rect.width, page.rect.height))
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
    return pages[title_page_position(pages):]


def split_into_chapters(pages: list[Page]) -> list[list[Page]]:
    """Cut a whole-book page list at every page that opens a chapter. Pages before the first are dropped."""
    starts = [pos for pos, p in enumerate(pages) if any(b.role == "chapter-number" for b in p.blocks)]
    # A chapter opener is followed by at least a few pages. Anything closer is a stray big digit.
    starts = [s for i, s in enumerate(starts) if i == 0 or s - starts[i - 1] >= 4]
    return [pages[a:b] for a, b in zip(starts, starts[1:] + [len(pages)])]


def _reading_order(blocks: list[Block], width: float) -> list[Block]:
    """Body column first (top to bottom), then side column, then the rest."""
    body = [b for b in blocks if b.role in ("body", "table", "h2", "h3", "dropcap", "chapter-number")]
    if body:
        col_left = min(b.x0 for b in body) - 6
        col_right = max(b.x1 for b in body) + 6
    else:
        col_left, col_right = 0.0, width
    main = sorted((b for b in blocks if col_left <= b.centre_x <= col_right), key=lambda b: (b.y0, b.x0))
    side = sorted((b for b in blocks if not (col_left <= b.centre_x <= col_right)), key=lambda b: (b.y0, b.x0))
    return main + side


def title_page_position(pages: list[Page]) -> int:
    """Position in `pages` of the page that opens the chapter.

    Some 2007 files start with the previous chapter's last page, so this is not always 0.
    """
    for pos, p in enumerate(pages):
        if any(b.role == "chapter-number" for b in p.blocks):
            return pos
    return 0


def split_number_and_title(text: str) -> tuple[str | None, str | None]:
    """'4' -> ('4', None). '2 NEW KINGS' -> ('2', 'NEW KINGS'). 'TOWNS 6' -> ('6', 'TOWNS')."""
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
    page = pages[title_page_position(pages)]
    number: str | None = None
    title: str | None = None
    for b in page.blocks:
        if b.role == "chapter-number":
            number, title = split_number_and_title(b.text)
            break
    if title is None:
        heads = sorted((b for b in page.blocks if b.role == "h2"), key=lambda b: b.y0)
        if heads:
            title = heads[0].text
            m = re.match(r"^(\d{1,2})\s+(.*)$", title)
            if m:
                number = number or m.group(1)
                title = m.group(2)
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
        marker = (
            f"<!-- page {page.printed_number} (pdf {page.index + 1}) -->"
            if page.printed_number
            else f"<!-- pdf page {page.index + 1} -->"
        )
        emit(marker, "")
        first_heading_done = page.index != pages[0].index
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
                level = "#" if not first_heading_done else "##"
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
    return _render(pages[title_page_position(pages):], width)


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
