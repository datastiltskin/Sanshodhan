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
  ("a French cartographer" followed by "cartographer" three times at the same place), and a
  clipped first copy of a heading ("Bhopal Gas T" four times before "Bhopal Gas Tragedy").
- A list item that wraps can arrive as two blocks, the marker line and a line indented to
  the item's text column right below it. The second is folded into the first, whatever
  letter it starts with.
- The Sustainable Development Goal badge printed in the margins since 2019 is tagged as a
  caption so that its label does not run into the paragraph below it.
- The 2016 civics files fake their bold by drawing each line again with the first glyph left
  off ("prosecution" then "rosecution"). Those copies are dropped like any other shadow.
- Letter-spaced lines in narrow boxes ("e d u c a t i o n w h i c h") are closed up. A space
  glyph that touches the letters on both sides is a letter space, one with a visible gap is a
  word space, so the result is "education which". Only runs of three or more one-letter
  tokens (or a line made of nothing else) are touched.
- Square list bullets (a Wingdings glyph, or "¢" where the font is re-embedded) start a new
  item written as `- item`, so a list without closing punctuation does not become one
  sentence. A capitalised paragraph after the last item starts a new paragraph.
- The rupee font of the 2019 and later civics files gives "₹" as a backtick, which is mapped
  back. A list number glued to its first word ("1.that" in the 2022 civics) gets its space.
- Decorative glyphs are dropped: the arrow before "Activity" (a control code or a dagger in
  the text layer), and an oversized letter that no paragraph starts beside, such as the "Q"
  of the question boxes and the "Po" of the police-station art. A real drop cap is joined to
  the paragraph that starts next to it.
- Text set smaller than the body that turns up while a body paragraph is still open (a box
  set into the column, a side question) is written after that paragraph, which goes on past
  it. A paragraph set straight under a caption in the caption's size is part of the caption.
- A box in the margin set at body size (the Our Pasts III Activity boxes, glossary entries and
  Source boxes) is told from the text column by where it sits: alone beside the column, or in
  a column of its own much narrower than the text column. On a page read with OCR only this
  geometry counts, since the sizes there are estimates. It is written after the column
  paragraph it sits beside, which goes on past it ("... could civilise India. To do" /
  "this, it was necessary ..." across the page turn). Its blocks join only where the next one
  plainly continues the last (a lower-case start), so each glossary entry stays a line of its
  own, and a box title there ("Language of the wise?") does not end the column paragraph.
- The Exploring Society "The Big Questions" title is set as two overlapping blocks, "The Big"
  over a larger "Questions". The two are one heading, so "Questions" alone never opens the
  exercises section.
- A line of nothing but small numbers, none above 20 (the badges 1 to 7 on a photo collage,
  the steps of a flow chart, the axis of a bar chart), is a label in a picture and is dropped.
  Larger values over a chart's bars are its data and stay.
- Spaces that the page does not show are dropped inside a word: a space with no advance at all
  ("The g overnment"), a space carrying the width of a letter the text layer made zero wide
  ("Kaṇṇ agi", "Pāṭ aliputra"), and a thin space between two letters ("cold s torage"). The
  space after a ligature ("off and") is an ordinary one and stays.
- The chapter title is a level-1 heading. Section headings are level 2, activity headings
  ("Let's recall", "Let's discuss") and box headings level 3.

## Captions

- A caption's second line, set as a block of its own, joins the caption straight above it
  when it starts in lower case, follows a comma or a bare "Fig. 1.23.", or overlaps a "Fig."
  caption in the same face that has no closing punctuation ("... in Bandhavgarh" / "National
  Park, Madhya Pradesh"). This keeps side-by-side captions apart. A description set under a
  caption title after a gap is a caption of its own.
- The first lines of two side-by-side captions that PyMuPDF puts on one line ("Fig. 1.13. ..."
  and, after a wide gap, "Fig. 1.14. ...") are split at the gap.
- A caption that starts "Fig." and a margin note's label ("Transparency:") start a new tagged
  block, whatever the block before them ends with.
- The lines of a centred speech bubble in the civics comics, cut into a block per line or two,
  are one block when the next line starts in lower case, so bubbles side by side no longer
  interleave. A poem's centred lines each start with a capital and stay apart. The same holds
  for a wrapped line set flush left under an unfinished line, so two columns of exercises read
  in page order do not interleave ("... the household tasks" / "undertaken by women in your
  home." beside "d. The work that women do is less" / "valued than that of men.").
- Map axis ticks ("60E", "70°E") are dropped, and ticks read onto the front of a caption line
  ("70E 80E 90E Fig. 6.2. ...") are cut from it.

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
same shape as the other printings. The 2022 Our Pasts III files embed their bold face without
the bold flag, so there a first line in a font the next line does not use counts as bold.
A short italic or bold line straight above a paragraph and aligned with it ("Gulamgiri"), a
bold italic figure-group title, and a short line in a display size well above the body
("The value of paper") are headings too.

## Outlined words

Some files (the 2024-25 Our Pasts II) draw their italic terms as vector outlines with no
text behind them. Those runs are read with Apple's Vision framework on macOS (the `ocrmac`
package) and with tesseract elsewhere. Vision reads the italic outlines that tesseract
garbled ("sawar", "pardesi", "flocks and herds."). The reading is then pulled towards words
the book is known to use in its other editions: a run whose letters spell a known word
becomes that word ("pardes i" to "pardesi", "Minhaj 1 Siraj" to "Minhaj-i-Siraj"), and an
unknown word is replaced by the nearest known one when they differ by a letter or two
("mugtis" to "muqtis"). Fragments of one word that the outline detector cut at a ligature
are joined before reading, and a run that stands alone (a diagram label, a whole outlined
line) is read from a crop a few points wider than the detector's box, which clips the first
and last letters of small labels. A quote the engine sees in the slant of an italic with no
partner on the line is dropped. A fragment as small as the "s." that finishes a word whose
stem is in the text layer is read too, and joined to that word without a space. Box labels
("Imagine", "Activity", "Elsewhere") are headings, so a paragraph cut short at a page foot
cannot run into the box below it. The raw reading is kept in the OCR cache under a key that
names the engine, so the rules can be changed without reading the page again.

A run is placed in the line it sits on when it comes within a word space of it. The reading is
then checked against the text around it: punctuation the text layer already has is not
repeated and gets no space before it, a full stop before a lower-case word is dropped, a
leading "- " is dropped, and an opening quote that nothing closes (or a closing quote that
nothing opens) is taken for the slant of an italic word and removed.

## Keyword columns

The Our Pasts books end a chapter with a KEYWORDS column in the margin: a label and one term
per line. The label becomes a "### Keywords" heading and each term a list item ("- iqta"),
which opens the glossary section, so the terms are compared as a set and never read as part
of the question beside them. Some printings put an instruction in that column instead
("Go through the chapter and make your own list of six keywords."), and one encoding sets it
one line per block. A run of column lines that reads as prose (a line of more than three
words, or a sentence end inside the run) is joined into one note rather than listed as terms.

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
(or `*`), the chapter (a number, `prelims` for the front matter pages, or `*`), the exact
text to find, its replacement, and a note saying why. A book in parts (Exploring Society)
repeats its chapter numbers, so there an entry also names the `part`, and an entry without
one reaches both parts (the shared front cover). The editions step applies them after extraction and before fingerprinting, so a
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

A sliver of text set smaller than the body that runs off the edge of the page is dropped: the
2007 files carry the ends of the facing page's caption lines ("har baghs", "hmir, 634.") in the
outer tenth of this one, where nothing legible is printed. A caption that only loses its first
letters to the edge is kept.

Dropped entirely: running footers (page number, book or chapter name, "Rationalised 2023-24"),
the rotated "©NCERT not to be republished" watermark in older files, and the chapter number
glyph. InDesign slug lines mostly sit outside the page crop box and never reach the text
layer, and the few that do are dropped as footers.

Position and size alone do not make a footer. The last lines of a page in the 2021-24 civics
files, and some photo captions, sit as low as the footers. A small block in the footer band
is dropped only when it is a page number, a print-run label, a running title, text that
recurs in the band on other pages of the same file, or a block on the row where other
pages' footers sit. When a caption's last line is glued to the running title ("Hampi. TOWNS,
TRADERS AND CRAFTSPERSONS"), the title is cut off and the rest is kept.

## OCR editions

Snapshots without a text layer are read with tesseract (`src/ncert_diff/ocr.py`). Pages are
rendered at 300 dpi, tesseract's TSV word boxes are grouped into its paragraphs, and those
become the same blocks the normal path classifies. Font sizes are estimated from line
heights, so roles are rougher: captions sometimes land as `[table]`, and paragraph breaks
follow tesseract's segmentation rather than the typesetter's. Such editions carry `-ocr` in
their id, `ocr: true` and an `ocr_confidence` in the front matter, and the raw tesseract
output is cached under `pdfs/<book>/<snapshot>/ocr/`. A paragraph whose words tesseract read
with a mean confidence under 50 is lettering on a map or a drawing ("i Lf wie Royats = __ DE
Morrie") and is dropped, as is a short fragment under 70. Treat word-level differences against an
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
