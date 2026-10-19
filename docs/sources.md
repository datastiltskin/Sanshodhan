# Where the textbooks come from

Research notes from October 2026. Everything here was checked against live responses from
ncert.nic.in and the Wayback Machine's CDX index at the time.

## NCERT file naming

NCERT serves each textbook as chapter PDFs plus a prelims PDF and a whole-book zip:

- `<code><NN>.pdf` is chapter NN (two digits)
- `<code>ps.pdf` is the prelims (title pages, foreword, contents)
- `<code>dd.zip` is the whole book
- `<code>cc.jpg` is the cover

The code is five or six letters: a class letter (f = 6, g = 7, h = 8, i = 9, j = 10, k = 11,
l = 12), a language or medium letter (e = English, h = Hindi, u = Urdu), a subject pair
(ss = social science, es = the new integrated social science books), and a book number.
The book number is not stable across subjects, so always confirm the title from the prelims.

| Book | Code | Status |
|---|---|---|
| Class 7 Our Pasts II (history, English) | `gess1` | Still served. Reprint 2024-25. |
| Class 7 Our Environment (geography) | `gess2` | Easy to confuse with the above. |
| Class 7 Social and Political Life II | `gess3` | |
| Class 7 Hamare Ateet II (Hindi history) | `ghss1` | Later. |
| Class 7 Exploring Society: India and Beyond, Part 1 | `gees1` | First edition April 2025. |
| Class 7 Exploring Society: India and Beyond, Part 2 | `gees2` | First edition November 2025. |
| Class 8 Our Pasts III (history) | `hess2` | Single volume. Older captures split the book into `hess1` (Part 1, chapters 1 to 6) and `hess2` (Part 2). `hess1` is now a 404. |
| Class 6 Exploring Society | `fees1` | Later. |
| Class 8 Exploring Society Parts 1 and 2 | `hees1`, `hees2` | Later. |

## URL eras on ncert.nic.in

| Years | Chapter PDFs | Listing page |
|---|---|---|
| 2007 to 2013 | `ncert.nic.in/NCERTS/l/<code>NN.pdf` (assumed, not captured) | `NCERTS/textbook/textbook.htm?<code>=0-10` |
| 2014 to 2018 | `ncert.nic.in/ncerts/l/<code>NN.pdf` | `ncerts/textbook/textbook.htm?<code>=0-10` |
| 2018 to now | `ncert.nic.in/textbook/pdf/<code>NN.pdf` | `textbook.php?<code>=0-10` |

## Wayback Machine coverage

The archive has no chapter PDF captures for Our Pasts II before 2014. The 2010 capture of the
listing page exists, but its PDF links were never saved. The 2014 whole-book zip contains PDFs
whose creation dates are 30 March and 18 April 2007, so it is the first edition text.

Whole-book zips with distinct content (these are what `sources.yaml` lists):

| Book | Capture | Notes |
|---|---|---|
| Our Pasts II | 2014-07-28 | 2007 files, 10 chapters |
| Our Pasts II | 2016-09-10 | |
| Our Pasts II | 2019-03-12, 2019-05-04 | two different zips two months apart |
| Our Pasts II | 2020-06-16 | |
| Our Pasts II | 2021-08-13 | |
| Our Pasts II | 2022-08-04 | |
| Our Pasts II | 2023-12-23 | Rationalised 2023-24, 8 chapters |
| Our Pasts II | 2024-05-24 | identical bytes in 2025 and 2026 captures |
| Our Pasts III | 2014-07-28, 2016-09-10, 2019-03-12, 2020-10-15, 2021-08-14, 2022-08-02, 2023-12-23, 2024-08-04 | |
| Social and Political Life III | 2014-07-28, 2016-09-10, 2019-05-04, 2020-06-16, 2021-08-14, 2022-08-02, 2023-02-10 (truncated), 2023-12-23, 2024-05-24 | 2020-06-16 and 2020-10-11 share a digest |
| Social and Political Life II | 2014-07-28, 2016-09-10, 2019-05-04, 2020-05-08, 2022-08-02, 2023-12-23, 2024-05-24 | no 2021 zip; three captures on 2022-08-02, two of them cut short; 2024-05-24 identical through 2026 |

What the downloaded zips turned out to contain:

- Our Pasts II 2019-03-12: NCERT's own packaging error, faithfully archived (the file sizes
  match the archive's records, so this is not a bad download). The zip holds no chapter
  files. Its `gess1dd.pdf` is itself a zip with the wrong extension, containing two cover
  images, the 2018-19 prelims (`gess1ps.pdf`, reused as `2018-partial/prelims.pdf`), and the
  whole Social and Political Life II civics book misnamed `gess301.pdf`.
- Our Pasts II 2017-partial and 2018-partial: the only per-chapter captures between the 2016
  and 2019 zips (three on the old path from 2017-18, four on the new path from 2018). Their
  text is identical, chapter for chapter, to the 2013-reprint edition and the 2019 edition
  respectively, so no printing is missing from the lineage: the "January 2019" edition is the
  text NCERT introduced with the December 2017 reprint.
- Our Pasts II 2022-08-04: the chapter PDFs are rasterised at 292 dpi. The only text in them
  is the "2022-23" footer. This printing (November 2021) is read with tesseract and kept as
  its own edition with an `-ocr` suffix. Word confidence is around 92 percent. A sentence-level
  fuzzy comparison against the 2019 edition found no changed sentences: every difference is
  an OCR split, a heading, or a fill-in-the-blank line. Chapter 10, the one file with a text
  layer, is byte-for-byte the 2019 text.
- Our Pasts III 2014 to 2019: two zips per year, `hess1dd.zip` (Part 1, chapters 1 to 6) and
  `hess2dd.zip` (Part 2, chapters 7 to 12, numbered 01 to 06 inside the files). From 2020 the
  book is one volume under `hess2`, with 10 chapters, then 8 after rationalisation.
- Our Pasts III 2019-03-12: the headings are set in fonts without a Unicode mapping and come
  out blank, so titles for that edition are taken from the contents page.
- Social and Political Life III 2023-02-10: the archive's copy of the zip stops at 11.9 MB
  of 24 MB (its recorded length, so a re-download gives the same bytes). Chapters 1 to 4
  were recovered from it with `scripts/salvage_truncated_zip.py`, and chapters 6, 7, 8 and
  10 from per-chapter captures of the same months. All eight are identical to the files in
  the 2022-08-02 zip, which already carry the "2022-23" session footer in every chapter
  (including 5 and 9). So the 2022-23 printing is complete in the 2022-08-02 snapshot, and
  the February 2023 zip was the same files re-served. The partial snapshot is kept as
  evidence and folded into that edition.
- Social and Political Life III 2022-08-02: the body font maps every character to the
  Unicode private-use range (U+F048 for "H"), as symbol fonts do. The extractor translates
  it back, so the text reads normally.
- Social and Political Life III, all editions: odd-numbered chapter files open with a unit
  title page and a Teacher's Note, and in 2016 and 2019 the first chapter file also carries
  the contents page. Chapter titles sit beside a "Chapter N" label rather than a numeral.
- Social and Political Life II 2014-07-28: the 2007 first-edition files (ten chapters, plus a
  one-page `gess3rf.pdf` of references). The 2016-09-10 zip has the same files except
  chapters 2, 3 and 10, which were re-set in January 2015, and chapter 10 grew a references
  page. The rungtaias.org copies are byte-for-byte the 2016 zip's files.
- Social and Political Life II 2019-05-04: nine chapters. "Understanding Advertising"
  (chapter 7) was dropped for the 2019-20 session and the later chapters renumbered. The
  first chapter file carries the contents page.
- Social and Political Life II 2022-08-02: the archive took the zip three times that day
  (07:47, 18:10 and 18:11 UTC) with three digests. The first two are truncated prefixes of
  the third (checked with `cmp`), so only the complete capture is listed. Its chapter files
  are rasterised page images with no text layer at all, like the 2022-23 Our Pasts II files,
  and are read with tesseract (word confidence 80 to 95 percent per chapter).
- Social and Political Life II 2023-12-23: `ch07.pdf` holds the Unit Five opener and chapter
  7, and `ch08.pdf` holds chapter 7 again followed by chapter 8 and the references. The
  extractor splits the second file and keeps the first copy of chapter 7.
- Social and Political Life II 2024-05-24: a re-export with generic `CIDFont+F1` font names
  whose Unicode maps put the typographic quotes and dashes on Latin-1 and Latin Extended-A
  code points (apostrophes become middle dots, "RamabaiĬs"). Three pages (the chapter 1 opener, page 14, and the
  road-safety poster at the back) are flat images and are OCR'd. Each unit opener and
  teacher's note sits at the end of the previous chapter's file rather than the start of its
  own; the extractor moves those pages to the chapter they introduce.

Per-chapter captures also exist for years without a zip (2017, 2018, 2025). Many of those are
re-encodes of the same text with very different file sizes, so a different file hash does not
mean different content. Editions are deduplicated by the hash of the cleaned text.

Access notes: plain HTTP clients work for both ncert.nic.in (send a browser User-Agent) and
web.archive.org. There is no bot blocking. The archive is intermittently down (504, or a
"Temporarily Offline" HTML page served with status 200), so retries with backoff are needed
and the fetcher checks that a download is actually a zip or PDF.

## Ground truth for the 2022-23 cuts

NCERT published per-class booklets listing every dropped page:
`https://ncert.nic.in/pdf/BookletClass7.pdf` and `BookletClass8.pdf`
(index at `https://ncert.nic.in/rationalised-content.php`).

For Our Pasts II (book number 0760):

| Chapter | Pages | Dropped |
|---|---|---|
| 2 New Kings and Kingdoms | 28 | "Elsewhere" box |
| 2 | 34 to 36 | full pages |
| 3 The Delhi Sultans | 41 | full page |
| 3 | 43 | "Elsewhere" box |
| 3 | 44 | question 8 |
| 4 The Mughal Empire | 48 to 49 | full pages (table of emperors' campaigns) |
| 4 | 57 | "Elsewhere" box |
| 5 Rulers and Buildings | 60 to 74 | full chapter |
| 6 Towns, Traders and Craftspersons | 75 to 90 | full chapter |
| 7 Tribes, Nomads and Settled Communities | 101 | "Elsewhere" box |
| 8 Devotional Paths to the Divine | 119 | "Elsewhere" box |
| 9 The Making of Regional Cultures | 135 | "Elsewhere" box |
| 10 Eighteenth-Century Political Formations | 152 | "Elsewhere" box |
| 10 | 153, 154 | questions 1, 2, 4, 5, 8, 11 |

Chapter 3 was retitled "Delhi: 12th to 15th Century" and chapter 4 "The Mughals (16th to 17th
Century)" in the rationalised edition.

For Social and Political Life II (book number 0764), the booklet lists:

| Chapter | Pages | Dropped |
|---|---|---|
| Introductory note for teachers | vii to xiii | the last three lines of page viii, the third point on page ix, the question on Omprakash Valmiki on page xi |
| 1 On Equality | 3 to 15 | on the teacher's-note page the second paragraph, the third paragraph, "Both" to "This" in the fourth, and the first sentence of the fifth; pages 4 to 8 in full; the first three paragraphs and the first sentence of the second column on page 9; "like Omprakash Valmiki" on page 11; question 3 on page 15 |
| 2 Role of the Government in Health (the booklet calls it "How the State Government works") | 21, 24, 25 | the box "The Story of Hakim Sheikh" and the activity after it; the last line of the second paragraph on page 24; the sentence beginning "Hakim ... hospitals" on page 25 |
| 8 A Shirt in the Market | 100 | the last sentence |
| 9 Struggles for Equality | 102 to 109 | the whole chapter |

The rationalised 2023-24 files match this list: chapter 1 shrank from 14 pages to 8, the
Hakim Seikh story is gone from chapter 2, and chapter 9 is absent.

## Lineage of the Class 7 history book

From NCERT's Library and Documentation Division catalogue
(`https://ncert.nic.in/ncertldd/collection/pdf/Textbooks.pdf`):

| Year | Title | Digital copy |
|---|---|---|
| 1967 | Medieval India: a textbook of history for middle schools (Romila Thapar) | |
| 1988 | Medieval India: history textbook for class VII (Thapar) | archive.org `dli.ernet.4041` (English, OCRed scan). Hindi: `dli.ernet.287038`, `in.ernet.dli.2015.447637` |
| 2003 | India and the World: a social science textbook for class VII | none found |
| 2004 | Social Science Part I: Medieval India: textbook in history for class VII | none found |
| 2007 | Our Pasts II | this project |
| 2025 | Exploring Society: India and Beyond, Parts 1 and 2 | this project |

The 2003 and 2004 books (the NCF-2000 era) exist only as physical copies in NCERT's textbook
archive as far as we can tell. Getting them means a scan or a request to the library
(dldi.ncert@gmail.com per the catalogue).

Class 8 for reference: 1980 History and Civics, 1989 Modern India, 2004 India and the World,
2008 Our Pasts III, 2025 Exploring Society Parts 1 and 2.

## Other places that hold copies

- archive.org has user uploads named after NCERT codes (`ncert-gess2`, `ncert-ghss1`, and so on)
  and the Digital Library of India scans listed above. Useful as a cross-check, not a primary
  source, since upload dates are missing.
- ePathshala (epathshala.nic.in) mirrors the current books as flipbooks. Not used.
- rungtaias.org/free-resources serves copies of NCERT's chapter files for classes 6 to 12.
  The first-page footer of most of its chapters reads "2015-16"; a few chapters carry no
  footer and cannot be dated from the site. Its Our Pasts II and Social and Political Life
  III files are identical to the December 2014 printing already held from the Wayback
  Machine, and its Social and Political Life II files to the January 2015 re-set of that book
  held in the 2016 zip. All are recorded as `rungtaias-2015-16` snapshots. It has no Class 8
  history book. Checked October 2026.
