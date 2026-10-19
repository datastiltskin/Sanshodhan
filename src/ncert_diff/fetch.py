"""Download every file listed in sources.yaml, exactly once.

Rules this module follows:
- A snapshot is never requested again once its file is on disk and looks valid.
- Downloads go to a .part file and are renamed only after the bytes check out.
- The Wayback Machine sometimes answers a 200 with an HTML "Temporarily Offline" page.
  We check the magic bytes of what we got, not just the status code.
- Retries use a slow backoff. We would rather wait than hammer the archive.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import time
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import subprocess

from . import MANIFEST_DIR, PDF_DIR
from .sources import Book, Snapshot

USER_AGENT = "Mozilla/5.0"  # what worked against both ncert.nic.in and web.archive.org
# The Wayback Machine rate-limits bursts and answers 429 (or an HTML page with status 200).
# Waiting a few minutes clears it. These are deliberately slow.
BACKOFF_SECONDS = (60, 180, 420, 900)
POLITE_PAUSE_SECONDS = 15  # between consecutive downloads from the same host
MAX_CHAPTERS_TO_PROBE = 20

ZIP_MAGIC = b"PK\x03\x04"
PDF_MAGIC = b"%PDF"


class FetchError(RuntimeError):
    pass


class NotFound(FetchError):
    pass


@dataclass
class FileRecord:
    path: str  # relative to the repo root
    source_url: str
    download_url: str
    wayback: str | None
    fetched_at: str
    sha256: str
    size: int
    members: list[str] = field(default_factory=list)  # for zips: readable member paths


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _expect_magic(path: Path) -> bytes:
    return ZIP_MAGIC if path.suffix == ".zip" else PDF_MAGIC


def looks_valid(path: Path, like: Path | None = None) -> bool:
    """Is `path` a plausible file of the kind its name (or `like`'s name) says?"""
    if not path.is_file() or path.stat().st_size < 1024:
        return False
    with path.open("rb") as fh:
        head = fh.read(4)
    return head.startswith(_expect_magic(like or path))


_last_request_at = 0.0


def _pause_between_requests() -> None:
    global _last_request_at
    gap = time.monotonic() - _last_request_at
    if _last_request_at and gap < POLITE_PAUSE_SECONDS:
        time.sleep(POLITE_PAUSE_SECONDS - gap)
    _last_request_at = time.monotonic()


def download(url: str, dest: Path, *, log=print) -> None:
    """Fetch url to dest with retries. Raises NotFound on a definite 404.

    The transfer itself is done by curl. The Wayback Machine answered 429 to the same
    requests made with httpx while curl got the file, and curl is everywhere.
    """
    if looks_valid(dest):
        log(f"  have    {dest.relative_to(PDF_DIR.parent)}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    last_error: Exception | None = None
    for wait in (0, *BACKOFF_SECONDS):
        if wait:
            log(f"  retry in {wait}s ({last_error})")
            time.sleep(wait)
        try:
            _pause_between_requests()
            status, err = _curl(url, part)
            if status == 404:
                raise NotFound(url)
            if status == 0:
                raise FetchError(f"curl failed for {url}: {err}")
            if status >= 400:
                raise FetchError(f"HTTP {status} for {url}")
            if not looks_valid(part, like=dest):
                snippet = part.read_bytes()[:160].decode("utf-8", "replace").replace("\n", " ")
                raise FetchError(f"response was not a {dest.suffix} file: {snippet!r}")
            part.rename(dest)
            log(f"  fetched {dest.relative_to(PDF_DIR.parent)} ({dest.stat().st_size // 1024} KB)")
            return
        except NotFound:
            part.unlink(missing_ok=True)
            raise
        except (FetchError, OSError) as exc:
            last_error = exc
            part.unlink(missing_ok=True)
    raise FetchError(f"gave up on {url}: {last_error}")


CURL = "/usr/bin/curl" if Path("/usr/bin/curl").exists() else "curl"


def _curl(url: str, part: Path) -> tuple[int, str]:
    """Run curl, return (final HTTP status, stderr). Status 0 means a transport failure."""
    cmd = [
        CURL, "--silent", "--show-error", "--location", "--fail-with-body",
        "--user-agent", USER_AGENT, "--max-time", "600", "--connect-timeout", "30",
        "--output", str(part), "--write-out", "%{http_code}", url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    code = proc.stdout.strip()[-3:]
    return (int(code) if code.isdigit() else 0), proc.stderr.strip()[-300:]


def readable_member_name(member: str, code: str, part: int | None) -> str | None:
    """Map gess104.pdf -> ch04.pdf, gess1ps.pdf -> prelims.pdf. None for junk entries."""
    base = Path(member).name
    if not base or base.startswith(".") or base.startswith("__MACOSX"):
        return None
    prefix = f"part{part}-" if part else ""
    m = re.fullmatch(rf"{re.escape(code)}(\d\d)\.pdf", base, re.IGNORECASE)
    if m:
        return f"{prefix}ch{m.group(1)}.pdf"
    if re.fullmatch(rf"{re.escape(code)}ps\.pdf", base, re.IGNORECASE):
        return f"{prefix}prelims.pdf"
    if re.fullmatch(rf"{re.escape(code)}dd\.pdf", base, re.IGNORECASE):
        return f"{prefix}whole-book.pdf"  # some zips hold the book as one PDF instead of chapters
    if base.lower().endswith(".pdf"):
        return f"{prefix}{base.lower()}"
    return None


def unzip_book(zip_path: Path, code: str, part: int | None, *, log=print) -> list[str]:
    """Extract a whole-book zip next to itself with readable names. Returns member paths."""
    out: list[str] = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = readable_member_name(info.filename, code, part)
            if name is None:
                continue
            target = zip_path.parent / name
            if not looks_valid(target):
                with zf.open(info) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
            out.append(str(target.relative_to(PDF_DIR.parent)))
    log(f"  unzipped {len(out)} files from {zip_path.name}")
    return sorted(out)


def snapshot_dir(book: Book, snap: Snapshot) -> Path:
    label = snap.label
    if label == "live":
        label = f"live-{date.today().isoformat()}"
    return PDF_DIR / book.id / label


def fetch_snapshot(book: Book, snap: Snapshot, *, log=print) -> list[FileRecord]:
    code = book.code_for(snap.part)
    prefix = f"part{snap.part}-" if snap.part else ""
    directory = snapshot_dir(book, snap)
    log(f"{book.id} / {snap.label}" + (f" part {snap.part}" if snap.part else ""))
    records: list[FileRecord] = []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def record(path: Path, url: str, members: list[str] | None = None, download_url: str | None = None) -> None:
        records.append(
            FileRecord(
                path=str(path.relative_to(PDF_DIR.parent)),
                source_url=url,
                download_url=download_url or (snap.download_url if url == snap.url else url),
                wayback=snap.wayback,
                fetched_at=now,
                sha256=sha256_of(path),
                size=path.stat().st_size,
                members=members or [],
            )
        )

    if snap.url.endswith("dd.zip"):
        zip_path = directory / f"{prefix}full-book.zip"
        try:
            download(snap.download_url, zip_path, log=log)
        except NotFound:
            log("  zip is a 404, falling back to per-chapter files")
            return _fetch_chapters(book, snap, directory, code, prefix, record, log)
        try:
            members = unzip_book(zip_path, code, snap.part, log=log)
        except zipfile.BadZipFile as exc:
            # Archived as published: some NCERT zips are truncated or not zips at all.
            log(f"  {zip_path.name} is not a readable zip ({exc}); kept for the record, nothing extracted")
            members = []
        record(zip_path, snap.url, members)
        for member in members:
            # A member's provenance is the zip it came out of: the archived copy when there is one.
            name = Path(member).name
            record(PDF_DIR.parent / member, f"{snap.url}#{name}", download_url=f"{snap.download_url}#{name}")
        return records

    target = directory / (readable_member_name(snap.url.rsplit("/", 1)[-1], code, snap.part) or "file.pdf")
    download(snap.download_url, target, log=log)
    record(target, snap.url)
    return records


def _fetch_chapters(book, snap, directory, code, prefix, record, log) -> list[FileRecord]:
    """Live-site fallback: prelims plus chapters 01.. until the first 404."""
    base = snap.url.rsplit("/", 1)[0]
    prelims_url = f"{base}/{code}ps.pdf"
    target = directory / f"{prefix}prelims.pdf"
    try:
        download(prelims_url, target, log=log)
        record(target, prelims_url)
    except NotFound:
        log("  no prelims file")
    for n in range(1, MAX_CHAPTERS_TO_PROBE + 1):
        url = f"{base}/{code}{n:02d}.pdf"
        target = directory / f"{prefix}ch{n:02d}.pdf"
        try:
            download(url, target, log=log)
        except NotFound:
            break
        record(target, url)
    return []  # records were appended through the closure


def load_manifest(book_id: str) -> dict[str, dict]:
    path = MANIFEST_DIR / book_id / "files.json"
    if not path.exists():
        return {}
    with path.open() as fh:
        return {r["path"]: r for r in json.load(fh)["files"]}


def save_manifest(book: Book, records: dict[str, dict]) -> Path:
    path = MANIFEST_DIR / book.id / "files.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "book": book.id,
        "title": book.title,
        "class": book.klass,
        "codes": {str(k) if k else "single": v for k, v in book.codes.items()},
        "files": sorted(records.values(), key=lambda r: r["path"]),
    }
    with path.open("w") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path


def fetch_book(book: Book, *, log=print) -> Path:
    records = load_manifest(book.id)
    for snap in book.snapshots:
        for rec in fetch_snapshot(book, snap, log=log):
            records[rec.path] = asdict(rec)
    return save_manifest(book, records)
