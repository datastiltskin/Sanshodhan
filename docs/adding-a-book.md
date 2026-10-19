# Adding a book

The steps that took Our Pasts II and III from "somewhere on the internet" to pages on the
site, with the traps met on the way. Follow them in order for each new book.

## 1. Find the code and the editions

- Open `https://ncert.nic.in/textbook.php` and find the book in the class and subject
  menus. The option's value gives the code, for example `textbook.php?hess2=0-10` means
  code `hess2` with chapters 1 to 10. Codes are not stable across subjects, so always
  confirm the title from the prelims PDF (`<code>ps.pdf`) rather than trusting the number.
- Ask the Wayback Machine's index for the whole-book zip on each URL path the site has used:

  ```sh
  for p in ncerts/l textbook/pdf; do
    curl -s "http://web.archive.org/cdx/search/cdx?url=ncert.nic.in/$p/<code>dd.zip&fl=timestamp,statuscode,digest,length&collapse=digest"
  done
  ```

  One row per distinct file. Expect roughly: 2014 and 2016 on `ncerts/l`, then 2019 onwards
  on `textbook/pdf`. Only query per file, never with wildcards, and do not repeat queries.
- If a book was printed in parts (Our Pasts III until 2019 was `hess1` and `hess2`), each
  part has its own code and zips. If a year has no zip, per-chapter captures may exist
  (`<code>01.pdf` and so on); fetch them as a `-partial` snapshot and the pipeline folds
  them into whichever full edition they match.
- A copy of a chapter file found elsewhere can be added as a snapshot with plain URLs and no
  `wayback` key, but only once the first-page session footer has dated it. A file without a
  footer is not evidence of any particular printing.
- Record the lineage from NCERT's library catalogue
  (`https://ncert.nic.in/ncertldd/collection/pdf/Textbooks.pdf`) in `docs/sources.md`, so
  the pre-2007 books are known even when no digital copy exists.

## 2. Describe it in sources.yaml

One entry per book with class, subject, title, code (or `parts` with a code each and
`first_chapter` for a part whose files restart at 01), and one snapshot line per distinct
zip: label (capture date), Wayback timestamp, original URL. Add a `live` snapshot for the
current file on ncert.nic.in. Comments in the file explain anything odd.

## 3. Fetch

```sh
uv run ncert-diff fetch <book-id>
```

Downloads each snapshot once into `pdfs/<book>/<label>/` with curl (the archive answered
429 to other clients), waits 15 seconds between requests, retries slowly, and unzips to
readable names (`ch04.pdf`, `prelims.pdf`, `part2-ch01.pdf`). Run it in the foreground. It
writes `manifest/<book>/files.json` with URLs, timestamps and sha256 for every file.

Then look at what arrived: `uv run ncert-diff status`, and the first lines of each prelims.
Things seen so far:

- A zip that is not chapters at all (the 2019-03 Our Pasts II zip held a civics book and a
  zip misnamed `.pdf`). Nothing to do but note it in `docs/sources.md`.
- Rasterised printings with no text layer (2022-23 Our Pasts II). The pipeline OCRs them if
  tesseract is installed. The edition gets an `-ocr` suffix and a caveat on the site.
- Files whose italic terms are drawn as outlines (2024-25 Our Pasts II). Recovered with
  OCR of the small rectangles automatically. Spot check a page.
- Fonts with no Unicode map (2018 Our Pasts III). Their text is marked `[unreadable]`.
- Fonts that map letters into the private-use range U+F0xx (2022 Social and Political Life
  III). Decoded automatically; if a new file shows `[unreadable]` or empty chapters, check
  the span text in PyMuPDF for `\uf0..` characters.
- A zip the archive cut short (2023-02 Social and Political Life III). Run
  `uv run python scripts/salvage_truncated_zip.py <zip>` to pull out the complete members,
  rename them to `chNN.pdf`, give the snapshot a `-partial` label in `sources.yaml`, and look
  for per-chapter captures of the same months to fill the gaps.
- Books whose chapters open with a unit page and a "Chapter N" label beside the title
  (the civics books). Handled: the label gives the number, the title is the heading beside
  it, unit pages and teacher's notes are kept, a bound-in contents page is dropped.
- The same capture listed several times on one day with different digests (2022-08-02
  Social and Political Life II). Compare the files with `cmp`: two of the three were
  truncated prefixes of the third, so only the complete one is listed.
- A chapter file that holds two chapters (the 2023-24 Social and Political Life II `ch08.pdf`
  carries chapters 7 and 8, and chapter 7 again in `ch07.pdf`). Split automatically at the
  chapter openers when their numbers differ, and the first copy of a chapter wins. The
  editions log says "holds 2 chapters, split".
- A file that ends with the next unit's opener and teacher's note instead of starting with
  it (2024-25 Social and Political Life II). Those pages are carried over to the front of
  the next chapter automatically, and the log says "opens with 2 pages carried over".
- A few rasterised pages inside a file that otherwise has a text layer (three pages in the
  2024-25 Social and Political Life II files). They are OCR'd one page at a time and listed
  as `ocr_pages` in the front matter. Expect some reading errors on those pages.
- Fonts whose quotes come out as "women·s" or "RamabaiĬs" (the 2024-25 Social and Political
  Life II files, re-exported with generic `CIDFont+F*` names). Repaired automatically when a
  file shows the pattern. If a new file shows middle dots or Latin Extended letters where
  apostrophes belong, extend `QUOTE_SHIFT` in `extract.py`.

## 4. Extract and check

```sh
uv run ncert-diff extract <book-id>
uv run ncert-diff editions <book-id>
```

Extraction writes `texts/<book>/<edition>/` and `manifest/<book>/editions.json`. The
editions listing shows which snapshots collapsed into one text and the chapter titles and
page ranges per edition. Check that:

- chapter numbers and titles are right (titles come from the opening page, or from the
  contents page, or are borrowed from a neighbouring edition);
- printed page ranges run continuously (a wrong footer rule shows up as odd ranges);
- no chapter opens with a lower-case word (a lost drop cap);
- the rationalised edition matches NCERT's booklet for that class
  (`https://ncert.nic.in/pdf/BookletClass<N>.pdf`).

If a new book's layout breaks a rule, the knobs are in `extract.py`: the footer band, the
body-size profile (the largest prose size carrying a quarter of the text), the side fonts,
the chapter-number and chapter-label detection, and the heading length limit (some fonts
report every weight as bold, so a long "bold" block is prose, not a heading). Add a fixture page to
`tests/fixtures/` and a test before changing them.

## 5. Diff

```sh
uv run ncert-diff diff <book-id>
```

Writes `diffs/<book>/<from>__<to>.json` and `.html` for consecutive editions. Read the HTML
for each pair once. Noise you can expect and how it is handled is in `docs/diff-engine.md`.
Add what you learn to `docs/findings.md`, with page numbers.

## 6. Page images

```sh
uv run ncert-diff render-pages <book-id>
scripts/upload-images.sh            # when the R2 bucket exists
```

One WebP per printed page under `site/images/<book>/<edition>/<chapter>/pNNN.webp`, about
120 KB each. Only pages that belong to the chapter text are rendered (a 2007 file that opens
with the previous chapter's last page skips it). The upload script copies new files only.

## 7. Build and look

```sh
uv run ncert-diff build
python3 -m http.server 8765 -d site
```

Open the book's timeline, one chapter in the newest edition with changes on, and the
"every change" page, at desktop and phone widths. Then commit `sources.yaml`, `manifest/`,
`texts/`, `diffs/`, and the docs. `pdfs/` and `site/` stay out of git.
