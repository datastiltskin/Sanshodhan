# Sanshodhan

See what changed in NCERT textbooks over the years. A `git diff` for NCERT textbooks: every
edition of a book is laid out beside the next, with the additions, deletions, and rewordings
between printings shown next to the original pages. Sanshodhan (संशोधन) is the Hindi word
for a revision or an amendment.

Current scope: history and civics for the middle classes. Class 7 "Our Pasts II" (2007 to
2025) and "Social and Political Life II", Class 8 "Our Pasts III" and "Social and Political
Life III", and the 2025 Class 7 successor "Exploring Society: India and Beyond". English
editions only for now.

## What is here

- `docs/verification.md` is the rule for checking any doubtful diff: open the page images of
  both editions. Text compared with text cannot tell an extraction fault from an edit.
  `scripts/text_changes.py` lists the sentences a rule change altered,
  `scripts/spellcheck.py` lists the words no dictionary and no other edition knows, and
  `scripts/ocr_check.py` has a local OCR model (glm-ocr under Ollama) re-read a page and
  prints the words the two readings disagree on, as pointers to what to open.
- The site's compare view (`/<book>/compare/`) shows any two editions of a chapter page
  against page, with both page images and both texts, in split or unified form.
- `overrides/<book>.yaml` holds hand corrections to extracted text (an OCR misreading, a stray
  glyph), applied on every extraction and listed on the chapter's page.
- `sources.yaml` lists every PDF the project uses: Wayback Machine snapshots (one per known
  distinct edition) and the live files on ncert.nic.in. This is the only place archive URLs live.
- `pdfs/` (not in git) holds the downloaded books, one folder per snapshot, with readable names.
- `manifest/` records what was downloaded (URL, timestamp, sha256, size) and how snapshots
  group into editions.
- `texts/` holds the extracted and cleaned Markdown, one file per chapter per edition, with
  page markers so text can later be shown beside the page image.
- `diffs/` holds the edition comparisons (JSON for machines, HTML for reading).
- `src/ncert_diff/site/` builds the website: Jinja templates, one hand-written stylesheet,
  and a little vanilla JavaScript (change toggles, the compare view, the search page). No
  framework, no build step beyond `ncert-diff build`, which also writes the search index
  with Pagefind. `docs/search.md` describes the search feature end to end.
- `docs/adding-a-book.md` is the step-by-step process for bringing in another book.
- `docs/sources.md` has the research behind all of this: book codes, URL eras, archive coverage,
  the 1967 to 2025 lineage, and NCERT's own list of what was cut in 2022-23.

## Running it

Needs [uv](https://docs.astral.sh/uv/), curl, and, for the rasterised 2022-23 printing,
[tesseract](https://github.com/tesseract-ocr/tesseract) with English data (`brew install tesseract`).
On macOS the words that some files draw as outlines are read with Apple's Vision framework
(the `ocrmac` package, installed with the project), which reads them far more reliably than
tesseract. Elsewhere tesseract is used for those too.

```sh
uv sync
uv run ncert-diff fetch            # download everything in sources.yaml, once
uv run ncert-diff fetch our-pasts-2
uv run ncert-diff status           # what is on disk
uv run ncert-diff extract          # PDFs -> texts/ and manifest/<book>/editions.json
uv run ncert-diff editions         # which snapshots collapsed into which edition
uv run ncert-diff diff             # compare consecutive editions -> diffs/<book>/*.json and .html
uv run ncert-diff render-pages     # one WebP per printed page -> site/images/<book>/<edition>/<chapter>/
uv run ncert-diff build            # the website -> site/ (images expected at --images-base, default /images)
                                   # also the search index -> site/pagefind/ (skip with --no-search)
                                   # --base-url /Sanshodhan when the site is served under a path, as on GitHub Pages
uv run pytest
```

To preview the site locally: `python3 -m http.server 8765 -d site` and open
http://127.0.0.1:8765/. Search works there too, since the index is plain files. To review it, `uv run python scripts/annotate_server.py` serves the
same pages with a flagging layer (select text, press Flag) that writes to
`review/annotations.jsonl`. In production the HTML is deployed to GitHub Pages by
`.github/workflows/site.yml` and the page images are uploaded to a Cloudflare R2 bucket by
`scripts/upload-images.sh`, with the bucket's public URL in the `IMAGES_BASE` repository
variable. The workflow builds for `/<repository name>`, where a GitHub Pages project site
lives. With a custom domain, set the `BASE_URL` repository variable to `/`.

`diffs/index.html` lists every comparison with counts. Each pair's HTML shows deleted,
inserted, and modified sentences per chapter with word-level highlights, and folds away the
quiet differences (moved, re-streamed, punctuation-only, case-only, unreadable). See
`docs/diff-engine.md` for how the comparison works and `docs/findings.md` for what it has
found so far.

An edition is a set of snapshots whose cleaned body text is identical. `editions.json` also
lists snapshots that were skipped and why (for example the 2022-23 Our Pasts II files, which
are rasterised and need OCR).

See `docs/text-format.md` for what the extracted Markdown looks like and why.

Downloads are skipped when the file already exists. The Wayback Machine is hit exactly once per
snapshot. Please keep it that way.

## Copyright and licence

The code in this repository (everything under `src/`, `scripts/`, `tests/`, and the site
templates and stylesheet) is released under the MIT licence, see `LICENSE`.

The textbooks are copyright NCERT. They are distributed free of charge by NCERT, and this
project exists to document how a public curriculum changes over time. The extracted text in
`texts/`, the comparisons in `diffs/`, and the page images on the site reproduce NCERT's
work for that purpose and are not covered by the MIT licence. The PDFs themselves are not
redistributed from this repository.
