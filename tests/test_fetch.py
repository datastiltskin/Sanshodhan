from pathlib import Path

from ncert_diff import fetch


def test_readable_member_name():
    assert fetch.readable_member_name("gess1dd/gess104.pdf", "gess1", None) == "ch04.pdf"
    assert fetch.readable_member_name("GESS1PS.PDF", "gess1", None) == "prelims.pdf"
    assert fetch.readable_member_name("gees201.pdf", "gees2", 2) == "part2-ch01.pdf"
    assert fetch.readable_member_name("gess1cs.pdf", "gess1", None) == "gess1cs.pdf"
    assert fetch.readable_member_name("__MACOSX/._gess101.pdf", "gess1", None) is None
    assert fetch.readable_member_name("readme.txt", "gess1", None) is None


def test_looks_valid_checks_magic_of_destination(tmp_path: Path):
    zip_part = tmp_path / "full-book.zip.part"
    zip_part.write_bytes(b"PK\x03\x04" + b"\0" * 2000)
    assert fetch.looks_valid(zip_part, like=tmp_path / "full-book.zip")
    assert not fetch.looks_valid(zip_part)  # judged as a PDF by its own suffix
    html = tmp_path / "ch01.pdf"
    html.write_bytes(b"<html>Temporarily Offline</html>" + b"\0" * 2000)
    assert not fetch.looks_valid(html)
    small = tmp_path / "ch02.pdf"
    small.write_bytes(b"%PDF-1.4")
    assert not fetch.looks_valid(small)
    stump = tmp_path / "ch03.pdf"
    stump.write_bytes(b"%PDF-1.4" + b"\0" * 4000)  # cut off before the trailer
    assert not fetch.looks_valid(stump)
    whole = tmp_path / "ch04.pdf"
    whole.write_bytes(b"%PDF-1.4" + b"\0" * 4000 + b"\n%%EOF\n")
    assert fetch.looks_valid(whole)


def test_pdf_with_its_eof_marker_before_a_cut_update_is_kept(tmp_path: Path):
    # A linearised PDF whose appended cross-reference update was cut off: the marker of the
    # complete first revision is far from the end, and the file still opens.
    cut = tmp_path / "ch08.pdf"
    cut.write_bytes(b"%PDF-1.4\n" + b"x" * 3000 + b"%%EOF\n" + b"0000928480 00000 n\r\n" * 200)
    assert fetch.looks_valid(cut)
    stump = tmp_path / "ch09.pdf"
    stump.write_bytes(b"%PDF-1.4\n" + b"x" * 5000)
    assert not fetch.looks_valid(stump)


def test_member_names_with_three_digits_and_the_fees101_slip():
    assert fetch.readable_member_name("fess1010.pdf", "fess1", None) == "ch10.pdf"
    assert fetch.readable_member_name("fess1011.pdf", "fess1", None) == "ch11.pdf"
    assert fetch.readable_member_name("fees101.pdf", "fess1", None) == "ch01.pdf"
    assert fetch.readable_member_name("fees101.pdf", "gess1", None) == "fees101.pdf"
    assert fetch.readable_member_name("jess4 ps.pdf", "jess4", None) == "prelims.pdf"
    assert fetch.readable_member_name("iess1ps.pdf", "iess3", None) == "prelims.pdf"
    assert fetch.readable_member_name("iess1ps.pdf", "iess1", None) == "prelims.pdf"
