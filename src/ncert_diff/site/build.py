"""Build the static site from manifests, texts, and diffs.

Pages:
  /                          home: the books, what this is
  /<book>/                   timeline of editions
  /<book>/<edition>/         chapter list, sources, caveats for one edition
  /<book>/<edition>/<ch>/    the viewer: page image beside text, changes since the previous edition
  /<book>/changes/           every change between consecutive editions, linked into the viewer
  /changes/                  the written summary of what changed (docs/findings.md)
  /method/                   how the data was made and how far to trust it
"""

from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from html import escape
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import MANIFEST_DIR, REPO_ROOT
from ..diff import DIFF_DIR
from ..sources import load_books
from ..textparse import Unit, parse_chapter
from .render_pages import chapter_dir_name
from ..textparse import SECTIONS

HERE = Path(__file__).parent
QUIET = {"moved", "typographic", "restreamed", "resplit", "unreadable", "punctuation"}
REAL = {"deleted", "inserted", "modified"}


# ---------- editions ----------

@dataclass
class Edition:
    book: str
    id: str
    raw: dict
    index: int
    label: str
    detail: str
    caveats: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"/{self.book}/{self.id}/"

    @property
    def cover(self) -> str:
        """Path of the edition's cover thumbnail below the images base."""
        return f"{self.book}/covers/{self.id}.webp"


_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def human_date(label: str) -> str:
    """'2016-09-10' -> '10 September 2016'; 'live-2026-10-18' -> 'ncert.nic.in, 18 October 2026'."""
    m = re.match(r"^(live-)?(\d{4})-(\d{2})-(\d{2})", label)
    if not m:
        return label
    d = f"{int(m.group(4))} {_MONTHS[int(m.group(3)) - 1]} {m.group(2)}"
    return f"ncert.nic.in, {d}" if m.group(1) else d


def files_year(ed: dict) -> str | None:
    """Year the chapter PDFs were produced, from their metadata, for editions whose prelims carry no date."""
    import pymupdf

    years = []
    for ch in ed["chapters"][:3]:
        try:
            with pymupdf.open(REPO_ROOT / ch["pdf"]) as doc:
                created = doc.metadata.get("creationDate") or ""
        except Exception:  # noqa: BLE001
            continue
        m = re.search(r"(\d{4})", created)
        if m:
            years.append(m.group(1))
    if not years:
        return None
    # The 2016 capture of Social and Political Life II mixes 2007 files with three re-set in 2015.
    return min(years) if min(years) == max(years) else f"{min(years)} to {max(years)}"


def describe_edition(book_id: str, ed: dict, prev_label: str | None) -> tuple[str, str, list[str]]:
    pre = next(iter(ed["prelims"].values()), {}) if ed["prelims"] else {}
    captured = ", ".join(human_date(s) for s in ed["snapshots"] if not s.endswith("partial"))
    caveats: list[str] = []
    if pre.get("rationalised"):
        label = f"{pre['rationalised']} rationalised edition"
        detail = f"NCERT's 'rationalised' edition: content cut after the 2022 review. Archived {captured}."
    elif pre.get("latest_print"):
        label = f"{pre['latest_print']} printing"
        detail = f"Printing dated {pre['latest_print']} (first edition {pre.get('first_edition') or 'unknown'}). Archived {captured}."
    else:
        year = files_year(ed)
        label = f"Files dated {year}" if year else f"Archived {human_date(ed['snapshots'][0])}"
        detail = f"The files carry no printing date; their PDF metadata is from {year}. Archived {captured}." if year else f"No printing date in the files. Archived {captured}."
    if ed.get("ocr"):
        label += " (OCR)"
        caveats.append("These files are page images without a text layer. The text was read with OCR and contains reading errors.")
    if ed["id"].startswith("2024-05-24") and book_id == "our-pasts-2":
        caveats.append("Transliterated terms in these files are drawn as outlines, not text. They were recovered by OCR and may be misspelt.")
    if book_id == "our-pasts-3" and ed["id"].startswith("2019-03-12"):
        caveats.append("Headings and boxes in these files use fonts without a Unicode map and could not be read. They appear as [unreadable].")
    return label, detail, caveats


def load_editions(book_id: str) -> list[Edition]:
    data = json.loads((MANIFEST_DIR / book_id / "editions.json").read_text())
    out: list[Edition] = []
    prev = None
    for i, ed in enumerate(data["editions"]):
        label, detail, caveats = describe_edition(book_id, ed, prev)
        out.append(Edition(book_id, ed["id"], ed, i, label, detail, caveats))
        prev = label
    return out


def previous_edition(editions: list[Edition], ed: Edition) -> Edition | None:
    """The edition the diffs compare against: the nearest earlier non-OCR edition."""
    for e in reversed(editions[: ed.index]):
        if not e.raw.get("ocr"):
            return e
    return None


# ---------- text and changes ----------

@dataclass
class Sentence:
    text: str
    stream: str
    change: str | None = None  # inserted | modified | deleted | moved | ... or None
    words: list[list[str]] | None = None
    similarity: float | None = None


@dataclass
class Block:
    kind: str  # heading | body | note | caption | source | table
    level: int
    sentences: list[Sentence]
    page: int | None
    para: int


def chapter_blocks(markdown_text: str) -> tuple[dict, list[Block]]:
    meta, units = parse_chapter(markdown_text)
    blocks: list[Block] = []
    current: Block | None = None
    for u in units:
        kind = "heading" if u.role == "heading" else (u.section or u.role)
        if current is None or u.para != current.para or kind != current.kind:
            level = 0
            current = Block(kind, level, [], u.page, u.para)
            blocks.append(current)
        current.sentences.append(Sentence(u.text, u.stream))
    # Heading levels come from the markdown, which parse_chapter does not keep. Recover them.
    levels = [len(m.group(1)) for m in re.finditer(r"^(#{1,3}) ", markdown_text, re.M)]
    hi = iter(levels)
    for b in blocks:
        if b.kind == "heading":
            b.level = next(hi, 2)
    return meta, blocks


def apply_changes(blocks: list[Block], chapter_diff: dict | None) -> dict:
    """Mark sentences with their change type and place deleted sentences beside the text."""
    counts = defaultdict(int)
    if not chapter_diff or chapter_diff.get("status") != "matched":
        return counts
    # Stream -> ordered list of sentences, mirroring parse_chapter's unit order per stream.
    per_stream: dict[str, list[Sentence]] = defaultdict(list)
    for b in blocks:
        for s in b.sentences:
            per_stream[s.stream].append(s)
    anchors: dict[str, list[tuple[int, int]]] = defaultdict(list)  # stream -> (old_pos, new_pos)
    page_anchors: list[tuple[int, int]] = []  # (old printed page, body new_pos) for text that survived
    deletions: list[tuple[str, int, dict]] = []
    for stream_name, st in chapter_diff["streams"].items():
        for h in st["hunks"]:
            t = h["type"]
            src_stream = h["stream"].split(">")[0]
            dst_stream = h["stream"].split(">")[-1]
            if h.get("old_pos") is not None and h.get("new_pos") is not None and src_stream == dst_stream:
                anchors[src_stream].append((h["old_pos"], h["new_pos"]))
                if src_stream == "body" and h.get("old_page"):
                    page_anchors.append((h["old_page"], h["new_pos"]))
            if t == "equal":
                continue
            if h.get("new_pos") is not None and dst_stream in per_stream and h["new_pos"] < len(per_stream[dst_stream]):
                s = per_stream[dst_stream][h["new_pos"]]
                s.change = t
                s.words = h.get("words") or None
                s.similarity = h.get("similarity")
                counts[t] += 1
            elif t in ("deleted", "unreadable") and h.get("old_pos") is not None:
                deletions.append((src_stream, h["old_pos"], h))
                counts[t] += 1
    # Place each deletion after the nearest surviving sentence that preceded it in the old text.
    # Body sentences go inline after that sentence. Boxes, captions, tables and headings go into a
    # ghost block right after the block that holds the anchor, so a removed box reads as a box.
    deletions.sort(key=lambda d: (d[0], d[1]))
    inline_offsets: dict[tuple[int, int], int] = defaultdict(int)
    ghost_blocks: dict[tuple[int, str], Block] = {}

    def locate(stream: str, new_pos: int) -> tuple[Block, int] | None:
        seen = -1
        for b in blocks:
            for i, s in enumerate(b.sentences):
                if s.stream == stream and s.change not in ("deleted", "unreadable"):
                    seen += 1
                    if seen == new_pos:
                        return b, i
        return None

    def ghost_after(anchor_block: Block | None, kind: str) -> Block:
        key = (id(anchor_block) if anchor_block else -1, kind)
        if key not in ghost_blocks:
            if anchor_block is None:
                at = 1 if blocks and blocks[0].kind == "heading" else 0
                page = blocks[0].page if blocks else None
            else:
                at = blocks.index(anchor_block) + 1
                page = anchor_block.page
            g = Block(kind, 2, [], page, -1)
            blocks.insert(at, g)
            ghost_blocks[key] = g
        return ghost_blocks[key]

    for stream, old_pos, h in deletions:
        ghost = Sentence(h["old"], stream, "deleted" if h["type"] == "deleted" else "unreadable")
        before = [np for op, np in anchors.get(stream, []) if op < old_pos]
        found = locate(stream, max(before)) if before else None
        if stream == "body" and found is not None:
            target_block, target_index = found
            k = (id(target_block), target_index)
            target_block.sentences.insert(target_index + 1 + inline_offsets[k], ghost)
            inline_offsets[k] += 1
            continue
        if found is None and h.get("old_page"):
            # No surviving neighbour in its own stream: go by page, next to the last body text
            # that survived from the same or an earlier old page.
            candidates = [np for op, np in page_anchors if op <= h["old_page"]]
            if candidates:
                found = locate("body", max(candidates))
        anchor_block = found[0] if found else None
        kind = "body" if stream == "body" else stream
        ghost_after(anchor_block, kind).sentences.append(ghost)
    return counts


def sentence_html(s: Sentence, prefix: str = "", heading: bool = False, side: str | None = None) -> str:
    """One sentence with its change marked. `side` limits a reworded sentence's word diff to
    the words of one edition: "old" shows removed words only, "new" added words only."""
    if heading and not (s.change == "modified" and s.words):
        shown = display_title(s.text)  # small-caps headings arrive as "the mughals (16th TO 17th CENTURY)"
        s = Sentence(shown, s.stream, s.change, s.words, s.similarity)
    if s.change in ("modified",) and s.words:
        parts = []
        for op, tok in s.words:
            if (side == "old" and op == "+") or (side == "new" and op == "-"):
                continue
            t = escape(tok)
            parts.append(t if op == "=" else (f"<del>{t}</del>" if op == "-" else f"<ins>{t}</ins>"))
        inner = " ".join(parts)
    else:
        inner = escape(s.text)
    if not s.change:
        return f"<span class=s>{inner}</span>"
    quiet = " quiet" if s.change in QUIET else ""
    title = {
        "inserted": "Added in this edition", "deleted": "Removed in this edition", "modified": "Reworded in this edition",
        "moved": "Moved within the chapter", "restreamed": "Moved between text and a box", "resplit": "Same words, split into sentences differently", "typographic": "Only case, dashes or quotes differ",
        "punctuation": "Only punctuation differs", "unreadable": "Could not be read in one of the editions",
    }.get(s.change, s.change)
    return f"<span class='s chg chg-{s.change}{quiet}' title='{title}'>{inner}</span>"


def block_html(b: Block, side: str | None = None) -> str:
    inner = " ".join(sentence_html(s, heading=(b.kind == "heading"), side=side) for s in b.sentences)
    if b.kind == "heading":
        tag = {1: "h2", 2: "h3", 3: "h4"}.get(b.level, "h3")
        cls = " class='ghost'" if b.para == -1 else ""
        return f"<{tag}{cls}>{inner}</{tag}>"
    if b.kind == "body":
        return f"<p>{inner}</p>"
    if b.kind in SECTIONS:
        return f"<p class='sec sec-{b.kind}'>{inner}</p>"
    label = {"note": "Note", "caption": "Caption", "source": "Source", "table": "Table"}[b.kind] if b.kind in ("note", "caption", "source", "table") else b.kind
    return f"<aside class='box box-{b.kind}'><span class=boxlabel>{label}</span> {inner}</aside>"


def page_checks(book_id: str, diffs: dict, editions: list) -> list[dict]:
    """Pages the diff engine flags for a human look, per edition pair, with both page images."""
    by_id = {e.id: e for e in editions}
    out = []
    for (from_id, to_id), r in diffs.items():
        if from_id not in by_id or to_id not in by_id:
            continue
        items = []
        for c in r["chapters"]:
            if c.get("status") != "matched" or "pages" not in c:
                continue
            old_dir = chapter_dir_name(c["from"]["part"], c["from"]["number"])
            new_dir = chapter_dir_name(c["to"]["part"], c["to"]["number"])
            for p in c["pages"]["old"]:
                if p["suspect"]:
                    items.append({"kind": "old", "chapter": c, "old_dir": old_dir, "new_dir": new_dir, "page": p["page"], "other": p["new_page"], "score": p["score"], "sentences": p["sentences"]})
            for p in c["pages"]["new"]:
                items.append({"kind": "new", "chapter": c, "old_dir": old_dir, "new_dir": new_dir, "page": p["page"], "other": None, "score": p["score"], "sentences": p["sentences"]})
        items.sort(key=lambda i: i["score"])
        out.append({"from": by_id[from_id], "to": by_id[to_id], "flagged": items, "ocr": r.get("ocr")})
    return out


def pages_html(blocks: list[Block]) -> list[dict]:
    """Group blocks by printed page: [{page, html}]."""
    out: list[dict] = []
    for b in blocks:
        if not out or out[-1]["page"] != b.page:
            out.append({"page": b.page, "parts": []})
        out[-1]["parts"].append(block_html(b))
    for p in out:
        p["html"] = "\n".join(p.pop("parts"))
    return out


# ---------- build ----------

_SMALL = {"a", "an", "and", "the", "of", "to", "in", "on", "for", "or", "nor", "at", "by", "from", "with", "under"}


def display_title(title: str | None) -> str:
    """Titles come out of small-caps fonts as 'the mughals (16th TO 17th CENTURY)' or all caps.
    Shown in title case; a title that is already mixed case is left alone."""
    if not title:
        return "Untitled"
    words = [w.strip("(“\":") for w in title.split()]
    all_caps = [w for w in words if len(w) >= 3 and w.isalpha() and w.isupper()]
    all_lower = [w for w in words if len(w) >= 3 and w.isalpha() and w.islower()]
    odd = (
        title[:1].islower()
        or title.isupper()
        or (all_caps and all_lower)  # "the mughals (16th TO 17th CENTURY)"
        or re.search(r"[a-z][A-Z]", title)  # "delhI"
    )
    if not odd:
        return title
    words = title.lower().split()
    out = []
    for i, w in enumerate(words):
        core = w.strip("(“\"")
        if re.match(r"^\d+(st|nd|rd|th)$", core):
            out.append(w)
        elif i and core in _SMALL and not words[i - 1].endswith(":"):
            out.append(w)
        else:
            out.append(re.sub(r"[a-z]", lambda m: m.group(0).upper(), w, count=1))
    return " ".join(out)


def _env() -> Environment:
    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["md"] = lambda text: markdown.markdown(text, extensions=["tables"])
    env.filters["ttl"] = display_title
    return env


def _read_doc(name: str) -> str:
    path = REPO_ROOT / "docs" / name
    text = path.read_text() if path.exists() else ""
    return re.sub(r"^# .*\n", "", text, count=1)  # the template supplies the title


def write_compare_data(book_id: str, editions: list, diffs: dict, out: Path, *, log=print) -> int:
    """JSON for the compare view: every pair of editions, one file per aligned chapter, plus
    an index of pairs and chapters. Returns the number of chapter files written."""
    from ..diff import diff_editions
    from .compare import compare_chapter, single_side

    data_dir = out / "data" / book_id
    data_dir.mkdir(parents=True, exist_ok=True)
    index: dict = {"editions": [{"id": e.id, "label": e.label, "ocr": bool(e.raw.get("ocr"))} for e in editions], "pairs": {}}
    written = 0
    for i, a in enumerate(editions):
        for b in editions[i + 1:]:
            r = diffs.get((a.id, b.id)) or diff_editions(book_id, a.id, b.id)
            key = f"{a.id}__{b.id}"
            pair_dir = data_dir / key
            pair_dir.mkdir(exist_ok=True)
            chapters = []
            for c in r["chapters"]:
                frm, to = c.get("from"), c.get("to")
                old_dir = chapter_dir_name(frm["part"], frm["number"]) if frm else None
                new_dir = chapter_dir_name(to["part"], to["number"]) if to else None
                slug = new_dir or f"old-{old_dir}"
                if c["status"] == "matched":
                    payload = compare_chapter((REPO_ROOT / frm["file"]).read_text(), (REPO_ROOT / to["file"]).read_text(), c)
                elif c["status"] == "dropped":
                    payload = single_side((REPO_ROOT / frm["file"]).read_text(), "old")
                else:
                    payload = single_side((REPO_ROOT / to["file"]).read_text(), "new")
                (pair_dir / f"{slug}.json").write_text(json.dumps(payload, ensure_ascii=False))
                written += 1
                chapters.append(
                    {
                        "slug": slug,
                        "status": c["status"],
                        "old": {"number": frm["number"], "part": frm["part"], "title": display_title(frm["title"]), "dir": old_dir} if frm else None,
                        "new": {"number": to["number"], "part": to["part"], "title": display_title(to["title"]), "dir": new_dir} if to else None,
                        "counts": payload["counts"],
                        "changed_pages": sum(1 for row in payload["rows"] if row["real"]),
                        "pages": len(payload["rows"]),
                    }
                )
            index["pairs"][key] = {"summary": r["summary"], "chapters": chapters}
    (data_dir / "pairs.json").write_text(json.dumps(index, ensure_ascii=False))
    log(f"{book_id}: compare data for {len(index['pairs'])} edition pairs, {written} chapter files")
    return written


def build(out: Path, images_base: str, *, log=print) -> Path:
    env = _env()
    books = load_books()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)

    def write(path: str, template: str, **ctx) -> None:
        target = out / path.strip("/") / "index.html" if path != "/" else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(env.get_template(template).render(images_base=images_base, books=books, **ctx))

    files_by_book = {b: json.loads((MANIFEST_DIR / b / "files.json").read_text()) for b in books if (MANIFEST_DIR / b / "files.json").exists()}
    all_editions = {b: load_editions(b) for b in books if (MANIFEST_DIR / b / "editions.json").exists()}

    write("/", "index.html", editions=all_editions)
    write("/changes/", "changes.html", findings=_read_doc("findings.md"))
    write("/method/", "method.html", sources=_read_doc("sources.md"), text_format=_read_doc("text-format.md"), engine=_read_doc("diff-engine.md"))

    for book_id, editions in all_editions.items():
        book = books[book_id]
        diffs = {}
        for p in sorted((DIFF_DIR / book_id).glob("*.json")) if (DIFF_DIR / book_id).exists() else []:
            r = json.loads(p.read_text())
            for c in r["chapters"]:
                if c["status"] == "matched":
                    hunks = [h for st in c["streams"].values() for h in st["hunks"] if h["type"] in REAL]
                    hunks.sort(key=lambda h: (h.get("old_page") or h.get("new_page") or 0, h["type"]))
                    c["real_hunks"] = hunks
            diffs[(r["from"], r["to"])] = r
        write(f"/{book_id}/", "book.html", book=book, editions=editions, diffs=diffs, previous_edition=previous_edition, suspect_total=sum(r["summary"].get("suspect_pages", 0) for r in diffs.values()))
        write(f"/{book_id}/changes/", "changes_book.html", book=book, editions=editions, diffs=diffs, previous_edition=previous_edition, REAL=REAL)
        checks = page_checks(book_id, diffs, editions)
        write(f"/{book_id}/checks/", "checks.html", book=book, editions=editions, checks=checks, total=sum(len(c["flagged"]) for c in checks))
        write_compare_data(book_id, editions, diffs, out, log=log)
        write(f"/{book_id}/compare/", "compare.html", book=book, editions=editions)
        for ed in editions:
            prev = previous_edition(editions, ed)
            pair = diffs.get((prev.id, ed.id)) if prev else None
            sources = [f for f in files_by_book.get(book_id, {}).get("files", []) if f["path"].split("/")[2] in ed.raw["snapshots"] and f["path"].endswith(".zip")]
            chapters = []
            for ch in ed.raw["chapters"]:
                chdir = chapter_dir_name(ch["part"], ch["number"])
                md_text = (REPO_ROOT / ch["file"]).read_text()
                meta, blocks = chapter_blocks(md_text)
                chapter_diff = None
                if pair:
                    chapter_diff = next((c for c in pair["chapters"] if c["to"] and c["to"]["file"] == ch["file"]), None)
                counts = apply_changes(blocks, chapter_diff)
                pages = pages_html(blocks)
                chapters.append({"ch": ch, "dir": chdir, "counts": dict(counts), "pages": pages, "diff": chapter_diff})
            dropped = [c for c in pair["chapters"] if c["status"] == "dropped"] if pair else []
            write(f"/{book_id}/{ed.id}/", "edition.html", book=book, editions=editions, ed=ed, prev=prev, chapters=chapters, dropped=dropped, sources=sources)
            for i, c in enumerate(chapters):
                write(
                    f"/{book_id}/{ed.id}/{c['dir']}/", "chapter.html", book=book, editions=editions, ed=ed, prev=prev, chapter=c,
                    prev_chapter=chapters[i - 1] if i > 0 else None, next_chapter=chapters[i + 1] if i + 1 < len(chapters) else None,
                    chdir=c["dir"],
                )
        log(f"{book_id}: {len(editions)} editions, {sum(len(e.raw['chapters']) for e in editions)} chapter pages")
    return out
