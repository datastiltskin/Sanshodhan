from ncert_diff import textparse
from ncert_diff.diff import Hunk, diff_stream, word_diff
from ncert_diff.textparse import Unit, normalise_key, parse_chapter, split_sentences


def test_normalise_key_ignores_case_dashes_quotes():
    assert normalise_key("The Making of the National Movement: 1870s--1947") == normalise_key("THE MAKING OF THE NATIONAL MOVEMENT: 1870s–1947")
    assert normalise_key("Akbar’s “group photograph”.") == normalise_key('Akbar\'s "group photograph"')


def test_split_sentences_keeps_abbreviations():
    s = split_sentences("Look at Fig. 1 carefully. It shows the Red Fort. Why was it built?")
    assert s == ["Look at Fig. 1 carefully.", "It shows the Red Fort.", "Why was it built?"]


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
