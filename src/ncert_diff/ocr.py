"""OCR for chapter PDFs that carry no text layer.

Some NCERT reprints (the 2022-23 Our Pasts II files) are rasterised page images with only
a footer in the text layer. Each page is rendered at 300 dpi and read with tesseract. The
word boxes come back as TSV, are grouped into tesseract's own paragraphs, and are turned
into the same Block objects the normal extractor uses, so classification and Markdown
output are shared. Tesseract output is cached next to the PDF because it is slow.
"""

from __future__ import annotations

import csv
import io
import json
import re
import shutil
import statistics
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

from . import clean
from .extract import Block, Page, _render, _reading_order  # noqa: F401  (reading order reused by callers)
from .extract import classify, fix_page_numbers, font_profile, title_page_position

DPI = 300
TESSERACT = shutil.which("tesseract")
LINE_HEIGHT_TO_SIZE = 0.8  # a text line's box spans ascender to descender, about 1.25 em
MIN_SHORT_CONFIDENCE = 70.0
SLUG = re.compile(r"^\d{4}\s*CH\s*\d{2}$", re.IGNORECASE)  # "0760CH04" print slugs


def available() -> bool:
    return TESSERACT is not None


def _tsv_for_page(pdf_path: Path, index: int, cache_dir: Path) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    tsv_path = cache_dir / f"{pdf_path.stem}-p{index + 1:02d}.tsv"
    if tsv_path.exists():
        return tsv_path.read_text()
    with pymupdf.open(pdf_path) as doc:
        pix = doc[index].get_pixmap(dpi=DPI, colorspace=pymupdf.csGRAY)
        png = cache_dir / f"{pdf_path.stem}-p{index + 1:02d}.png"
        pix.save(png)
    proc = subprocess.run(
        [TESSERACT, str(png), "stdout", "--psm", "3", "-l", "eng", "tsv"],
        capture_output=True, text=True, check=True,
    )
    png.unlink(missing_ok=True)
    tsv_path.write_text(proc.stdout)
    return proc.stdout


def blocks_from_tsv(tsv: str, scale: float) -> tuple[list[Block], float]:
    """Tesseract word rows -> Blocks (one per tesseract paragraph). Returns (blocks, mean confidence)."""
    rows = list(csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE))
    words = [r for r in rows if r["level"] == "5" and r["text"].strip()]
    paragraphs: dict[tuple[str, str], dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for w in words:
        paragraphs[(w["block_num"], w["par_num"])][w["line_num"]].append(w)
    blocks: list[Block] = []
    confs: list[float] = []
    for _, lines in sorted(paragraphs.items(), key=lambda kv: (int(kv[0][0]), int(kv[0][1]))):
        texts: list[str] = []
        heights: list[float] = []
        x0 = y0 = float("inf")
        x1 = y1 = 0.0
        for _, ws in sorted(lines.items(), key=lambda kv: int(kv[0])):
            ws.sort(key=lambda w: int(w["left"]))
            texts.append(" ".join(w["text"] for w in ws))
            top = min(int(w["top"]) for w in ws)
            bottom = max(int(w["top"]) + int(w["height"]) for w in ws)
            heights.append((bottom - top) * scale)
            x0 = min(x0, min(int(w["left"]) for w in ws) * scale)
            x1 = max(x1, max(int(w["left"]) + int(w["width"]) for w in ws) * scale)
            y0 = min(y0, top * scale)
            y1 = max(y1, bottom * scale)
        text = clean.join_lines(texts)
        if not text or not clean.has_content(text):
            continue
        block_conf = [float(w["conf"]) for ws in lines.values() for w in ws if float(w["conf"]) >= 0]
        mean_conf = statistics.fmean(block_conf) if block_conf else 0.0
        # Short, unsure fragments are picture noise read as text ("; i Eatiteed ik 2").
        if len(text) < 25 and mean_conf < MIN_SHORT_CONFIDENCE:
            continue
        if SLUG.fullmatch(text):
            continue
        size = round(statistics.median(heights) * LINE_HEIGHT_TO_SIZE, 1)
        blocks.append(Block(x0, y0, x1, y1, "OCR", size, False, False, text, size))
        confs.extend(block_conf)  # confidence is reported over the words that were kept
    return blocks, (statistics.fmean(confs) if confs else 0.0)


def read_pages_ocr(pdf_path: Path) -> tuple[list[Page], float, float]:
    """Pages with classified blocks from OCR. Returns (pages, page width, mean word confidence)."""
    if not available():
        raise RuntimeError("tesseract is not installed")
    cache_dir = pdf_path.parent / "ocr"
    raw = []
    confs = []
    with pymupdf.open(pdf_path) as doc:
        width = doc[0].rect.width if doc.page_count else 600.0
        geometry = [(p.rect.width, p.rect.height) for p in doc]
    for i, (w, h) in enumerate(geometry):
        tsv = _tsv_for_page(pdf_path, i, cache_dir)
        blocks, conf = blocks_from_tsv(tsv, 72.0 / DPI)
        confs.append(conf)
        raw.append((i, blocks, w, h))
    # Rounded sizes vote better than the noisy per-paragraph estimates.
    body_size = font_profile([[_rounded(b) for b in blocks] for _, blocks, _, _ in raw])
    pages = []
    for i, blocks, w, h in raw:
        for b in blocks:
            b.size = round(b.size)
            b.max_size = b.size
        printed = classify(blocks, w, h, body_size)
        pages.append(Page(i, printed, blocks))
    fix_page_numbers(pages)
    return pages, width, (statistics.fmean(confs) if confs else 0.0)


_OUTLINED_JUNK = re.compile(r"[^A-Za-z0-9\u00C0-\u024F’'\"“”‘.,;:()\-\s]")


def clean_outlined(raw: str) -> str:
    """Tesseract's reading of an outlined word or line, with the symbols it hallucinates on
    italics and macrons removed ("pardes i |" -> "pardes i")."""
    word = _OUTLINED_JUNK.sub("", raw).strip()
    word = re.sub(r"\s+", " ", word)
    return word if sum(ch.isalpha() for ch in word) >= 2 else ""


_TOKEN = re.compile(r"^([^A-Za-z]*)([A-Za-z][A-Za-z'’-]*)([^A-Za-z]*)$")


def _ratio(a: str, b: str) -> float:
    import difflib

    return difflib.SequenceMatcher(None, a, b).ratio()


def _best_word(core: str, vocab: dict[int, list[str]]) -> str | None:
    """The vocabulary word nearest to an OCR'd word, or None when nothing is close enough."""
    low = core.lower()
    need = 0.75  # one letter wrong in a four-letter word, two in an eight-letter one
    best, best_r = None, 0.0
    for length in range(len(low) - 2, len(low) + 3):
        for w in vocab.get(length, ()):
            if w[0] != low[0] and w[-1] != low[-1]:
                continue  # a misread keeps at least one end of the word
            r = _ratio(low, w)
            if r > best_r:
                best, best_r = w, r
    return best if best_r >= need else None


def _recase(word: str, like: str) -> str:
    """Give a vocabulary word the case pattern of the OCR'd token it replaces. A token with
    stray capitals inside ("EXYIcise") is treated as lower case."""
    if like.isupper() and len(like) > 1:
        return word.upper()
    if like[:1].isupper() and like[1:].islower() and like[:1].lower() == word[:1]:
        return word[:1].upper() + word[1:]  # the capital survived the misread, so keep it
    return word


def _recase_parts(candidate: str, tokens: list[str]) -> str:
    """Case each hyphen-separated part of a vocabulary word like the token it replaces."""
    parts = candidate.split("-")
    if len(parts) != len(tokens):
        return _recase(candidate, tokens[0])
    return "-".join(_recase(part, tok.strip(".,;:!?") or "x") for part, tok in zip(parts, tokens))


def snap_to_vocabulary(text: str, vocab: dict[int, list[str]], known: set[str]) -> str:
    """Pull an OCR'd outlined run towards words the book is known to use.

    The runs are italic lines whose glyphs were drawn as outlines; tesseract reads most of
    them cleanly but drops or doubles letters at ligatures ("EXYIcise", "pardes i",
    "Minhaj 1 Siraj"). A run whose letters, joined, spell a known word becomes that word.
    Otherwise each unknown word is replaced by the nearest known word when one is close."""
    if not text or not vocab:
        return text
    tokens = text.split()
    cores = [m.group(2) if (m := _TOKEN.match(t)) else "" for t in tokens]
    # Whole run: "pardes i" -> "pardesi", "fi or" -> "for", "Minhaj 1 Siraj" -> "Minhaj-i-Siraj".
    if 2 <= len(tokens) <= 3 and all(cores) or (len(tokens) == 3 and tokens[1].isdigit()):
        letters = "".join(c for c in text if c.isalpha()).lower()
        joined = "".join(ch if ch.isalnum() else "" for ch in text).lower()
        hyphenated = "-".join(t.strip(".,;:") for t in tokens).lower().replace("1", "i")
        tail = text[len(text.rstrip(".,;:!?")):]
        for candidate in (letters, joined, hyphenated):
            if candidate in known:
                return (_recase_parts(candidate, tokens) if "-" in candidate else _recase(candidate, tokens[0])) + tail
        close = _best_word(hyphenated, vocab) if "-" in hyphenated else None
        if close and "-" in close:
            return _recase_parts(close, tokens) + tail
        if len(tokens) == 2 and min(len(c) for c in cores) <= 2:
            # A ligature read as its own token: "fi or" for "for".
            close = _best_word(letters, vocab)
            if close:
                return _recase(close, tokens[0]) + tail
    out = []
    for tok, core in zip(tokens, cores):
        if not core or len(core) < 3 or core.lower() in known:
            out.append(tok)
            continue
        better = _best_word(core, vocab)
        out.append(tok.replace(core, _recase(better, core)) if better else tok)
    # A ligature split doubles letters across two runs ("diffi" + "ifficult"). After snapping
    # that leaves the same word twice, or an unknown fragment that begins the next word.
    deduped: list[str] = []
    for i, tok in enumerate(out):
        if deduped and tok.lower() == deduped[-1].lower() and len(tok) > 3:
            continue
        core = (m.group(2) if (m := _TOKEN.match(tok)) else "").lower()
        nxt = (m.group(2) if i + 1 < len(out) and (m := _TOKEN.match(out[i + 1])) else "").lower()
        if core and core not in known and len(core) >= 3 and nxt.startswith(core) and nxt != core:
            continue
        deduped.append(tok)
    return " ".join(deduped)


def vocabulary_index(words: set[str]) -> dict[int, list[str]]:
    """Known words grouped by length, for snap_to_vocabulary."""
    index: dict[int, list[str]] = {}
    for w in words:
        index.setdefault(len(w), []).append(w)
    return index


def outlined_reader(pdf_path: Path, vocab: set[str] | None = None):
    """A callable that OCRs a small page rectangle (an outlined word), cached per PDF.
    With `vocab` (words the book uses elsewhere) the reading is snapped to known words."""
    if not available():
        return None
    cache_path = pdf_path.parent / "ocr" / f"{pdf_path.stem}-outlined.json"
    cache: dict[str, str] = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    index = vocabulary_index(vocab) if vocab else {}
    known = vocab or set()

    def read(page: pymupdf.Page, rect: pymupdf.Rect) -> str | None:
        key = f"{page.number}:{round(rect.x0)}:{round(rect.y0)}:{round(rect.x1)}:{round(rect.y1)}"
        if key in cache:
            return snap_to_vocabulary(cache[key], index, known) or None
        clip = (rect + (-4, -4, 4, 4)) & page.rect
        if clip.is_empty or clip.width < 3 or clip.height < 3:
            cache[key] = ""
            return None
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        png = cache_path.parent / f"{pdf_path.stem}-outlined.png"
        page.get_pixmap(dpi=600, clip=clip, colorspace=pymupdf.csGRAY).save(png)
        proc = subprocess.run([TESSERACT, str(png), "stdout", "--psm", "7", "-l", "eng"], capture_output=True, text=True, check=False)
        png.unlink(missing_ok=True)
        word = clean_outlined(proc.stdout)
        cache[key] = word  # the raw reading is cached; snapping happens on the way out
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=0))
        return snap_to_vocabulary(word, index, known) or None

    return read


def _rounded(b: Block) -> Block:
    return Block(b.x0, b.y0, b.x1, b.y1, b.font, float(round(b.size)), b.bold, b.italic, b.text, b.max_size)


def extract_chapter_ocr(pdf_path: Path) -> tuple[str, dict]:
    pages, width, conf = read_pages_ocr(pdf_path)
    md, meta = _render(pages[title_page_position(pages):], width)
    meta["ocr"] = True
    meta["ocr_confidence"] = round(conf, 1)
    return md, meta
