"""Render one JPEG per printed page for every edition, in the layout the site expects.

Output: <out>/<book>/<edition>/<chapter dir>/p<printed page>.webp, where the chapter dir is
"ch04" or "part1-ch04". The same layout is uploaded to object storage, so the site only
needs a base URL to find any page.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf
from PIL import Image

from datetime import date

from .. import MANIFEST_DIR, PDF_DIR, REPO_ROOT, TEXTS_DIR
from ..textparse import PAGE_MARKER

WIDTH_PX = 1200
WEBP_QUALITY = 72  # about half the size of a JPEG of the same look; every browser decodes it
COVER_WIDTH_PX = 480


def chapter_dir_name(part: int | None, number: int) -> str:
    return f"part{part}-ch{number:02d}" if part else f"ch{number:02d}"


def page_map(markdown_path: Path) -> list[tuple[int, int, str | None]]:
    """(printed page number, pdf page index (0-based), source file name or None) for every
    page marker in the chapter text. The source is set for pages carried over from a
    neighbouring chapter PDF."""
    out: list[tuple[int, int, str | None]] = []
    for line in markdown_path.read_text().splitlines():
        m = PAGE_MARKER.match(line)
        if m and m.group(1):
            out.append((int(m.group(1)), int(m.group(2)) - 1, m.group(3)))
    return out


def _label_date(label: str) -> date:
    m = re.match(r"^(?:live-)?(\d{4})-(\d{2})-(\d{2})", label)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else date.today()


def _is_title_page(pdf: Path) -> bool:
    """The first prelims page of the 2019 and later files reproduces the cover art with the
    book's title; the 2007-era prelims open with a contents page instead."""
    with pymupdf.open(pdf) as doc:
        if doc.page_count == 0:
            return False
        text = doc[0].get_text().lower()
    return "textbook" in text and "contents" not in text[:200]


def _save_webp(image: Image.Image, target: Path, width: int) -> None:
    scale = width / image.width
    image = image.convert("RGB").resize((width, round(image.height * scale)), Image.LANCZOS)
    image.save(target, "WEBP", quality=80, method=4)


def render_covers(book_id: str, out_root: Path, *, log=print, force: bool = False) -> int:
    """A cover thumbnail per edition at <out>/<book>/covers/<edition>.webp, plus book.webp.

    An edition whose prelims open with the title page gets that page rendered. Otherwise it
    gets NCERT's cover image (pdfs/<book>/covers/, fetched from the archive or the live site)
    nearest in date to the edition's capture. The book cover is the newest cover image."""
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    covers_dir = PDF_DIR / book_id / "covers"
    covers = sorted(covers_dir.glob("*.jpg")) if covers_dir.exists() else []
    target_dir = out_root / book_id / "covers"
    target_dir.mkdir(parents=True, exist_ok=True)
    written = 0

    def nearest_cover(label: str) -> Path | None:
        if not covers:
            return None
        when = _label_date(label)
        return min(covers, key=lambda c: abs((_label_date(c.stem) - when).days))

    for ed in data["editions"]:
        target = target_dir / f"{ed['id']}.webp"
        if target.exists() and not force:
            continue
        snap_dir = PDF_DIR / book_id / ed["snapshots"][0]
        prelims = next(iter(sorted(snap_dir.glob("*prelims.pdf"))), None)
        if prelims and _is_title_page(prelims):
            with pymupdf.open(prelims) as doc:
                pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), colorspace=pymupdf.csRGB)
                image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            _save_webp(image, target, COVER_WIDTH_PX)
            written += 1
            continue
        cover = nearest_cover(ed["snapshots"][0])
        if cover:
            _save_webp(Image.open(cover), target, COVER_WIDTH_PX)
            written += 1
        else:
            log(f"{book_id} / {ed['id']}: no cover source")
    book_target = target_dir / "book.webp"
    if covers and (force or not book_target.exists()):
        newest = max(covers, key=lambda c: _label_date(c.stem))
        _save_webp(Image.open(newest), book_target, COVER_WIDTH_PX)
        written += 1
    log(f"{book_id}: {written} cover images")
    return written


def render_book(book_id: str, out_root: Path, *, log=print, force: bool = False) -> int:
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    rendered = 0
    for ed in data["editions"]:
        for ch in ed["chapters"]:
            pdf = REPO_ROOT / ch["pdf"]
            target_dir = out_root / book_id / ed["id"] / chapter_dir_name(ch["part"], ch["number"])
            target_dir.mkdir(parents=True, exist_ok=True)
            docs: dict[str | None, pymupdf.Document] = {}
            try:
                # Pages before the chapter opener have no marker and are not rendered.
                for printed, index, source in page_map(REPO_ROOT / ch["file"]):
                    target = target_dir / f"p{printed:03d}.webp"
                    if target.exists() and not force:
                        continue
                    if source not in docs:
                        docs[source] = pymupdf.open(pdf.with_name(source) if source else pdf)
                    page = docs[source][index]
                    scale = WIDTH_PX / page.rect.width
                    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), colorspace=pymupdf.csRGB)
                    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(target, "WEBP", quality=WEBP_QUALITY, method=4)
                    rendered += 1
            finally:
                for doc in docs.values():
                    doc.close()
        log(f"{book_id} / {ed['id']}: pages rendered so far {rendered}")
    return rendered
