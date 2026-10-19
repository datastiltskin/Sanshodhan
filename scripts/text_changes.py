"""List the sentences that changed in an edition's texts since the last commit.

Usage: uv run python scripts/text_changes.py <book> [<edition>]

A rule or OCR change re-makes texts, and every sentence it altered must be checked against
the page images before the texts are committed (docs/verification.md). This prints, per
chapter and printed page, the sentences that are in the working tree but not in HEAD and
the reverse, so a reviewer can open exactly those pages. Markers, section lines and role
tags are ignored, so a re-flowed paragraph with the same sentences prints nothing.
"""

from __future__ import annotations

import difflib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ncert_diff import TEXTS_DIR  # noqa: E402
from ncert_diff.textparse import PAGE_MARKER, parse_chapter  # noqa: E402


def sentences(markdown: str) -> dict[str, int | None]:
    """sentence text -> printed page, for the body of a chapter text."""
    out: dict[str, int | None] = {}
    _, units = parse_chapter(markdown)
    for u in units:
        out.setdefault(u.text, u.page)
    return out


def committed(path: Path) -> str | None:
    rel = path.relative_to(Path(__file__).resolve().parents[1])
    proc = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    book = sys.argv[1]
    editions = [sys.argv[2]] if len(sys.argv) > 2 else sorted(p.name for p in (TEXTS_DIR / book).iterdir() if p.is_dir())
    total = 0
    for edition in editions:
        for md in sorted((TEXTS_DIR / book / edition).glob("*.md")):
            now = sentences(md.read_text())
            before_text = committed(md)
            before = sentences(before_text) if before_text else {}
            gone = [(before[s], s) for s in before if s not in now]
            new = [(now[s], s) for s in now if s not in before]
            if not gone and not new:
                continue
            # A removed sentence with a near-identical added one is a rewording of the
            # extraction (a join, a split, a reread word): shown as one "~" line so the
            # reviewer sees what changed. The rest are losses ("-") and gains ("+").
            paired = []
            new_left = list(new)
            for page, s in sorted(gone, key=lambda t: (t[0] or 0, t[1])):
                best = max(new_left, key=lambda t: difflib.SequenceMatcher(None, s, t[1]).ratio(), default=None)
                if best and difflib.SequenceMatcher(None, s, best[1]).ratio() >= 0.75:
                    new_left.remove(best)
                    paired.append((page, s, best[1]))
                else:
                    paired.append((page, s, None))
            print(f"\n== {book} / {edition} / {md.name}" + ("  (new file)" if before_text is None else ""))
            for page, s, t in paired:
                if t is None:
                    print(f"  - p{page}: {s[:160]}")
                else:
                    print(f"  ~ p{page}: {s[:120]}")
                    print(f"      -> {t[:120]}")
            for page, s in sorted(new_left, key=lambda t: (t[0] or 0, t[1])):
                print(f"  + p{page}: {s[:160]}")
            total += len(paired) + len(new_left)
    print(f"\n{total} changed sentences" if total else "no changed sentences")
    return 0


if __name__ == "__main__":
    sys.exit(main())
