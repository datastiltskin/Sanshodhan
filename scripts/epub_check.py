"""Check an edition's extracted text against NCERT's ePub of the same printing.

Usage: uv run python scripts/epub_check.py <book> [<edition>] [--roles] [--all]

The ePubs under pdfs/_epub/2016-epathshala/ (one bundle per book, one ePub per chapter) are
reflowable XHTML from the same InDesign files as the PDFs, so they carry the same text with
each paragraph's role in a class name. That makes them an oracle for the extractor: a
sentence the ePub has and the extracted text lacks was lost, one the extracted text has and
the ePub lacks is junk or a layout fault, and one both have under different roles is a
misclassification. The edition compared is the one whose sentences overlap the ePub most,
unless given. Matching ignores spaces and punctuation, because the ePub export leaves stray
spaces inside words ("discon tinuity") and the two carry quotes differently.

Roles come from the class names, which differ by book (docs/sources.md, "ePubs"), with the
stylesheet's sizes and weights as a fallback for generic names. By default the report lists
lost and junk sentences per chapter; --roles adds the role disagreements, --all adds every
unmatched short fragment too.
"""

from __future__ import annotations

import collections
import difflib
import io
from html.parser import HTMLParser
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ncert_diff import PDF_DIR, TEXTS_DIR  # noqa: E402
from ncert_diff.textparse import parse_chapter, split_sentences  # noqa: E402

EPUB_DIR = PDF_DIR / "_epub" / "2016-epathshala"
BUNDLES = {  # book id -> bundle file names (Our Pasts III was two parts in 2016)
    "our-pasts-3": ["our-pasts-3-part1.epub", "our-pasts-3-part2.epub"],
}
ROLE_WORDS = [  # order matters: first match wins
    (r"caption|credit|fig", "caption"),
    (r"exercise|excercise|question|qestion|let.?s|recall|discuss", "exercises"),
    (r"glossary|newword|new-word|definition|orange|keyword|concept", "note"),
    (r"box|activity|imagine|elsewhere|source|quote|ai-", "note"),
    (r"chapterhead|chapter_head|chaptertitle|chapter-title", "h1"),
    (r"head|heading|subhead|topic|title", "heading"),
    (r"table|td", "table"),
    (r"body|fpara|para|text|indent|normal|basic", "body"),
]
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "li", "td", "th", "blockquote", "section", "aside", "figcaption"}


def key(text: str) -> str:
    """Spaces and punctuation out, so 'discon tinuity' and 'discontinuity' agree."""
    return re.sub(r"[\W_]+", "", text).lower()


def stylesheet_roles(css: str) -> dict[str, str]:
    """Class -> role from font size and weight, for stylesheets with generic class names."""
    roles: dict[str, str] = {}
    for name, body in re.findall(r"\.([A-Za-z0-9_-]+)\s*\{([^}]*)\}", css):
        size = re.search(r"font-size\s*:\s*([\d.]+)\s*(%|em|pt|px)?", body)
        bold = "bold" in body or re.search(r"font-weight\s*:\s*[6-9]00", body) is not None
        big = False
        if size:
            n, unit = float(size.group(1)), size.group(2) or ""
            big = (unit == "%" and n >= 115) or (unit == "em" and n >= 1.15) or (unit in ("pt", "px") and n >= 14)
        if big or (bold and size is None):
            roles[name] = "heading"
    return roles


def role_of(tag: str, classes: list[str], css_roles: dict[str, str]) -> str | None:
    """The role a tag and its classes name, or None when they say nothing."""
    if tag in HEADING_TAGS:
        return "heading"
    for cls in classes:
        low = cls.lower()
        for pattern, role in ROLE_WORDS:
            if re.search(pattern, low):
                return role
    for cls in classes:
        if cls in css_roles:
            return css_roles[cls]
    return None


class _Blocks(HTMLParser):
    """Collects the text of every leaf block element with the role of the nearest element
    (itself or an ancestor) whose class says what it is."""

    def __init__(self, css_roles: dict[str, str]):
        super().__init__(convert_charrefs=True)
        self.css_roles = css_roles
        self.stack: list[tuple[str, str | None, list[str]]] = []  # (tag, role, text parts)
        self.units: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        if tag not in BLOCK_TAGS:
            if tag == "br" and self.stack:
                self.stack[-1][2].append(" ")
            return
        classes = (dict(attrs).get("class") or "").split()
        role = role_of(tag, classes, self.css_roles)
        if role is None:
            role = next((r for _, r, _ in reversed(self.stack) if r), None)
        self.stack.append((tag, role, []))

    def handle_endtag(self, tag):
        if tag not in BLOCK_TAGS or not self.stack:
            return
        # close the innermost open element of this tag (the export's markup is well formed)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, role, parts = self.stack.pop(i)
                text = re.sub(r"\s+", " ", "".join(parts)).strip()
                if len(text) >= 2:
                    text = re.sub(r"^([A-Z]) (?=[a-z])", r"\1", text)  # a drop cap set apart: "T ake"
                    self.units.append((role or "body", text))
                break

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][2].append(data)


def epub_units(bundle: Path) -> dict[int, list[tuple[str, str]]]:
    """chapter number -> [(role, paragraph text)] from one bundle, leaf blocks only."""
    outer = zipfile.ZipFile(bundle)
    chapters: dict[int, list[tuple[str, str]]] = {}
    for name in outer.namelist():
        m = re.search(r"_(\d+)\.epub$", name)
        if not m:
            continue
        inner = zipfile.ZipFile(io.BytesIO(outer.read(name)))
        css = "".join(inner.read(n).decode("utf-8", "replace") for n in inner.namelist() if n.endswith(".css"))
        parser = _Blocks(stylesheet_roles(css))
        for n in inner.namelist():
            if n.lower().endswith((".xhtml", ".html", ".htm")) and "cover" not in n.lower():
                parser.feed(inner.read(n).decode("utf-8", "replace"))
        chapters[int(m.group(1))] = parser.units
    return chapters


def our_units(book: str, edition: str) -> dict[int, list]:
    out: dict[int, list] = {}
    for md in sorted((TEXTS_DIR / book / edition).glob("*.md")):
        m = re.match(r"(?:part\d-)?(\d+)-", md.name)
        if not m:
            continue
        _, units = parse_chapter(md.read_text())
        out[int(m.group(1))] = units
    return out


def best_edition(book: str, epub: dict[int, list[tuple[str, str]]]) -> str:
    keys = {key(s) for units in epub.values() for _, t in units for s in split_sentences(t) if len(s) > 30}
    best, score = "", -1.0
    for d in sorted(p for p in (TEXTS_DIR / book).iterdir() if p.is_dir()):
        ours = {key(u.text) for units in our_units(book, d.name).values() for u in units if len(u.text) > 30}
        overlap = len(keys & ours) / max(1, len(keys))
        if overlap > score:
            best, score = d.name, overlap
    return best


CONVERTER_NOTE = re.compile(r"ePub conversion was done by")  # SASTRA University's credit line, in the ePub only


def _pair_variants(lost: list, junk: list) -> tuple[list, list, list]:
    """Pull out of `lost` and `junk` the pairs that are the same sentence in different words."""
    differs: list = []
    used: set[int] = set()
    still_lost = []
    for e in lost:
        ek = key(e[1])
        best, ratio = None, 0.0
        for i, o in enumerate(junk):
            if i in used:
                continue
            r = difflib.SequenceMatcher(None, ek, key(o[1])).ratio()
            if r > ratio:
                best, ratio = i, r
        if best is not None and ratio >= 0.75:
            used.add(best)
            differs.append((e, junk[best]))
        else:
            still_lost.append(e)
    return still_lost, [o for i, o in enumerate(junk) if i not in used], differs


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    book = args[0]
    show_roles, show_all = "--roles" in sys.argv, "--all" in sys.argv
    bundles = BUNDLES.get(book, [f"{book}.epub"])
    epub: dict[int, list[tuple[str, str]]] = {}
    offset = 0
    for b in bundles:
        part = epub_units(EPUB_DIR / b)
        for n, units in part.items():
            epub[n + offset] = units
        offset += max(part) if part else 0  # Our Pasts III part 2 restarts at chapter 1
    edition = args[1] if len(args) > 1 else best_edition(book, epub)
    ours = our_units(book, edition)
    print(f"{book}: ePub (2015-16) against edition {edition}")
    totals = collections.Counter()
    for number in sorted(epub):
        if number not in ours:
            print(f"\n== chapter {number}: not in our edition")
            continue
        e_sent: dict[str, tuple[str, str]] = {}
        for role, text in epub[number]:
            for s in split_sentences(text):
                e_sent.setdefault(key(s), (role, s))
        o_sent: dict[str, tuple[str, str, int | str | None]] = {}  # page is "pdfN" when the printing has no page numbers
        for u in ours[number]:
            r = "exercises" if u.section == "exercises" else "note" if u.section in ("glossary", "teachers-note") else u.role
            for s in split_sentences(u.text):
                o_sent.setdefault(key(s), (r, s, u.page if u.page is not None else f"df{u.pdf_page}"))
        e_all = "".join(key(t) for _, t in epub[number])
        o_all = "".join(key(u.text) for u in ours[number])
        lost = [v for k, v in e_sent.items() if k not in o_sent and k not in o_all and (show_all or len(v[1]) > 25) and not CONVERTER_NOTE.search(v[1])]
        junk = [v for k, v in o_sent.items() if k not in e_sent and k not in e_all and (show_all or len(v[1]) > 25)]
        # A sentence the other side has in slightly different words is a wording difference
        # between the ePub's printing and ours, or a stray space, not a lost sentence.
        lost, junk, differs = _pair_variants(lost, junk)
        roles = [(e_sent[k][0], o_sent[k][0], o_sent[k][1], o_sent[k][2]) for k in e_sent if k in o_sent and e_sent[k][0] != o_sent[k][0]
                 and {e_sent[k][0], o_sent[k][0]} not in ({"heading", "h1"},)]
        totals.update({"lost": len(lost), "junk": len(junk), "differs": len(differs), "roles": len(roles), "matched": len(set(e_sent) & set(o_sent))})
        if not lost and not junk and not (show_roles and roles) and not (show_all and differs):
            continue
        print(f"\n== chapter {number}: {len(set(e_sent) & set(o_sent))} sentences in both, {len(lost)} in the ePub only, {len(junk)} in our text only, {len(differs)} worded differently, {len(roles)} role disagreements")
        if show_all:
            for (er, es), (orole, os_, page) in differs:
                print(f"   differs p{page}: ePub: {es[:100]}\n                  ours: {os_[:100]}")
        for role, s in lost:
            print(f"   ePub only [{role}]: {s[:140]}")
        for role, s, page in junk:
            print(f"   ours only [{role}] p{page}: {s[:140]}")
        if show_roles:
            for er, orole, s, page in roles:
                print(f"   role ePub={er} ours={orole} p{page}: {s[:110]}")
    print(f"\nmatched {totals['matched']}, ePub only {totals['lost']}, ours only {totals['junk']}, worded differently {totals['differs']}, role disagreements {totals['roles']}" + ("" if show_roles else " (--roles lists them, --all the wording differences)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
