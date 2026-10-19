import json
from pathlib import Path

import pytest

from ncert_diff import extract

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    d = json.loads((FIXTURES / name).read_text())
    blocks = extract.blocks_from_dict(d)
    printed = extract.classify(blocks, d["page_width"], d["page_height"])
    return blocks, printed


@pytest.fixture
def page_2007():
    return load("our-pasts-2_2007_ch04_p1.json")


@pytest.fixture
def page_2023():
    return load("our-pasts-2_2023_ch04_p1.json")


def test_watermark_is_dropped(page_2007):
    blocks, _ = page_2007
    assert not any("republished" in b.text or "©" in b.text for b in blocks)


def test_footer_and_page_number_2007(page_2007):
    blocks, printed = page_2007
    assert printed == 45
    footers = [b.text for b in blocks if b.role == "footer"]
    assert any(t.startswith("45") for t in footers)
    assert any("MUGHAL" in t for t in footers)


def test_footer_and_page_number_2023(page_2023):
    blocks, printed = page_2023
    assert printed == 39
    assert any(b.role == "footer" and "Rationalised" in b.text for b in blocks)
    assert not any(b.role == "body" and "Rationalised" in b.text for b in blocks)


def test_roles_2007(page_2007):
    blocks, _ = page_2007
    roles = {b.text[:20]: b.role for b in blocks}
    assert roles["THE CREATION OF AN E"] == "h2"
    assert roles["Fig. 1 The Red Fort."] == "caption"
    assert roles["R"] == "dropcap"
    assert roles["4"] == "chapter-number"
    assert roles["uling as large a ter"] == "body"


def test_markdown_merges_dropcap_and_titles(page_2007, page_2023):
    for (blocks, printed), expected_title in [(page_2007, "THE CREATION OF AN EMPIRE: The Mughal Dynasty"), (page_2023, "the mughals (16th TO 17th CENTURY)")]:
        pages = [extract.Page(0, printed, blocks)]
        number, title = extract.chapter_title(pages)
        assert number == "4"
        assert title == expected_title
        md = extract.to_markdown(pages)
        assert md.startswith(f"<!-- page {printed} (pdf 1) -->\n\n# ")
        assert "\nRuling as large a territory" in md
        assert "> [caption] Fig. 1 The Red Fort." in md
        assert "\n\n\n" not in md


def test_body_text_strips_markers_and_asides():
    md = "<!-- page 1 (pdf 1) -->\n\n# Title\n\nA paragraph.\n\n> [caption] Fig. 1\n"
    assert extract.body_text(md) == "# Title\nA paragraph."


def test_decode_symbol_font():
    assert extract.decode_symbol_font("\uf048\uf069\uf073\uf074\uf06f\uf072\uf079\uf020\uf048\uf069\uf074\uf06c\uf065\uf072\uf092\uf073") == "History Hitler’s"
    assert extract.decode_symbol_font("plain text") == "plain text"


def _page(blocks_spec, width=600.0, height=800.0, font_fixes=None):
    """A PyMuPDF-style text dict from (text, size, x0, y0, font) tuples, classified."""
    textpage = {"blocks": []}
    for text, size, x0, y0, font in blocks_spec:
        span = {"text": text, "size": size, "font": font, "flags": 0, "bbox": (x0, y0, x0 + 6 * len(text), y0 + size)}
        textpage["blocks"].append({"type": 0, "bbox": span["bbox"], "lines": [{"dir": (1.0, 0.0), "bbox": span["bbox"], "spans": [span]}]})
    blocks = extract.blocks_from_dict(textpage, font_fixes) if font_fixes else extract.blocks_from_dict(textpage)
    printed = extract.classify(blocks, width, height, 12.0)
    return blocks, printed


BODY = "Members of the Legislative Assembly are elected by the people of a constituency. " * 2


def test_running_title_at_body_size_is_a_footer():
    blocks, printed = _page([
        (BODY, 12.0, 80, 100, "Bookman-Light"),
        ("32 Social and Political Life", 12.0, 66, 765, "Bookman-Demi"),
    ])
    assert [b.role for b in blocks] == ["body", "footer"]
    assert printed == 32
    blocks, printed = _page([
        (BODY, 12.0, 80, 100, "Bookman-Light"),
        ("Chapter 3: How the State Government Works 31", 12.0, 290, 768, "Bookman-Demi"),
    ])
    assert blocks[-1].role == "footer" and printed == 31
    # A numberless running title in the band is still a footer, and a short table row is not.
    blocks, printed = _page([(BODY, 12.0, 80, 100, "Bookman-Light"), ("Chapter 1: On Equality", 10.0, 407, 721, "Bookman-Demi")])
    assert blocks[-1].role == "footer" and printed is None
    blocks, _ = _page([(BODY, 12.0, 80, 100, "Bookman-Light"), ("Kerala 93", 12.0, 80, 700, "Bookman-Light")])
    assert blocks[-1].role != "footer"


def test_session_label_is_not_a_page_number():
    blocks, printed = _page([(BODY, 12.0, 80, 100, "Bookman-Light"), ("2022-23", 8.0, 290, 770, "Arial")])
    assert blocks[-1].role == "footer" and printed is None


def test_shifted_quotes_are_repaired_per_font():
    fixes = {"CIDFont+F5": extract.QUOTE_SHIFT}
    blocks, _ = _page([
        ("Teacher·s note on ¶health· ² and ´equality.µ", 12.0, 80, 100, "CIDFont+F5"),
        ("Teacher·s note", 12.0, 80, 300, "Bookman-Light"),
    ], font_fixes=fixes)
    assert blocks[0].text == "Teacher’s note on ‘health’ – and “equality.”"
    assert blocks[1].text == "Teacher·s note"  # a font not in the fix list is untouched


def test_chapter_title_skips_unit_opener_and_teachers_note():
    def page(index, spec):
        blocks, printed = _page(spec)
        return extract.Page(index, printed, blocks)
    pages = [
        page(0, [("UNIT", 60.0, 106, 242, "TT351T00"), ("ONE", 60.0, 113, 312, "TT351T00")]),
        page(1, [("Equality in Indian Democracy", 24.0, 85, 83, "TT2E7T00"), ("Teacher’s note", 12.0, 85, 248, "Bookman-Demi"), (BODY, 12.0, 85, 278, "Bookman-Light")]),
        page(2, [("WHOSE RESPONSIBILITY?", 16.0, 307, 70, "TT440T00"), ("On Equality", 24.0, 85, 404, "TT2EBT00"), (BODY, 12.0, 85, 446, "Bookman-Light")]),
    ]
    assert extract.chapter_title(pages) == (None, "On Equality")


def test_long_caption_in_footer_band_is_not_a_footer():
    blocks, _ = _page([
        (BODY, 12.0, 80, 100, "Bookman-Light"),
        ("Fig. 4 – Thousands joined the demonstrations during the Swadeshi movement", 9.0, 80, 698, "Bookman-LightItalic"),
    ])
    assert blocks[-1].role != "footer"


def test_chapter_title_ignores_dropcap_line():
    blocks, printed = _page([
        ("TRIBES, NOMADS AND SETTLED COMMUNITIES", 20.0, 85, 90, "LucidaSans"),
        ("Y crafts and production activities flourished in towns", 36.0, 85, 300, "Bookman-Light"),
        (BODY, 12.0, 85, 340, "Bookman-Light"),
    ])
    assert extract.chapter_title([extract.Page(0, printed, blocks)]) == (None, "TRIBES, NOMADS AND SETTLED COMMUNITIES")
