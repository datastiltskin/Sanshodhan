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


def _raw_block(text, bbox, size=11.0, font="Bookman-Light", flags=0):
    span = {"text": text, "size": size, "font": font, "flags": flags, "bbox": bbox}
    return {"type": 0, "bbox": bbox, "lines": [{"dir": (1.0, 0.0), "bbox": bbox, "spans": [span]}]}


def test_activity_box_in_the_margin_does_not_split_the_column_sentence():
    # Pages 3 and 4 of the 2019 Our Pasts III chapter 1: the Activity box sits at body size
    # beside the paragraph that ends "dominated" at the foot of page 3 and goes on "social
    # life." on page 4.
    p3 = {"blocks": [
        _raw_block("When we write history, or a story, we divide it into chapters. Why do we do this? It is to give each chapter some coherence.", (91, 276, 397, 432)),
        _raw_block("Mill thought that all Asian societies were at a lower level of civilisation than Europe. Religious intolerance, caste taboos and superstitious practices dominated", (91, 664, 397, 728)),
        _raw_block("Activity", (436, 567, 477, 581), font="TT633T00"),
        _raw_block("Interview your mother or another member of your family to find out about their life.", (425, 586, 546, 718), font="TT615T00"),
    ]}
    p4 = {"blocks": [
        _raw_block("social life. British rule, Mill felt, could civilise India. To do this, it was necessary to introduce European manners.", (233, 98, 539, 202)),
        _raw_block("In this idea of history, British rule represented all the forces of progress and civilisation.", (233, 207, 539, 300)),
    ]}
    pages = []
    for n, d in enumerate((p3, p4)):
        blocks = extract.blocks_from_dict(d)
        extract.classify(blocks, 630.0, 842.0, 11.0)
        pages.append(extract.Page(n, 3 + n, blocks))
    md = extract.to_markdown(pages, 630.0)
    assert "dominated social life. British rule" in md
    assert "\nInterview your mother or another member of your family to find out about their life.\n" in md
    assert md.index("### Activity") > md.index("dominated social life")


def test_glossary_column_and_source_box_title_do_not_end_the_column_paragraph():
    # Pages 67 and 68 of the 2019 Our Pasts III chapter 6: four glossary entries at body size
    # in the margin column beside a paragraph that runs over the page, and a Source box with
    # its own title read before the column on page 68.
    p67 = {"blocks": [
        _raw_block("Colonialism and the City", (91, 90, 397, 110), size=20.0, font="TT633T00"),
        _raw_block("Set amidst densely packed mohallas and several dozen bazaars, the Jama Masjid was among the largest and grandest mosques in India.", (91, 610, 397, 660)),
        _raw_block("Delhi during Shah Jahan’s time was also an important centre of Sufi culture. No wonder the poet Mir Taqi Mir said, “The", (91, 666, 397, 729)),
        _raw_block("Dargah – The tomb of a Sufi saint", (420, 509, 554, 534)),
        _raw_block("Khanqah – A sufi lodge, often used as a rest house for travellers", (420, 541, 557, 644)),
        _raw_block("Idgah – An open prayer place of Muslims primarily meant for id prayers", (420, 651, 559, 689)),
        _raw_block("Cul-de-sac – Street with a dead end", (420, 697, 555, 721)),
    ]}
    p68 = {"blocks": [
        _raw_block("“Dilli jo ek shahr tha alam mein intikhab...”", (73, 434, 212, 469), size=16.0, font="TT62BT00"),
        _raw_block("By 1739, Delhi had been sacked by Nadir Shah and plundered many times. Expressing the sorrow of those who witnessed it, Mir said:", (79, 483, 206, 587), font="TT63CT00"),
        _raw_block("streets of Delhi aren’t mere streets; they are like the album of a painter.”", (359, 99, 538, 137)),
        _raw_block("Yet, even this was no ideal city, and its delights were enjoyed only by some. There were sharp divisions between rich and poor.", (359, 142, 538, 298)),
        _raw_block("The Making of New Delhi", (233, 541, 441, 558), size=17.0, font="TT633T00"),
        _raw_block("In 1803, the British gained control of Delhi after defeating the Marathas. Since the capital of British India was Calcutta, the emperor stayed.", (233, 566, 538, 656)),
        _raw_block("Before 1857, developments in Delhi were somewhat different from those in other colonial cities.", (233, 685, 538, 735)),
    ]}
    pages = []
    for n, d in enumerate((p67, p68)):
        blocks = extract.blocks_from_dict(d)
        extract.classify(blocks, 630.0, 842.0, 11.0)
        pages.append(extract.Page(n, 67 + n, blocks))
    md = extract.to_markdown(pages, 630.0)
    assert "Mir Taqi Mir said, “The streets of Delhi aren’t mere streets" in md
    for entry in ("Dargah – The tomb of a Sufi saint", "Idgah – An open prayer place of Muslims primarily meant for id prayers", "Cul-de-sac – Street with a dead end"):
        assert f"\n{entry}\n" in md
    assert "\n## “Dilli jo ek shahr tha alam mein intikhab...”\n" in md


def test_big_questions_title_set_in_two_overlapping_blocks_is_one_heading():
    # Page 27 of Exploring Society part 1 chapter 2: "The Big" (12 pt, with a 23 pt "Big")
    # overlaps "Questions" (18 pt) set below and to the right of it.
    textpage = {"blocks": [
        _raw_block("Understanding the Weather", (64, 78, 303, 158), size=30.0, font="NotoSerif-SemiBold", flags=16),
        _raw_block("A change in the weather is sufficient to create the world and oneself anew, a long line of verse.", (99, 187, 418, 223), size=12.0, font="NotoSerif-Italic"),
        {"type": 0, "bbox": (64, 597, 130, 630), "lines": [{"dir": (1.0, 0.0), "bbox": (64, 597, 130, 630), "spans": [
            {"text": "The ", "size": 12.0, "font": "NotoSerif-Bold", "flags": 16, "bbox": (64, 610, 88, 627)},
            {"text": "Big", "size": 23.0, "font": "NotoSerif-Bold", "flags": 16, "bbox": (88, 597, 125, 630)},
            {"text": " ", "size": 12.0, "font": "NotoSerif-Bold", "flags": 16, "bbox": (125, 610, 130, 627)},
        ]}]},
        _raw_block("Questions", (82, 619, 174, 645), size=18.0, font="NotoSerif-Bold", flags=16),
        _raw_block("1. How can we measure and monitor the weather around us?", (223, 596, 445, 633), size=13.0, font="NotoSerif-Italic"),
    ]}
    blocks = extract.blocks_from_dict(textpage)
    extract.classify(blocks, 592.8, 842.0, 12.0)
    md = extract.to_markdown([extract.Page(0, 27, blocks)], 592.8)
    assert "## The Big Questions" in md
    assert "\nThe Big\n" not in md and "## Questions\n" not in md


def test_map_axis_ticks_are_dropped_and_cut_from_the_caption_they_landed_on():
    # Page 119 of Exploring Society part 1 chapter 6: the outlined ticks at the map's bottom
    # edge are read back onto the caption line beside them, and the "60E" left of it stays a
    # block of its own.
    blocks = [
        extract.Block(106, 564, 463, 592, "NotoSerif-Medium", 10.0, False, True, "70E 80E 90E Fig. 6.2. Prominent dynasties of India during the age of reorganisation", 10.0),
        extract.Block(77, 564, 98, 571, "OUTLINED", 5.9, False, False, "60E", 5.9),
        extract.Block(77, 48, 98, 55, "OUTLINED", 5.9, False, False, "70°E 75°E", 5.9),
        extract.Block(73, 100, 520, 300, "NotoSerif-Regular", 12.0, False, False, BODY, 12.0),
    ]
    extract.classify(blocks, 592.8, 842.0, 12.0)
    assert blocks[0].text == "Fig. 6.2. Prominent dynasties of India during the age of reorganisation"
    assert blocks[0].role == "caption"
    assert blocks[1].role == blocks[2].role == "decoration"


def test_side_by_side_captions_keep_their_own_second_lines():
    # Page 10 of Exploring Society part 1 chapter 1: two rows of photos with a caption under
    # each, the second lines set as blocks of their own, and the first lines of Fig. 1.13
    # and Fig. 1.14 in one PyMuPDF line.
    def cap(text, bbox):
        return _raw_block(text, bbox, size=10.0, font="NotoSerif-MediumItalic", flags=2)
    pair = {"type": 0, "bbox": (93, 394, 504, 408), "lines": [
        {"dir": (1.0, 0.0), "bbox": (93, 394, 291, 408), "spans": [{"text": "Fig. 1.13. Multi-cropping in Uttar Pradesh", "size": 10.0, "font": "NotoSerif-MediumItalic", "flags": 2, "bbox": (93, 394, 291, 408)}]},
        {"dir": (1.0, 0.0), "bbox": (330, 394, 504, 408), "spans": [{"text": "Fig. 1.14. Rural women working in a ", "size": 10.0, "font": "NotoSerif-MediumItalic", "flags": 2, "bbox": (330, 394, 504, 408)}]},
    ]}
    textpage = {"blocks": [
        cap("Fig. 1.11. Modern agricultural practices ", (97, 212, 291, 227)),
        cap("Fig. 1.12. Aerial view of Delhi with the ", (326, 212, 508, 227)),
        cap("in the plains", (162, 224, 221, 239)),
        cap("river Yamuna on top right", (353, 224, 478, 239)),
        pair,
        cap("paddy field in West Bengal", (353, 406, 486, 420)),
        _raw_block(BODY, (161, 429, 532, 531), size=12.0, font="NotoSerif-Regular"),
    ]}
    blocks = extract.blocks_from_dict(textpage)
    extract.classify(blocks, 592.8, 842.0, 12.0)
    captions = sorted(b.text for b in blocks if b.role == "caption")
    assert captions == [
        "Fig. 1.11. Modern agricultural practices in the plains",
        "Fig. 1.12. Aerial view of Delhi with the river Yamuna on top right",
        "Fig. 1.13. Multi-cropping in Uttar Pradesh",
        "Fig. 1.14. Rural women working in a paddy field in West Bengal",
    ]


def test_caption_line_in_the_captions_face_goes_on_with_it_but_a_description_does_not():
    # Page 11 of Exploring Society part 1 chapter 1 ("... in Bandhavgarh" over "National
    # Park, Madhya Pradesh", the second line overlapping the first), and page 3 of the 2014
    # Our Pasts III chapter 1, where the description is a paragraph of its own under the
    # caption title, in the same face, after a gap.
    blocks = [
        extract.Block(330, 300, 520, 330, "NotoSerif-MediumItalic", 10.0, False, True, "Fig. 1.17. The Northern plains grey langur sits on a wooden beam in Bandhavgarh", 10.0),
        extract.Block(380, 327, 500, 341, "NotoSerif-MediumItalic", 10.0, False, True, "National Park, Madhya Pradesh", 10.0),
        extract.Block(404, 502, 552, 532, "Bookman-LightItalic", 9.0, False, True, "Fig. 3 – Warren Hastings became the first Governor-General of India in 1773", 9.0),
        extract.Block(404, 537, 552, 589, "Bookman-LightItalic", 9.0, False, True, "While history books narrated the deeds of Governor-Generals, biographies glorified them.", 9.0),
    ]
    for b in blocks:
        b.role = "caption"
    extract._stack_caption_lines(blocks)
    assert [b.text for b in blocks] == [
        "Fig. 1.17. The Northern plains grey langur sits on a wooden beam in Bandhavgarh National Park, Madhya Pradesh",
        "Fig. 3 – Warren Hastings became the first Governor-General of India in 1773",
        "While history books narrated the deeds of Governor-Generals, biographies glorified them.",
    ]


def test_spaces_the_page_does_not_show_are_dropped():
    # Exploring Society part 1: "The g overnment" (ch10 p223, a space with no advance),
    # "Kaṇṇ agi" (ch6 p131, the second "ṇ" zero wide and the space as wide as the letter),
    # "cold s torage" (ch12 p257, a thin space). "story of Kaṇṇagi" keeps its word spaces,
    # which a kern pulls the next letter into.
    # Sizes are 10 pt, as in the caption.
    def line(chars):
        return {"spans": [{"size": 10.0, "chars": [{"c": c, "bbox": (x0, 0, x1, 10)} for c, x0, x1 in chars]}]}
    cases = [
        ([("e", 100.9, 107.32), (" ", 107.38, 110.5), ("g", 116.75, 123.2), (" ", 123.26, 126.38), ("o", 123.26, 130.19), ("v", 130.25, 137.19)], "e gov"),
        ([("n", 372.39, 378.58), ("̣", 378.58, 378.58), ("n", 378.58, 378.58), ("̣", 378.58, 378.58), (" ", 378.58, 384.77), ("a", 384.77, 390.8)], "ṇṇa"),
        ([("d", 266.65, 273.66), (" ", 273.72, 276.48), ("s", 277.52, 282.94), (" ", 283.0, 285.4), ("t", 285.4, 289.0)], "d st"),
        ([("y", 120.53, 127.31), (" ", 127.37, 130.49), ("o", 128.79, 135.72), ("f", 135.78, 140.21), (" ", 140.27, 143.39), ("K", 141.7, 150.1)], "y of K"),
        # "broke off and" (ch5 p108): the ligature leaves the second "f" zero wide, and the
        # space after it is an ordinary one.
        ([("o", 484.22, 491.14), ("f", 491.2, 499.7), ("f", 499.7, 499.7), (" ", 499.76, 502.88), ("a", 506.61, 513.37)], "off a"),
    ]
    for chars, expected in cases:
        ln = line(chars)
        extract._text_from_chars(ln)
        assert ln["spans"][0]["text"] == expected


def test_photo_badge_numbers_are_not_paragraphs():
    # Page 7 of Exploring Society part 1 chapter 1: the badges 1 to 7 on the photo collage
    # sit in the body column at body size.
    blocks = [
        extract.Block(64, 100, 520, 300, "NotoSerif-Regular", 12.0, False, False, BODY, 12.0),
        extract.Block(120, 320, 128, 334, "NotoSans-Bold", 12.0, False, False, "1", 12.0),
        extract.Block(300, 320, 330, 334, "NotoSans-Bold", 12.0, False, False, "4 5", 12.0),
        extract.Block(64, 400, 520, 500, "NotoSerif-Regular", 12.0, False, False, "2. " + BODY, 12.0),
    ]
    extract.classify(blocks, 592.8, 842.0, 12.0)
    assert [b.role for b in blocks] == ["body", "decoration", "decoration", "body"]


def test_a_figure_label_or_a_note_label_starts_a_new_aside():
    # Exploring Society: photo-grid captions carry no closing punctuation (part 1 p10), and a
    # margin note's bold label follows a caption that ends in a handle (part 2 p158).
    lines = [
        "> [caption] Fig. 1.11. Modern agricultural practices in the plains", "",
        "> [caption] Fig. 1.12. Aerial view of Delhi with the river Yamuna on top right", "",
        "> [caption] Fig. 6.15. The official X account to reach out to Indian Railways @RailwaySeva", "",
        "> [caption] Transparency:", "",
    ]
    out = [ln for ln in extract._merge_split_asides(lines) if ln]
    assert out == [
        "> [caption] Fig. 1.11. Modern agricultural practices in the plains",
        "> [caption] Fig. 1.12. Aerial view of Delhi with the river Yamuna on top right",
        "> [caption] Fig. 6.15. The official X account to reach out to Indian Railways @RailwaySeva",
        "> [caption] Transparency:",
    ]


def test_centred_speech_bubble_lines_are_one_block():
    # Page 47 of the 2019 Social and Political Life II chapter 4: two bubbles side by side,
    # each cut into blocks of a line or two, centred on its own axis.
    def bubble(text, bbox):
        return extract.Block(*bbox, "TT351T00", 10.0, False, False, text, 10.0)
    blocks = [
        bubble("Ma, we are going on a school excursion. Rosie Ma’am", (90, 112, 213, 133)),
        bubble("needs volunteers. Can’t you", (96, 133, 207, 143)),
        bubble("take a holiday from office", (101, 145, 202, 155)),
        bubble("and volunteer?", (122, 156, 181, 166)),
        bubble("Shonali, how can you say that! You know that Jaspreet aunty is up at 5 a.m.", (356, 79, 436, 122)),
        bubble("everyday doing all", (360, 123, 432, 133)),
        bubble("the housework!", (364, 134, 428, 144)),
        bubble("How would I know? I’m on strike, remember? Besides, Mangala has also", (178, 738, 268, 770)),
        bubble("taken leave today.", (191, 771, 254, 781)),
    ]
    for b in blocks:
        b.role = "table"
    blocks[-1].role = "footer"  # it sits in the footer band
    extract._stack_centred_lines(blocks)
    assert sorted(b.text for b in blocks) == [
        "How would I know? I’m on strike, remember? Besides, Mangala has also taken leave today.",
        "Ma, we are going on a school excursion. Rosie Ma’am needs volunteers. Can’t you take a holiday from office and volunteer?",
        "Shonali, how can you say that! You know that Jaspreet aunty is up at 5 a.m. everyday doing all the housework!",
    ]


def test_wide_box_title_set_smaller_beside_the_column_is_a_margin_box():
    # Pages 57 and 58 of the 2024 Our Pasts II chapter 5: the box title beside the column is
    # wider than a narrow margin, but a point smaller than the body, and must not run into the
    # first paragraph of page 58.
    def blk(text, bbox, size, font="CIDFont+F3"):
        return extract.Block(*bbox, font, size, False, False, text, size)
    p57 = [
        blk("The Ahoms migrated to the Brahmaputra valley from present-day Myanmar in the thirteenth century.", (72, 246, 325, 428), 12.9),
        blk("The Ahom state depended upon forced labour. As a result, the administration became quite centralised.", (72, 567, 325, 703), 12.9),
        blk("Lachit Barphukan and the defeat of the Mughals in Assam", (344, 82, 538, 110), 11.9, "CIDFont+F5"),
    ]
    p58 = [
        blk("Discuss why the Mughals were interested in the land of the Gonds.", (76, 351, 178, 407), 11.9, "CIDFont+F7"),
        blk("Almost all adult males served in the army during war. At other times, they built dams.", (206, 77, 545, 137), 12.9),
        blk("Ahom society was divided into clans or khels. There were very few castes of artisans.", (206, 146, 546, 237), 12.9),
    ]
    pages = []
    for n, blocks in enumerate((p57, p58)):
        extract.classify(blocks, 612.0, 792.0, 12.9)
        pages.append(extract.Page(n, 57 + n, blocks))
    md = extract.to_markdown(pages, 612.0)
    assert "\nLachit Barphukan and the defeat of the Mughals in Assam\n" in md
    assert "\nAlmost all adult males served" in md


def test_centred_poem_lines_and_lettered_questions_stay_apart():
    # Page 96 of Social and Political Life III chapter 8 (a centred poem) and the lettered
    # questions of chapter 10 page 121.
    def blk(text, bbox):
        b = extract.Block(*bbox, "Bookman", 10.0, False, True, text, 10.0)
        b.role = "note"
        return b
    blocks = [
        blk("The body is polluted from within,", (200, 100, 360, 112)),
        blk("Be sure of it says the Mahari Chokha", (190, 112, 370, 124)),
        blk("a) What is the minimum wage for a construction worker?", (100, 300, 420, 312)),
        blk("b) Do you think it is adequate, low or high?", (120, 312, 400, 324)),
    ]
    extract._stack_centred_lines(blocks)
    for b in blocks:
        b.role = "caption"
    extract._stack_caption_lines(blocks)
    assert len(blocks) == 4


def test_text_running_off_the_page_edge_is_dropped():
    # Page 66 of the 2007 Our Pasts II chapter 5 (the 2014 snapshot): the ends of the facing
    # page's caption lines reach this page past its left edge.
    blocks = [
        extract.Block(-7, 531, 26, 554, "BookmanPlain", 10.0, False, False, "hmir, 634.", 10.0),
        extract.Block(73, 100, 500, 300, "BookmanPlain", 13.0, False, False, BODY, 13.0),
    ]
    extract.classify(blocks, 595.0, 842.0, 13.0)
    assert [b.role for b in blocks] == ["decoration", "body"]


def test_bar_chart_values_are_kept():
    # Page 89 of the 2019 Social and Political Life III chapter 7: the values over the bars.
    blocks = [
        extract.Block(64, 100, 520, 300, "Bookman", 12.0, False, False, BODY, 12.0),
        extract.Block(100, 320, 400, 334, "Bookman", 12.0, False, False, "74 63 57 74 67 71 86", 12.0),
    ]
    extract.classify(blocks, 592.8, 842.0, 12.0)
    assert blocks[1].role != "decoration"


def test_flush_left_wrapped_lines_of_two_exercise_columns_do_not_interleave():
    # Page 47 of the 2024 Social and Political Life II chapter 4: question 2 on the left and
    # statement d. of question 1 on the right, each wrapping into a block of its own.
    def blk(text, bbox, font):
        b = extract.Block(*bbox, font, 9.6, False, False, text, 9.6)
        b.role = "table"
        return b
    blocks = [
        blk("‘invisible’, ‘physically demanding’, and ‘time consuming’? Give one example of each based on the household tasks", (82, 238, 358, 263), "CIDFont+F2"),
        blk("d. The work that women do is less", (376, 264, 545, 275), "CIDFont+F1"),
        blk("undertaken by women in your home.", (82, 267, 252, 277), "CIDFont+F2"),
        blk("valued than that of men.", (376, 279, 497, 289), "CIDFont+F1"),
    ]
    extract._stack_centred_lines(blocks)
    assert sorted(b.text for b in blocks) == [
        "d. The work that women do is less valued than that of men.",
        "‘invisible’, ‘physically demanding’, and ‘time consuming’? Give one example of each based on the household tasks undertaken by women in your home.",
    ]


def test_opaque_side_font_is_inferred_from_the_file_profile():
    # The 2015 Our Pasts II files: Bookman-Light 13 body, Lucida Sans embedded as TT3DBT00 at 12.
    body = extract.Block(90, 100, 425, 300, "Bookman-Light", 13.0, False, False, BODY)
    note = extract.Block(216, 400, 520, 460, "TT3DBT00", 12.0, False, False, "Make a list of the languages mentioned by Amir Khusrau. Prepare another list of the names of languages spoken today.")
    assert extract.inferred_side_fonts([[body, note]], 13.0) == ("TT3DBT00",)
    # A file whose body face is itself opaque (the civics files) infers nothing.
    body2 = extract.Block(90, 100, 425, 300, "TT18AT00", 13.0, False, False, BODY)
    assert extract.inferred_side_fonts([[body2, note]], 13.0) == ()
    blocks = [body, note]
    extract.classify(blocks, 630.0, 842.0, 13.0, side_fonts=("TT3DBT00",))
    assert [b.role for b in blocks] == ["body", "note"]


def test_overprinted_label_is_a_heading_over_its_paragraph():
    # Page 49 of the 2007 Our Pasts II chapter 4: "Shah Jahan 1627-1658" drawn five times (the
    # file's bold), then its paragraph in the plain face, all at 11 pt under a 13 pt body.
    def line(spans, y):
        return {"dir": (1.0, 0.0), "bbox": (89, y, 403, y + 12), "spans": [dict(sp, bbox=(sp["x0"], y, sp["x1"], y + 12)) for sp in spans]}
    def span(text, x0, x1, flags=4):
        return {"text": text, "font": "BookmanPlain", "size": 11.0, "flags": flags, "x0": x0, "x1": x1}
    copies = [span("Shah Jahan 1627-1658", 89 + 0.3 * k, 210 + 0.3 * k) for k in range(5)]
    body_lines = ["Mughal campaigns continued in the Deccan under", "Shah Jahan. The Afghan noble Khan Jahan Lodi", "rebelled and was defeated. Campaigns were launched", "against Ahmadnagar; the Bundelas were defeated."]
    lines = [line(copies, 269)] + [line([span(t, 89, 400)], 283 + 14 * k) for k, t in enumerate(body_lines)]
    textpage = {"blocks": [
        {"type": 0, "bbox": (89, 100, 403, 200), "lines": [{"dir": (1.0, 0.0), "bbox": (89, 100, 403, 112), "spans": [{"text": BODY, "font": "BookmanPlain", "size": 13.0, "flags": 4, "bbox": (89, 100, 403, 112)}]}]},
        {"type": 0, "bbox": (89, 269, 403, 339), "lines": lines},
    ]}
    blocks = extract.blocks_from_dict(textpage)
    assert [b.text[:20] for b in blocks] == [BODY[:20], "Shah Jahan 1627-1658", "Mughal campaigns con"]
    assert blocks[1].bold and not blocks[2].bold
    extract.classify(blocks, 595.0, 842.0, 13.0)
    assert [b.role for b in blocks] == ["body", "h3", "body"]


def test_bold_label_opening_a_line_splits_off_as_a_heading():
    # "Jahangir 1605-1627" in a Demi face on the same line as the first sentence (2015 file).
    def line(spans, y):
        return {"dir": (1.0, 0.0), "bbox": (237, y, 534, y + 12), "spans": [dict(sp, bbox=(sp["x0"], y, sp["x1"], y + 12)) for sp in spans]}
    first = [{"text": "Jahangir 1605-1627", "font": "Bookman-Demi", "size": 11.0, "flags": 20, "x0": 237, "x1": 345},
             {"text": " Military campaigns started by Akbar continued.", "font": "Bookman-Light", "size": 11.0, "flags": 4, "x0": 345, "x1": 534}]
    more = ["The Sisodiya ruler of Mewar, Amar Singh, accepted", "Mughal service. Less successful campaigns against", "the Sikhs, the Ahoms and Ahmadnagar followed."]
    lines = [line(first, 137)] + [line([{"text": t, "font": "Bookman-Light", "size": 11.0, "flags": 4, "x0": 237, "x1": 534}], 151 + 14 * k) for k, t in enumerate(more)]
    textpage = {"blocks": [{"type": 0, "bbox": (237, 137, 534, 205), "lines": lines}]}
    blocks = extract.blocks_from_dict(textpage)
    assert [b.text[:22] for b in blocks] == ["Jahangir 1605-1627", "Military campaigns sta"]
    extract.classify(blocks, 630.0, 842.0, 13.0)
    assert [b.role for b in blocks] == ["h3", "body"]
    # A lead-in with a colon stays in its sentence.
    colon = [{"text": "Transparency:", "font": "Bookman-Demi", "size": 11.0, "flags": 20, "x0": 237, "x1": 320},
             {"text": " the state must act openly and be seen to do so.", "font": "Bookman-Light", "size": 11.0, "flags": 4, "x0": 320, "x1": 534}]
    assert extract._bold_lead(line(colon, 100)["spans"]) == ([], line(colon, 100)["spans"])


def test_two_line_overprinted_label_with_its_paragraph_beside_it():
    # Page 48 of the 2007 Our Pasts II chapter 4: "AKBAR" over "1556-1605", each drawn five
    # times, with the paragraph starting beside the label on the same line.
    def span(text, x0, x1, y):
        return {"text": text, "font": "BookmanPlain", "size": 11.0, "flags": 4, "bbox": (x0, y, x1, y + 12)}
    def line(spans, y):
        return {"dir": (1.0, 0.0), "bbox": (89, y, 403, y + 12), "spans": spans}
    lines = [line([span(" AKBAR", 89 + 0.3 * k, 150 + 0.3 * k, 456) for k in range(5)], 456),
             line([span("1556-1605", 89 + 0.3 * k, 160 + 0.3 * k, 469) for k in range(5)], 469)]
    words = "Akbar was 13 years old when he became emperor. His reign can be divided into three periods. Akbar was 13 years old when he became emperor.".split()
    for k, i in enumerate(range(0, len(words), 7)):
        lines.append(line([span(" ".join(words[i:i + 7]), 187, 403, 455 + 13 * k)], 455 + 13 * k))
    textpage = {"blocks": [
        {"type": 0, "bbox": (89, 100, 403, 200), "lines": [line([span(BODY, 89, 403, 100)], 100)]},
        {"type": 0, "bbox": (89, 455, 403, 520), "lines": lines},
    ]}
    for ln in textpage["blocks"][0]["lines"]:
        ln["spans"][0]["size"] = 13.0
    blocks = extract.blocks_from_dict(textpage)
    assert [b.text[:24] for b in blocks] == [BODY[:24], "AKBAR 1556-1605", "Akbar was 13 years old w"]
    extract.classify(blocks, 595.0, 842.0, 13.0)
    assert [b.role for b in blocks] == ["body", "h3", "body"]
