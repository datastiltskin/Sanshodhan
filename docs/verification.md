# Verifying a diff against the page images

The texts come out of PDFs by rules, and some printings by OCR. Both produce faults that
look like edits: a dropped paragraph, a caption glued to a sentence, a misread word, two
sentences joined across a page break. No comparison of text with text can tell such a
fault from a change NCERT made. The page images can.

So the rule for anyone, and for any agent, checking the diffs is:

1. When a hunk looks like noise (a rewording that touches one near-identical word, a
   deletion whose words reappear nearby, a sentence that runs into a caption or a heading,
   a page where most sentences "vanished"), open the page image of **both** editions
   before deciding. The images are rendered per printed page under
   `site/images/<book>/<edition>/<chapter>/pNNN.webp` (`uv run ncert-diff render-pages`),
   and the compare view shows them side by side at `/<book>/compare/`.
2. Decide from the images which of these it is, and record it with the book, edition,
   chapter and printed page:
   - a real change in the book (nothing to fix, worth noting in `docs/findings.md`);
   - an extraction fault that a rule can fix for every file of that kind (a change in
     `extract.py` or `clean.py`, with a test);
   - a one-off fault, such as an OCR misreading on one page (an entry in
     `overrides/<book>.yaml`, which is applied on every later extraction);
   - noise the diff engine should classify as minor (a rule in `diff.py`).
3. Never "correct" a text from memory or from the other edition's text alone. The image
   is the evidence; the text of the other edition is only a hint of what to look for.

An OCR reading without this check is not evidence of anything. The outlined-word OCR, the
page OCR for rasterised printings, and the vocabulary snapping that steadies them are all
guesses until a page image confirms them.

## A second reading by a local model

`scripts/ocr_check.py <book> <edition> <chapter> [pages]` has a local OCR model (glm-ocr
under Ollama) read a page at 150 dpi and prints the words that only one of the two readings
has. It is a mechanical cross-check, not a judge: a word only in the model's reading says
where to open the page image, and the image still decides. At about fifteen seconds a page
it is for the flagged pages and the changed sentences, not for the build.

It is not a replacement for tesseract on the two rasterised printings. Measured on
2026-10-19 against the text layer of the neighbouring printing (chapter word bags, body
and headings), tesseract missed 1.5% of the true words of the 2022-23 Our Pasts II scan
and glm-ocr 1.2%, and on the 2021-22 Social and Political Life II scan tesseract missed
0.7% and glm-ocr 2.0%, because the model skips whole paragraphs on pages dense with boxes
and speech bubbles. Both engines read the margin boxes, so the noise in the pairs against
a scan comes from layout and roles, not from word reading, and that is where the rules
work. The one place the model reads better is a table (the Mughal emperors table in
chapter 4, where tesseract drops most of the dates), so it is worth a second reading there.

## Flagging from the browser

`uv run python scripts/annotate_server.py` serves `site/` on port 8765 with an annotation
layer on every page. Select any text, press the Flag button that appears, pick what kind of
fault it is (extraction, wrong role, wrong diff, the book's own) and say what it should be.
The flag lands in `review/annotations.jsonl` with the page address, the printed page and
side it came from, the selected text and its sentence. A panel at the bottom right lists the
page's flags and deletes them. Nothing in `site/` changes, so the deployed site never carries
the layer. The file is the input to a fix pass, the same way a review file is.

## A spelling pass

`scripts/spellcheck.py [<book> [<edition>]]` lists the words in the texts that no dictionary
knows and that no other edition of any book uses. An extraction fault mostly leaves such a
word behind: a misread ("Błack"), two words glued ("QImagine"), a word cut after its first
letter ("g overnment"), a word doubled by a shadow line ("India India"). By default it prints
the lower-case plain-letter words, the doubled and the glued ones. Capitalised words and
words with transliteration marks are hidden unless asked for (`--names`, `--diacritics`,
`--all`), because for a book with one edition those are mostly names the dictionary lacks.

The list is a set of places to open, not a list of faults. The page image decides: a word
the book itself misspells ("recieves" in the 2007 Our Pasts II) is accepted into
`scripts/spelling-accept.txt` and left in the text, a word the extraction broke gets a rule
or an override like any other finding. A spelling pass is cheap enough to run after every
rule change, alongside `scripts/text_changes.py`.

## The 2015-16 ePubs as a reference

`scripts/epub_check.py <book> [<edition>] [--roles] [--all]` compares the extracted text of
one edition with NCERT's own ePub of the 2015-16 printing (docs/sources.md, "ePubs"). The
ePub is reflowable XHTML from the same InDesign files, so its paragraphs are an independent
reading of the same text, with the role of each in a class name. The edition compared is
the one whose sentences overlap the ePub most, unless named. Per chapter the report lists:

- sentences the ePub has and our text lacks ("ePub only"): a lost paragraph, a page the
  extractor dropped, or text the 2015-16 revision added that our nearest printing lacks;
- sentences our text has and the ePub lacks ("ours only"): a glued caption, a speech
  bubble the ePub left in its image, an insert page, or junk;
- the same sentence in different words ("worded differently", listed with `--all`): the
  revision between printings, or a stray space the ePub export left;
- the same sentence under different roles (`--roles`).

Matching ignores spaces and punctuation, and a sentence contained in a longer unit on the
other side counts as present, so sentence splitting does not raise the counts. The counts
are places to open, not faults: a whole chapter with no matches is a fault (the first run
found the 2014 to 2024 India and the Contemporary World I editions with chapter 3 missing
and its last page filed as chapter 6, because an 80 pt question-mark ornament had made an
exercise line pass for a chapter number), a few "ePub only" sentences per chapter are
usually the 2015-16 revision (the Rani Avantibai sentences of Our Pasts III chapter 5
appear in 2019, not 2014), and the "ours only" count of a civics book is mostly its comic
strips, whose speech bubbles the ePub keeps as pictures.

Limits: one printing per book, no page numbers (reports print the PDF page as "pdfN"
where the printing has no printed numbers), and the Our Pasts II bundle's chapter 10 is a
geography chapter packed in by mistake.

## After changing a rule

A change to the extractor or the OCR re-makes the texts of every edition it touches, and a
rule that fixes one page can break another ("sawar" read right, but a margin box glued to
the paragraph beside it). So a rule change is not done when its tests pass: the affected
editions' pairs are reviewed again against the images, with the same entries as a first
review, before the texts are committed. A review made before the change says nothing
about the texts made after it.

A fall in the hunk counts is not proof either, and a rise is not always a regression. Two
printings of one page are often broken the same way, and then the pair shows nothing. A rule
that fixes one printing and not the other makes the pair rise while the texts got better
(the 2023 and 2024 Social and Political Life II shared a caption glued into a sentence until
2026-10-19). So after a rule change the changed sentences are read on both sides of every
pair, not just the pairs whose counts moved, and the spelling pass (below) is run, because a
fault both editions share is invisible to the comparison but not to a dictionary.

## Reviewing systematically

A review pass goes book by book over the consecutive edition pairs (every edition takes
part in the pair before it and the pair after it, so a fault in any edition surfaces
there). For each pair, `diffs/<book>/<from>__<to>.json` lists the hunks per chapter and
stream, and `pages` per chapter lists the pages where fewer than half the sentences
survived. The reviewer reads the hunks, opens the images for anything doubtful, and writes
what they found to `review/<book>.md` in the form above. A fix pass then works from those
files: overrides per book, rules in the code with tests, and a re-run of `extract`, `diff`
and `build` to confirm the counts fell.

When the review is delegated to an agent, the page images fill its context quickly. A
reviewer given a whole book at once can spend an hour re-opening the same pages and write
nothing. So a brief gives one agent one part or a few hundred changed sentences, asks it to
open each page once and judge every sentence on it in one go, to write its findings file
after every chapter and resume from that file after a reset, and to reuse pages already
rendered. A run that has read far more images than there are pages has looped, and is
stopped rather than waited on.
