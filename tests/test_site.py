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
