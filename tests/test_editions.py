from ncert_diff.editions import apply_overrides


def test_overrides_apply_by_snapshot_and_chapter():
    overrides = [
        {"snapshot": "2024-05-24", "chapter": 2, "find": "I 1,174", "replace": "11,174", "note": "OCR"},
        {"snapshot": "*", "chapter": 6, "find": "EXERCISES oD.", "replace": "EXERCISES", "note": "glyph"},
    ]
    md, applied, missed = apply_overrides("there were I 1,174 hospitals", "2024-05-24", 2, overrides)
    assert md == "there were 11,174 hospitals" and applied == ["OCR"] and missed == []
    # Another snapshot: the specific entry does not apply, and is not missed either.
    md, applied, missed = apply_overrides("there were 11,174 hospitals", "2023-12-23", 2, overrides)
    assert (md, applied, missed) == ("there were 11,174 hospitals", [], [])
    # A specific entry whose text is gone is reported.
    md, applied, missed = apply_overrides("there were 11,174 hospitals", "2024-05-24", 2, overrides)
    assert missed == ["OCR"]
    # A wildcard entry applies wherever it matches and never counts as missed.
    md, applied, missed = apply_overrides("EXERCISES oD.", "2020-05-08", 6, overrides)
    assert md == "EXERCISES" and applied == ["glyph"]
    assert apply_overrides("EXERCISES", "2020-05-08", 6, overrides)[2] == []


def test_append_references_renames_markers_and_demotes_the_title():
    from ncert_diff.editions import append_references
    chapter = "---\nchapter: 10\n---\n\n<!-- page 121 (pdf 8) -->\n\nLast paragraph.\n"
    refs = "<!-- page 122 (pdf 1) -->\n\n# References\n\n> [note] Dreze, Jean. 2003.\n"
    out = append_references(chapter, refs, "gess3rf.pdf")
    assert out.endswith("Last paragraph.\n\n<!-- page 122 (pdf 1 of gess3rf.pdf) -->\n\n## References\n\n> [note] Dreze, Jean. 2003.\n")


def test_chapters_match_tolerates_a_sentence_in_a_box():
    from ncert_diff.editions import chapters_match
    body = " ".join(f"Sentence number {i} says something." for i in range(60))
    a = "# T\n\n" + body + "\n\nFind out how many states have been created.\n"
    b = "# T\n\n" + body + "\n\n> [note] Find out how many states have been created.\n"
    assert chapters_match(a, b)
    assert not chapters_match(a, "# T\n\n" + " ".join(f"Other sentence {i} here." for i in range(60)) + "\n")


def test_overrides_can_address_the_prelims():
    overrides = [{"snapshot": "2023-12-23", "chapter": "prelims", "find": "THE CO ONSTITUTIO ON", "replace": "THE CONSTITUTION", "note": "Preamble"}]
    md, applied, missed = apply_overrides("WE, THE PEOPLE OF INDIA ... THE CO ONSTITUTIO ON", "2023-12-23", "prelims", overrides)
    assert md.endswith("THE CONSTITUTION") and applied == ["Preamble"] and missed == []
    assert apply_overrides("chapter text", "2023-12-23", 3, overrides) == ("chapter text", [], [])


def test_override_with_a_part_reaches_only_that_part():
    overrides = [{"snapshot": "live", "chapter": 2, "part": 2, "find": "Bhutan S emblem", "replace": "Bhutan emblem", "note": "stray S"}]
    assert apply_overrides("Bhutan S emblem", "live", 2, overrides, part=2) == ("Bhutan emblem", ["stray S"], [])
    assert apply_overrides("Bhutan S emblem", "live", 2, overrides, part=1) == ("Bhutan S emblem", [], [])
    # A book without parts ignores the field, and an entry without it reaches every part.
    assert apply_overrides("Bhutan S emblem", "live", 2, overrides)[1] == ["stray S"]
    loose = [{"snapshot": "live", "chapter": "prelims", "find": "x", "replace": "y", "note": "cover"}]
    assert apply_overrides("x", "live", "prelims", loose, part=1)[1] == ["cover"]
