# ncert-textbook-git-diff

Tracks what changes between editions of NCERT (India) history textbooks, so that additions,
deletions, and rewordings over the years can be seen side by side with the original pages.

Current scope: Class 7 "Our Pasts II" (2007 to 2025), its 2025 successor "Exploring Society:
India and Beyond", and Class 8 "Our Pasts III". English editions only for now.

## What is here

- `sources.yaml` lists every PDF the project uses: Wayback Machine snapshots (one per known
  distinct edition) and the live files on ncert.nic.in. This is the only place archive URLs live.
- `pdfs/` (not in git) holds the downloaded books, one folder per snapshot, with readable names.
- `manifest/` records what was downloaded (URL, timestamp, sha256, size) and how snapshots
  group into editions.
- `texts/` holds the extracted and cleaned Markdown, one file per chapter per edition, with
  page markers so text can later be shown beside the page image.
- `docs/sources.md` has the research behind all of this: book codes, URL eras, archive coverage,
  the 1967 to 2025 lineage, and NCERT's own list of what was cut in 2022-23.

## Running it

Needs [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run ncert-diff fetch            # download everything in sources.yaml, once
uv run ncert-diff fetch our-pasts-2
uv run ncert-diff status           # what is on disk
uv run ncert-diff extract          # PDFs -> texts/ and manifest/<book>/editions.json
uv run ncert-diff editions         # which snapshots collapsed into which edition
uv run pytest
```

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
