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
import unicodedata
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
# Some re-exported files (the 2024-25 Class 7 civics) carry fonts whose Unicode map lands the
# typographic quotes and dashes on nearby Latin-1 or Latin Extended-A code points.
QUOTE_SHIFT = str.maketrans({"¶": "‘", "·": "’", "´": "“", "µ": "”", "²": "–", "³": "—", "ī": "‘", "Ĭ": "’", "Į": "“", "į": "”", "ĩ": "–", "ŏ": "’", "ő": "“", "«": "…", "§": "‘", "Œ": "”"})
_SHIFTED_APOSTROPHE = re.compile(r"[·Ĭ]s\b")  # "women·s", "RamabaiĬs"
UNREADABLE = "[unreadable]"  # text set in a font without a Unicode map comes out as blanks
# Headings that label a unit or chapter rather than name it. Not titles, not evidence of a chapter opener.
LABEL_HEADING = re.compile(r"^(unit\s+\w+|chapter\s*\d*|contents|notes|teacher[’']s note)[\s:.-]*$", re.IGNORECASE)
DROPCAP_LINE = re.compile(r"^[A-Z] [a-z]")  # a drop cap glued to its line ("Y crafts and production") is not a heading
TEACHERS_NOTE = re.compile(r"^teacher[’']s note", re.IGNORECASE)
UNIT_OPENER = re.compile(r"^(unit(\s+\w+)?|one|two|three|four|five|six|seven|eight|nine|ten)$", re.IGNORECASE)
UNIT_WORD = re.compile(r"^(unit|one|two|three|four|five|six|seven|eight|nine|ten)$", re.IGNORECASE)  # unit openers set one word per line
ICON_FONT = re.compile(r"webdings|wingdings|dingbat|zapfdingbats", re.IGNORECASE)
OPAQUE_FONT = re.compile(r"^TT[0-9A-F]{3,}T\d\d$")  # a font embedded under a generic name ("TT3DBT00")
DATED_LABEL = re.compile(r"\b1\d{3}\b")  # a label with a year in it ("Jahangir 1605-1627")
CHAPTER_LABEL = re.compile(r"^chapter\s+(\d{1,2})$", re.IGNORECASE)
SDG_LABEL = re.compile(r"^Sustainable Development Goal", re.IGNORECASE)  # the UN goal badge printed in the margin since 2019
ACTIVITY_HEADING = re.compile(r"Let[’']s (recall|discuss|do|understand|imagine|find out|write)|Activity|Imagine|Elsewhere", re.IGNORECASE)  # box labels
# Map axis ticks ("60E", "70°E", "10N"): the 2025 Exploring Society maps draw them as outlines,
# and a tick read back can land on the caption line printed level with the map's bottom edge.
AXIS_TICKS = re.compile(r"(?:\d{1,3}\s?°?\s?[NESW]\s*)+")
LEADING_TICKS = re.compile(r"^(?:\d{1,3}\s?°?\s?[NESW]\s+)+(?=Fig\.\s)")
NUMBER_LABELS = re.compile(r"\d{1,2}(?: \d{1,2})*")
FOOTER_BAND = 0.86  # fraction of page height below which small text is a footer
HEADER_BAND = 0.06
SLUG_BAND = 0.975  # below this, under the print-run label, nothing is part of the printed page
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
    ocr: bool = False  # a rasterised page inside a text PDF, read with tesseract
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
    kept_spans: dict[tuple[str, tuple], dict] = {}
    copies: Counter = Counter()  # identical spans dropped on top of a kept one
    shadows: list[tuple[str, tuple]] = []  # duplicates dropped so far, by text and box
    out: list[list[dict]] = []
    for ln in lines:
        spans = []
        for s in ln["spans"]:
            text = s["text"].strip()
            under = next(((t, tuple(bb)) for t, bb in kept if text == t and _overlap_ratio(s["bbox"], bb) >= 0.7), None) if text else None
            if under is not None:
                copies[under] += 1
                shadows.append((text, s["bbox"]))
                continue
            # The last word of a line drawn again on top of itself ("...a French cartographer"
            # then "cartographer" three times at the same place).
            # The 2016 civics files fake their bold by drawing a line again with the first glyph
            # left off ("prosecution " then "rosecution " three times, ending at the same x), so
            # a copy that ends where the kept span ends may start inside its first word.
            if text and any(
                t.endswith(text) and len(t) > len(text) and (not t[-len(text) - 1].isalnum() or abs(s["bbox"][2] - bb[2]) <= 1.5) and _overlap_ratio(s["bbox"], bb) >= 0.7
                for t, bb in kept
            ):
                shadows.append((text, s["bbox"]))
                continue
            # A span that begins with that same shadowed word and continues ("cartographer. The"):
            # keep only what comes after it.
            for t, bb in shadows:
                if text.startswith(t) and len(text) > len(t) and not text[len(t)].isalnum() and abs(s["bbox"][0] - bb[0]) <= 2.5 and _overlap_ratio(s["bbox"], bb) >= 0.7:
                    cut = s["text"].index(t) + len(t)
                    s = dict(s, text=s["text"][cut:], bbox=(bb[2], s["bbox"][1], s["bbox"][2], s["bbox"][3]))
                    text = s["text"].strip()
                    break
            if text:
                # A clipped copy drawn first ("Bhopal Gas T" four times, then the whole heading):
                # a kept span that is a prefix of this one at the same place is the clipped copy.
                for t, bb in list(kept):
                    if text.startswith(t) and len(text) > len(t) and _overlap_ratio(s["bbox"], bb) >= 0.7:
                        kept.remove((t, bb))
                        for earlier in out:
                            earlier[:] = [e for e in earlier if not (e["text"].strip() == t and e["bbox"] == bb)]
                        spans = [e for e in spans if not (e["text"].strip() == t and e["bbox"] == bb)]
                kept.append((text, s["bbox"]))
                kept_spans[(text, tuple(s["bbox"]))] = s
            spans.append(s)
        if any(s["text"].strip() for s in spans) or any(len(s["text"]) >= 3 and s["bbox"][2] - s["bbox"][0] > 20 for s in spans):
            out.append(spans)
    # A span drawn three or more times on top of itself is the 2007 files' bold face (the
    # emperor labels of chapter 4, "Jahangir 1605-1627" five times). It is marked, not flagged
    # bold: the mark is read only by the dated-label rules, so the page's columns, which skip
    # bold blocks, are not disturbed by it.
    for key, n in copies.items():
        if n >= 2 and key in kept_spans:
            kept_spans[key]["overprint"] = n
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
            # Fragments of one word overlap where a ligature was drawn ("can be prot" and
            # "ofitably"), so an overlap of up to most of a line height still joins.
            if -0.8 * current.height <= g.x0 - current.x1 <= max(9.0, 0.8 * current.height):
                current |= g
            else:
                runs.append(current)
                current = pymupdf.Rect(g)
        runs.append(current)
    # A run can be as small as the "s." that finishes a word whose stem is in the text layer.
    return [r for r in runs if r.width >= 5 and 6 <= r.height <= 30]


def read_blocks(page: pymupdf.Page, read_outlined: OutlinedReader | None = None, font_fixes: dict[str, dict] | None = None) -> list[Block]:
    """Text blocks with rotated (watermark) lines removed and lines joined."""
    textpage = page.get_text("rawdict")
    for raw in textpage["blocks"]:
        for ln in raw.get("lines", []):
            _text_from_chars(ln)
    if read_outlined is not None:
        _fill_outlined_words(page, textpage, outlined_word_rects(page), read_outlined)
    return blocks_from_dict(textpage, font_fixes)


_SPACED_TOKEN = re.compile(r"[^\W\d_]|[.,;:’'-]")  # one letter, or punctuation that sits inside a letter-spaced run ("M r . T e l a n g")


def _text_from_chars(line: dict) -> None:
    """Give each span of a rawdict line its text, closing up letter-spaced words.

    Narrow justified boxes are sometimes set with a space character after every letter
    ("e d u c a t i o n w h i c h", "R e m e m b e r t h a t"). Inside a word the space glyph
    touches the letters on both sides. Between words there is a visible gap before or
    after it, so that space is kept. Only runs of three or more one-character tokens are
    touched (or a line made of nothing else, such as "t o"), so ordinary text with a
    one-letter word ("a", "I") is left alone.
    """
    chars = [c for sp in line["spans"] for c in sp["chars"]]
    drop: set[int] = set()
    # Tokens: (first index, last index) of each run of non-space characters.
    tokens: list[tuple[int, int]] = []
    i = 0
    while i < len(chars):
        if chars[i]["c"].isspace():
            i += 1
            continue
        j = i
        while j + 1 < len(chars) and not chars[j + 1]["c"].isspace():
            j += 1
        tokens.append((i, j))
        i = j + 1
    single = [a == b and bool(_SPACED_TOKEN.fullmatch(chars[a]["c"])) for a, b in tokens]
    k = 0
    while k < len(tokens):
        if not single[k]:
            k += 1
            continue
        m = k
        # A run continues while the next token is one character too. Several spaces between
        # two of them ("I N   T H I S") are a word space inside the same run.
        while m + 1 < len(tokens) and single[m + 1]:
            m += 1
        letters = sum(chars[tokens[t][0]]["c"].isalpha() for t in range(k, m + 1))
        whole_line = k == 0 and m == len(tokens) - 1
        # Counting letters, not tokens, leaves runs of punctuation ("; ; ;", ". . .") alone.
        if letters >= 3 or (whole_line and letters >= 2):
            for t in range(k, m):
                if tokens[t + 1][0] - tokens[t][1] != 2:
                    continue
                a, sp, b = chars[tokens[t][1]], chars[tokens[t][1] + 1], chars[tokens[t + 1][0]]
                if sp["bbox"][0] - a["bbox"][2] <= 0.5 and b["bbox"][0] - sp["bbox"][2] <= 0.5:
                    drop.add(tokens[t][1] + 1)
        k = m + 1
    drop |= _phantom_spaces(chars, [sp.get("size", 0.0) for sp in line["spans"] for _ in sp["chars"]])
    pos = 0
    for sp in line["spans"]:
        n = len(sp["chars"])
        sp["text"] = "".join(c["c"] for idx, c in enumerate(sp.pop("chars"), start=pos) if idx not in drop)
        pos += n


def _letterlike(ch: str) -> bool:
    return ch.isalpha() or unicodedata.category(ch).startswith("M")


def _phantom_spaces(chars: list[dict], sizes: list[float] | None = None) -> set[int]:
    """Indices of space characters inside a word that the page does not show.

    The 2025 Exploring Society files have three kinds. A space with no advance at all, the
    next letter starting where the space starts ("The g overnment", "C onstitution"). A
    space that carries the advance of the letter before it, which the text layer gives no
    width ("Kaṇṇ agi", "Pāṭ aliputra", where the last "ṇ" or "ṭ" is zero wide and the space
    is as wide as the letter). And a thin space between two letters ("cold s torage",
    "Dis tributors"). A real word space always leaves a gap, so the next letter starts past
    the space's left edge. A ligature also leaves a zero-wide letter ("off" is "of" and an
    empty "f"), but the space after it is an ordinary one, so the stand-in is told by its
    width: wider than a word space ever is, with the next letter abutting it."""
    out: set[int] = set()
    for i in range(1, len(chars) - 1):
        sp, prev, nxt = chars[i], chars[i - 1], chars[i + 1]
        if not sp["c"].isspace() or not _letterlike(prev["c"]) or not nxt["c"].isalpha():
            continue
        size = sizes[i] if sizes else 0.0
        width = sp["bbox"][2] - sp["bbox"][0]
        if sp["c"] in "\u2009\u200a":
            out.add(i)
        elif sp["c"] == " " and nxt["bbox"][0] - sp["bbox"][0] <= 0.1:
            out.add(i)  # no advance at all
        elif sp["c"] == " " and prev["bbox"][2] - prev["bbox"][0] <= 0.05 and size and width >= 0.4 * size and abs(nxt["bbox"][0] - sp["bbox"][2]) <= 0.1:
            out.add(i)  # the advance of the zero-wide letter before it
    return out


def shifted_quote_fonts(doc: pymupdf.Document) -> dict[str, dict]:
    """Fonts to repair in a document whose quotes come out as "women·s" or "RamabaiĬs":
    font name -> translation table. The symptom is judged over the whole document (a
    chapter has a few dozen apostrophes spread over many fonts). Fonts that do produce a
    real apostrophe are left alone."""
    texts: dict[str, list[str]] = {}
    for page in doc:
        for raw in page.get_text("dict")["blocks"]:
            for ln in raw.get("lines", []):
                for sp in ln["spans"]:
                    texts.setdefault(sp["font"], []).append(sp["text"])
    if len(_SHIFTED_APOSTROPHE.findall(" ".join(t for parts in texts.values() for t in parts))) < 2:
        return {}
    return {font: QUOTE_SHIFT for font, parts in texts.items() if "’" not in " ".join(parts)}


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
        # The text line this run belongs to: nearest vertical centre among lines it touches
        # horizontally. A word space is 4 to 6 pt, so a run that ends a little short of its line
        # ("mansabdars." then "themselves served ...") must still reach it.
        tol = max(8.0, 0.5 * r.height)
        best = None
        for raw, ln in all_lines:
            lx0, ly0, lx1, ly1 = ln["bbox"]
            if r.x1 < lx0 - tol or r.x0 > lx1 + tol or r.height > 1.4 * (ly1 - ly0):
                continue
            dist = abs((ly0 + ly1) / 2 - cy)
            if dist <= 0.4 * (ly1 - ly0) and (best is None or dist < best[0]):
                best = (dist, raw, ln)
        if best is not None:
            _, host, ln = best
            spans = [sp for sp in ln["spans"] if sp["text"].strip()]
            # The line can be cut into fragments on either side of the run ('. But unlike ' and
            # ', most ' around "muqtis"), so the neighbours are looked for on the whole baseline.
            lcy, lh = (ln["bbox"][1] + ln["bbox"][3]) / 2, ln["bbox"][3] - ln["bbox"][1]
            baseline = sorted(
                (sp for other in host["lines"] if abs((other["bbox"][1] + other["bbox"][3]) / 2 - lcy) <= 0.4 * lh for sp in other["spans"] if sp["text"].strip()),
                key=lambda sp: sp["bbox"][0],
            )
            # Overlapping real text means decoration behind it, or invisible text already there.
            # A span's box includes its trailing space, so a sliver of overlap does not count.
            if any(min(sp["bbox"][2], r.x1) - max(sp["bbox"][0], r.x0) > max(2.0, 0.3 * r.width) for sp in baseline):
                continue
            word = read_outlined(page, r)
            if not word:
                continue
            before = "".join(sp["text"] for sp in baseline if sp["bbox"][2] <= r.x0 + 2)
            after = "".join(sp["text"] for sp in baseline if sp["bbox"][0] >= r.x1 - 2)
            if not after.strip():
                # The run ends its line: what follows is the first text of the next line.
                below = [o for o in host["lines"] if o["bbox"][1] >= ln["bbox"][3] - 2 and any(sp["text"].strip() for sp in o["spans"])]
                nxt_line = min(below, key=lambda o: (o["bbox"][1], o["bbox"][0]), default=None)
                after_next = "".join(sp["text"] for sp in nxt_line["spans"]) if nxt_line else ""
            else:
                after_next = after
            word = _tidy_ocr_word(word, before, after, after_next)
            if not word:
                continue
            tail = "" if after.lstrip()[:1] in tuple(",.;:!?)’”") and after.lstrip() else " "
            # A fragment that finishes the word before it ("empire" + "s.") abuts that span.
            prev_end = max((sp["bbox"][2] for sp in baseline if sp["bbox"][2] <= r.x0 + 2), default=None)
            lead = "" if prev_end is not None and r.x0 - prev_end <= 1.5 and not before.endswith(" ") else " "
            if lead == "":
                # The crop around the fragment takes in the tail of the word it finishes, so the
                # reading can repeat it ("empire" then "es."): drop the repeated letters.
                stem = before.rstrip().split()[-1] if before.strip() else ""
                for n in (2, 1):
                    if len(stem) >= n and word.lower().startswith(stem[-n:].lower()) and len(word) > n:
                        word = word[n:]
                        break
            ln["spans"].append({"text": f"{lead}{word}{tail}", "bbox": tuple(r), "size": spans[0]["size"], "font": "OUTLINED", "flags": 0})
            ln["spans"].sort(key=lambda sp: sp["bbox"][0])
            continue
        # No text line there: a whole outlined line. Attach it to the block it sits in or next to.
        # The outline detector clips the first and last letters of small labels ("rader sells
        # the", "Ginning mil"), and a standalone run has no text-layer neighbour to bleed in,
        # so it is read from a crop widened by a few points on each side.
        word = read_outlined(page, pymupdf.Rect(r.x0 - 4, r.y0, r.x1 + 4, r.y1) & page.rect if page is not None else r)
        if not word:
            continue
        word = _tidy_ocr_line(word)
        host = None
        for raw in text_blocks:
            bx0, by0, bx1, by1 = raw["bbox"]
            if _is_big_glyph_block(raw, r.height):
                continue  # a drop cap beside the line: hosting the line in it would make the line a heading ("R extremely difficult task")
            # Runs of one line are separated by word spaces, so a block made of runs is reached
            # a little sideways. A text block is not: a margin box of outlined lines sits a
            # few points from the paragraph beside it and must stay a block of its own.
            gap = r.height * 1.5 if _outlined_only(raw) else 4.0
            if r.x0 < bx1 + gap and r.x1 > bx0 - gap and by0 - r.height * 1.6 <= cy <= by1 + r.height * 1.6:
                host = raw
                break
        size = max((sp["size"] for ln in host["lines"] for sp in ln["spans"]), default=r.height * 0.9) if host else r.height * 0.9
        span = {"text": word, "bbox": tuple(r), "size": size, "font": "OUTLINED", "flags": 0}
        # Several runs on one baseline ("and the nature of their investigation.", "Last year,",
        # "for") are one line: joining them in x order keeps a line-end word in its place
        # instead of sorting it by its slightly different top edge.
        same_line = next((ln for ln in (host["lines"] if host else []) if ln["spans"] and ln["spans"][0]["font"] == "OUTLINED" and abs((ln["bbox"][1] + ln["bbox"][3]) / 2 - cy) <= 0.5 * max(r.height, ln["bbox"][3] - ln["bbox"][1])), None)
        if same_line is not None:
            same_line["spans"].append(dict(span, text=f" {word}"))
            same_line["spans"].sort(key=lambda sp: sp["bbox"][0])
            same_line["bbox"] = tuple(pymupdf.Rect(same_line["bbox"]) | r)
            host["bbox"] = tuple(pymupdf.Rect(host["bbox"]) | r)
            continue
        line = {"dir": (1.0, 0.0), "bbox": tuple(r), "spans": [span]}
        if host:
            host["lines"].append(line)
            host["lines"].sort(key=lambda ln: round((ln["bbox"][1] + ln["bbox"][3]) / 2))
            host["bbox"] = tuple(pymupdf.Rect(host["bbox"]) | r)
        else:
            textpage["blocks"].append({"type": 0, "bbox": tuple(r), "lines": [line]})
            text_blocks.append(textpage["blocks"][-1])


_OPENING_QUOTES = "‘“"
_CLOSING_QUOTES = "’”"


def _tidy_ocr_word(word: str, before: str, after: str, following: str) -> str:
    """Clean an OCR reading of an outlined run against the text around it on the page.

    `before` and `after` are the text on the same baseline to the left and right of the run,
    `following` is `after`, or the first text of the next line when the run ends its line.
    """
    word = word.strip()
    if word.startswith("- "):
        word = word[2:]  # a rule or hyphen drawn before the word ("their - jagirs")
    nxt = after.lstrip()
    if nxt and word and word[-1] in ",.;:" and nxt.startswith(word[-1]):
        word = word[:-1]  # the text layer keeps the punctuation as its own span
    if word.endswith(".") and not word.endswith("..") and following.lstrip()[:1].islower():
        word = word[:-1]  # single-word OCR adds a full stop that is not there ("mansabdars. did not")
    # Quotes that tesseract sees in the slant of an italic word ("‘Mansabdars", "‘ur"). A real
    # one is closed later in the sentence, or opened earlier on the line.
    if word[:1] in _OPENING_QUOTES:
        rest = re.split(r"(?<=[.!?])\s", after, maxsplit=1)[0]
        if not any(q in word[1:] + rest for q in _CLOSING_QUOTES + "'\""):
            word = word[1:]
    if word[-1:] in _CLOSING_QUOTES and not word[:-1].endswith(("s", "S")):
        if not any(q in word[:-1] + before for q in _OPENING_QUOTES):
            word = word[:-1]
    return word.strip()


def _outlined_only(raw: dict) -> bool:
    spans = [sp for ln in raw["lines"] for sp in ln["spans"] if sp["text"].strip()]
    return bool(spans) and all(sp["font"] == "OUTLINED" for sp in spans)


def _tidy_ocr_line(text: str) -> str:
    """Drop quotes an OCR engine saw in the slant of italics on a whole outlined line: an
    opening quote with no closing one after it, a closing quote with no opening one before
    it (a closing quote after "s" may be a plural possessive and stays)."""
    out = []
    for i, ch in enumerate(text):
        if ch in _OPENING_QUOTES and not any(q in text[i + 1:] for q in _CLOSING_QUOTES):
            continue
        if ch in _CLOSING_QUOTES and not any(q in text[:i] for q in _OPENING_QUOTES) and not text[:i].endswith(("s", "S")):
            continue
        out.append(ch)
    return "".join(out).replace("  ", " ").strip()


def _is_big_glyph_block(raw: dict, line_height: float) -> bool:
    """A block holding one or two oversized letters and nothing else (a drop cap)."""
    spans = [sp for ln in raw["lines"] for sp in ln["spans"] if sp["text"].strip()]
    text = "".join(sp["text"].strip() for sp in spans)
    return 0 < len(text) <= 2 and all(sp["size"] >= 2 * line_height for sp in spans)


def _split_side_lines(raw: dict) -> list[dict]:
    """Split off lines set smaller than the rest of the block and lying wholly beside it.

    PyMuPDF sometimes puts a margin caption into the body block whose last line it shares a
    baseline with ("He also established a close" and "Fig. 8 - Tipu Sultan" in the 2019 Our
    Pasts III), and the caption then lands inside the sentence."""
    lines = [ln for ln in raw.get("lines", []) if any(sp["text"].strip() for sp in ln["spans"])]
    if len(lines) < 2:
        return [raw]
    def size(ln: dict) -> float:
        return max(sp["size"] for sp in ln["spans"] if sp["text"].strip())
    weight: Counter = Counter()
    for ln in lines:
        weight[round(size(ln), 1)] += sum(len(sp["text"].strip()) for sp in ln["spans"])
    dominant = weight.most_common(1)[0][0]
    main = [ln for ln in lines if abs(size(ln) - dominant) < 1.0]
    left, right = min(ln["bbox"][0] for ln in main), max(ln["bbox"][2] for ln in main)
    side = [ln for ln in lines if size(ln) <= dominant - 1.4 and (ln["bbox"][2] < left - 3 or ln["bbox"][0] > right + 3)]
    if not side:
        return [raw]
    rest = [ln for ln in raw["lines"] if not any(ln is sd for sd in side)]
    def box(group: list[dict]) -> tuple:
        r = pymupdf.Rect(group[0]["bbox"])
        for ln in group[1:]:
            r |= pymupdf.Rect(ln["bbox"])
        return tuple(r)
    return [dict(raw, lines=rest, bbox=box(rest)), dict(raw, lines=side, bbox=box(side))]


def _split_caption_pair(raw: dict) -> list[dict]:
    """Split a one-line block holding the first lines of two captions set side by side
    ("Fig. 1.13. Multi-cropping in Uttar Pradesh" and, after a wide gap, "Fig. 1.14. Rural
    women working in a" in Exploring Society). PyMuPDF puts them in one line, and the two
    captions then read as one."""
    lines = [ln for ln in raw.get("lines", []) if any(sp["text"].strip() for sp in ln["spans"])]
    if not lines:
        return [raw]
    # The two captions can come as one line or as two lines on one baseline.
    centre = lambda ln: (ln["bbox"][1] + ln["bbox"][3]) / 2  # noqa: E731
    if any(abs(centre(ln) - centre(lines[0])) > 2 for ln in lines):
        return [raw]
    every = sorted((sp for ln in lines for sp in ln["spans"]), key=lambda sp: sp["bbox"][0])
    spans = [sp for sp in every if sp["text"].strip()]
    for k in range(1, len(spans)):
        gap = spans[k]["bbox"][0] - spans[k - 1]["bbox"][2]
        if re.match(r"^Fig\.\s", spans[k]["text"].strip()) and gap >= 1.5 * spans[k]["size"]:
            parts = []
            # Space spans are kept, or the words they separate run together.
            cut = spans[k]["bbox"][0]
            left = [sp for sp in every if sp["bbox"][0] < cut]
            right = [sp for sp in every if sp["bbox"][0] >= cut]
            for group in (left, right):
                box = tuple(pymupdf.Rect(group[0]["bbox"]) | pymupdf.Rect(group[-1]["bbox"]))
                parts.append(dict(raw, bbox=box, lines=[dict(lines[0], bbox=box, spans=group)]))
            return parts
    return [raw]


def blocks_from_dict(textpage: dict, font_fixes: dict[str, dict] | None = None) -> list[Block]:
    out: list[Block] = []
    for raw in [half for raw in textpage["blocks"] if raw["type"] == 0 for part in _split_side_lines(raw) for half in _split_caption_pair(part)]:
        lines = [ln for ln in raw["lines"] if tuple(round(v, 1) for v in ln["dir"]) == HORIZONTAL]
        if not lines:
            continue
        sizes: Counter = Counter()
        fonts: Counter = Counter()
        flags: Counter = Counter()
        texts: list[str] = []
        line_bold: list[bool] = []  # every span on the line is bold
        line_overprint: list[bool] = []  # every span on the line was drawn several times over itself
        line_faces: list[tuple[set, float]] = []  # fonts and largest size of each line
        line_text_x: list[float] = []  # where each line's text starts, after any bullet
        line_boxes: list[tuple] = []
        max_size = 0.0
        for ln in lines:
            for sp in ln["spans"]:
                if _is_bullet_span(sp):
                    sp.update(text=BULLET, font="BULLET", flags=0)
                elif _is_icon_glyph(sp):
                    sp["text"] = ""
            # Icon fonts carry activity glyphs ("Q" in Webdings is a question-mark bubble), not words.
            ln["spans"] = [sp for sp in ln["spans"] if not ICON_FONT.search(sp["font"])]
            for sp in ln["spans"]:
                sp["text"] = decode_symbol_font(sp["text"])
                if font_fixes and sp["font"] in font_fixes:
                    sp["text"] = sp["text"].translate(font_fixes[sp["font"]])
        deduped = _dedupe_shadow_spans(lines)
        for spans in deduped:
            joined = _join_spans(spans)
            if not joined.strip() and any(len(sp["text"]) >= 3 and sp["bbox"][2] - sp["bbox"][0] > 20 for sp in spans):
                joined = UNREADABLE  # glyphs are drawn but the font maps them to nothing
                for sp in spans:
                    sizes[round(sp["size"], 1)] += 10
                    fonts[sp["font"]] += 10
                    flags[_span_flags(sp)] += 10
            texts.append(joined)
            inked = [sp for sp in spans if sp["text"].strip()]
            line_bold.append(bool(inked) and all(_span_flags(sp)[0] for sp in inked))
            line_overprint.append(bool(inked) and all(sp.get("overprint", 0) >= 2 for sp in inked))
            line_faces.append(({sp["font"] for sp in inked}, max((sp["size"] for sp in inked), default=0.0)))
            line_text_x.append(next((sp["bbox"][0] for sp in inked if sp["text"].strip() != BULLET), spans[0]["bbox"][0] if spans else raw["bbox"][0]))
            line_boxes.append(tuple(pymupdf.Rect(spans[0]["bbox"]) | pymupdf.Rect(spans[-1]["bbox"])) if spans else raw["bbox"])
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
        if len(text) <= 60 and line_overprint and all(line_overprint):
            bold = True  # a short block drawn several times over itself: a 2007 heading or label
        x0, y0, x1, y1 = raw["bbox"]
        items = _bullet_items(texts, line_boxes, line_text_x)
        if items:
            # One block per list item, so that the items stay separate paragraphs.
            for item_lines, (ix0, iy0, ix1, iy1), is_item in items:
                item = clean.join_lines(item_lines)
                if item and clean.has_content(item):
                    out.append(Block(ix0, iy0, ix1, iy1, font, size, bold, italic, f"- {item}" if is_item else item, max_size))
            continue
        k = 0
        while k < min(2, len(deduped) - 1) and line_overprint[k]:
            k += 1
        if k:
            # A dated label drawn several times over itself (the 2007 files' bold), on one line
            # ("Shah Jahan 1627-1658") or two ("AKBAR" over "1556-1605"), with its paragraph on
            # the lines after it or beside it. The label becomes the heading of that paragraph.
            label = " ".join(t.strip() for t in texts[:k])
            rest_texts = texts[k:]
            if not DATED_LABEL.search(label) and rest_texts:
                m = re.match(r"^(\d{4}(?:-\d{4})?(?:, \d{4}-\d{4})?)\s+(\S.*)$", rest_texts[0].strip())
                if m:
                    label, rest_texts = f"{label} {m.group(1)}", [m.group(2)] + rest_texts[1:]
            if DATED_LABEL.search(label) and len(label) <= 40 and len(label.split()) <= 6 and not re.search(r"[.?!:;,]$", label) and len(" ".join(rest_texts)) >= 80:
                box = pymupdf.Rect(line_boxes[0])
                for i in range(1, k):
                    box |= pymupdf.Rect(line_boxes[i])
                out.append(Block(box.x0, box.y0, box.x1, box.y1, font, size, True, italic, label, max_size))
                rest = clean.join_lines(rest_texts)
                if rest and clean.has_content(rest):
                    out.append(Block(x0, line_boxes[k][1], x1, y1, font, size, False, italic, rest, max_size))
                continue
        lead, rest_spans = _bold_lead(deduped[0]) if len(deduped) >= 2 else ([], [])
        if lead:
            # A bold label opening the first line of a plain paragraph ("Jahangir 1605-1627
            # Military campaigns started by Akbar continued."): the label is written as its own
            # block, so it classifies as the heading of that paragraph.
            r = pymupdf.Rect(lead[0]["bbox"]) | pymupdf.Rect(lead[-1]["bbox"])
            out.append(Block(r.x0, r.y0, r.x1, r.y1, font, size, True, italic, _join_spans(lead).strip(), max_size))
            texts[0] = _join_spans(rest_spans).strip()
            rest = clean.join_lines(texts)
            if rest and clean.has_content(rest):
                out.append(Block(x0, y0, x1, y1, font, size, False, italic, rest, max_size))
            continue
        if _run_in_heading(texts, line_bold, line_faces, line_overprint):
            # A sub-heading set as the bold first line of its paragraph (2023-24 Our Pasts III).
            # Written as its own block so it classifies as a heading, as it does in other printings.
            hx0, hy0, hx1, hy1 = line_boxes[0]
            head_spans = [sp for sp in _dedupe_shadow_spans(lines[:1])][0]
            head_size = max(sp["size"] for sp in head_spans) if head_spans else size
            out.append(Block(hx0, hy0, hx1, hy1, font, round(head_size, 1), True, italic, texts[0].strip(), head_size))
            rest = clean.join_lines(texts[1:])
            if rest and clean.has_content(rest):
                out.append(Block(x0, line_boxes[1][1], x1, y1, font, size, bold, italic, rest, max_size))
            continue
        out.append(Block(x0, y0, x1, y1, font, size, bold, italic, text, max_size))
    return out


BULLET = "\u2022"
# Square list bullets as the text layer has them: "\x84" and U+F0A2 in Wingdings 2 (2014 and
# 2023 Our Pasts III), and the same U+F0A2 decoded to "¢" by a re-embedded font (2019 to 2022).
_BULLET_GLYPHS = {"\x84", "\uf0a2", "\uf0a7", "\uf06e", "¢", "▪", "■"}


def _is_icon_glyph(span: dict) -> bool:
    """The arrow before an "Activity" box label (Our Pasts III): a lone 20 pt glyph that the
    text layer gives as a control code ("\\x02" in 2014, "\\x86" in 2020) or, decoded through
    Windows-1252, as a dagger (2019)."""
    text = decode_symbol_font(span["text"]).strip()
    return len(text) == 1 and (unicodedata.category(text).startswith("C") or (text == "†" and span["size"] >= 16))


def _is_bullet_span(span: dict) -> bool:
    """A lone small list-bullet glyph. Size keeps a real cent sign or a big icon out."""
    text = span["text"].strip()
    return text == BULLET or (text in _BULLET_GLYPHS and span["size"] <= 9)


def _bullet_items(texts: list[str], boxes: list[tuple], text_x: list[float] | None = None) -> list[tuple[list[str], tuple, bool]]:
    """Split a block's lines at list bullets: [(lines, box, is_item)], or [] when there are none.

    A bullet is either its own line beside the first line of the item ("¢" then "The British
    conquest of territories, ...") or the first character of that line. Without the split the
    items join into one sentence, because they carry no closing punctuation."""
    marks = [boxes[i] for i, t in enumerate(texts) if t.strip() == BULLET]
    starts: set[int] = set()
    kept: list[int] = []
    for i, t in enumerate(texts):
        stripped = t.strip()
        if stripped == BULLET:
            continue
        if stripped.startswith(BULLET):
            texts[i] = stripped[1:]
            starts.add(i)
        elif any(m[2] <= boxes[i][0] + 2 and boxes[i][1] - 2 <= (m[1] + m[3]) / 2 <= boxes[i][3] + 2 for m in marks):
            starts.add(i)
        kept.append(i)
    if not starts:
        return []
    groups: list[tuple[list[str], tuple, bool]] = []
    indent = 0.0  # left edge of the current item's text
    for i in kept:
        # A line back at the margin, left of the item text, is a paragraph after the list.
        x = text_x[i] if text_x else boxes[i][0]
        back_out = bool(groups) and groups[-1][2] and x < indent - 4
        if i in starts or not groups or back_out:
            groups.append(([], boxes[i], i in starts))
            indent = x
        lines, box, is_item = groups[-1]
        lines.append(texts[i])
        groups[-1] = (lines, tuple(pymupdf.Rect(box) | pymupdf.Rect(boxes[i])), is_item)
    return groups


def _bold_lead(spans: list[dict]) -> tuple[list[dict], list[dict]]:
    """The bold dated label that opens a line otherwise set plain, and the spans after it.

    The timeline inserts of the Our Pasts books ("Jahangir 1605-1627 Military campaigns
    started by Akbar continued."): two to six words with a four-digit year, at most 40
    characters, starting with a capital, with no closing punctuation, followed on the same
    line by at least 20 characters of plain text. A bold lead-in without a date ("A nation in
    the making", "Transparency:") stays in its sentence."""
    inked = [sp for sp in spans if sp["text"].strip()]
    lead: list[dict] = []
    for sp in inked:
        if not (_span_flags(sp)[0] or sp.get("overprint", 0) >= 2):
            break
        lead.append(sp)
    if not lead or len(lead) == len(inked):
        return [], spans
    label = _join_spans(lead).strip()
    words = label.split()
    if not (2 <= len(words) <= 6) or len(label) > 40 or not label[0].isupper() or re.search(r"[.?!:;,]$", label) or not DATED_LABEL.search(label):
        return [], spans
    rest = [sp for sp in spans if sp not in lead]
    if len(_join_spans(rest).strip()) < 20:
        return [], spans
    return lead, rest


def _prose_follows(b: Block, blocks: list[Block]) -> bool:
    """Is there a paragraph at this block's size right under it (or beside it on the same line)?"""
    for c in blocks:
        if c is b or len(c.text) < 80 or abs(c.size - b.size) > 0.6:
            continue
        # Under the label, or beside it starting no higher than its top (a two-line label with
        # its paragraph alongside).
        if b.y0 - max(b.size, 1.0) <= c.y0 <= b.y1 + 1.5 * max(b.size, 1.0) and c.x0 < b.x1 + 30 and c.x1 > b.x0 - 30:
            return True
    return False


def _prose_under_headings(blocks: list[Block]) -> None:
    """A paragraph set below the body size counts as a table row when short. One that sits
    right under a dated label heading at its own size is prose (the emperors' campaigns in
    chapter 4 of Our Pasts II, set at 11 pt under their bold labels)."""
    for b in blocks:
        if b.role != "table" or len(b.text) < 100 or not re.search(r"[.!?]", b.text):
            continue
        for a in blocks:
            if a is b or a.role != "h3" or not DATED_LABEL.search(a.text) or abs(a.size - b.size) > 0.6:
                continue
            if a.y0 <= b.y0 + 2 and b.y0 - a.y1 <= 1.5 * max(b.size, 1.0) and a.x0 < b.x1 and a.x1 > b.x0:
                b.role = "body"
                break


def _run_in_heading(texts: list[str], line_bold: list[bool], line_faces: list[tuple[set, float]] | None = None, overprinted: list[bool] | None = None) -> bool:
    """Is the first line of this block a short bold heading followed by regular text?

    The 2022 Our Pasts III files embed the bold face under a name without "Bold" and
    without the bold flag ("Revenue for the Company" in TT179EE2O00 over body text in
    TT179E82O00, the "Brahmo Samaj" box titles). There a first line in fonts that the next
    line does not use, at least as large, counts as bold."""
    if len(texts) < 2:
        return False
    if overprinted and overprinted[0] and not overprinted[1] and DATED_LABEL.search(texts[0]):
        line_bold = [True, False] + list(line_bold[2:])  # a dated label drawn five times (2007 Our Pasts II)
    if not (line_bold[0] and not line_bold[1]):
        if not line_faces or len(line_faces) < 2:
            return False
        (fonts0, size0), (fonts1, size1) = line_faces[0], line_faces[1]
        if not fonts0 or not fonts1 or fonts0 & fonts1 or size0 < size1 or line_bold[1]:
            return False
    first = texts[0].strip()
    words = [w for w in first.split() if sum(ch.isalpha() for ch in w) >= 2]
    rest = " ".join(texts[1:]).strip()
    # Two or more words, no figure label, no closing punctuation, and a paragraph after it
    # (a caption's bold "Fig. 1" line followed by its short text is not a heading).
    min_words = 1 if DATED_LABEL.search(first) else 2  # "Jahangir 1605-1627" is one word and a date
    return min_words <= len(words) and len(first) <= 60 and not re.match(r"^fig", first, re.IGNORECASE) and not re.search(r"[.?!:;,]$", first) and len(rest) >= 80


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
    bold_sizes: Counter = Counter()
    for blocks in pages_blocks:
        for b in blocks:
            if 9.0 <= b.size <= 14.5 and len(b.text) > 60:
                (bold_sizes if b.bold else sizes)[b.size] += len(b.text)
    if bold_sizes and max(bold_sizes.values()) > max(sizes.values(), default=0):
        # The 2016 civics files set the whole body in a bold face ("Garamond,Bold"). When one
        # bold size outweighs every regular size, counting only regular prose would take the
        # side questions' size for the body size.
        sizes += bold_sizes
    if not sizes:
        return DEFAULT_BODY_SIZE
    total = sum(sizes.values())
    big = [size for size, n in sizes.items() if n >= 0.25 * total]
    return max(big) if big else sizes.most_common(1)[0][0]


SIDE_FONTS = ("Lucida", "Courier")  # fonts the books reserve for side notes and activity boxes


def footer_key(text: str) -> str:
    """A footer's text without page numbers, print-run labels and punctuation, for spotting
    the running titles that repeat from page to page."""
    return re.sub(r"[\W\d_]+", " ", SESSION_LABEL.sub("", text)).strip().lower()


PRINT_RUN_TAIL = re.compile(r"(Reprint|Rationalised)\s*20\d\d-\d\d\s*$")  # only with its word: "Union Budget 2018-19" is text
SLUG_LINE = re.compile(r"\.indd\b")  # "Chapter 10.indd 227 10-Apr-25 10:53:23 AM", the typesetter's slug


@dataclass
class RunningFooters:
    """What the footers of one document look like, gathered over all of its pages."""

    keys: set[str]  # footer-band texts that repeat on two or more pages (running titles)
    rows: set[int]  # rounded tops of blocks that are certainly footers


def _plain_footer(text: str, keys: set[str] = frozenset()) -> bool:
    """A page number, a print-run label, a slug line, or a running title."""
    bare = SESSION_LABEL.sub("", text).strip()
    return (
        len(text) <= 4
        or not footer_key(text)  # "2019-2020", "75 Rationalised 2023-24": no words at all
        or bool(SLUG_LINE.search(text))
        or bool(RUNNING_TITLE.fullmatch(bare) and len(bare.split()) >= 3)
        or footer_key(text) in keys
    )


def running_footers(pages_blocks: list[tuple[list[Block], float]]) -> RunningFooters:
    """Running titles ("RULERS AND BUILDINGS", "OUR PASTS") repeat from page to page and
    real last lines of a page do not. A running title printed only once in a file is still
    caught by its position: it sits on the same row as the footers of other pages."""
    pages_with: Counter = Counter()
    for blocks, height in pages_blocks:
        pages_with.update({footer_key(b.text) for b in blocks if b.y0 > FOOTER_BAND * height})
    keys = {k for k, n in pages_with.items() if k and n >= 2}
    rows = {round(b.y0) for blocks, height in pages_blocks for b in blocks if b.y0 > FOOTER_BAND * height and _plain_footer(b.text, keys)}
    return RunningFooters(keys, rows)


def _strip_running_title(text: str, keys: set[str]) -> str | None:
    """The text before a running title or print-run label glued to its end ("Hampi. TOWNS,
    TRADERS AND CRAFTSPERSONS", "better already! Rationalised 2023-24"): the last line of a
    caption printed down into the footer. None when nothing is glued."""
    m = PRINT_RUN_TAIL.search(text)
    if m:
        head = text[:m.start()].strip()
        return head if footer_key(head) and not _plain_footer(head, keys) else None
    words = text.split()
    for cut in range(1, len(words)):
        head, tail = " ".join(words[:cut]), " ".join(words[cut:])
        if footer_key(tail) in keys and footer_key(head) and not _plain_footer(head, keys):
            return head
    return None


def inferred_side_fonts(pages_blocks: list[list[Block]], body_size: float) -> tuple[str, ...]:
    """Fonts a file embeds under a generic name and uses the way the books use Lucida Sans.

    The 2015 re-encoding of the Our Pasts II files keeps the body face's name (Bookman-Light)
    but embeds Lucida Sans as "TT3DBT00", so the side-font rule cannot see it and the activity
    boxes set in the body column pass as body text. An opaque font that carries a quarter or
    more of the prose set a point below the body size, and none of the prose at body size,
    is that face."""
    at_body: Counter = Counter()
    below: Counter = Counter()
    for blocks in pages_blocks:
        for b in blocks:
            if len(b.text) < 60:
                continue
            if abs(b.size - body_size) <= 0.5:
                at_body[b.font] += len(b.text)
            elif body_size - 1.6 <= b.size <= body_size - 0.5:
                below[b.font] += len(b.text)
    if not at_body or not below or OPAQUE_FONT.match(at_body.most_common(1)[0][0]):
        return ()
    total = sum(below.values())
    return tuple(f for f, n in below.items() if OPAQUE_FONT.match(f) and n >= 0.25 * total and at_body[f] == 0)


def classify(blocks: list[Block], width: float, height: float, body_size: float = DEFAULT_BODY_SIZE, running: RunningFooters | None = None, side_fonts: tuple[str, ...] = ()) -> int | None:
    """Assign a role to each block in place. Returns the printed page number if found.

    `running` (from running_footers) makes the footer test strict: a block in the footer
    band is a footer only when it is a page number, a print-run label, a running title, text
    that repeats in the band on other pages, or a block on the row where the footers of
    other pages sit. Without it, any short small block there is a footer (the OCR path,
    whose noisy footers do not repeat exactly)."""
    printed: int | None = None
    near = lambda s, target, tol=0.6: abs(s - target) <= tol  # noqa: E731
    # Exercise questions are set a point smaller than the body, and on an exercises page they
    # are the only prose, so they must count or no column is found and margin words such as
    # the KEYWORDS list pass as body text.
    body = [b for b in blocks if near(b.size, body_size, 1.4) and not b.bold and len(b.text) > 40]
    if not body:
        # The 2016 civics files set the body in a "Garamond,Bold" face throughout. Without
        # this the column spans the page and a side question counts as body text, which
        # then splits the sentence running over the page break.
        body = [b for b in blocks if near(b.size, body_size) and len(b.text) > 40]
    if body:
        col_left = min(b.x0 for b in body) - 6
        col_right = max(b.x1 for b in body) + 6
    else:
        col_left, col_right = 0.0, width

    for b in blocks:
        if AXIS_TICKS.fullmatch(b.text.strip()):
            b.role = "decoration"  # a map's axis tick, not text of the book
            continue
        if ((b.x0 < -0.5 and b.x1 < 0.12 * width) or (b.x1 > width + 0.5 and b.x0 > 0.88 * width)) and b.size <= body_size - 1:
            # Text running off the page in a sliver at its edge: the 2007 files print the
            # facing page's caption so that only its last letters reach this one ("har baghs",
            # "hmir, 634."). A caption that only loses its first letters to the edge stays.
            b.role = "decoration"
            continue
        b.text = LEADING_TICKS.sub("", b.text)
        in_column = col_left <= b.centre_x <= col_right
        side_font = any(f in b.font for f in SIDE_FONTS) or b.font in side_fonts
        delta = body_size - b.size  # positive when smaller than body text
        # Footers are short and set small. An exercise question that happens to end the
        # page is neither, even though it sits in the same band.
        # "2022-23" is a print-run label, not page 23. Some files glue it to the running title.
        in_band = b.y0 > FOOTER_BAND * height
        glued = None
        if in_band and running is not None:
            glued = _strip_running_title(b.text, running.keys)
            if glued is not None:
                b.text = glued  # the caption's tail is kept and classified like any block
        bare = SESSION_LABEL.sub("", b.text).strip()
        title_like = RUNNING_TITLE.fullmatch(bare) and len(bare.split()) >= 3
        short = len(b.text) <= 60 or (title_like and len(b.text) <= 80)  # a glued "Rationalised 2023-24" makes a running title longer
        # The last lines of a page in the 2021-24 civics files sit at 86 to 87 per cent of the
        # height, inside the band ("armed forces for being a woman.", "Tyranny: ..."), and
        # photo captions can sit lower still. They are set small too, so position and size
        # are not enough: the block must also look like a footer.
        footer_like = running is None or (glued is None and (
            _plain_footer(b.text, running.keys)
            or any(abs(round(b.y0) - row) <= 2 for row in running.rows)
            or b.y0 > SLUG_BAND * height  # left on the pasteboard below the print run label ("H.T. Colebrook")
        ))
        if in_band and short and footer_like and (delta >= 1.4 or len(b.text) <= 4 or SESSION_LABEL.fullmatch(b.text) or title_like):
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
        if b.size >= body_size + 1.5 and len(b.text) <= 60 and sum(ch.isalpha() for ch in b.text) >= 2 and not re.search(r"[.?!,;]$", b.text.strip()):
            # A box title in a display face whose bold the file does not flag ("The value of
            # paper", 15 pt over 13 pt body in the 2016 Our Pasts II).
            b.role = "h3"
            continue
        if "Corsiva" in b.font:
            b.role = "source"
            continue
        if SDG_LABEL.match(b.text) and len(b.text) <= 80:
            b.role = "caption"  # a badge label, not a sentence, so it must not join the paragraph below it
            continue
        if ACTIVITY_HEADING.fullmatch(b.text):
            b.role = "h3"
            continue
        if b.bold and in_column and delta <= 2.6 and len(b.text) <= 60 and DATED_LABEL.search(b.text) and not re.search(r"[.?!:;,]$", b.text) and _prose_follows(b, blocks):
            b.role = "h3"  # a dated label over its paragraph in a timeline insert set below the body size
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
    _prose_under_headings(blocks)
    _keyword_list(blocks)
    _join_wrapped_items(blocks)
    _extend_captions(blocks, body_size)
    _stack_caption_lines(blocks)
    _stack_centred_lines(blocks)
    _short_headings(blocks, body_size)
    _join_split_titles(blocks)
    _join_stacked_titles(blocks)
    for b in blocks:
        # A line of nothing but one- or two-digit numbers among the body text is a picture's
        # label, not a paragraph: the numbered badges on a photo collage ("1" to "7" in
        # Exploring Society), the steps of a flow chart, the axis of a bar chart.
        # Values of 20 and more are a chart's data ("74 63 57" over the bars), which stays.
        if b.role in ("body", "note") and NUMBER_LABELS.fullmatch(b.text.strip()) and b.y1 - b.y0 < 2.2 * max(b.size, 1.0) and all(int(n) <= 20 for n in b.text.split()):
            b.role = "decoration"
    return printed


def _join_stacked_titles(blocks: list[Block]) -> None:
    """A box title set as two overlapping blocks in two sizes, "The Big" (12 pt with a 23 pt
    "Big") over "Questions" (18 pt) in Exploring Society, is one heading. Apart, the first
    words pass as a paragraph and "Questions" alone reads as the exercises heading."""
    for h in blocks:
        if h.role != "h2":
            continue
        for b in blocks:
            if b is h or not b.bold or b.role in ("footer", "h2", "decoration") or len(b.text.split()) > 3 or re.search(r"[.?!:;,]$", b.text):
                continue
            # The first block starts above the heading, its box reaches down into the
            # heading's, and the heading starts inside its width.
            if b.y0 < h.y0 < b.y1 and b.x0 <= h.x0 < b.x1:
                # The heading keeps its own top, so it is still read after a question that
                # starts level with "The Big" and wraps past it.
                h.text = f"{b.text} {h.text}"
                h.x0 = min(h.x0, b.x0)
                b.role = "decoration"  # written as part of the heading
                break


def _join_split_titles(blocks: list[Block]) -> None:
    """A heading broken over two blocks ("Why do we" over "need cash!", an Elsewhere box
    title) is one heading: the lower-case second line is joined to it."""
    for b in blocks:
        if b.role != "h3":
            continue
        for o in blocks:
            if o is not b and o.role not in ("footer", "h2", "h3") and abs(o.size - b.size) < 0.5 and 0 <= o.y0 - b.y1 <= 0.6 * b.size and o.x0 < b.x1 and b.x0 < o.x1 and o.text[:1].islower() and len(o.text) <= 60:
                b.text = f"{b.text} {o.text}"
                o.role = "decoration"  # written as part of the heading
                break


def _short_headings(blocks: list[Block], body_size: float) -> None:
    """A short italic or bold line at body size set straight above a paragraph and aligned
    with it is a sub-heading ("Gulamgiri" in Our Pasts III). As body text it reads as a
    one-word paragraph, or glues to whatever is pending from the page before."""
    for b in blocks:
        if b.role != "body" or not (b.italic or b.bold) or b.size < body_size - 1.5 or b.font == "OUTLINED":
            continue  # an outlined run is a paragraph's own words read back, never evidence of a heading
        text = b.text.strip()
        if len(text) > 60 or len(text.split()) > 8 or re.search(r"[.?!:;,]$", text) or not text[:1].isupper():
            continue
        if b.size >= body_size - 0.5 and any(o is not b and o.role == "body" and not o.bold and 0 <= o.y0 - b.y1 <= b.size and abs(o.x0 - b.x0) <= 4 for o in blocks):
            b.role = "h3"
        elif b.bold and b.italic and len(text.split()) >= 2 and not text.lower().startswith("fig"):
            # A figure group's title in bold italic ("Temple Construction in the Early
            # Eleventh Century", 2016 Our Pasts II), which otherwise runs into the question
            # box or paragraph that follows it.
            b.role = "h3"


def _lower_start(text: str) -> bool:
    """Does this block start the way a wrapped line goes on, in lower case? A letter with a
    bracket or a full stop is a list marker ("b) Do you think", "b. to defend the country"),
    and so is a lone letter before a capital (the Wingdings bullet "q" of the imprint page
    read as a letter, "q The correct price"). Neither is a continuation."""
    return text[:1].islower() and not re.match(r"^[a-z][).]\s|^[a-z]\s+[A-Z]", text)


def _stack_caption_lines(blocks: list[Block]) -> None:
    """The second line of a caption that PyMuPDF set as a block of its own ("in the plains"
    under "Fig. 1.11. Modern agricultural practices", beside "river Yamuna on top right"
    under "Fig. 1.12. ...") belongs to the caption straight above it. Left to the reading
    order, it follows whichever caption ends nearest, which for side-by-side captions is the
    neighbour. Only a line that starts in lower case, or follows a caption ending in a comma,
    is joined, or one in the caption's own face that the caption runs into: a description
    set under a caption title, in another face, is a caption of its own."""
    for b in sorted([b for b in blocks if b.role == "caption"], key=lambda b: b.y0):
        if b not in blocks or b.text.startswith("Fig"):
            continue
        above = [
            c for c in blocks
            if c is not b and c.role == "caption" and abs(c.size - b.size) <= 1.0
            and -0.5 * b.size <= b.y0 - c.y1 <= 0.8 * b.size and c.x0 - 2 <= b.centre_x <= c.x1 + 2
        ]
        if len(above) != 1:
            continue
        c = above[0]
        # A line in the caption's own face that the caption runs into (no closing
        # punctuation) goes on with it too ("... in Bandhavgarh" / "National Park, Madhya
        # Pradesh"). A description under a caption title is set in another face.
        # The next line of one caption overlaps it (line boxes are taller than the leading),
        # a separate paragraph under it leaves a gap.
        runs_on = c.text.startswith("Fig") and b.font == c.font and b.italic == c.italic and not clean.ends_sentence(c.text) and b.y0 <= c.y1
        bare_label = bool(re.fullmatch(r"Fig\.\s*[\d.]+", c.text.strip()))  # "Fig. 1.23." over its text
        after_comma = c.text.startswith("Fig") and c.text.rstrip().endswith(",")  # a poem's line ends in a comma too
        if not (_lower_start(b.text) or after_comma or runs_on or bare_label):
            continue
        c.text = clean.merge_paragraphs(c.text, b.text)
        c.x0, c.x1, c.y1 = min(c.x0, b.x0), max(c.x1, b.x1), max(c.y1, b.y1)
        blocks.remove(b)


def _stack_centred_lines(blocks: list[Block]) -> None:
    """Lines of one small block that PyMuPDF cut apart. A speech bubble of the civics comics is set centred, and PyMuPDF cuts it into a block
    per line or two ("Ma, we are going on a school excursion. Rosie Ma’am" / "needs
    volunteers. Can’t you" / "take a holiday from office" / "and volunteer?"). Read in page
    order, the lines of bubbles side by side interleave. Blocks in one small face, centred on
    the same axis (or flush left on the same edge) and set at line spacing, are one block
    when the next one starts in lower case."""
    changed = True
    while changed:
        changed = False
        for c in sorted(blocks, key=lambda b: b.y0):
            if c.role not in ("table", "caption", "note"):
                continue
            below = [
                b for b in blocks
                # The last line of a bubble at the foot of the page can sit in the footer band
                # ("taken leave today."), but no footer starts in lower case.
                if b is not c and b.role in (c.role, "footer") and b.font == c.font and abs(b.size - c.size) < 0.5
                and not b.text.startswith("Fig")
                and ((-1 <= b.y0 - c.y1 <= 0.3 * c.size and abs(b.centre_x - c.centre_x) <= 3)
                     # A wrapped line set flush left under its block, in a page of two columns
                     # that reading order would otherwise interleave ("... based on the household
                     # tasks" / "undertaken by women in your home." beside "d. The work that
                     # women do is less" / "valued than that of men.").
                     # A line that closes ("rabi season (winter crops)") is a label of its own.
                     or (-1 <= b.y0 - c.y1 <= 0.5 * c.size and abs(b.x0 - c.x0) <= 3 and c.role != "footer" and not clean.ends_sentence(c.text)))
            ]
            if len(below) != 1:
                continue
            b = below[0]
            # Only a lower-case start runs on: the centred lines of a poem each start with a
            # capital, and "b) Do you think ..." is the next item of a list.
            if not _lower_start(b.text):
                continue
            c.text = clean.merge_paragraphs(c.text, b.text)
            c.x0, c.x1, c.y1 = min(c.x0, b.x0), max(c.x1, b.x1), max(c.y1, b.y1)
            blocks.remove(b)
            changed = True
            break


def _extend_captions(blocks: list[Block], body_size: float) -> None:
    """A paragraph set smaller than the body text straight under a caption is the rest of
    that caption ("Fig. 7 - The rebels of 1857" then "Images need to be carefully studied
    ..." in the 2019 Our Pasts III). Left as body text, it splices into the sentence that
    runs from the foot of the previous page to the top of this one."""
    changed = True
    while changed:
        changed = False
        captions = [c for c in blocks if c.role == "caption"]
        for b in blocks:
            if b.role not in ("body", "table") or body_size - b.size < 1.4:
                continue
            for c in captions:
                gap = b.y0 - c.y1
                if -2 <= gap <= 0.8 * b.size and b.x0 < c.x1 and c.x0 < b.x1 and abs(c.size - b.size) <= 1.0:
                    b.role = "caption"
                    changed = True
                    break


def _read_all_pages(pdf_path: Path, vocab: set[str] | None = None) -> tuple[list[Page], float]:
    from .ocr import outlined_reader  # lazy: tesseract is optional

    reader = outlined_reader(pdf_path, vocab)
    pages: list[Page] = []
    width = 600.0
    rasterised: set[int] = set()
    with pymupdf.open(pdf_path) as doc:
        raw = []
        font_fixes = shifted_quote_fonts(doc)
        for i, page in enumerate(doc):
            if i == 0:
                width = page.rect.width
            blocks = read_blocks(page, reader, font_fixes)
            if all(b.font == "OUTLINED" for b in blocks) and _is_page_image(page):
                # A few pages of an otherwise normal file are flat images (2024-25 Class 7
                # civics has three). They are read the way whole image-only files are.
                blocks = _ocr_page_blocks(pdf_path, i)
                rasterised.add(i)
            raw.append((i, blocks, page.rect.width, page.rect.height))
    body_size = font_profile([blocks for i, blocks, _, _ in raw if i not in rasterised])
    side_fonts = inferred_side_fonts([blocks for i, blocks, _, _ in raw if i not in rasterised], body_size)
    running = running_footers([(blocks, h) for i, blocks, _, h in raw if i not in rasterised])
    for i, blocks, w, h in raw:
        if i in rasterised:
            # Sizes guessed from OCR line heights do not match the real fonts, so an OCR'd
            # page is judged against its own commonest size.
            printed = classify(blocks, w, h, _commonest_size(blocks) or body_size)
        else:
            printed = classify(blocks, w, h, body_size, running, side_fonts)
        pages.append(Page(i, printed, blocks, ocr=i in rasterised))
    fix_page_numbers(pages)
    return pages, width


def _commonest_size(blocks: list[Block]) -> float | None:
    votes: Counter = Counter()
    for b in blocks:
        votes[b.size] += len(b.text)
    return votes.most_common(1)[0][0] if votes else None


def _is_page_image(page: pymupdf.Page, min_cover: float = 0.7) -> bool:
    """True when one image covers most of the page (a rasterised page)."""
    area = page.rect.width * page.rect.height
    for info in page.get_image_info():
        x0, y0, x1, y1 = info["bbox"]
        if (max(0.0, x1 - x0) * max(0.0, y1 - y0)) >= min_cover * area:
            return True
    return False


def _ocr_page_blocks(pdf_path: Path, index: int) -> list[Block]:
    from . import ocr  # lazy: tesseract is optional

    if not ocr.available():
        return []
    tsv = ocr._tsv_for_page(pdf_path, index, pdf_path.parent / "ocr")
    blocks, _ = ocr.blocks_from_tsv(tsv, 72.0 / ocr.DPI)
    for b in blocks:
        b.size = round(b.size)
        b.max_size = b.size
    return blocks


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


KEYWORDS_LABEL = re.compile(r"^keywords?\s*:?$", re.IGNORECASE)


def _join_wrapped_items(blocks: list[Block]) -> None:
    """A list item that wraps can arrive as two blocks: the marker line and, right below it,
    a line indented to the item's text column ("- If a group ... to open a" then
    "Telugu-medium school in Kerala."). The second is the rest of the item, whatever letter
    it starts with, so it is folded into the first."""
    by_pos = sorted(blocks, key=lambda b: (b.y0, b.x0))
    for prev, nxt in zip(by_pos, by_pos[1:]):
        if nxt not in blocks or prev not in blocks:
            continue
        marker = re.match(r"^(?:[-•–]|\d{1,2}\.|[a-z]\.)\s", prev.text)
        if not marker or re.search(r"[.!?:;]$", prev.text.rstrip("’”\")")):
            continue
        line_h = max(prev.size, 1.0)
        if not (0 <= nxt.y0 - prev.y1 <= 0.6 * line_h) or not (prev.x0 + 3 <= nxt.x0 <= prev.x0 + 3 * line_h):
            continue
        if abs(nxt.size - prev.size) > 0.6 or nxt.role != prev.role or "\n" in nxt.text:
            continue
        prev.text = clean.merge_paragraphs(prev.text, nxt.text)
        prev.x1, prev.y1 = max(prev.x1, nxt.x1), nxt.y1
        blocks.remove(nxt)


def _keyword_list(blocks: list[Block]) -> None:
    """The KEYWORDS column of the Our Pasts books: a label and one term per line in a narrow
    margin column. The label and its terms get the role "keyword", written as a heading and
    a list, so the terms neither pass as body text nor scatter as notes."""
    for label in [b for b in blocks if KEYWORDS_LABEL.match(b.text.strip())]:
        label.role = "keyword"
        column = sorted(
            (b for b in blocks if b is not label and b.y0 > label.y0 and b.role not in ("h2", "footer", "decoration")
             and abs(b.centre_x - label.centre_x) <= 40 and b.x1 - b.x0 <= 2 * (label.x1 - label.x0)),
            key=lambda b: b.y0,
        )
        # Lines set at the column's own pitch form one run. A run that reads as prose (a line
        # of more than three words, or a sentence end inside it) is the column's instruction
        # set one line per block ("Go through the chapter and make your own list of six
        # keywords." in the 2020 Our Pasts II files), not terms: it becomes one note.
        runs: list[list[Block]] = []
        for b in column:
            if runs and b.y0 - runs[-1][-1].y1 <= 1.5 * max(b.size, 1.0):
                runs[-1].append(b)
            else:
                runs.append([b])
        for run in runs:
            if any(len(b.text.split()) > 3 for b in run) or ". " in " ".join(b.text for b in run):
                first = run[0]
                for b in run[1:]:
                    first.text = clean.merge_paragraphs(first.text, b.text)
                    first.x0, first.x1, first.y1 = min(first.x0, b.x0), max(first.x1, b.x1), b.y1
                    blocks.remove(b)
                continue
            for b in run:
                b.role = "keyword"


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


def _margin_blocks(blocks: list[Block], width: float, use_size: bool = True) -> set[int]:
    """ids of the body-size blocks that sit in the margin rather than in a text column.

    The Our Pasts III margin boxes (an Activity box, a column of glossary entries) are set at
    body size, so they classify as body text. A box like that is either alone beside the
    column (outside every column) or one of a few blocks forming a column of its own, much
    narrower than the text column. Read as body text, it runs into the sentence the column
    paragraph is still in ("... British rule, Mill felt, could civilise India. To do" then
    "Interview your mother ..."), so it is written as a box instead."""
    body = [b for b in blocks if b.role in ("body", "table", "h2", "h3", "dropcap", "chapter-number")]
    cols = _columns(body, width)
    widest = max(right - left for left, right in cols)
    # The size of the text in the widest column. A box beside it can be as wide as a narrow
    # column but is set a point smaller ("Lachit Barphukan and the defeat of the Mughals in
    # Assam" in the 2024 Our Pasts II), which a second column of body text is not.
    main = [b for b in body if b.role == "body" and any(left <= b.centre_x <= right and right - left == widest for left, right in cols)]
    sizes = Counter(round(b.size, 1) for b in main for _ in range(len(b.text)))
    col_size = sizes.most_common(1)[0][0] if sizes else None
    out: set[int] = set()
    for b in blocks:
        if b.role not in ("body", "h2"):
            continue
        smaller = use_size and b.role == "body" and col_size is not None and col_size - b.size >= 0.5
        if b.x1 - b.x0 > 0.6 * widest and not smaller:
            continue
        col = next(((left, right) for left, right in cols if left <= b.centre_x <= right), None)
        if col is None or col[1] - col[0] < 0.7 * widest:
            out.add(id(b))
    return out


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
    pending_dropcap: Block | None = None
    pending_size, pending_font = 0.0, ""  # font size and font of the pending paragraph
    pending_box: str | None = None  # a margin box paragraph, kept apart from the column's paragraph
    first_heading_done = False  # the chapter title gets "#", wherever in the file it falls

    def emit(*items: str) -> None:
        target = deferred if pending_body is not None else lines
        target.extend(items)

    def close_box() -> None:
        nonlocal pending_box
        if pending_box is not None:
            text, pending_box = pending_box, None
            emit(text, "")

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
        pending_dropcap = None  # a drop cap opens a paragraph on its own page
        # On a page read with OCR the sizes are guesses, so only the geometry counts there.
        margin = _margin_blocks(page.blocks, width, use_size=not page.ocr)
        for b in _reading_order(page.blocks, width):
            if b.role in ("footer", "decoration"):
                continue
            if id(b) in margin and b.role == "h2" and first_heading_done:
                # A box title in the margin ("Language of" / "the wise?" over a Source box)
                # does not end the column paragraph beside it.
                close_box()
                emit(f"## {b.text}", "")
                continue
            if id(b) in margin and b.role == "body":
                # A margin box at body size: its blocks join each other, but it is written
                # after the column paragraph it sits beside, which goes on past it. Only a
                # plain continuation joins: glossary entries carry no closing punctuation,
                # and each one is a block of its own.
                if pending_box is not None and clean.continues(pending_box, b.text) and (_lower_start(b.text) or b.text[:1] in ",;" or pending_box.endswith("-")):
                    pending_box = clean.merge_paragraphs(pending_box, b.text)
                else:
                    close_box()
                    pending_box = b.text
                continue
            close_box()
            if b.role == "chapter-number":
                _, embedded_title = split_number_and_title(b.text)
                if embedded_title and not first_heading_done:
                    flush()
                    lines.extend((f"# {embedded_title}", ""))
                    first_heading_done = True
                continue
            if b.role == "dropcap":
                pending_dropcap = b
                continue
            if b.role == "body":
                text = b.text
                if pending_dropcap is not None and _opens_with_dropcap(pending_dropcap, b):
                    text = pending_dropcap.text + text
                pending_dropcap = None
                # (OCR sizes are guesses, so OCR'd pages and outlined runs are left out.)
                if pending_body is not None and not page.ocr and pending_font != "OUTLINED" and pending_size - b.size >= 0.9 and not clean.ends_sentence(pending_body):
                    # Smaller text met while a body paragraph is still open is a box set into
                    # the column ("The value of paper" box in the 2016 Our Pasts II): written
                    # after the paragraph, which goes on past it ("... cheaper and" / "widely
                    # available.").
                    emit(text, "")
                    continue
                if pending_body is not None and clean.continues(pending_body, text):
                    pending_body = clean.merge_paragraphs(pending_body, text)
                else:
                    flush()
                    pending_body = text
                    pending_size, pending_font = b.size, b.font
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
            if b.role == "keyword":
                emit("### Keywords" if KEYWORDS_LABEL.match(b.text.strip()) else f"- {b.text}", "")
                continue
            # Captions, notes, sources, tables: kept in place, without ending the paragraph.
            if clean.has_content(b.text):
                emit(f"> [{b.role}] {b.text}", "")
        close_box()
    flush()
    lines = _merge_split_asides(lines)
    lines = [ln for i, ln in enumerate(lines) if ln != "" or (i > 0 and lines[i - 1] != "")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def _opens_with_dropcap(cap: Block, body: Block) -> bool:
    """Does this body block start beside the drop cap? The big "Q" of a question box and the
    "Po" of the police-station art (Social and Political Life III) are oversized glyphs too,
    but nothing starts next to them, and the paragraph that follows them in reading order
    sits well below or on the next page ("QImagine", "PoFrom")."""
    height = cap.y1 - cap.y0
    return cap.x0 - 10 <= body.x0 <= cap.x1 + 30 and cap.y0 - 0.5 * height <= body.y0 <= cap.y1


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
            # A "Fig." label starts a caption of its own, whatever the one before ends with
            # (the captions of a photo grid carry no closing punctuation).
            # So does a margin note's label ("Transparency:"), which is set in bold above its text.
            new_figure = m.group(1) == "caption" and re.match(r"^Fig\.\s", m.group(2))
            label = re.fullmatch(r"[A-Z][\w’' -]{0,40}:", m.group(2).strip())
            if pm and pm.group(1) == m.group(1) and not new_figure and not label and clean.continues(pm.group(2), m.group(2)):
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


def extract_chapter_file(pdf_path: Path, carry: list[Page] | None = None, vocab: set[str] | None = None) -> tuple[list[tuple[str, dict]], list[Page]]:
    """Every chapter in a per-chapter PDF, plus any trailing unit opener that belongs to the
    next file. Usually one chapter, but NCERT sometimes packs two chapters into one file (the
    2023-24 Class 7 civics ch08 holds chapters 7 and 8), so a file is cut at its chapter
    openers when they carry distinct chapter numbers. `carry` is the previous file's trailing
    opener, placed in front of this chapter. `vocab` (words the book uses in other editions)
    steadies the OCR of outlined words."""
    pages, width = _read_all_pages(pdf_path, vocab)
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
    if any(p.ocr for p in pages):
        meta["ocr_pages"] = [p.index + 1 for p in pages if p.ocr]
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
