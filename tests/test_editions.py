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
