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


def _rounded(b: Block) -> Block:
    return Block(b.x0, b.y0, b.x1, b.y1, b.font, float(round(b.size)), b.bold, b.italic, b.text, b.max_size)


def extract_chapter_ocr(pdf_path: Path) -> tuple[str, dict]:
    pages, width, conf = read_pages_ocr(pdf_path)
    md, meta = _render(pages[title_page_position(pages):], width)
    meta["ocr"] = True
    meta["ocr_confidence"] = round(conf, 1)
    return md, meta
