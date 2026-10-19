"""A plain HTML view of a diff result, for reading and checking. Not the site."""

from __future__ import annotations

import html
import json
from pathlib import Path

from .diff import DIFF_DIR

CSS = """
body { font: 15px/1.5 Georgia, serif; max-width: 62em; margin: 2em auto; padding: 0 1em; color: #222; }
h1, h2, h3 { font-family: system-ui, sans-serif; }
h2 { margin-top: 2.5em; border-top: 1px solid #ddd; padding-top: 1em; }
.summary { font-family: system-ui, sans-serif; font-size: 14px; background: #f6f6f6; padding: .8em 1em; }
.hunk { margin: 1em 0; padding: .6em .9em; border-left: 4px solid #999; background: #fafafa; }
.hunk.deleted { border-color: #c33; } .hunk.inserted { border-color: #393; } .hunk.modified { border-color: #c80; }
.hunk.moved, .hunk.typographic, .hunk.restreamed, .hunk.resplit, .hunk.unreadable, .hunk.punctuation { border-color: #bbb; color: #666; }
.tag { font: 12px system-ui, sans-serif; text-transform: uppercase; color: #666; margin-right: .6em; }
.stream { font: 12px system-ui, sans-serif; color: #888; }
.pg { font: 12px system-ui, sans-serif; color: #888; float: right; }
del { background: #fdd; text-decoration: line-through; } ins { background: #dfd; text-decoration: none; }
.dropped { color: #c33; } .added { color: #393; }
details summary { cursor: pointer; font-family: system-ui, sans-serif; color: #666; }
"""


def _hunk_html(h: dict) -> str:
    pg = ""
    if h.get("old_page") or h.get("new_page"):
        pg = f"<span class=pg>p. {h.get('old_page') or '–'} → p. {h.get('new_page') or '–'}</span>"
    head = f"<span class=tag>{h['type']}</span><span class=stream>{h['stream']}</span>{pg}"
    if h["type"] == "modified":
        parts = []
        for op, tok in h["words"]:
            t = html.escape(tok)
            parts.append(t if op == "=" else (f"<del>{t}</del>" if op == "-" else f"<ins>{t}</ins>"))
        body = " ".join(parts)
    elif h["type"] == "deleted":
        body = f"<del>{html.escape(h['old'])}</del>"
    elif h["type"] == "inserted":
        body = f"<ins>{html.escape(h['new'])}</ins>"
    else:
        old, new = html.escape(h["old"] or ""), html.escape(h["new"] or "")
        body = f"{old}<br><span class=stream>→</span> {new}" if old and new else (old or new)
    return f"<div class='hunk {h['type']}'>{head}<div>{body}</div></div>"


def render(result: dict) -> str:
    s = result["summary"]
    out = [f"<!doctype html><meta charset=utf-8><title>{result['book']}: {result['from']} → {result['to']}</title><style>{CSS}</style>"]
    out.append(f"<h1>{result['book']}<br><small>{result['from']} → {result['to']}</small></h1>")
    if result.get("ocr"):
        out.append("<p class=summary><b>One side of this comparison is OCR text.</b> Small word-level differences are likely reading errors, not edits.</p>")
    out.append(
        f"<p class=summary>Chapters dropped: {s['chapters_dropped']}, added: {s['chapters_added']}. "
        f"Body sentences deleted {s['body']['deleted']}, inserted {s['body']['inserted']}, modified {s['body']['modified']}, "
        f"moved {s['body']['moved']}, typographic only {s['body']['typographic']}. "
        f"Other streams (notes, captions, tables, sources, headings): deleted {s['other_streams']['deleted']}, inserted {s['other_streams']['inserted']}, modified {s['other_streams']['modified']}.</p>"
    )
    for ch in result["chapters"]:
        a, b = ch["from"], ch["to"]
        if ch["status"] == "dropped":
            out.append(f"<h2 class=dropped>Dropped: {a['number']} {html.escape(a['title'] or '')}</h2>")
            continue
        if ch["status"] == "added":
            out.append(f"<h2 class=added>Added: {b['number']} {html.escape(b['title'] or '')}</h2>")
            continue
        title = f"{a['number']} {html.escape(a['title'] or '')}"
        if (a["title"] or "").lower() != (b["title"] or "").lower() or a["number"] != b["number"]:
            title += f" → {b['number']} {html.escape(b['title'] or '')}"
        out.append(f"<h2>{title}</h2>")
        real = [h for st in ch["streams"].values() for h in st["hunks"] if h["type"] in ("deleted", "inserted", "modified")]
        quiet = [h for st in ch["streams"].values() for h in st["hunks"] if h["type"] in ("moved", "typographic", "restreamed", "resplit", "unreadable", "punctuation")]
        # "equal" hunks exist only for the viewer
        if not real and not quiet:
            out.append("<p class=stream>No differences.</p>")
        real.sort(key=lambda h: (h.get("old_page") or h.get("new_page") or 0))
        out.extend(_hunk_html(h) for h in real)
        if quiet:
            out.append(f"<details><summary>{len(quiet)} moved, re-streamed, punctuation-only, typographic-only, or unreadable differences</summary>")
            out.extend(_hunk_html(h) for h in quiet)
            out.append("</details>")
    return "\n".join(out)


def write_report(result: dict) -> Path:
    out = DIFF_DIR / result["book"] / f"{result['from']}__{result['to']}.html"
    out.write_text(render(result))
    return out


def write_index() -> Path:
    rows = []
    for jpath in sorted(DIFF_DIR.glob("*/*.json")):
        r = json.loads(jpath.read_text())
        s = r["summary"]
        rows.append(
            f"<tr><td>{r['book']}</td><td><a href='{jpath.parent.name}/{jpath.stem}.html'>{r['from']} → {r['to']}</a>{' (OCR)' if r.get('ocr') else ''}</td>"
            f"<td>{s['chapters_dropped']}</td><td>{s['chapters_added']}</td><td>{s['body']['deleted']}</td><td>{s['body']['inserted']}</td><td>{s['body']['modified']}</td>"
            f"<td>{s['other_streams']['deleted'] + s['other_streams']['inserted'] + s['other_streams']['modified']}</td></tr>"
        )
    page = (
        f"<!doctype html><meta charset=utf-8><title>NCERT textbook diffs</title><style>{CSS} table {{ border-collapse: collapse; font-family: system-ui, sans-serif; font-size: 14px }} td, th {{ padding: .3em .7em; border-bottom: 1px solid #ddd; text-align: left }}</style>"
        "<h1>Edition diffs</h1><table><tr><th>Book</th><th>Pair</th><th>Ch. dropped</th><th>Ch. added</th><th>Body deleted</th><th>Body inserted</th><th>Body modified</th><th>Other changes</th></tr>"
        + "".join(rows) + "</table>"
    )
    out = DIFF_DIR / "index.html"
    out.write_text(page)
    return out
