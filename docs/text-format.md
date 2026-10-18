# Extracted text format

`uv run ncert-diff extract` turns every downloaded chapter PDF into one Markdown file under
`texts/<book>/<edition>/`. The aim is text that diffs cleanly between editions while still
mapping back to the printed page.

## Files

- `NN-<slug>.md` per chapter, `prelims.md` for the front matter pages. Books with two parts
  (Exploring Society) use `partP-NN-<slug>.md`.
- YAML front matter records the book, edition id, the snapshots that share this text, chapter
  number and title, the source PDF path and its sha256, PDF page count, printed page range, and
  a fingerprint of the body text.

## Body

- One paragraph per line. Lines inside a PDF text block are joined with single spaces.
- A paragraph interrupted by a figure, a side note, or a page break is joined back together.
  The joined paragraph is written where it starts.
- Line-end hyphens are kept and the next line is attached without a space
  ("great-great-grandfather", "1526-1530"). NCERT's PDFs have no automatic hyphenation, so
  a hyphen at a line end is always part of the word.
- Decorative headings drawn several times for a shadow effect ("Let's recall" x5) are
  collapsed to one.
- The chapter title is a level-1 heading. Section headings are level 2, activity headings
  ("Let's recall", "Let's discuss") and box headings level 3.

## Page markers

`<!-- page 47 (pdf 3) -->` marks the start of each page: the printed number and the
position in the chapter PDF. Printed numbers come from the running footer and are checked to
advance one per page. A paragraph that runs across a page break is written before the marker
of the page it ends on. Some 2007-era chapter PDFs begin with the last page of the previous
chapter. Those pages are dropped.

## Tagged blocks

Anything that is not body text is kept as a blockquote with a role tag, so later diffs can
compare body only, or everything:

| Tag | What it is |
|---|---|
| `[caption]` | figure and map captions (Bookman 10 pt) |
| `[note]` | side-column notes, activity questions, "Elsewhere" boxes, glossary entries (Lucida Sans) |
| `[source]` | quoted primary sources set in Monotype Corsiva |
| `[table]` | table cells (Bookman 11 pt in the body column), one row per block |

Dropped entirely: running footers (page number, book or chapter name, "Rationalised 2023-24"),
the rotated "©NCERT not to be republished" watermark in older files, and the chapter number
glyph. InDesign slug lines sit outside the page crop box and never reach the text layer.

## OCR editions

Snapshots without a text layer are read with tesseract (`src/ncert_diff/ocr.py`). Pages are
rendered at 300 dpi, tesseract's TSV word boxes are grouped into its paragraphs, and those
become the same blocks the normal path classifies. Font sizes are estimated from line
heights, so roles are rougher: captions sometimes land as `[table]`, and paragraph breaks
follow tesseract's segmentation rather than the typesetter's. Such editions carry `-ocr` in
their id, `ocr: true` and an `ocr_confidence` in the front matter, and the raw tesseract
output is cached under `pdfs/<book>/<snapshot>/ocr/`. Treat word-level differences against an
OCR edition with suspicion until they are checked against the page image.

## Known limits

- Consecutive printings that were re-typeset (2023-24 to 2024-25, 2014 to 2019 for Class 8)
  show many changed lines even where the words are the same: small-caps headings come out in
  a different case, table rows arrive in a different block order, and a paragraph split by a
  figure in one printing may be whole in the other. The diff stage will need word-level,
  case-aware comparison and a table-row sort. Do not read line counts as content changes.

- Titles in the 2023 files are set in a small-caps font and come out in lower case
  ("the mughals (16th TO 17th CENTURY)"). They are left as the PDF has them.
- Reading order is body column first, then side column, per page. Multi-column tables are
  flattened one block per row.
- Role assignment is by font size and position. Pages with unusual layouts (full-page maps,
  timelines) can produce `[note]` blocks that are really body text. Check `role_counts` in
  `manifest/<book>/editions.json` for outliers.
