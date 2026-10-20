"""Serve the built site locally with an annotation layer for review.

Usage: uv run python scripts/annotate_server.py [port]   (default 8765, serves site/)

Every HTML page gets scripts/annotate.js injected. Select any text on a page, press the
"Flag" button that appears, say what is wrong, and the note is appended to
review/annotations.jsonl with the page address, the selected text, the page number and
side it came from, and the time. Nothing in site/ is changed, so the deployed site never
carries this. GET /_annotations?path=... lists the notes for a page and DELETE
/_annotations?id=... removes one.
"""

from __future__ import annotations

import json
import sys
import time
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
NOTES = ROOT / "review" / "annotations.jsonl"
SCRIPT = Path(__file__).with_name("annotate.js")
INJECT = b'<script src="/_annotate.js"></script>\n</body>'


def load_notes() -> list[dict]:
    if not NOTES.exists():
        return []
    return [json.loads(line) for line in NOTES.read_text().splitlines() if line.strip()]


def save_notes(notes: list[dict]) -> None:
    NOTES.parent.mkdir(parents=True, exist_ok=True)
    NOTES.write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in notes))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, fmt, *args):  # quieter: only non-200s and annotation calls
        if "_annot" in str(args[0]) or not str(args[1]).startswith(("2", "3")):
            super().log_message(fmt, *args)

    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/_annotate.js":
            body = SCRIPT.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if url.path == "/_annotations":
            path = parse_qs(url.query).get("path", [""])[0]
            notes = [n for n in load_notes() if not path or n.get("path") == path]
            self._json(200, {"notes": notes, "total": len(load_notes())})
            return
        # An HTML page: serve it with the annotation script injected before </body>.
        target = self.translate_path(url.path)
        p = Path(target)
        if p.is_dir():
            p = p / "index.html"
        if p.suffix == ".html" and p.is_file():
            body = p.read_bytes()
            if b"</body>" in body:
                body = body.replace(b"</body>", INJECT, 1)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/_annotations":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        note = json.loads(self.rfile.read(length) or b"{}")
        note = {
            "id": uuid.uuid4().hex[:10],
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "path": str(note.get("path", ""))[:500],
            "page": str(note.get("page", ""))[:80],
            "side": str(note.get("side", ""))[:40],
            "text": str(note.get("text", ""))[:2000],
            "context": str(note.get("context", ""))[:600],
            "kind": str(note.get("kind", ""))[:40],
            "note": str(note.get("note", ""))[:2000],
        }
        notes = load_notes()
        notes.append(note)
        save_notes(notes)
        print(f"flagged: {note['path']} p{note['page']} {note['side']} :: {note['text'][:60]!r} -> {note['kind']} {note['note'][:60]!r}", flush=True)
        self._json(200, {"ok": True, "note": note, "total": len(notes)})

    def do_DELETE(self):
        url = urlparse(self.path)
        if url.path != "/_annotations":
            self.send_error(404)
            return
        note_id = parse_qs(url.query).get("id", [""])[0]
        notes = [n for n in load_notes() if n.get("id") != note_id]
        save_notes(notes)
        self._json(200, {"ok": True, "total": len(notes)})


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    if not SITE.exists():
        print("site/ does not exist, run `uv run ncert-diff build` first")
        return 1
    print(f"serving {SITE} with annotations at http://127.0.0.1:{port}/  (notes go to {NOTES.relative_to(ROOT)})")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
