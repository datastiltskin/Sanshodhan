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

## Reviewing systematically

A review pass goes book by book over the consecutive edition pairs (every edition takes
part in the pair before it and the pair after it, so a fault in any edition surfaces
there). For each pair, `diffs/<book>/<from>__<to>.json` lists the hunks per chapter and
stream, and `pages` per chapter lists the pages where fewer than half the sentences
survived. The reviewer reads the hunks, opens the images for anything doubtful, and writes
what they found to `review/<book>.md` in the form above. A fix pass then works from those
files: overrides per book, rules in the code with tests, and a re-run of `extract`, `diff`
and `build` to confirm the counts fell.
