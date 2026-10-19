"""Pull every complete member out of a truncated zip (one the Wayback Machine cut short).

Walks the local file headers from the start of the file, inflates each member that is
wholly present and whose CRC matches, and writes it next to the zip. Members with a data
descriptor (sizes stored after the data) are skipped, as is the member the truncation lands in.

Usage: uv run python scripts/salvage_truncated_zip.py pdfs/<book>/<snapshot>/full-book.zip
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


def salvage(zip_path: Path) -> list[tuple[str, int]]:
    data = zip_path.read_bytes()
    pos = 0
    saved: list[tuple[str, int]] = []
    while True:
        i = data.find(b"PK\x03\x04", pos)
        if i < 0:
            break
        _, flags, method, _, _, crc, csize, _, nlen, xlen = struct.unpack("<HHHHHIIIHH", data[i + 4 : i + 30])
        name = data[i + 30 : i + 30 + nlen].decode("utf-8", "replace")
        start = i + 30 + nlen + xlen
        if flags & 8:
            print(f"skip {name}: size is in a data descriptor")
            pos = start
            continue
        end = start + csize
        if end > len(data):
            print(f"truncated inside {name}: {len(data) - start} of {csize} bytes present")
            break
        raw = data[start:end]
        try:
            content = zlib.decompress(raw, -15) if method == 8 else raw
        except zlib.error as exc:
            print(f"skip {name}: {exc}")
            pos = end
            continue
        if zlib.crc32(content) & 0xFFFFFFFF != crc:
            print(f"skip {name}: CRC mismatch")
        else:
            out = zip_path.parent / Path(name).name
            out.write_bytes(content)
            saved.append((name, len(content)))
        pos = end
    return saved


if __name__ == "__main__":
    for name, size in salvage(Path(sys.argv[1])):
        print(f"salvaged {name} ({size // 1024} KB)")
