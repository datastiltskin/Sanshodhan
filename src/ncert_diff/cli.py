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
def diff(
    book: str = typer.Argument(None, help="Book id. Default: all."),
    from_edition: str = typer.Option(None, "--from", help="Edition id to compare from."),
    to_edition: str = typer.Option(None, "--to", help="Edition id to compare to."),
):
    """Compare editions and write diffs/<book>/<from>__<to>.json plus an HTML view."""
    from .diff import diff_editions, edition_pairs, write_diff
    from .report import write_index, write_report

    for b in _select(book):
        pairs = [(from_edition, to_edition)] if from_edition and to_edition else edition_pairs(b.id)
        written: set[Path] = set()
        for a, c in pairs:
            result = diff_editions(b.id, a, c)
            written.add(write_diff(result))
            written.add(write_report(result))
            s = result["summary"]
            typer.echo(
                f"{b.id}: {a} -> {c}: chapters -{s['chapters_dropped']} +{s['chapters_added']}; body sentences "
                f"deleted {s['body']['deleted']}, inserted {s['body']['inserted']}, modified {s['body']['modified']}, "
                f"punctuation-only {s['body']['punctuation']}, moved {s['body']['moved']}, restreamed {s['body']['restreamed']}, resplit {s['body']['resplit']}, typographic {s['body']['typographic']}; "
                f"pages to look at {s['suspect_pages']}"
            )
        if not (from_edition and to_edition):
            # Pairs from an earlier run that no longer exist (an edition that merged into
            # another) would otherwise linger and reach the site.
            from .diff import DIFF_DIR

            for stale in (DIFF_DIR / b.id).glob("*__*.*") if (DIFF_DIR / b.id).exists() else []:
                if stale not in written:
                    stale.unlink()
                    typer.echo(f"removed stale {stale.relative_to(PDF_DIR.parent)}")
    typer.echo(f"index at {write_index().relative_to(PDF_DIR.parent)}")


@app.command()
def render_pages(
    book: str = typer.Argument(None, help="Book id. Default: all."),
    out: Path = typer.Option(Path("site/images"), help="Where to write <book>/<edition>/<chapter>/pNNN.webp."),
    force: bool = typer.Option(False, help="Re-render pages that already exist."),
):
    """Render a JPEG of every printed page, for the site and for upload to object storage."""
    from .site.render_pages import render_book, render_covers

    total = 0
    for b in _select(book):
        total += render_book(b.id, out, log=typer.echo, force=force)
        render_covers(b.id, out, log=typer.echo, force=force)
    typer.echo(f"rendered {total} pages into {out}")


@app.command()
def build(
    out: Path = typer.Option(Path("site"), help="Output directory for the HTML."),
    images_base: str = typer.Option("/images", help="URL prefix where page images are served (local folder or object storage)."),
    base_url: str = typer.Option("", help="Path the site is served under: empty at a domain root, /Sanshodhan on a GitHub Pages project site."),
    no_search: bool = typer.Option(False, "--no-search", help="Skip the Pagefind search index (faster local builds)."),
):
    """Build the static site into site/, including the search index."""
    from .site.build import build as build_site

    build_site(out, images_base.rstrip("/"), base_url=base_url.strip().rstrip("/"), search=not no_search, log=typer.echo)
    typer.echo(f"site written to {out}")


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
