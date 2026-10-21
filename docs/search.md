# Site search

The search page at `/search/` finds every chapter that carries a word or a phrase and
shows, for each, which editions of the book have it. This document is the whole design,
so that the feature can be changed without re-deriving it. The moving parts are small: a
hook in the site build, a few attributes in one template, one JSON file, one script, and
the Pagefind library.

## What a reader sees

- A search box in every page's navbar sends the query to `/search/?q=...`.
- The search page has the query box and five filters: class, subject, book, and (once a
  book is chosen) edition and chapter. The address bar follows the choices, so a search
  can be shared as a link, for example `/search/?q=secularism&subject=civics`.
- One result is one **chapter**, not one page of one edition. It shows the book and
  class, the chapter title (from the newest edition that has the chapter), an excerpt
  with the words marked, which edition and page the excerpt comes from, and a row of
  **chips**, one per edition of the book, in date order:
  - found (green): the phrase is in that edition's chapter. The chip opens the chapter at
    the page and marks the words.
  - chapter present, phrase not found (outlined): the chip opens the chapter.
  - chapter not in that edition (struck through): the chapter was dropped or had not
    been written yet.
- A result whose newest complete edition is not a hit, or whose chapter is absent from
  the latest complete edition, is tagged "only in older editions" with a red left border.
  That is the signal for text that was removed. Partial captures (a few chapters of one
  year) are left out of that judgement, since they say nothing about the rest of the book.
- Twenty chapters are shown at a time, "Show more chapters" loads the next twenty.

## How it works

### Indexing (build time)

`ncert-diff build` writes the site and then runs Pagefind over it
(`build_search_index` in `src/ncert_diff/site/build.py`). Pagefind is a static-site
search engine: it reads the HTML files, builds an index of every word with its position,
and writes it as many small files under `site/pagefind/`. The browser loads only the
chunks a query needs (a few hundred kilobytes), never the whole index (about 12 MB for
the 646 chapter pages, 2026-10-20). Pagefind ships as the Python package `pagefind[bin]`,
which bundles the binary for macOS and Linux, so `uv sync` is the only installation and
the GitHub Actions workflow needs no Node. `--no-search` skips the index for a quick
local build, and a missing package only logs a line.

What is indexed is decided by attributes in `templates/chapter.html`:

- `data-pagefind-body` on every page's `div.text`. Once any page on the site has this
  attribute, pages without it are left out, so book, edition, compare, and method pages
  are not indexed.
- `data-pagefind-ignore` on `<del>` (words removed since the previous edition, which the
  chapter page shows struck through) and on ghost headings, so removed text does not
  count as present in the edition that removed it. These are set in `sentence_html` and
  `block_html` in `build.py`.
- One hidden `<span>` per key inside the first page's `div.text` carries the filters and
  metadata (Pagefind takes one inline `key:value` per attribute):
  - filters, used to narrow a search: `book` (book id), `class` (6 to 10), `subject`
    (history, civics, social science), `edition` (edition id), `lineage`
    (`<book id>/<lineage id>`, the chapter filter).
  - metadata, returned with every hit: the same five, plus `book_title`, `edition_label`,
    `edition_short`, `chapter` (the chapter directory, `ch04` or `part2-ch03`), and
    `chapter_title`.
- The page's `<h1>` is the hit's title. Each page's `div.text` opens with an empty
  `<span id="tNN">` (NN the printed page), and Pagefind records every element with an id
  inside the indexed body as an **anchor** with its word position, which is how the script
  finds the printed page of a hit. The `section.page` ids (`pNN`, the targets of page
  links) sit outside the indexed body, so they are not anchors.

### Chapter lineage

A chapter keeps its identity across editions even when its number or title changes (the
2023 rationalised Our Pasts II drops two chapters and renumbers the rest, and retitles
"The Mughal Empire" as "The Mughals (16th to 17th Century)"). `chapter_lineages` in
`build.py` joins chapters that the diffs matched between consecutive editions (status
`matched` in `diffs/<book>/<from>__<to>.json`, plus `merged_from` and `merged_to`) into
one lineage with a union-find, and numbers the lineages `L01`, `L02`... in the order they
first appear. A chapter that no diff links to anything is a lineage of its own. The
lineage id goes into the page's filters and metadata, and into the catalogue.

### The catalogue

`site/search/catalogue.json` (written by `search_catalogue` in `build.py`) is what the
search page needs to draw a result without more requests: every book with its class and
subject, its editions in order with the chip name (`short`, from `short_label`: the year,
the month when two editions share a year, and a word for a rationalised, scanned,
partial, live, or undated edition), the full label, and the URL, and every lineage with
its title and the chapter directory it has in each edition. The script uses it to fill
the filters, to know which editions have a chapter (the difference between an outlined
chip and a struck one), and to build the links for chips that are not hits.

### The script

`static/search.js` (vanilla JS, no build step):

1. Loads the catalogue, fills the selects, reads the address, and runs the search.
2. Loads Pagefind on the first keystroke or focus (`import("/pagefind/pagefind.js")`),
   with `excerptLength: 30` and `highlightParam: "highlight"`, which makes every hit URL
   carry `?highlight=<query>`.
3. Runs `pagefind.search(query, {filters})` (debounced while typing). The result is a
   ranked list of chapter pages, one per edition, with a `data()` promise each.
4. Loads hit data in batches of forty, in rank order, and groups the hits by
   `meta.book + "/" + meta.lineage` until twenty chapters are on show. The first hit of a
   group (the best ranked) provides the excerpt. For every hit the printed page is the
   last `tNN` anchor whose position is at or before the first matching word (`pageOf`),
   and the chip links to `<hit url>#p<page>`.
5. Draws the chips from the catalogue's edition list and the group's hits.

On a chapter page, `static/viewer.js` sees the `highlight` parameter, loads Pagefind's
`pagefind-highlight.js`, and marks the words.

### Styling

The search rules sit at the end of `static/style.css` under "Search": the navbar box,
the filter bar, the result cards, the chips (`.chip.hit`, `.chip.miss`, `.chip.absent`),
and the `mark` colour, all on the existing colour tokens, light and dark.

## Changing it

- **Another filter or metadata key**: add a hidden span in `chapter.html`, read it from
  `d.meta` in `search.js`, and, for a filter, add it to `filters()` and the form. Values
  must be strings.
- **Index more or less of a page**: move the `data-pagefind-body` attribute or add
  `data-pagefind-ignore` to the elements to leave out (`data-pagefind-ignore="all"` also
  removes them from title and metadata detection). The role classes (`box-note`,
  `sec-exercises`) make it easy to exclude notes or exercises if that is ever wanted.
- **Ranking and excerpt length**: `pagefind.options` in `search.js` (Pagefind's
  `ranking` settings are documented at pagefind.app/docs/ranking).
- **Chip names**: `short_label` in `build.py`, with its test in `tests/test_site.py`.
- **A plain list instead of grouped results**: Pagefind's own Component UI
  (`pagefind-component-ui.js`, shipped in `site/pagefind/`) renders a classic result list
  from the same index with no script of ours. The grouping exists only because one result
  per chapter with edition chips answers "when did this disappear?" and a plain list does
  not.
- **Hosting under a subpath**: the build's `--base-url` (the `BASE_URL` repository
  variable in CI, `/<repository name>` by default) is put before every site URL by the
  templates (`{{ base }}`) and by the scripts, which read it from `<html data-base>`.
  The script passes it to Pagefind as `baseUrl`, so hit URLs carry it too.
- **Hindi editions**: Pagefind indexes any language. Set `force_language` per directory or
  drop it, and check the stemming (`pagefind.app/docs/multilingual`).

## Limits worth knowing

- Spelling must match the book's. "Orissa" and "Odisha" are different words to the
  index, and so are the stray spaces an OCR'd edition can leave inside a word.
- A hit is a chapter page, so a phrase that spans a page break in the text may be missed
  for that edition only.
- Exercises, glossary entries, captions, and notes are indexed like body text.
- A search for a word in a `<del>` (removed) span finds the edition that still had it,
  not the one that removed it. That is the intended reading of the chips.
- The index is rebuilt from scratch on every build (about a minute for the eleven books).

## Checks after a change

- `uv run pytest tests/test_site.py` covers lineage, chip names, and the catalogue.
- `uv run ncert-diff build` should log "search index: N pages" with N equal to the number
  of chapter pages (646 on 2026-10-20).
- `python3 -m http.server 8765 -d site`, then `/search/?q=Mughal+emperors` should show
  grouped results with chips, and a chip should open the chapter at the page with the
  words marked. Try the filters, a phone-width window, and a query with no hits.
