"""Read the extracted Markdown back into units the diff engine can compare."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# "<!-- page 37 (pdf 14 of ch03.pdf) -->" names the file when the page was carried over from another chapter PDF.
PAGE_MARKER = re.compile(r"^<!-- (?:page (\d+) \(pdf (\d+)(?: of ([^)]+))?\)|pdf page (\d+)(?: of (\S+))?) -->$")
ASIDE = re.compile(r"^> \[(\w+)\] (.*)$")
HEADING = re.compile(r"^(#{1,3}) (.*)$")
# Sentence ends: terminal punctuation, then space, then an opener. Common abbreviations are kept whole.
_ABBREV = r"(?<!\bFig\.)(?<!\bNo\.)(?<!\bSt\.)(?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bvs\.)(?<!\bi\.e\.)(?<!\be\.g\.)(?<!\bc\.)(?<!\bch\.)(?<!\bpp\.)(?<!\bp\.)"
_SENT_SPLIT = re.compile(r"(?<=[.!?])" + _ABBREV + r"[”’\")]?\s+(?=[A-Z“‘\"(\[0-9])")


@dataclass
class Unit:
    """One comparable piece of text: a sentence of body text, a heading, or an aside block."""
    stream: str  # body | heading | note | caption | table | source
    text: str
    page: int | None
    pdf_page: int | None
    para: int  # paragraph index within the chapter, so sentences can be regrouped
    key: str = field(default="")

    def __post_init__(self) -> None:
        if not self.key:
            self.key = normalise_key(self.text)


_DASHES = str.maketrans({"–": "-", "—": "-", "‒": "-", "‐": "-", "‑": "-", "­": ""})
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "′": "'", "´": "'"})


def normalise_key(text: str) -> str:
    """Case, dash, quote, and spacing variants collapse to one key. Used for matching only."""
    t = unicodedata.normalize("NFKC", text).translate(_DASHES).translate(_QUOTES).lower()
    t = re.sub(r"\s*-\s*", "-", t)  # "1870s -- 1947", "1870s-1947" and "1870s – 1947" agree
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"[.,;:!?]+$", "", t)  # trailing punctuation only
    return t


def split_sentences(paragraph: str) -> list[str]:
    parts = [p.strip() for p in _SENT_SPLIT.split(paragraph)]
    return [p for p in parts if p]


def parse_chapter(markdown: str) -> tuple[dict, list[Unit]]:
    """Front matter dict and the chapter's units in reading order."""
    meta: dict = {}
    body = markdown
    if markdown.startswith("---\n"):
        _, fm, body = markdown.split("---\n", 2)
        for line in fm.splitlines():
            m = re.match(r"^(\w+): (.*)$", line)
            if m:
                v = m.group(2).strip()
                meta[m.group(1)] = v[1:-1] if v.startswith('"') and v.endswith('"') else v
    units: list[Unit] = []
    page = pdf_page = None
    para = 0
    for line in body.splitlines():
        if not line.strip():
            continue
        m = PAGE_MARKER.match(line)
        if m:
            page = int(m.group(1)) if m.group(1) else None
            pdf_page = int(m.group(2) or m.group(4))
            continue
        m = HEADING.match(line)
        if m:
            para += 1
            units.append(Unit("heading", m.group(2), page, pdf_page, para))
            continue
        m = ASIDE.match(line)
        if m:
            para += 1
            role, text = m.group(1), m.group(2)
            if role == "table":
                units.append(Unit(role, text, page, pdf_page, para))
            else:
                for sent in split_sentences(text):
                    units.append(Unit(role, sent, page, pdf_page, para))
            continue
        para += 1
        for sent in split_sentences(line):
            units.append(Unit("body", sent, page, pdf_page, para))
    return meta, units
