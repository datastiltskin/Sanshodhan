"""Read the extracted Markdown back into units the diff engine can compare."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# "<!-- page 37 (pdf 14 of ch03.pdf) -->" names the file when the page was carried over from another chapter PDF.
PAGE_MARKER = re.compile(r"^<!-- (?:page (\d+) \(pdf (\d+)(?: of ([^)]+))?\)|pdf page (\d+)(?: of (\S+))?) -->$")
ASIDE = re.compile(r"^> \[(\w+)\] (.*)$")
HEADING = re.compile(r"^(#{1,3}) (.*)$")
# Sections are flat runs of a chapter that the books set apart and that change layout between
# printings: the exercises, the glossary, the references, and a unit's teacher's note. A
# section starts at the line that announces it and runs to the next section (a teacher's
# note ends at the chapter title). The extractor writes a marker line before the start line,
# and the parser also recognises the start lines themselves, so older texts parse the same.
SECTION_MARKER = re.compile(r"^<!-- section: ([\w-]+) -->$")
SECTION_STARTS = (
    (re.compile(r"^(exercises?|questions|let[’']s (recall|discuss|do|understand|imagine|find out|write|try))[\s:.!]*$", re.IGNORECASE), "exercises"),
    (re.compile(r"^(glossary|keywords?)[\s:.]*$", re.IGNORECASE), "glossary"),
    (re.compile(r"^(references|notes?|bibliography|credits)[\s:.]*$", re.IGNORECASE), "references"),
    (re.compile(r"^teacher[’']s note[\s:.]*$", re.IGNORECASE), "teachers-note"),
)
SECTIONS = tuple(name for _, name in SECTION_STARTS)


def section_start(line: str) -> str | None:
    """The section a Markdown line opens, or None. Works on headings, aside lines and plain lines."""
    text = line.strip()
    m = HEADING.match(text)
    if m:
        text = m.group(2)
    m = ASIDE.match(text)
    if m:
        text = m.group(2)
    for pattern, name in SECTION_STARTS:
        if pattern.match(text.strip()):
            return name
    return None


def annotate_sections(markdown: str) -> str:
    """Insert a "<!-- section: name -->" marker before every line that opens a section.
    Idempotent: lines that already have their marker are left alone."""
    out: list[str] = []
    current: str | None = None
    for line in markdown.splitlines():
        m = SECTION_MARKER.match(line)
        if m:
            current = m.group(1)
        name = section_start(line)
        if name and name != current:
            # "Let's recall", "Let's discuss" and "Let's do" all open the exercises: one marker.
            out.append(f"<!-- section: {name} -->")
            out.append("")
            current = name
        elif current == "teachers-note" and not name:
            m = HEADING.match(line)
            if m and len(m.group(1)) <= 2:
                current = None  # the chapter title ends the teacher's note
        out.append(line)
    return "\n".join(out) + ("\n" if markdown.endswith("\n") else "")
# Sentence ends: terminal punctuation, then space, then an opener. Common abbreviations are kept whole.
_ABBREV = r"(?<!\bFig\.)(?<!\bNo\.)(?<!\bSt\.)(?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bvs\.)(?<!\bi\.e\.)(?<!\be\.g\.)(?<!\bc\.)(?<!\bch\.)(?<!\bpp\.)(?<!\bp\.)(?<!\b\d\.)(?<!\b\d\d\.)"  # "1. Why..." is one question, not "1." and "Why..."
_SENT_SPLIT = re.compile(r"(?<=[.!?])" + _ABBREV + r"[”’\")]?\s+(?=[A-Z“‘\"(\[0-9])")


@dataclass
class Unit:
    """One comparable piece of text: a sentence of body text, a heading, or an aside block."""
    stream: str  # the comparison stream: a section name when inside one, else the role
    text: str
    page: int | None
    pdf_page: int | None
    para: int  # paragraph index within the chapter, so sentences can be regrouped
    key: str = field(default="")
    role: str = field(default="")  # body | heading | note | caption | table | source
    section: str | None = field(default=None)  # exercises | glossary | references | teachers-note

    def __post_init__(self) -> None:
        if not self.key:
            self.key = normalise_key(self.text)
        if not self.role:
            self.role = self.stream


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
    section: str | None = None

    def add(role: str, text: str) -> None:
        # Headings keep their own stream so the viewer can recover their levels in order.
        stream = section if section and role != "heading" else role
        units.append(Unit(stream, text, page, pdf_page, para, role=role, section=section))

    for line in body.splitlines():
        if not line.strip():
            continue
        m = PAGE_MARKER.match(line)
        if m:
            page = int(m.group(1)) if m.group(1) else None
            pdf_page = int(m.group(2) or m.group(4))
            continue
        m = SECTION_MARKER.match(line)
        if m:
            section = m.group(1)
            continue
        started = section_start(line)
        if started:
            section = started
        m = HEADING.match(line)
        if m:
            if len(m.group(1)) <= 2 and section == "teachers-note" and not started:
                section = None  # the chapter title ends the unit's teacher's note
            para += 1
            add("heading", m.group(2))
            continue
        m = ASIDE.match(line)
        if m:
            para += 1
            role, text = m.group(1), m.group(2)
            if role == "table" and not section:
                add(role, text)  # a real table row stays whole
            else:
                # Inside a section a "table" block is a text box (questions, glossary entries)
                # whose rows are sentences, and the other printing may set them as notes.
                for sent in split_sentences(text):
                    add(role, sent)
            continue
        para += 1
        for sent in split_sentences(line):
            add("body", sent)
    return meta, units
