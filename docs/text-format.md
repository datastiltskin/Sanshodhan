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
  collapsed to one, and so is a word redrawn over the end of its own line in the 2007 files
  ("a French cartographer" followed by "cartographer" three times at the same place).
- The Sustainable Development Goal badge printed in the margins since 2019 is tagged as a
  caption so that its label does not run into the paragraph below it.
- The chapter title is a level-1 heading. Section headings are level 2, activity headings
  ("Let's recall", "Let's discuss") and box headings level 3.

## Page markers

`<!-- page 47 (pdf 3) -->` marks the start of each page: the printed number and the
position in the chapter PDF. Printed numbers come from the running footer and are checked to
advance one per page. A paragraph that runs across a page break is written before the marker
of the page it ends on. Some 2007-era chapter PDFs begin with the last page of the previous
chapter. Those pages are dropped. The opposite also happens: a file ends with the next unit's
opener and teacher's note (the 2024-25 Class 7 civics files). Those pages are moved to the
front of the next chapter, and their markers name the file they came from, as in
`<!-- page 37 (pdf 14 of ch03.pdf) -->`, so the page images still come from the right PDF.
A few pages inside an otherwise normal file can be flat images. They are read with OCR and
listed as `ocr_pages` in the front matter.

## Run-in headings

Some printings set a sub-heading as the bold first line of its paragraph rather than as a
block of its own (the 2023-24 Our Pasts III). A bold first line of two or more words with
no closing punctuation, followed by a paragraph, is written as a heading so the text has the
same shape as the other printings.

## Outlined words

Some files (the 2024-25 Our Pasts II) draw their italic terms as vector outlines with no
text behind them. Those runs are read with tesseract and then pulled towards words the
book is known to use in its other editions: a run whose letters spell a known word
becomes that word ("pardes i" to "pardesi", "Minhaj 1 Siraj" to "Minhaj-i-Siraj"), and an
unknown word is replaced by the nearest known one when they differ by a letter or two
("EXYIcise" to "exercise"). The raw reading is kept in the OCR cache, so the rule can be
changed without re-running tesseract.

## Sections

Four runs of a chapter are marked as sections, because the books set them apart and
reflow them between printings: `exercises` (from "Exercises" or the first "Let's recall"
heading to the end), `glossary` ("Glossary" or "Keywords"), `references` ("References",
"Notes"), and `teachers-note` (the unit's note to teachers, which ends at the chapter
title). A marker line `<!-- section: exercises -->` precedes the line that opens the
section. The parser also recognises the opening lines themselves, so a text without
markers reads the same. Inside a section every block keeps its role tag, but it is compared
in the section's own stream, and exercises, glossaries, and references are compared without
regard to order (questions get renumbered and glossary entries reflowed). A `[table]` block
inside a section is a text box, not a table, so its rows are split into sentences like any
other text.

## Hand corrections

`overrides/<book>.yaml` holds corrections to extracted text that no rule should make: an OCR
misreading on one page, a glyph that leaked into a heading. Each entry names the snapshot
(or `*`), the chapter (or `*`), the exact text to find, its replacement, and a note saying
why. The editions step applies them after extraction and before fingerprinting, so a
corrected text still groups with the snapshots that share it. Applied corrections are listed
in the chapter's front matter and on its page on the site. An entry addressed to a specific
snapshot and chapter that no longer matches is reported in the log and in
`manifest/<book>/editions.json` under `overrides_missed`, so a re-extraction cannot drop a
fix silently.

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
