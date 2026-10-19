# Review of our-pasts-3 (Class 8 history, Our Pasts III)

Scope: the six consecutive pairs in `diffs/our-pasts-3/`. Page images were rendered from the source PDFs at 110 dpi. A page marked "not viewed" in an entry is one where the render could not be opened in this pass, so that verdict rests on the neighbouring page that was viewed and on the extracted text, and should be re-checked. The 2019-03-12 "[unreadable]" fonts were not logged, as agreed.

Printed page numbers are the numbers in the page markers of the Markdown. Chapter numbers are the chapter numbers of the edition named first in each heading.

Three things recur and are described once here so the entries can be short.

- Rule A, "caption glued to body". Figure captions that sit in a column beside the text, or a caption title followed by a second caption paragraph, are emitted as part of the surrounding paragraph or as a `table` block, so the sentence either swallows "Fig. N - ..." or is split around it. Seen in every pair.
- Rule B, "heading glued to body". Small run-in or italic headings are emitted as plain text at the start of the next paragraph (or the end of the previous caption) instead of as `###` headings. The edition that glues and the edition that does not change between pairs, which is what makes the diff report an edit.
- Rule C, "letter-spaced text". Justified lines in narrow boxes are set with very wide word spaces, and the extractor then writes the letters separately ("e d u c a t i o n w h i c h"), or the opposite (two words run together such as "openedup").

## our-pasts-3 2014-07-28 -> 2019-03-12

Note: the 2019 edition is the first printing with these fonts. The file `part1/part2` split means that chapter numbers 7 to 12 in 2014 and 2019 are the same chapters that are numbered 6 to 10 and later in 2020.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 1, printed page 1 (old) / 1 (new)
- Hunk: deleted/body " Activity", modified/body "... imperial perception." -> "... imperial perception. † Activity All such historical questions refer us back to notions of time."
- Images: 2019 page 7 (same box type, page 1 not viewed) shows the Activity box headed by an orange arrow icon, not a dagger. The 2019 text carries "†" where the icon is, and the 2014 text carries a leading space.
- Verdict: extraction fault (rule)
- Fix: strip the decorative Activity arrow glyph (seen as "†" in 2019, as "\x86" in 2020, as a leading space in 2014) before the word "Activity". Seen in ch1 p1 and p7, ch3 p28, p30, p36 (2019/2020), and in 2014 ch1 p1.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 1, printed page 6 (old) / 7 (new)
- Hunk: modified/body "They tell us what the officials thought, what they were interested in, and what they wished to preserve for posterity." -> "they were interested in, and what they wished to preserve for posterity." and modified/caption "Images need to be carefully studied..." -> "They tell us what the officials thought, what Images need to be carefully studied..."
- Images: 2019 page 7 starts the paragraph with "they were interested in, and what they wished to preserve for posterity.", directly under the Fig. 7 caption. The first half of the sentence is at the foot of the previous page. The words are identical in both printings.
- Verdict: extraction fault (rule)
- Fix: Rule A. A body sentence broken by a page turn must not be joined to a caption that sits between the two halves. The words "They tell us what the officials thought, what" belong to the 2019 body stream. Place seen once (ch1 p6/7).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 2, printed page 16 (old) / 16 (new)
- Hunk: modified/body "He also established a close Fig. 7 - Tipu Sultan relationship with the French..." -> "... Fig. 8 - Tipu Sultan relationship ..."
- Images: both pages show "Fig. 7 / Fig. 8 - Tipu Sultan" in the left column and the sentence "He also established a close" at the foot of the right column. In 2019 a new Fig. 6 (Sirajuddaulah) is added at the top of the previous page, so every later figure moves up by one.
- Verdict: extraction fault (rule)
- Fix: Rule A. The caption is swallowed by the sentence in both editions. The figure number change itself (7 to 8) is real.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 2, printed page 16 (old) / 16 (new)
- Hunk: modified/caption "Fig. 6 - Nawab Shujauddaulah ..." -> "Fig. 7 - ...", deleted/caption "Here, however, he poses in regal splendour, towering over the Resident.", modified/caption "The treaties ... authority." -> "... authority. Here, however, he poses ..."
- Images: both pages show the Nawab Shujauddaulah picture with one two-part caption (title then two sentences). Only the figure number differs (6 vs 7).
- Verdict: real change
- Fix: none. The figure renumbering is real. The moved sentence is engine noise (same caption, split differently). The pair of deleted/inserted hunks for the same sentence should be classed restreamed.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 3, printed page 34 (old) / 34 (new)
- Hunk: inserted/body "Gradually the indigo separated out in flakes ...", deleted/caption x4 (the Fig. 12 and Fig. 13 caption sentences), modified/caption "to the surface. The liquid was drained off...", inserted/table "The indigo worker here is standing with the paddle...".
- Images: the page is the same full-page "How was indigo produced?" layout in both editions. The sentence "Gradually the indigo separated out ... a clear liquid rose / to the surface." runs through the body column and across the picture wrap, and the Fig. 12 and Fig. 13 captions are in boxes at the foot. Wording is identical on both pages.
- Verdict: engine noise
- Fix: none. Text was reassigned between the body, caption and table streams. A rule in `diff.py` that matches a deleted or inserted sentence against the other streams of the same page would class all five as restreamed.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: deleted/body "W." and "S.", inserted/body "W.S."
- Images: 2020 page 36 (same layout, 2019 and 2014 page 36 not viewed) shows "W.S. Seton Karr" in the Activity box and in the Source 3 box. The initials are printed as one run.
- Verdict: engine noise
- Fix: the sentence splitter must not split after a single capital letter followed by a full stop ("W.", "S."). Seen again in 2019 -> 2020 ch3 p36.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 3, printed page 37 (old) / 37 (new)
- Hunk: modified/body "a peasant from Bihar persuaded him visit Champaran" -> "persuaded him to visit Champaran"
- Images: the 2014 page prints "persuaded him visit Champaran" (the word "to" is genuinely missing). The 2022 and 2023 pages print "persuaded him to visit".
- Verdict: real change
- Fix: none. A printing error was corrected in 2019.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 4, printed page 62 and 63 (new only)
- Hunk: inserted/heading "The Khurda Uprising - A Case Study" and about 50 inserted body sentences (pages 62 and 63), plus inserted body "In the Mandla region of Madhya Pradesh, Rani Avantibai Lodhi ..." (page 57) and "A similar fate awaited Rani Avantibai ..." (page 59)
- Images: 2019 page 62 shows a full-page purple source box titled "The Khurda Uprising - A Case Study" that is not in the 2014 book. The two suspect pages (62, 63) are this box, which the sentence matcher could not align because there is nothing to align to.
- Verdict: real change
- Fix: none. New content in 2019 (Khurda case study and Rani Avantibai). The "suspect" flag on those pages is correct for an inserted page and is not a fault.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 4, printed pages 55-56 (old) / 55-56 (new)
- Hunk: modified/body "Mutiny - When soldiers as a group disobey their officers in the army On 29 March 1857, a young soldier..." -> "On 29 March 1857, ..." and modified/body "Firangis - Foreigners ..." -> "Mutiny - ... Firangis - Foreigners ..."
- Images: 2020 page 55 (2019 not viewed) shows the "Mutiny" glossary box in the right margin of the "A Mutiny Becomes a Popular Rebellion" page, and the "Firangis" box beside page 56. The two glossary boxes are on different pages from the paragraphs they were glued to in 2014.
- Verdict: extraction fault (rule)
- Fix: Rule A for glossary boxes. Margin glossary boxes ("Term - definition") must be emitted as their own block and not prefixed to the nearest paragraph. Also seen in ch6 (pages 65-67, "Urbanisation", "Presidency", "Khanqah", "Idgah", "Dargah") and ch9 (pages 120-121 note boxes).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 4, printed pages 56-61 (old) / 56-61 (new)
- Hunk: modified/caption "Fig. 6 - The battle in the cavalry lines" -> "Fig. 4 - ...", "Fig. 5 -> Fig. 8", "Fig. 7 -> Fig. 11", "Fig. 4 -> Fig. 12", "Fig. 8/9 -> Fig. 14/15", "Fig. 10 -> Fig. 16", and inserted captions Fig. 5, 6, 7, 9, 10, 13
- Images: 2020 page 56 (the 2019 page was not viewed) shows Fig. 4 (battle in the cavalry lines), Fig. 5 (Mangal Pandey stamp). 2022 page 58 shows Fig. 9 (Nana Saheb), Fig. 10 (Vir Kunwar Singh), Fig. 11. The numbering in 2014 had only eight figures in this chapter.
- Verdict: real change
- Fix: none. Pictures were added (Mangal Pandey stamp, Bahadur Shah Zafar, Rani Laxmibai, Nana Saheb, Vir Kunwar Singh, Tantia Tope stamp), so the later numbers move. The garbled "Fig. 13 - Postal stamp Essued" is a one-off (see 2022 -> 2023).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 6, printed pages 65-68 (old) / 66-68 (new)
- Hunk: modified/body "Of these, the most Presidency - For administrative purposes ..." -> "Presidency - ...", modified/caption "You can see the Red Fort on the left." -> "Of these, the most You can see the Red Fort on the left.", inserted/body "important are the capital cities built between the twelfth and seventeenth centuries.", inserted/body "No wonder the poet Mir Taqi Mir said, "The Cul-de-sac - Street with a dead end"
- Images: 2019 page 67 starts with "important are the capital cities built between the twelfth and seventeenth centuries." under the Fig. 3 caption, and ends with "No wonder the poet Mir Taqi Mir said, "The" next to the glossary box that includes "Cul-de-sac - Street with a dead end". The sentence "Of these, the most / important are the capital cities ..." is split by the page turn, and the Fig. 3 caption sits between its halves.
- Verdict: extraction fault (rule)
- Fix: Rule A. A sentence broken at a page turn must be rejoined across the turn, skipping margin glossary boxes and captions. Seen at ch6 p66/67 ("Of these, the most" + "important are"), and p67/68 ("The" + "streets of Delhi aren't mere streets...").

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 6, printed pages 70-75 (old) / 71-75 (new)
- Hunk: modified/body "The government complex in New Delhi consisted of a two-mile avenue, Kingsway ..." split, "Activity Think of the life of two young people ..." moved, "Amir - A nobleman running in the front, and sometimes on three sides."
- Images: not viewed (2019 page 75 only was rendered, and it shows the Activity box and the glossary box "Amir - A nobleman" in the margin).
- Verdict: extraction fault (rule)
- Fix: Rule A, same pattern as above (margin box emitted into the paragraph that it sits beside, running text broken at a box).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 7, printed pages 102-104 (old) / 102-104 (new)
- Hunk: inserted/body "In a speech delivered on January 15, 1908 in Bombay, Aurobindo Ghose stated ..." (5 sentences), inserted/caption "Fig. 9 - Sri Aurobindo Ghose", Fig. 9 to Fig. 10, Fig. 10 to Fig. 11, Fig. 11 to Fig. 12
- Images: not viewed (page 102 of the 2019 chapter was rendered but not opened).
- Verdict: real change (provisional, from the text and the consistent figure renumbering by one)
- Fix: none. A new Sri Aurobindo Ghose passage and figure were added in 2019. Re-check with the 2019 page 102 image.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 8, printed page 116 (old) / 116 (new)
- Hunk: modified/body "Fig. 12 - Shri Narayana Guru Gulamgiri One of the most vocal amongst the "low-caste" leaders was Jyotirao Phule." -> "Fig. 12 - Shri Narayana Guru One of the most vocal ...", inserted/heading "Gulamgiri" (page 117)
- Images: 2019 page 116 and the 2020 page 102/103 show the same layout. The italic word "Gulamgiri" is the first line of the next page, above "One of the most vocal amongst the "low-caste" leaders was Jyotirao Phule." It is a small italic sub-heading, not part of the Fig. 12 caption.
- Verdict: extraction fault (rule)
- Fix: Rule B. The heading is emitted as a heading in 2019, glued to the previous caption in 2014 and again in 2020. The same fault toggles in the later pairs.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 8, printed pages 120-121 (old) / 120-121 (new)
- Hunk: modified/note "The Brahmo Samaj, formed in 1830 ..." -> "The Brahmo Samaj The Brahmo Samaj, formed ..." (and the same for Prarthana Samaj, Aligarh, Derozio, Singh Sabha, Ramakrishna Mission), deleted/note x6 (the six headings)
- Images: not viewed for these pages. The 2019 page 122 (the next) was viewed and shows normal exercises. The structure is the same as the Rule B headings above.
- Verdict: extraction fault (rule)
- Fix: Rule B for the small bold headings inside the "Reformers" note boxes. Six places, pages 120 and 121.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 8, printed page 122 (old) / 122 (new)
- Hunk: modified/exercises "10. Why were Jyotirao Phule and Ramaswamy Naicker ..." -> "10. Why were Jyoti rao Phule ...", "6. ... new opportunities opened up for people" -> "openedup for people", and the "1. What social ideas ..." name list becoming one inserted run.
- Images: the 2019 page 122 prints "Jyoti rao" (so the space is in the book), prints "opened up" with a very tight space (the text has "openedup", which is an extraction fault), and prints "in1829." as one run in item 2(d). The list of eight names is a single block on the page.
- Verdict: real change
- Fix: none for "Jyoti rao" (printed spacing error that NCERT introduced in 2019 and fixed in 2023). The fault in "openedup" is recorded in its own entry below.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 8, printed page 122
- Hunk: modified/exercises "opened up" -> "openedup"
- Images: 2019 page 122, question 6: the printed words are "opened up" with a tight space.
- Verdict: extraction fault (one-off)
- Fix: override for 2019-03-12, 2020-10-15, 2021-08-14 and 2022-08-02 (the faulty text carries into all four):
  - snapshot: "2019-03-12" (repeat for "2020-10-15", "2021-08-14", "2022-08-02"), chapter: 9 (2019) or 8 (the other three)
  - find: "what new opportunities openedup for people"
  - replace: "what new opportunities opened up for people"
  - note: "tightly justified line, the extractor lost the space (2019 page 122 and later). The image reads 'opened up'."

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 9, printed pages 126-130 (old) / 126-130 (new)
- Hunk: modified/body "1. In what ways are the Indians depicted as inferior?" -> "1.In what ways ...", "2. Notice" -> "2.Notice", "3. Do you think" -> "3.Do you think" (pages 126, 128, 130, about 8 items)
- Images: not viewed.
- Verdict: extraction fault (rule) (provisional, to be checked against the images)
- Fix: the numbered Activity items lose the space after the numeral in 2019 but not in 2014. A rule that restores "N. " after a leading numeral in the activity boxes would remove about eight hunks.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 9, printed pages 133-136 (old) / 133-136 (new)
- Hunk: modified/body "The characteristic elements This painting is a typical example ..." -> "The characteristic elements Fig. 14 - Englishman on an elephant hunting a tiger, Kalighat painting ... This painting ...", deleted/caption Fig. 13, 14, 15, 22, and the Fig. 22 caption glued before "The railway station was built between 1878 and 1887."
- Images: not viewed.
- Verdict: extraction fault (rule) (provisional)
- Fix: Rule A. Figure titles are merged into the paragraph they are next to in 2019.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 10, printed page 141 (old) / 141 (new)
- Hunk: deleted/body "The British conquest of territories, and takeover of kingdoms Introduction of new laws ..." -> inserted/body "¢ The British conquest of territories, and takeover of kingdoms" (nine lines, each starting "¢")
- Images: 2019 page 141 shows nine square bullets (a filled black square) before each item in the "In the previous chapters we have looked at:" list.
- Verdict: extraction fault (rule)
- Fix: the square bullet is extracted as "¢" in 2019, and is dropped in 2014 (so the list collapses into one sentence). Map the glyph to a list marker. The suspect flag on the 2019 page 141 is this fault (13 sentences, score 0.31).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 10, printed pages 152-156 (old) / 152-156 (new)
- Hunk: modified/note "Revolutionary nationalists such as Bhagat Singh and his comrades wanted ..." -> "... Bhagat Singh, Chandra Shekhar Azad, Sukhdev and others wanted to fight against the colonial rule ...", "Dutt, he threw a bomb in the Central Legislative Assembly on 8 April 1929." -> "Dutt threw a bomb in the Central Legislative Assembly.", "Members of the HSRA assassinated Saunders ..." -> "On 17 December, 1928, Bhagat Singh, Azad and Rajguru assassinated Saunders ...", "In 1944 the INA tried to invade India" -> "To free India from British control, in 1944, the INA tried to enter India"
- Images: the 2019 page 152 was rendered but not opened. The wording changes touch several clauses of different notes on the same page and are not near-identical rewordings.
- Verdict: real change (provisional)
- Fix: none. The 2019 reprint reworded these notes (and added three sentences on Bhagat Singh to the body).

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 11, printed page 160 (old) / 160 (new)
- Hunk: inserted/body "Less than six months after independence the nation was in mourning." and two more sentences, deleted/caption "Fig. 1 - Thousands gathered on the occasion of the flag hoisting ceremony at the Red Fort on 15 August 1947", inserted/caption "Fig. 1 - Mahatma Gandhi's ashes being immersed in Allahabad, February 1948"
- Images: 2019 page 160 shows a new photograph of Gandhi's ashes immersed in Allahabad, whose caption continues with "Less than six months after independence the nation was in mourning. On 30 January 1948 ..." The 2014 page 160 shows the flag-hoisting photograph.
- Verdict: real change
- Fix: none. The Fig. 1 picture, its caption and the three-sentence note were replaced.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 11, printed page 172 (old) / 172 (new)
- Hunk: modified/body "Contrary to the fears of Jawaharal Nehru and Sardar Patel" -> "Contrary to the fears of Jawahalal Nehru and Sardar Patel"
- Images: a crop of the same line on both pages. 2014 prints "Jawaharal". 2019 prints "Jawahalal".
- Verdict: real change
- Fix: none. Both are printed misspellings of "Jawaharlal" and the misspelling itself changed.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 11, printed pages 161-166 (old) / 161-166 (new)
- Hunk: "which was adopted on 26 January 1950" -> "which came into effect on 26 January 1950", "hunger fast" -> "hunger strike", "the new state of Andhra Pradesh came into being." -> "the new state of Andhra came into being, which subsequently became Andhra Pradesh.", "was broken up" -> "was also to be broken up", "31 October 1955" -> "31 October 1956"
- Images: not viewed. The wording changes are factual (a date, a term, a state name), which agree across the 2020 and later texts, so they are not an extraction fault.
- Verdict: real change (provisional)
- Fix: none.

### our-pasts-3 2014-07-28 -> 2019-03-12, chapter 11, printed page 174 (new)
- Hunk: modified/references "11, Fig. 20, Ch." -> "11, Fig. 20,", "U Ball," -> "U.Ball,", "Aggarwala" -> "Aggarwal", inserted/references "Ch." x2
- Images: 2019 page 174 shows the CREDITS page. The "(Ch. 9, Fig. 15)" style entries wrap onto indented continuation lines. In the image "U.Ball" is printed as "U.Ball" with a tight space.
- Verdict: engine noise
- Fix: the credits entries are a wrapped list. Splitting at the line wraps leaves the word "Ch." at the end of a line, which is read as a sentence end. A rule that joins an indented continuation line to its entry would remove all of the references churn (it is 80 hunks in the next pair as well).

## our-pasts-3 2019-03-12 -> 2020-10-15

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 1, printed page 1 and 7 (old) / 1 and 7 (new)
- Hunk: punctuation/body "...imperial perception. † Activity ..." -> "...perception.  Activity ..." and "Activity †" -> "Activity \x86"
- Images: 2019 page 7 and 2020 page 7 are the same page (same Source 2 box, same Activity box with the orange arrow icon, same text). Only the footer differs (2018-19 against 2020-21).
- Verdict: extraction fault (rule)
- Fix: Rule from the first pair, the Activity arrow icon is extracted as "†" in 2019 and "\x86" in 2020. Seen in ch1 p1 and p7, ch3 p28, p30 and p36. Five hunks.

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: deleted/body "W.S.", inserted/body "W." and "S."
- Images: 2020 page 36 shows "W.S. Seton Karr" both in the Activity box ("Imagine you are a witness giving evidence before the Indigo Commission. W.S. Seton Karr asks you ...") and in the Source 3 box. The 2019 page 36 has the same layout.
- Verdict: engine noise
- Fix: do not split sentences after a single capital letter followed by a full stop. Same pattern as in the first pair.

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 8 (old 9), printed page 116 (old) / 102 (new)
- Hunk: deleted/heading "Gulamgiri" and modified/body "Fig. 12 - Shri Narayana Guru One of the most vocal ..." -> "Fig. 12 - Shri Narayana Guru Gulamgiri One of the most vocal ..."
- Images: 2019 page 116 and 2020 page 102 are the same page, with "Fig. 12 - Shri Narayana Guru" at the foot of the left column. The italic word "Gulamgiri" is the first line of page 103 (2020), above "One of the most vocal amongst the "low-caste" leaders was Jyotirao Phule."
- Verdict: extraction fault (rule)
- Fix: Rule B. The 2020 extraction lost the heading and welded it between the caption and the next page's first paragraph. Note that the 2019 heading was placed on a different page (117) from the caption (116), which is the correct page order.

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 8 (old 9), printed page 118 (old) / 104 (new)
- Hunk: deleted/caption "Fig. 14 - The gateway to the Madurai temple, drawn by Thomas Daniell, 1792" and modified/table ""Untouchables" were not allowed anywhere near such gateways ..." -> "Fig. 14 - The gateway to the Madurai temple, drawn by Thomas Daniell, 1792 "Untouchables" were not allowed ..."
- Images: 2020 page 104 shows one caption block at the left, with the bold italic title "Fig. 14 - The gateway to the Madurai temple, drawn by Thomas Daniell, 1792" and, under it in regular type, ""Untouchables" were not allowed anywhere near such gateways until the temple entry movement began." The temple picture runs across the foot of the page. Both printings have the same words.
- Verdict: extraction fault (rule)
- Fix: Rule A. The title line and the description are one caption, but the 2019 text emits the title twice (as a table and as a caption) and the 2020 text emits it once, glued into the table. The "caption + table" pair should be one caption block (this also explains the same fault in the 2022 -> 2023 pair, which goes the other way).

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 11 (old 12), printed page 174 (old) / 142 (new)
- Hunk: 66 deleted/references ("(Ch.", "1, 2, 4, 6, 7, 9)", "Institutions", "Books", "CREDITS" ...) and inserted/references "NOTES"
- Images: 2019 page 174 is a full CREDITS page (Institutions, Journals, Books, with "Ch. 7, Figs. 4, 5" style references). The 2020 page 142 is an empty page with only the title "NOTES" and the watermark. The suspect flag on 2019 page 174 is this deletion.
- Verdict: real change
- Fix: none. NCERT removed the picture credits from the book in 2020 and put a blank Notes page in its place. The 66 deleted hunks are one deletion and could be collapsed by treating a references stream with no counterpart as a single deleted block.

### our-pasts-3 2019-03-12 -> 2020-10-15, chapters 1, 10 (old 12), printed pages 1, 169-170
- Hunk: typographic/body "1870s-1947" -> "1870s--1947", "1945-47" -> "1945- 47", "war-often" -> "war - often", "Fig. 8-" -> "Fig. 8 -"
- Images: 2019 page 141 and the 2020 equivalent show "1870s-1947" in the heading as a single hyphen. The other three are spacing around a dash.
- Verdict: engine noise
- Fix: none. These are already classed as typographic and are minor. Listed so that the counts reconcile.

### our-pasts-3 2019-03-12 -> 2020-10-15, chapter 6 (old 7), printed page 93 (old) / 79 (new)
- Hunk: moved/heading "Let's recall"
- Images: not viewed. The heading is on the same layout in the two editions (the chapter lost its first pages, so it moves from p93 to p79).
- Verdict: engine noise
- Fix: none. Already classed as moved.

## our-pasts-3 2020-10-15 -> 2021-08-14

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 2, printed page 20 (old) / 20 (new)
- Hunk: modified/caption "Fig. 11 a, b, c - Expansion of British territorial power in India" -> "Fig. 14 a, b, c - ...", and "Fig. 14c - India, 1857" -> "Fig. 14 c - India, 1857"
- Images: the 2020 page shows "Fig. 11 a, b, c - Expansion of British territorial power in India" in the box at the bottom right, and "Fig. 14c - India, 1857" under the third map. The 2021 page shows "Fig. 14 a, b, c" in the same box and "Fig. 14 c - India, 1857" with the extra space.
- Verdict: real change
- Fix: none. NCERT corrected the label in the box (11 was a leftover from the 2014 numbering) and the spacing. The hunks are accurate.

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 5, printed page 56 (old) / 56 (new)
- Hunk: modified/body "On 29 March 1857, a young soldier, Mangal Pandey, was hanged to death for attacking his officers in Barrackpore." -> "On 8 April 1857, ..."
- Images: the 2020 page reads "On 29 March 1857, a young soldier, Mangal Pandey, was hanged to death" and the 2021 page reads "On 8 April 1857, a young soldier, Mangal Pandey, was hanged to death". The date is the only difference, and 8 April is the historically correct date for the hanging.
- Verdict: real change
- Fix: none. A factual correction. The 2022 and later texts keep 8 April 1857.

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 5, printed pages 54-55 (old) / 54-55 (new)
- Hunk: resplit/caption "Fig. 3 - Rebel sepoys at Meerut attack officers, enter their homes and set fire to buildings Source 2" and deleted/table "Source 2 contd."
- Images: the 2020 page 54 shows "Fig. 3 - Rebel sepoys at Meerut ... set fire to buildings" under the picture and "Source 2 contd." at the foot of the purple box. Page 55 starts with "Source 2 contd." above the box. The 2021 pages are the same. The "Source 2 contd." label occurs once at the foot of page 54 and once at the top of page 55 in both printings.
- Verdict: engine noise
- Fix: none. The 2020 text emits three blocks (table "Source 2 contd.", caption "Source 2", table "Source 2 contd.") and the 2021 text glues "Source 2" onto the Fig. 3 caption and keeps two "contd." labels. Rule A, also seen in 2014 and 2022. The words are identical.

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 6, printed page 71 (old) / 71 (new)
- Hunk: deleted/table "Proceedings of the Board of Trade, 3 February 1824" (reappears as inserted/table in 2021 -> 2022)
- Images: 2020 page 71 and 2021 page 71 both show "Proceedings of the Board of Trade, 3 February 1824" in italic at the foot of the Source 1 box ("We must starve for food"). The PDFs of 2020, 2021 and 2022 all contain the line as text.
- Verdict: extraction fault (one-off)
- Fix: the 2021 text lost the attribution line, and the 2022 text restored it (see the next pair). Override for 2021-08-14, ch6:
  - snapshot: "2021-08-14", chapter: 6
  - find: "kindness towards us and give orders for clothes."
  - replace: "kindness towards us and give orders for clothes.\n\n> [table] Proceedings of the Board of Trade, 3 February 1824"
  - note: "2021 extraction dropped the italic source line at the foot of the Source 1 box on page 71. It is printed in the page and is present in the 2020 and 2022 texts."
  (The exact block separator should be copied from the 2020 text, line 124 of `06-weavers-iron-smelters-and-factory-owners.md`.)

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 7, printed page 81 (old) / 81 (new)
- Hunk: deleted/caption "Fig. 1 - William Jones learning Persian"
- Images: the 2020 and 2021 pages both show the picture of William Jones with the caption "Fig. 1 - William Jones learning Persian" below it in the right column. The line is text in the PDF of both.
- Verdict: extraction fault (one-off)
- Fix: override for 2021-08-14, ch7 (and the same for 2022-08-02, which also lacks it):
  - snapshot: "2021-08-14" (and "2022-08-02"), chapter: 7
  - find: "the subtleties of Sanskrit language, grammar and"
  - replace: "the subtleties of Sanskrit language, grammar and\n\n> [caption] Fig. 1 - William Jones learning Persian"
  - note: "caption dropped by extraction on page 81. The line is in the PDF text of the 2021 and 2022 files and visible in the image."
  (The fix pass should check how the 2020 text positions the caption, line 32 of `07-civilising-the-native-educating-the-nation.md`, and mirror it.)

### our-pasts-3 2020-10-15 -> 2021-08-14, chapter 10, printed page 135 (old) / 135 (new)
- Hunk: deleted/caption "Fig. 5 (c) - Indian States in 1975"
- Images: both pages show the lower map with "Fig. 5 (c) - Indian States in 1975" under it. 2020 has the map at the left margin of the box and the 2021 page has it indented. The text is in both PDFs.
- Verdict: extraction fault (one-off)
- Fix: override for 2021-08-14 and 2022-08-02, ch10:
  - snapshot: "2021-08-14" (and "2022-08-02"), chapter: 10
  - find: "Identify the new states that were formed in 1956 and later and the languages of these states."
  - replace: "Identify the new states that were formed in 1956 and later and the languages of these states.\n\n> [caption] Fig. 5 (c) - Indian States in 1975"
  - note: "caption under the third map of page 135 was dropped. Visible in the image and in the PDF text of the 2021 and 2022 files."
  (Check the block order against the 2020 text, line 124 of `10-india-after-independence.md`, where the caption follows the Activity paragraph.)

## our-pasts-3 2021-08-14 -> 2022-08-02

### our-pasts-3 2021-08-14 -> 2022-08-02, chapter 3, printed page 27 (old) / 27 (new)
- Hunk: deleted/heading "Revenue for the Company" and modified/body "The Company had become the Diwan, ..." -> "Revenue for the Company The Company had become the Diwan, ..."
- Images: both pages show "Revenue for the Company" as a bold sub-heading above "The Company had become the Diwan, but it still saw itself primarily as a trader."
- Verdict: extraction fault (rule)
- Fix: Rule B. The heading is merged into the next paragraph in 2022. It flips again in 2022 -> 2023.

### our-pasts-3 2021-08-14 -> 2022-08-02, chapter 3, printed page 27 (old) / 27 (new)
- Hunk: modified/body "Before 1865, the Company had purchased goods in India by importing gold and silver from Britain." -> "Before 1765, ..."
- Images: the 2021 page prints "Before 1865," and the 2022 page prints "Before 1765,". The Diwani was granted in 1765.
- Verdict: real change
- Fix: none. A printed error in 2021 was corrected in 2022. Worth a line in `docs/findings.md`.

### our-pasts-3 2021-08-14 -> 2022-08-02, chapter 4, printed page 43 (old) / 43 (new)
- Hunk: modified/caption "Fig. 5 - A log house being built in a village of the Nishi tribes of Arunachal Pradesh." -> "... the Nyishi tribes ..." and restreamed/heading x3
- Images: the 2021 caption reads "Nishi tribes" and the 2022 caption reads "Nyishi tribes". The three sub-headings are the same bold lines on both pages.
- Verdict: real change
- Fix: none. The spelling was corrected. The three restreamed headings are noise that the engine has already classed as minor.

### our-pasts-3 2021-08-14 -> 2022-08-02, chapter 6, printed page 71 (new)
- Hunk: inserted/table "Proceedings of the Board of Trade, 3 February 1824"
- Images: the same page as above. The italic line is at the foot of the Source 1 box.
- Verdict: extraction fault (one-off)
- Fix: this is the mirror of the 2020 -> 2021 hunk. Fixing the 2021 text by the override above clears both hunks.

## our-pasts-3 2022-08-02 -> 2023-12-23-rationalised

The 2023 edition is the rationalised book. Chapters 6 and 10 of the 2022 book (weavers, India after independence) are dropped. A page of ELSEWHERE boxes was removed in most chapters, which accounts for most of the deleted hunks and for all of the suspect pages (24, 37, 92, 107, 109, 126 in the old book).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 1, printed pages 3-4 (old) / 3-4 (new)
- Hunk: modified/body "Religious intolerance, caste taboos and superstitious practices dominated Activity Interview ..." -> "To do Activity Interview ...", inserted/body "Religious intolerance, caste taboos and superstitious practices dominated social life.", deleted/body "social life.", "To do this it was necessary ..." -> "this, it was necessary ..."
- Images: the 2023 page 3 and the 2022 page 3 differ in layout (the 2023 page has a "To do" header in the Activity column). A paragraph that crosses a page turn is cut by the Activity box in 2022 and rebuilt in 2023.
- Verdict: extraction fault (rule)
- Fix: Rule A. Sentences broken at a page turn or by a margin box. The words are the same apart from "To do this" -> "this," and "Introduction:" in the chapter title, which are real edits.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 1, printed page 5 (old) / 5 (new)
- Hunk: modified/body "Vizagapatnam: The position is completely under control and no violence has occurred." -> "Vizagapatnam: The positionis completely under control ..."
- Images: the 2023 page 5 prints "positionis completely under control" in the Source 1 box (the two words really are run together in the printed page, in the justified text of the narrow box). The 2022 text has the words separated.
- Verdict: real change
- Fix: none. The printed text changed. (The line "Home (Political), Government of India" moving between the caption and table streams is engine noise.)

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 1, printed page 7 (old) / 7 (new)
- Hunk: modified/body "Explain what you observe." -> "Explain what you observed."
- Images: not viewed. The text is a one-word wording change that agrees with the 2024 text.
- Verdict: real change (provisional)
- Fix: none.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 2, printed page 24 (old)
- Hunk: deleted/body "ELSEWHERE", "Slave Trade in South Africa", "The Dutch trading ships reached southern Africa in the seventeenth century." and ten more sentences, deleted/table "Quoted in Nigel Wordon et. al., The Chains that Bind us ..."
- Images: not viewed for 2022 page 24. The 2023 page 25 was viewed and the chapter now runs straight into the exercises, with no ELSEWHERE box. The structure is the same as page 37 of chapter 3 (viewed, below).
- Verdict: real change (provisional)
- Fix: none. The Elsewhere box on the slave trade was removed in the rationalised book.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 2, printed pages 24-25 (old) / 24-25 (new)
- Hunk: modified/exercises "(c) Dalhousie implemented the Doctrine of ___________." -> "(c) Dalhousie implemented the Doctrine of", "Calcutta grew from a small village" -> "grew from small village"
- Images: the 2023 page 25 reads "Calcutta grew from small village to a big city" (the article "a" is missing in the printed book). Page 24 (blank in the text) was not viewed.
- Verdict: real change
- Fix: none for the missing article. The dropped blank "___________" in (c) is an extraction fault (one-off) in the 2023 text. Override: snapshot "2023-12-23-rationalised", chapter 2, find "(c) Dalhousie implemented the Doctrine of\n", replace "(c) Dalhousie implemented the Doctrine of __________.\n", note "the answer blank at the end of the line is not extracted. It is printed in the exercise (check the exact number of underscores on the page image)".

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 27 (old) / 27 (new)
- Hunk: inserted/heading "Revenue for the Company", modified/body "Revenue for the Company The Company had become the Diwan ..." -> "The Company had become the Diwan ..."
- Images: 2022 page 27 shows "Revenue for the Company" as a bold heading above the paragraph. The 2023 text restores it.
- Verdict: extraction fault (rule)
- Fix: Rule B (the 2022 extraction is the faulty side).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 30 (old) / 30 (new)
- Hunk: modified/body "There is one thing common in the two prints" -> "There is one thing common in the Fig. 5 - A kalamkari print, twentieth-century India two prints ..." and deleted/caption "Fig. 5 - A kalamkari print, twentieth-century India"
- Images: both pages (2022 and 2023) show Fig. 5 (kalamkari print) and Fig. 6 (Morris print) in a box on the left and a "Does colour have a history?" paragraph that ends with "There is one thing common in the" at the foot and continues on the next page. The caption lies between the two.
- Verdict: extraction fault (rule)
- Fix: Rule A. The 2023 text glues the Fig. 5 caption into the middle of the sentence.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 32 (old) / 32 (new)
- Hunk: modified/body "commercial agents and officials of the Company" -> "commercial agents a n d o f f i c i a l s o f t h e Company"
- Images: the 2023 page 32 sets "and officials of the" with very wide word spaces. The 2022 text has the words together.
- Verdict: extraction fault (rule)
- Fix: Rule C. Same cause as "e d u c a t i o n w h i c h" in chapter 6 (2023 page 69) and "T e l a n g t o o r em ain s" in the 2024 chapter 8 (page 96). Three places in this book. A rule that merges runs of single letters separated by single spaces when the merged word is in the vocabulary would remove them.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 37 (old) / 37 (new)
- Hunk: deleted/body "ELSEWHERE", "Indigo making in the West Indies", "In the early eighteenth century, a French missionary, Jean Baptiste Labat, ..." and seven more sentences, deleted/caption "Fig. 14 - Making indigo in a Caribbean slave plantation"
- Images: the 2022 page 37 has the blue ELSEWHERE box "Indigo making in the West Indies" with Fig. 14. The 2023 page 37 has no box, and goes from the Champaran paragraph straight to "Let's recall".
- Verdict: real change
- Fix: none. Cause of the suspect flag on 2022 page 37.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 36 (new)
- Hunk: inserted/caption "Indigo Commission Report, Vol." and "II, Minutes of Evidence, p. 67", deleted/table "Indigo Commission Report, Vol. II, Minutes of Evidence, p. 67"
- Images: the 2020 page 36 (same layout, the 2022/2023 pages were not viewed) shows the line as one italic source line at the foot of the Source 3 box.
- Verdict: engine noise
- Fix: a sentence splitter issue ("Vol." read as an end of sentence). The words are the same, a `restreamed` rule would clear it.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 4, printed pages 46-49 (old) / 46-49 (new)
- Hunk: "The growers were paid Rs 3 to Rs 4" -> "The growers were paid ` 3 to ` 4", deleted/exercises "Cash cropping is all very well ..." and "ELSEWHERE ... Why do we need cash!", "____________" -> "_________" (blanks)
- Images: not viewed for these pages. "Rs" -> "`" is the rupee symbol extracted from a font that maps it to a backtick (the text reads "` 3", a space and the glyph).
- Verdict: extraction fault (rule) (provisional)
- Fix: map the backtick rupee glyph ("` 3", "` 4") to "Rs 3", "Rs 4" in the 2023 and 2024 files. Seen once in ch4 of the 2023 file (the 2024 page 14 prints "Rs. 500,000" with the plain form).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5, printed pages 57-59 (old) / 56-58 (new)
- Hunk: modified/body "In Jhansi, Rani Lakshmibai joined the rebel sepoys and fought the British along with Tantia Tope, the general of Nana Saheb." -> "fought the British along with Tantia Tope, the general of Nana Saheb." and inserted/body "In Jhansi, Rani Lakshmibai joined the rebel sepoys and Activity"
- Images: the 2022 page 58 starts with "fought the British along with Tantia Tope, the general of Nana Saheb." under the Activity box. The first half of the sentence is at the foot of the previous page. The 2023 page 58 is the same.
- Verdict: extraction fault (rule)
- Fix: Rule A. The sentence is broken at the page turn and the Activity box has been inserted between its halves in 2023, which the rejoining rule should skip. The same page contains the identical pair for "Nana Saheb, the adopted son of" (p51/52), "It brought" (p58/59) and "Mutiny - ... On 8 April" (glossary box).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5, printed page 62 (old) / 62 (new)
- Hunk: "in the south-eastern part of Odisha," -> "Orissa,", and ten more "Odisha" -> "Orissa" hunks (pages 62 and 63)
- Images: the 2022 page 62 prints "Odisha" in the Khurda box. The 2023 page 62 prints "Orissa" in the same box.
- Verdict: real change
- Fix: none. The rationalised book reverts to the older spelling "Orissa". (The 2019 book also said "Odisha", so the spelling moved twice.)

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5, printed page 63 (old)
- Hunk: deleted/body "ELSEWHERE", "For a Heavenly Kingdom of Great Peace", "While the revolt was spreading in India in 1857, a massive popular uprising was raging in the southern parts of China." and seven more, deleted/caption "Fig. 16 - Taiping army meeting their leader"
- Images: not viewed for 2022 page 63. The 2023 pages 57 and 58 were viewed (no Taiping box).
- Verdict: real change (provisional)
- Fix: none. The Elsewhere box on the Taiping rebellion was removed.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5, printed page 59 (old) / 59 (new)
- Hunk: modified/caption "Fig. 13 - Postal stamp Essued in commemoration of Tantia Tope" -> "Fig. 13 - Postal stamp issued ..."
- Images: not viewed. The 2024 text and the 2019 text both read "Essued" only in the 2019-2022 files, which is a misread of an italic "issued" (the 2023 file reads "issued").
- Verdict: extraction fault (one-off)
- Fix: override for 2019-03-12, 2020-10-15, 2021-08-14 and 2022-08-02:
  - snapshot: "2019-03-12" (and the other three), chapter: 5
  - find: "Fig. 13 - Postal stamp Essued in commemoration of Tantia Tope"
  - replace: "Fig. 13 - Postal stamp issued in commemoration of Tantia Tope"
  - note: "OCR or font misread of 'issued' in the caption on page 59. The 2023 edition has 'issued'. Check on the page image before pasting."

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 6 (old 7), printed page 85 (old) / 69 (new)
- Hunk: modified/body "We must emphatically declare that the education which we desire ..." -> "the e d u c a t i o n w h i c h we desire ..." and modified/body "With great energy" -> "With gr eat energy"
- Images: the 2023 page 69 shows the Source 2 box ("An argument for European knowledge") set in a narrow column with very wide letter and word spacing in "education which". The words are not misspelled on the page.
- Verdict: extraction fault (rule)
- Fix: Rule C. For "gr eat" the same applies to the justified paragraph on page 68 (not viewed, same mechanism).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 6 (old 7), printed page 92 (old)
- Hunk: deleted/body "ELSEWHERE", "Education as a civilising mission", "Until the introduction of the Education Act in 1870 ..." and thirteen more sentences
- Images: not viewed. The 2023 chapter 6 ends at page 76 without the box.
- Verdict: real change (provisional)
- Fix: none. The suspect flag (21 sentences, score 0.29) is this deletion.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 6 (old 7), printed pages 86-90 (old) / 70-74 (new)
- Hunk: modified/caption "Fig. 6 - William Carey ..." -> "Fig. 6 - William Carey ... Fig. 7 - Serampore College on the banks of the river Hooghly near Calcutta", deleted/caption "Fig. 7 - ...", modified/table "The Collected Works of Mahatma Gandhi, Vol. 72, p. 79" -> "... Vol." and inserted/caption "72, p. 79"
- Images: not viewed.
- Verdict: engine noise (provisional)
- Fix: Rule A (two captions on one page glued together) and the "Vol." sentence-split noted above.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 7 (old 8), printed pages 106-107 (old) / 90-91 (new)
- Hunk: modified/body "The Brahmo Samaj The Brahmo Samaj, formed in 1830 ..." -> "The Brahmo Samaj, formed in 1830 ..." (six headings: Brahmo Samaj, Prarthana Samaj, Aligarh Movement, Derozio and Young Bengal, Singh Sabha Movement, Ramakrishna Mission) and inserted/note x6
- Images: not viewed for this page. The same six boxes appear in the 2019 and 2022 text with the heading glued, and with the heading separate in the 2023 text.
- Verdict: extraction fault (rule)
- Fix: Rule B. In 2022 the headings are glued and in 2023 they are separate notes. Twelve hunks.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 7 (old 8), printed page 107 (old)
- Hunk: deleted/body "ELSEWHERE", "Black slaves and white planters", "You have read about how Jyotirao Phule established a connection ..." and nine more, deleted/caption "Fig. 21 - Slave Sale, South Carolina, USA, 1856", deleted/table "Here you see potential buyers examining African slaves at an auction."
- Images: not viewed. The suspect flag is this box (22 sentences, score 0.36).
- Verdict: real change (provisional)
- Fix: none.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 7 (old 8), printed page 104 (old) / 88 (new)
- Hunk: modified/table "Fig. 14 - The gateway to the Madurai temple ... "Untouchables" were not allowed ..." -> ""Untouchables" were not allowed ..." and inserted/caption "Fig. 14 - The gateway to the Madurai temple, drawn by Thomas Daniell, 1792"
- Images: the 2020 page 104 (same layout) shows the title and the description in one caption block. Both are in the 2023 page as well.
- Verdict: extraction fault (rule)
- Fix: Rule A (title and description of one caption emitted once as one block and once as two). Same cause as in 2019 -> 2020.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 7 (old 8), printed page 108 (old) / 91-92 (new)
- Hunk: "in1829." -> "in 1829.", "Jyoti rao Phule" -> "Jyotirao Phule", "openedup" -> "opened up", "Jyotirao the reformers" -> "Jyotirao, and other reformer", "2. State whether true or false:" moved
- Images: the 2019 page 122 (viewed, same exercise text) prints "in1829." and "Jyoti rao" (printed faults) and "opened up" (printed fine, the text lost the space). The 2023 text corrects "in 1829" and "Jyotirao". "Jyotirao the reformers" is printed in 2019 and re-worded in 2023 ("Jyotirao, and other reformer", with the singular "reformer" which looks like a further printing error).
- Verdict: real change
- Fix: none for "in 1829", "Jyotirao" and "Jyotirao, and other reformer". "openedup" -> "opened up" is the fix of an extraction fault already listed (one-off override above), so the hunk disappears once that override is in place.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 8 (old 9), printed pages 109 and 93 (old / new)
- Hunk: deleted/body "In the previous chapters we have looked at: ..." and inserted/body "The British conquest of territories, and takeover of kingdoms Introduction of new laws ..." (one block)
- Images: 2019 page 141 shows the list as nine bullets. The 2023 text joins the nine into one paragraph (without the "¢" glyph) and the 2022 text has the glyph "¢" at the start of each line.
- Verdict: extraction fault (rule)
- Fix: the square bullet rule from the first pair. The 2022 and earlier files emit "¢" bullets and the 2023 file emits a single block with no marker. Treat the glyph as a list bullet and emit one `-` item per line in every edition.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 8 (old 9), printed page 126 (old) / 109 (new)
- Hunk: deleted/body "ELSEWHERE", "Nationalism in Africa: The case of Ghana", "The late nineteenth and early twentieth centuries witnessed the rise of nationalism in many Afro-Asian countries." and fourteen more
- Images: not viewed for 2022 page 126. The 2023 page 109 was rendered but not opened.
- Verdict: real change (provisional)
- Fix: none. Cause of the suspect flag (26 sentences, score 0.38).

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 8 (old 9), printed pages 109-110 (new)
- Hunk: modified/body "Torn asunder from their homelands, they were reduced to being refugees in alien lands." -> "... in alien" and inserted/exercises "lands."
- Images: not viewed.
- Verdict: extraction fault (rule) (provisional)
- Fix: Rule A. The last word of a sentence is carried onto the next page. Join across the turn.

### our-pasts-3 2022-08-02 -> 2023-12-23-rationalised, chapter 8 (old 9), printed pages 124-125 (old) / 107-108 (new)
- Hunk: "Fig. 20 - Jawaharlal Nehru listens ..." moved from the body into a caption (Fig. 16 in 2023), "Patel hailed from an impoverished peasant-proprietor family of Nadiad, Gujarat." moved between two paragraphs, Fig. 17, 18, 19, 20 renumbered
- Images: not viewed.
- Verdict: real change (provisional, figure numbers), engine noise (moved sentences)
- Fix: none. A new list of figures follows the removal of chapter pictures, and the re-numbering by one is consistent in every hunk.

## our-pasts-3 2023-12-23-rationalised -> 2024-08-04

This pair is a reprint. The changes come from the 2024-25 reprint of the rationalised book. Most of the remaining hunks are the word changes listed below.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 2, printed page 14 (old) / 14 (new)
- Hunk: modified/heading "Company officials become "nabobs"" -> "Company officials become "nabobs" (nawabs)"
- Images: the 2024 page 14 prints "Company officials become "nabobs" (nawabs)" as a bold sub-heading.
- Verdict: real change
- Fix: none.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 2, printed pages 17-18 (old / new)
- Hunk: "Seringapatam" -> "Shrirangapatnam" (four places), "Benaras" -> "Banaras" (page 22), deleted/body "Finally, the Third Anglo-Maratha War of 1817-19 crushed Maratha power." and modified/body "The Peshwa was removed ..." -> "Finally, the Maratha power came to end with the Third Anglo-Maratha War of 1817-19. The Peshwa was removed ..."
- Images: not viewed for these pages. The 2024 page 14 (viewed) is in the same reprint and carries the new spellings. The place name changes are consistent across all places.
- Verdict: real change (provisional)
- Fix: none. The reprint renamed Seringapatam and Benaras, and reworded the Third Anglo-Maratha War sentence. The deleted and rewritten sentence pair is one rewording that the matcher reports as a deletion and a modification.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 3 (tribals), printed pages 48-49 (old / new)
- Hunk: "Birsa also turned against missionaries and Hindu landlords." -> "... and landlords." (three places), inserted/exercises "Postal stamp issued in memory of Birsa Munda"
- Images: not viewed for page 48. The 2024 text was checked with the text of page 49.
- Verdict: real change (provisional)
- Fix: none. The word "Hindu" was removed in three sentences. The caption inserted under the "exercises" stream is a Fig. caption of a new stamp picture placed at the foot of page 49, which the extractor placed in the exercises stream (Rule A).

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 4, printed pages 51-61 (old / new)
- Hunk: "When People Rebel 1857 and After" -> "When People Revolt 1857 and After", "A Mutiny Becomes a Popular Rebellion" -> "... Uprising", "The rebellion spreads" -> "The uprising spreads", and fourteen body hunks "rebellion" -> "uprising"
- Images: the 2024 page 57 and page 58 were rendered but not opened. The change is a uniform word substitution.
- Verdict: real change (provisional)
- Fix: none. The 2024 reprint changes "rebellion" to "uprising" and "rebel" to "revolt" in the chapter title.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 4, printed pages 57-58 (old / new)
- Hunk: "In Jhansi, Rani Lakshmibai joined the rebel sepoys and Activity" -> "... and fought the British along with Tantia Tope, the Activity", deleted/body "fought the British along with Tantia Tope, the general of Nana Saheb.", inserted/body "general of Nana Saheb."
- Images: not viewed. The 2022 page 58 (viewed) shows the break after "the general of" at the page turn.
- Verdict: extraction fault (rule)
- Fix: Rule A. The break point moved by two words between the 2023 and 2024 extractions of the same sentence. Page turn rejoining would remove all three hunks.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 6, printed page 83 (old / new)
- Hunk: "criticising the social differences between men and women." -> "... men and women (Men Dominant Society)."
- Images: the 2024 page 83 prints "criticising the social differences between men and women (Men Dominant Society)." in the second paragraph.
- Verdict: real change
- Fix: none.

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 8, printed page 96 (old / new)
- Hunk: "T e l a n g t o o r em ains busy." -> "T e l a n g t o o r em ain s busy."
- Images: the 2024 page 96 shows the Source 2 box "In pursuit of gold", where the line "Mr. Telang too remains busy." is set with very wide word spacing. The word is spelt correctly in print.
- Verdict: extraction fault (one-off)
- Fix: Rule C covers it. As a one-off, override for both snapshots, find "T e l a n g t o o r em ain s busy." replace "Telang too remains busy." with snapshot "2024-08-04" and the same text without "ain s" for "2023-12-23-rationalised" (find "T e l a n g t o o r em ains busy.").

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 1, printed page 2 (old / new)
- Hunk: typographic/body "... deeds of others - Hastings ..." (a long dash against a short one)
- Images: not viewed.
- Verdict: engine noise
- Fix: none (typographic, already minor).

### our-pasts-3 2023-12-23-rationalised -> 2024-08-04, chapter 2, printed page 22 (old / new)
- Hunk: typographic/body "composed from c. 500 BCE onwards" -> "c. 500 bce onwards"
- Images: not viewed.
- Verdict: engine noise
- Fix: none. Already minor. The 2024 file has small capitals for BCE in the glossary. Mapping the lowercase form back to "BCE" would remove the hunk.

## Summary

Counts per verdict (several entries cover a group of hunks that have one cause): 77 entries: 32 real change, 27 extraction fault (rule), 11 engine noise, 7 extraction fault (one-off). Of these, 18 are marked provisional because the page image was not opened.

Pages not viewed (marked "not viewed" or "provisional" above): most of the 2014 -> 2019 chapters 7 to 10 pages, 2022 -> 2023 chapters 4, 7 and 8 pages with Elsewhere boxes, and the 2023 -> 2024 chapter 2, 3 and 4 spelling changes. The verdicts on those rest on the neighbouring viewed page and on the extracted text, and the fix pass should re-open them before any override is applied.

The three patterns that would remove the most noise if fixed by a rule:

1. Page-turn and margin-box joining (Rule A and B together). Sentences broken at a page turn, captions and margin glossary boxes emitted into the middle of paragraphs, small run-in headings glued to the next paragraph ("Revenue for the Company", "Gulamgiri", the six reform-movement headings), and caption titles emitted twice. This touches every pair, in roughly 80 hunks. A rule that rejoins a sentence over a page turn while skipping captions, glossary boxes and Activity boxes, and a rule that treats a short bold or italic first line as a heading, would clear most of them.
2. Glyph and list-marker mapping. The Activity arrow icon (extracted as "†", "\x86", or a leading space), the square bullet (extracted as "¢" or dropped), the rupee sign (extracted as a backtick), and the credits list whose wrapped continuation lines make "Ch." a sentence end. About 130 hunks across 2014 -> 2019, 2019 -> 2020 and 2022 -> 2023, 80 of them from the 2019 credits page alone.
3. Letter-spaced and tight text (Rule C) plus initials splitting. "e d u c a t i o n", "T e l a n g", "a n d o f f i c i a l s", "gr eat", "openedup", "1.In", "2.Notice", and the sentence splitter that cuts after "W.", "S.", "Vol." and "No.". About 25 hunks, all with identical words on both sides.
