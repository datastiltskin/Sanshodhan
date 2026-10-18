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
