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

from .. import MANIFEST_DIR, REPO_ROOT, TEXTS_DIR
from ..textparse import PAGE_MARKER

WIDTH_PX = 1200
WEBP_QUALITY = 72  # about half the size of a JPEG of the same look; every browser decodes it


def chapter_dir_name(part: int | None, number: int) -> str:
    return f"part{part}-ch{number:02d}" if part else f"ch{number:02d}"


def page_map(markdown_path: Path) -> dict[int, int]:
    """pdf page index (0-based) -> printed page number, from the chapter's page markers."""
    out: dict[int, int] = {}
    for line in markdown_path.read_text().splitlines():
        m = PAGE_MARKER.match(line)
        if m and m.group(1):
            out[int(m.group(2)) - 1] = int(m.group(1))
    return out


def render_book(book_id: str, out_root: Path, *, log=print, force: bool = False) -> int:
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    rendered = 0
    for ed in data["editions"]:
        for ch in ed["chapters"]:
            pdf = REPO_ROOT / ch["pdf"]
            target_dir = out_root / book_id / ed["id"] / chapter_dir_name(ch["part"], ch["number"])
            target_dir.mkdir(parents=True, exist_ok=True)
            mapping = page_map(REPO_ROOT / ch["file"])
            with pymupdf.open(pdf) as doc:
                for index in range(doc.page_count):
                    printed = mapping.get(index)
                    if printed is None:
                        continue  # a page before the chapter opener, not part of the text
                    target = target_dir / f"p{printed:03d}.webp"
                    if target.exists() and not force:
                        continue
                    page = doc[index]
                    scale = WIDTH_PX / page.rect.width
                    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), colorspace=pymupdf.csRGB)
                    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(target, "WEBP", quality=WEBP_QUALITY, method=4)
                    rendered += 1
        log(f"{book_id} / {ed['id']}: pages rendered so far {rendered}")
    return rendered
