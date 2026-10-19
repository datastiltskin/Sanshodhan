from ncert_diff import textparse
from ncert_diff.diff import Hunk, diff_stream, word_diff
from ncert_diff.textparse import Unit, normalise_key, parse_chapter, split_sentences


def test_normalise_key_ignores_case_dashes_quotes():
    assert normalise_key("The Making of the National Movement: 1870s--1947") == normalise_key("THE MAKING OF THE NATIONAL MOVEMENT: 1870s–1947")
    assert normalise_key("Akbar’s “group photograph”.") == normalise_key('Akbar\'s "group photograph"')


def test_split_sentences_keeps_abbreviations():
    s = split_sentences("Look at Fig. 1 carefully. It shows the Red Fort. Why was it built?")
    assert s == ["Look at Fig. 1 carefully.", "It shows the Red Fort.", "Why was it built?"]
    assert split_sentences("1. Why was it built? 12. Who built it?") == ["1. Why was it built?", "12. Who built it?"]


def test_parse_chapter_streams_and_pages():
    md = "---\nchapter: 4\ntitle: \"X\"\n---\n\n<!-- page 45 (pdf 1) -->\n\n# X\n\nOne. Two!\n\n> [caption] Fig. 1 The fort.\n\n<!-- page 46 (pdf 2) -->\n\nThree.\n"
    meta, units = parse_chapter(md)
    assert meta["title"] == "X"
    assert [(u.stream, u.text, u.page) for u in units] == [
        ("heading", "X", 45), ("body", "One.", 45), ("body", "Two!", 45), ("caption", "Fig. 1 The fort.", 45), ("body", "Three.", 46),
    ]


def U(text, page=1):
    return Unit("body", text, page, page, 0)


def test_diff_stream_classifies():
    old = [U("The Mughals were descendants of two great lineages."), U("Babur was the first Mughal emperor."), U("He seized Kabul in 1504."), U("This sentence moves.")]
    new = [U("This sentence moves."), U("The Mughals were descendants of two great lineages of rulers."), U("Babur was the first Mughal emperor."), U("Akbar came next.")]
    hunks = diff_stream(old, new, "body")
    types = {(h.type, h.old or h.new) for h in hunks}
    assert ("equal", "Babur was the first Mughal emperor.") in types
    deleted = next(h for h in hunks if h.type == "deleted")
    assert deleted.old_pos == 2 and deleted.new_pos is None
    moved = next(h for h in hunks if h.type == "moved")
    assert (moved.old_pos, moved.new_pos) == (3, 0)
    assert ("modified", "The Mughals were descendants of two great lineages.") in types
    assert ("deleted", "He seized Kabul in 1504.") in types
    assert ("inserted", "Akbar came next.") in types
    assert ("moved", "This sentence moves.") in types


def test_typographic_only():
    hs = diff_stream([U("THE DELHI SULTANS")], [U("The Delhi Sultans")], "heading")
    assert [h.type for h in hs] == ["typographic"]


def test_word_diff():
    assert word_diff("Why not their Mughal descent?", "Why not their Mongol descent?") == [["=", "Why not their"], ["-", "Mughal"], ["+", "Mongol"], ["=", "descent?"]]


def test_punctuation_only_is_quiet():
    hs = diff_stream([U("By 1696 it began building a fort around the settlement.")], [U("By 1696, it began building a fort around the settlement.")], "body")
    assert [h.type for h in hs] == ["punctuation"]
    hs = diff_stream([U("Why did the Mughals emphasise their Timurid and not their Mughal descent?")], [U("Why did the Mughals emphasise their Timurid and not their Mongol descent?")], "body")
    assert [h.type for h in hs] == ["modified"]


def test_sections_are_detected_and_annotated():
    md = "# Title\n\nBody one.\n\n## Let’s recall\n\n1. First question?\n\n> [note] Glossary\n\n> [note] Term: meaning.\n"
    annotated = textparse.annotate_sections(md)
    assert "<!-- section: exercises -->\n\n## Let’s recall" in annotated
    assert "<!-- section: glossary -->\n\n> [note] Glossary" in annotated
    assert textparse.annotate_sections(annotated) == annotated  # idempotent
    two = textparse.annotate_sections("## Let’s recall\n\nOne?\n\n## Let’s discuss\n\nTwo?\n")
    assert two.count("<!-- section: exercises -->") == 1  # consecutive exercise headings share one marker
    _, units = parse_chapter(annotated)
    assert [(u.stream, u.role, u.section) for u in units] == [
        ("heading", "heading", None), ("body", "body", None),
        ("heading", "heading", "exercises"), ("exercises", "body", "exercises"),
        ("glossary", "note", "glossary"), ("glossary", "note", "glossary"),
    ]
    # Without markers the start lines themselves open the sections.
    assert [u.section for u in parse_chapter(md)[1]] == [u.section for u in units]


def test_table_rows_inside_a_section_are_sentences():
    md = "# T\n\n> [table] Year 1991 | 11,174\n\n<!-- section: exercises -->\n\n> [table] 1. Why? 2. How?\n"
    _, units = parse_chapter(md)
    assert [(u.stream, u.text) for u in units] == [("heading", "T"), ("table", "Year 1991 | 11,174"), ("exercises", "1. Why?"), ("exercises", "2. How?")]


def test_teachers_note_ends_at_chapter_title():
    md = "## Unit title\n\nTeacher’s note\n\nAdvice for teachers.\n\n# Chapter title\n\nBody.\n"
    _, units = parse_chapter(md)
    assert [(u.text[:8], u.section) for u in units] == [
        ("Unit tit", None), ("Teacher’", "teachers-note"), ("Advice f", "teachers-note"), ("Chapter ", None), ("Body.", None),
    ]


def test_exercises_compare_without_regard_to_order():
    old = [Unit("exercises", "1. Why did the trader pay less?", 10, None, 1), Unit("exercises", "2. What is a weekly market?", 10, None, 2)]
    new = [Unit("exercises", "What is a weekly market?", 9, None, 1), Unit("exercises", "Why did the trader pay less?", 9, None, 2)]
    types = sorted(h.type for h in diff_stream(old, new, "exercises"))
    assert types == ["modified", "modified"]  # renumbering only; nothing deleted or inserted
    old = [Unit("exercises", "Explain how a chain of markets is formed.", 10, None, 1), Unit("exercises", "What purpose does it serve?", 10, None, 1)]
    new = [Unit("exercises", "What purpose does it serve?", 9, None, 1), Unit("exercises", "Explain how a chain of markets is formed.", 9, None, 1)]
    assert sorted(h.type for h in diff_stream(old, new, "exercises")) == ["equal", "equal"]


def test_page_check_flags_pages_that_mostly_vanished():
    from ncert_diff.diff import page_check
    hunks = [Hunk("equal", "body", 1.0, "a", "a", 5, 5, [], 0, 0)] * 2 + [Hunk("deleted", "body", None, "x", None, 5, None, [], 1, None)] * 3
    hunks += [Hunk("equal", "body", 1.0, "b", "b", 6, 6, [], 2, 2)] * 4
    hunks += [Hunk("inserted", "body", None, None, "n", None, 9, [], None, 3)] * 5
    checks = page_check({"body": hunks})
    assert [(p["page"], p["new_page"], p["suspect"]) for p in checks["old"]] == [(5, 5, True), (6, 6, False)]
    assert [(p["page"], p["suspect"]) for p in checks["new"]] == [(9, True)]
    assert checks["suspect"] == 2


def test_resplit_pairs_one_sentence_with_its_parts():
    old = [Unit("body", "Grand Total 543 Once elected, these candidates become MPs.", 35, None, 1)]
    new = [Unit("body", "Grand Total 543", 35, None, 1), Unit("body", "Once elected, these candidates become MPs.", 36, None, 2)]
    hunks = diff_stream(old, new, "body")
    assert [h.type for h in hunks] == ["resplit"]
    assert hunks[0].old_page == 35 and hunks[0].new_page == 35
    # The reverse direction too, and unrelated sentences stay deleted or inserted.
    hunks = diff_stream(new + [Unit("body", "Something else entirely was here.", 36, None, 3)], old, "body")
    assert sorted(h.type for h in hunks) == ["deleted", "resplit"]
