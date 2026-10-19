# Review of social-political-life-3 (Social and Political Life III, Class 8 civics)

Every entry below was judged by rendering the page of both editions from the source PDF and looking at it. Chapter numbers are those of the new edition unless written old:new. Page numbers are printed pages.

Pairs reviewed: 2014-07-28 -> 2016-09-10, 2016-09-10 -> 2019-05-04, 2019-05-04 -> 2020-06-16, 2020-06-16 -> 2021-08-14, 2021-08-14 -> 2022-08-02, 2022-08-02 -> 2023-12-23-rationalised, 2023-12-23-rationalised -> 2024-05-24.

## Patterns referred to in the entries

Each pattern has a short name so that the entries can point to it.

- Rule A, stray decorative glyph. The large "Q" of the exercise boxes (a 100 pt glyph in the box, PDF font TT2ADT00 in 2019) and the lettering "Po" in the police-station comic art are read as text and glued to the next or previous line. The "Q" also reaches paragraphs on the page after a Q box where nothing is drawn (ch5 page 61). Places seen: ch1 p10 "QNow" (2014 only), ch5 p56 "QImagine" (2014, 2019 to 2024), ch5 p56 "QDispute" and ch5 p60 "QA group" (2016), ch5 p61 "QIn principle" (2014, 2019 to 2024), ch6 p70 "PoFrom" (2014, 2019 to 2022), ch6 p68 "PoMr" (2016), ch6 p72 "Q2." (2014, 2019 to 2022) and "Qb)" (2016), ch6 p75 "Qa." (2016), ch6 p76 "QIn a town" (2014, 2019 to 2022), ch9 p112 "Q2. The government can get private companies" (every edition, ch7 p92 in the rationalised books). Rule: drop a lone "Q" or "Po" span whose font size is far above the body size, or the leading capital Q glued to a following capital letter, when no such letter is in the page image.
- Rule B, footer band cuts real text. `FOOTER_BAND = 0.86` in `src/ncert_diff/extract.py` marks any short small block that starts below 86 per cent of the page height as a footer. In the 2021 to 2024 files real last lines sit at 86.1 to 86.9 per cent and are dropped. Places seen (all in every file from 2021 to 2024 unless stated): ch1 p14 last list line "armed forces for being a woman.", ch1 p17 glossary "Tyranny: The cruel and unjust use of power or authority.", ch9/7 pie chart label "Central Sector Scheme" (2021 to 2023), ch10/8 reference "Sustainable Development Goals (SDGs), www.in.undp.org" (2021 to 2024), ch5/4 caption "High Court of Karnataka http://karnatakajudiciary.kar.nic.in" (2023 and 2024 only, the 2022 file keeps it). Two photo captions in ch10/8 on the Bhopal spread, "A child severely affected by the gas" and "The struggle for justice goes on…" (blocks at 91 to 94 per cent of the height), are dropped in every edition from 2014 to 2024, so they never show in a diff but the text is missing everywhere. Rule: the footer test needs a stronger condition (a page number or running title in the block, or the block lying below the last body block with a gap) before dropping a block.
- Rule C, side question spliced into a paragraph at a page break. When a paragraph runs over a page break the grey side question of that page is written in the middle of the sentence and the first line of the next page becomes a fragment. Places seen: 2016 ch6 p73/74 "the chargesheet and What did the judge say in Shanti’s case ...", 2016 ch6 p70/71 "it is not the job" plus the sub-heading, 2014 and 2016 ch7 p83/84 "them, Explain at least three different reasons ...", 2014 and 2016 ch7 p86/87 "They, thus, get caught Adivasis use around ...", 2014 and 2016 ch7 p87/88 "may In your opinion, why is it important ...".
- Rule D, same text in another stream or in another reading order (engine noise). Speech bubbles and storyboard captions, table rows and the "Q" boxes come out in a different order or in a different stream (body, caption, table, heading, note) in two editions with identical content, so a hunk pair of deleted and inserted appears. Places seen are named in the entries. Fix: in `diff.py` match deleted and inserted hunks of one chapter across streams by normalised word bag when the similarity is 0.9 or more, and class the result as restreamed or moved.
- Rule E, chart labels. The labels of the two pie charts (ch9 p111 and p112, and ch7 p91 and p92 in the rationalised books) are written as one caption fragment per label ("5 p.", "Pensions", "(4%)"). Any change of the chart or of the extraction shows as dozens of one-word deletions and insertions. Fix: join the chart labels of one figure into one caption block, or class captions of three words or fewer made of digits, "p." and "%" as minor.
- Rule F, list label glued in the 2022 file. The 2022-08-02 text writes "1.that", "2.that", "3.that" (ch2 p21) and "1.Throughout" to "4.Within" (ch9 p114 and p115). The page image of both the 2021 and the 2022 printing shows the normal "1. that". Fix: in `clean.py` insert a space after a list label of the form `^\d+\.` when a letter follows directly.
- Rule G, chapter pairing when chapters are merged (2022 to 2023 only). Old ch4 "Understanding Laws" and old ch6 "Understanding Our Criminal Justice System" are marked dropped. The page images show that the storyboard, the glossary and the exercises of old ch4 are now in new ch3 "Parliament and the Making of Laws". Old ch3 is therefore compared with a chapter that is half old ch4, and about 170 hunks of ch3 are noise. Fix: match a new chapter against the concatenation of two old chapters when the page images and the text of the dropped chapter reappear (word-bag overlap above 0.6).
- Rule H, doubled fake-bold text in the 2016 file. Paragraphs set in a heavy face are drawn twice and the second pass loses or repeats letters ("prosecution rosecution", "an itnesses."). This is the "drawn twice" trait named for the 2016 to 2022 files.

---

## 2014-07-28 -> 2016-09-10

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 7 (old) / 7 (new)
- Hunk: modified body "misuse of power by our political leaders" -> "misuse of authority by our political leaders" and "Om Prakash Valmiki" -> "Omprakash Valmiki" (two places)
- Images: old page reads "misuse of power" and "Om Prakash", new page reads "misuse of authority" and "Omprakash". The comic strip and the layout are the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 10 (old) / 10 (new)
- Hunk: modified body "QNow let us try and understand the ways" -> "Now let us try and understand the ways"
- Images: both pages show the large grey "Q" watermark inside the recap table above the paragraph. The paragraph itself starts with "Now" on both pages.
- Verdict: extraction fault (rule)
- Fix: Rule A. The "Q" is in the 2014 text only.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 11 (old) / 11 (new)
- Hunk: modified body "emphasing" -> "emphasising", modified caption "Dr Babasaheb Ambedkar is known as the Father" -> "Baba Saheb Dr Ambedkar is known as the Father"
- Images: old page prints "emphasing" (a spelling slip in the 2014 printing) and "Dr Babasaheb Ambedkar". New page prints "emphasising" and "Baba Saheb Dr Ambedkar".
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 13 (old) / 13 (new)
- Hunk: modified body "three organs of the State" -> "three organs of government" (and two more "the State" -> "government" in the same section), deleted caption "The above photo shows members of the Constituent Assembly deep in discussion."
- Images: old page says "organs of the State" three times and has the extra sentence under the photo. New page says "organs of government" and the caption ends after "government as a whole."
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 14 (old) / 14 (new)
- Hunk: deleted table "- If a 13-year old child is working ..." and three more bullet lines, inserted table "Which Fundamental Rights will the following situations violate: - If a 13-year old child ..."
- Images: both pages show the same grey question box with four bullet lines and the heading above them. Only the last bullet changed: old "because she is a woman", new "for being a woman".
- Verdict: engine noise
- Fix: Rule D. Same lines read as four table hunks in 2014 and as one merged table hunk in 2016. The wording change of the last bullet is real.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 14 (old) / 14 (new)
- Hunk: modified caption "3. Right against Exploitation: The Constitution prohibits trafficking, forced labour, and children working under 14 years of age." -> "... prohibits human trafficking, forced labour, and employment of children under 14 years of age."
- Images: the grey box on the page shows the 2014 wording on the old page and the 2016 wording on the new page.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 15 (old) / 15 (new)
- Hunk: modified body "Indian Constitution has been changed over the years" -> "has been amended over the years", inserted body "Illustrate each of the 11 Fundamental Duties with drawings, pictures, poems or songs ...", modified caption "The above photos show various members signing a copy" -> "... members of the Constituent Assembly signing a copy ... on 24 January 1950."
- Images: old page has the word "changed" and ends after the grey question about fundamental duties. New page has "amended", the extra line "Illustrate each of the 11 Fundamental Duties ..." and the longer photo caption.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 16 (old) / 16 (new)
- Hunk: modified exercises "Article 35: Executive Power: The executive The executive power power of the kingdom of Nepal shall be to this Constitution ..." -> "Article 35 ... Article 37: Executive Power: ...", deleted "The executive functions of Nepal shall be taken in the name of the Prime Minister."
- Images: old table has the 1990 text "exercised exclusively by His Majesty" and the 2007 text with two paragraphs. New table has "vested in His Majesty and the Council of Ministers" and "Article 37" with one paragraph.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 1, printed page 17 (old) / 17 (new)
- Hunk: modified glossary "Trafficking: The practice of the illegal buying and selling" -> "Human Trafficking: The practice ...", inserted exercises "Note: Telangana became the 29th State of India on the 2nd June, 2014 ..."
- Images: old glossary has "Trafficking", new has "Human Trafficking". The new page has the Telangana note under the map and the old page has none.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 2, printed page 20 (old) / 20 (new)
- Hunk: modified caption "Ashita Jain, V, Srijan School, Delhi." -> "Akshita Jain, V, Srijan School, Delhi."
- Images: the small credit under the drawing reads "Ashita Jain" on the old page and "Akshita Jain" on the new page. Body text of the page is the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 3, printed page 35 (old) / 35 (new)
- Hunk: deleted body 19 lines "Bharatiya Janta Party (BJP) 2", "Indian National Congress (INC) 404", ... "Grand Total 514", inserted body "Bharatiya Janata Party (BJP) 282 Communist Party of India (CPI) 1 ... Grand Total 543", modified table "Results of 8th Lok Sabha elections (1984)" -> "Results of the 16th Lok Sabha Elections, (May 2014)"
- Images: old page shows the 8th Lok Sabha (1984) table with 514 seats, new page shows the 16th Lok Sabha (May 2014) table with 543 seats. The questions beside the table are the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: deleted caption 25 rows "National Parties Bharatiya Janata Party (BJP) 182", "Bahujan Samaj Party (BSP) 14", ..., modified caption "Results of 13th Lok Sabha elections" -> "Results of the 15th Lok Sabha Elections,", "the BJP got a large number of seats" -> "the INC got ...", "National Democratic Alliance (NDA)" -> "United Progressive Alliance (UPA)"
- Images: old page has the 13th Lok Sabha (1999) table and the note about the BJP and the NDA. New page has the 15th Lok Sabha (May 2009) table with the INC and the UPA.
- Verdict: real change
- Fix: none. The 25 one-row deletions are the table cells of the old table and carry no separate information.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 3, printed page 39 (old) / 39 (new)
- Hunk: modified table "1st 1951-52 44.87" -> "1st 1951-52 61.16", "4th 1967 61.04" -> "61.33", "5th 1971 55.27" -> "55.29", "14th 2004 58.07" -> "57.98", "8th 1984 63.56" -> "8th 1984-85 64.01", "10th 1991 56.73" -> "10th 1991-92 55.88", inserted "15th 2009 58.19" and "16th 2014 66.40"
- Images: old table lists 7 elections (to 2004), new table lists 10 elections (to 2014) with the revised figures. Both prints were read digit by digit from the images.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 5, printed page 56 (old) / 56 (new)
- Hunk: modified body "QImagine a situation in which a powerful politician" -> "Imagine a situation ..." and modified caption "Dispute between centre and the state" -> "QDispute between centre and the state"
- Images: the grey "Q" watermark is inside the table above the heading on both pages. The paragraph on the page starts with "Imagine" on both. The 2016 page is set in the heavy face.
- Verdict: extraction fault (rule)
- Fix: Rule A. "QImagine" is in 2014, "QDispute" is in 2016.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 5, printed page 60 (old) / 60 (new)
- Hunk: deleted table "1. Deals with conduct or acts that the Deals with any harm or injury ..." and "3. If found guilty, the accused can be sent ...", inserted body of the same text, modified caption "Description of Violation Branch of Law Procedure to be Followed QA group of girls"
- Images: both pages show the same criminal law versus civil law table and the same fill-in table below it. Nothing differs in the content.
- Verdict: engine noise
- Fix: Rule D and Rule A. The same table cells are in the table stream in 2014 and in the body stream in 2016, and the "Q" of the fill-in table is glued to the first row in 2016.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 5, printed page 63 (old) / 63 (new)
- Hunk: modified body "In a speech made on 26 November 2007" -> "In a speech made on 26 November 2014", inserted body "Number of Judges in India", "No.* Name of the Court ... A Supreme Court 31 28 3", "B High Courts 984 635 349", "C District and 19,421 15,039?", inserted note "Calculate the number of vacancies in the district and subordinate courts."
- Images: old page has only the quotation box. New page has the quotation box with the date 2014 and, below it, the new "Number of Judges in India" table with a "?" in the last cell and the new question in the margin.
- Verdict: real change
- Fix: none

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 67 (old) / 67 (new)
- Hunk: modified caption "He screams at Shanti Shanti Hembram has been working in the house for Saab, my brother and I ..." -> "Saab, my brother and I ...", inserted body "He screams at Shanti saying that this is the money she’s got from selling the chain." and "Shanti Hembram has been working in the house for the past three years.", inserted table "I plead not guilty. And I claim trial."
- Images: both pages carry the same comic strip with the same speech bubbles and the same lines of narration. The sentence "Mr Shinde searches Shanti’s trunk ... He screams at Shanti" is cut in the middle in the old extraction and whole in the new. There is a big "Po" sign in the art of the last panel.
- Verdict: engine noise
- Fix: Rule D. Narration and bubbles are in a different order and stream. See also Rule A for "Po".

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 68 (old) / 68 (new)
- Hunk: modified caption "Mr Shinde returns with Sub Inspector Rao." -> "PoMr Shinde returns with Sub Inspector Rao."
- Images: both pages show the same panel with the caption "Mr Shinde returns with Sub Inspector Rao." The letters "Po" belong to the police sign drawn in the artwork.
- Verdict: extraction fault (rule)
- Fix: Rule A.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 70 (old) / 70 (new)
- Hunk: modified body "PoFrom the above incident, you can see that the four key players" -> "From the above incident ...", modified caption "As the trial is nearing completion, Sushil learns ..." -> "14.5.07 As the trial is nearing completion ...", deleted caption "14.5.07"
- Images: both pages are identical in content. The date "14.5.07" is above the panel text on both pages. The 2016 body paragraph is set in the heavy face.
- Verdict: extraction fault (rule)
- Fix: Rule A for "Po" and Rule D for the date that moves between the caption and its own stream.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 73 (old) / 73 (new)
- Hunk: modified body "What if the court did not give a copy of the chargesheet and statements of witnesses to Shanti?" -> "What if the court did not give a copy of the chargesheet and What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?"
- Images: both pages are the same. The grey side question "What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?" sits in the margin and the paragraph runs on to the next page with "statements of witnesses to Shanti?".
- Verdict: extraction fault (one-off)
- Fix: Rule C. Ready-to-paste override for the 2016 text:
  ```
  - snapshot: "2016-09-10"
    chapter: 6
    find: "What if the court did not give a copy of the chargesheet and What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?"
    replace: "What if the court did not give a copy of the chargesheet and\n\n> [caption] What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?"
    note: "the grey side question of page 73 was written into the sentence that runs over to page 74, the page images of 2014 and 2016 are identical"
  ```

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 74 (old) / 74 (new)
- Hunk: modified body "cross-examine all the prosecution witnesses." -> "cross-examine all the prosecution rosecution witnesses.", inserted body "Advocate Roy was given an itnesses.", inserted body "statements of witnesses to Shanti?"
- Images: the 2016 paragraph is in the heavy face and reads "opportunity to cross-examine all the prosecution witnesses. Advocate Roy was given an opportunity to present witnesses in Shanti’s defence." There is no "rosecution" and no "itnesses." on the page. The 2014 page has the same words in the light face.
- Verdict: extraction fault (one-off)
- Fix: Rule H. Ready-to-paste override:
  ```
  - snapshot: "2016-09-10"
    chapter: 6
    find: "all the prosecution rosecution witnesses. Advocate Roy was given an itnesses. Advocate Roy was given an opportunity to present witnesses"
    replace: "all the prosecution witnesses. Advocate Roy was given an opportunity to present witnesses"
    note: "heavy face drawn twice on page 74 repeated and lost letters, page image shows the plain sentence"
  ```

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 6, printed page 75 (old) / 75 (new)
- Hunk: deleted table "a. If she were not defended by a lawyer. b. If the court had not assumed her to be innocent.", deleted body "Qa.", "Open Court: b.", modified table "a. Open Court: b. Basis of Evidence: c. ..." -> "Basis of Evidence: c. ..."
- Images: both pages show the same grey box with "a. Open Court: b. Basis of Evidence: c. Cross-examination of Prosecution Witnesses:" and the two discussion lines "a. If she were not defended by a lawyer. b. If the court had not assumed her to be innocent." The "Q" watermark is in the box.
- Verdict: engine noise
- Fix: Rule D with Rule A. The lines are split in a different order and the "Q" is attached to "a." in the 2016 text.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 82 (old) / 82 (new)
- Hunk: deleted caption "I never saw most of my friends again.", "After a few years your father got a job in Delhi and we all moved here.", "The money hardly lasted in the city.", "We had no means of livelihood anymore." and inserted table "The money hardly lasted in the city. We had no means of livelihood anymore. We were all cramped into a tiny rented room. ..."
- Images: both pages carry the same comic strip with the same lines. Only the order and the stream of the lines differ. The text of the bubbles is identical.
- Verdict: engine noise
- Fix: Rule D.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 83 (old) / 83 (new)
- Hunk: deleted caption "Explain at least three different reasons why groups may be marginalised.", modified body "influenced dominant religions of the empires around them, for example, the Jagannath cult of Orissa ..." -> "... around them," and inserted body "for example, the Jagannath cult of Orissa and Shakti and Tantric traditions in Bengal and Assam." on the next page
- Images: both pages are the same. The sentence goes on to the next page in both printings. The side question sits on page 83 in the margin.
- Verdict: extraction fault (rule)
- Fix: Rule C. The 2016 text keeps the sentence whole across the break and the 2014 text has the side question inside it.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 85 (old) / 85 (new)
- Hunk: deleted caption "Come Mini, let’s go to Assam", "Our country has so much suffering", "The country of Assam, oh Mini", "Has tea gardens full of greenery...", modified caption "Jharkhand Movement: Ethnicity and Culture of Silence What metals are important in present-day India?" -> "Jharkhand Movement: Ethnicity and Culture of Silence"
- Images: both pages carry the poem in the grey box and the same source line. The side question "What metals are important in present-day India? Why? ..." is in the margin on both pages.
- Verdict: engine noise
- Fix: Rule D. The first lines of the poem are a separate caption in 2014 and part of the body in 2016. One sentence of the box differs in fact: the 2016 box adds "and death" after "heartbreak".

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 86 (old) / 87 (new)
- Hunk: modified body "They, thus, get caught in a cycle of poverty and deprivation." -> "in a cycle of poverty and deprivation.", modified caption "They, thus, get caught Adivasis use around 10,000 plant species ..."
- Images: old and new page 86 both end with "They, thus, get caught", and page 87 begins "in a cycle of poverty and deprivation." in both. The grey box with the plant species is in the margin of page 86.
- Verdict: extraction fault (rule)
- Fix: Rule C. The words at the end of page 86 are glued to the box text in 2016 and to the page 87 line in 2014.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 88 (old) / 88 (new)
- Hunk: deleted body "Kutcha houses: 63.6% of Muslims live in kutcha houses ..." (old), modified body "Muslims are 13.4 per cent of India’s population" -> "According to 2001 census, Muslims are 13.4 per cent ...", inserted heading "Kutcha houses: 63.6% ...", "Electricity: 30% ...", "Piped water: 19.4% ..."
- Images: both pages carry the same table "Basic Amenities, 1994" with the same numbers. The new page has "According to 2001 census," at the start of the sentence. The table sits in the heading stream in 2016 and in the body stream in 2014.
- Verdict: real change
- Fix: none for the added words. The moved table is engine noise under Rule D.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 7, printed page 89 (old) / 89 (new)
- Hunk: inserted heading "All Hindus Muslims Christians Sikhs Buddhists Jains", "65% 65% 59% 80% 70% 73% 94%", modified table "III. Public Employment of Muslims (percentages)" -> "Public Employment of Muslims (percentages)"
- Images: both pages hold the literacy table with the figures 65%, 65%, 59%, 80%, 70%, 73%, 94% and the employment table. The Roman numerals "I.", "II.", "III." are in the box heading on both pages.
- Verdict: engine noise
- Fix: Rule D. The figures are the same and only the stream differs, with the numerals split off in 2016.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 8, printed page 98 (old) / 98 (new)
- Hunk: modified body "specific laws that guard against the discrimination and explitation of marginalised communities" -> "... discrimination and exploitation ...", deleted body "Those from Rathnam’s own caste were fearful of angering the powerful." (note inserted)
- Images: the old page prints "explitation" (a slip in the 2014 printing) and the new page prints "exploitation". The sentence about Rathnam’s caste is in the body in both pages.
- Verdict: real change
- Fix: none for the spelling. The sentence that moves between body and note is engine noise under Rule D.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 8, printed page 99 (old) / 99 (new)
- Hunk: deleted caption "Why do you think tahe Dalit families were afraid of angering the powerful castes?" and modified body "Why do you think the Dalit families ..." / "The Scheduled Castes and the Scheduled Tribes (Prevention of Atrocities) Act, 1989"
- Images: old margin question reads "tahe Dalit families", new margin question reads "the Dalit families". The sub-heading "The Scheduled Castes and the Scheduled Tribes (Prevention of Atrocities) Act, 1989" is on both pages.
- Verdict: real change
- Fix: none for the typo repair. The moved heading and question are engine noise under Rule D.

### social-political-life-3 2014-07-28 -> 2016-09-10, chapter 8, printed page 102 (old) / 102 (new)
- Hunk: modified body "The central government passed the Scheduled Tribes and Other Traditional Forest Dwellers (Recognition of Forest Rights) Act, 2006." (caption deleted)
- Images: the photo caption under the picture is the same on both pages.
- Verdict: engine noise
- Fix: Rule D. The caption is in the body stream in 2016 and the caption stream in 2014.

---

## 2016-09-10 -> 2019-05-04

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 1, printed page 6 (old) / 6 (new)
- Hunk: modified body "Until quite recently, Nepal was a monarchy." -> "Until recently ...", "Now the people have to write a new Constitution" -> "The people had to write", "the people of Nepal are in the process of writing a new Constitution" -> "adopted a new Constitution for the country in 2015", deleted caption "In 2007, Nepal adopted an interim Constitution.", inserted caption "In 2008, Nepal became a democracy after abolishing the monarchy."
- Images: old page is written in the present tense with the 2007 interim Constitution. New page has the past tense, 2015 and 2008 in the caption.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 1, printed page 16 (old) / 16 (new)
- Hunk: modified exercises "2007 Interim Constitution Part 5: Executive" -> "2015 Constitution of Nepal Part 7: Federal Executive", deleted "Keeping this in mind, why do you think Nepal needs a new Constitution today?", inserted exercises "Ministers."
- Images: the table on the old page has the 2007 Interim Constitution and the new page has the 2015 Constitution of Nepal with Article 75 and the shorter wording "pursuant to this Constitution and law". The old page also has the sentence "Keeping this in mind, why do you think Nepal needs a new Constitution today?" and the new page has dropped it.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 1, printed page 17 (old) / 17 (new)
- Hunk: deleted exercises "6. Colour in the following countries in this map:", "(a) Colour India in red.", "(b) Colour Nepal in green.", modified "(c) Colour Bangladesh in yellow." -> "(a) Bangladesh", inserted "6. Write down the names of the Indian States, which share borders with the following neighbouring nations:", deleted "Note: Telangana became the 29th State of India ..."
- Images: old page has the colouring task and the Telangana note. New page asks for the names of the Indian States bordering Bangladesh, Bhutan and Nepal with a new map and no Telangana note. The glossary is the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 3, printed page 38 (old) / 38 (new)
- Hunk: deleted caption "UNSTARRED QUESTION NO 2007 ANSWERED ON 30.11.2007 JUNK FOOD IN SCHOOLS 2007.", deleted table "(a) and (b) No, Sir. A letter was issued to the States ...", inserted table "Converge of Schemes for Children", "Manoj Rajoria", "Unstarred Question No: 48 Answered On: 15.12.2017", inserted body "(a) to (c) The Ministry has developed the National Plan of Action for Children 2016 ..."
- Images: the old page quotes a 2007 question on junk food in schools. The new page quotes a 2017 question on convergence of schemes for children. The margin questions and the paragraph below are the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 3, printed page 40 (old) / 40 (new)
- Hunk: modified body "today it is just above nine per cent" -> "today it is just above eleven per cent"
- Images: the sentence on the old page reads "nine per cent" and on the new page "eleven per cent".
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 5, printed page 56 (old) / 56 (new)
- Hunk: modified body "Imagine a situation in which a powerful politician" -> "QImagine a situation ...", modified body "QDispute between centre and the state" -> "Dispute between centre and the state"
- Images: the "Q" watermark is in the table above on both pages. The old page body is in the heavy face, the new in the normal face.
- Verdict: extraction fault (rule)
- Fix: Rule A.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 5, printed page 58 (old) / 58 (new)
- Hunk: modified caption "Currently there are 24 High Courts." -> "Currently there are 25 High Courts.", "Andhra Pradesh and Telangana have a common High Court at Hyderabad." -> "Andhra Pradesh (Amaravati) and Telangana (Hyderabad) have separate High Courts from 1 January 2019.", deleted captions "High Court of Patna" and "High Court of Karnataka", inserted caption "High Court of Patna http://patnahighcourt.gov.in High Court of Karnataka http://karnatakajudiciary.kar.nic.in", modified "High Court of Madras" -> "High Court of Madras http://www.hcmadras.tn.nic.in"
- Images: old page has no web addresses under the photos and the old caption text. New page has the addresses and the new caption text.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 5, printed page 59 (old) / 59 (new)
- Hunk: deleted caption "Alongside is a photograph of the District Court in Raipur, Chhattisgarh.", inserted caption "District Courts Complex in Namchi, South Sikkim http://districtcourtsnamchi.nic.in Aizawl (Mizoram) Bench of the Gauhati High Court http://ghcazlbench.nic.in Write two sentences ..."
- Images: old page has the Raipur court photograph with its sentence. New page has a Namchi photograph and an Aizawl photograph with the new captions and no Raipur sentence.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 5, printed page 61 (old) / 61 (new)
- Hunk: modified body "In principle, all citizens of India can access the courts in this country." -> "QIn principle, all citizens ..."
- Images: neither page shows a "Q" near the paragraph. The paragraph begins "In principle" on both pages.
- Verdict: extraction fault (rule)
- Fix: Rule A. The "Q" in the 2019 text comes from the Q box of the previous page.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 5, printed page 63 (old) / 63 (new)
- Hunk: deleted body "In a speech made on 26 November 2014, the Chief Justice of India K.G. Balakrishnan noted that ...", modified body "B High Courts 984 635 349" -> "B High Courts 1,079 645 434", "* Data in A and B (as on 1 November 2014) C (as on 31 December 2013)" -> "(as on 1 November 2018) C (as on 30 September 2018)", deleted note "Calculate the number of vacancies in the district and subordinate courts."
- Images: old page has the quotation box, the table with the question mark and the older data. New page has no quotation, the table with full numbers (31 28 3, 1,079 645 434, 22,644 17,509 5,135) and the new footnote. The photo caption adds "Finally, the Delhi High Court convicted the accused persons on 31 October 2018."
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 6, printed page 70 (old) / 70 (new)
- Hunk: modified body "From the above incident, you can see ..." -> "PoFrom the above incident, you can see ...", modified body "As stated at the beginning of this chapter, it is not the job You read in Unit 2 about the rule of law" -> "You read in Unit 2 about the rule of law ..."
- Images: both pages carry the same paragraphs, the sub-heading "What is the Role of the Police in Investigating a Crime?" and the same comic panels. No "Po" letters are on the text area.
- Verdict: extraction fault (rule)
- Fix: Rule A and Rule C. The 2016 text splits the sentence "it is not the job of the police ..." across the sub-heading and the next page, the 2019 text is whole.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 6, printed page 72 (old) / 72 (new)
- Hunk: deleted body "a) When Shanti was arrested for theft, S.I.", "Rao also kept her brother Sushil in the police lock up for two days.", ... "Qb) Did S.I.", modified body "2. Now let us take a slightly different scenario." -> "Now let us take a slightly different scenario.", inserted body "Q2.", inserted table "a) When Shanti was arrested for theft, S.I. Rao also kept her brother ..."
- Images: both pages show the same grey box with questions 1 (a and b) and 2. The "Q" watermark is in the box.
- Verdict: engine noise
- Fix: Rule D with Rule A. The questions are split into body sentences in 2016 and into a table block in 2019, and the "Q" jumps from "b)" to "2.".

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 6, printed page 73 (old) / 73 (new)
- Hunk: modified body "What if the court did not give a copy of the chargesheet and What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?" -> "What if the court did not give a copy of the chargesheet and statements of witnesses to Shanti? ..."
- Images: both pages are identical. The side question is in the margin on both.
- Verdict: extraction fault (one-off)
- Fix: see the override given under the 2014 -> 2016 entry for page 73. Rule C. The 2019 text is correct.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 6, printed page 75 (old) / 75 (new)
- Hunk: deleted body "All of the processes, written in bold on page 74, are crucial to a fair trial.", "Qa.", "Open Court: b.", modified body "Basis of Evidence: c. ..." -> "a. Open Court: b. Basis of Evidence: c. ..."
- Images: both pages show the same box with the same text "a. Open Court: b. Basis of Evidence: c. Cross-examination of Prosecution Witnesses:". The "Q" watermark is in the box.
- Verdict: extraction fault (rule)
- Fix: Rule A. Also Rule D for the box paragraph that is split in 2016.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 7, printed page 83 (old) / 83 (new)
- Hunk: modified body "in Orissa" -> "in Odisha" in six places (the narrative, the question "Why was Dadu forced to leave his village in Odisha?" and the caption "Niyamgiri Hill ... Kalahandi district of Odisha")
- Images: the old page prints "Orissa" and the new page prints "Odisha" in each place.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 7, printed page 86 (old) / 86 (new)
- Hunk: modified body "India has 54 national parks and 372 wildlife sanctuaries covering 1,09,652 sq km." -> "India has 104 national parks covering 40,501 sq km and 543 wildlife sanctuaries covering 1,18,918 sq km.", "militarised and war-torn." -> "militarised."
- Images: the old page has "54 national parks", "372 wildlife sanctuaries" and "war-torn". The new page has the new figures and no "war-torn".
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 7, printed page 88 (old) / 88 (new)
- Hunk: deleted body "Basic Amenities, 1994", "Kutcha houses: 63.6% of Muslims live in kutcha houses ...", inserted body "Religious Community Pucca House Electricity Tap Water Hindu 65.4 75.2 43.7", "Muslim 63.8 67.5 35.8", "Christian 69.3 86.2 48.0", "Sikh 91.3 96.0 49.3", inserted table "I. Access to Basic Amenities, 2008–2009", modified caption "Source: Abusaleh Shariff (1999) ..." -> "Source: India Human Development Report 2011 ..."
- Images: the old page has the 1994 table with Kutcha houses, Electricity and Piped water. The new page has the 2008-2009 table with the figures above, a different source and a different question below it.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 7, printed page 89 (old) / 89 (new)
- Hunk: deleted heading "65% 65% 59% 80% 70% 73% 94%", modified heading "All Hindus Muslims Christians Sikhs Buddhists Jains" -> "... 74 63 57 74 67 71 86", modified body "Literacy Rate by Religion, 2001" -> "II. Literacy Rate by Religion, 2011 (percentages)", "Source: Census of India 2001" -> "2011", inserted table "Which of these communities have the highest and the lowest literacy rate?"
- Images: old page lists 65 65 59 80 70 73 94 for 2001, new page lists 74 63 57 74 67 71 86 for 2011 with the new question.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 8, printed page 96 (old) / 96 (new)
- Hunk: deleted heading "Promoting Social Justice", deleted body "This is the glory of God, Defilement exists within.", inserted caption "This is the glory of God," and "Defilement exists within."
- Images: both pages show the same heading, the same intro paragraph and the same picture with its two lines of text.
- Verdict: engine noise
- Fix: Rule D. The heading is written into the note in 2019 and the picture words are split into captions.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 8, printed page 101 (old) / 101 (new)
- Hunk: modified body "there are 13 lakh persons from Dalit communities ... in the 96 lakh private and community dry latrines" -> "there are one lakh persons ... in the 26 lakh ...", "Rs 30-40 per day" -> "₹ 200 per day", inserted body "The Prohibition of Employment as Manual Scavengers and their Rehabilitation Act came into force on 6 December 2013."
- Images: old page prints "13 lakh", "96 lakh" and "Rs 30-40". New page prints "one lakh", "26 lakh" and "₹ 200" and adds the 2013 Act sentence at the end of the box.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 9, printed page 111 (old) / 111 (new)
- Hunk: inserted caption 22 one-word labels "Central Government Spends Money on", "Pensions", "5 p.", "States’ share of taxes & duties", "24 p.", ... "Source: Union Budget 2018-19"
- Images: the old page has a photograph of a polio vaccination with its caption in the place of the chart. The new page has the pie chart "Central Government Spends Money on Rupee Goes To" with the labels.
- Verdict: real change
- Fix: none for the chart itself. The 22 fragments are Rule E.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 9, printed page 112 (old) / 112 (new)
- Hunk: inserted caption "Tax Revenue of Central Government", "Rupee Comes From", "Non-debt Capital Receipts", "Customs", "3 p.", "4 p.", "Goods and Service Tax (GST)", "& Other Taxes", "23 p. Non-Tax Revenue", ... "16 p."
- Images: the new page has the second pie chart "Tax Revenue of Central Government Rupee Comes From" and the old page has none.
- Verdict: real change
- Fix: Rule E for the fragments.

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 9, printed page 116 (old) / 116 (new)
- Hunk: modified body "Official figures for 2001 show that 68 percent of the households ... about 36 percent have access to sanitation" -> "for 2011 show that 87 percent ... about 53 percent", "working for three decades" -> "working for nearly five decades", "more than 7,500 public toilet blocks and 1.2 million private toilets, giving access to sanitation to 10 million people" -> "more than 8,500 community toilet blocks and 1.5 million household toilets ... 20 million people", "Re 1" -> "₹2"
- Images: the old page prints the 2001 figures and the new page the 2011 figures and the revised numbers.
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 10, printed page 123 (old) / 123 (new)
- Hunk: modified caption "According to the 2001 census, over 12 million children ..." -> "According to the 2011 census, over 4 million children ...", deleted captions "In October 2006, the government amended the Child Labour Prevention Act ...", "To date, only three state governments ...", inserted caption "In 2016, Parliament amended the Child Labour (Prohibition and Regulation) Act, 1986 ...", "An online portal, https://pencil.gov.in ..."
- Images: the long photo caption has the old 2006 text on the old page and the new 2016 text with the PENCIL portal on the new page. The main paragraphs are the same apart from "shall be employed to work in any factory or mines or engaged in any other hazardous employment."
- Verdict: real change
- Fix: none

### social-political-life-3 2016-09-10 -> 2019-05-04, chapter 10, printed page 134 (old) / 134 (new)
- Hunk: deleted references "Accessed on", modified "Democracy in Nepal http://www.himalmag.com Accessed on 15 December 2008." -> "Democracy in Nepal, http://www.himalmag.com (Accessed on 15 December 2007)", "NEWSPAPER ARTICLES" -> "ARTICLES", inserted entries "Election Commission of India", "HARI PHUYAL ... The Diplomat", "Lok Sabha", "Paschim Banga Khet Mazdoor Samiti vs. State of West Bengal (1996)"
- Images: the new page lists the added references and the old page lacks them. The year of access for the Nepal site is 2008 on the old page and 2007 on the new page.
- Verdict: real change
- Fix: none

---

## 2019-05-04 -> 2020-06-16

### social-political-life-3 2019-05-04 -> 2020-06-16, chapter 3, printed page 35 (old) / 35 (new)
- Hunk: deleted body 4 blocks "Political Party No. of MPs", "National Parties", "Bharatiya Janata Party (BJP) 282 Communist Party of India (CPI) 1 ...", "Grand Total 543", modified table "Results of the 16th Lok Sabha Elections, (May 2014)" -> "Results of the 17th Lok Sabha Elections, (May 2019)"
- Images: old page has the 16th Lok Sabha table (BJP 282). New page has the 17th Lok Sabha table (BJP 303, INC 52, DMK 24 and so on) and a different source line.
- Verdict: real change
- Fix: none

### social-political-life-3 2019-05-04 -> 2020-06-16, chapter 3, printed page 35 (old) / 35 (new)
- Hunk: deleted caption "Source: http://.eci.nic.in", inserted caption "Political Party No. of MPs Bharatiya Janata Party (BJP) 303 ...", "4 Nationalist Congress Party (NCP) 4 ..."
- Images: the old source line reads "http://.eci.nic.in" (a slip in the print) and the new line reads "http://loksabha.nic.in". The new table is the 17th Lok Sabha table.
- Verdict: real change
- Fix: none. The two inserted caption fragments are the table rows split into lines, which is Rule D.

### social-political-life-3 2019-05-04 -> 2020-06-16, chapter 3, printed page 39 (old) / 39 (new)
- Hunk: inserted table "17th 2019 67.11"
- Images: old table ends with the 16th Lok Sabha (2014, 66.40). The new table has an extra last row "17th 2019 67.11". The rest is the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2019-05-04 -> 2020-06-16, chapter 4, printed page 45 (old) / 45 (new)
- Hunk: modified body "Domestic violence refers to the injury or harm" -> "Domestic violence generally refers to the injury or harm"
- Images: the grey box on the old page reads "Domestic violence refers to" and the new page reads "Domestic violence generally refers to".
- Verdict: real change
- Fix: none

### social-political-life-3 2019-05-04 -> 2020-06-16, chapter 5, printed page 63 (old) / 63 (new)
- Hunk: modified body "A Supreme Court 31 28 3" -> "34 34 0", "B High Courts 1,079 645 434" -> "1,079 655 424", modified table "* Data in A and B (as on 1 November 2018) C (as on 30 September 2018)" -> "* Data in A and B (as on 1 November 2019)"
- Images: the table on the old page reads 31 28 3, 1,079 645 434 and 22,644 17,509 5,135. The new table reads 34 34 0, 1,079 655 424 and 22,644 17,509 5,135, with the footnote "as on 1 November 2019".
- Verdict: real change
- Fix: none

---

## 2020-06-16 -> 2021-08-14

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 1, printed page 14 (old) / 14 (new)
- Hunk: modified table "- If the government decides not to promote an officer of the armed forces for being a woman." -> "- If the government decides not to promote an officer of the"
- Images: both pages are identical. The last bullet runs on to a second line "armed forces for being a woman." on both.
- Verdict: extraction fault (rule)
- Fix: Rule B. The line "armed forces for being a woman." lies at 86.5 per cent of the page height in the 2021 PDF and is taken as a footer.

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 1, printed page 17 (old) / 17 (new)
- Hunk: deleted glossary "Tyranny: The cruel and unjust use of power or authority."
- Images: both pages show the Tyranny entry as the last glossary line.
- Verdict: extraction fault (rule)
- Fix: Rule B. The block lies at 86.9 per cent of the height in the 2021 PDF. The line is missing in the 2021, 2022, 2023 and 2024 texts and present in 2014 to 2020 as `> [table] Tyranny: The cruel and unjust use of power or authority.`

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: modified body "political parties that oppose the majority party/coalition formed" -> "political parties that are not part of the majority party/coalition formed"
- Images: the old page reads "that oppose the majority party/coalition" and the new page reads "that are not part of the majority party/coalition".
- Verdict: real change
- Fix: none

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 7, printed page 86 (old) / 86 (new)
- Hunk: modified body "India has 104 national parks covering 40,501 sq km and 543 wildlife sanctuaries covering 1,18,918 sq km." -> "India has 101 national parks covering 40,564 sq km and 543 wildlife sanctuaries covering 1,19,776 sq km."
- Images: the figures on the old page are 104, 40,501 and 1,18,918 and on the new page 101, 40,564 and 1,19,776.
- Verdict: real change
- Fix: none

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 9, printed page 111 (old) / 111 (new)
- Hunk: deleted caption "Scheme", "Central Sector Scheme", "Source: Union Budget 2018-19", "9 p.", "10 p."
- Images: both pages show the identical pie chart with the labels "Centrally Sponsored Scheme 9 p.", "Central Sector Scheme 10 p." and the source line under it.
- Verdict: extraction fault (rule)
- Fix: Rule B for "Central Sector Scheme" (at 86.7 per cent of the height in the 2021 PDF) and Rule E for the other fragments of the same label group.

### social-political-life-3 2020-06-16 -> 2021-08-14, chapter 10, printed page 134 (old) / 134 (new)
- Hunk: modified references "... Supreme Court of India, https://www.sci.gov.in Sustainable Development Goals (SDGs), www.in.undp.org" -> "... Supreme Court of India, https://www.sci.gov.in"
- Images: both pages list "Sustainable Development Goals (SDGs), www.in.undp.org" as the last website.
- Verdict: extraction fault (rule)
- Fix: Rule B. The line lies at 86.5 per cent of the page height in the 2021 PDF. The same line is missing in 2022, 2023 and 2024 (ch10/8).

---

## 2021-08-14 -> 2022-08-02

### social-political-life-3 2021-08-14 -> 2022-08-02, chapter 2, printed page 21 (old) / 21 (new)
- Hunk: modified body "1. that one religious community does not dominate another" -> "1.that one religious community does not dominate another", and the same for "2. that some members ..." and "3. that the State does not enforce ..."
- Images: both pages print the list as "1. that", "2. that", "3. that" with the usual space.
- Verdict: extraction fault (rule)
- Fix: Rule F. The 2022 text is the faulty one. The 2023 text has the space again.

### social-political-life-3 2021-08-14 -> 2022-08-02, chapter 8, printed page 97 (old) / 97 (new)
- Hunk: deleted table "List of schemes What is this How do you think it will help promote scheme about? social justice?", inserted table "Scholarships for students", "Special police stations", modified table "Special schemes for girls in government schools Q Scholarships for students Special police stations" -> "... Q List of schemes What is this ..."
- Images: both pages show the same table with the header "List of schemes, What is this scheme about?, How do you think it will help promote social justice?" and three rows (Scholarships for students, Special police stations, Special schemes for girls in government schools). No cell changed.
- Verdict: engine noise
- Fix: Rule D. The header row and the first rows are read in a different order.

### social-political-life-3 2021-08-14 -> 2022-08-02, chapter 9, printed page 114 and 115 (old) / 114 and 115 (new)
- Hunk: modified body "1. Throughout the world, water supply is a function of the government." -> "1.Throughout the world ...", and the same for items 2, 3 and 4 ("2.There", "3.In", "4.Within")
- Images: the lines of page 115 in both printings read "2. There are areas in the world", "3. In a few cases", "4. Within India" with a normal space after the number.
- Verdict: extraction fault (rule)
- Fix: Rule F.

---

## 2022-08-02 -> 2023-12-23-rationalised

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 1, printed page 7 (old) / 7 (new)
- Hunk: deleted body "Do you recall the chapter on the Dalit writer, Omprakash Valmiki’s experiences in school from your Class VII book?" and "In that chapter, we talked about the discrimination Omprakash faced because he was a Dalit."
- Images: the old paragraph has the two sentences about Omprakash Valmiki. The new paragraph goes straight from "Fundamental Rights." to "You read about how the Indian Constitution guarantees the right to equality".
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 2, printed page 21 (old) / 21 (new)
- Hunk: modified body "3.that the State does not enforce any particular religion" -> "3. that the State does not enforce ...", "2.that" -> "2. that", "1.that" -> "1. that"
- Images: both pages print "1. that ...", "2. that ...", "3. that ..." with the space.
- Verdict: extraction fault (rule)
- Fix: Rule F. The 2022 text is the faulty one.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3 (old 3, 4), printed page 30 (old) / 30 (new)
- Hunk: deleted heading "Why Do We Need a Parliament?" and inserted heading "Parliament and the Making of Laws"
- Images: the running title on the old page is "Chapter 3: Why Do We Need a Parliament?" and on the new page "Chapter 3: Parliament and the Making of Laws".
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 39 (old) / 39 (new)
- Hunk: deleted body 17 sentences from "C. Law-Making" and "Who are the People in Parliament?" to "This has been done so that the MPs elected from these constituencies will be familiar with and can represent Dalit and Adivasi interests in Parliament.", deleted table 11 rows "Lok Sabha Election Years Voter Turnout (%)", "1st 1951-52 61.16", ... "17th 2019 67.11"
- Images: the old page has the section "C. Law-Making", "Who are the People in Parliament?" and the voter turnout table. The new page begins "How Do New Laws Come About?" and has the SDG Goal 5 picture and the domestic violence box.
- Verdict: real change
- Fix: none. The section on the people in Parliament and the turnout table are gone from the book.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 40 (old) / 40 (new)
- Hunk: deleted body "Similarly, it has more recently been suggested that there should be reservation of seats for women." through "Discuss.", deleted glossary "The above photo shows a few women Members of Parliament."
- Images: the old page has the photo of women MPs, the text about women in Parliament and a three-word glossary (Approval, Coalition, Unresolved). The new page is the first page of the domestic violence storyboard.
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3 (old 4), printed page 46 (old) / 40 (new)
- Hunk: inserted caption 40 lines "October 2006", "Not just women.", "Violence-free homes will benefit everyone.", "Kusum, it’s taken such a long time to get this law passed." and so on (the storyboard of the domestic violence law)
- Images: old ch4 page 46 and new ch3 page 40 are the same comic page with the same bubbles.
- Verdict: engine noise
- Fix: Rule G. The storyboard of old ch4 is the storyboard of new ch3.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3 (old 4), printed page 42 and 43 (old) / 39 and 43 (new)
- Hunk: inserted body "How Do New Laws Come About?", "The Parliament has an important role in making laws.", "Let us now look at the situation where the Parliament passes laws that turn out to be very unpopular." and the other sentences of new ch3 pages 39, 42, 43, 44
- Images: the text of these pages is present in old ch4 (pages 42 to 50) and in new ch3. The new pages carry it unchanged apart from the page numbers (for example old p50 and new p44 have the same "We need to remember that our role as citizens does not end with electing our representatives").
- Verdict: engine noise
- Fix: Rule G.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3 (old 4), printed page 51 (old) / 44 and 45 (new)
- Hunk: inserted glossary "Criticise: To find fault with or disapprove of a person or thing.", "Evolution: Process of development ...", "Repressive: To control severely ...", "Sedition: This applies to anything ..."
- Images: the glossary on old ch4 page 51 has Criticise, Evolution, Sedition and Repressive and the new ch3 glossary on pages 44 and 45 has the same entries after Approval and Coalition. New page 45 has "Unresolved" after "Repressive" as on the old ch3 page.
- Verdict: engine noise
- Fix: Rule G.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3 (old 4), printed page 51 (old) / 45 (new)
- Hunk: inserted exercises "4. Re-read the storyboard on how a new law on domestic violence got passed." and "Describe in your own words the different ways in which women’s groups worked to make this happen."
- Images: the old exercise "3. Re-read the storyboard on how a new law on domestic violence got passed" becomes "4." at the end of the new ch3 exercises, which also hold the old ch3 questions 1 to 3 (vote, map, table). The question set differs from the old two chapters.
- Verdict: real change
- Fix: none for the renumbering of the exercises. The text itself is Rule G noise.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 3, printed page 35 (old) / 35 (new)
- Hunk: inserted table "d. Which party do you think will form the government? Give reasons why. Source: http://loksabha.nic.in", deleted caption "d.", "Which party do you think will form the government?", "Give reasons why."
- Images: both pages are the same. The 17th Lok Sabha table and the four questions a to d are in the same place.
- Verdict: engine noise
- Fix: Rule D.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 4 (old 5), printed page 55 (old) / 49 (new)
- Hunk: deleted body "For example, in the Class VII book, you read about Hakim Sheikh ..." and two more sentences (Article 21 and the Right to Health)
- Images: the old paragraph "Upholding the Law and Enforcing Fundamental Rights" runs on with the Hakim Sheikh example and ends with the 1996 citation. The new paragraph ends after "Fundamental Rights have been violated."
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 4 (old 5), printed page 63 (old) / 57 (new)
- Hunk: inserted body "C District and 22,644 17,509 5,135 Subordinate Courts", modified body "C District and 22,644 17,509 5,135 Subordinate Courts However, inspite of this ..." -> "(photo was taken at Press Club, Lucknow, 24 May 2007) However, inspite of this ..."
- Images: both pages show the same "Number of Judges in India" table (34 34 0, 1,079 655 424, 22,644 17,509 5,135) and the same caption and paragraph.
- Verdict: engine noise
- Fix: Rule D. The last table row is carried to a different place in the reading order.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 4 (old 5), printed page 58 (old) / 52 (new)
- Hunk: modified caption "High Court of Patna http://patnahighcourt.gov.in High Court of Karnataka http://karnatakajudiciary.kar.nic.in" -> "High Court of Patna http://patnahighcourt.gov.in"
- Images: both pages show the Patna and the Karnataka photographs, each with its web address below it.
- Verdict: extraction fault (rule)
- Fix: Rule B. The Karnataka caption lies at 86.1 per cent of the height in the 2023 PDF. The 2023 and 2024 texts need `> [caption] High Court of Patna http://patnahighcourt.gov.in High Court of Karnataka http://karnatakajudiciary.kar.nic.in` as the 2022 text has it.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 4 (old 5), printed page 53 (old) / 47 (new)
- Hunk: deleted teachers-note 7 sentences about Chapter 6 and the criminal justice system, modified "Chapter 5 covers topics" -> "Chapter 4 covers topics", "Before starting Chapter 5," -> "Before starting Chapter 4", "discussed in Chapter 5." -> "Chapter 4."
- Images: the old Teacher’s Note has the paragraph about the criminal justice chapter and "Chapter 5". The new note is one paragraph shorter and names Chapter 4.
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5 (old 7), printed page 89 and 90 (old) / 70 and 71 (new)
- Hunk: deleted body "Do you remember reading in your Class VII book about how the Ansaris were finding it difficult to rent a house?", deleted body and caption "I live in a Muslim-dominated area. Some days back during Ramzan ...", "Ainee A.", "Farooqi", "The above essay has been written by a child around your age. What do you think she is trying to convey?"
- Images: old page 90 has the sentence about the Ansaris, the grey essay box by Ainee A. Farooqi and the margin question. New page 71 goes from "treat them unfairly" straight to the paragraph "In the above section of this chapter".
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 5 (old 7), printed page 89 (old) / 70 (new)
- Hunk: typographic body "between the ages of 7-16 ... (page 56)" -> "7–16" (old 89, new 71)
- Images: the old page 89 prints "7-16" and the new page 71 prints "7–16" in the same sentence.
- Verdict: real change
- Fix: none. Classed as typographic and minor already.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 6 (old 8), printed page 97 (old) / 77 (new)
- Hunk: inserted table "List of schemes What is this ...", deleted table "Scholarships for students", "Special police stations", modified table "... Q List of schemes ..." -> "... Q Scholarships for students Special police stations"
- Images: both pages show the same table with the same three rows. The margin question ends with "?" on the old page and "." on the new page.
- Verdict: engine noise
- Fix: Rule D. The change of the question mark is a real but trivial change.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 7 (old 9), printed page 114 and 115 (old) / 94 and 95 (new)
- Hunk: modified body "1.Throughout the world ..." -> "1. Throughout ...", "2.There ..." -> "2. There ...", "3.In a few cases ..." -> "3. In a few cases ...", "4.Within India ..." -> "4. Within India ..."
- Images: the old page 115 prints "2. There", "3. In", "4. Within" with the usual space.
- Verdict: extraction fault (rule)
- Fix: Rule F.

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 8 (old 10), printed page 131 (old) / 111 (new)
- Hunk: modified exercises "How does it relate to the 2016 law that you read about on page 123?" -> "on page 103?"
- Images: the old page 131 reads "page 123" and the new page 111 reads "page 103".
- Verdict: real change
- Fix: none

### social-political-life-3 2022-08-02 -> 2023-12-23-rationalised, chapter 1, printed page 17 (old) / 17 (new)
- Hunk: none, the glossary entry "Tyranny: The cruel and unjust use of power or authority." and the last list line "armed forces for being a woman." are missing in both texts
- Images: both pages show both lines.
- Verdict: extraction fault (rule)
- Fix: Rule B. Missing in 2021, 2022, 2023 and 2024 and so not shown as a diff.

---

## 2023-12-23-rationalised -> 2024-05-24

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 2, printed page 25 (old) / 25 (new)
- Hunk: deleted caption "Can you think of a recent incident, from any part of India, in which the secular ideals of the Constitution were violated and persons were persecuted and killed because of their religious backgrounds?", inserted caption "Can you think of an example from India where individuals or communities of different faiths came together to promote social harmony and celebrate constitutional values?"
- Images: the margin question differs as written on the old page and the new page. The rest of the page is the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 3, printed page 34 (old) / 34 (new)
- Hunk: modified body "as shown in the map on page 41." -> "on page 45.", modified caption "Rajya Sabha ... total strength of 245 members" -> "250 members", "Lok Sabha ... total membership of 545" -> "543", deleted caption "3 2", inserted caption "3", "2"
- Images: the old page shows the old Parliament building and the old chambers. The new page shows the new Parliament building and its chambers, with "250" and "543" in the captions and "page 45" in the text. The small digits 2 and 3 are the picture numbers on the photos.
- Verdict: real change
- Fix: none for the wording. The digit captions "3 2" versus "3" and "2" are engine noise (Rule D).

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: modified body "Since there are 543 elected (plus 2 Anglo-Indian nominated) members in Lok Sabha" -> "Since there are 543 elected members in Lok Sabha"
- Images: the old page has "(plus 2 Anglo-Indian nominated)" and the new page has not.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 3, printed page 43 (old) / 43 (new)
- Hunk: modified caption "As you read in the earlier section on the rule of law, Indian nationalists protested ..." -> "As you have read in your previous class and will read in your history textbooks this year on the rule of law, ...", inserted caption "The above photo shows Rosa Parks seated in a bus."
- Images: the grey margin box differs as written and the new page has an extra last line about the photo.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 47 (old) / 47 (new)
- Hunk: deleted teachers-note "Before starting Chapter 4 it might be useful to reiterate the discussion on the ‘rule of law’ from the previous unit.", modified "through these chapters." -> "through this unit.", "This can then lead to a discussion on the role of the judiciary" -> "Chapter 4 discusses the role of the judiciary", moved "Five separate though inter-related concepts ..." to "... have been discussed in this Chapter."
- Images: the second paragraph of the Teacher’s Note is rewritten as the hunks say. The first sentence moves and is reworded.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 48 (old) / 48 (new)
- Hunk: modified body "As you have read in Unit 2, in India we have the rule of law." -> "In India we have the rule of law."
- Images: the sentence starts with "As you have read in Unit 2," on the old page and with "In India" on the new page.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 50 and 55 (old) / 50 and 55 (new)
- Hunk: none, "QImagine a situation" and "QIn principle, all citizens" appear in both texts
- Images: on page 50 the "Q" watermark sits inside the grey table above the heading and the paragraph itself starts with "Imagine" on both editions. Page 55 has no "Q" anywhere and the paragraph starts with "In principle" on both editions.
- Verdict: extraction fault (rule)
- Fix: Rule A. Same sites as in 2014 to 2022.

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 57 (old) / 57 (new)
- Hunk: modified body "C District and 22,644 17,509 5,135 Subordinate Courts" -> "C District and 25,042 19,192 5,850 Subordinate Courts", "B High Courts 1,079 655 424" -> "B High Courts 1,108 775 333", modified table "(as on 1 November 2019)" -> "(as on 19 Decenber 2022)"
- Images: old page shows 34 34 0 / 1,079 655 424 / 22,644 17,509 5,135 and the footnote "1 November 2019". New page shows 34 34 0 / 1,108 775 333 / 25,042 19,192 5,850. A crop at 250 dpi shows that the printed footnote reads "19 Decenber 2022", so the typo is in the book and not in the extraction.
- Verdict: real change
- Fix: none. Do not correct "Decenber".

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 59 (old) / 59 (new)
- Hunk: modified exercises "... relate to the photo essay on the Right to Food on page 61?" -> "on page 55?"
- Images: the old page reads "page 61" and the new page reads "page 55".
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 65 (old) / 65 (new)
- Hunk: modified body "Nagaland and Tripura" -> "Nagaland, Sikkim and Tripura", "range of tribal religions that are different from Islam, Hinduism and Christianity." -> "range of belief systems that are different from other religions."
- Images: the old page lists the north-eastern states without Sikkim and has "tribal religions ... Islam, Hinduism and Christianity". The new page adds Sikkim and has "belief systems ... other religions".
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 68 (old) / 68 (new)
- Hunk: modified body "India has 101 national parks covering 40,564 sq km and 543 wildlife sanctuaries covering 1,19,776 sq km." -> "As per the data provided by the Wildlife Institute of India (November, 2023), India has 106 national parks covering 44,402.9 sq km and 573 wildlife sanctuaries Covering 123,762.56 sq km."
- Images: old and new pages carry the sentence as written in the hunk, including the capital C of "Covering" in the 2024 print.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 70 (old) / 70 (new)
- Hunk: modified body "According to 2011 census, Muslims are 14.2 per cent of India’s population and are considered to be a marginalised community in India today because in comparison to other communities, they have over the years been deprived of the benefits of socio-economic development." -> "According to 2011 Census, Muslims are 14.2 percent of India's population and are considered to be a marginalized community because of their having comparatively lower status of socio-economic development.", modified table "I. Access to Basic Amenities, 2008–2009" -> "... (percentage)"
- Images: the old page and the new page differ as written, with the spellings "marginalised" and "marginalized". The table title has "(percentage)" on the new page.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 71 and 72 (old) / 71 and 72 (new)
- Hunk: deleted body "The report discusses in detail the marginalisation of this community.", modified "according to the Report the average years of schooling ... (page 56)." -> "according to page 56 of the Report ...", "It suggests that on a range" -> "The report discussed in detail the marginalisation of this community and suggested that on a range ... was comparable", "treat them unfairly, and discriminate" -> "treat them differently and discriminate", "leads to hatred and violence" -> "has also led to hatred", "there is a link" -> "there used to be a link", "redress this situation" -> "redress the situation", "marginalisation of Muslims" -> "marginalization of Muslims"
- Images: both pages differ in each of these places as the hunks say. The tables on page 71 are the same.
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 6, printed page 75 (old) / 75 (new)
- Hunk: modified body "(you learnt a lot about this in your Class VII textbook in the chapter On Equality)." -> "... in the chapter On Equality in Indian Democracy)."
- Images: the old page ends the bracket with "On Equality)." and the new page with "On Equality in Indian Democracy)."
- Verdict: real change
- Fix: none

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 7, printed page 91 and 92 (old) / 91 and 92 (new)
- Hunk: deleted caption 16 labels "5 p.", "24 p.", "8 p.", "Subsidies", "9 p.", "18 p.", "3 p.", "4 p.", "Goods and Service Tax (GST)" and others, modified caption "Source: Union Budget 2018-19" -> "Source: Union Budget 2024-25", "States’ share of taxes & duties" -> "Subsidies taxes & duties", inserted caption "(4%)", "(9%)", "(20%)", "(28%)", "(7%)", "Tax (17%)" and others
- Images: both charts are pie charts with the labels as the hunks say. The old charts give each share as "24 p." (paise in the rupee) and the new charts as percentages ("(20%)"), the sources are the 2018-19 and the 2024-25 Union Budgets, and the new charts have a rupee sign in the middle.
- Verdict: real change
- Fix: none for the chart itself. The 40 odd one-word hunks are Rule E. "Subsidies taxes & duties" in the extraction is two labels joined ("Subsidies" and "States’ share of taxes & duties").

### social-political-life-3 2023-12-23-rationalised -> 2024-05-24, chapter 7, printed page 97 (old) / 97 (new)
- Hunk: deleted caption "The Census of India, 2001 puts rural household electrification at 44 per cent, leaving around 78 million households still in the dark.", inserted caption "The rural household electrification stands at 96 percent in 2022." and "(Source: National Family Health Survey (NFHS–5), 2019–22)"
- Images: the photo caption of the tangled wires reads as the hunk says on the two pages.
- Verdict: real change
- Fix: none

---

## Summary

### Counts per verdict (entries above)

106 entries in all. Many entries cover several hunks of one page, so the hunks judged are well above 300.

| Verdict | Entries |
| --- | --- |
| real change | 65 |
| extraction fault (rule) | 21 |
| extraction fault (one-off) | 3 |
| engine noise | 17 |

Per pair (real / rule / one-off / noise):

| Pair | Real | Rule | One-off | Noise |
| --- | --- | --- | --- | --- |
| 2014-07-28 -> 2016-09-10 | 15 | 6 | 2 | 8 |
| 2016-09-10 -> 2019-05-04 | 18 | 4 | 1 | 2 |
| 2019-05-04 -> 2020-06-16 | 5 | 0 | 0 | 0 |
| 2020-06-16 -> 2021-08-14 | 2 | 4 | 0 | 0 |
| 2021-08-14 -> 2022-08-02 | 0 | 2 | 0 | 1 |
| 2022-08-02 -> 2023-12-23-rationalised | 10 | 4 | 0 | 6 |
| 2023-12-23-rationalised -> 2024-05-24 | 15 | 1 | 0 | 0 |

The one-off entries have ready overrides: 2016 ch6 page 73 (side question spliced into a sentence) and page 74 (doubled letters), both in the 2016-09-10 snapshot. The 2016 -> 2019 entry for page 73 points to the same override. The 2019 -> 2020, 2020 -> 2021 and 2021 -> 2022 pairs are small and mostly clean. The real changes there are the 17th Lok Sabha table, the court vacancy table, the Opposition definition and the national parks figures, and the faults are all rule faults (footer band and the glued list labels).

Not shown in any diff but wrong in the texts: the lines named under Rule B and the two Bhopal photo captions are missing from every edition from 2021 to 2024 (the captions from 2014), and the stray "Q" is present in every edition.

### The three patterns that would remove the most noise if fixed by a rule

1. Compare identical text across streams and reading order (Rule D), plus the chart label fragments (Rule E). Storyboard bubbles, table rows and box paragraphs come out as separate deleted and inserted hunks in different streams in nearly every pair. This is the bulk of the delete and insert pairs in 2014 to 2016 (ch1, ch5, ch6, ch7, ch8) and 2016 to 2019 (ch6, ch7, ch8, ch9 with about 44 pie-chart labels), and of the 40 label hunks of ch7 in 2023 to 2024. A cross-stream match by normalised word bag and one caption block per chart would class these as moved or restreamed.
2. Chapter pairing for merged chapters in the 2022 to 2023 pair (Rule G). About 170 of the 224 hunks of that pair sit in ch3 because old ch4 (and old ch3 pages) were merged into the new ch3 and the old ch4 is marked dropped. Matching a new chapter against two old chapters would leave only the real deletions (the people-in-Parliament section, the women MPs text, the Hakim Sheikh and Ainee Farooqi passages and the Teacher’s Note) and the new exercises.
3. Extraction rules A, B and F together. The stray "Q" and "Po" glyphs (Rule A) appear in ten places in every edition. The footer band at 86 per cent (Rule B) loses real lines from 2021 to 2024 (Tyranny, "armed forces for being a woman.", the SDG reference, the Karnataka caption, one pie label) and two Bhopal photo captions in every edition. The glued list labels of the 2022 file (Rule F) make seven false "modified" hunks. Fixing the footer test and the Q span filter in `extract.py` and the list label in `clean.py` removes these and also restores text that no diff can show because it is missing from every edition.
