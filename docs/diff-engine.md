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

The sentence splitter keeps common abbreviations whole ("Fig.", "Figs.", "No.", "Vol.", "Ch.",
"p.", "Rs." and the like) and treats a single capital with a full stop as an initial ("W.
Daniell", "S.I. Rao", "D.K. Basu"), so a credits list or a name does not split into pieces.
A lone "I." still ends a sentence, since it is usually a regnal number ("Rajendra I.").

The labels of a chart come out of the PDFs as one short caption each ("Pensions", "5 p.",
"(4%)"). A run of four or more consecutive short captions on one page, at least one of them
a figure such as "5 p." or "(4%)", is read as one caption unit with the labels joined by " / ".
A changed chart is then one change and a new chart one insertion, rather than dozens of
one-word hunks.

Matching uses a normalised key: case-folded, NFKC, all dash variants to "-", curly quotes
straightened, spaces around dashes removed, trailing punctuation dropped. A fill-in blank
(any run of three or more underscores or dashes) becomes one blank token, since the printed
rule changes length between printings. A list label glued to its text ("1.that") gets its
space back. In the exercises and glossary streams the leading label ("12.", "(a)", "b.",
"(iv)") is dropped from the key, so renumbered questions match. The original text is what
gets reported.

## Chapters

Chapters are paired by the share of body sentences they have in common (at least 20 percent
of the smaller chapter), not by number or title. The 2023 rationalisation dropped two
chapters from each book and renumbered the rest, and the 2023 titles are set in small caps,
so neither number nor title is reliable. A chapter with no partner is reported as dropped or
added.

Rationalisation also merged chapters. In Social and Political Life III, the storyboard,
glossary and exercises of old chapter 4 moved into new chapter 3 and the rest of old chapter
4 was cut. So after the one-to-one pairing, a chapter left without a partner is folded into
a pair when at least 60 percent of its sentences (any stream, not only body text) reappear in
that pair's chapter on the other side. The pair is then compared against the concatenation
of the two chapters, so the moved half matches and only the real cuts remain as deletions.
The same works the other way, for one old chapter split into two new ones. The chapter entry
keeps its usual fields and names the primary chapter in `from` and `to`, and adds
`merged_from` (old chapters folded in) or `merged_to` (new chapters folded in), each a list
of `{number, part, title, file}`. Hunk positions count through the concatenation, primary
chapter first, and the compare view renders the same concatenated text for that side.

Text can also be filed under the neighbouring chapter in one edition (a unit opener and its
teacher's note, cut into the files at a different page). After the chapters are compared, a
deletion in one matched chapter whose key matches an insertion in another (keys of 20
characters or more) is classed `moved` in both. Each half keeps only its own side's position
and page, because positions count within one chapter's file.

## Inside a chapter

For each stream, difflib aligns the two key sequences. Runs it cannot match exactly are
paired greedily by similarity (at least 0.55) so that a reworded sentence becomes one
"modified" hunk with a word-level diff instead of a deletion plus an insertion. What is left
is "deleted" or "inserted", except:

| Type | Meaning |
|---|---|
| `moved` | same sentence, different position in the same stream |
| `restreamed` | same sentence, different stream (a box became body text or the reverse) |
| `resplit` | the same words, split into sentences differently (one sentence here, two there, as when a page break or a table read as text moves a sentence boundary) |
| `typographic` | same key, different surface form (case, dashes, quotes) |
| `punctuation` | the only word-level differences are punctuation or spacing (the 2023-24 editions inserted commas throughout) |
| `unreadable` | one side is text whose font has no Unicode map, or an edit on a page where the other edition has such text |

Modified hunks across streams (a note that became body text with one word changed) are
found in a second pass over the leftover deletions and insertions.

Two more passes compare word bags (the words of a unit as a multiset, case and punctuation
and order ignored) across all streams of a chapter. Speech bubbles, table rows and box
paragraphs are read in a different order, or into a different stream, from one printing to
the next, and cut into sentences differently. In the first pass, a piece whose words are
exactly the words of one or more pieces on the other side, all on one page or two facing
pages, is the same text: one piece becomes `moved` or `restreamed`, several become one
`resplit`. Halves of `modified` hunks take part, so a fuzzy pairing of a whole with one of
its parts is undone. Only exact word bags count, so a real edit stays loud. In the second
pass, a leftover deletion and insertion whose word bags are at least 90 percent alike become
one `modified` hunk, since the words differ.

The HTML view shows deleted, inserted, and modified hunks and folds the rest away. Counts in
`summary` separate body text from the other streams.

## The compare view

The site's compare page (`/<book>/compare/`) takes any two editions and a chapter. Its data
is written at build time for every pair of editions, one JSON file per chapter, so no server
is needed. Pages are paired by where their text went: each old page goes with the new page
that most of its surviving sentences landed on, walking forward through both editions, so
a page that was cut or inserted stands alone in its row. The old page's text carries the
removals and the old half of each rewording, the new page's text the additions and the new
half, and a unified rendering puts the removals inline in the new text. Settings (side by
side or unified text, side by side or onion-skin images, only changed pages, minor
differences) are remembered in the browser and carried in the address: `layout=split|unified`,
`images=side|onion|hidden`, `changed=1`, `minor=1`, and `fade=0..100` for the onion skin,
alongside `from`, `to`, and `chapter`.

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
- Exercises ("match the following" tables read by columns) still change layout between
  printings and produce noisy hunks that are not content changes. Blanks and renumbering are
  handled in the key, but OCR drops blank lines and detaches exercise numbers.
- Table rows are compared whole, so a change to one cell shows as a modification of the
  whole row, and a row whose cells were read in a different order shows as a change when
  the table did not change. Comparing cell by cell (a row as a bag of cells, a cell as the
  unit of change) is the planned fix. It changes what the counts mean for tables, so it is
  a deliberate step for later rather than a quiet tweak.
- No comparison yet between the old history books and the 2025 Exploring Society books.
  They share no chapter structure, so that needs topic-level alignment rather than this
  sentence-level engine.
