# How editions are compared

`ncert-diff diff` compares consecutive editions of a book (and each OCR edition against the
born-digital edition before it). The output for a pair is `diffs/<book>/<from>__<to>.json`
and a matching `.html`.

## Units

Each chapter's Markdown is read back into units: body sentences, headings, and the tagged
blocks (notes, captions, sources, table rows). Body text, notes, captions, and sources are
split into sentences so that a paragraph split by a figure in one printing and whole in
another does not count as a change. Table rows stay whole and are sorted before comparison,
because typesetting changes their order. Every unit carries the printed page it sits on.

Matching uses a normalised key: case-folded, NFKC, all dash variants to "-", curly quotes
straightened, spaces around dashes removed, trailing punctuation dropped. The original text
is what gets reported.

## Chapters

Chapters are paired by the share of body sentences they have in common (at least 20 percent
of the smaller chapter), not by number or title. The 2023 rationalisation dropped two
chapters from each book and renumbered the rest, and the 2023 titles are set in small caps,
so neither number nor title is reliable. A chapter with no partner is reported as dropped or
added.

## Inside a chapter

For each stream, difflib aligns the two key sequences. Runs it cannot match exactly are
paired greedily by similarity (at least 0.55) so that a reworded sentence becomes one
"modified" hunk with a word-level diff instead of a deletion plus an insertion. What is left
is "deleted" or "inserted", except:

| Type | Meaning |
|---|---|
| `moved` | same sentence, different position in the same stream |
| `restreamed` | same sentence, different stream (a box became body text or the reverse) |
| `typographic` | same key, different surface form (case, dashes, quotes) |
| `punctuation` | the only word-level differences are punctuation or spacing (the 2023-24 editions inserted commas throughout) |
| `unreadable` | one side is text whose font has no Unicode map, or an edit on a page where the other edition has such text |

Modified hunks across streams (a note that became body text with one word changed) are
found in a second pass over the leftover deletions and insertions.

The HTML view shows deleted, inserted, and modified hunks and folds the rest away. Counts in
`summary` separate body text from the other streams.

## Pages to check

For every matched chapter the engine also scores each page: the share of its sentences
that survived into the other edition (equal, reworded, moved, or restreamed sentences all
count as survived). A page with at least four comparable sentences and fewer than half
surviving is listed on the book's "Pages to check" page with both page images, and a page
of the newer edition whose sentences mostly have no source is listed the same way. The list
cannot tell a real cut from a reading error. A person can, from the two images, and the
fix for a reading error goes into the book's overrides file (see `docs/text-format.md`).

## Known limits

- Hunks involving the OCR edition (2022-23 Our Pasts II) or the outlined-word recovery in
  the 2024-25 Our Pasts II files include reading errors. Check them against the page before
  quoting them.
- The 2018-19 Our Pasts III files have unreadable headings and boxes, so the comparison into
  and out of that edition is dominated by `unreadable` hunks and should not be read as a
  count of edits.
- Exercises ("match the following", fill-in-the-blank lines) change layout between printings
  and produce noisy hunks that are not content changes.
- No comparison yet between the old history books and the 2025 Exploring Society books.
  They share no chapter structure, so that needs topic-level alignment rather than this
  sentence-level engine.
