"""Compare two editions of a book: which chapters survive, and what changed inside them.

Chapters are paired by shared sentences, not by number, because the 2023 rationalisation
renumbered everything. Inside a chapter pair, every stream (body sentences, headings, notes,
captions, tables, sources) is aligned with difflib on normalised keys. Runs that difflib
cannot match exactly are paired fuzzily so that a reworded sentence shows as one "modified"
hunk with a word-level diff rather than a deletion plus an insertion. Sentences that merely
moved, or differ only in case, dashes, or quotes, are kept out of the way.
"""

from __future__ import annotations

import difflib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import MANIFEST_DIR, REPO_ROOT
from .extract import UNREADABLE
from .textparse import Unit, normalise_key, parse_chapter

DIFF_DIR = REPO_ROOT / "diffs"
STREAMS = ("heading", "body", "note", "caption", "table", "source", "exercises", "glossary", "references", "teachers-note")
# Streams whose order carries no meaning: table cells arrive in layout order, and exercise
# questions and glossary entries get renumbered and reflowed between printings.
ORDERLESS = ("table", "exercises", "glossary", "references")
SURVIVED = ("equal", "typographic", "punctuation", "modified", "moved", "restreamed")
PAGE_MIN_SENTENCES = 4  # a page with fewer comparable sentences is not judged
PAGE_SUSPECT = 0.5  # below this share of surviving sentences a page needs a look
CHAPTER_MATCH_MIN = 0.2  # share of sentences two chapters must have in common to be the same chapter
PAIR_MIN = 0.55  # similarity for two unmatched sentences to count as one reworded sentence


@dataclass
class Hunk:
    type: str  # inserted | deleted | modified | moved | typographic
    stream: str
    similarity: float | None = None
    old: str | None = None
    new: str | None = None
    old_page: int | None = None
    new_page: int | None = None
    words: list[list[str]] = field(default_factory=list)  # [op, token] with op in "=", "-", "+"
    old_pos: int | None = None  # index of the unit within its stream, old edition
    new_pos: int | None = None


def word_diff(a: str, b: str) -> list[list[str]]:
    ta, tb = a.split(), b.split()
    out: list[list[str]] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if tag == "equal":
            out.append(["=", " ".join(ta[i1:i2])])
        else:
            if i2 > i1:
                out.append(["-", " ".join(ta[i1:i2])])
            if j2 > j1:
                out.append(["+", " ".join(tb[j1:j2])])
    return out


_PUNCT = re.compile(r"[^\w\s]+", re.UNICODE)


def punctuation_only(words: list[list[str]]) -> bool:
    """True when every removed and added token differs only in punctuation or spacing."""
    removed = " ".join(t for op, t in words if op == "-")
    added = " ".join(t for op, t in words if op == "+")
    strip = lambda s: re.sub(r"\s+", " ", _PUNCT.sub("", s)).strip().lower()  # noqa: E731
    return strip(removed) == strip(added)


def _similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def _pair_fuzzy(old: list[Unit], new: list[Unit]) -> tuple[list[tuple[Unit, Unit, float]], list[Unit], list[Unit]]:
    """Greedy best-first pairing of two runs of unmatched units."""
    cands = []
    for i, u in enumerate(old):
        for j, v in enumerate(new):
            if abs(len(u.key) - len(v.key)) > 0.6 * max(len(u.key), len(v.key), 1):
                continue
            r = _similarity(u.key, v.key)
            if r >= PAIR_MIN:
                cands.append((r, i, j))
    cands.sort(reverse=True)
    used_i: set[int] = set()
    used_j: set[int] = set()
    pairs = []
    for r, i, j in cands:
        if i in used_i or j in used_j:
            continue
        used_i.add(i)
        used_j.add(j)
        pairs.append((old[i], new[j], r))
    rest_old = [u for i, u in enumerate(old) if i not in used_i]
    rest_new = [v for j, v in enumerate(new) if j not in used_j]
    return pairs, rest_old, rest_new


def diff_stream(old: list[Unit], new: list[Unit], stream: str) -> list[Hunk]:
    """Hunks between two unit sequences. Every hunk records the unit positions it refers to,
    and "equal" pairs are recorded too (type "equal", not reported) so a viewer can place
    deletions next to the surviving text."""
    hunks: list[Hunk] = []
    pos_old = {id(u): i for i, u in enumerate(old)}
    pos_new = {id(v): j for j, v in enumerate(new)}
    if stream in ORDERLESS:
        old = sorted(old, key=lambda u: u.key)
        new = sorted(new, key=lambda u: u.key)
    a = [u.key for u in old]
    b = [v.key for v in new]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    deleted: list[Unit] = []
    inserted: list[Unit] = []

    def H(type_: str, u: Unit | None, v: Unit | None, sim: float | None = None, words: list | None = None) -> Hunk:
        return Hunk(type_, stream, sim, u.text if u else None, v.text if v else None, u.page if u else None, v.page if v else None,
                    words or [], pos_old.get(id(u)) if u else None, pos_new.get(id(v)) if v else None)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            # Same key, possibly different surface form (case, dashes, quotes).
            for u, v in zip(old[i1:i2], new[j1:j2]):
                hunks.append(H("typographic" if u.text != v.text else "equal", u, v, 1.0))
            continue
        run_old, run_new = old[i1:i2], new[j1:j2]
        pairs, rest_old, rest_new = _pair_fuzzy(run_old, run_new)
        for u, v, r in pairs:
            hunks.append(H("modified", u, v, round(r, 3), word_diff(u.text, v.text)))
        deleted.extend(rest_old)
        inserted.extend(rest_new)
    # A sentence deleted here and inserted elsewhere just moved.
    ins_by_key: dict[str, list[Unit]] = {}
    for v in inserted:
        ins_by_key.setdefault(v.key, []).append(v)
    for u in deleted:
        if u.key in ins_by_key and ins_by_key[u.key]:
            v = ins_by_key[u.key].pop(0)
            hunks.append(H("moved", u, v, 1.0))
            continue
        hunks.append(H("deleted", u, None))
    for key, vs in ins_by_key.items():
        for v in vs:
            hunks.append(H("inserted", None, v))
    # Second pass: reworded sentences that difflib placed in different runs.
    dels = [h for h in hunks if h.type == "deleted"]
    inss = [h for h in hunks if h.type == "inserted"]
    if dels and inss:
        pairs, _, _ = _pair_fuzzy(
            [Unit(stream, h.old, h.old_page, None, 0) for h in dels],
            [Unit(stream, h.new, h.new_page, None, 0) for h in inss],
        )
        for u, v, r in pairs:
            hd = next(h for h in hunks if h.type == "deleted" and h.old == u.text)
            hi = next(h for h in hunks if h.type == "inserted" and h.new == v.text)
            hunks = [h for h in hunks if h is not hd and h is not hi]
            hunks.append(Hunk("modified", stream, round(r, 3), u.text, v.text, u.page, v.page, word_diff(u.text, v.text), hd.old_pos, hi.new_pos))
    for h in hunks:
        if (h.old and UNREADABLE in h.old) or (h.new and UNREADABLE in h.new):
            h.type = "unreadable"
        elif h.type == "modified" and h.words and punctuation_only(h.words):
            h.type = "punctuation"
    order = {"deleted": 0, "modified": 1, "inserted": 2, "moved": 3, "typographic": 4, "unreadable": 5, "punctuation": 6, "equal": 7}
    hunks.sort(key=lambda h: (h.old_page or h.new_page or 0, order[h.type]))
    return hunks


@dataclass
class ChapterText:
    number: int
    part: int | None
    title: str | None
    file: str
    units: list[Unit]

    @property
    def body_keys(self) -> set[str]:
        return {u.key for u in self.units if u.stream == "body" and len(u.key) > 30}


def load_edition(book_id: str, edition_id: str) -> tuple[dict, list[ChapterText]]:
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    ed = next(e for e in data["editions"] if e["id"] == edition_id)
    chapters = []
    for ch in ed["chapters"]:
        _, units = parse_chapter((REPO_ROOT / ch["file"]).read_text())
        chapters.append(ChapterText(ch["number"], ch["part"], ch["title"], ch["file"], units))
    return ed, chapters


def align_chapters(old: list[ChapterText], new: list[ChapterText]) -> list[tuple[ChapterText | None, ChapterText | None, float]]:
    """Pair chapters by the share of body sentences they have in common."""
    scores = []
    for i, a in enumerate(old):
        for j, b in enumerate(new):
            ka, kb = a.body_keys, b.body_keys
            if not ka or not kb:
                continue
            overlap = len(ka & kb) / min(len(ka), len(kb))
            if overlap >= CHAPTER_MATCH_MIN:
                scores.append((overlap, i, j))
    scores.sort(reverse=True)
    used_i: set[int] = set()
    used_j: set[int] = set()
    pairs: dict[int, tuple[int, float]] = {}
    for s, i, j in scores:
        if i in used_i or j in used_j:
            continue
        used_i.add(i)
        used_j.add(j)
        pairs[i] = (j, s)
    out: list[tuple[ChapterText | None, ChapterText | None, float]] = []
    for i, a in enumerate(old):
        if i in pairs:
            j, s = pairs[i]
            out.append((a, new[j], round(s, 3)))
        else:
            out.append((a, None, 0.0))
    for j, b in enumerate(new):
        if j not in used_j:
            out.append((None, b, 0.0))
    return out


def page_check(per_stream: dict[str, list[Hunk]]) -> dict:
    """How much of each page's text survived into the other edition, from the hunks.

    A page whose sentences mostly vanished (or a new page whose sentences mostly appeared)
    is either a real cut or an extraction fault. The site lists these pages with both page
    images so a person can tell which. Modified and moved sentences count as survived."""
    old_pages: dict[int, Counter] = {}
    new_pages: dict[int, Counter] = {}
    best_new: dict[int, Counter] = {}
    for hs in per_stream.values():
        for h in hs:
            if h.old_page is not None:
                old_pages.setdefault(h.old_page, Counter())["survived" if h.type in SURVIVED else h.type] += 1
                if h.type in SURVIVED and h.new_page is not None:
                    best_new.setdefault(h.old_page, Counter())[h.new_page] += 1
            if h.new_page is not None and (h.type in SURVIVED or h.type == "inserted"):
                new_pages.setdefault(h.new_page, Counter())["survived" if h.type in SURVIVED else "inserted"] += 1
    old_out = []
    for page in sorted(old_pages):
        c = old_pages[page]
        total = c["survived"] + c["deleted"]
        if total < PAGE_MIN_SENTENCES:
            continue
        score = round(c["survived"] / total, 2)
        best = best_new.get(page)
        old_out.append({"page": page, "new_page": best.most_common(1)[0][0] if best else None, "sentences": total, "score": score, "suspect": score < PAGE_SUSPECT})
    new_out = []
    for page in sorted(new_pages):
        c = new_pages[page]
        total = c["survived"] + c["inserted"]
        if total < PAGE_MIN_SENTENCES:
            continue
        score = round(c["survived"] / total, 2)
        if score < PAGE_SUSPECT:
            new_out.append({"page": page, "sentences": total, "score": score, "suspect": True})
    return {"old": old_out, "new": new_out, "suspect": sum(p["suspect"] for p in old_out) + len(new_out)}


def _counts(hunks: list[Hunk]) -> dict[str, int]:
    c = Counter(h.type for h in hunks if h.type != "equal")
    return {k: c.get(k, 0) for k in ("deleted", "inserted", "modified", "moved", "typographic", "restreamed", "unreadable", "punctuation")}


def match_across_streams(streams: dict[str, list[Hunk]]) -> None:
    """A sentence deleted from one stream and inserted into another only changed role.

    Typesetting changes move text between the body column and boxes, and the extractor's
    role guess follows. Exact key matches become "restreamed"; near matches (an italic
    word lost, a dash changed) become a cross-stream "modified" hunk.
    """
    deleted = [(s, h) for s, hs in streams.items() for h in hs if h.type == "deleted"]
    inserted = [(s, h) for s, hs in streams.items() for h in hs if h.type == "inserted"]
    by_key: dict[str, list[tuple[str, Hunk]]] = {}
    for s, h in inserted:
        by_key.setdefault(normalise_key(h.new), []).append((s, h))
    leftover_del: list[tuple[str, Hunk]] = []
    for s, h in deleted:
        k = normalise_key(h.old)
        if by_key.get(k):
            t, g = by_key[k].pop(0)
            if t == s:
                continue  # same stream, already handled as moved by diff_stream
            streams[s].remove(h)
            streams[t].remove(g)
            streams[s].append(Hunk("restreamed", f"{s}>{t}", 1.0, h.old, g.new, h.old_page, g.new_page, [], h.old_pos, g.new_pos))
        else:
            leftover_del.append((s, h))
    leftover_ins = [(t, g) for lst in by_key.values() for t, g in lst]
    if leftover_del and leftover_ins:
        # Units carry their index into the leftover lists, so each hunk is matched by identity.
        pairs, _, _ = _pair_fuzzy(
            [Unit(s, h.old, h.old_page, None, i) for i, (s, h) in enumerate(leftover_del)],
            [Unit(t, g.new, g.new_page, None, j) for j, (t, g) in enumerate(leftover_ins)],
        )
        for u, v, r in pairs:
            if u.stream == v.stream or r < 0.7:
                continue
            s, h = leftover_del[u.para]
            t, g = leftover_ins[v.para]
            streams[s].remove(h)
            streams[t].remove(g)
            streams[s].append(Hunk("modified", f"{s}>{t}", round(r, 3), h.old, g.new, h.old_page, g.new_page, word_diff(h.old, g.new), h.old_pos, g.new_pos))


def diff_editions(book_id: str, from_id: str, to_id: str) -> dict:
    ed_a, old = load_edition(book_id, from_id)
    ed_b, new = load_edition(book_id, to_id)
    chapters_out = []
    total: Counter = Counter()
    for a, b, overlap in align_chapters(old, new):
        entry: dict = {
            "from": {"number": a.number, "part": a.part, "title": a.title, "file": a.file} if a else None,
            "to": {"number": b.number, "part": b.part, "title": b.title, "file": b.file} if b else None,
            "similarity": overlap,
        }
        if a and b:
            entry["status"] = "matched"
            per_stream = {
                s: diff_stream([u for u in a.units if u.stream == s], [u for u in b.units if u.stream == s], s)
                for s in STREAMS
            }
            match_across_streams(per_stream)
            # Where the other edition has text its fonts cannot map, a deletion or insertion on
            # that page is more likely unreadable text than an edit.
            unreadable_new = {u.page for u in b.units if UNREADABLE in u.text}
            unreadable_old = {u.page for u in a.units if UNREADABLE in u.text}
            for hs in per_stream.values():
                for h in hs:
                    if h.type == "deleted" and h.old_page in unreadable_new:
                        h.type = "unreadable"
                    elif h.type == "inserted" and h.new_page in unreadable_old:
                        h.type = "unreadable"
            streams = {}
            for s, hs in per_stream.items():
                streams[s] = {"counts": _counts(hs), "hunks": [asdict(h) for h in hs]}
                for h in hs:
                    total[(s, h.type)] += 1
            entry["streams"] = streams
            entry["pages"] = page_check(per_stream)
            total[("pages", "suspect")] += entry["pages"]["suspect"]
        else:
            entry["status"] = "dropped" if a else "added"
            total[("chapter", entry["status"])] += 1
        chapters_out.append(entry)
    summary = {
        "chapters_dropped": total[("chapter", "dropped")],
        "chapters_added": total[("chapter", "added")],
        "body": {t: total[("body", t)] for t in ("deleted", "inserted", "modified", "moved", "typographic", "restreamed", "unreadable", "punctuation")},
        "other_streams": {t: sum(total[(s, t)] for s in STREAMS if s != "body") for t in ("deleted", "inserted", "modified", "moved", "typographic", "restreamed", "unreadable", "punctuation")},
        "suspect_pages": total[("pages", "suspect")],
    }
    return {
        "book": book_id,
        "from": from_id,
        "to": to_id,
        "ocr": bool(ed_a.get("ocr") or ed_b.get("ocr")),
        "summary": summary,
        "chapters": chapters_out,
    }


def edition_pairs(book_id: str, include_ocr: bool = True) -> list[tuple[str, str]]:
    """Consecutive non-OCR editions, plus each OCR edition against the non-OCR edition before it."""
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    eds = data["editions"]
    clean = [e["id"] for e in eds if not e.get("ocr")]
    pairs = list(zip(clean, clean[1:]))
    if include_ocr:
        for i, e in enumerate(eds):
            if e.get("ocr"):
                prev = next((p["id"] for p in reversed(eds[:i]) if not p.get("ocr")), None)
                if prev:
                    pairs.append((prev, e["id"]))
    return pairs


def write_diff(result: dict) -> Path:
    out = DIFF_DIR / result["book"] / f"{result['from']}__{result['to']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
    return out
