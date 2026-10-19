# ncert-textbook-git-diff

Tracks what changes between editions of NCERT (India) history textbooks, so that additions,
deletions, and rewordings over the years can be seen side by side with the original pages.

Current scope: history and civics for the middle classes. Class 7 "Our Pasts II" (2007 to
2025) and "Social and Political Life II", Class 8 "Our Pasts III" and "Social and Political
Life III", and the 2025 Class 7 successor "Exploring Society: India and Beyond". English
editions only for now.

## What is here

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
- `src/ncert_diff/site/` builds the website: Jinja templates, one stylesheet on top of Pico CSS,
  and a few lines of JavaScript for the change toggles. No framework, no build step beyond
  `ncert-diff build`.
- `docs/adding-a-book.md` is the step-by-step process for bringing in another book.
- `docs/sources.md` has the research behind all of this: book codes, URL eras, archive coverage,
  the 1967 to 2025 lineage, and NCERT's own list of what was cut in 2022-23.

## Running it

Needs [uv](https://docs.astral.sh/uv/), curl, and, for the rasterised 2022-23 printing,
[tesseract](https://github.com/tesseract-ocr/tesseract) with English data (`brew install tesseract`).

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
uv run pytest
```

To preview the site locally: `python3 -m http.server 8765 -d site` and open
http://127.0.0.1:8765/. In production the HTML is deployed to GitHub Pages by
`.github/workflows/site.yml` and the page images are uploaded to a Cloudflare R2 bucket by
`scripts/upload-images.sh`, with the bucket's public URL in the `IMAGES_BASE` repository
variable.

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

## Copyright

The textbooks are copyright NCERT. They are distributed free of charge by NCERT, and this
project exists to document how a public curriculum changes over time. Extracted text and diffs
are published here for that purpose. The PDFs themselves are not redistributed from this
repository.
