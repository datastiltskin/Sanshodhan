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
whose creation dates are 30 March and 18 April 2007, so it is the first edition text. Those
files are not complete pages: in chapter 5 (pages 62 to 72 at least) the outer margin is cut
off at the page edge, so the figures and captions set there are missing from the image and
only their last letters reach the text layer. The extractor drops those slivers. A caption
that the compare view shows in a later printing and not in the 2007 one on those pages is a
defect of the 2007 file, not of the extraction, and cannot be recovered from it.

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
| Our Pasts I (fess1) | 2014-06-28, 2015-04-02, 2019-03-12, 2019-05-04, 2020-06-16, 2023-12-23 | added 2026-10-20; the live site no longer serves the Class 6 books |
| Social and Political Life I (fess3) | 2014-06-28, 2015-04-01, 2019-05-04, 2020-06-16, 2022-10-13, 2023-12-23 | added 2026-10-20 |
| India and the Contemporary World I (iess3) | 2014-07-28, 2016-09-10, 2019-03-12, 2021-08-15, 2022-08-02, 2023-12-23, 2024-08-04, 2025-04-27 | added 2026-10-20; code to be confirmed from the prelims |
| India and the Contemporary World II (jess3) | 2011-10-17, 2014-09-07, 2019-03-12, 2019-05-04, 2020-05-17, 2022-08-24, 2023-12-23, 2025-02-12, 2025-04-22, 2026-05-08 | added 2026-10-20; the 2011 zip is the earliest in the project |
| Democratic Politics I (iess4) | 2014-07-28, 2016-09-11, 2019-05-04, 2020-06-16, 2021-08-14, 2022-09-09, 2023-12-23, 2024-05-24, 2025-04-27 | added 2026-10-20 |
| Democratic Politics II (jess4) | 2011-10-17, 2013-02-19, 2014-09-07, 2015-04-01, 2019-05-04, 2020-05-17, 2022-08-03, 2023-02-28, 2023-12-23, 2024-05-24, 2025-04-26, 2026-05-08 | added 2026-10-20 |

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
  one-page `gess3rf.pdf` of references, which the extractor appends to chapter 10 because
  the later printings bind that page into the chapter). The 2016-09-10 zip has the same
  files except chapters 2, 3 and 10, which were re-set in January 2015: chapter 10 grew the
  references page, and the re-set chapter 2 file lacks printed pages 16 and 17 (the Unit Two
  opener and teacher's note), a gap in the source, not a change in the book. The
  rungtaias.org copies are byte-for-byte the 2016 zip's files.
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

Oddities in the new books' zips, as of 20 October 2026:

- The 2022-10-13 Social and Political Life I zip is cut short inside chapter 7. Chapters 1
  to 6 were salvaged, and chapter 9 and the prelims came from per-chapter captures of the
  same 2022-23 printing (their footers agree), so the snapshot is `2022-10-13-partial` with
  seven of nine chapters. Chapter 7's only capture is a 1 MiB stump and chapter 8's transfer
  breaks off before its end, so those two are still missing.
- The 2023-02-28 Democratic Politics II zip is cut inside chapter 4: chapters 1 to 3
  salvaged, snapshot `2023-02-28-partial`.
- The 2025-04-27 India and the Contemporary World I zip packs the book's own prelims under
  the geography book's file name (`iess1ps.pdf`, "Reprint 2025-26"); the 2025-04-21 capture
  of `iess3ps.pdf` is byte-identical and is listed so the snapshot has a `prelims.pdf`.
- The 2025-02-12 India and the Contemporary World II zip has the five chapters and no
  prelims, and no 2024-25 prelims survives anywhere: the one capture of that session is a
  stump whose original length equals the 2023-24 prelims. Nothing was added rather than
  misdate it.
- NCERT's zips carry slips of naming that the fetcher maps to the right chapter: the 2020
  Our Pasts I zip (and the archive.org upload of the same printing) names chapters 10 and
  11 `fess1010.pdf` and `fess1011.pdf` and chapter 1 `fees101.pdf`; the 2023 Democratic
  Politics II zip has `jess4 ps.pdf` with a space; the 2025 India and the Contemporary
  World I zip has its prelims as `iess1ps.pdf`. A member the fetcher does not recognise is
  kept under its own name and ignored by the extractor, so an edition with fewer chapters
  than its zip has files is the sign to look for.
- The live site answers 404 for the Class 6 books, the Class 9 history book and Democratic
  Politics I, under every path and name tried, so their `live` entries fetch nothing. The
  Class 10 books are still served (files dated 27 March 2026).

Captures of single chapter files are often cut at exactly 1 MiB (sometimes 5 MiB) by the
archive's crawler. Before listing one, check its length against the other captures of the
same file, or ask for a byte range and read the total size the archive reports. The index's
digest is the base32 SHA-1 of the file, so a capture can be compared with files already on
disk without downloading it: of 105 gap-year candidates for the six new books, 66 were
byte-identical to held files and 39 were new. The gap-year partial snapshots added this way
(one label per year, `<year>-partial`, or `<year>-ncerts-partial` when both URL paths have
captures that year) are: Our Pasts I 2016 to 2018, 2021, 2022, 2024; Social and Political
Life I 2016 to 2018, 2021, 2024; India and the Contemporary World I 2017, 2018, 2020; India
and the Contemporary World II 2013, 2015, 2016, 2018, 2021, 2024; Democratic Politics I 2012,
2017; Democratic Politics II 2016 to 2018, 2021; Our Pasts II 2015, 2025, 2026; Our Pasts III
2015, 2017, 2018, 2025, 2026; Social and Political Life III 2015, 2017, 2018; Social and
Political Life II 2017, 2018, 2021, 2025, 2026.

## Cover images

NCERT serves a cover image for each book at `textbook/pdf/<code>cc.jpg` (and did at
`ncerts/l/<code>cc.jpg` before 2018). `sources.yaml` lists one archived capture per era and
the live file under `covers:`, and the fetcher stores them in `pdfs/<book>/covers/`. The
2019 and later prelims open with a title page that reproduces the cover art, so those
editions are shown with that page rendered. Older editions, whose prelims open with the
contents, are shown with the archived cover nearest in date. The zips themselves hold no
cover files, except the mis-packaged 2019-03 Our Pasts II zip, which carries `gess1cs.pdf`
and `gess2cs.pdf`, cover sheets for two books.

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

## The Azim Premji University School Books Archive

schoolbooksarchive.azimpremjiuniversity.edu.in holds scans of Indian school textbooks from
the 1860s on, NCERT's among them (1,323 items under NCERT as publisher, checked 20 October
2026). Every file looked at is a 2021 flatbed scan (ScanSnap SV600) with an invisible OCR
text layer, split into parts of about 10 MB. The scans are clean and sharp, the OCR layer
reads body text well and headings and contents pages badly. There are no born-digital PDFs,
so for text the archive is another OCR source, and its value to this project is different:
it has the first editions of the NCF-2005 books (2006 to 2008), one printing of each, and
the whole pre-2005 lineage that the library catalogue lists and that no other site has,
including the 2002 and 2003 "India and the World" books. Later printings of one title are
not there.

The site is DSpace 6.2 behind a scripted front end. Its item pages load by script, its
REST and OAI endpoints are off, and its browse and search paging drop and repeat items. What
answers reliably, with a browser-like User-Agent: `GET /dspace-mvc/getItemSearch` with the
publisher filter (`filtername=publisher`, `filtertype=contains`, `filterquery=National
Council of Educational Research`) and one class at a time (`filter_field_1=educationlevelclass`,
`filter_type_1=equals`, `filter_value_1=Class 9`), which fits on one page of `rpp=500`;
`GET /dspace-mvc/getMetaDataValues?itemID=<uuid>&configProp=metadata.ItemDisplay` for
publisher, year and edition; `GET /dspace-mvc/getItemBitstream?handle=20.500.12497/<n>` for
the file ids; and `GET /dspace-mvc/retrieve?bitstreamID=<id>` for the PDF itself. Downloaded
parts live under `pdfs/_apu/<handle>/partN.pdf`, outside git.

NCERT history and civics items for classes 6 to 10 (class and year as the archive records them):

| Class | Year | Title | Files | Item |
|---|---|---|---|---|
| Class 6 | 1980 | History and civics : a textbook for class VI | 5 | [4282](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/4282) |
| Class 6 | 1987 | Our civic life : a textbook of civics for class VI | 1 | [11075](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/11075) |
| Class 6 | 1987 | Our civic life : a textbook of civics for class VI | 1 | [8177](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/8177) |
| Class 6 | 1990 | Ancient India : a textbook of history for class VI | 3 | [2300](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2300) |
| Class 6 | 1991 | Ancient India : a textbook of history for class VI | 1 | [10932](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/10932) |
| Class 6 | 2002 | India and the World : social sciences textbook for class VI | 5 | [2154](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2154) |
| Class 6 | 2003 | History in the new NCERT textbooks : fallacies in the IHC report | 1 | [6686](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/6686) |
| Class 6 | 2006 | Our pasts I : class VI | 4 | [5853](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/5853) |
| Class 6 | 2006 | Social science, social and political life part I : textbook for class VI | 3 | [1414](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1414) |
| Class 7 | 1988 | How we govern ourselves : a textbook of civics for class VII | 1 | [10992](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/10992) |
| Class 7 | 1988 | Medieval India : history textbook for class VII | 1 | [3164](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/3164) |
| Class 7 | 1989 | How we govern ourselves : a textbook of civics for class VII | 2 | [1263](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1263) |
| Class 7 | 2003 | India and the World : a social science textbook for class VII | 6 | [1991](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1991) |
| Class 7 | 2007 | Our pasts part II : textbook in history for class VII | 4 | [1415](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1415) |
| Class 7 | 2007 | Social science social and political life - II : textbook for class VII | 3 | [1418](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1418) |
| Class 8 | 1980 | History and civics : a textbook for class VIII | 1 | [10897](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/10897) |
| Class 8 | 1981 | History and civics : a textbook for class VIII | 9 | [1990](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1990) |
| Class 8 | 1989 | Modern India : a history of textbook for class VIII | 8 | [2236](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2236) |
| Class 8 | 1989 | Our country today : problems and challenges, a textbook in civics for class VIII | 2 | [8184](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/8184) |
| Class 8 | 1989 | Our country today : problems and challenges, a textbook in civics for class VIII | 1 | [11077](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/11077) |
| Class 8 | 2006 | Social science part II, India and the World : textbook for class VII | 5 | [1416](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1416) |
| Class 8 | 2008 | Our Pasts part I : class VIII | 3 | [5854](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/5854) |
| Class 8 | 2013 | Social and political life III : textbook for class VIII | 3 | [1395](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/1395) |
| Class 9 | 1988 | Medieval India : history textbook for class VII | 1 | [11008](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/11008) |
| Class 9 | 1990 | The story of civilization : volume 1, a history textbook for class IX | 3 | [11146](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/11146) |
| Class 9 | 1998 | India constitution and government : a textbook in civics for classes IX and X | 3 | [2290](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2290) |
| Class 9 | 2006 | Democratic politics : I, textbook in political science for class IX | 4 | [2244](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2244) |
| Class 9 | 2006 | Social science India and the contemporary World - I : textbook in history for class IX | 5 | [2245](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/2245) |
| Class 10 | 1989 | Our government : how it functions, a textbook in civics for class - X | 1 | [11078](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/11078) |
| Class 10 | 1989 | Our government : how it functions, a textbook in civics for class X | 2 | [8189](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/8189) |
| Class 10 | 1989 | The story of civilization part 1 : textbook in history for class X | 1 | [3171](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/3171) |
| Class 10 | 1989 | The story of civilization part volume two : history textbook for class X | 1 | [3172](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/3172) |
| Class 10 | 2002 | The story of civilization, history : textbook for class X, volume two | 1 | [9347](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/9347) |
| Class 10 | 2005 | Social science, part I : textbook in history for class X | 1 | [6614](https://schoolbooksarchive.azimpremjiuniversity.edu.in/handle/20.500.12497/6614) |

The first editions are whole-book scans, not chapter files, so wiring them into the
pipeline needs a split by chapter from the contents page and an OCR edition each. That is
deferred: the project's aim is the text-layer printings, and those are on the Wayback
Machine from 2011 (the Class 10 books) or 2014 (the rest) onwards. No copy at all has been
found, in English, of the 2007 first editions of India and the Contemporary World II and
Democratic Politics II (the archive has only their Hindi versions, items 12379 and 12380,
and archive.org and library catalogues list no file).

## Other places that hold copies

Checked again on 20 October 2026 for the ten history and civics books of classes 6 to 10.
Every copy found is listed in `sources.yaml` and downloaded, whatever its quality: the
pipeline groups snapshots by their text, so a duplicate costs nothing and a different
printing is a find. The rule for a copy from outside NCERT and the Wayback Machine is that
its label says what is known about its date, and no more.

- **archive.org, items `ncert-<code>`** (uploaded 26 and 27 June 2021 by one user, one item
  per book, chapter files plus prelims): every file's first-page footer reads 2020-21, so
  they are the 2020-21 session printing. Labelled `archive-org-2020-21`. Item `jess3dd`
  (March 2021) holds the whole-book zip of the August 2019 reprint of India and the
  Contemporary World II, labelled `archive-org-2019-reprint`. The `ncert-fess1` item lacks
  chapter 1 and 12 and carries a stray `fees101.pdf`, which is skipped. File lists come from
  `https://archive.org/metadata/<item>`; downloads from
  `https://archive.org/download/<item>/<file>`. The site is fast and sets no rate limit
  that a two-second pause does not respect.
- **rungtaias.org/free-resources** (an IAS coaching site): chapter files for classes 6 to
  12 under `public/uploads/NCERT TEXT BOOKS/Class N/<book folder>/<code>NN.pdf`. The Class 7
  and 8 files carry a 2015-16 footer and are labelled so. The Class 6, 9 and 10 files carry
  no footer, and are byte-identical to files NCERT served on `ncerts/l` between 2013 and
  2017, so they are copies of those printings. They are labelled `rungtaias-undated` and
  dated by the editions step from their prelims. One of them, Our Pasts I chapter 8, is cut
  short on the mirror itself after a complete first revision, which the fetcher keeps.
- **archive.org, item `OldNCERTBooks`** (February 2026): whole-book zips of nine of the ten
  books, every file byte-identical to a snapshot already held. Listed anyway as
  `archive-org-oldncert-<session>` snapshots, since a duplicate confirms a printing. Item
  `class910deletedhistorychapters` holds six chapters cut from the Class 9 and 10 history
  books, all identical to held files, and is not listed. An Arvind Gupta collection scan of
  Our Pasts III part 1 (January 2009 reprint) is kept at
  `pdfs/_archive-org/our-pasts-3-part1-2009-01-scan.pdf`, not wired in. Two scans sit in the
  archive's lending library and need a browser borrow:
  https://archive.org/details/ourpasts3part2te0000ncer (Our Pasts III part 2, dated 2016) and
  https://archive.org/details/bwb_W8-BHV-450 (Social and Political Life III, 2012).
- **selfstudys.com/books/ncert-old-book** lists chapter PDFs of a "2015-2016" set and of
  the 2019-20, 2020-21, 2021-22 and 2022-23 sessions, but hands out a download link only by
  e-mail after a sign-up, and the viewer renders pages without exposing the file. Not used.
- **iasexamportal.com** sells "old NCERT" kits (the pre-2005 books) without stating years.
  Not used.
- **The Azim Premji University School Books Archive** (section above): first editions and
  the pre-2005 lineage as scans with an OCR layer. Downloaded under `pdfs/_apu/`, not wired
  into the pipeline.

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
