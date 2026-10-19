"""Second reading of a page by a local OCR model, diffed against the extracted text.

Usage: uv run python scripts/ocr_check.py <book> <edition> <chapter number> [printed pages...]

Renders each printed page of the chapter at 150 dpi, has the glm-ocr model running under
Ollama (http://localhost:11434) read it, and prints the words that only one of the two
readings has. The model reads the main text column well and ignores margin boxes and page
furniture, so a word only in our text is usually a box; a word only in the model's reading
is where to open the page image (docs/verification.md). About 15 seconds a page, cached under
pdfs/<book>/<snapshot>/ocr/glm-pNNN.md, so this is for flagged pages, not the build.
"""

from __future__ import annotations

import base64
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pymupdf  # noqa: E402

from ncert_diff import MANIFEST_DIR, REPO_ROOT, TEXTS_DIR  # noqa: E402
from ncert_diff.textparse import PAGE_MARKER, parse_chapter  # noqa: E402

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "glm-ocr"
DPI = 150
WORD = re.compile(r"[A-Za-zÀ-ɏ][A-Za-zÀ-ɏ’'-]*|\d[\d,.]*")


def ocr_page(pdf: Path, index: int, cache: Path) -> str:
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        return cache.read_text()
    with pymupdf.open(pdf) as doc:
        png = doc[index].get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB).tobytes("png")
    payload = {
        "model": MODEL, "stream": False, "think": False,
        "options": {"num_ctx": 8192, "num_predict": 2048, "temperature": 0},
        "messages": [{"role": "user", "content": "Text Recognition:", "images": [base64.b64encode(png).decode()]}],
    }
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        text = json.load(resp)["message"]["content"]
    cache.write_text(text)
    return text


def words(text: str) -> Counter:
    return Counter(w.lower().strip("’'-") for w in WORD.findall(text))


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    book, edition, number = sys.argv[1], sys.argv[2], int(sys.argv[3])
    only = {int(p) for p in sys.argv[4:]}
    md = next(iter(sorted((TEXTS_DIR / book / edition).glob(f"{number:02d}-*.md"))), None)
    if md is None:
        print(f"no chapter {number} in {book}/{edition}")
        return 1
    meta, units = parse_chapter(md.read_text())
    pdf = REPO_ROOT / meta["source_pdf"]
    pages: dict[int, tuple[Path, int]] = {}  # printed page -> (pdf, 0-based index)
    for line in md.read_text().splitlines():
        m = PAGE_MARKER.match(line)
        if m and m.group(1):
            source = pdf.with_name(m.group(3)) if m.group(3) else pdf
            pages[int(m.group(1))] = (source, int(m.group(2)) - 1)
    total = 0
    for printed, (source, index) in sorted(pages.items()):
        if only and printed not in only:
            continue
        # The model reads the main text column only, so boxes, captions and tables are left
        # out of our side too; what remains is the body text and its headings.
        ours = " ".join(u.text for u in units if u.page == printed and u.role in ("body", "heading") and not u.section)
        theirs = ocr_page(source, index, source.parent / "ocr" / f"{source.stem}-glm-p{index + 1:03d}.md")
        a, b = words(ours), words(theirs)
        only_ours = sorted((a - b).elements())
        only_theirs = sorted((b - a).elements())
        total += len(only_ours) + len(only_theirs)
        print(f"\n== {book} / {edition} / chapter {number} / page {printed}  ({len(a)} words in our text, {len(b)} in the model's)")
        if only_ours:
            print("  only in our text:   " + " ".join(only_ours)[:400])
        if only_theirs:
            print("  only in the model:  " + " ".join(only_theirs)[:400])
        if not only_ours and not only_theirs:
            print("  identical word sets")
    print(f"\n{total} differing words" if total else "\nno differing words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
