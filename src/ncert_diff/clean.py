"""Text normalisation for extracted spans, lines, and paragraphs."""

from __future__ import annotations

import re
import unicodedata

_WS = re.compile(r"[ \t ]+")
_SOFT_HYPHEN = "­"
_SENTENCE_END = re.compile(r"[.!?:;\"”’)\]…]$")
_BROKEN_HYPHEN = re.compile(r"(?<=[A-Za-z])- (?=[a-z])")
_LIST_ITEM = re.compile(r"^(\d{1,2}\.|\(?[a-z]\)|\(?[ivx]+\))\s")
# "1.that", "4.Within": the 2022-23 civics files set the space after a list number as a
# tab or a gap that the text layer loses. The printed page has "1. that".
_GLUED_LIST_LABEL = re.compile(r"^(\d{1,2}\.)(?=[^\W\d_])")
# The rupee font of the 2019 and later civics files maps "₹" to a backtick ("` 3,000",
# "` _______"). A backtick has no other use in the books.
_RUPEE = re.compile(r"`(?=\s*[\d_]|\s*$)")


def normalise_text(text: str) -> str:
    """NFC, drop soft hyphens, squeeze whitespace."""
    text = unicodedata.normalize("NFC", text).replace(_SOFT_HYPHEN, "")
    text = text.replace(" ", " ").replace(" ", " ")
    return _WS.sub(" ", text).strip()


def collapse_repeats(text: str) -> str:
    """'Map 1 Map 1 Map 1 Map 1 Map 1 Major kingdoms' -> 'Map 1 Major kingdoms'.

    NCERT's PDFs draw some decorative headings several times on top of each other
    for a shadow effect, which shows up in the text layer as a phrase repeated three
    or more times in a row. Any run of three or more identical n-grams (n up to 6)
    is reduced to one.
    """
    tokens = text.split(" ")
    changed = True
    while changed:
        changed = False
        for n in range(1, 7):
            i = 0
            while i + 3 * n <= len(tokens):
                gram = tokens[i : i + n]
                if gram == tokens[i + n : i + 2 * n] == tokens[i + 2 * n : i + 3 * n]:
                    j = i + n
                    while tokens[j : j + n] == gram:
                        j += n
                    del tokens[i + n : j]
                    changed = True
                i += 1
    return " ".join(tokens)


def join_lines(lines: list[str]) -> str:
    """Join the lines of one block into a paragraph.

    NCERT's PDFs are set without automatic hyphenation, so a hyphen at the end of a
    line is a real one ("great-great-" / "grandfather", "1526-" / "1530"). It is kept
    and the next line is attached to it without a space.
    """
    out = ""
    for line in lines:
        line = _RUPEE.sub("₹", _GLUED_LIST_LABEL.sub(r"\1 ", normalise_text(line)))
        if not line:
            continue
        if not out:
            out = line
            continue
        if line[0] in ".,;:!?)":
            out += line  # a fragment left after a shadowed word was cut away: ". The"
            continue
        out = merge_paragraphs(out, line)
    return collapse_repeats(_BROKEN_HYPHEN.sub("-", out))


def ends_sentence(text: str) -> bool:
    return bool(_SENTENCE_END.search(text))


def continues(prev: str, nxt: str) -> bool:
    """Does `nxt` look like the continuation of paragraph `prev`?

    A paragraph that stops without end punctuation was cut by a page break, a figure,
    or a column boundary. Short unpunctuated lines are labels, so they are left alone
    unless the next piece starts in lower case.
    """
    if not prev or not nxt:
        return False
    if _SENTENCE_END.search(prev) or _LIST_ITEM.match(nxt):
        return False
    first = nxt[0]
    if first.islower() or first in ",;" or (prev.endswith("-") and first.isalnum()):
        return True
    if prev.startswith("- ") and first.isupper():
        # A list item carries no closing punctuation, so a capitalised paragraph after the
        # last item is a new paragraph ("- The decline of crafts" then "On the basis of ...").
        return False
    if prev[-1].isdigit() and first.isupper():
        # "Grand Total 543" then "Once elected, these candidates..." is a table read as body
        # text followed by a new paragraph, not a sentence cut by the page break.
        return False
    return len(prev) > 40 and first.isalnum()


def has_content(text: str) -> bool:
    return any(ch.isalnum() for ch in text)


def merge_paragraphs(prev: str, nxt: str) -> str:
    if prev.endswith("-") and len(prev) > 1 and prev[-2].isalnum() and nxt[:1].isalnum():
        return prev + nxt
    return f"{prev} {nxt}"


def slugify(title: str, max_len: int = 48) -> str:
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:max_len].rstrip("-") or "untitled"
