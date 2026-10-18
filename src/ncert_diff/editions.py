"""Group downloaded snapshots into editions and write the extracted texts.

A snapshot is one folder under pdfs/<book>/ (one archive capture or one live download).
An edition is the set of snapshots whose cleaned body text is identical. Two captures of
the same reprint, or a re-encoded PDF with the same words, collapse into one edition.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from . import MANIFEST_DIR, PDF_DIR, TEXTS_DIR
from .clean import normalise_text, slugify
from .extract import body_text, extract_chapter, extract_whole_book, has_text_layer
from .fetch import load_manifest
from .sources import Book

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
CHAPTER_FILE = re.compile(r"^(?:part(\d)-)?ch(\d\d)\.pdf$")


@dataclass
class Prelims:
    title: str | None = None
    first_edition: str | None = None
    reprints: list[str] = field(default_factory=list)
    revised: str | None = None
    rationalised: str | None = None
    reprint_label: str | None = None  # "Reprint 2024-25"
    pages: int = 0

    @property
    def latest(self) -> str | None:
        """The most recent print date mentioned, as 'Month Year'."""
        candidates = [d for d in (self.first_edition, self.revised, *self.reprints) if d]
        if not candidates:
            return None
        return max(candidates, key=_date_key)


def _date_key(month_year: str) -> tuple[int, int]:
    m = re.match(rf"({MONTHS})\s+(\d{{4}})", month_year)
    if not m:
        return (0, 0)
    return int(m.group(2)), MONTHS.split("|").index(m.group(1))


def contents_titles(pdf_path: Path) -> dict[int, str]:
    """Chapter number -> title from a prelims contents page ('7. Weavers, Iron ... 79')."""
    out: dict[int, str] = {}
    with pymupdf.open(pdf_path) as doc:
        text = "\n".join(page.get_text() for page in doc)
    lines = [normalise_text(ln) for ln in text.splitlines()]
    for i, ln in enumerate(lines):
        m = re.match(r"^(\d{1,2})\.\s+(.+?)(?:\s+\d{1,3})?$", ln)
        if m and 1 <= int(m.group(1)) <= 20 and len(m.group(2)) > 3 and not m.group(2)[0].islower():
            out.setdefault(int(m.group(1)), m.group(2))
    return out


def parse_prelims(pdf_path: Path) -> Prelims:
    out = Prelims()
    with pymupdf.open(pdf_path) as doc:
        out.pages = doc.page_count
        text = "\n".join(page.get_text() for page in doc.pages(0, min(6, doc.page_count)))
    flat = normalise_text(text.replace("\n", " "))
    m = re.search(rf"First Edition\s+(?:\w+\s+)?({MONTHS})\s+(\d{{4}})", flat)
    if m:
        out.first_edition = f"{m.group(1)} {m.group(2)}"
    m = re.search(rf"Revised Edition\s+({MONTHS})\s+(\d{{4}})", flat)
    if m:
        out.revised = f"{m.group(1)} {m.group(2)}"
    m = re.search(r"Reprinted\s+(.{0,600}?)(?:ALL RIGHTS|PD \d|©|No part of)", flat)
    if m:
        out.reprints = [f"{a} {b}" for a, b in re.findall(rf"({MONTHS})\s+(\d{{4}})", m.group(1))]
    m = re.search(r"Rationalised\s+(\d{4}-\d{2})", flat)
    if m:
        out.rationalised = m.group(1)
    m = re.search(r"Reprint\s+(\d{4}-\d{2})", flat)
    if m:
        out.reprint_label = f"Reprint {m.group(1)}"
    m = re.search(r"\d{3,4}\s*[–-]\s*([A-Z][^\n]{3,60}?)\s+ISBN", flat)
    if m:
        out.title = m.group(1).strip()
    return out


def snapshot_dirs(book: Book) -> list[Path]:
    root = PDF_DIR / book.id
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir())


def chapter_files(snapshot: Path) -> list[tuple[int | None, int, Path]]:
    out = []
    for p in snapshot.glob("*.pdf"):
        m = CHAPTER_FILE.match(p.name)
        if m:
            out.append((int(m.group(1)) if m.group(1) else None, int(m.group(2)), p))
    return sorted(out, key=lambda t: (t[0] or 0, t[1]))


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _front_matter(fields: dict) -> str:
    lines = ["---"]
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines.extend(f"  - {json.dumps(x, ensure_ascii=False)}" for x in v)
        else:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def edition_id(label: str, prelims: Prelims | None) -> str:
    if prelims and prelims.rationalised:
        return f"{label}-rationalised"
    return label


def process_book(book: Book, *, log=print) -> Path:
    """Extract every snapshot, group into editions, write texts/ and editions.json."""
    manifest = load_manifest(book.id)
    extracted: dict[str, dict] = {}  # snapshot label -> details
    skipped: list[dict] = []

    for snap in snapshot_dirs(book):
        label = snap.name
        log(f"{book.id} / {label}")
        chapters = []
        units: list[tuple[int | None, int | None, Path, tuple[str, dict]]] = []
        files = chapter_files(snap)
        image_only = [pdf for _, _, pdf in files if not has_text_layer(pdf)]
        if image_only:
            log(f"  {len(image_only)} of {len(files)} chapter PDFs have no text layer (needs OCR), skipped")
            skipped.append({"snapshot": label, "reason": "no text layer, needs OCR", "files": [str(p.relative_to(PDF_DIR.parent)) for p in image_only]})
            continue
        toc: dict[int, str] = {}
        for pre in sorted(snap.glob("*prelims.pdf")):
            toc.update(contents_titles(pre))
        for part, file_number, pdf in files:
            units.append((part, file_number, pdf, extract_chapter(pdf)))
        if not units:
            for whole in sorted(snap.glob("*whole-book.pdf")):
                m = re.match(r"^(?:part(\d)-)?whole-book\.pdf$", whole.name)
                part = int(m.group(1)) if m and m.group(1) else None
                if not has_text_layer(whole):
                    log(f"  {whole.name} is unreadable or has no text layer, skipped")
                    skipped.append({"snapshot": label, "reason": "whole-book PDF unreadable or without text layer", "files": [str(whole.relative_to(PDF_DIR.parent))]})
                    continue
                log(f"  splitting {whole.name} into chapters")
                units.extend((part, None, whole, result) for result in extract_whole_book(whole))
        for part, file_number, pdf, (md, meta) in units:
            # The number printed on the opening page wins. The 2014 to 2019 Class 8 zips hold
            # Part 2 only, so their files ch01..ch06 are really chapters 7 to 12.
            if meta["chapter_number"]:
                number = int(meta["chapter_number"])
            elif file_number is not None and part in book.first_chapter:
                number = file_number + book.first_chapter[part] - 1  # files restart at 01 in each part
            else:
                number = file_number
            if number is None:
                log(f"  {pdf.name}: no chapter number found, skipped")
                continue
            if not meta["title"] or not any(ch.isalpha() for ch in meta["title"]):
                meta["title"] = toc.get(number)  # headings in fonts without a Unicode map come out blank
            chapters.append(
                {
                    "part": part,
                    "number": number,
                    "title": meta["title"],
                    "pdf": str(pdf.relative_to(PDF_DIR.parent)),
                    "pdf_pages": meta["pdf_pages"],
                    "printed_pages": meta["printed_pages"],
                    "fingerprint": _sha(body_text(md)),
                    "markdown": md,
                    "role_counts": meta["role_counts"],
                }
            )
        prelims_meta: dict[int | None, Prelims] = {}
        for pre in sorted(snap.glob("*prelims.pdf")):
            m = re.match(r"^(?:part(\d)-)?prelims\.pdf$", pre.name)
            part = int(m.group(1)) if m and m.group(1) else None
            prelims_meta[part] = parse_prelims(pre)
        if not chapters:
            log("  no chapter PDFs, skipped")
            continue
        chapters.sort(key=lambda c: (c["part"] or 0, c["number"]))
        fingerprint = _sha("\n".join(c["fingerprint"] for c in chapters))
        extracted[label] = {"chapters": chapters, "prelims": prelims_meta, "fingerprint": fingerprint}
        log(f"  {len(chapters)} chapters, fingerprint {fingerprint[:12]}")

    # Titles lost to unmapped fonts: borrow from the nearest snapshot that has one.
    labels = sorted(extracted)
    for i, label in enumerate(labels):
        for ch in extracted[label]["chapters"]:
            if ch["title"]:
                continue
            for other in sorted(labels, key=lambda o: abs(labels.index(o) - i)):
                if other == label:
                    continue
                match = next((c for c in extracted[other]["chapters"] if c["number"] == ch["number"] and c["part"] == ch["part"] and c["title"]), None)
                if match:
                    ch["title"] = match["title"]
                    ch["title_borrowed_from"] = other
                    break

    # Group by fingerprint. The earliest snapshot names the edition.
    groups: dict[str, list[str]] = {}
    for label, info in extracted.items():
        groups.setdefault(info["fingerprint"], []).append(label)

    editions = []
    for fingerprint, labels in sorted(groups.items(), key=lambda kv: kv[1][0]):
        first = labels[0]
        info = extracted[first]
        prelims = info["prelims"].get(None) or next(iter(info["prelims"].values()), None)
        eid = edition_id(first, prelims)
        out_dir = TEXTS_DIR / book.id / eid
        if out_dir.exists():
            for old in out_dir.glob("*.md"):
                old.unlink()
        out_dir.mkdir(parents=True, exist_ok=True)
        chapter_records = []
        # Part prefixes only when parts restart their numbering (Exploring Society does,
        # the two-part Our Pasts III numbers 1 to 12 straight through).
        numbers = [c["number"] for c in info["chapters"]]
        use_part_prefix = len(set(numbers)) < len(numbers)
        for ch in info["chapters"]:
            prefix = f"part{ch['part']}-" if (ch["part"] and use_part_prefix) else ""
            fname = f"{prefix}{ch['number']:02d}-{slugify(ch['title'] or 'chapter')}.md"
            pdf_record = manifest.get(ch["pdf"], {})
            fm = _front_matter(
                {
                    "book": book.id,
                    "book_title": book.title,
                    "edition": eid,
                    "snapshots": labels,
                    "part": ch["part"],
                    "chapter": ch["number"],
                    "title": ch["title"],
                    "source_pdf": ch["pdf"],
                    "source_sha256": pdf_record.get("sha256"),
                    "pdf_pages": ch["pdf_pages"],
                    "printed_pages": ch["printed_pages"],
                    "body_fingerprint": ch["fingerprint"],
                }
            )
            (out_dir / fname).write_text(fm + ch["markdown"], encoding="utf-8")
            chapter_records.append(
                {k: ch[k] for k in ("part", "number", "title", "pdf", "pdf_pages", "printed_pages", "fingerprint", "role_counts")}
                | ({"title_borrowed_from": ch["title_borrowed_from"]} if ch.get("title_borrowed_from") else {})
                | {"file": str((out_dir / fname).relative_to(TEXTS_DIR.parent))}
            )
        for part, pre in info["prelims"].items():
            pre_pdf = next(iter(sorted((PDF_DIR / book.id / first).glob(f"{'part%d-' % part if part else ''}prelims.pdf"))), None)
            if pre_pdf:
                md, _ = extract_chapter(pre_pdf)
                pname = f"{'part%d-' % part if part else ''}prelims.md"
                (out_dir / pname).write_text(
                    _front_matter({"book": book.id, "edition": eid, "part": part, "source_pdf": str(pre_pdf.relative_to(PDF_DIR.parent))}) + md,
                    encoding="utf-8",
                )
        editions.append(
            {
                "id": eid,
                "fingerprint": fingerprint,
                "snapshots": labels,
                "prelims": {
                    (f"part{k}" if k else "single"): {
                        "title": v.title,
                        "first_edition": v.first_edition,
                        "revised": v.revised,
                        "reprints": v.reprints,
                        "latest_print": v.latest,
                        "rationalised": v.rationalised,
                        "reprint_label": v.reprint_label,
                        "pages": v.pages,
                    }
                    for k, v in info["prelims"].items()
                },
                "chapter_count": len(chapter_records),
                "chapters": chapter_records,
            }
        )

    path = MANIFEST_DIR / book.id / "editions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        json.dump({"book": book.id, "title": book.title, "editions": editions, "skipped_snapshots": skipped}, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path
