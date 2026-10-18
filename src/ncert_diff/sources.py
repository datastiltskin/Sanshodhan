"""Load sources.yaml into plain dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import SOURCES_FILE


@dataclass(frozen=True)
class Snapshot:
    label: str
    url: str
    wayback: str | None = None
    part: int | None = None

    @property
    def download_url(self) -> str:
        """The URL to actually fetch. Wayback snapshots use the raw-file (id_) form."""
        if self.wayback:
            return f"http://web.archive.org/web/{self.wayback}id_/{self.url}"
        return self.url

    @property
    def is_live(self) -> bool:
        return self.wayback is None


@dataclass
class Book:
    id: str
    title: str
    klass: int
    subject: str
    language: str
    codes: dict[int | None, str]  # part number (or None) -> NCERT code
    first_chapter: dict[int, int] = field(default_factory=dict)  # part -> number of its first chapter
    snapshots: list[Snapshot] = field(default_factory=list)

    def code_for(self, part: int | None) -> str:
        return self.codes[part]


def load_books(path: Path = SOURCES_FILE) -> dict[str, Book]:
    with path.open() as fh:
        raw = yaml.safe_load(fh)
    books: dict[str, Book] = {}
    for book_id, entry in raw["books"].items():
        codes: dict[int | None, str] = {}
        if "code" in entry:
            codes[None] = entry["code"]
        first_chapter: dict[int, int] = {}
        for part in entry.get("parts", []):
            codes[part["part"]] = part["code"]
            if "first_chapter" in part:
                first_chapter[part["part"]] = int(part["first_chapter"])
        snapshots = [
            Snapshot(
                label=str(s["label"]),
                url=s["url"],
                wayback=str(s["wayback"]) if s.get("wayback") else None,
                part=s.get("part"),
            )
            for s in entry["snapshots"]
        ]
        books[book_id] = Book(
            id=book_id,
            title=entry["title"],
            klass=int(entry["class"]),
            subject=entry["subject"],
            language=entry["language"],
            codes=codes,
            first_chapter=first_chapter,
            snapshots=snapshots,
        )
    return books
