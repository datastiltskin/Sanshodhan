"""Command line entry point: ncert-diff fetch | status."""

from __future__ import annotations

from pathlib import Path

import typer

from . import PDF_DIR
from .sources import load_books

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _select(book_id: str | None):
    books = load_books()
    if book_id is None:
        return list(books.values())
    if book_id not in books:
        raise typer.BadParameter(f"unknown book {book_id!r}. Known: {', '.join(books)}")
    return [books[book_id]]


@app.command()
def fetch(book: str = typer.Argument(None, help="Book id from sources.yaml. Default: all.")):
    """Download every snapshot in sources.yaml that is not already on disk."""
    from .fetch import fetch_book

    for b in _select(book):
        manifest = fetch_book(b, log=typer.echo)
        typer.echo(f"wrote {manifest.relative_to(PDF_DIR.parent)}")


@app.command()
def extract(book: str = typer.Argument(None, help="Book id from sources.yaml. Default: all.")):
    """Extract text from every downloaded snapshot, group into editions, write texts/ and manifest/."""
    from .editions import process_book

    for b in _select(book):
        path = process_book(b, log=typer.echo)
        typer.echo(f"wrote {path.relative_to(PDF_DIR.parent)}")


@app.command()
def editions(book: str = typer.Argument(None)):
    """Summarise manifest/<book>/editions.json: which snapshots collapsed into which edition."""
    import json

    from . import MANIFEST_DIR

    for b in _select(book):
        path = MANIFEST_DIR / b.id / "editions.json"
        if not path.exists():
            typer.echo(f"{b.id}: not extracted yet")
            continue
        data = json.loads(path.read_text())
        typer.echo(f"{b.id}: {b.title}")
        for ed in data["editions"]:
            pre = next(iter(ed["prelims"].values()), {}) if ed["prelims"] else {}
            label = pre.get("rationalised") and f"rationalised {pre['rationalised']}" or pre.get("latest_print") or ""
            typer.echo(f"  {ed['id']:<26} {ed['chapter_count']:>2} chapters  snapshots: {', '.join(ed['snapshots'])}  {label}")
            for ch in ed["chapters"]:
                part = f"p{ch['part']} " if ch["part"] else ""
                typer.echo(f"      {part}{ch['number']:>2} {ch['printed_pages'] or '':<9} {ch['title']}")


@app.command()
def status(book: str = typer.Argument(None)):
    """Show what is on disk for each snapshot."""
    import pymupdf

    for b in _select(book):
        typer.echo(f"{b.id}: {b.title} (class {b.klass})")
        root: Path = PDF_DIR / b.id
        if not root.exists():
            typer.echo("  nothing downloaded")
            continue
        for snap_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            pdfs = sorted(snap_dir.glob("*.pdf"))
            chapters = [p for p in pdfs if "ch" in p.stem]
            pages = 0
            for p in pdfs:
                try:
                    with pymupdf.open(p) as doc:
                        pages += doc.page_count
                except Exception:  # noqa: BLE001 - a corrupt file is a status, not a crash
                    pass
            typer.echo(f"  {snap_dir.name:<18} {len(chapters):>2} chapters, {len(pdfs):>2} pdfs, {pages:>4} pages")


if __name__ == "__main__":
    app()
