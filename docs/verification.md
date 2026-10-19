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
where to open the page image, and the image still decides. The model reads the main text
column and skips margin boxes and page furniture, so words only in our text are usually a
box. At about fifteen seconds a page it is for the flagged pages and the changed sentences,
not for the build.

## After changing a rule

A change to the extractor or the OCR re-makes the texts of every edition it touches, and a
rule that fixes one page can break another ("sawar" read right, but a margin box glued to
the paragraph beside it). So a rule change is not done when its tests pass: the affected
editions' pairs are reviewed again against the images, with the same entries as a first
review, before the texts are committed. A review made before the change says nothing
about the texts made after it.

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
