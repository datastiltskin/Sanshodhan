"""Words in the extracted texts that no dictionary and no other edition knows.

Usage: uv run python scripts/spellcheck.py [<book> [<edition>]] [--all]

An extraction fault usually leaves a word that exists nowhere else: an OCR misreading
("Błack", "rosecution"), two words glued ("QImagine"), a word cut in two ("empire" and "es"),
or a word doubled by a shadow line ("India India"). A word is taken as known when the
pyspellchecker dictionary or the system word list has it (or its stem, or its American
spelling), when a hand-kept list accepts it (scripts/spelling-accept.txt, one word per line),
or when at least two editions, of any book, use it. That last rule lets
the books vouch for their own transliterations and names ("muqtis", "Kaṇiṣhka"), so what is
left is mostly worth a look. A word the source itself misspells will also show up. The page
image decides which it is (docs/verification.md): a fault in the source is accepted into the
list, a fault in the extraction gets a rule or an override.

The report groups by book, edition and chapter, and gives the printed page and the sentence
around each word. By default it prints the words most likely to be faults: lower-case words
in plain letters, doubled words, and words with a capital letter inside. --names adds
capitalised words (mostly people and places the dictionary lacks), --diacritics adds words
with transliteration marks (one edition's "Kaṇiṣhka" cannot be vouched for), and --all adds
both plus the words the edition uses three times or more, since a real name recurs where a
misreading mostly does not. British spellings are accepted through their American forms.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ncert_diff import TEXTS_DIR  # noqa: E402
from ncert_diff.textparse import parse_chapter  # noqa: E402

WORDS = Path("/usr/share/dict/words")
ACCEPT = Path(__file__).with_name("spelling-accept.txt")
LETTER = r"A-Za-zÀ-ɏḀ-ỿ"
WORD = re.compile(rf"[{LETTER}][{LETTER}’']*")
DOUBLED = re.compile(rf"\b([{LETTER}]{{3,}}) \1\b")
GLUED = re.compile(rf"[a-z][A-Z][a-z]")  # "QImagine", "theMughals"
SUFFIXES = ("s", "es", "ed", "d", "ing", "ly", "er", "est", "'s", "’s")
BRITISH = (("isation", "ization"), ("ising", "izing"), ("ised", "ized"), ("ises", "izes"), ("ise", "ize"),
           ("yse", "yze"), ("ysed", "yzed"), ("our", "or"), ("ours", "ors"), ("tre", "ter"), ("tres", "ters"),
           ("ogue", "og"), ("ogues", "ogs"), ("ence", "ense"), ("lled", "led"), ("lling", "ling"))


def dictionary() -> set[str]:
    words = {w.strip().lower() for w in WORDS.read_text(errors="ignore").splitlines()} if WORDS.exists() else set()
    try:
        from spellchecker import SpellChecker

        words |= set(SpellChecker(language="en").word_frequency.dictionary)
    except ImportError:
        pass
    if ACCEPT.exists():
        words |= {w.strip().lower() for w in ACCEPT.read_text().splitlines() if w.strip() and not w.startswith("#")}
    return words


def known(word: str, dic: set[str]) -> bool:
    w = word.lower().strip("’'")
    if len(w) <= 1:
        return True
    forms = [w] + [w[: -len(brit)] + amer for brit, amer in BRITISH if w.endswith(brit)]
    for form in forms:
        if form in dic:
            return True
        for suf in SUFFIXES:
            if form.endswith(suf):
                stem = form[: -len(suf)]
                if stem in dic or stem + "e" in dic or (stem.endswith("i") and stem[:-1] + "y" in dic):
                    return True
                if len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in dic:  # "running" -> "run"
                    return True
    return False


def tokens(text: str) -> list[str]:
    return [t for piece in WORD.findall(text) for t in piece.split("-") if t]


def edition_units(book: str, edition: str) -> list[tuple[str, int | None, str]]:
    """(chapter file name, printed page, unit text) for every unit of an edition, tagged blocks included."""
    out = []
    for md in sorted((TEXTS_DIR / book / edition).glob("*.md")):
        _, units = parse_chapter(md.read_text())
        for u in units:
            out.append((md.name, u.page, u.text))
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all" in sys.argv
    show_names = show_all or "--names" in sys.argv
    show_marks = show_all or "--diacritics" in sys.argv
    books = [args[0]] if args else sorted(p.name for p in TEXTS_DIR.iterdir() if p.is_dir())
    only_edition = args[1] if len(args) > 1 else None
    dic = dictionary()

    # Every edition of every book votes for the words it uses, so a word two editions share
    # is known even when it is in no dictionary.
    editions: dict[tuple[str, str], list[tuple[str, int | None, str]]] = {}
    for book_dir in sorted(p for p in TEXTS_DIR.iterdir() if p.is_dir()):
        for ed_dir in sorted(p for p in book_dir.iterdir() if p.is_dir()):
            editions[(book_dir.name, ed_dir.name)] = edition_units(book_dir.name, ed_dir.name)
    votes: Counter[str] = Counter()
    for units in editions.values():
        votes.update({t.lower() for _, _, text in units for t in tokens(text)})

    total = 0
    recurring: list[str] = []
    hidden = Counter()
    for (book, edition), units in editions.items():
        if book not in books or (only_edition and edition != only_edition):
            continue
        counts = Counter(t.lower() for _, _, text in units for t in tokens(text))
        findings: dict[str, list[tuple[int | None, str, str]]] = defaultdict(list)  # chapter -> (page, word, context)
        seen: set[tuple[str, str]] = set()
        for chapter, page, text in units:
            for t in tokens(text):
                low = t.lower()
                if known(t, dic) or votes[low] >= 2:
                    continue
                if (chapter, low) in seen:
                    continue
                seen.add((chapter, low))
                entry = (page, t, text[:110])
                if counts[low] >= 3:
                    recurring.append(f"  {book} / {edition} / {chapter} p{page}: {t} (x{counts[low]})  {text[:80]}")
                elif not t.isascii() and not show_marks:
                    hidden["diacritics"] += 1
                elif t[0].isupper() and not show_names:
                    hidden["names"] += 1
                else:
                    findings[chapter].append(entry)
            for m in DOUBLED.finditer(text):
                findings[chapter].append((page, f"doubled: {m.group(0)}", text[:110]))
            for m in GLUED.finditer(text):
                word = next((t for t in tokens(text) if m.group(0) in t), m.group(0))
                if not known(word, dic) and votes[word.lower()] < 2 and (chapter, "glued:" + word) not in seen:
                    seen.add((chapter, "glued:" + word))
                    findings[chapter].append((page, f"glued: {word}", text[:110]))
        if not findings:
            continue
        print(f"\n== {book} / {edition}")
        for chapter in sorted(findings):
            print(f"  -- {chapter}")
            for page, word, context in sorted(findings[chapter], key=lambda e: (e[0] or 0, e[1])):
                print(f"     p{page}: {word}  |  {context}")
                total += 1
    if show_all and recurring:
        print("\n== used three times or more in one edition, known nowhere else")
        print("\n".join(recurring))
    note = ", ".join(f"{n} {k}" for k, n in hidden.items()) + (f", {len(recurring)} recurring" if recurring and not show_all else "")
    print(f"\n{total} words to look at" + (f" (hidden: {note}. --names, --diacritics, --all)" if note else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
