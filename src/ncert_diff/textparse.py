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
# A marker with this name closes the current section. The diff engine writes it between two
# chapters it compares as one, so the first chapter's exercises do not run on into the second.
NO_SECTION = "none"
# The civics books set a question's lettered statements in a side box beside the glossary box,
# and the reading order (column first, then the side) puts them after the "Glossary" heading.
EXERCISE_ITEM = re.compile(r"^(\(?[a-h]\)|[a-h]\.|\d{1,2}\.)\s+\S")
GLOSSARY_ENTRY = re.compile(r"^[A-Z][A-Za-z’' -]{1,40}:\s+\S")


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
    seen: set[str] = set()
    for line in markdown.splitlines():
        m = SECTION_MARKER.match(line)
        if m:
            current = m.group(1)
        name = section_start(line)
        if not name and current in ("glossary", "exercises") and {"glossary", "exercises"} <= seen | {current}:
            # A lettered statement after the glossary heading belongs to the exercises beside
            # it, and a "Term: meaning" line after that belongs to the glossary again.
            text = line.strip()
            m2 = ASIDE.match(text)
            if m2:
                text = m2.group(2).strip()
            if current == "glossary" and EXERCISE_ITEM.match(text) and not GLOSSARY_ENTRY.match(text) and "exercises" in seen:
                name = "exercises"
            elif current == "exercises" and GLOSSARY_ENTRY.match(text) and "glossary" in seen:
                name = "glossary"
        if name and name != current:
            # "Let's recall", "Let's discuss" and "Let's do" all open the exercises: one marker.
            out.append(f"<!-- section: {name} -->")
            out.append("")
            current = name
            seen.add(name)
        elif current == "teachers-note" and not name:
            m = HEADING.match(line)
            if m and len(m.group(1)) <= 2:
                current = None  # the chapter title ends the teacher's note
        out.append(line)
    return "\n".join(out) + ("\n" if markdown.endswith("\n") else "")
# Sentence ends: terminal punctuation, then space, then an opener. Common abbreviations are kept whole.
# "1. Why..." is one question, not "1." and "Why...". Credits lists ("Vol. 72, Ch. 3") and
# initials ("S.I. Rao", "D.K. Basu", "W. Daniell") are not sentence ends either: a single capital
# followed by a full stop is read as an initial, which costs a rare split after "Group D." but
# stops a printing that wraps a name differently from showing as a changed sentence. A lone "I."
# is left out because it is usually a regnal number ending a sentence ("Rajendra I. During ..."),
# and "S.I." is caught as a pair of initials instead.
_ABBREV = (
    r"(?<!\bFig\.)(?<!\bFigs\.)(?<!\bNo\.)(?<!\bNos\.)(?<!\bSt\.)(?<!\bDr\.)(?<!\bMr\.)(?<!\bMrs\.)(?<!\bvs\.)(?<!\bi\.e\.)(?<!\be\.g\.)"
    r"(?<!\bc\.)(?<!\bch\.)(?<!\bCh\.)(?<!\bVol\.)(?<!\bvol\.)(?<!\bVols\.)(?<!\bRs\.)(?<!\bJr\.)(?<!\bSr\.)(?<!\bProf\.)(?<!\bpp\.)(?<!\bp\.)"
    r"(?<!\b[A-HJ-Z]\.)(?<!\b[A-Z]\.[A-Z]\.)(?<!\b\d\.)(?<!\b\d\d\.)"
)
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
            if self.stream in LISTED_STREAMS:
                self.key = strip_list_label(self.key)
        if not self.role:
            self.role = self.stream


_DASHES = str.maketrans({"–": "-", "—": "-", "‒": "-", "‐": "-", "‑": "-", "­": ""})
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "′": "'", "´": "'"})


# A fill-in blank is printed as a rule of any length, in underscores or dashes, and the length
# changes between printings. Any run of three or more becomes one blank token.
_BLANK = re.compile(r"\s*(?:_{3,}|[-–—‒‐‑]{3,})\s*")
BLANK = "___"


def normalise_key(text: str) -> str:
    """Case, dash, quote, and spacing variants collapse to one key. Used for matching only."""
    t = _BLANK.sub(f" {BLANK} ", unicodedata.normalize("NFKC", text))
    t = t.translate(_DASHES).translate(_QUOTES).lower()
    t = re.sub(r"\s*-\s*", "-", t)  # "1870s -- 1947", "1870s-1947" and "1870s – 1947" agree
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(\(?\d{1,2}[.)])(?=[a-z])", r"\1 ", t)  # "1.that" is "1. that" with the space lost
    t = re.sub(r"[.,;:!?]+$", "", t).rstrip()  # trailing punctuation only
    return t


# Exercise questions and the items under them are renumbered whenever one is cut ("12." becomes
# "11."), so the leading label does not take part in matching: "1.", "12)", "(a)", "b.", "(iv)".
LISTED_STREAMS = ("exercises", "glossary")
_LIST_LABEL = re.compile(r"^(?:\(?\d{1,2}[.)]|\(?[a-z][.)]|\([ivx]+\)|[ivx]+[.)])\s+")


def strip_list_label(key: str) -> str:
    return _LIST_LABEL.sub("", key, count=1)


def split_sentences(paragraph: str) -> list[str]:
    parts = [p.strip() for p in _SENT_SPLIT.split(paragraph)]
    return [p for p in parts if p]


# Chart labels. A pie or bar chart's labels come out as one short caption each ("Pensions",
# "5 p.", "(4%)"), so any change to the chart shows as dozens of one-word hunks. A run of
# CHART_RUN_MIN or more consecutive short captions on one page, at least one of them a figure,
# is read as one caption unit: a changed chart is then one change, and a new chart one insertion.
CHART_RUN_MIN = 4
CHART_LABEL_WORDS = 6
_CHART_FIGURE = re.compile(r"\d\s*(%|p\.)")
_SENTENCE_END = re.compile(r"[.?!:]$")


def _chart_label(text: str) -> bool:
    """A caption line short enough, and unpunctuated enough, to be one label of a chart."""
    t = text.strip()
    if len(t.split()) > CHART_LABEL_WORDS:
        return False
    return not _SENTENCE_END.search(t) or bool(re.search(r"\d\s*p\.$", t))


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

    labels: list[str] = []  # consecutive caption lines that may be one chart's labels

    def flush_labels() -> None:
        nonlocal para
        if len(labels) >= CHART_RUN_MIN and any(_CHART_FIGURE.search(t) for t in labels):
            para += 1
            add("caption", " / ".join(labels))
        else:
            for t in labels:
                para += 1
                for sent in split_sentences(t):
                    add("caption", sent)
        labels.clear()

    for line in body.splitlines():
        if not line.strip():
            continue
        m = ASIDE.match(line)
        if m and m.group(1) == "caption" and _chart_label(m.group(2)):
            labels.append(m.group(2))
            continue
        flush_labels()
        m = PAGE_MARKER.match(line)
        if m:
            page = int(m.group(1)) if m.group(1) else None
            pdf_page = int(m.group(2) or m.group(4))
            continue
        m = SECTION_MARKER.match(line)
        if m:
            section = None if m.group(1) == NO_SECTION else m.group(1)
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
        if line.startswith("- "):
            add("body", line[2:].strip())  # a list item is one unit, whatever its punctuation
            continue
        for sent in split_sentences(line):
            add("body", sent)
    flush_labels()
    return meta, units
