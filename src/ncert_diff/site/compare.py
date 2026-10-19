"""Data for the compare view: any two editions of a chapter, page against page.

For every pair of editions of a book the site build writes one JSON file per chapter under
`data/<book>/<from>__<to>/<chapter>.json`. Each holds rows of aligned pages: the old page's
text with its removals marked, the new page's text with its additions marked, and a unified
rendering (the new text with removals placed inline). The browser does the rest: layout,
image modes, and filters (static/compare.js).
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .build import QUIET, REAL, Block, apply_changes, block_html, chapter_blocks

SURVIVED = ("equal", "typographic", "punctuation", "modified", "moved", "restreamed")


def mark_side(blocks: list[Block], chapter_diff: dict, side: str) -> Counter:
    """Mark the sentences of one edition's text with the hunks that touch them.

    `side` is "old" (hunks found by old_pos: deletions and the old half of rewordings) or
    "new" (by new_pos: insertions and the new half). Unchanged sentences stay unmarked."""
    per_stream: dict[str, list] = defaultdict(list)
    for b in blocks:
        for s in b.sentences:
            per_stream[s.stream].append(s)
    counts: Counter = Counter()
    for st in chapter_diff["streams"].values():
        for h in st["hunks"]:
            t = h["type"]
            if t == "equal":
                continue
            stream = h["stream"].split(">")[0 if side == "old" else -1]
            pos = h.get("old_pos") if side == "old" else h.get("new_pos")
            if pos is None or stream not in per_stream or pos >= len(per_stream[stream]):
                continue
            s = per_stream[stream][pos]
            s.change = t
            s.words = h.get("words") or None
            s.similarity = h.get("similarity")
            counts[t] += 1
    return counts


def align_pages(old_pages: list, new_pages: list, chapter_diff: dict) -> list[tuple]:
    """Rows of (old page, new page), either side None when a page has no counterpart.

    Pagination shifts between printings, so pages are paired by where their sentences
    went: each old page goes with the new page that most of its surviving sentences landed
    on, walking forward through both editions. New pages nobody landed on become rows of
    their own, as do old pages whose text went nowhere or backwards."""
    votes: dict = defaultdict(Counter)
    for st in chapter_diff["streams"].values():
        for h in st["hunks"]:
            if h["type"] in SURVIVED and h.get("old_page") is not None and h.get("new_page") is not None:
                votes[h["old_page"]][h["new_page"]] += 1
    best = {p: c.most_common(1)[0][0] for p, c in votes.items()}
    new_index = {p: i for i, p in enumerate(new_pages)}
    rows: list[tuple] = []
    j = 0
    for p in old_pages:
        q = best.get(p)
        if q is not None and q in new_index and new_index[q] >= j:
            rows.extend((None, new_pages[k]) for k in range(j, new_index[q]))
            rows.append((p, q))
            j = new_index[q] + 1
        else:
            rows.append((p, None))
    rows.extend((None, new_pages[k]) for k in range(j, len(new_pages)))
    return rows


def _pages_in_order(blocks: list[Block]) -> list:
    seen: list = []
    for b in blocks:
        if b.page not in seen:
            seen.append(b.page)
    return seen


def _html_by_page(blocks: list[Block], side: str | None) -> dict:
    out: dict = defaultdict(list)
    for b in blocks:
        out[b.page].append(block_html(b, side=side))
    return {page: "\n".join(parts) for page, parts in out.items()}


def _page_flags(chapter_diff: dict) -> tuple[dict, dict]:
    """(old page -> set of hunk types, new page -> set of hunk types), equal hunks left out."""
    old: dict = defaultdict(set)
    new: dict = defaultdict(set)
    for st in chapter_diff["streams"].values():
        for h in st["hunks"]:
            if h["type"] == "equal":
                continue
            if h.get("old_page") is not None:
                old[h["old_page"]].add(h["type"])
            if h.get("new_page") is not None:
                new[h["new_page"]].add(h["type"])
    return old, new


def compare_chapter(old_markdown: str, new_markdown: str, chapter_diff: dict) -> dict:
    """Rows of aligned pages with marked text for both editions and a unified rendering."""
    _, old_blocks = chapter_blocks(old_markdown)
    _, new_blocks = chapter_blocks(new_markdown)
    mark_side(old_blocks, chapter_diff, "old")
    mark_side(new_blocks, chapter_diff, "new")
    _, unified_blocks = chapter_blocks(new_markdown)
    apply_changes(unified_blocks, chapter_diff)
    old_pages = _pages_in_order(old_blocks)
    new_pages = _pages_in_order(new_blocks)
    old_html = _html_by_page(old_blocks, "old")
    new_html = _html_by_page(new_blocks, "new")
    unified_html = _html_by_page(unified_blocks, None)
    old_flags, new_flags = _page_flags(chapter_diff)
    rows = []
    for p, q in align_pages(old_pages, new_pages, chapter_diff):
        types = (old_flags.get(p, set()) if p is not None else set()) | (new_flags.get(q, set()) if q is not None else set())
        rows.append(
            {
                "old": {"page": p, "html": old_html.get(p, "")} if p is not None or q is None else None,
                "new": {"page": q, "html": new_html.get(q, "")} if q is not None else None,
                "unified": unified_html.get(q, "") if q is not None else old_html.get(p, ""),
                "real": bool(types & REAL),
                "minor": bool(types & QUIET),
            }
        )
    counts = Counter()
    for st in chapter_diff["streams"].values():
        for t, n in st["counts"].items():
            if t in REAL:
                counts[t] += n
    return {"rows": rows, "counts": dict(counts), "similarity": chapter_diff.get("similarity")}


def single_side(markdown: str, side: str) -> dict:
    """A chapter that exists in only one of the two editions: every sentence removed or added."""
    _, blocks = chapter_blocks(markdown)
    change = "deleted" if side == "old" else "inserted"
    for b in blocks:
        for s in b.sentences:
            s.change = change
    html = _html_by_page(blocks, side)
    rows = []
    for p in _pages_in_order(blocks):
        rows.append(
            {
                "old": {"page": p, "html": html.get(p, "")} if side == "old" else None,
                "new": {"page": p, "html": html.get(p, "")} if side == "new" else None,
                "unified": html.get(p, ""),
                "real": True,
                "minor": False,
            }
        )
    n = sum(len(b.sentences) for b in blocks)
    return {"rows": rows, "counts": {change: n}, "similarity": 0.0}
