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
