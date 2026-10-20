from ncert_diff import textparse
from ncert_diff.diff import (
    STREAMS,
    ChapterText,
    Hunk,
    align_chapters,
    diff_stream,
    match_across_chapters,
    match_across_streams,
    merged_markdown,
    word_diff,
)
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
    assert types == ["typographic", "typographic"]  # renumbering only, nothing deleted or inserted
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


def _streams(old: list[Unit], new: list[Unit]) -> dict[str, list[Hunk]]:
    """Per-stream hunks for two unit lists, with the cross-stream passes applied."""
    out = {s: diff_stream([u for u in old if u.stream == s], [v for v in new if v.stream == s], s) for s in STREAMS}
    match_across_streams(out)
    return out


def _loud(streams: dict[str, list[Hunk]]) -> list[tuple[str, str]]:
    return sorted((h.type, h.old or h.new) for hs in streams.values() for h in hs if h.type in ("deleted", "inserted", "modified"))


def test_same_words_in_another_stream_and_cut_differently_are_quiet():
    # One printing sets the bubble as a table row, the other as two captions.
    old = [Unit("table", "I plead not guilty. And I claim trial.", 66, None, 1)]
    new = [Unit("caption", "I plead not guilty.", 66, None, 1), Unit("caption", "And I claim trial.", 66, None, 2)]
    streams = _streams(old, new)
    assert _loud(streams) == []
    [h] = [h for hs in streams.values() for h in hs if h.type != "equal"]
    assert (h.type, h.stream) == ("resplit", "table>caption")
    # A box read as three notes in one printing and one table row in the other, plus a sentence
    # whose cut moved (a fuzzy "modified" pairing that the word bags undo).
    old = [Unit("note", s, 11, None, 1) for s in ("What is the midday meal programme?", "Can you list three benefits of the programme?", "Discuss.")]
    new = [Unit("table", "What is the midday meal programme? Can you list three benefits of the programme? Discuss.", 11, None, 1)]
    assert _loud(_streams(old, new)) == []


def test_word_bags_keep_real_edits_visible():
    # Same box, but a word changed: one modified hunk across streams, not a quiet one.
    old = [Unit("table", "Why do you think the Dalit families were afraid of angering the powerful landlords?", 99, None, 1)]
    new = [Unit("caption", "the Dalit families were afraid of angering the powerful landlords? Why do you think", 99, None, 1)]
    assert [t for t, _ in _loud(_streams(old, new))] == []  # same words, reordered: quiet
    new = [Unit("caption", "Why do you think the Dalit families were afraid of angering the rich landlords? Discuss", 99, None, 1)]
    assert [t for t, _ in _loud(_streams(old, new))] == ["modified"]
    # A real deletion beside a recut box stays a deletion.
    old = [Unit("note", "Can you make up a social advertisement on equality?", 121, None, 1), Unit("note", "You can do this in small groups.", 121, None, 1),
           Unit("body", "This paragraph was cut from the book.", 121, None, 2)]
    new = [Unit("table", "Can you make up a social advertisement on equality? You can do this in small groups.", 121, None, 1)]
    assert _loud(_streams(old, new)) == [("deleted", "This paragraph was cut from the book.")]


def _chapter(number: int, markdown: str) -> ChapterText:
    _, units = parse_chapter(markdown)
    return ChapterText(number, None, f"Chapter {number}", f"ch{number}.md", units, markdown)


_PARLIAMENT = "\n\n".join(f"Parliament sentence number {i} is long enough to be compared by the engine." for i in range(10))
_LAWS = "\n\n".join(f"> [caption] Storyboard frame {i} shows how a new law on domestic violence was passed." for i in range(8))
_CUT = "This passage on the rule of law in colonial India was removed by the rationalisation."


def test_merged_chapter_is_compared_against_the_concatenation():
    old3 = _chapter(3, f"# Parliament\n\n<!-- page 30 (pdf 1) -->\n\n{_PARLIAMENT}\n")
    old4 = _chapter(4, f"---\nchapter: 4\n---\n\n# Understanding Laws\n\n<!-- page 42 (pdf 1) -->\n\n{_CUT}\n\n{_LAWS}\n")
    other = _chapter(5, "# Judiciary\n\n" + "\n\n".join(f"Judiciary sentence number {i} has nothing in common with the rest." for i in range(10)) + "\n")
    new3 = _chapter(3, f"# Parliament and the Making of Laws\n\n<!-- page 30 (pdf 1) -->\n\n{_PARLIAMENT}\n\n{_LAWS}\n")
    new4 = _chapter(4, other.markdown)
    pairs = align_chapters([old3, old4, other], [new3, new4])
    assert [(a.number if a else None, b.number if b else None) for a, b, _ in pairs] == [(3, 3), (5, 4)]  # old 4 is not dropped
    a, b, _ = pairs[0]
    assert [c.number for c in a.merged] == [4]
    hunks = _loud(_streams(a.units, b.units))
    assert hunks == sorted([("deleted", "Parliament"), ("deleted", "Understanding Laws"), ("deleted", _CUT), ("inserted", "Parliament and the Making of Laws")])
    # The other direction: one old chapter split into two new ones.
    pairs = align_chapters([new3, new4], [old3, old4, other])
    assert [(a.number if a else None, b.number if b else None) for a, b, _ in pairs] == [(3, 3), (4, 5)]
    assert [c.number for c in pairs[0][1].merged] == [4]


def test_merged_markdown_closes_the_first_chapters_section():
    md = merged_markdown(["# One\n\n## Exercises\n\n1. Why?\n", "---\nchapter: 2\n---\n\n# Two\n\nBody of two.\n"])
    _, units = parse_chapter(md)
    assert [(u.text, u.stream) for u in units][-2:] == [("Two", "heading"), ("Body of two.", "body")]


def test_text_filed_under_the_next_chapter_is_moved():
    note = "Gender is a term that you may often have heard."
    ch3 = {"teachers-note": [Hunk("inserted", "teachers-note", None, None, note, None, 42, [], None, 5)]}
    ch4 = {"teachers-note": [Hunk("deleted", "teachers-note", None, note, None, 42, None, [], 3, None)]}
    match_across_chapters([ch3, ch4])
    [g], [h] = ch3["teachers-note"], ch4["teachers-note"]
    assert (g.type, g.old_pos, g.new_pos) == ("moved", None, 5)
    assert (h.type, h.old_pos, h.new_pos) == ("moved", 3, None)


def test_chart_labels_are_one_caption():
    labels = ["Rupee Goes To", "Pensions", "5 p.", "Interest Payments", "24 p."]
    md = "# T\n\n" + "\n\n".join(f"> [caption] {t}" for t in labels) + "\n\n> [caption] Fig. 1 A short caption.\n\n> [caption] Amu: Why should slums be like that?\n"
    _, units = parse_chapter(md)
    assert [u.text for u in units if u.stream == "caption"] == [" / ".join(labels), "Fig. 1 A short caption.", "Amu: Why should slums be like that?"]
    # Short captions with no figure among them are ordinary captions.
    _, units = parse_chapter("> [caption] A\n\n> [caption] B\n\n> [caption] C\n\n> [caption] D\n")
    assert [u.text for u in units] == ["A", "B", "C", "D"]


def test_split_sentences_keeps_credits_and_initials_whole():
    assert split_sentences("The Collected Works of Mahatma Gandhi, Vol. 72, Ch. 3, p. 79 and more. Next.") == ["The Collected Works of Mahatma Gandhi, Vol. 72, Ch. 3, p. 79 and more.", "Next."]
    assert split_sentences("When Shanti was arrested, S.I. Rao kept her brother. Does it violate the D.K. Basu guidelines?") == [
        "When Shanti was arrested, S.I. Rao kept her brother.", "Does it violate the D.K. Basu guidelines?",
    ]
    assert split_sentences("A painting by W. Daniell (Ch. 7, Figs. 4, 5).") == ["A painting by W. Daniell (Ch. 7, Figs. 4, 5)."]
    assert split_sentences("He was a contemporary of Rajendra I. During his campaigns he attacked temples.") == [
        "He was a contemporary of Rajendra I.", "During his campaigns he attacked temples.",
    ]


def test_blanks_and_list_labels_do_not_count():
    assert normalise_key("(a) Archives are places where ——————— are kept.") == normalise_key("(a) Archives are places where _______________ are kept.")
    assert normalise_key("1.that the Constitution") == normalise_key("1. That the Constitution")
    assert normalise_key("1.5 million") == "1.5 million"
    old = [Unit("exercises", "12. Find out whether there were any temples in your area.", 44, None, 1)]
    new = [Unit("exercises", "11. Find out whether there were any temples in your area.", 38, None, 1)]
    assert [h.type for h in diff_stream(old, new, "exercises")] == ["typographic"]
    assert Unit("body", "1. Body text", 1, None, 0).key == "1. body text"  # only lists lose their labels


def test_keywords_list_parses_into_the_glossary_stream():
    md = "# T\n\nBody.\n\n### Keywords\n\n- iqta\n\n- garrison\n"
    _, units = parse_chapter(md)
    assert [(u.stream, u.text) for u in units][-2:] == [("glossary", "iqta"), ("glossary", "garrison")]


def test_lettered_statements_after_the_glossary_heading_are_exercises():
    from ncert_diff.textparse import annotate_sections, parse_chapter
    md = "\n\n".join([
        "---\nbook: x\n---",
        "EXERCISES",
        "> [note] 1. Are the statements given alongside true or false.",
        "Glossary",
        "> [note] a. All societies do not think similarly about the roles that boys and girls play.",
        "> [note] d. The work that women do is less valued than that of men.",
        "> [note] Identity: Identity is a sense of self-awareness of who one is.",
    ]) + "\n"
    annotated = annotate_sections(md)
    assert annotated.count("<!-- section: exercises -->") == 2 and annotated.count("<!-- section: glossary -->") == 2
    _, units = parse_chapter(annotated)
    by_text = {u.text[:12]: u.section for u in units}
    assert by_text["All societie"] == "exercises" and by_text["The work tha"] == "exercises"
    assert by_text["Identity: Id"] == "glossary"
