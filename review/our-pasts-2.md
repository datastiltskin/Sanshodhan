# Review: our-pasts-2 (Our Pasts II, Class 7 history)

Reviewed from rendered page images of both editions of each pair (PDF pages at 85 dpi, old and new side by side). Printed page numbers are given as old / new. Where an entry covers a pattern seen in several places, the other places are listed in its Fix line.

## 2014-07-28 -> 2016-09-10

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 3 (old) / 3 (new)
- Hunk: modified heading "New and old terminologies" -> "New and Old Termi New and Old Terminologies nologies"
- Images: both pages show a clean one-line heading, "New and old terminologies" (old) and "New and Old Terminologies" (new). The garbled duplicate is not on the page, so it comes from a doubled text layer in the 2016 heading.
- Verdict: extraction fault (one-off)
- Fix: override
  - snapshot: "2016-09-10"
  - chapter: 1
  - find: "## New and Old Termi New and Old Terminologies nologies"
  - replace: "## New and Old Terminologies"
  - note: "doubled text layer in the 2016 heading on page 3, the page shows only 'New and Old Terminologies'"

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 4 (old) / 4 (new)
- Hunk: modified body "Through this period paper gradually became cheaper and more widely available." -> "Through this period paper gradually became cheaper and more The value of paper Compare the following:" with "widely available." inserted at the top of page 5; heading "The value of paper" deleted
- Images: both pages show the same body paragraph ending "cheaper and more" at the foot of the text column, then a purple box titled "The value of paper" (box title in a teal bar). The sentence continues on page 5 with "widely available." in both editions. The 2016 box content is bold, the 2014 box is plain, but the wording of the box is the same apart from the edits below.
- Verdict: extraction fault (rule)
- Fix: pattern is a boxed sidebar that interrupts a paragraph across a page break. The box title and the first line of the box ("Compare the following:") are glued onto the end of the interrupted sentence, so the continuation on the next page ("widely available.") becomes a separate inserted sentence. The 2014 text handled it correctly, so the rule is a 2016-layout case (box title in a coloured bar over bold text). The same glue of box title and first box line occurs in 2016 chapter 4 page 54 ("Nur Jahan's influence in Jahangir's court Mehrunnisa married ...", see below). A rule should treat a title bar in the box colour as a heading and keep the running sentence across the break.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 4 (old) / 4 (new)
- Hunk: modified note "He did not have enough paper." -> "But he did not have enough paper."
- Images: the box on page 4 reads "wanted to copy a book. He did not have enough paper." (old) and "... a book. But he did not have enough paper." (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 2 (old) / 2 (new)
- Hunk: deleted body "But look at the areas inland." and note "Are they as detailed as those on the coast?", inserted body "Look at the areas in the interior of the subcontinent on Map 2. Are they as detailed as those on the coast?"; modified body "... 600 years after the first, ..." -> "... after Map 1, ..."
- Images: the old page ends the paragraph with "But look at the areas inland." and puts "Are they as detailed as those on the coast? Follow the course of the River Ganga ..." in a blue box. The new page ends the paragraph at "(see Chapter 6)." and the blue box begins "Look at the areas in the interior of the subcontinent on Map 2. Are they as detailed as those on the coast? Follow ...". New text reads "after Map 1".
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 10 (old) / 10 (new)
- Hunk: modified source "“a different language in every region of this land: Sindhi, ...”." -> "In 1318 the poet Amir Khusrau noted that there was a different language in every region of this land: ... Delhi)." plus deleted note "In 1318 the poet Amir Khusrau noted that there was"
- Images: both pages carry the same box, with the line "In 1318 the poet Amir Khusrau noted that there was" followed by the italic quotation. In 2014 the lead-in line is set as plain text and the quote has quotation marks, in 2016 the lead-in is bold and the quote has no quotation marks.
- Verdict: engine noise
- Fix: none (the wording is the same, only the typesetting of the lead-in differs, so the lead-in line is classed differently per edition). A typographic rule that ignores a lead-in glued to a quotation would remove it.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 10 (old) / 10 (new)
- Hunk: modified note "Prepare another list ... mentioned: underline names that are similar and circle those that are different." -> "... mentioned." with inserted body "Underline names that are similar and circle those that are different."
- Images: old box ends "... he mentioned: underline names that are similar and circle those that are different." New box reads "... he mentioned. Underline names that are similar and circle those that are different."
- Verdict: real change (colon became a full stop). The split into two units is then engine behaviour.
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 1, printed page 10 (old) / 10 (new)
- Hunk: modified body "Compare, for example, Tables 1 in Chapters 3 and 4." -> "Table 1 in Chapters 3 and 4."
- Images: old page reads "Tables 1", new reads "Table 1".
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 45 (old) / 45 (new)
- Hunk: deleted heading "THE CREATION OF AN EMPIRE: The Mughal Dynasty", inserted heading "THE MUGHAL EMPIRE"; modified body "Today the Prime Minister ... Red Fort ..., on Independence Day." -> "... the nation on Independence Day from the ramparts ..."
- Images: chapter title bars differ ("THE CREATION OF AN EMPIRE: The Mughal Dynasty" and "THE MUGHAL EMPIRE"). The last sentence of the opening paragraph has "on Independence Day" at the end (old) and after "the nation" (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 48 (old) / 48 (new)
- Hunk: modified body "... died in an accident the following year." -> "... died the next year after an accident in this building."; "Campaigns in the north-west." -> "Campaigns were launched in the north-west."
- Images: both readings are on the page in the Table 1 panel (Humayun and Akbar entries).
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 49 (old) / 49 (new)
- Hunk: modified body "Shah Jahan 1627-1658 Mughal campaigns continued in the Deccan under Shah Jahan." -> "Mughal campaigns continued ..."; inserted table "Shah Jahan 1627-1658"
- Images: the panel has a bold run-in heading "Shah Jahan 1627-1658" on its own line above the paragraph in both editions. The 2014 extraction glued it into the sentence, the 2016 extraction made it a table row. The panel's Aurangzeb heading reads "1653-1707" (old) and "1658-1707" (new), and "Golcunda" (old) is "Golconda" (new).
- Verdict: extraction fault (rule) for the heading glue, real change for the dates and spelling
- Fix: pattern is a bold run-in king heading ("Babur", "Humayun", "Akbar", "Jahangir", "Shah Jahan", "Aurangzeb" with years) inside the Table 1 panel being treated inconsistently, glued to the first sentence in 2014 and read as a table row in 2016. Seen at chapter 4 page 49 in both editions. A rule should emit these as a heading or a fixed-form paragraph in the same way for every edition.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 52 (old) / 52 (new)
- Hunk: modified caption "Fig. 6 ... corruption in his father's administration." -> "... administration: (1) a corrupt officer receiving a bribe and (2) a tax-collector punishing poor peasants." and deleted caption "(1) A corrupt officer recieves a bribe and (2) a tax-collector punishes poor peasants."; "mansadar" -> "mansabdar"; "ten-year" -> "10-year"
- Images: old caption reads "... father's administration. (1) A corrupt officer recieves a bribe and (2) a tax-collector punishes poor peasants." with the misspelling "recieves". New reads "... administration: (1) a corrupt officer receiving a bribe and (2) a tax-collector punishing poor peasants." Body text spells "mansadar" (old) and "mansabdar" (new), "ten-year" (old) and "10-year" (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 54 (old) / 54 (new)
- Hunk: deleted heading "Nur Jahan's influence in Jahangir's court"; modified note "Mehrunnisa, married ..." -> "Nur Jahan's influence in Jahangir's court Mehrunnisa married ..."; modified body "It made him realise ..." -> "Akbar's interaction with people of different faiths made him realise ..."
- Images: both pages have a purple box with a teal title bar "Nur Jahan's influence in Jahangir's court" over the text "Mehrunnisa(,) married the Emperor Jahangir in 1611 ...". The 2014 page has a comma after Mehrunnisa, the 2016 page has none. The bottom paragraph reads "It made him realise" (old) and "Akbar's interaction with people of different faiths made him realise" (new).
- Verdict: extraction fault (rule) for the title glue, real change for the wording
- Fix: same rule as chapter 1 page 4. In 2016 the box title bar is glued into the first line of the box note. Seen also at chapter 1 page 4 ("The value of paper Compare the following:").
  - Reference text in 2016-09-10 chapter 4: "Nur Jahan’s influence in Jahangir’s court Mehrunnisa married the Emperor Jahangir in 1611"

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 57 (old) / 57 (new)
- Hunk: deleted notes "These included Queen Elizabeth I (1558-1603) of England. ..." (eight sentences) and inserted body "These included the ruler of Ottoman Turkey, Sultan Suleyman 1520-1566. ..." (ten sentences); modified note "Find out more about Akbar's other contemporaries – the ruler of Ottoman Turkey ..." -> "... the ruler of England, Queen Elizabeth I ..."; deleted body "Queens and kings", inserted "Kings and queens"; "Imagine you have inherited a kingdom." -> "You have inherited a kingdom."
- Images: the "Elsewhere" box on page 57 is about Queen Elizabeth I in the old edition and about Sultan Suleyman in the new one. Its title reads "Queens and kings" (old) and "Kings and queens" (new). The Imagine box reads "Babur and Akbar were about your age when they became rulers. Imagine you have inherited a kingdom." (old) and "You have inherited a kingdom. (Remember Babur and Akbar were about your age when they became rulers)." (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 57 (old) / 57 (new)
- Hunk: modified exercises "1. Match the following mansab Marwar" -> "1. Match the following:", deleted exercises "Nur Jahan Babur subadar rank", "Rathor Rajput Mewar"; modified exercises "Mongol governor" -> "mansab Marwar Mongol governor"; glossary#8 modified, with "Rathor Rajput Mewar Nur Jahan rank subadar Jahangir KEYWORDS" glued before "Mughal mansab jagir zat ..."
- Images: the match-the-following table has two columns (mansab / Marwar, Mongol / governor, Sisodiya Rajput / Uzbeg, Rathor Rajput / Mewar, Nur Jahan / Babur or rank, subadar / rank or Jahangir). The right column is reordered in the new edition (the last items read rank, Jahangir instead of Babur, rank). The table is not text-ordered, and the keywords column of page 58 is not related to it.
- Verdict: extraction fault (rule)
- Fix: pattern is a two-column match-the-following table whose rows are read by columns, spilling the last rows into the next stream (here into the glossary of page 58) and gluing a first row to the instruction line. Seen at chapter 4 pages 57 and 58 in both editions. A rule should read each row as "left item / right item" and keep the whole table in the exercises stream.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 58 (old) / 58 (new)
- Hunk: modified exercises "7. Why did the Mughals emphasise their Timurid and not their Mughal descent?" -> "... Mongol descent?"
- Images: old page reads "not their Mughal descent?", new page reads "not their Mongol descent?".
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 4, printed page 58 (old) / 58 (new)
- Hunk: modified glossary "(b) The five Deccan Sultanates were Berar, Khandesh, Ahmadnagar, _____________ and _________________." and similar blank-line hunks (a), (d)
- Images: the fill-in-the-blank lines are printed as rules of different length in the two editions.
- Verdict: engine noise
- Fix: none, but a rule that collapses runs of underscores to a single token before comparison would remove all such hunks (chapter 4 page 58 items (a), (b), (d)). Also the fill-in-the-blanks lines are in the glossary stream although they are exercises.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 5, printed page 60 (old) / 60 (new)
- Hunk: deleted captions "inar is five", ".", "or was by Aybak and tutmish 9. Over the damaged and s and Alauddin ammad uz Shah d"; modified caption "The band ns you er its y." -> "The band of inscriptions you see are under its first balcony."; inserted captions "Fig. 1 The Qutb Minar is five storeys high." and two more
- Images: on the old page the left margin is cut off: the caption column of Figure 1 is clipped at the page edge, so only the right-hand ends of the lines ("nar is five", "The band", "as you", "r its") remain. The new page shows the whole caption, "Fig. 1 The Qutb Minar is five storeys high. The band of inscriptions you see are under its first balcony. The first floor was constructed by Qutbuddin Aybak and the rest by Iltutmish around 1229. ..."
- Verdict: extraction fault (rule)
- Fix: pattern is a 2014 chapter 5 PDF whose page box clips the left margin, so margin captions, box titles and notes appear as the tail ends of lines. Seen in 2014-07-28 chapter 5 at printed pages 60 (Fig. 1 caption), 62 (Fig. 3a/3b captions and the "Can you make out ..." box, note#3 and note#4 "rences tice he of the es?"), 64 (note#5 "l emperor n's chro-ared ..." and caption "mi masjid h Jahan in tal at bad"), 66 (captions "har baghs har bagh n's tomb"), 68 (note#9 "ura ra hard aced in ns o marble ..." and captions "balcony", "-i am in eted"), 70 (captions "e ahal ction from a map ...", "f Shahjahanabad.", "ears to be very crowded ..."). The page text for those lines should be treated as unreadable (typed as unreadable, or read from the full media box), not compared.

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 5, printed page 62 (old) / 63 (new)
- Hunk: modified body "Temple Construction in the Early Eleventh Century Two technological and stylistic developments are noticeable from the twelfth century." -> "Two technological and stylistic developments ..." with inserted body "Temple Construction in the Early Eleventh Century What differences do you notice between the shikharas of the two temples?"
- Images: the old page 62 carries the italic figure heading "Temple Construction in the Early Eleventh Century" over the Kandariya Mahadeva and Rajarajeshvara photographs. The sentence "Two technological and stylistic developments ..." is the first line of the next printed page (63) on both editions. So the heading belongs to the figures and not the sentence.
- Verdict: extraction fault (rule)
- Fix: pattern is a figure group heading from a preceding page being glued into the first body sentence of the next page, because the figure caption's last unit is left open. Seen at chapter 5 page 62 -> 63 in 2014. (The 2016 and 2019 texts attach it to a different unit, see the 2016 -> 2019 entry.)

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 5, printed page 64 (old) / 64 (new)
- Hunk: modified body "An inscription in the Delhi mosque ... law-givers" -> "An inscription in the Quwwat al-Islam mosque ... lawgivers"
- Images: the old page reads "Delhi mosque" and "law-giver", the new page "Quwwat al-Islam mosque" and "lawgivers".
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 5, printed page 72 (old) / 71 (new)
- Hunk: modified body "The Mughals liked this “Bangla dome” (see Fig. ... in Chapter 9)" -> "(see Figures 11 and 12 in Chapter 9)"
- Images: old page 72 reads "(see Fig. ... in Chapter 9)" with the dots in print. The 2016 page 72 (seen in the 2016 -> 2019 review) reads "see Figures 11 and 12 in Chapter 9". The 2016 paragraph starts at the foot of page 71 and runs on to page 72, which explains the page number 71 in the hunk.
- Verdict: real change
- Fix: none

### our-pasts-2 2014-07-28 -> 2016-09-10, chapter 5, printed page 72 (old) / 72 (new)
- Hunk: deleted notes "From the twelfth century onwards, attempts began in France ..." (three) and inserted table "From the twelfth century onwards, attempts began in France ... flying buttresses ..." 
- Images: the Gothic churches box ("Churches that touched the skies") has the same wording in both editions, with a picture of Notre Dame. In 2014 it is read as notes, in 2016 as a single table cell.
- Verdict: engine noise
- Fix: none (stream assignment of the same box differs by edition). A rule that treats a text box with a figure as a note in each edition would remove it.

## 2016-09-10 -> 2019-05-04

Most hunks in the first chapters of this pair are the 2016 faults from the previous pair being cleared in 2019, so they appear here from the other side.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 1, printed page 3 (old) / 3 (new)
- Hunk: modified heading "New and Old Termi New and Old Terminologies nologies" -> "New and Old Terminologies"
- Images: both pages show the single heading "New and Old Terminologies" (the 2016 page is the one examined in the previous pair).
- Verdict: extraction fault (one-off) in the 2016 text. The 2019 text is right.
- Fix: the override given in the 2014 -> 2016 pair, chapter 1 page 3, removes this hunk.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 1, printed page 4 (old) / 4 (new)
- Hunk: modified body "... cheaper and more The value of paper Compare the following:" -> "... cheaper and more widely available."; deleted body "widely available." (page 5); inserted heading "The value of paper" and note "Compare the following:"
- Images: both pages are identical in layout and wording: the paragraph stops at "cheaper and more", a purple box titled "The value of paper" follows, and the sentence continues on page 5. Only the box's type weight differs (bold in 2016, regular in 2019).
- Verdict: extraction fault (rule) in 2016, already described in the previous pair. The 2019 text is right.
- Fix: none new. Same rule as the 2014 -> 2016 entry for chapter 1 page 4.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 1, printed page 1 (old) / 1 (new)
- Hunk: modified caption "Map 1 ... showing the Indian subcontinent." -> "... showing the Indian subcontinent from land to sea."
- Images: the margin caption of Map 1 ends "subcontinent." (old) and "subcontinent from land to sea." (new). The 2019 page also has a QR code above the caption.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 1, printed page 10 (old) / 10 (new)
- Hunk: modified source "In 1318 the poet Amir Khusrau noted that there was a different language ..." -> "a different language ..." with inserted note "In 1318 the poet Amir Khusrau noted that there was"
- Images: the "Language and region" box has the same wording on both pages. The lead-in "In 1318 ... there was" is a line above the italic quotation on both.
- Verdict: engine noise
- Fix: none. Same box as the previous pair. In 2016 the lead-in was read into the source, in 2019 into a note. Same pattern at chapter 3 page 38 ("The Sultans were advised:") and page 40 ("Ibn Battuta ... chieftains sometimes").

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 2, printed page 21 (old) / 21 (new)
- Hunk: modified body "He was interested in finding out ... al-Biruni ..." -> "Sultan Mahmud was also interested ... Al-Biruni ..."; "Kitab-al Hind" -> "Kitab ul-Hind"; note "Sultan is an Arabic term meaning ruler." -> "Sultan An Arabic term meaning ruler."
- Images: the paragraph is split differently (the 2019 page starts a new paragraph at "Sultan Mahmud was also interested") and the margin box reads "Sultan is an Arabic term meaning ruler." (old) and "Sultan / An Arabic term meaning ruler." (new, glossary style). The Kitab spelling differs on the page.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 2, printed page 27 (old) / 27 (new)
- Hunk: deleted note "The working of a sabha according to the Uttaramerur inscription:", inserted notes "Who could be a member of a sabha?" and "The Uttaramerur inscription lays down:"; modified source "... as well as those of his relatives ..." -> "... and those of his relatives ..."
- Images: the box opens with "The working of a sabha according to the Uttaramerur inscription:" (old) and "Who could be a member of a sabha? The Uttaramerur inscription lays down:" (new). The last line of the inscription reads "as well as those" (old) and "and those" (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 3, printed page 32 (old) / 32 (new)
- Hunk: modified captions "1. Preparing the paper." -> "Preparing the paper." and similar, "Fig.1 Four stages in the preparation of a manuscript." -> "... making of a manuscript: A.", deleted captions "1 2" and "3 4", inserted captions "A B", "C D", "B.", "C.", "D."
- Images: the four miniatures are numbered 1 to 4 in the old edition and lettered A to D in the new edition, and the caption lists "1. Preparing the paper ... 4. Preparing the binding" become "A. ... D.". The caption also changes "preparation" to "making".
- Verdict: real change (relabelling). The hunks splitting the letters into captions are engine noise from the corner labels of the images.
- Fix: none. A rule that ignores one- or two-character corner labels of a figure ("1 2", "A B") would drop the noise.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: modified caption "The minar was built by three Sultans– Qutbuddin Aybak, Iltutmish and Firuz Shah Tughluq." -> "The minar was built by two Sultans: Qutbuddin Aybak and Iltutmish."
- Images: Fig. 2 caption reads "three Sultans– Qutbuddin Aybak, Iltutmish and Firuz Shah Tughluq" (old) and "two Sultans: Qutbuddin Aybak and Iltutmish" (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 3, printed page 38 (old) / 38 (new)
- Hunk: modified note "A client is someone who is under the protection of another, ..." -> "Client Someone who is under the protection of another; ..."; modified note "The Sultans were advised: “A slave, whom one has brought up ..." -> "A slave, whom one has brought up ..." with inserted note "The Sultans were advised:"; quote marks removed
- Images: the margin glossary note reads "A client is someone ..." (old) and "Client / Someone who ..." (new). The box "Slaves rather than sons" has the lead-in "The Sultans were advised:" followed by the quotation. The 2019 quotation is in italics without quotation marks, the 2016 one is in roman type with marks.
- Verdict: real change for the glossary note. Engine noise for the box (same words, the typesetting moves the quotation marks).
- Fix: none for the glossary note. Rule for the box: when a box quotation lacks quotation marks in one edition, compare without surrounding quotation marks and treat a lead-in line ("The Sultans were advised:") as part of the same unit. Seen at chapter 3 pages 38 and 40 and chapter 1 page 10.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 3, printed page 40 (old) / 40 (new)
- Hunk: modified note "Ibn Battuta ... chieftains sometimes “fortified themselves in mountains ... bamboo groves." -> "... chieftains sometimes" with inserted source "fortified themselves in mountains, ... bamboo groves."; modified note "... prepared instruments.”" -> "... prepared instruments."
- Images: the "Chieftains and their fortifications" box reads the same on both pages. The 2016 box is roman text with quotation marks, the 2019 box has a lead-in line and an italic quotation without marks.
- Verdict: engine noise
- Fix: none (same rule as chapter 3 page 38)

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 3, printed page 41 (old) / 41 (new)
- Hunk: modified caption "But to meet the need of the large number of soldiers ..." -> "... the expense of maintaining such a large number of soldiers ..."; modified caption "Delhi was attacked twice, in 1299/1300 and 1302-03. As a defensive measure, ..." -> "As a defensive measure, ..." with inserted caption "Delhi was attacked twice, in 1299/1300 and 1302-1303."
- Images: the comparison table has "1302-03" (old) and "1302-1303" (new) and "need of the large number" (old) and "expense of maintaining such a large number" (new) in its cells.
- Verdict: real change for the wording and date style. Engine noise for the sentence split, which comes from the table cell being read as a caption.
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 4, printed page 47 (old) / 47 (new)
- Hunk: inserted captions "Gun powder technology was brought to India for warfare in the 14th century." and "Fire arms were used for the first time ..."
- Images: the new page has a new orange margin note under Fig. 4 on gunpowder technology. The old page has none.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 4, printed page 55 (old) / 55 (new)
- Hunk: inserted captions "Akbar commissioned the translation of many Sanskrit works into Persian." and three more sentences
- Images: a new orange margin note on the Sanskrit translations (Maktab Khana, Razmnamah) appears on the new page and not on the old.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 4, printed page 54 (old) / 54 (new)
- Hunk: modified body "Nur Jahan's influence in Jahangir's court Mehrunnisa married ..." -> "Mehrunnisa married ..."; inserted heading "Nur Jahan's influence in Jahangir's court"
- Images: the box on page 54 carries the same title and text in both editions (see the previous pair).
- Verdict: extraction fault (rule) in 2016 (box title glued to the box text). The 2019 text is right.
- Fix: none new. Same rule as chapter 4 page 54 in the previous pair.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 4, printed page 57 (old) / 57 (new)
- Hunk: modified body "... Shah Abbas (1588-1629); ; and the more controversial Russian ruler ..." -> "... (1588-1629); and the more ..."
- Images: the Elsewhere box on both pages reads "Shah Abbas (1588-1629); and the more controversial Russian ruler". There is a single semicolon on each page.
- Verdict: extraction fault (one-off) in 2016
- Fix: override
  - snapshot: "2016-09-10"
  - chapter: 4
  - find: "Shah Abbas (1588-1629); ; and"
  - replace: "Shah Abbas (1588-1629); and"
  - note: "doubled semicolon from a kerned character in the Elsewhere box on page 57, the page has one"

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 5, printed page 61 (old) / 61 (new)
- Hunk: deleted note "Superstructure The part of a building above the ground floor."; inserted captions "Raniji ki baori or the 'Queen's Stepwell' ..." and "Known for its architectural beauty ..."
- Images: the old margin box is the glossary entry "Superstructure: the part of a building above the ground floor". The new margin has a different box about Raniji ki baori in Bundi (the glossary entry is gone from the margin).
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 5, printed page 62 (old) / 62 (new), and 63
- Hunk: modified body "Two technological and stylistic developments ..." -> "Temple Construction in the Early Eleventh Century Two technological and stylistic developments ..." and modified body "Temple Construction in the Early Eleventh Century What differences do you notice ..." -> "What differences do you notice ..."
- Images: page 62 has the same figure group on both editions, headed by the italic title "Temple Construction in the Early Eleventh Century" over the Kandariya Mahadeva text, with the blue question box in the margin. "Two technological and stylistic developments ..." is the first sentence on page 63. The title is a figure heading and belongs to neither sentence.
- Verdict: extraction fault (rule)
- Fix: pattern is an italic figure-group title on one page being attached to a body unit (the question box in 2016, the first sentence of the next page in 2019, the next page in 2014). Seen at chapter 5 page 62 in 2014, 2016 and 2019. It should be emitted as its own heading or caption.
  - 2019-05-04 chapter 5 find: "Temple Construction in the Early Eleventh Century Two technological and stylistic developments"
  - replace: "Two technological and stylistic developments"
  - 2016-09-10 chapter 5 find: "Temple Construction in the Early Eleventh Century What differences do you notice"
  - replace: "What differences do you notice"
  - note: "figure group title glued to the next unit, it belongs to the figures on page 62"
  (These work as one-off overrides but the pattern is the same one rule.)

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 5, printed page 72 (old) / 72 (new)
- Hunk: inserted notes "From the twelfth century onwards, attempts began in France ..." (three) and deleted table "From the twelfth century onwards ... flying buttresses ..."
- Images: the "Churches that touched the skies" box is identical in wording on both pages.
- Verdict: engine noise
- Fix: none (box read as table in 2016 and as notes in 2019, and as notes in 2014). A rule that makes these boxes one stream in every edition would remove it.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 6, printed page 77 (old) / 77 (new)
- Hunk: modified body "Bronze, bell metal and the “lost wax” technique Temple authorities used their wealth to finance trade and banking." -> "Temple authorities used ..."; inserted heading "Bronze, bell metal and the “lost wax” technique"
- Images: both pages have a purple box titled "Bronze, bell metal and the “lost wax” technique" at the top, followed by the body paragraph "Temple authorities used their wealth ...".
- Verdict: extraction fault (rule) in 2016. The 2019 text is right.
- Fix: pattern is a box title glued to the paragraph that follows the box. Same family as chapter 1 page 4 and chapter 4 page 54. Reference text in 2016-09-10 chapter 6: "Bronze, bell metal and the “lost wax” technique Temple authorities used". Override
  - snapshot: "2016-09-10"
  - chapter: 6
  - find: "Bronze, bell metal and the “lost wax” technique Temple authorities used"
  - replace: "Temple authorities used"
  - note: "box title glued to the next paragraph, the page has it in the box heading above the picture"

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 6, printed page 83 (old) / 83 (new)
- Hunk: modified caption "Fig. 7 Stone chariot, Vitthala temple," -> "Fig. 7 Stone chariot, Vitthala temple, Hampi."; modified body "Moors (a name used collectively for Muslim merchants), Chettis ..." -> "Muslim merchants, Chettis ..."
- Images: in the old page the last word of the caption, "Hampi.", is set over the running footer ("TOWNS, TRADERS AND ...") and does not belong to the caption column, so the 2016 caption looks cut off. The new page has the full caption. The body text on the old page reads "Moors (a name used collectively for Muslim merchants)" and on the new page "Muslim merchants".
- Verdict: extraction fault (one-off) for the caption, real change for the body
- Fix: override
  - snapshot: "2016-09-10"
  - chapter: 6
  - find: "Fig. 7 Stone chariot, Vitthala temple,"
  - replace: "Fig. 7 Stone chariot, Vitthala temple, Hampi."
  - note: "'Hampi.' overlaps the page footer in the 2016 file, the caption ends with Hampi"
  The same overflow is visible in the images at chapter 6 page 87 ("Fig. 8 A Bombay street, early nineteenth", the word "century." is printed over the footer, find "Fig. 8 A Bombay street, early nineteenth" in 2016-09-10 chapter 6) and chapter 9 page 123 ("Fig. 2 ... palm-leaf manuscript,", the word "Orissa." is printed over the footer, find "Fig. 2 The icons of Balabhadra, Subhadra and Jagannatha, palm-leaf manuscript," in 2016-09-10 chapter 9). Rule: in the 2016 PDFs the last line of a margin caption that spills below the caption column lands in the footer band and is dropped. All three places are completed in the 2019 edition.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 6, printed page 85 / 88
- Hunk: modified note "Factor Official merchant of the East India Company." -> "Factor Official in-charge of trading activities of the European Trading Companies."; modified note on Vasco da Gama
- Images: page 85 margin note and page 88 Elsewhere box show the rewritten wording in the new edition ("sailed down the African Coast, went round the Cape of Good Hope" and "Official in-charge of trading activities of the European Trading Companies").
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 8, printed page 110 (old) / 110 (new)
- Hunk: deleted body "It also rejected idol worship and considerably simplified rituals of worship into collective prayers." and "At the same time Muslim scholars developed a holy law called Shariat."; inserted body "In the eighth and ninth centuries religious scholars developed different aspects of the Holy Law (Shariat) ..." and "While the religion of Islam gradually became more complex, Sufis ..."
- Images: the Islam and Sufism section is rewritten on page 110 in the new edition. The old page has the sentences about idol worship and the Shariat and the new page has the Holy Law and Sufi dimension text.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 8, printed page 111 (old) / 111 (new)
- Hunk: inserted notes "In Kashmir the Rishi order of Sufism flourished in the 15th and 16th centuries." and two more; modified body "a genealogy of Sufi teachers" -> "a spiritual genealogy of Sufi teachers"
- Images: the new page has an orange margin note on the Rishi order below Fig. 4. The old page has none. "spiritual" is present in the new text.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 8, printed page 117 (old) / 117 (new)
- Hunk: modified body "We know more about Guru Nanak ..." -> "We know more about Baba Guru Nanak ..." (and eleven more sentences on pages 117 and 118)
- Images: the heading and the body on page 117 read "Baba Guru Nanak" in both editions in the heading (the 2016 heading already has "Baba") and in the body in the new edition only.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 9, printed page 127 (old) / 127 (new)
- Hunk: modified note "... Odissi (Orissa) ..." -> "... Odissi (Odisha) ..."
- Images: the "Classical dances" box lists "Odissi (Orissa)" (old) and "Odissi (Odisha)" (new).
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 10, printed page 143 (old) / 143 (new)
- Hunk: modified body "... the founder of Hyderabad state, ..." -> "... state (1724-1748), ..."; "Taking advantage" -> "Taking subsequent advantage"; "Asaf Jah already had full control" -> "during 1720-22 Asaf Jah had already gained control"; "the Nizam" -> "the Nizam-ul-Mulk Asaf Jah"
- Images: all four edits are visible on the two pages.
- Verdict: real change
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 10, printed page 146 (old) / 147 (new)
- Hunk: modified body "Maratha campaigns into Rajasthan from the 1740s put severe pressure ..." -> "from the 1740s put severe pressure ..." with inserted body "Maratha campaigns into Rajasthan Many Rajput chieftains built a number of forts ..." and two more sentences
- Images: on page 147 of the new edition a new box about Rajput hill forts (Fig. 4b, Chittorgarh) is set into the text and the paragraph wraps around it. The sentence "Maratha campaigns into Rajasthan from the 1740s put severe pressure on these principalities ..." runs on both sides of the box. The old page has no box.
- Verdict: extraction fault (rule) for the sentence split, real change for the new box
- Fix: pattern is a text box set inside a wrapped paragraph, so the box text is inserted at the line where it starts and splits a sentence. The sentence should be rejoined and the box emitted as a note. Seen at chapter 10 page 147 in 2019.
  - 2019-05-04 chapter 10: the text "Maratha campaigns into Rajasthan Many Rajput chieftains built" is the join to undo.

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 10, printed page 149 (old) / 149 (new)
- Hunk: inserted captions "Fig. 7a Portrait of Shivaji", "Towards the end of the 17th century a powerful state started emerging ..." and seven more sentences; deleted caption "Fig. 5 Mehrangarh Fort, Jodhpur." and "Fig. 6 Guru Gobind Singh, the tenth guru."
- Images: the new page has a Shivaji portrait and an orange margin note about Shivaji, the old page has the sword of Maharaja Ranjit Singh as its figure. The Mehrangarh caption (page 147) is still there in 2019 under the picture.
- Verdict: real change for the Shivaji additions. Engine noise for the "Fig. 5 Mehrangarh Fort" deletion, because the caption exists in the new edition below the image (the new text places it with different spacing, "Fig. 5 Mehrangarh Fort, Jodhpur" with no full stop).
- Fix: none

### our-pasts-2 2016-09-10 -> 2019-05-04, chapter 10, printed page 153 (old) / 153 (new)
- Hunk: modified exercises "(c) Asaf Jah was given charge of the Deccan subadari in ____" -> "(c) Asaf Jah founded the Hyderabad state in ____"; "(d) ... Awadh nawabi ..." -> "Awadh state"
- Images: both exercises read differently on the two pages as in the hunk.
- Verdict: real change
- Fix: none

## 2019-05-04 -> 2022-08-04-ocr

The 2022-08-04 file is a flat set of page images read by OCR. For the pages examined below (chapters 1, 2, 3, 4, 7 and 9 and the exercise pages) the printed wording is the same as in 2019. In every pair of images I found the sentences, numbers and spellings in agreement, so I found no real change in this pair. Every hunk below is an OCR or layout reading fault. The vocabulary of the faults is small and repeats, so they are grouped by pattern where possible.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 1, printed page 1 (old) / 1 (new)
- Hunk: modified heading "TRACING CHANGES THROUGH A THOUSAND YEARS" -> "TRACING CHANGES THROUGH" and body "Take a look at Maps 1 and 2. ... 1154 CE ..." -> "A THOUSAND YEARS ake a look at Maps 1 and 2. ... 1154 ce ..."; inserted caption "0760CHO1"
- Images: both pages carry the same two-line chapter title bar "TRACING CHANGES THROUGH / A THOUSAND YEARS", the same drop-capital "T" opening "Take a look at Maps 1 and 2", the same small-capital "CE", and the QR code with its code number under it.
- Verdict: extraction fault (rule)
- Fix: pattern for the OCR edition: (1) the second line of the chapter title is glued onto the first sentence of the opening paragraph, (2) the drop capital is dropped or misread (chapter 1 "ake" for "Take", chapter 7 page 91 "F = Yo saw" for "You saw", chapter 9 "Or of the commonest ways" for "One of the commonest ways"), (3) small-capital "CE" and "BCE" come out lower case ("ce", "sce", chapter 8 page 130), (4) the QR code number is read as a caption or body text ("0760CHO1", "0760cHO7", chapter 7 "0760cHO7 towns and villages"). A rule should cut the title bar at the end of its line, rebuild the drop capital from the first word, upper-case small-capital "ce" after a year, and drop a token of the form NNNNCHNN.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 1, printed page 2 (old) / 2 (new)
- Hunk: inserted captions "i Lf wie Royats = __ DE Morrie.", "Me ap aoe psn Sa he Geant Ve a, rites .", and three more; modified caption "Map 2 The subcontinent, from ... Guillaume de l'Isle." -> "The subcontinent, from ... Guillaume de U'Isle."
- Images: the page has the same map of the subcontinent, and the same margin caption "Map 2 The subcontinent, from the early-eighteenth-century Atlas Nouveau of Guillaume de l'Isle." The map is a picture with tiny place-names. All the inserted captions are the OCR's reading of those place-names.
- Verdict: extraction fault (rule)
- Fix: pattern is text read from inside a picture (maps and figures) and filed as captions or table rows. It was seen at chapter 1 pages 2 and 9 (maps), chapter 2 pages 16 and 22 ("TIBET", "OF Yas SS ety a Sigs?", "INDIAN OGEAN", "CHALUKYAS ~~ & S oF"), chapter 3 pages 30, 34 and 35 ("LUQABAD", "Hansie Kaslig DELHI P83” eBudaun", "PUNJAB Delhi -, i. s Cy) Joff"). A rule should drop OCR lines whose words are mostly not dictionary words, or whose block lies inside a picture, and should keep only text outside picture boxes. The figure label "Map 2" is then read on its own line, which the rule should join with its caption.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 1, printed page 4 (old) / 4 (new)
- Hunk: modified body "... cheaper and more widely available." -> "... cheaper and more The value of paper Compare the following:"; inserted body "widely available." (page 5); deleted heading "The value of paper"; modified note "When was paper more expensive ... – in the thirteenth or ..." -> "?) When was paper more expensive and easily available °/ - inthe thirteenth or ..."
- Images: same page as the 2019 and the 2016 pages: the paragraph stops at "more", the purple box "The value of paper" follows, and the closing question sits next to an orange question-mark icon.
- Verdict: extraction fault (rule)
- Fix: same box-title glue rule as in the 2014 -> 2016 pair (chapter 1 page 4). Also the question-mark icon is read as "?)" and "°/" and the dash with its spaces is lost ("inthe"). These icon tokens appear on many pages, such as chapter 3 page 38 ("2?)"), page 40 ("°/"), page 33 (">", "»_)") and chapter 2 page 18 ("?)"). A rule should strip the icon tokens "?)", "°/", "2?)", ">", "»_)" from the start or end of a note.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 1, printed page 14 (old) / 14 (new)
- Hunk: modified exercises "(a) We do not find inscriptions for the period after 700." -> "(a) We do not find inscriptions for the period after KEYWORDS 700."; deleted exercises "KEYWORDS manuscript jati region periodisation"; modified exercises "(c) ——, ———, ———, ——— and ——— were some of the new crops ..." -> "some of the new crops ..."; and similar for the blanks
- Images: both pages have the same Let's recall exercises and the same KEYWORDS margin column (manuscript, jati, region, periodisation). The blanks are printed as dashes. The margin column sits to the left of the exercises.
- Verdict: extraction fault (rule)
- Fix: pattern is the margin column interleaved by reading order. The "KEYWORDS" title and its word list land inside an exercise line (chapter 1 page 14 "(a) ... after KEYWORDS 700.", chapter 3 page 44 "KEYWORDS iqta tarikh garrison Mongols gender kharaj According to the “circle of justice”", chapter 4 page 73 and page 59). Also dashed blanks of the form "———" are dropped from the line, leaving "Archives are places where are kept" and "some of the new crops". A rule should take the margin column as its own block, and keep dash runs as a blank token.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 2, printed page 26 (old) / 26 (new)
- Hunk: deleted note "Chola inscriptions mention several categories of land: vellanvagai land of non-Brahmana peasant proprietors brahmadeya ..." and inserted table row "shalabhoga land for the maintenance of a school" and body "Chola inscriptions mention several categories of land:" with "vellanvagai land of ... brahmadeya land gifted to Brahmanas devadana, tirunamattu ..."
- Images: the "Types of land" box has the same five entries in the same order on both pages, with wording the same.
- Verdict: engine noise
- Fix: none. The OCR reads the box as body lines and table rows, the 2019 text reads it as a note. A rule that compares boxes regardless of stream would remove it.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 2, printed page 27 (old) / 27 (new)
- Hunk: deleted heading "Inscriptions and texts", deleted notes "The Uttaramerur inscription lays down:", "Do you think women participated in these assemblies?"; inserted body "Inscriptions and texts inscription lays down:" and "In the thresholds of the huts covered with strips of leather, ..."; modified source "Pulaiyas" -> "Pulatyas", "kanji" -> "Ranji", "knowledge" -> "Rnowledge"
- Images: both pages carry the same box "Inscriptions and texts" with the Uttaramerur inscription and the Periyapuranam excerpt, and the same two question boxes in the margin. The words in the images read "Pulaiyas", "kanji" and "knowledge".
- Verdict: extraction fault (rule) for the misreadings, engine noise for the stream changes
- Fix: pattern is italic text in a coloured box read with the usual confusions: "l" and "i" to "1" and "t" ("is" -> "1s", "ts", "Pulaiyas" -> "Pulatyas"), "k" to "R" ("know" -> "Rnow", "kanji" -> "Ranji", "kul" -> "Rul", "knowledge" -> "Rnowledge"), "q" to "g" in "Tughluq" -> "Tughlug", "iqtas" -> "igtas", "muqtis" -> "mugqtis", and "a" glued to the next word ("a ladder" -> "aladder", "born as a" -> "bornasa"). Seen in chapters 1 to 9. The vocabulary snapping step already used for outlined words could be extended to these tokens. One example override
  - snapshot: "2022-08-04-ocr"
  - chapter: 2
  - find: "Rnowledge"
  - replace: "knowledge"
  - note: "OCR misreading of k as R in the Inscriptions and texts box on page 27, the page reads knowledge"

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 3, printed page 31 (old) / 31 (new)
- Hunk: deleted body "Table 1", "RAJPUT DYNASTIES", "Tomaras Early twelfth century-1165", "Ananga Pala 1130-1145" ... (sixteen lines) and inserted body "Table 1 RAJPUT DYNASTIES Tomaras Early twelfth century-1165 Ananga Pala 1130-1145 Chauhans ..."
- Images: "The Rulers of Delhi, Table 1" is a coloured panel with the same rulers and the same dates on both pages (Tomaras, Ananga Pala, Chauhans, Prithviraj Chauhan, Qutbuddin Aybak, Iltutmish, Raziyya, Balban, Khalji, Tughluq, Sayyid, Lodi dynasties).
- Verdict: engine noise
- Fix: none for the dates (they agree). The OCR joins the whole panel into one long body line and the 2019 text has one line per ruler. The page was flagged suspect (old page 31 score 0.41) only for that reason. A rule should split the OCR panel at date patterns, or compare it as a bag of tokens.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 3, printed page 36 (old) / 36 (new)
- Hunk: deleted body "Members of the congregation choose the most respected, learned male as their leader (imam) ..." and modified body "(masjid-i-jami or jama masjid) Muslims read their prayers (namaz) together." -> "(masjid-ijami ...) ... together, Members of the congregation choose the most respected ..."; modified caption "Fig. 2 Quwwat" -> "Quuwwat"
- Images: the section "The Masjid" reads the same on both pages, including the sentence "Members of the congregation choose the most respected, learned male as their leader (imam) for the rituals of prayer." The new image has the same text in the same place.
- Verdict: engine noise for the sentence move, extraction fault (one-off) for the OCR misreadings
- Fix: override for the caption word
  - snapshot: "2022-08-04-ocr"
  - chapter: 3
  - find: "Quuwwat"
  - replace: "Quwwat"
  - note: "OCR doubled the letter in the Fig. 2 caption on page 36, the page reads Quwwat"
  (The same hunk shows hyphens in "masjid-i-jami" lost as "masjid-ijami" and a full stop read as a comma before "Members".)

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 3, printed page 41 (old) / 41 (new)
- Hunk: deleted captions "The soldiers had to be fed.", "This was done through the produce collected as tax from lands between the Ganga and Yamuna.", "Tax was fixed at 50 per cent of the peasant's yield.", "See Map 1."; inserted table "The soldiers had to be fed. This was done through ..."
- Images: the Alauddin Khalji and Muhammad Tughluq comparison table has the same cells on both pages.
- Verdict: engine noise
- Fix: none (a table cell read as captions in 2019 and as one table row by OCR)

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 3, printed page 44 (old) / 44 (new)
- Hunk: modified exercises "5. According to the “circle of justice” ..." -> "KEYWORDS iqta tarikh garrison Mongols gender kharaj According to the “circle of justice” ..." and exercise numbers "9.", "6.", "8.", "12.", "7.", "10.", "11." as separate hunks, inserted ".", "12.", "5.", "9."
- Images: both pages have exercises 5 to 12 with the same text and numbers under Let's understand, Let's discuss and Let's do, and the KEYWORDS column on the left.
- Verdict: extraction fault (rule)
- Fix: pattern is the number of a numbered exercise detached from its text, or numbers swapped between lines, when the exercises are read with the margin column. Seen at chapter 3 page 44, chapter 4 page 59, chapter 5 page 90, chapter 6 page 102, chapter 7 page 120, chapter 8 page 137, chapter 9 page 137 (matching list numbers 4, 6, 7, 8, 9 become hunks). A rule should read the exercises by their column, and bind a number to its text. The margin column rule above covers the "KEYWORDS" part.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 4, printed page 48 (old) / 48 (new)
- Hunk: modified body "1527 - defeated Rana Sanga, ..." and "Salim" -> "paling" and similar single-word changes in the Table 1 panel
- Images: the Mughal emperors panel reads the same on both pages. The 2022 image shows "Rana Sanga" and "Prince Salim".
- Verdict: extraction fault (rule)
- Fix: same OCR confusion family as chapter 2 page 27. Seen "Sanga" -> "anges", "Salim" -> "paling" in the red-text lines. A rule that snaps words to the book vocabulary (as already done for outlined words) would fix these. Suggested one-off overrides
  - snapshot: "2022-08-04-ocr", chapter: 4, find: "anges", replace: "Sanga", note: "OCR misreading of Sanga on page 48"
  - snapshot: "2022-08-04-ocr", chapter: 4, find: "paling", replace: "Salim", note: "OCR misreading of Salim on page 48"
  (check the context in the file before applying, as "anges" and "paling" are also words inside others.)

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 4, printed page 58 (old) / 58 (new)
- Hunk: deleted glossary lines of blanks and modified glossary "____________" runs; deleted exercises of the KEYWORDS column
- Images: page 58 shows the same fill-in-the-blank items and the same keyword list (Mughal, mansab, jagir, zat, sawar, sulh-i kul, primogeniture, coparcenary, zabt, zamindar).
- Verdict: engine noise
- Fix: none. Same underscore rule as the 2014 -> 2016 pair, and the OCR drops the underscores altogether. The page was flagged suspect (old page 58, score 0.46) because of this.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 6, printed page 83 / 85 (and chapter 3 page 34)
- Hunk: caption "Fig. 7" detached from its caption, "Fig 9 Vasco da Gama" glued, and the margin notes "Factor Official in-charge ..." -> "Official in-charge ..." with the term moved out
- Images: the margin glossary note "Factor" on page 85 and "Hinterland" and "Garrison town" on chapter 3 page 34 are present on both printed pages, each term in an orange bold-italic line above its definition. The figure label "Fig. 7" on page 83 sits at the head of its caption in both. In the 2022 text the term or figure label appears as a separate caption ("Hinterland", "Archive", "Patron") or is missing from its note.
- Verdict: extraction fault (rule)
- Fix: pattern is the term line of a margin glossary note (orange, bold italic) and the figure number being read as separate lines or dropped: chapter 1 page 5 ("Archive"), page 11 ("Patron"), chapter 3 page 34 ("Hinterland"), chapter 6 page 84 ("Hundi", from the hunk list only) and page 85 ("Factor"), chapter 6 page 93 ("Clan"), chapter 8 page 132 ("Pir"). The term should be kept at the head of the note.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 9, printed page 125 (old) / 125 (new)
- Hunk: page flagged suspect (new page 125, score 0.33) with the sentence beginning "Did women find a place within these stories? ..." as inserted or deleted text
- Images: the two pages hold the same text and the same map ("Map 1 Regions discussed in this chapter"), with the break after "So those" at the same place. The map labels are read as text in 2022.
- Verdict: engine noise
- Fix: none beyond the map-text rule. The suspect flag comes from the map labels and the sentence split at the foot of the page.

### our-pasts-2 2019-05-04 -> 2022-08-04-ocr, chapter 9, printed page 136 (old) / 136 (new)
- Hunk: page flagged suspect (old page 136, score 0.31)
- Images: both pages have the same Imagine box, the same match-the-following list and the same exercises 2 to 4. The KEYWORDS column (classical, miniature, pir, dialect) is in the margin of both.
- Verdict: engine noise
- Fix: none beyond the margin column and exercise-number rules above (the matching list is read by columns in 2019 and by lines in 2022, so every pair is a hunk).

## 2019-05-04 -> 2023-12-23-rationalised

The rationalised edition drops two chapters (Rulers and Buildings, Towns Traders and Craftspersons) and cuts material inside the others, so most deleted hunks are real. The faults here are in the titles, in letter-spaced lines and in a few figure texts. Chapter numbers in the entries are the 2019 numbers (and the new numbers where they differ).

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapters 5 and 6 (old), printed pages 60 to 90
- Hunk: chapter status "dropped" for "Rulers and Buildings" and "Towns, Traders and Craftspersons"
- Images: the rationalised book has eight chapters. Its chapter 5 is Tribes, Nomads and Settled Communities (old 7), its chapter 6 is Devotional Paths (old 8), and so on. No pages of the two dropped chapters are present (the text files for the new chapters 5 to 8 start at printed pages 53, 61, 79 and 94).
- Verdict: real change
- Fix: none

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 1, printed page 1 (old) / 1 (new)
- Hunk: modified heading "TRACING CHANGES THROUGH A THOUSAND YEARS" -> "Introduction: Tracing Changes through a Thousand Years"; modified body "(see Chapter 6)" dropped
- Images: the title bar reads "TRACING CHANGES THROUGH A THOUSAND YEARS" (old) and "INTRODUCTION: TRACING CHANGES THROUGH A THOUSAND YEARS" (new). The first page is otherwise as before. The cross-reference changes in the later hunks ("see Chapter 6" dropped, Chapters 6, 7, 8, 9, 10 becoming 5, 7, 6, 7, 8) are on pages 2 to 11, which I did not render, so they rest on the hunk text and on the known drop of two chapters.
- Verdict: real change
- Fix: none

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 3, printed page 30 (old) / 30 (new)
- Hunk: modified heading "THE DELHI SULTANS" -> "Understanding Delhi under the Sultans", inserted heading "delhI: 12th TO 15th CENTURY", similar for chapter 4: inserted heading "the mughals (16th TO 17th CENTURY)"
- Images: the old title bar reads "THE DELHI SULTANS". The new title bar reads "DELHI: 12th TO 15th CENTURY", all in capitals with the "th" set as superscripts. The title "Understanding Delhi under the Sultans" is the first section heading on page 32.
- Verdict: extraction fault (rule)
- Fix: pattern is the small-capital chapter titles of the 2023 edition coming out as lower-case or mixed-case ("delhI: 12th TO 15th CENTURY", "the mughals (16th TO 17th CENTURY)") with the superscript "th" kept as normal text. Seen in chapters 3 and 4 of 2023-12-23-rationalised (and the two chapters of the new edition have a chapter title that does not match the 2019 title, so the chapter title is also compared with the first section heading). A rule should upper-case the title in the title bar and treat superscript ordinal suffixes as part of the number. The same title in the same chapters of 2024-05-24 is affected.

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 1, printed page 14 (old) / 14 (new)
- Hunk: modified exercises "(a) Archives are places where ——————— are kept." -> "... where _______________ are kept." and (b), (c)
- Images: blank lines are printed as rules of different length ("———" and "_______"), the question text is the same.
- Verdict: engine noise
- Fix: none, same underscore and dash rule as in earlier pairs. Runs of "—" or "_" should collapse to a single blank token before comparison. Seen in chapter 1 page 14, chapter 7 (old) page 120 and chapter 8 (old) page 120, chapter 6 (old) page 102.

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 2, printed page 21 (old) / 21 (new)
- Hunk: modified body "One of the best known of such rulers is Sultan Mahmud of Ghazni, Afghanistan. He raided the subcontinent almost every year – ..." -> "One such ruler is Mahmud of Ghazni, Afghanistan. ... His targets were wealthy temples ..." and inserted body "He raided the subcontinent 17 times (1000–1025) with a religious motive."
- Images: the passage on page 21 is rewritten in the new edition as shown. The margin box "Sultan: an Arabic term meaning ruler" is gone from the new page, and the pointer "As we will see (pp. 62-66)" is gone too.
- Verdict: real change
- Fix: none

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 3, printed page 32 (old) / 32 (new)
- Hunk: modified body "Although inscriptions, coins and architecture provide a lot of information, especially valuable are “histories”, tarikh ..." -> "Histories are known as tarikh (singular)/tawarikh (plural), in Persian, ..."; deleted captions "Fig.1 Four stages in the making of a manuscript", and the note "Do you think the circle of justice is an appropriate term ..." moved
- Images: the old page opens with the heading "Finding Out about the Delhi Sultans" and the four manuscript miniatures A to D, while the new page opens with the heading "Understanding Delhi under the Sultans" and has no miniatures. The circle-of-justice box and the question box are on both pages, and the new page adds margin notes for "Birthright" and "Gender distinctions".
- Verdict: real change
- Fix: none

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 3, printed page 41 (old) / 35 (new)
- Hunk: deleted body and captions of the Alauddin Khalji and Muhammad Tughluq comparison table (suspect pages old 41, 43), and further deletions on old pages 32, 34, 35, 36 and 43
- Images: the old page is the two-column comparison table of Alauddin Khalji and Muhammad Tughluq. The new page 35 carries only running text about the iqta system, the kharaj tax and the limits of Delhi's control, and the table does not appear anywhere in the new chapter 3.
- Verdict: real change (the suspect flag is the deletion, no sentence survives)
- Fix: none

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 3, printed page 44 (old) / 38 (new)
- Hunk: modified exercises "12. Find out whether ..." -> "11. Find out whether ...", "11." -> "10.", "9." -> "8.", and "8. What was the impact of the Mongol invasions on the Delhi Sultanate?" -> "9. Raziyya Sultan was unique ..."
- Images: the old page has exercises 5 to 12, the new page has 5 to 11 (the Mongol question is missing, the later questions move up by one).
- Verdict: real change for the removed question. Engine noise for the pairings of "8." with "9.", which are a result of renumbering.
- Fix: none. A rule that ignores the leading exercise number when matching would remove the other hunks (chapter 3 page 44, chapter 4 pages 57 and 58, chapter 9 page 153).

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 4, printed page 47 (old) / 40 (new)
- Hunk: deleted body "Take a look at Figure 2, which is somewhat like a “group photograph”." and "Table 1 charts some of the major campaigns of the Mughals. ..." (seven sentences); modified captions "Fig. 4 Cannons ..." -> "Fig. 3 Cannons ...", "Fig. 3 Mughal army on campaign." -> "Fig. 2 ..."
- Images: the old page has Table 1 text and the Figure 2 pointer, a gunpowder note, and the figures 3 and 4. The new page has a new heading "Who were the Mughals?" with Figures 2 and 3 only, so the figures are renumbered and the Table 1 sentences are absent.
- Verdict: real change
- Fix: none. The following hunks are the same real change. Old pages 48 and 49 (Table 1, "Mughal emperors, major campaigns and events", about sixty sentences) have no counterpart in the new chapter 4. Old page 50 loses "Take a look at Table 1 once again. You will notice that" ("The Mughal rulers campaigned constantly ..." is what is left).

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 4, printed page 57 (old) / 46 (new)
- Hunk: modified exercises "Rathor Rajput Mewar" -> "Rathor Rajput rank", "Sisodiya Rajput Uzbeg" -> "Sisodiya Rajput Mewar", "Nur Jahan rank subadar Jahangir" -> "Nur Jahan Jahangir", "Mongol governor" -> "Mongol Uzbeg"; modified glossary and exercises renumbering (a) to (d) -> (a) to (c)
- Images: the match-the-following exercise has 6 pairs in 2019 (mansab/Marwar, Mongol/governor, Sisodiya Rajput/Uzbeg, Rathor Rajput/Mewar, Nur Jahan/rank, subadar/Jahangir) and 5 in the new edition (mansab/Marwar, Mongol/Uzbeg, Sisodiya Rajput/Mewar, Rathor Rajput/rank, Nur Jahan/Jahangir), the pair "subadar / governor" is removed and the right column moves up.
- Verdict: real change (the sixth pair is deleted), and extraction fault (rule) for the row reading, the same match-the-following table rule as in the first pair
- Fix: none new. The pairing hunks are the text of one table read row by row, not independent edits. The fill-in-the-blank items change from (a) to (d) to (a) to (c) because one blank was dropped.

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 7 (old) / 5 (new), printed page 101 (old) / 59 (new)
- Hunk: deleted body "The Mongols" and notes "Find Mongolia in your atlas." and eight more (the Elsewhere box); modified exercises "garh khel tanda ... paik KEYWORDS varna jati ..." -> "garh khel tanda ... paik", inserted exercises "Keywords varna jati tanda garh chaurasi barhot bhuiyans paik khel buranji census"
- Images: the old page 101 has the Elsewhere box "The Mongols" and the exercises start at the foot of the page, with the keywords in the margin of the next page. The new page 59 has the exercises with the margin column "KEYWORDS varna jati tanda garh chaurasi barhot bhuiyans paik khel buranji census" and the Mongols box is gone.
- Verdict: real change for the box. Extraction fault (rule) for the margin column read into an exercise line (the same rule as the OCR pair, "KEYWORDS ... glued into the exercise").
- Fix: none new

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 8 (old) / 6 (new), printed page 105 (old) / 62 (new)
- Hunk: modified body "At the same time, gods and goddesses worshipped in different areas came to be identified with Shiva, Vishnu or Durga." -> "... areas c a m e t o b e identified with Shiva, Vishnu or Durga."; inserted captions "The beginning of Bhakti Worship of certain deities, ..." (six sentences)
- Images: the new page 62 is set in narrow lines around the picture, so the justified lines are letter-spaced ("c a m e   t o   b e   identified" is spread out on the page). The words themselves are the same as the old page. The "The beginning of Bhakti" captions come from page 61 of the new edition, which I did not render, so that part rests on the hunk text only.
- Verdict: extraction fault (rule) for the spaced letters, real change for the new note
- Fix: pattern is justified text in a narrow column being set with wide letter-spacing, which the extractor reads as single letters separated by spaces. Seen in chapter 6 page 62 ("c a m e t o b e") and chapter 7 page 86 ("R e m e m b e r t h a t"). A rule should merge a run of three or more single letters back into a word, using the spacing between words (wider than the spacing between letters). Overrides
  - snapshot: "2023-12-23-rationalised", chapter: 6, find: "c a m e t o b e identified", replace: "came to be identified", note: "letter-spaced justified line on page 62, the words are 'came to be'"
  - snapshot: "2023-12-23-rationalised", chapter: 7, find: "R e m e m b e r t h a t", replace: "Remember that", note: "letter-spaced justified line on page 86"

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 9 (old) / 7 (new), printed page 128 (old) / 86 (new)
- Hunk: modified body "By the late seventeenth century this region had developed a bold and intense style of miniature painting called Basohli." -> "R e m e m b e r t h a t ordinary women and men painted as well — on pots, walls, floors, cloth — works of art that have century, this region had developed a bold and intense style of miniature painting called Basohli." and modified body "... breathed a new spirit into miniature painting." -> "... into miniature occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries."; inserted body "By the late seventeenth painting."
- Images: the new page 86 has a text block that wraps around Fig. 9 and then a paragraph "Remember that ordinary women and men painted as well – on pots, walls, floors, cloth – works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries." that is set to the right of the picture. The sentences of the main paragraph ("By the late seventeenth century, this region had developed ...", "... a new spirit into miniature painting.") are continuous in the page text. The extraction cuts the main paragraph at the figure ("By the late seventeenth", "painting.") and splices the Remember sentence into the middle of it.
- Verdict: extraction fault (rule)
- Fix: pattern is a paragraph wrapped around a figure whose second half sits to the right of the figure, so the reading order interleaves two paragraphs and splits a sentence ("By the late seventeenth ... century, this region", "... miniature ... painting."). Seen at chapter 7 page 86 and in the 2019 text at chapter 10 page 147 (old) / 98 (new). Same family as the "box set inside a wrapped paragraph" rule from the 2016 -> 2019 pair. Override
  - snapshot: "2023-12-23-rationalised", chapter: 7, find: "R e m e m b e r t h a t ordinary women and men painted as well — on pots, walls, floors, cloth — works of art that have century, this region", replace: "By the late seventeenth century, this region", note: "interleaved wrap around Fig. 9 on page 86, the Remember paragraph is a separate paragraph after the main one"
  (the pieces of the Remember sentence have to go in as a new paragraph, which an override with a plain find and replace cannot do alone. A rule is the better fix.)

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 10 (old) / 8 (new), printed page 147 (old) / 98 (new)
- Hunk: modified body "from the 1740s put severe pressure on these principalities ..." -> "Maratha campaigns into Rajasthan from the 1740s put severe pressure ..." and modified body "Maratha campaigns into Rajasthan Many Rajput chieftains built a number of forts ..." -> "Many Rajput chieftains built a number of forts ..."; deleted notes on Rajput forts and Jats in the deletions
- Images: the old 2019 page has the Rajput forts box (Fig. 4b) set inside the paragraph and the sentence split by it. The new page 98 has the whole sentence "Maratha campaigns into Rajasthan from the 1740s put severe pressure on these principalities and checked their further expansion." in one piece, and the fort box is gone.
- Verdict: extraction fault (rule) in the 2019 text (the box split the sentence), real change for the removed box
- Fix: none new. This confirms the 2016 -> 2019 chapter 10 page 147 entry from the other side, and shows the join is the correct form.

### our-pasts-2 2019-05-04 -> 2023-12-23-rationalised, chapter 10 (old) / 8 (new), printed page 153 (old) / 104 (new)
- Hunk: modified exercises "3. State whether true or false:" -> "1. State whether true or false:", "9. Do you think merchants ..." -> "4. ...", "12. Collect popular tales ..." -> "6. ...", "6." -> "2.", "10." -> "5.", "7." -> "3."
- Images: the exercises are fewer in the new edition (6 against 12) and are renumbered. The old page has the match-the-following and fill-in-the-blanks exercises, the new page does not.
- Verdict: real change
- Fix: none

## 2023-12-23-rationalised -> 2024-05-24

The 2024-05-24 reprint has the same wording as the 2023 printing on every page I rendered (the footer reads "Rationalised 2023-24" and "Reprint 2024-25"). Almost every hunk in this pair is an extraction fault in the 2024 text, because the reprint's text layer is out of order around figures and margin boxes, and the italic and spaced text comes out garbled. The real changes found are few: a new margin note on taxes in chapter 3, a new Lachit Barphukan box in chapter 5, and shortened headings. The live snapshot (live-2026-10-18) shares the 2024 text files, so every override below needs the snapshot label "2024-05-24" and the "live-2026-10-18" label as well.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 1, printed page 4 (old) / 4 (new)
- Hunk: modified body "Historians use different types of sources ... the period of their study and the nature of their investigation." -> "... the period of their study for and the nature of their investigation." and "Last year, for example, you read ..." -> "Last year, example, you read ..."
- Images: both pages carry the same paragraph "Historians use different types of sources to learn about the past depending upon the period of their study and the nature of their investigation. Last year, for example, you read about rulers of the Gupta dynasty and Harshavardhana." The word "for" sits at the end of a line, before "example".
- Verdict: extraction fault (rule)
- Fix: pattern is a word at the end of a line being moved to the line above in the 2024 text. Seen at chapter 1 page 4 ("study for and", "Last year, example"), page 5 ("not a Sometimes you cannot read your simple exercise"), page 9 ("and 'apparently fled", "Historians Gujarat regard"), page 13 ("copied ... Look out for changes and what you"), chapter 2 page 17 ("and so Sometimes they asserted their Of)"), page 18 ("compelled to Sometimes surrender"), page 25, page 26 ("in the way in was organised", "had which the sabha separate committees"), chapter 3 pages 35 and 37, chapter 4 pages 43 and 45, chapter 5 pages 50, 56 and 58, chapter 6 page 67, and chapter 7 page 83. The fragment that follows the break in the printed line is spliced into the line before. A rule should sort the words of a block by line and then by the horizontal position, and should not let a short last line of a paragraph precede its previous line. Overrides can only fix one place each. One example
  - snapshot: "2024-05-24", chapter: 1, find: "the period of their study for and the nature of their investigation. Last year, example, you", replace: "the period of their study and the nature of their investigation. Last year, for example, you", note: "line-end word moved to the line above in the 2024 text on page 4"

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 1, printed pages 4 and 5 (old) / 4 and 5 (new)
- Hunk: modified body "Through this period, paper gradually became cheaper and more widely available." -> "... cheaper and more Compare the following:" with inserted body "widely available."
- Images: the paragraph stops at "cheaper and more" and the purple "The value of paper" box follows on both pages. The sentence is finished on page 5.
- Verdict: extraction fault (rule)
- Fix: the box-title glue rule from the first pair (chapter 1 page 4 is also hit in the 2014, 2016 and 2022 OCR editions). The 2024 text drops the box title but keeps "Compare the following:".

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 1, printed page 9 (old) / 9 (new)
- Hunk: modified body "A Sanskrit prashasti (see Chapter 2 for an example of a prashasti ) praising the Delhi Sultan Ghiyasuddin Balban (1266-1287) explained that ..." -> "explained that he was the ruler ..." with inserted body "(see Chapter 2 for an example of a prashasti) praising the Delhi Sultan Ghiyasuddin Balban (1266-1287)"; modified body "... Tughluqs (Chapter 3) or Mughals (Chapter 4) encompassed many regions." -> "... Mughals (Chapter 4) A Ss sanskrit prashasti encompassed many regions."
- Images: the paragraph on page 9 reads continuously on both pages: "Large states like those of the Cholas (Chapter 2), Tughluqs (Chapter 3) or Mughals (Chapter 4) encompassed many regions. A Sanskrit prashasti (see Chapter 2 for an example of a prashasti) praising the Delhi Sultan Ghiyasuddin Balban (1266-1287) explained that ...". The italic "prashasti" is the cause: the 2024 text takes italic words out of the line and places them elsewhere.
- Verdict: extraction fault (rule)
- Fix: pattern is italic or emphasised words, and the text that follows them, being extracted as a separate run and reordered. The pieces here are "A Sanskrit prashasti" (read as "A Ss sanskrit prashasti" in the wrong sentence) and "(see Chapter 2 ...)". Seen at chapter 1 page 9, chapter 2 page 17 ("maha-samanta ,"), chapter 4 page 42 ("SQAUWAaT", "mUuq list ;"), chapter 5 page 54 ("Jats", "VaTTlas"), and chapter 6 pages 67, 71, 73. This is the same family as the line-end rule above, and the garbled spelling is in the next entry.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 2, printed page 26 (old) / 26 (new)
- Hunk: modified body "Associations of traders known as nagarams also occasionally performed administrative functions in towns." -> "... known as Ma Claims also ..." and modified body "Inscriptions from Uttaramerur ... the way in which the sabha was organised." -> "... the way in was organised."
- Images: both pages show the same three paragraphs, with "nagarams" in italics and "the sabha" in italics at the end of a line. The page has no "Ma Claims".
- Verdict: extraction fault (rule)
- Fix: italic words in the 2024 text are read through a second pass (OCR of the italic run), which produces garbled words ("Ma Claims" for "nagarams", "UT" for "ur", "mUuq list ;" for "muqtis", "SQAUWAaT" for "sawar", "balochis" for "sakhis", "Jats" for "jatis", "VaTTlas" for "varnas", "ASIA" for "rasa", "akbari" for "Varkari"). Seen in chapters 2 to 7 for italic terms. The vocabulary snapping step could replace them, but the better rule is to take the italic words from the text layer of the page instead of the second pass. One example
  - snapshot: "2024-05-24", chapter: 2, find: "known as Ma Claims also", replace: "known as nagarams also", note: "italic word garbled by the italic second pass on page 26, the page reads nagarams"

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 3, printed page 31 (old) / 31 (new)
- Hunk: modified body "Chauhans 1165 –1192" -> "Chauhans 1165 1192 Prithviraj Chauhan", "Tomaras Early twelfth century –1165" -> "Tomaras Early twelfth century 1165 Ananga Pala", "Alauddin Khalji 1296 –1316" -> "Alauddin Khalji", "Lodi Dynasty 1451–1526" -> "LODI DYNASTY Bahlul Lodi"; inserted body "Qutbuddin Aybak 1206 –1210 Shamsuddin Iltutmish Raziyya Ghiyasuddin Balban KHALJI DYNASTY ..."
- Images: "The Rulers of Delhi, Table 1" is the same on both pages: every dynasty has its rulers and every date range has its en dash ("1165–1192", "1296–1316").
- Verdict: extraction fault (rule)
- Fix: pattern is the text of a panel with a coloured gradient: the date range loses its en dash, a date range is left behind in the wrong line, and ruler names move to the line above ("Chauhans 1165 1192 Prithviraj Chauhan"). Seen at chapter 3 page 31 only. A rule should read the panel row by row (by the vertical position), and keep en dashes. This table is a one-page panel, so an override of the whole panel is possible but long.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 3, printed page 35 and 36 (old) / 35 and 36 (new)
- Hunk: inserted notes "There were also other Taxes levied–", "1. Khums 2. Zakat 3. Jizyah", "1. Khums was Consisted of one-fifth of war booty ...", and ten more sentences; inserted body "Ibn Battuta, a fourteenth-century traveller from Morocco ... deified themselves lives in mounting, ..."; modified source "In India the bamboo is not hollow; it is big." -> "In hindi fia the bamboo is pala places as well not holy low; it is big."
- Images: page 36 has a new margin note in the 2024 edition: a text about taxes (Khums, Zakat, Jizyah) with the source "U.N. Day, 1959, Administrative system of Delhi Sultanat, Kitab Mahal Publishers", set in orange italic. The 2023 page has no such note. The "Chieftains and their fortifications" box is the same on both pages (italic quotation, not garbled).
- Verdict: real change for the tax note. Extraction fault (rule) for the box: the second pass of the italic quotation produces duplicate garbled sentences ("Ibn Battuta ... deified themselves lives in mounting", "Its several parts are so interacted that even fierce cannot y felt them") and the garbled words in the source hunks ("slab slave", "exp fame", "persistence", "cult do own the by power")
- Fix: the italic second-pass rule above. The garbled duplicates are the 2024 reading of italic box text that is also in the correct form in the same chapter. A rule should drop a second-pass line when the first-pass text contains it. Seen at chapter 3 pages 34 and 36, chapter 6 pages 63 and 66 ("This is an abhang ... He who wide titles fentif"), chapter 5 page 57.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 39 (old) / 39 (new)
- Hunk: inserted heading "R extremely difficult task for any ruler to accomplish in", modified body "Ruling as large a territory ..." -> "uling as large a territory ... was an the Middle Ages."
- Images: the chapter's first paragraph on both pages begins with a large drop capital "R" ("Ruling as large a territory as the Indian subcontinent ... an extremely difficult task for any ruler to accomplish in the Middle Ages."). The drop capital is at the margin and the third line wraps round it.
- Verdict: extraction fault (rule)
- Fix: the drop capital rule. The big first letter is cut from the first word and put in the heading, with the line that wraps round the letter ("extremely difficult task ... accomplish in") moved up. Seen at chapter 4 page 39 ("R extremely difficult task..." heading and "uling as large"), chapter 5 page 49 (heading "Y crafts and production activities flourished in towns", body "ou saw in Chapters 2, 3 and 4") and chapter 7 page 80 ("T he first literary works"). Same pattern as the OCR pair (chapter 1 "ake a look", chapter 7 "F = Yo saw"). Overrides
  - snapshot: "2024-05-24", chapter: 5, find: "ou saw in Chapters 2, 3 and 4", replace: "You saw in Chapters 2, 3 and 4", note: "drop capital Y lost on page 49"
  - snapshot: "2024-05-24", chapter: 4, find: "uling as large a territory", replace: "Ruling as large a territory", note: "drop capital R lost on page 39"
  The headings "R extremely difficult task for any ruler to accomplish in" and "Y crafts and production activities flourished in towns" must also be removed (the text moves back into the paragraph).

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 4, printed page 42 (old) / 42 (new)
- Hunk: modified body "The mansabdar's military responsibilities required him to maintain a specified number of sawar or cavalrymen." -> "... a specified number of SQAUWAaT or cavalrymen." and "But unlike muqtis, ..." -> "But unlike mUuq list ;, ..."
- Images: both pages show "sawar" and "muqtis" in italics in the same lines. The new page has an identical layout (the "Zat ranking" box at the left).
- Verdict: extraction fault (rule) (the italic second pass)
- Fix: same rule as above. One-off overrides
  - snapshot: "2024-05-24", chapter: 4, find: "SQAUWAaT", replace: "sawar", note: "italic word garbled on page 42"
  - snapshot: "2024-05-24", chapter: 4, find: "mUuq list ;,", replace: "muqtis,", note: "italic word garbled on page 42"

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 49 (old) / 49 (new)
- Hunk: see the previous entry (drop capital)
- Images: the same opening page: title bar "TRIBES, NOMADS AND SETTLED COMMUNITIES", a drop capital "Y" before "ou saw in Chapters 2, 3 and 4", the QR code and Fig. 1 in the margin.
- Verdict: extraction fault (rule)
- Fix: drop capital rule

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 5, printed page 57 (old) / 57 (new)
- Hunk: inserted notes "Lachit Barphukan and the defeat of the Mughals in Assam" and captions "Lachit Barphukan, the Ahom his war skills and'excellent use battle." and "Source: Janasanyog Assam, Decorated of I information Public Relations, Government of Assam, Dispur, Gujarati."; modified body "However, the Ahoms faced many invasions ..." and so on
- Images: the 2024 page has a new orange box "Lachit Barphukan and the defeat of the Mughals in Assam" with a statue picture and a text about the Battle of Saraighat (1671), with the source "Janasanyog Assam, Directorate of Information & Public Relations, Government of Assam, Dispur, Guwahati". The 2023 page has a blue question box "Discuss why the Mughals were interested in the land of the Gonds." in its place.
- Verdict: real change for the box. Extraction fault (rule) for the garbled caption and the garbled source (the italic second pass).
- Fix: italic rule. One-off overrides can only be written after the text of the box is re-read from the page, which I did not do for the whole box.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 6, printed page 62 (old) / 62 (new)
- Hunk: modified heading "A New Kind of Bhakti in South India – Nayanars and Alvars" -> "Bhakti in South India – Nayanars and Alvars"; modified body "... gods and goddesses c a m e t o b e identified ..." -> "... gods and goddesses w or shi pped in different areas c a m e t o b e identified with Shi va, Vish n u or Durga."
- Images: the heading reads "A New Kind of Bhakti in South India – Nayanars and Alvars" (2023) and "Bhakti in South India – Nayanars and Alvars" (2024). The narrow justified column round the figure is letter-spaced in both ("c a m e   t o   b e").
- Verdict: real change for the heading. Extraction fault (rule) for the broken words ("w or shi pped", "Shi va", "Vish n u").
- Fix: the letter-spacing rule from the previous pair (chapter 6 page 62 in 2023 and 2024). The 2024 text adds breaks inside words. Override
  - snapshot: "2024-05-24", chapter: 6, find: "w or shi pped in different areas c a m e t o b e identified with Shi va, Vish n u or Durga.", replace: "worshipped in different areas came to be identified with Shiva, Vishnu or Durga.", note: "letter-spaced column on page 62 read as broken words"

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 6, printed page 69 (old) / 69 (new)
- Hunk: modified caption "Fig. 5 A page from a manuscript of the Quran, Deccan, late fifteenth century." -> "... Deccan, late eighteenth-century."; modified body "It had a long line of teachers like ..." -> "Iqtadar long line of teachers like ..."
- Images: both pages show the caption "Fig. 5 A page from a manuscript of the Quran, Deccan, late fifteenth century." and the paragraph "The Chishti silsila was among the most influential orders. It had a long line of teachers like Khwaja Muinuddin Chishti of Ajmer ...". There is no "Iqtadar" and no "eighteenth".
- Verdict: extraction fault (one-off)
- Fix: overrides
  - snapshot: "2024-05-24", chapter: 6, find: "Deccan, late eighteenth-century", replace: "Deccan, late fifteenth century", note: "OCR misreading in the Fig. 5 caption on page 69, the page reads late fifteenth century"
  - snapshot: "2024-05-24", chapter: 6, find: "Iqtadar long line of teachers", replace: "It had a long line of teachers", note: "italic word 'silsila' garbled and the line start replaced on page 69, the page reads 'It had a long line of teachers'"
  (check for the exact context of the second one in the file before use.)

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 6, printed page 66 and 71 (old) / 66 and 71 (new)
- Hunk: modified source "He who identifies with the battered and the beaten ..." -> "This is an abhang (Marathi devotional hymn) of Sant Tukaram: He who wide titles fentif with the battered ..."; modified notes "The essence of Shankaradeva's devotion came to be known as Eka Sarana Nama Dharma ..." -> "devotion came to Eka best-known Sarana Nama Dharma ..." and "His major compositions included Kirtana-ghosha." -> "H is ma or composed actions included Kirtana-ghosha"
- Images: page 66 shows the box "Questioning the social order" with the same lines in both editions ("This is an abhang (Marathi devotional hymn) of Sant Tukaram:" followed by the italic verse, then the Chokhamela's son abhang). The verse is clean on both pages. I did not render page 71, so the two note hunks from page 71 rest on the pattern.
- Verdict: extraction fault (rule) (the italic second pass)
- Fix: italic rule

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 7, printed page 86 (old) / 86 (new)
- Hunk: modified body "By the mid-eighteenth century the Kangra artists developed a style which breathed a new spirit into miniature occasionally survived, unlike the miniatures ..." -> "works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries." and body "R e m e m b e r t h a t ordinary women and men painted as well — on pots, walls, floors, cloth — works of art that have century, this region ..." -> "R e m e m b e r t h a t ordinary women ... cloth."; inserted body "By the late seventeenth century, this region had developed ..." and "By the mid-eighteenth century the Kangra artists developed ... miniature painting."
- Images: the layout of page 86 is the same in both editions (Fig. 8 above, the Kangra paragraph and Fig. 9 beside it, and the letter-spaced "Remember that ... works of art that have" line at the foot). The 2024 text cleans up the splice of the two paragraphs that the 2023 text had, so the 2024 reading is nearer to the page.
- Verdict: extraction fault (rule) in the 2023 text. The 2024 reading is better.
- Fix: none new. The 2023 splice is described under "2019-05-04 -> 2023-12-23-rationalised, chapter 9 (old) / 7 (new), printed page 128 / 86". The letter-spaced "R e m e m b e r t h a t" remains in 2024 and needs the letter-spacing rule.

### our-pasts-2 2023-12-23-rationalised -> 2024-05-24, chapter 1, printed page 14 and 15 (old) / 14 and 15 (new)
- Hunk: modified exercises "2. State whether true or false:" -> "State whether true or false:", "(a) We do not find inscriptions for the period after" -> "We do not find inscriptions for the period after 700.", "7. How were the affairs of jatis regulated?" -> "7. How were the affairs of regulated?", and similar for exercises 8 and 9
- Images: pages 14 of both editions are identical: numbered questions 1 to 4 with lettered sub-items, the KEYWORDS margin column (manuscript, jati, region, periodisation) at the left, and blanks printed as short rules. Page 29 (chapter 2) likewise has the same questions 7 to 12 and the same KEYWORDS column (samanta, temple, nadu, sabha) on both. The numbers and the "700." that the 2024 text drops are on the pages.
- Verdict: extraction fault (rule)
- Fix: the numbering of the exercises and the italic word are lost in the second pass. Seen at chapter 1 pages 14 and 15, chapter 2 page 29 ("9." and "8." dropped), chapter 3 pages 37 and 38, chapter 4 page 47 ("9.", "8.", "3." dropped and "(a)" lost from the fill-in-the-blanks), chapter 5 page 60 ("-based society" for "varna-based"), chapter 6 page 77. Also the margin KEYWORDS words are shuffled into the exercise list (chapter 2 page 29 "KEYWORDS temple" and "samanta nadu sabha", chapter 3 page 38 "KEYWORDS garrison" and "iqta tarikh", chapter 4 page 47 "mansab jagir zat sawar sulh-i kul zabt"). See the margin-column rule of the OCR pair.

## Summary

Entries written: 95, each from a rendered pair of page images (old and new side by side). Counts by the leading verdict of each entry (an entry with a mixed verdict is counted under the first part): extraction fault (rule) 39, real change 37, engine noise 13, extraction fault (one-off) 6. Entries per pair are 22 (2014 -> 2016), 28 (2016 -> 2019), 16 (2019 -> 2022 OCR), 13 (2019 -> 2023) and 13 (2023 -> 2024), so the target of 25 to 40 was met only for 2016 -> 2019. The OCR pair and the 2024 pair are dominated by a few repeating patterns, so I judged by pattern and listed every place instead of imaging every hunk. Not every place in a list was rendered. Places named from hunk text only are marked as such in their entries (chapter 6 page 71, chapter 1 pages 2 to 11 of 2019 -> 2023, and chapter 6 page 61).

Findings that matter for trusting the counts:
- 2014 -> 2016 and 2016 -> 2019 hold the real wording edits (spelling, dates, rewritten sentences, a new Suleyman box replacing Queen Elizabeth, Baba Guru Nanak, Orissa to Odisha, a rewritten Hyderabad paragraph). Most other hunks there are 2014 faults (left margin clipped on the chapter 5 PDF) and 2016 faults (box titles glued into text).
- 2019 -> 2022 OCR: I found no real change on any page I compared. Every hunk I judged was an OCR fault or a stream difference.
- 2019 -> 2023: two chapters dropped, the Table 1 panels in chapters 3 and 4 removed, exercises cut and renumbered, and figure numbers shifted. These are real.
- 2023 -> 2024: wording is the same on every page I compared. The real changes are the new tax note in chapter 3, the Lachit Barphukan box in chapter 5 and a shortened heading in chapter 6.

The three patterns that would remove the most noise if fixed by a rule:
1. The italic and emphasised text in the 2024-05-24 files (and its live snapshot), plus words at the end of a line, being read out of order or garbled. This gives "SQAUWAaT" for "sawar", "Ma Claims" for "nagarams", a fragment spliced into the line above ("study for and the nature", "so Sometimes they asserted their Of)"), and duplicate garbled copies of the quotations in boxes. It affects nearly all of the hunks of 2023 -> 2024 and would also fix the 2024 side of every later pair. The fix is to take italic words from the same text layer as the rest of the line and to drop a second-pass line when the first pass already holds it. Places: chapters 1 to 7, pages 4, 5, 9, 13, 17, 18, 25, 26, 34, 35, 36, 42, 43, 45, 50, 54, 56, 57, 58, 63, 66, 67, 71, 73, 75 (chapter 3 pages 34 and 36, chapter 4 page 42, chapter 5 page 57, chapter 6 pages 63 and 66 were the ones I viewed).
2. A box title, margin column or drop capital being attached to the wrong unit. Box titles are glued to the next sentence ("The value of paper Compare the following:", "Nur Jahan's influence in Jahangir's court Mehrunnisa married ...", "Bronze, bell metal and the lost wax technique Temple authorities used ...", "Temple Construction in the Early Eleventh Century Two technological ..."), the "KEYWORDS" margin column is glued into an exercise line (chapter 1 page 14, chapter 3 page 44, chapter 4 pages 57 to 59, chapter 7 page 59), the drop capital is cut from its word and its line moves up ("R extremely difficult task ...", "ou saw", "T he first literary", "ake a look"), and the second line of the chapter title is glued to the first body sentence. This runs through every edition and makes the "widely available." deletion and insertion pair that recurs in four pairs. The fix is to read title bars, the margin column and the drop capital as separate blocks.
3. Fills and exercise layout read differently between editions: blanks printed as dashes or underscores of different lengths, numbered exercises with their numbers detached or shifted, and match-the-following tables read by columns instead of rows. This gives dozens of small modified hunks in the exercises and glossary streams in every pair (chapter 1 page 14, chapter 3 page 44, chapter 4 pages 57 and 58, chapter 7 page 120, chapter 10 page 153). The fix is to collapse runs of "_" and dashes to one blank token, to compare an exercise without its leading number, and to read a two-column table by rows.

Runners-up, each smaller: letter-spaced justified lines ("c a m e t o b e", "R e m e m b e r t h a t", chapter 6 page 62 and chapter 7 page 86), a text box inside a wrapped paragraph that splits a sentence (chapter 10 page 147 in 2019 and chapter 7 page 86), text read from inside maps and figures in the OCR edition, and the 2014 chapter 5 PDF with a clipped left margin (pages 60 to 70, 72).
