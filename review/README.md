# Review files

One file per book, `review/<book>.md`, written by a review pass over the consecutive
edition pairs and kept as the record of what was checked. The rule for the pass is in
`docs/verification.md`: nothing is called a fault or an edit without looking at the page
images of both editions.

Each entry has this shape:

```
### <book> <from edition> -> <to edition>, chapter N, printed page P (old) / Q (new)
- Hunk: <type and stream> "<old text>" -> "<new text>"
- Images: <what the two pages actually show, one line each>
- Verdict: real change | extraction fault (rule) | extraction fault (one-off) | engine noise
- Fix: <the override entry, or the rule to add, or "none">
```

Verdicts are what the fix pass works from. "Extraction fault (one-off)" entries carry a
ready-to-paste override (`snapshot`, `chapter`, `find`, `replace`, `note`). "Rule" entries
describe the pattern and name every place it was seen, so a code change can be tested
against them.

## Reviewing after a rule change

A review of texts that were re-made after a rule or OCR change starts from the sentences
that changed, not from all hunks:

```sh
uv run python scripts/text_changes.py <book> [<edition>]
```

lists, per chapter and printed page, the sentences present in the working tree but not in
the last commit and the reverse. Every listed page is opened in both the old and the new
rendering of that edition's PDF page (the same page, since the edition did not change, only
its extraction), and the entry records whether the new text matches the page. Only then are
the diffs against the neighbouring editions read, as in a first review.
