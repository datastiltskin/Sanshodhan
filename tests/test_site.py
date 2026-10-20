from ncert_diff.site.build import Block, Sentence, apply_changes, chapter_blocks, display_title, pages_html


def test_display_title():
    assert display_title("the mughals (16th TO 17th CENTURY)") == "The Mughals (16th to 17th Century)"
    assert display_title("THE DELHI SULTANS") == "The Delhi Sultans"
    assert display_title("delhI: 12th TO 15th CENTURY") == "Delhi: 12th to 15th Century"
    assert display_title("From Trade to Territory The Company Establishes Power") == "From Trade to Territory The Company Establishes Power"
    assert display_title(None) == "Untitled"


MD = """---
chapter: 4
title: "X"
---

<!-- page 45 (pdf 1) -->

# X

One stays. Two goes. Three stays.

> [caption] Fig. 1 Same caption.

<!-- page 46 (pdf 2) -->

Four stays.
"""


def test_apply_changes_places_deletions_after_their_anchor():
    _, blocks = chapter_blocks(MD)
    # New edition keeps "One stays", "Three stays", "Four stays"; the diff is from the old edition's view.
    diff = {
        "status": "matched",
        "streams": {
            "body": {"hunks": [
                {"type": "equal", "stream": "body", "old": "One stays.", "new": "One stays.", "old_pos": 0, "new_pos": 0, "old_page": 45, "new_page": 45},
                {"type": "deleted", "stream": "body", "old": "Two goes.", "new": None, "old_pos": 1, "new_pos": None, "old_page": 45, "new_page": None},
                {"type": "equal", "stream": "body", "old": "Three stays.", "new": "Three stays.", "old_pos": 2, "new_pos": 1, "old_page": 45, "new_page": 45},
                {"type": "inserted", "stream": "body", "old": None, "new": "Four stays.", "old_pos": None, "new_pos": 2, "old_page": None, "new_page": 46},
            ]},
            "caption": {"hunks": [
                {"type": "deleted", "stream": "caption", "old": "Fig. 2 Gone.", "new": None, "old_pos": 1, "new_pos": None, "old_page": 46, "new_page": None},
            ]},
        },
    }
    # The new text in this test has only "One stays. Two goes. Three stays." so pretend "Two goes." is the surviving second sentence.
    blocks[1].sentences = [Sentence("One stays.", "body"), Sentence("Three stays.", "body")]
    counts = apply_changes(blocks, diff)
    assert counts["deleted"] == 2 and counts["inserted"] == 1
    texts = [(s.text, s.change) for s in blocks[1].sentences]
    assert texts == [("One stays.", None), ("Two goes.", "deleted"), ("Three stays.", None)]
    kinds = [b.kind for b in blocks]
    assert "caption" in kinds and any(s.change == "deleted" and s.text == "Fig. 2 Gone." for b in blocks for s in b.sentences)
    html = pages_html(blocks)
    assert html[0]["page"] == 45 and "chg-deleted" in html[0]["html"]


def test_align_pages_pairs_by_where_text_went():
    from ncert_diff.site.compare import align_pages
    H = lambda t, op, np: {"type": t, "stream": "body", "old_page": op, "new_page": np}  # noqa: E731
    diff = {"streams": {"body": {"hunks": [H("equal", 10, 10), H("equal", 11, 12), H("modified", 11, 12), H("deleted", 12, None), H("inserted", None, 13)]}}}
    assert align_pages([10, 11, 12], [10, 11, 12, 13], diff) == [(10, 10), (None, 11), (11, 12), (12, None), (None, 13)]


def test_mark_side_marks_each_edition_with_its_own_half():
    from ncert_diff.site.compare import compare_chapter
    old = "# T\n\n<!-- page 5 (pdf 1) -->\n\nOne. Two.\n"
    new = "# T\n\n<!-- page 7 (pdf 1) -->\n\nOne. Three.\n"
    diff = {"status": "matched", "similarity": 0.5, "streams": {"body": {"counts": {"equal": 1, "deleted": 1, "inserted": 1}, "hunks": [
        {"type": "equal", "stream": "body", "old": "One.", "new": "One.", "old_page": 5, "new_page": 7, "words": [], "old_pos": 0, "new_pos": 0},
        {"type": "deleted", "stream": "body", "old": "Two.", "new": None, "old_page": 5, "new_page": None, "words": [], "old_pos": 1, "new_pos": None},
        {"type": "inserted", "stream": "body", "old": None, "new": "Three.", "old_page": None, "new_page": 7, "words": [], "old_pos": None, "new_pos": 1},
    ]}, "heading": {"counts": {"equal": 1}, "hunks": [{"type": "equal", "stream": "heading", "old": "T", "new": "T", "old_page": None, "new_page": None, "words": [], "old_pos": 0, "new_pos": 0}]}}}
    out = compare_chapter(old, new, diff)
    row = [r for r in out["rows"] if r["old"] and r["old"]["page"] == 5][0]
    assert row["new"]["page"] == 7 and row["real"]
    assert "chg-deleted" in row["old"]["html"] and "chg-inserted" not in row["old"]["html"]
    assert "chg-inserted" in row["new"]["html"] and "chg-deleted" not in row["new"]["html"]
    assert "chg-deleted" in row["unified"] and "chg-inserted" in row["unified"]
    assert out["counts"] == {"deleted": 1, "inserted": 1}


def _edition(book, ed_id, chapters, index):
    from ncert_diff.site.build import Edition

    raw = {"chapters": [{"part": None, "number": n, "title": t, "file": f"texts/{book}/{ed_id}/{n:02d}-x.md"} for n, t in chapters]}
    return Edition(book, ed_id, raw, index, ed_id, "")


def test_chapter_lineages_follow_renumbered_and_dropped_chapters():
    from ncert_diff.site.build import chapter_lineages

    eds = [
        _edition("b", "2014-01-01", [(1, "One"), (2, "Two"), (3, "Three")], 0),
        _edition("b", "2023-01-01-rationalised", [(1, "One"), (2, "Three")], 1),  # chapter 2 dropped, 3 renumbered to 2
    ]
    diffs = {("2014-01-01", "2023-01-01-rationalised"): {"chapters": [
        {"status": "matched", "from": {"file": "texts/b/2014-01-01/01-x.md"}, "to": {"file": "texts/b/2023-01-01-rationalised/01-x.md"}},
        {"status": "dropped", "from": {"file": "texts/b/2014-01-01/02-x.md"}, "to": None},
        {"status": "matched", "from": {"file": "texts/b/2014-01-01/03-x.md"}, "to": {"file": "texts/b/2023-01-01-rationalised/02-x.md"}},
    ]}}
    lin = chapter_lineages(eds, diffs)
    assert lin[("2014-01-01", "ch01")] == lin[("2023-01-01-rationalised", "ch01")] == "L01"
    assert lin[("2014-01-01", "ch02")] == "L02"
    assert lin[("2014-01-01", "ch03")] == lin[("2023-01-01-rationalised", "ch02")] == "L03"


def test_short_label_adds_months_and_words_only_when_needed():
    from ncert_diff.site.build import short_label

    eds = [_edition("b", i, [], n) for n, i in enumerate(["2014-07-28", "2019-03-12", "2019-05-04", "2022-08-04-ocr", "2023-12-23-rationalised", "2025-partial", "rungtaias-undated", "live-2026-10-18"])]
    labels = [short_label(e, eds) for e in eds]
    assert labels == ["2014", "2019 Mar", "2019 May", "2022 scanned", "2023 rationalised", "2025 partial", "undated mirror", "2026 live"]


def test_search_catalogue_lists_editions_and_lineages():
    from ncert_diff.site.build import search_catalogue
    from ncert_diff.sources import Book

    eds = [_edition("b", "2014-01-01", [(1, "ONE"), (2, "Two")], 0), _edition("b", "2023-01-01", [(1, "One, Renamed")], 1)]
    lineages = {"b": {("2014-01-01", "ch01"): "L01", ("2014-01-01", "ch02"): "L02", ("2023-01-01", "ch01"): "L01"}}
    book = Book(id="b", title="Book", klass=7, subject="history", language="en", codes=[], first_chapter={}, snapshots=[])
    cat = search_catalogue({"b": book}, {"b": eds}, lineages)
    b = cat["books"][0]
    assert [e["short"] for e in b["editions"]] == ["2014", "2023"]
    assert b["lineages"][0] == {"id": "L01", "title": "One, Renamed", "chapters": {"2014-01-01": "ch01", "2023-01-01": "ch01"}}
    assert b["lineages"][1]["chapters"] == {"2014-01-01": "ch02"}
