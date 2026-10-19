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


def test_bold_first_line_becomes_its_own_heading_block():
    def span(text, font, size=11.0):
        return {"text": text, "font": font, "size": size, "flags": 0, "bbox": (80, 100, 400, 100 + size)}
    textpage = {"blocks": [{"type": 0, "bbox": (80, 100, 400, 140), "lines": [
        {"dir": (1.0, 0.0), "bbox": (80, 100, 240, 112), "spans": [span("A nation in the making", "Bookman-Demi", 12.0)]},
        {"dir": (1.0, 0.0), "bbox": (80, 114, 400, 126), "spans": [span("It has often been said that the Congress", "Bookman-Light")]},
        {"dir": (1.0, 0.0), "bbox": (80, 128, 400, 140), "spans": [span("in the first twenty years was moderate.", "Bookman-Light")]},
    ]}]}
    for ln in textpage["blocks"][0]["lines"]:
        for sp in ln["spans"]:
            sp["bbox"] = ln["bbox"]  # each span sits on its own line, as on a real page
    blocks = extract.blocks_from_dict(textpage)
    assert [(b.text, b.bold) for b in blocks] == [("A nation in the making", True), ("It has often been said that the Congress in the first twenty years was moderate.", False)]
    # A bold lead-in that shares its line with regular text is left in the paragraph.
    tail = span(" It has often been said", "Bookman-Light")
    tail["bbox"] = (240, 100, 400, 112)  # beside the bold words on the same line, not on top of the next line
    textpage["blocks"][0]["lines"][0]["spans"].append(tail)
    assert len(extract.blocks_from_dict(textpage)) == 1


def test_sdg_badge_label_is_a_caption_not_body():
    blocks, _ = _page([
        ("Sustainable Development Goal (SDG) www.in.undp.org", 11.0, 85, 702, "TT38DT00"),
        (BODY, 12.0, 80, 100, "Bookman-Light"),
    ])
    assert blocks[0].role == "caption"


def test_word_drawn_again_over_the_line_end_is_dropped():
    def line(text, bbox):
        return {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": text, "font": "BookmanPlain", "size": 13.0, "flags": 4, "bbox": bbox}]}
    lines = [
        line("was made in the 1720s by a French cartographer", (73.2, 660.8, 376.5, 675.8)),
        line("cartographer", (294.4, 661.0, 376.1, 675.8)),
        line("cartographer", (294.8, 660.6, 376.5, 675.4)),
        line("cartographer", (294.4, 660.6, 376.1, 675.4)),
        line("cartographer. The", (294.6, 660.8, 407.2, 675.6)),
    ]
    from ncert_diff import clean
    texts = [extract._join_spans(spans) for spans in extract._dedupe_shadow_spans(lines)]
    assert clean.join_lines(texts) == "was made in the 1720s by a French cartographer. The"


def test_outlined_runs_on_one_baseline_join_in_reading_order():
    import pymupdf
    textpage = {"blocks": [{"type": 0, "bbox": (206, 250, 546, 290), "lines": [
        {"dir": (1.0, 0.0), "bbox": (206, 276, 540, 290), "spans": [{"text": "on the period of their study", "font": "Bookman", "size": 11.0, "flags": 0, "bbox": (206, 276, 540, 290)}]},
    ]}]}
    words = {(206, 294, 450, 306): "and the nature of their investigation.", (455, 294, 515, 306): "Last year,", (525, 294, 542, 303): "for"}
    rects = [pymupdf.Rect(*k) for k in words]
    extract._fill_outlined_words(None, textpage, rects, lambda page, r: words[tuple(round(v) for v in r)])
    blocks = extract.blocks_from_dict(textpage)
    assert blocks[0].text == "on the period of their study and the nature of their investigation. Last year, for"


def _fill(lines, words):
    """Run the outlined-word filler on one block of `lines` [(bbox, [(text, x0, x1)])] with OCR `words` {rect: reading}."""
    import pymupdf
    block_lines = [
        {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": t, "font": "Bookman", "size": 12.0, "flags": 0, "bbox": (x0, bbox[1], x1, bbox[3])} for t, x0, x1 in spans]}
        for bbox, spans in lines
    ]
    box = pymupdf.Rect(block_lines[0]["bbox"])
    for ln in block_lines[1:]:
        box |= pymupdf.Rect(ln["bbox"])
    textpage = {"blocks": [{"type": 0, "bbox": tuple(box), "lines": block_lines}]}
    rects = [pymupdf.Rect(*k) for k in words]
    extract._fill_outlined_words(None, textpage, rects, lambda page, r: words[tuple(round(v) for v in r)])
    return extract.blocks_from_dict(textpage)[0].text


def test_outlined_run_a_word_space_short_of_its_line_joins_that_line():
    text = _fill(
        [((206, 672, 545, 687), [("was collected for them by their servants while the ", 206, 545)]),
         ((289, 688, 545, 703), [("themselves served in some other part of ", 289, 545)]),
         ((206, 704, 288, 719), [("the country. ", 206, 288)])],
        {(207, 690, 285, 700): "mansabdars"},
    )
    assert text == "was collected for them by their servants while the mansabdars themselves served in some other part of the country."


def test_outlined_run_before_punctuation_gets_no_space():
    text = _fill([((100, 100, 400, 114), [("Today we understand it as India, the modern ", 100, 300), (". When the term", 352, 400)])], {(302, 102, 350, 112): "nation-state."})
    assert text == "Today we understand it as India, the modern nation-state. When the term"


def test_outlined_run_between_two_line_fragments_drops_the_doubled_comma():
    text = _fill(
        [((236, 300, 319, 314), [(". But unlike ", 236, 319)]), ((363, 300, 408, 314), [(", most ", 363, 408)])],
        {(322, 302, 360, 312): "muqtis,"},
    )
    assert text == ". But unlike muqtis, most"


def test_outlined_run_loses_a_full_stop_before_lower_case():
    text = _fill([((100, 100, 400, 114), [("But most ", 100, 160), ("did not actually", 230, 400)])], {(165, 102, 225, 112): "mansabdars."})
    assert text == "But most mansabdars did not actually"


def test_outlined_run_loses_unmatched_quotes_and_a_leading_rule():
    assert _fill([((100, 100, 400, 114), [("as ", 100, 120), ("received their salaries", 200, 400)])], {(125, 102, 195, 112): "‘Mansabdars"}) == "as Mansabdars received their salaries"
    assert _fill([((100, 100, 400, 114), [("administer their ", 100, 200), (". They only", 260, 400)])], {(205, 102, 255, 112): "- jagirs."}) == "administer their jagirs. They only"
    assert _fill([((100, 100, 400, 114), [("known as ", 100, 160), (", became", 200, 400)])], {(165, 102, 195, 112): "‘ur"}) == "known as ur, became"
    # A quote that is closed later in the sentence is real.
    assert _fill([((100, 100, 400, 114), [("the word ", 100, 160), (" stuck’ to them.", 200, 400)])], {(165, 102, 195, 112): "‘raja"}) == "the word ‘raja stuck’ to them."


def _blk(text, size, x0, y0, x1=None, y1=None, font="Bookman-Light", bold=False, italic=False):
    return extract.Block(x0, y0, x1 if x1 is not None else x0 + 6 * len(text), y1 if y1 is not None else y0 + size, font, size, bold, italic, text)


def test_real_last_line_in_the_footer_band_is_kept():
    # 2021 Social and Political Life III, ch1 p17: the glossary's last entry sits at 86.9 per
    # cent of the height, above the real footers.
    def page(last, number):
        return [_blk(BODY, 13.0, 138, 100), _blk(last, 11.0, 138, 680),
                _blk("Chapter 1: The Indian Constitution", 9.0, 384, 721), _blk("2021-22", 8.0, 291, 753), _blk(number, 12.0, 358, 721)]
    pages = [page("Tyranny: The cruel and unjust use of power or authority.", "17"), page("armed forces for being a woman.", "16")]
    running = extract.running_footers([(blocks, 783.0) for blocks in pages])
    blocks = pages[0]
    printed = extract.classify(blocks, 612.0, 783.0, 13.0, running)
    assert [b.role for b in blocks] == ["body", "table", "footer", "footer", "footer"]
    assert printed == 17
    # A running title printed once is caught by the row the footers sit on.
    once = [_blk(BODY, 13.0, 138, 100), _blk("THE MUGHAL DYNASTY", 9.0, 384, 721.5)]
    extract.classify(once, 612.0, 783.0, 13.0, running)
    assert once[1].role == "footer"


def test_caption_tail_glued_to_the_running_title_is_kept():
    running = extract.RunningFooters({"towns traders and craftspersons"}, set())
    blocks = [_blk(BODY, 13.0, 80, 100), _blk("Hampi. TOWNS, TRADERS AND CRAFTSPERSONS", 9.0, 80, 700)]
    extract.classify(blocks, 600.0, 800.0, 13.0, running)
    assert blocks[1].text == "Hampi." and blocks[1].role != "footer"
    blocks = [_blk(BODY, 13.0, 80, 100), _blk("Reprint 2024-25", 6.6, 278, 760)]
    extract.classify(blocks, 600.0, 800.0, 13.0, running)
    assert blocks[1].role == "footer" and blocks[1].text == "Reprint 2024-25"


def test_question_box_glyph_is_not_a_drop_cap():
    q = _blk("Q", 100.0, 393, 145, 482, 245)
    q.role = "dropcap"
    body = _blk("Imagine a situation in which a powerful politician has encroached on land.", 13.0, 252, 310)
    body.role = "body"
    md = extract.to_markdown([extract.Page(0, 56, [q, body])])
    assert "\nImagine a situation" in md and "QImagine" not in md


def test_letter_spaced_words_are_closed_up():
    def chars(text, gaps):
        out, x = [], 100.0
        for ch, gap in zip(text, gaps):
            x += gap
            w = 3.0 if ch == " " else 6.0
            out.append({"c": ch, "bbox": (x, 100, x + w, 112)})
            x += w
        return out
    text = "R e m e m b e r t h a t "
    gaps = [0.0] * len(text)
    gaps[text.index("r t") + 1] = 3.0  # the word space carries a visible gap
    line = {"spans": [{"chars": chars(text, gaps)}]}
    extract._text_from_chars(line)
    assert line["spans"][0]["text"] == "Remember that "
    line = {"spans": [{"chars": chars("I am a b ", [0.0] * 9)}]}
    extract._text_from_chars(line)
    assert line["spans"][0]["text"] == "I am a b "  # two one-letter words in ordinary text stay apart


def test_square_bullets_keep_list_items_apart():
    def line(text, x0, y0, size=11.0, font="Bookman-Light"):
        bbox = (x0, y0, x0 + 6 * len(text), y0 + size)
        return {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": text, "font": font, "size": size, "flags": 0, "bbox": bbox}]}
    textpage = {"blocks": [{"type": 0, "bbox": (100, 500, 400, 560), "lines": [
        line("In the previous chapters we have looked at:", 100, 486),
        line("¢", 108, 515, 6.0, "TT95AT00"),
        line("The British conquest of territories, and takeover", 122, 513),
        line("of kingdoms", 122, 526),
        line("\x84", 108, 545, 6.0, "Wingdings2"),
        line("Introduction of new laws and administrative", 122, 542),
    ]}]}
    assert [b.text for b in extract.blocks_from_dict(textpage)] == [
        "In the previous chapters we have looked at:",
        "- The British conquest of territories, and takeover of kingdoms",
        "- Introduction of new laws and administrative",
    ]


def test_drop_cap_does_not_host_an_outlined_line():
    textpage = {"blocks": [
        {"type": 0, "bbox": (69, 217, 94, 258), "lines": [{"dir": (1.0, 0.0), "bbox": (69, 217, 94, 258), "spans": [{"text": "R", "font": "F3", "size": 40.0, "flags": 0, "bbox": (69, 217, 94, 258)}]}]},
        {"type": 0, "bbox": (94, 222, 411, 252), "lines": [
            {"dir": (1.0, 0.0), "bbox": (94, 222, 411, 237), "spans": [{"text": "uling as large a territory as the Indian subcontinent ", "font": "F3", "size": 12.9, "flags": 0, "bbox": (94, 222, 411, 237)}]},
            {"dir": (1.0, 0.0), "bbox": (97, 238, 411, 252), "spans": [{"text": "with such a diversity of people and cultures was an ", "font": "F3", "size": 12.9, "flags": 0, "bbox": (97, 238, 411, 252)}]},
        ]},
    ]}
    import pymupdf
    words = {(71, 257, 407, 269): "extremely difficult task for any ruler to accomplish in"}
    extract._fill_outlined_words(None, textpage, [pymupdf.Rect(*k) for k in words], lambda page, r: words[tuple(round(v) for v in r)])
    blocks = extract.blocks_from_dict(textpage)
    assert blocks[0].text == "R"
    assert blocks[1].text.endswith("cultures was an extremely difficult task for any ruler to accomplish in")


def test_margin_caption_sharing_a_body_block_is_split_off():
    def line(text, bbox, size):
        return {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": text, "font": "Bookman-Light", "size": size, "flags": 0, "bbox": bbox}]}
    textpage = {"blocks": [{"type": 0, "bbox": (67, 709, 539, 734), "lines": [
        line("of his kingdom, and disallowed local merchants from", (234, 709, 539, 720), 11.0),
        line("trading with the Company. He also established a close", (234, 722, 539, 733), 11.0),
        line("Fig. 8 – Tipu Sultan", (67, 725, 158, 734), 9.0),
    ]}]}
    assert [b.text for b in extract.blocks_from_dict(textpage)] == [
        "of his kingdom, and disallowed local merchants from trading with the Company. He also established a close",
        "Fig. 8 – Tipu Sultan",
    ]


def test_small_paragraph_under_a_caption_is_part_of_it():
    blocks = [_blk(BODY, 11.0, 91, 100, 397), _blk("Fig. 7 – The rebels of 1857", 9.0, 96, 323, 213, 333, italic=True),
              _blk("Images need to be carefully studied for they project the viewpoint of those who create them. " * 3, 9.0, 96, 337, 392, 400)]
    extract.classify(blocks, 600.0, 842.0, 11.0)
    assert [b.role for b in blocks] == ["body", "caption", "caption"]


def test_short_italic_line_over_a_paragraph_is_a_heading():
    blocks = [_blk("Gulamgiri", 12.0, 91, 98, 153, 110, italic=True), _blk(BODY, 11.0, 91, 116, 397, 300)]
    extract.classify(blocks, 600.0, 842.0, 11.0)
    assert blocks[0].role == "h3"
    blocks = [_blk("Temple Construction in the Early Eleventh Century", 12.0, 209, 102, bold=True, italic=True), _blk(BODY, 13.0, 209, 300)]
    extract.classify(blocks, 600.0, 842.0, 13.0)
    assert blocks[0].role == "h3"


def test_run_in_heading_in_an_unflagged_bold_face():
    def line(text, font, size, y):
        bbox = (74, y, 409, y + size)
        return {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": text, "font": font, "size": size, "flags": 4, "bbox": bbox}]}
    textpage = {"blocks": [{"type": 0, "bbox": (74, 203, 409, 253), "lines": [
        line("Revenue for the Company", "TT179EE2O00", 12.0, 203),
        line("The Company had become the Diwan, but it still saw", "TT179E82O00", 11.0, 228),
        line("itself primarily as a trader. It wanted a large revenue income.", "TT179E82O00", 11.0, 241),
    ]}]}
    blocks = extract.blocks_from_dict(textpage)
    assert blocks[0].text == "Revenue for the Company" and blocks[0].bold


def test_fake_bold_copy_missing_its_first_glyph_is_dropped():
    def line(text, x0, x1):
        return {"dir": (1.0, 0.0), "bbox": (x0, 450, x1, 463), "spans": [{"text": text, "font": "Garamond,Bold", "size": 13.0, "flags": 0, "bbox": (x0, 450, x1, 463)}]}
    textpage = {"blocks": [{"type": 0, "bbox": (252, 450, 552, 463), "lines": [
        line("prosecution ", 252.2, 323.4), line("rosecution ", 258.8, 323.0), line("rosecution ", 259.2, 323.4),
        line("rosecution witnesses. Advocate Roy was given an", 259.0, 552.3),
        line("itnesses. Advocate Roy was given an", 334.8, 551.9),
    ]}]}
    assert extract.blocks_from_dict(textpage)[0].text == "prosecution witnesses. Advocate Roy was given an"


def test_bold_body_face_sets_the_body_size():
    bold_body = [_blk(BODY * 3, 13.0, 60, 100, font="Garamond,Bold", bold=True)]
    side = [_blk(BODY, 11.0, 384, 100, font="RotisSansSerif"), _blk(BODY, 10.0, 384, 300, font="RotisSansSerif")]
    assert extract.font_profile([bold_body + side]) == 13.0
    assert extract.font_profile([side]) == 11.0


def test_activity_arrow_glyph_is_dropped():
    def span(text, font, size, x0):
        return {"text": text, "font": font, "size": size, "flags": 0, "bbox": (x0, 100, x0 + 40, 100 + size)}
    for glyph in ("\x86", "\x02", ""):
        textpage = {"blocks": [{"type": 0, "bbox": (82, 100, 160, 120), "lines": [
            {"dir": (1.0, 0.0), "bbox": (82, 100, 160, 120), "spans": [span(glyph, "TT637T00", 20.0, 82), span(" ", "TT633T00", 11.0, 98), span("Activity", "TT633T00", 11.0, 104)]},
        ]}]}
        assert extract.blocks_from_dict(textpage)[0].text == "Activity"


def test_smaller_box_text_waits_for_the_open_paragraph():
    def block(text, size, y0, role, x0=205):
        b = _blk(text, size, x0, y0)
        b.role = role
        return b
    page4 = extract.Page(3, 4, [
        block("But by the thirteenth and fourteenth centuries paper had become cheaper and", 13.0, 400, "body"),
        block("The value of paper", 15.0, 540, "h3"),
        block("Compare the following:", 12.0, 566, "body"),
    ])
    page5 = extract.Page(4, 5, [block("widely available. People used it to write holy texts.", 13.0, 100, "body")])
    md = extract.to_markdown([page4, page5])
    assert "cheaper and widely available." in md
    assert md.index("cheaper and widely") < md.index("### The value of paper") < md.index("Compare the following:")


def test_tidy_ocr_line_drops_unbalanced_quotes():
    assert extract._tidy_ocr_line("‘Gujarat: ‘apparently fled") == "Gujarat: apparently fled"
    assert extract._tidy_ocr_line("called ‘Hindustan’ by Babur") == "called ‘Hindustan’ by Babur"
    assert extract._tidy_ocr_line("the mansabdars’ horses") == "the mansabdars’ horses"


def test_margin_box_of_outlined_lines_stays_its_own_block():
    import pymupdf
    body = {"type": 0, "bbox": (206, 100, 420, 160), "lines": [
        {"dir": (1.0, 0.0), "bbox": (206, 100, 420, 114), "spans": [{"text": "The Banjaras were the most important", "font": "Bookman", "size": 11.0, "flags": 0, "bbox": (206, 100, 420, 114)}]},
    ]}
    textpage = {"blocks": [body]}
    words = {(429, 104, 498, 112): "Nomads are", (430, 118, 532, 129): "wandering people."}
    extract._fill_outlined_words(None, textpage, [pymupdf.Rect(*k) for k in words], lambda page, r: words[tuple(round(v) for v in r)])
    blocks = extract.blocks_from_dict(textpage)
    assert [b.text for b in blocks] == ["The Banjaras were the most important", "Nomads are wandering people."]


def test_margin_keywords_beside_exercise_questions_are_notes():
    questions = "5. According to the “circle of justice”, why was it important for military commanders to keep the interests of the peasantry in mind?"
    blocks, _ = _page([
        (questions, 12.0, 206, 117, "Bookman-Light"),
        ("10. Why were the Delhi Sultans interested in cutting down forests? Does deforestation occur today?", 12.0, 206, 479, "Bookman-Light"),
        ("KEYWORDS", 11.9, 91, 232, "LucidaSans"),
        ("garrison", 12.9, 103, 343, "Bookman-Light"),
        ("Mongols", 12.9, 103, 370, "Bookman-Light"),
    ])
    roles = {b.text[:8]: b.role for b in blocks}
    assert roles["5. Accor"] == "body" and roles["10. Why "] == "body"
    assert roles["garrison"] == "keyword" and roles["Mongols"] == "keyword"


def test_keywords_column_becomes_a_heading_and_a_list():
    blocks, printed = _page([
        (BODY, 12.0, 206, 117, "Bookman-Light"),
        ("KEYWORDS", 11.9, 91, 232, "LucidaSans"),
        ("iqta", 12.9, 118, 291, "Bookman-LightItalic"),
        ("garrison", 12.9, 103, 343, "Bookman-Light"),
        ("Mongols", 12.9, 103, 370, "Bookman-Light"),
    ])
    assert [b.role for b in blocks] == ["body", "keyword", "keyword", "keyword", "keyword"]
    md = extract.to_markdown([extract.Page(0, printed, blocks)], 600.0)
    assert "### Keywords\n\n- iqta\n\n- garrison\n\n- Mongols" in md


def test_clipped_shadow_copies_of_a_heading_are_dropped():
    def line(text, bbox):
        return {"dir": (1.0, 0.0), "bbox": bbox, "spans": [{"text": text, "font": "RotisSansSerif-Ext", "size": 24.0, "flags": 0, "bbox": bbox}]}
    lines = [line("Bhopal Gas T", (103, 47, 237, 71)), line("Bhopal Gas T", (102, 47, 237, 71)), line("Bhopal Gas Tragedy", (102, 46, 307, 71)), line("ragedy", (236, 47, 306, 71))]
    from ncert_diff import clean
    texts = [extract._join_spans(spans) for spans in extract._dedupe_shadow_spans(lines)]
    assert clean.join_lines(texts) == "Bhopal Gas Tragedy"


def test_wrapped_list_item_in_two_blocks_is_one_item():
    blocks, _ = _page([
        ("- If a group of people are not given permission to open a", 11.0, 251, 634, "RotisSansSerif-Ext"),
        ("Telugu-medium school in Kerala.", 11.0, 260, 647, "RotisSansSerif-Ext"),
        ("Fundamental Rights are guaranteed by the Constitution to every citizen of the country.", 11.0, 251, 700, "RotisSansSerif-Ext"),
    ])
    assert [b.text for b in blocks][:2] == ["- If a group of people are not given permission to open a Telugu-medium school in Kerala.", "Fundamental Rights are guaranteed by the Constitution to every citizen of the country."]


def test_outlined_first_line_of_a_paragraph_is_not_a_heading():
    import pymupdf
    body = {"type": 0, "bbox": (206, 300, 546, 360), "lines": [
        {"dir": (1.0, 0.0), "bbox": (206, 300, 546, 314), "spans": [{"text": "establishment, as well as for the construction of temples and forts.", "font": "Bookman-Light", "size": 11.0, "flags": 0, "bbox": (206, 300, 546, 314)}]},
    ]}
    textpage = {"blocks": [body]}
    run = (206, 284, 540, 296)
    extract._fill_outlined_words(None, textpage, [pymupdf.Rect(*run)], lambda page, r: "These resources were used to finance the kings")
    blocks = extract.blocks_from_dict(textpage)
    extract.classify(blocks, 600.0, 800.0, 11.0)
    assert [b.role for b in blocks] == ["body"] or [b.role for b in blocks] == ["body", "body"]
    assert not any(b.role in ("h2", "h3") for b in blocks)


def test_imagine_box_label_is_a_heading_that_ends_the_paragraph_before_it():
    blocks, printed = _page([
        ("This brought them into conflict with larger and more complex kingdoms and empire", 12.0, 75, 600, "Bookman-Light"),
        ("Imagine", 12.9, 149, 76, "CIDFont+F9"),
        ("You are a member of a nomadic community that shifts residence every three months. How would this change your life?", 12.9, 163, 121, "CIDFont+F1"),
    ])
    roles = {b.text[:7]: b.role for b in blocks}
    assert roles["Imagine"] == "h3"
    md = extract.to_markdown([extract.Page(0, printed, blocks)], 600.0)
    assert "### Imagine" in md and "empire Imagine" not in md


def test_fragment_finishing_a_word_joins_without_a_space():
    import pymupdf
    body = {"type": 0, "bbox": (75, 600, 400, 614), "lines": [
        {"dir": (1.0, 0.0), "bbox": (75, 600, 400, 614), "spans": [{"text": "complex kingdoms and empire", "font": "Bookman-Light", "size": 12.0, "flags": 0, "bbox": (75, 600, 232, 614)}]},
    ]}
    textpage = {"blocks": [body]}
    extract._fill_outlined_words(None, textpage, [pymupdf.Rect(232.5, 602, 240, 613)], lambda page, r: "s.")
    assert extract.blocks_from_dict(textpage)[0].text == "complex kingdoms and empires."
    # The crop can take in the last letter of the word before it.
    textpage["blocks"][0]["lines"][0]["spans"] = textpage["blocks"][0]["lines"][0]["spans"][:1]
    extract._fill_outlined_words(None, textpage, [pymupdf.Rect(232.5, 602, 240, 613)], lambda page, r: "es.")
    assert extract.blocks_from_dict(textpage)[0].text == "complex kingdoms and empires."


def test_keywords_column_set_as_a_sentence_per_line_is_one_note():
    # Page 73 of the 2020 Our Pasts II chapter 5: the KEYWORDS column holds an instruction,
    # one line per block at a 19 pt pitch, not a list of terms.
    def block(text, bbox, size=12.0, font="Bookman-Light"):
        span = {"text": text, "size": size, "font": font, "flags": 0, "bbox": bbox}
        return {"type": 0, "bbox": bbox, "lines": [{"dir": (1.0, 0.0), "bbox": bbox, "spans": [span]}]}
    textpage = {"blocks": [
        block(BODY, (91, 100, 425, 200), 13.0),
        block("KEYWORDS", (466, 289, 542, 306)),
        block("Go through the", (459, 348, 550, 360)),
        block("chapter and make", (451, 367, 557, 379)),
        block("your own list of", (459, 386, 550, 398)),
        block("six keywords.", (465, 405, 544, 417)),
        block("For each of these,", (453, 433, 556, 445)),
        block("write a sentence", (457, 452, 551, 464)),
        block("indicating", (474, 471, 534, 483)),
        block("why you chose", (461, 490, 547, 502)),
        block("the word.", (477, 509, 532, 521)),
    ]}
    blocks = extract.blocks_from_dict(textpage)
    extract.classify(blocks, 630.0, 842.0, 13.0)
    texts = {b.text: b.role for b in blocks}
    assert texts["KEYWORDS"] == "keyword"
    assert texts["Go through the chapter and make your own list of six keywords. For each of these, write a sentence indicating why you chose the word."] == "note"
    assert len(blocks) == 3
