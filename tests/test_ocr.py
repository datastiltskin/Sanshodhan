from ncert_diff import ocr

HEADER = "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext"


def row(block, par, line, word, left, top, width, height, conf, text):
    return f"5\t1\t{block}\t{par}\t{line}\t{word}\t{left}\t{top}\t{width}\t{height}\t{conf}\t{text}"


def test_blocks_from_tsv_groups_paragraphs_and_drops_noise():
    tsv = "\n".join([
        HEADER,
        row(1, 1, 1, 1, 300, 1000, 200, 60, 96, "Ruling"),
        row(1, 1, 1, 2, 520, 1000, 150, 60, 95, "as"),
        row(1, 1, 2, 1, 300, 1080, 400, 60, 97, "large"),
        row(1, 1, 2, 2, 720, 1080, 100, 60, 90, "a"),
        row(2, 1, 1, 1, 1800, 2000, 90, 40, 31, "ik"),        # low-confidence picture noise
        row(2, 1, 1, 2, 1900, 2000, 20, 40, 28, "2"),
        row(3, 1, 1, 1, 400, 3300, 300, 40, 93, "0760CH04"),  # print slug
    ])
    blocks, conf = ocr.blocks_from_tsv(tsv, 72 / 300)
    assert [b.text for b in blocks] == ["Ruling as large a"]
    b = blocks[0]
    assert round(b.x0) == 72 and round(b.y0) == 240  # pixels scaled to points
    assert 10 <= b.size <= 13  # 60 px line at 300 dpi is about 14 pt tall, scaled by 0.8
    assert conf > 90


def test_restore_dropcap_uses_the_books_own_vocabulary():
    from ncert_diff.editions import restore_dropcap

    vocab = {"ruling", "as", "in", "on", "an", "chapter", "we"}
    bigrams = {("ruling", "as"), ("in", "chapter")}
    md = "<!-- page 45 (pdf 1) -->\n\n# THE MUGHAL EMPIRE\n\nuling as large a territory.\n"
    fixed, word = restore_dropcap(md, vocab, bigrams)
    assert word == "Ruling" and "\nRuling as large" in fixed
    md = "# T\n\nn Chapter 2 we saw.\n"
    fixed, word = restore_dropcap(md, vocab, bigrams)
    assert word == "In"  # "on" and "an" also exist, the bigram with "chapter" decides
    md = "# T\n\nxyzzy nothing known.\n"
    assert restore_dropcap(md, vocab, bigrams) == (md, None)
    md = "# T\n\nAlready fine.\n"
    assert restore_dropcap(md, vocab, bigrams) == (md, None)


def test_clean_outlined():
    assert ocr.clean_outlined("pardes i |\n") == "pardes i"
    assert ocr.clean_outlined("EX€YIcise.") == "EXYIcise."
    assert ocr.clean_outlined("dehliwal,") == "dehliwal,"
    assert ocr.clean_outlined("|| 1") == ""


def test_snap_to_vocabulary_repairs_outlined_runs():
    words = {"exercise", "pardesi", "for", "minhaj-i-siraj", "difficult", "official", "records", "jati", "a", "sanskrit", "prashasti", "simple", "old"}
    index = ocr.vocabulary_index(words)
    snap = lambda t: ocr.snap_to_vocabulary(t, index, words)  # noqa: E731
    assert snap("simple EXYIcise.") == "simple exercise."
    assert snap("pardes i") == "pardesi"
    assert snap("fi or") == "for"
    assert snap("Minhaj 1 Siraj,") == "Minhaj-i-Siraj,"
    assert snap("Ufficult. The") == "difficult. The"
    assert snap("Jatt") == "Jati"
    assert snap("Sikhs,") == "Sikhs,"  # an unknown word with nothing close is left alone
    assert snap("and more diffi ifficult.") == "and more difficult."
