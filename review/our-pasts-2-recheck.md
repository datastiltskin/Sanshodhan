# Recheck after the rule change: our-pasts-2 (Our Pasts II, Class 7 history)

Input: review/changes-our-pasts-2.txt (2368 changed sentences). Method: for each edition and chapter, the listed printed pages were rendered from the edition's own PDF (page markers in the Markdown) and compared with the new text. Pages are named by printed number. Editions 2014-07-28, 2016-09-10 and 2019-05-04 share most chapter PDFs (the same file hash for chapters 2, 3, 6 to 10 in the first two), so a verdict on one applies to the other where the page was identical, and this is said where used. The earlier review is review/our-pasts-2.md.

Short form for entries: book our-pasts-2, then edition, chapter, printed page. "Match" means the new text agrees with the page.

Note on "2018-partial": the change list has a block for 2018-partial (chapters 1, 3, 4, 9 and prelims, all "+", marked "new file"). That text is not in texts/our-pasts-2 and not in HEAD, only a snapshot name under edition 2019-05-04 in the manifest. There is nothing to compare, so the block is "not viewed" (one entry).

## 2014-07-28

Common change in all chapters: the margin "KEYWORDS" word list is no longer glued into exercise lines. The "-" lines (KEYWORDS plus words) now reappear as a "### Keywords" heading and one word per line, and the exercise sentences that used to be cut by it are whole.

### our-pasts-2 2014-07-28, chapters 1, 2, 3, 4, 7, 8, 9, 10, printed pages 14, 29, 44, 58, 102, 120, 136, 153
- Hunk: "- KEYWORDS ..." lines gone, "+ Keywords / word / word" new, "~ p120 Virashaivism bhakti -> Virashaivism", "~ p57 1. Match the following mansab Marwar -> 1. Match the following"
- Images: each page shows the margin box "KEYWORDS" with the words in a column. The words are all in the new text, none lost. p120 shows "Virashaivism, bhakti, Sufi, khanqah" as four words, so the split is right.
- Verdict: matches the page
- Fix: none

### our-pasts-2 2014-07-28, chapter 1, printed page 14
- Hunk: "~ Choose one of the themes ... -> such as economic ..." and "+ Choose one of the / themes mentioned in this chapter,"
- Images: the "Imagine" box is a magenta paragraph of six lines. The new text splits it into three lines ("Choose one of the", "themes mentioned in this chapter,", then the rest). The words are all there.
- Verdict: extraction fault (rule)
- Fix: pattern, "Imagine" box text set in a narrow shaped column is broken at line ends into separate paragraphs. Seen at chapter 1 page 14, chapter 3 page 43 ("You are a peasant in Alauddin Khalji's" / "or Muhammad Tughluq's reign ..."), chapter 5 page 73 (artisan on a platform in 2016), chapter 6 page 88 ("You are planning a journey from Surat" / "to West Asia ..."), in 2014, 2016 and 2019. Rule: join consecutive lines of one coloured text block of the same size and colour into one paragraph. All words survive, so this only changes sentence counts.

### our-pasts-2 2014-07-28, chapter 2, printed page 24
- Hunk: "+ p24 To find out how these images were made, see Chapter 6."
- Images: the page has this sentence as a second caption below Fig. 4.
- Verdict: matches the page (it was merged into another unit before).
- Fix: none

### our-pasts-2 2014-07-28, chapter 3, printed page 31
- Hunk: "+ Firuz Shah Tughluq's tomb"
- Images: caption below the Table 1 panel, as on the page. Table rows show dates with stray spaces before the dash ("1165 -1192") but dates are all there.
- Verdict: matches the page
- Fix: none

### our-pasts-2 2014-07-28, chapter 3, printed page 33
- Hunk: "- Gender distinctions Social and biological differences between women and men." "- Usually, these differences ..." and "+ Gender distinctions ... Usually, ..."
- Images: the orange "Gender distinctions" definition is one note of two sentences. The new unit has both sentences. Nothing lost.
- Verdict: matches the page
- Fix: none

### our-pasts-2 2014-07-28, chapter 3, printed page 37
- Hunk: "- Mosques also helped to create the sense of a community of believers who shared ..." and "+ Mosques also helped ... believers" and "+ who shared a belief system and a code of conduct."
- Images: the paragraph runs "Mosques also helped to create the sense of a community of believers", then the Fig. 4 caption sits in the text column, then "who shared a belief system and a code of conduct. It was necessary ...". So the page itself interrupts the sentence with a picture caption. The new text keeps the caption out of the sentence but breaks the sentence in two units. The words are on the page.
- Verdict: extraction fault (rule)
- Fix: pattern, a figure caption set inside the text column splits a sentence into two units. Rule: when a body unit ends without a full stop and the next body unit starts lower case after a caption, rejoin them. Seen at chapter 3 page 37 (2014, 2016, 2019), chapter 4 page 43 and 5 page 62 (Fig. 4 caption cut by the question, see 2019).

### our-pasts-2 2014-07-28, chapter 3, printed page 43
- Hunk: "~ You are a peasant in Alauddin Khalji 's or Muhammad Tughluq's reign ... -> or Muhammad Tughluq's reign ..." and "+ You are a peasant in Alauddin Khalji 's"
- Images: one magenta Imagine paragraph, "You are a peasant in Alauddin Khalji's or Muhammad Tughluq's reign and you cannot pay the taxes demanded by the Sultan. What will you do?"
- Verdict: extraction fault (rule), see the Imagine pattern above. Words kept.
- Fix: see pattern

### our-pasts-2 2014-07-28, chapter 4, printed page 54
- Hunk: "- Dogma A statement ... Bigot An individual ..." and "+ Bigot ..." "+ Dogma ..."
- Images: two orange glossary notes at the head of the page, Dogma above Bigot. Now two units, one each, in the wrong order (Bigot first) but whole.
- Verdict: matches the page (order differs only in the sentence list, the Markdown has Dogma first).
- Fix: none

### our-pasts-2 2014-07-28, chapter 4, printed page 57
- Hunk: "- Nur Jahan Babur subadar rank" and "+ Nur Jahan Babur" "+ mansab Marwar" "+ subadar rank"
- Images: the match-the-following table has two columns, six rows (mansab / Marwar, Mongol / governor, ...). The new text reads row by row, two items per line. The rows were previously spilling into the next page. Now they stay on p57.
- Verdict: matches the page (the pairs are by row)
- Fix: none. This clears the "match the following" pattern of the earlier review for this page.

### our-pasts-2 2014-07-28, chapter 5, printed pages 66 and 68
- Hunk: "~ ar bagh a arden at -> ar bagh a arden at ari, 1637." and "~ ura ra hard aced in ns o marble ... -> ura hard aced ..."
- Images: the 2014 chapter 5 PDF has its left margin clipped, so captions are tails of words. The page cannot be read as it stands. The new text is still unreadable, only differently so.
- Verdict: extraction fault (rule) (unreadable page, unchanged pattern)
- Fix: same as the earlier review (treat as unreadable). Also seen at pages 60, 62, 64, 70, 72 in 2014 chapter 5.

### our-pasts-2 2014-07-28, chapter 5, printed page 73
- Hunk: "- Go through the chapter and make your own list of six keywords." and "+ Go through the" "+ chapter and make" "+ six keywords." "+ For each of these," ...
- Images: the keyword box on this page is a yellow note that says "Go through the chapter and make your own list of six keywords. For each of these, write a sentence indicating why you chose the word." The new text splits it at every line end, one list item per line.
- Verdict: extraction fault (rule)
- Fix: pattern, a free-text instruction placed in the Keywords margin box is read line by line as keywords. Rule: a Keywords box whose lines end with a full stop or have more than three words per line is a note, joined into one paragraph. Seen at chapter 5 page 73 in 2014, 2016 and 2019. Override for each edition (snapshot label, chapter 5): find "- Go through the\n- chapter and make\n> [note] your own list of\n- six keywords.\n> [note] For each of these,\n- write a sentence\n- indicating\n- why you chose\n- the word." replace "> [note] Go through the chapter and make your own list of six keywords. For each of these, write a sentence indicating why you chose the word." note "free-text box in the Keywords column on page 73".

### our-pasts-2 2014-07-28, chapter 6, printed pages 77 and 83
- Hunk: "- Bronze, bell metal and the "lost wax" technique Temple authorities used their wealth ..." now "+ Bronze, bell metal and the "lost wax" technique" and "+ Temple authorities used their wealth to finance trade and banking."; "+ Hampi." at p83
- Images: p77 has the box title in a teal bar and the paragraph "Temple authorities ..." under the box. They are now separate. p83: "Fig. 7 Stone chariot, Vitthala temple, Hampi." is one caption.
- Verdict: matches the page. The glued box title of the earlier review is gone for 2014.
- Fix: none

### our-pasts-2 2014-07-28, chapter 6, printed page 87
- Hunk: "~ Fig. 8 A Bombay street, early nineteenth -> ... century."
- Images: caption "Fig. 8 A Bombay street, early nineteenth century."
- Verdict: matches the page

### our-pasts-2 2014-07-28, chapter 6, printed pages 88 and 89
- Hunk: "~ (b) Merchants preferred to travel individually rather than in caravans. -> (b) ... individually", "+ rather than in caravans.", and similar for (a), (c), (d); "- Vishwakarma emporium" and "+ Vishwakarma" "+ emporium"
- Images: the True/False items are printed with a forced line break ("... architect of the / Rajarajeshvara temple from an inscription."). The new text keeps the line break as a unit break. Words are all present. Keywords: five words in a column, all present.
- Verdict: extraction fault (rule)
- Fix: pattern, items in a numbered or lettered list where the printed line is short (a column narrower than the page) are cut at the line end into two units. Rule: a unit that starts lower case and follows a lettered item is a continuation of it. Seen at chapter 6 page 89 and chapter 6 page 88 (Imagine) in 2014, 2016, 2019, chapter 1 page 14 (2022).

### our-pasts-2 2014-07-28, chapter 7, printed pages 101 and 102
- Hunk: "- garh khel tanda chaurasi ... KEYWORDS varna jati ..." and "+ garh khel" "+ tanda chaurasi" ... "+ Keywords ..."
- Images: p101 shows the Match the following table (six rows, two columns) and p102 the Keywords column. The old text had the table fused with the keywords. Now apart and complete.
- Verdict: matches the page

### our-pasts-2 2014-07-28, chapter 8, printed page 120
- Hunk: "- Nizamuddin Auliya questioned social differences Nayanars Sufi saint Alvars worship of Shiva" and "+ Nayanars Sufi saint" etc.
- Images: table rows, two per line in the page. All present.
- Verdict: matches the page

### our-pasts-2 2014-07-28, chapter 9, printed page 123
- Hunk: "~ Fig. 2 ... palm-leaf manuscript, -> ... Orissa."
- Images: the caption ends "Orissa." Match.
- Verdict: matches the page

## 2016-09-10

The chapters 2, 3 (except p37 text), 6, 7, 8, 9 and 10 pages in the list were compared by text with 2014 on the same PDF (identical pages: ch7 p101, p102, ch8 p120, ch9 p123, p136, ch10 p153, ch3 p31, p33, p44) and rendered for 2016. All entries given for 2014 for these pages apply and are not repeated, with these differences.

### our-pasts-2 2016-09-10, chapter 1, printed page 3
- Hunk: "~ New and Old Termi New and Old Terminologies nologies -> New and Old Termi New and Old Terminologies"
- Images: the page shows one heading, "New and Old Terminologies". The new text is "## New and Old Termi New and Old Terminologies", still doubled (half the doubled copy was removed).
- Verdict: extraction fault (one-off)
- Fix: override
  - snapshot: "2016-09-10"
  - chapter: 1
  - find: "## New and Old Termi New and Old Terminologies"
  - replace: "## New and Old Terminologies"
  - note: "doubled text layer in the heading on page 3, page shows only 'New and Old Terminologies'"

### our-pasts-2 2016-09-10, chapter 1, printed pages 4 and 5
- Hunk: "- Through this period paper gradually became cheaper and more The value of paper Compare the following:", "- p5 widely available.", "+ Compare the following:", "+ The value of paper", "+ Through this period paper gradually became cheaper and more widely available."
- Images: p4 ends "... cheaper and more" then the teal-barred box "The value of paper"; p5 begins "widely available." The new text has the sentence whole across the page break and the box title and "Compare the following:" as their own units.
- Verdict: matches the page. The earlier "box title glued to a sentence, widely available inserted" pattern is gone here.
- Fix: none

### our-pasts-2 2016-09-10, chapter 3, printed page 37, chapter 4 page 54
- Hunk: as 2014 p37 (caption inside sentence). ch4 p54: "~ Nur Jahan's influence in Jahangir's court Mehrunnisa married ... -> Mehrunnisa married ..." and "+ Nur Jahan's influence in Jahangir's court"
- Images: p37 as in 2014. p54 has the teal bar "Nur Jahan's influence in Jahangir's court" over the text box "Mehrunnisa married the Emperor ...". Now separate.
- Verdict: p37 extraction fault (rule) as above, p54 matches the page.
- Fix: none for p54

### our-pasts-2 2016-09-10, chapter 4, printed pages 57 and 58
- Hunk: "- Rathor Rajput Mewar Nur Jahan rank subadar Jahangir KEYWORDS Mughal mansab ..." and "+ Rathor Rajput Mewar Nur Jahan rank" "+ subadar Jahangir" and keywords split
- Images: match table rows (six) and the Keywords column. Present. In the 2016 text the table rows are two to a line but all there.
- Verdict: matches the page

### our-pasts-2 2016-09-10, chapter 4, printed page 57 (text, Kings and queens box)
- Hunk: not in the list, seen while viewing: "Shah Abbas (1588-1629); ; and the more controversial"
- Images: the page has "(1588-1629); and the more controversial". Double semicolon.
- Verdict: extraction fault (one-off)
- Fix: override
  - snapshot: "2016-09-10"
  - chapter: 4
  - find: "(1588-1629); ; and"
  - replace: "(1588-1629); and"
  - note: "doubled semicolon from the box rule on page 57"

### our-pasts-2 2016-09-10, chapter 5, printed page 62
- Hunk: "- Temple Construction in the Early Eleventh Century What differences do you notice ...?" and "+ Temple Construction in the Early Eleventh Century" "+ What differences do you notice between the shikharas of the two temples?"
- Images: the title "Temple Construction in the Early Eleventh Century" is a bold italic heading over the Kandariya Mahadeva text, and the question box is a separate blue note. Now separate.
- Verdict: matches the page

### our-pasts-2 2016-09-10, chapter 5, printed page 65
- Hunk: "- Importance of water" and "~ ... invaded Sri Lanka and defeated the king, Sena I ( -> ... defeated the Importance of water king, Sena I ("
- Images: the margin note "Importance of water" (a glossary-like note, "The Persian terms abad ... derived from the word ab") is in the column beside the text. Its title word sits inside the sentence "defeated the king, Sena I". The title is not a sentence of the paragraph.
- Verdict: extraction fault (one-off) (it is the same fault in 2016 and 2019, one place)
- Fix: override, one per snapshot
  - snapshot: "2016-09-10" and again "2019-05-04"
  - chapter: 5
  - find: "defeated the Importance of water king, Sena I"
  - replace: "defeated the king, Sena I"
  - note: "margin note title 'Importance of water' glued into the sentence on page 65"
- The title itself should appear as a heading of the note on the same page. Not checked what the note text now looks like beyond the line "The Persian terms abad ..." which sits on the page and is present.

### our-pasts-2 2016-09-10, chapter 5, printed page 73
- Same as 2014 p73 (keyword box). Also "+ You are an artisan standing on a tiny" / "+ wooden platform held together by" / "+ bamboo and rope fifty metres above the ground." is the Imagine pattern.
- Verdict: extraction fault (rule), see the two patterns above.

### our-pasts-2 2016-09-10, prelims
- Hunk: "~ I N T H I S B O O K -> IN THIS BOOK", "~ ` 50.00 -> ₹ 50.00", "- Kothari, Sunil." "~ Kathak: Indian Classical Dance Art -> Kothari, Sunil. Kathak: ...", "+ Reetu Singh, Lecturer, DESS, NCERT, New Delhi", "+ These are to remind you of important ideas/ themes introduced There is a lot to read ... in the lesson."
- Images: p13 "In this book" page: the Keywords box reads "At the end of each chapter, you will find a list of keywords. These are to remind you of important ideas/ themes introduced in the lesson." and "There is a lot to read, see, think about and do in this book. We hope you will enjoy it." is a separate paragraph under it. The new text interleaves them and puts "in the lesson." as a bullet. The price, heading and the reference line "Kothari, Sunil. Kathak ..." (credits page 10) are right. "Reetu Singh" is on the credits page.
- Verdict: matches the page for the heading, price, credits. The Keywords box sentence is an extraction fault (rule).
- Fix: pattern, a centred box in a bordered frame is split by the line order. Seen in prelims of 2016, 2019, 2022, 2023, 2024. One override per snapshot in prelims: find "These are to remind you of important ideas/ themes introduced There is a lot to read, see, think about and do in this book. We hope you will enjoy it." replace "These are to remind you of important ideas/ themes introduced in the lesson." note "Keywords box, text interleaved with the closing line". The closing line "There is a lot to read, see, think about and do in this book. We hope you will enjoy it." then has to be added as its own paragraph. Also "- in the lesson." (a list bullet) is to be removed.

## 2019-05-04

Same chapters and pages as 2016 on equal PDFs (chapters 2, 3, 6 and 9 mostly differ in text only by small real edits: ch2 p24 "Agriculture and Irrigation" capitals, ch3 p31 row formats with real "1165-1192" and "###" row headings, ch6 p88 Vasco da Gama rewritten, ch6 p83 Domingo Paes box typed as source, ch10 p153 "Asaf Jah founded the Hyderabad state" and "Awadh state"). All viewed pages agree with the new text.

### our-pasts-2 2019-05-04, chapters 1, 2, 3, 4, 7, 8, 9, 10, printed pages 14, 29, 44, 58, 101, 102, 120, 136, 153 and the Keywords lists
- Verdict: matches the page, same as 2014/2016. Viewed 14, 24, 29, 31, 43, 57, 88, 89, 146, 147, 153 and the other keyword pages as one montage.

### our-pasts-2 2019-05-04, chapter 3, printed page 43 and chapter 6, printed pages 88 and 89
- Imagine split as above (extraction fault (rule)). p89 lettered items split (extraction fault (rule)). The old "- (a) We know the name of the architect of the Rajarajeshvara temple from an inscription." is now two units joined by the page's own line break.

### our-pasts-2 2019-05-04, chapter 5, printed page 62
- Hunk: "~ Temple Construction in the Early Eleventh Century Two technological ... -> Two technological ..." and "~ The path started more than 4 km away ... -> 4 km away ..." and "+ The path started more than"
- Images: the Fig. 4 caption reads "... The path started more than 4 km away so that it would not be too steep. This was dismantled after the temple was constructed ... Charupallam, the "Village of the Incline"." In the page the caption runs on both sides of the blue question. The new text breaks it at "more than" and continues with "4 km away" after the question note, so the question interrupts the caption in the text. Words complete.
- Verdict: extraction fault (rule) (same family as the caption inside a sentence above)
- Fix: see pattern "caption inside a sentence". The "Two technological ..." line is on p63 in the edition, the "~" only shows that the title is no longer glued, which matches the page.

### our-pasts-2 2019-05-04, chapter 10, printed pages 146 and 147
- Hunk: "~ Maratha campaigns into Rajasthan Many Rajput chieftains built ... -> Many Rajput chieftains ..." and "~ from the 1740s put severe pressure ... -> Maratha campaigns into Rajasthan from the 1740s put ..." and "+ Fig. 5 Mehrangarh Fort, Jodhpur"
- Images: p146 ends the Watan jagirs section with "Maratha campaigns into Rajasthan from the 1740s put severe pressure on these principalities and checked their further expansion." (the first words were the margin title of an orange note on p147). The new text rejoins the sentence. The p147 note starts "Many Rajput chieftains built a number of forts ...". Fig. 5 caption is on the page.
- Verdict: matches the page. The earlier "text box set inside a wrapped paragraph, chapter 10 page 147" pattern is gone here.
- Fix: none

### our-pasts-2 2019-05-04, prelims
- As 2016. Also "~ Imagine -> Imagine", "- Raq" (stray token gone, good), "- cla erfar FAA SR TERT fap sty f1aToT WATIONAL COUNCI OF EDUCATIONAL RESEARCH AND" -> "+ VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND".
- Images: the title page (pdf 3) carries a logo with the words "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING" in the NCERT emblem band, set in a stylised font. The text reads "VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND", a misreading (V for N, a letter lost).
- Verdict: extraction fault (one-off)
- Fix: override per snapshot (2019-05-04, 2022-08-04, 2023-12-23, 2024-05-24; prelims)
  - find: "VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND"
  - replace: "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING"
  - note: "emblem lettering misread on the title page"
  (The word TRAINING is on the emblem; I did not check that it is on the same line, so check the override against the page before use.)

## 2022-08-04-ocr

Images: pages 1, 4, 11, 14 (ch1), 20, 24, 25, 26, 27, 28 (ch2), 32, 34, 35, 36, 37, 43, 44 (ch3), 46 to 50, 52, 53, 57 (ch4), 62 to 64, 71 (ch5), 77, 79, 82, 83 (ch6), 92, 94, 95, 98 (ch7), 109, 115, 119, 120 (ch8), 128, 130, 132, 135, 136, 137 (ch9), 146, 147 (ch10) were rendered. Pages in the list not viewed: ch7 p99, p100, p101 text, ch8 p105, p113, ch9 p131, ch4 p58, ch6 p87 (see Summary).

### our-pasts-2 2022-08-04-ocr, chapter 1, printed page 1
- Hunk: "~ A THOUSAND YEARS ake a look at Maps 1 and 2. ... -> ake a look at Maps 1 and 2." and "+ A THOUSAND YEARS"
- Images: the title is two lines "TRACING CHANGES THROUGH / A THOUSAND YEARS" in a bar, and the opening paragraph starts with a drop capital T. The title is now apart from the paragraph (good). The drop capital "T" is still missing ("ake a look"), and "1154 ce" should be "1154 CE".
- Verdict: extraction fault (one-off) for the drop capital
- Fix: override
  - snapshot: "2022-08-04"
  - chapter: 1
  - find: "ake a look at Maps 1 and 2. Map 1 was made in 1154 ce"
  - replace: "Take a look at Maps 1 and 2. Map 1 was made in 1154 CE"
  - note: "drop capital T and small-capital CE lost on page 1"
  - Pattern (rule) of the earlier review "drop capital lost" persists in 2022 (page 1 ch1) but is fixed in 2024 (ch4 p39 "Ruling", ch5 p49 "You saw", ch7 p80 "The first").

### our-pasts-2 2022-08-04-ocr, chapter 1, printed pages 4, 11, 14
- Hunk: "~ Through this period paper gradually became cheaper and more The value of paper Compare the following: -> ... more The value of paper", "+ Compare the following:", "+ a noble."; "- (d) Sultan Ghiyasuddin Balban controlled Assam," "- periodisation Manipur and Kashmir." "+ (d) Sultan Ghiyasuddin Balban controlled Assam, periodisation Manipur and Kashmir."
- Images: p4: the box title "The value of paper" is still glued to the end of the paragraph sentence, and "widely available." is on p5. p11: Patron note, "a noble." was cut off into a caption, now sentences agree but it is split into two units. p14: the margin words "periodisation" are inside exercise (d), and the exercise list has the KEYWORDS title and words "manuscript, jati, region" inside (a), (b), (c). The page has all the words in the margin column, and (d) ends "Manipur and Kashmir."
- Verdict: extraction fault (rule)
- Fix: pattern, "margin column interleaved by reading order" (earlier review) still present in the OCR edition, p14 ch1 (KEYWORDS, manuscript, Jati, region, periodisation inside (a) to (d)), ch3 p44 (the Keywords words are one note "iqta tarikh garrison Mongols gender" plus "kharaj"), ch4 p58 ("(b) The five Deccan Sultanates were Berar, Khandesh, KEYWORDS Ahmadnagar, and"), ch9 p136 ("NSA"). The gain here is that (d) now reads as one unit but with "periodisation" in it. Rule: OCR blocks inside the left margin column (x less than the text column) are the Keywords column.

### our-pasts-2 2022-08-04-ocr, chapter 2, printed pages 20, 24, 25
- Hunk: "~ List all the possible sources of irrigation mentioned @ Unusual for the twelfth century ... -> Unusual for ...", "+ List all the possible sources of irrigation mentioned @", "+ One particularly"; p24 "- In the delta region embankments ... canals had to be constructed to y= — To find out how these images were made, see Chapter 6." then "+ In the delta region embankments ... constructed to In many cases it was necessary to water crops artificially. ..." and "+ y= — To find out how these images were made, see Chapter 6."; "- p25 In many cases it was necessary to water crops artificially."
- Images: p20: the question "List all the possible sources of irrigation mentioned in the inscription, and discuss how these might have been used." is the blue note, now split as a fragment "... mentioned @" and the rest "in the inscription ..." in a table note. "One particularly" is the last words of the p20 text and "prized area was the city of Kanauj" is on the next page. p24: the paragraph ends "canals had to be constructed to carry water to the fields. In many areas two crops were grown in a year." with "carry water to the fields ..." on p25. The new text puts the first sentence of the p25 paragraph into p24 ("constructed to In many cases it was necessary to water crops artificially. A variety ...") and drops the p25 lead. The word order is wrong: "In many cases it was necessary to water crops artificially." is the first sentence of the second paragraph on p24 (page 25 starts "carry water to the fields. In many areas two crops were grown in a year.") and is correct, but it is inserted in the middle of the first. "y= —" is a stray symbol from the picture, the caption sentence is on the page.
- Verdict: extraction fault (rule) for the p24 sentence order, extraction fault (one-off) for the stray symbol.
- Fix: override
  - snapshot: "2022-08-04"
  - chapter: 2
  - find: "canals had to be constructed to In many cases it was necessary to water crops artificially. A variety"
  - replace: "canals had to be constructed to carry water to the fields. In many areas two crops were grown in a year.\n\nIn many cases it was necessary to water crops artificially. A variety"
  - note: "page 24 text column ends at 'carry water to the fields' (the line continues on the page after the picture)"
  I did not check how "carry water to the fields. In many areas two crops were grown in a year." on p25 reads after the change, so the author of the fix should remove the duplicate on p25.

### our-pasts-2 2022-08-04-ocr, chapter 2, printed pages 26, 27, 28
- Hunk: "- vellanvagai land of non-Brahmana peasant proprietors brahmadeya land gifted to Brahmanas devadana ... " and "+ vellanvagai land of non-Brahmana peasant proprietors", "+ brahmadeya land gifted to Brahmanas", "+ devadana, tirunamattukkani land gifted to temples", "+ pallichchhandam land donated to Jaina institutions", "+ We have seen that Brahmanas often received land grants or brahmadeya." ; "- Inscriptions and texts inscription lays down:" -> "+ Inscriptions and texts" "+ inscription lays down:"; "- Gurjara-Pratiharas Western Deccan Rashtrakutas Bengal Palas Gujarat and Rajasthan Cholas Tamil Nadu" -> two rows per line
- Images: p26 box "Types of land" has the five categories and "shalabhoga land for the maintenance of a school" (kept in the Markdown as a table note, not in the changed list). Rows are all there. p27: "Inscriptions and texts" is the box title and "Who could be a member of a sabha? The Uttaramerur inscription lays down:" the first line. Match words present, the title split from the sentence is right but "Who could be a member of a sabha? The Uttaramerur" sits in a table note apart. p28: match table four rows, two lines.
- Verdict: matches the page. Remaining small OCR errors on p27 ("Rnowledge", "1s collected", "Pulatyas") are the unchanged confusion pattern of the earlier review.
- Fix: none for the changed lines. The "k to R" confusion still needs a snap rule (see Summary).

### our-pasts-2 2022-08-04-ocr, chapter 3, printed pages 32, 34, 35, 36, 37
- Hunk: "~ This happens when the king d his subjects? promotes justice and honest governance. and his subjects? -> d his subjects? promotes justice ..." and "+ This happens when the king"; "- Ip Dewal Benaras @ LAKHNAUTI ... In the early thirteenth century the control of the Delhi Sultans rarely went beyond heavily fortified towns occupied by garrisons." then "+ In the early thirteenth century ... garrisons." and "+ Ip Dewal Benaras ... Muslims came from a Fig-5 ; iety. of Mosque of Jamali backgrounds. la..." ; p35 "- VS ; Dwarasamydrae ..." and "+ VS ; Dwarasamydrae ... "; "+ p36 The Masjid A mosque is called a masjid in Arabic, ..."; p37 "- It was necessary to reinforce this idea of a community because Muslims came from a Fig-5 ; iety. of Mosque of Jamali variety O Kamali, built in the backgrounds." and "- who shared a belief system and a code of conduct." and "+ It was necessary to reinforce this idea of a community because", "+ system and a code of conduct.", "+ variety O Kamali, built in the", "+ who shared a belief"
- Images: p32: the "circle of justice" box ends "This happens when the king promotes justice and honest governance." and the blue question beside it is "Do you think the circle of justice is an appropriate term to describe the relationship between the king and his subjects?" The OCR sentence is interleaved with the question words ("d his subjects?"). Still wrong. p34 and p35: the map pictures are read as noise (words like "Ip Dewal Benaras @ LAKHNAUTI"), and "Muslims came from a Fig-5 ; iety. of Mosque of Jamali backgrounds. late 1520s." on p34 is text from p37 (the mosque paragraph) moved onto p34's map caption. The p36 sentence "The Masjid A mosque is called a masjid in Arabic, literally a place where a Muslim prostrates in reverence to Allah." is the orange box text (the heading "The Masjid" glued to the text) and is on the page. p37: the orange text runs in two columns around the two mosque photographs, so "Mosques also helped / to create the sense of a community of believers / who shared a belief / system and a code of conduct. It was necessary to reinforce this idea of a community because / variety of backgrounds" are in three chunks. The new text keeps "variety O Kamali, built in the" which mixes the "variety of backgrounds." with Fig. 5's caption. All words are in the text but the sentence is broken.
- Verdict: extraction fault (rule) for p32, p34, p35, p37. The p36 line matches the page.
- Fix: patterns. (1) Text from inside pictures (maps) is kept as captions: p34, p35 chapter 3 (earlier review pattern, still present, no change). (2) Text wrapped around pictures is interleaved with captions: p37 here, ch4 p52 (Fig. 7 caption spliced), ch5 p63 and p64, ch6 p82 and p83, ch7 p95 and p98, ch9 p130 and p132, ch9 p135. Rule: when a sentence is cut by a caption or note, flow the text by column and keep the caption as its own unit. Override for p37 (snapshot "2022-08-04", chapter 3) is possible, find "It was necessary to reinforce this idea of a community because\n\n> [caption] ..." but the order in the Markdown is not stable. Not given.

### our-pasts-2 2022-08-04-ocr, chapter 3, printed pages 43 and 44
- Hunk: "- Imagine", "- The "Three Orders" ... Knights and the Crusades The idea of the "Three Orders" was first formulated ..." and "~ You are a peasant ... -> The "Three Orders", the "Peace of God", Knights and the Crusades Imagine You are a peasant ...", "+ The idea of the "Three Orders" was first formulated ..."; p44 "~ KEYWORDS iqta tarikh garrison Mongols gender kharaj According to the "circle of justice", ... -> According to ..." and "+ Keywords" "+ iqta tarikh garrison Mongols gender" "+ kharaj"
- Images: p43: the Elsewhere box title and the Imagine title run in sequence, the new text writes both titles and "Imagine" before "You are a peasant ...". The Imagine line is wrong. The Elsewhere box text then comes separate (good). p44: all words present. Exercise numbers 5, 9, 12 are detached ("> [caption] 5.") but the sentences are whole. "Keywords" title no longer in the exercise (an improvement).
- Verdict: p43 extraction fault (rule), p44 matches the page for the sentences.
- Fix: the box title glued to the next title is the "box title glued" pattern, ch3 p43 and ch9 p135. Rule: a title bar is the first line of its box.

### our-pasts-2 2022-08-04-ocr, chapter 4, printed pages 46 to 49
- Hunk: many "~" and "+" lines: "~ On the other hand, the Mughals were A miniature painting (dated 1702-1712) ... -> A miniature painting ..." and "~ proud of their Timurid ancestry ... -> On the other hand, the Mughals were proud of ...", "~ (1) 1556-1570 —- Akbar became independent of the regent Bairam Khan ... -> Bairam Khan and other members ...", "+ (1) 1556-1570 —- Akbar became independent of the regent", "~ _ (2) In Iran Humayun received help from the Safavid Shah. 4 § He recaptured Delhi ... -> 4 § He recaptured ...", "+ ‘", "+ E"
- Images: p46/47: the paragraph "On the other hand, the Mughals were proud of their Timurid ancestry ..." runs across the page and the new text joins it correctly. p48 (Table 1): the panel is a parchment sheet with three rulers' texts. The new text still splits "Akbar became independent of the regent / Bairam Khan" into two paragraphs, has "Rana anges" for "Rana Sanga", "ye an accident" for "after an accident", "his: brother", "Anmadnagar", and two stray tokens "‘" and "E". p49: a garbage heading "## oe), eee wn" and stray "E", "yo Safavid Iran", "cama himself", the Aurangzeb paragraph cut into five "table" units with two "##" headings made from OCR noise lines.
- Verdict: extraction fault (rule) for the panel split and noise headings, extraction fault (one-off) for each misread.
- Fix: patterns: OCR noise lines in a picture region become headings (ch4 p49, ch5 p62 "Gl", ch8 p115 "## E, es i Beyond the Rana's palace", ch3 p32 "## aire 2 Gi fein 2 te"). Rule: a line with more than 40 per cent non-dictionary tokens is never a heading. The Table 1 panel needs the row-by-ruler split (earlier review: OCR panel).
  Overrides (snapshot "2022-08-04", chapter 4): find "defeated Rana anges Rajput rulers" replace "defeated Rana Sanga, Rajput rulers"? Not used, the exact text in the Markdown is "defeated Rana anges Rajput rulers and allies at Khanua" and the page reads "defeated Rana Sanga, Rajput rulers and allies at Khanua". Override: find "defeated Rana anges Rajput rulers and allies at Khanua." replace "defeated Rana Sanga, Rajput rulers and allies at Khanua." note "OCR misread on page 48". And find "died the next year after ye an accident in this building." replace "died the next year after an accident in this building." note "stray OCR token on page 48".

### our-pasts-2 2022-08-04-ocr, chapter 4, printed pages 50, 52, 53
- Hunk: "- Mughal marriages with the Rajputs" and "~ princess, daughter of the Rajput ruler of Amber (modern-day Jaipur). -> Mughal marriages with the Rajputs princess, daughter of the Rajput ruler of Amber (modern-day Jaipur)."; "~ Each province was divided into revenue circles ... -> divided into revenue circles ...", "+ Each province was", "~ ~-.» used one term - zamindars - to describe all intermediaries ... ->", "~ The most interesting aspect about the Ain-i Akbari is its rich Fig.7 statistical details about things as diverse as = Akbar recieving the Akbar Nama crops, yields, prices, wages and revenues. -> ~-.» used one term - zamindars - to describe all statistical details about ...", "+ and keep very careful accounts."
- Images: p50: the margin box "Mughal marriages with the Rajputs" has a teal title and the text "The mother of Jahangir was a Kachhwaha princess, daughter of the Rajput ruler of Amber (modern-day Jaipur). The mother of Shah Jahan was a Rathor princess ...". The new text glues the title to "princess, daughter ..." and leaves "The mother of Jahangir was a Kachhwaha" as a caption. p52: the new text puts the Ain-i Akbari box text ("statistical details about things as diverse as crops, yields ...", which is on p53) in the middle of the sentence "The Mughals used one term - zamindars - to describe all intermediaries" and prefixes the stray "~-.»". The p53 sentence is therefore cut. The sentences "divided into revenue circles ..." and "It was prevalent ... survey the land / and keep very careful accounts." are cut at the page break, as on the page, with the p53 rest in a separate unit.
- Verdict: extraction fault (rule) (box title glued, caption words spliced into body)
- Fix: pattern above. One-off override (snapshot "2022-08-04", chapter 4): find "~-.» used one term - zamindars - to describe all statistical details about things as diverse as = Akbar recieving the Akbar Nama crops, yields, prices, wages and revenues. from Abul Fazl.\nintermediaries" replace "used one term – zamindars – to describe all\nintermediaries" note "Ain-i Akbari box text from page 53 spliced into page 52". The Markdown may have different line breaks, so the find string must be taken from the file.

### our-pasts-2 2022-08-04-ocr, chapter 4, printed page 57
- Hunk: "~ Find out more about Akbar's other contemporaries - the ruler of Imagine You have inherited a kingdom. -> ... the ruler of", "+ Imagine", "+ You have inherited a kingdom.", "~ How would you make your kingdom stable and prosperous? -> your kingdom stable and prosperous?", "+ How would you make"
- Images: the Elsewhere box ends with the question "Find out more about Akbar's other contemporaries - the ruler of England, Queen Elizabeth I ..." and below it the magenta Imagine box. The new text splits the question at "the ruler of" with "England ..." in a later table unit, and splits the Imagine paragraph.
- Verdict: extraction fault (rule) (Imagine pattern and notes split at line ends)
- Fix: see patterns.

### our-pasts-2 2022-08-04-ocr, chapter 5, printed pages 62, 63, 64, 71
- Hunk: p62: "- So the architects ' built an inclined path to the top of the temple, What differences do you notice between the shikharas ..." and "+ So the architects ' built an inclined path ... rolled it all the way to the top." "+ What differences do you notice ...?" ; "~ This was dismantled after the temple was constructed. -> ..." ; p63 "~ Notice how the names A royal architect of the ruler and the god are very similar." "~ The "keystone" at: the centre of the arch transferred Compare Figures 2a and the weight of the superstructure ... -> ... Compare Figures 2a and the weight of the superstructure" "+ 2b with Figures 5a and 5b. to the base of the arch." "~ This architectural form was called "arcuate". _A "true" arch. -> form was called ..." "+ This architectural"; "- A royal architect"
- Images: p62: caption for Fig. 4 and the question are now separate units (match). p63: the Fig. 5a caption ("A "true" arch. The "keystone" at the centre of the arch transferred the weight of the superstructure to the base of the arch.") and the blue question ("Compare Figures 2a and 2b with Figures 5a and 5b.") are interleaved with the sentence "(1) The weight of the superstructure above the doors and windows was sometimes carried by arches. This architectural form was called "arcuate"." Text is spliced. p64: "A royal architect" is the margin box title, and the text beside it reads "of the ruler and the god are very similar." The new text pastes the title inside the sentence "Notice how the names A royal architect of the ruler and the god are very similar."
- Verdict: extraction fault (rule) for p63 and p64, p62 matches the page. p71 matches the page ("Region and Empire", Fig. 16).
- Fix: patterns above. Override (snapshot "2022-08-04", chapter 5): find "Notice how the names A royal architect of the ruler and the god are very similar." replace "Notice how the names of the ruler and the god are very similar." note "margin box title 'A royal architect' glued into the sentence on page 64 (the sentence starts at the foot of page 63)". Same family as the 2016 and 2019 "Importance of water" override.

### our-pasts-2 2022-08-04-ocr, chapter 6, printed pages 77, 79, 82, 83
- Hunk: p77 "- Bronze, bell metal and the "lost wax" technique Bronze is an alloy containing copper and tin." and "+ Bronze is an alloy ...", "+ Bronze, bell metal and the "lost wax" technique"; p79 "- Sugar and jaggery, dyes, thread, and cotton, On coconuts, salt, areca nuts, butter, sesame oil, Besides, there were taxes on traders, ..." and "+ Sugar and jaggery, dyes, thread, and cotton," "+ On coconuts, salt, areca nuts, butter, sesame oil," "+ Besides, there were taxes ..."; p82 "- A Closer Look: Hampi, Masulipatnam and Surat The Architectural Splendour of Hampi Hampi is located ..." and "+ Hampi is located in the Krishna-Tungabhadra basin ...", "+ The Architectural Splendour of Hampi"; "~ This is how a Portuguese traveller, Domingo Paes, Vijaynagara rulers described Hampi in the sixteenth century: took keen -> A Closer Look: Hampi, Masulipatnam and Surat A fortified city This is how a Portuguese traveller, Domingo Paes, Vijaynagara rulers described Hampi in the sixteenth century: took keen interest in" ; p83 "- A fortified city" "- During their rule, the" "- building tanks and canals." "+ During their rule, the building tanks and canals."
- Images: p77, p79 match the page (the tax list is three lines "Sugar and jaggery, dyes, thread, and cotton, / On coconuts, ... / On cloth."). p82: the section title "A Closer Look: Hampi, Masulipatnam and Surat" is a teal heading over "The Architectural Splendour of Hampi" and the text; the "A fortified city" box is on p83. The new text moves "A Closer Look: ... A fortified city This is how a Portuguese traveller, Domingo Paes, ..." together at the end of the p82 box "The changing fortunes of towns", and mixes the margin note "During their rule, the Vijayanagara rulers took keen interest in building tanks and canals" into the Paes line. p83: the Domingo Paes text is interleaved with the orange margin note about Anantraj Sagar and the figure caption.
- Verdict: p77 and p79 match the page, p82 and p83 extraction fault (rule)
- Fix: the "box title glued" and "margin note interleaved" patterns above (ch6 p82, p83).

### our-pasts-2 2022-08-04-ocr, chapter 7, printed pages 92, 94, 95, 98
- Hunk: p92 "~ The Balochis were another large and powerful p-oN ~ ) KHOKHARS z= JANJUHAS ..." -> "p-oN ~ ) KHOKHARS ... "; "+ The Balochis were another large and powerful"; p94 "- _* Nomadic pastoralists moved over long distances with their animals." and "+ _* Nomadic pastoralists moved over" "+ long distances with their animals."; p95 "- Peter Mundy, an English trader who came to India during the early seventeenth century, has described the Banjaras: In the morning we met a tanda of Banjaras with 14,000 oxen." ... "+ Peter Mundy, an English trader who came to India" "+ The Banjaras the Banjaras: In the morning we met a tanda of Banjaras with14,000 oxen." "+ during the early seventeenth century, has described"; p98 "- Dalpat, however, died early." "- His son, Dalpat, married princess Durgawati, the daughter of Salbahan, the Chandel Rajput raja of Mahoba." and "+ His son, Dalpat, married princess Durgawati, the daughter of Dalpat, however, died early." "+ Salbahan, the Chandel Rajput raja of Mahoba."
- Images: p92: the first words of the map picture are read as a long string of OCR noise attached to "The Balochis were another large and powerful" (map text from p93, no change). p94: the heading "How Nomads and Mobile People Lived" and the run-in bold words "Nomadic pastoralists" are fine except for the stray "_*" symbol, and the sentence split in two. p95: the Banjaras box title, the first words "Peter Mundy ..." and the quote are interleaved: the new text has "The Banjaras the Banjaras: In the morning ..." (the title repeated), "with14,000". p98: the paragraph wraps round Fig. 6 so the right-hand piece "princess Durgawati, the daughter of Salbahan, the Chandel Rajput raja of Mahoba." is interleaved with "Dalpat, however, died early." The words are present.
- Verdict: extraction fault (rule)
- Fix: wrapped text and box title patterns. Override for p98 (snapshot "2022-08-04", chapter 7): find "His son, Dalpat, married princess Durgawati, the daughter of Dalpat, however, died early.\n\nSalbahan, the Chandel Rajput raja of Mahoba." replace "His son, Dalpat, married princess Durgawati, the daughter of Salbahan, the Chandel Rajput raja of Mahoba.\n\nDalpat, however, died early." note "paragraph wraps round Fig. 6 on page 98". The exact paragraph breaks must be checked in the file.

### our-pasts-2 2022-08-04-ocr, chapter 7, printed page 101
- Hunk: "~ Imagine community that shifts residence every three months. -> community that shifts residence every", "+ Imagine", "+ three months."; "- garh khel clan Garha Katanga Sib Singh Ahom state Durgawati paik KEYWORDS The mentions that Garha Katanga had 70,000 villages." and "+ garh khel" "+ clan Garha Katanga Sib Singh Ahom state Durgawati paik", p102 "+ The mentions that Garha Katanga had 70,000 villages." "+ Keywords"
- Images: not viewed for p101 and p102 of the OCR edition in the rendering, but the 2014 pages carry the same table and the Keywords. The OCR text has the Imagine split and the blank in "The ____ mentions that Garha Katanga had 70,000 villages." lost (the blank dashes are dropped).
- Verdict: not viewed (OCR edition p101, p102)
- Fix: none. The blank-token rule of the earlier review is still needed (also ch1 p14 "Archives are places where are kept").

### our-pasts-2 2022-08-04-ocr, chapter 8, printed pages 109, 115, 119, 120
- Hunk: p109 "- He who identifies with the battered and the beaten Mark fim as a saint For God is with him Every forsaken man ..." and "+ He who identifies", "+ with the battered and the beaten Mark fim as a saint", "+ For God is with him", "+ Every forsaken man Close to his heart He treats", "+ A slave", "+ As his own son", "+ Says Tuka", "+ to repeat again", "+ Is God", "+ In person."; "~ Here is an abhang composed by Chokhamela's son: You made us low caste, Why don't you face that fact, Great Lord? -> ... You made us low caste," "+ Why don't you face that fact, Great Lord?"; p115 "- And yet Rana why have you Rept up enmity against me?" "+ enmity against me?" ; p119 "~ He encouraged the use of the language of ordinary people rather than Latin, and translated Key ga ag Se 7 qt the Bible into German. -> ... and translated" "+ Key ga ag Se 7 qt the Bible into German."; p120 "~ (b) Ramanuja was influenced by the Describe the beliefs ..." "+ (b) Ramanuja was influenced by the" "- KEYWORDS"
- Images: p109 box: the verse lines are all there. "Mark fim" is "Mark him" on the page. p115: "kept" is OCR'd "Rept" twice (the k to R confusion), and the box title "Beyond the Rana's palace" became "## E, es i Beyond the Rana's palace" (noise word). p119: the page reads "Luther felt that several practices in the Roman Catholic Church went against the teachings of the Bible. He encouraged the use of the language of ordinary people rather than Latin, and translated the Bible into German." The OCR gives a noise string "Key ga ag Se 7 qt" for the second half of the picture-wrapped lines ("went against the teachings of the Bible. He encouraged ... translated the"). Words "went against the teachings of the Bible. He encouraged the use of the language of ordinary people rather than Latin, and translated" are in other units, the connecting part is lost. p120: all items match the page. The Imagine and Keywords are right.
- Verdict: p109, p120 match the page (except "fim", "Rept" one-off), p115 and p119 extraction fault (one-off)
- Fix: override (snapshot "2022-08-04", chapter 8): find "Mark fim as a saint" replace "Mark him as a saint" note "OCR h read as f on page 109"; find "have you Rept up" replace "have you kept up" note "OCR k read as R on page 115" (two places, replace all); find "translated Key ga ag Se 7 qt the Bible into German." replace "translated the Bible into German." note "noise from the picture on page 119"; find "## E, es i Beyond the Rana's palace" replace "## Beyond the Rana's palace" note "noise words before the box title on page 115".

### our-pasts-2 2022-08-04-ocr, chapter 9, printed pages 125, 128, 130, 132, 135, 136, 137
- Hunk: p128 "~ Painting for Patrons: The Tradition of Miniatures Another tradition ... -> Another tradition ..." and "+ Painting for Patrons: ..."; p130 "- (south Bihar), which may have led to the growing influence of Sanskrit." and "+ (south Bihar), which may have led to the growing Maynamati, Gopichandra and" and "+ influence of Sanskrit." p131; "~ A Closer Look: Bengal The Growth of a Regional Language As we saw ... -> As we saw ..." and "+ A Closer Look: Bengal The Growth of a Regional Language"; p132 "- Maynamati, Gopichandra and" "- This particular song, which was often enacted, described how Maynamati, a queen, encouraged her son ..." and "+ This particular song ... encouraged her" "+ son Gopichandra to adopt the path ..."; p135 "- The Brihaddharma Purana ... Emergence of nation-states in Europe Till the eighteenth ..." "+ The Brihaddharma Purana, ... Emergence of nation-states in Europe You are a Raj..." "+ Till the eighteenth century, ..."; p136 "- Match the following: NSA Anantavarman Kerala ..." "+ Match the following: NSA Anantavarman Kerala" "+ Jagannatha Bengal" etc.; p137 "~ Why did conquerors try to control the temple of Jagannatha at Puri?" split, "- Why do we know much more about the cultural practices ..." split.
- Images: p128 matches. p130: the box title of the Maynamati box (which sits on p132, not p131) is in the p130 sentence ("growing Maynamati, Gopichandra and") (box title glued into a sentence). The sentence on the page is "may have led to the growing influence of Sanskrit." across the page break, so the glue has to be removed. p132: the box is "Maynamati, Gopichandra and Dharma Thakur" with the song text; the new text has it right apart from a break after "encouraged her". p135: the "Emergence of nation-states in Europe" title is glued to the next page's Imagine ("You are a Rajput prince" is p136) text. p136: the "Keywords" margin column's top triangle is read as "NSA" and added to "Match the following: NSA Anantavarman Kerala". Imagine belongs to the top of p136. p137: numbers detached ("5." etc.), sentences broken at line ends, but the words are right.
- Verdict: extraction fault (rule) for p130, p135, p136. p128, p132, p137 match the page for the words.
- Fix: overrides (snapshot "2022-08-04", chapter 9): find "growing Maynamati, Gopichandra and" replace "growing" note "box title from page 132 glued into the sentence on page 130" (and then the sentence is continued on the next page, "influence of Sanskrit."); find "Match the following: NSA Anantavarman Kerala" replace "Match the following: Anantavarman Kerala" note "stray OCR token 'NSA' from the margin triangle on page 136".

### our-pasts-2 2022-08-04-ocr, chapter 10, printed pages 146 and 147
- Same as 2019 chapter 10: matches the page. p153 Keywords match.
- Verdict: matches the page

### our-pasts-2 2022-08-04-ocr, prelims
- As 2019. "+ MEMBER-COORDINATOR" is the page's heading. The NCERT emblem line reads "VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND", see the 2019 override.

## 2023-12-23-rationalised

All viewed pages match.

### our-pasts-2 2023-12-23-rationalised, chapter 1, printed page 14
- Hunk: "~ (a) We do not find inscriptions for the period after -> ... after 700." "~ 4. List some of the technological changes associated with -> ... with this period." "- 700." "- this period." "- Keywords manuscript jati region periodisation" and "+ Keywords ..."
- Images: (a) ends "after 700." and (4) ends "associated with this period." The Keywords are four words. 
- Verdict: matches the page. The fault of the earlier review (the numbered exercises and "700." dropped in the second pass) is gone here.

### our-pasts-2 2023-12-23-rationalised, chapter 2, printed pages 24, 28, 29
- Hunk: "+ p24 Notice how carefully it is decorated." "~ p28 2. Who were the parties involved in the "tripartite -> ... struggle"?" "- struggle"?" "- p29 Keywords samanta temple nadu sabha"
- Images: p24 caption "Fig. 4 A Chola bronze sculpture. Notice how carefully it is decorated." p28 question 2 is whole. p29 Keywords: four words (samanta, temple, nadu, sabha).
- Verdict: matches the page. Item 12 on p29 is split into two lines ("12. Find out more about taxes that are collected at present." / "Are these in cash, kind, or labour services?") which the page shows as one wrapped item (minor, same unit family as above).

### our-pasts-2 2023-12-23-rationalised, chapters 3, 4, 5, 8, printed pages 38, 47, 59, 104
- Hunk: Keywords lists split into words; "~ 3. Why did the Marathas want to expand beyond the -> ... Deccan?" "+ Fig. 5 Mehrangarh Fort, Jodhpur" (p99)
- Images: p99 shows the Fig. 5 caption beside the fort. p104 the question reads in full. 
- Verdict: matches the page

### our-pasts-2 2023-12-23-rationalised, chapter 6, printed pages 62, 69, 77
- Hunk: "~ ... worshipped in different areas c a m e t o b e identified ... -> ... came to be identified ..." "+ p69 Fig. 6 Devotees of all backgrounds visit Sufi shrines." "~ Virashaivism bhakti -> Virashaivism"
- Images: p62: the justified text in the narrow column reads "came to be identified with Shiva, Vishnu or Durga" (letter-spaced). Now fixed. p69 Fig. 6 caption is on the page.
- Verdict: matches the page. The letter-spacing pattern of the earlier review is gone for chapter 6.

### our-pasts-2 2023-12-23-rationalised, chapter 7, printed page 86
- Hunk: "~ R e m e m b e r t h a t ordinary women and men painted as well — on pots, walls, floors, cloth — works of art that have century, this region ... -> Remember that ordinary women and men painted as well — on pots, walls, floors, cloth — works of art that have century, this region ..."
- Images: the page has the sentence "Remember that ordinary women and men painted as well – on pots, walls, floors, cloth – works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries." in a narrow column beside Fig. 9, and above it the Kangra paragraph. The new text still pastes the Kangra paragraph into the middle of the Remember sentence ("works of art that have century, this region had developed a bold and intense style ... miniature occasionally survived, unlike the miniatures"). The letter-spacing is fixed, the splice is not.
- Verdict: extraction fault (one-off)
- Fix: override
  - snapshot: "2023-12-23"
  - chapter: 7
  - find: "works of art that have century, this region had developed a bold and intense style of miniature painting called Basohli."
  - replace: "works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries.\n\nBy the late seventeenth century, this region had developed a bold and intense style of miniature painting called Basohli."
  - note: "text wrapped round Fig. 9 on page 86, the splice of two paragraphs". The exact text after the "miniature" part has to be taken from the file and cleaned the same way.

### our-pasts-2 2023-12-23-rationalised, prelims
- As 2019 (price, "In this book", Reetu Singh, the Keywords box and the emblem line). The bullets "• Content, which ..." lose the bullet, a match for the page.

## 2024-05-24

Pages rendered from the 2024 PDF: ch1 p3 to 6, 8 to 15, ch2 p17, 18, 20, 24, 25, 26, 28, ch3 p30, 31, 33 to 38, ch4 p39, 40, 42 to 45, 47, ch5 p49, 50, 53, 55 to 59, ch6 p63, 66, 68, 71, ch7 p80, 84, 86, 89, 91, ch8 p104, prelims p13. The outlined words are now read with Apple Vision. The effect is large: "SQAUWAaT" is now "sawar", "Ma Claims" is "nagarams", "mUuq list ;" is "muqtis", "VaTTlas" is "varnas", "dy difficult" is "difficult", "A Ss sanskrit" is gone, "hoc h cult" lines are mostly right. The old pattern of words moving to the line above is almost gone.

### our-pasts-2 2024-05-24, chapter 1, printed pages 3, 4, 5, 6, 8, 10, 11, 14
- Hunk: all the "~" with fixed words ("nation-state ." -> "nation-state.", "by Minhaj-i-Siraj, a chronicler ... ", "study for and the nature" -> "study and the nature", "Last year, example" -> "Last year, for example", "cheaper and more Compare the following: -> cheaper and more widely available.", "- widely available.", "not a Sometimes you cannot read your simple exercise" -> "not a simple exercise", "OUR PASS" -> "OUR PASTS", "Jati" -> "jati", "Ahoms Jats" -> "Jats, Ahoms", "+ There was considerable conflict between these states.", "Patron influential ..." -> "Patron An influential ...", "ulama learned" -> "ulama - learned")
- Images: each new reading is what the page shows. The moved words are back in place ("Sometimes you cannot read your friend's handwriting" is on p5 after the break). p8: "As a result, significant economic and social differences emerged amongst peasants." and "Some possessed more productive land, others also kept cattle, ..." are right.
- Verdict: matches the page
- Fix: none

### our-pasts-2 2024-05-24, chapter 1, printed pages 6, 9, 12, 13, 15
- Hunk: "~ Fig. 2 ... The nastaliq style -> The : nastaliq style", "~ (see Chapter 2 for an example of a prashasti) -> (see Chapter 2 for an example of a . prashasti))", "~ ... Masalik -al-Absar -> Masalik : al-Absar", "~ ... Maharashtra and 'apparently fled -> ... and Gujarati apparently fled", "~ ... schools of law (Hanafi Shafi'i: mainly in India), and in theology ... -> ... (Hanafi and in theology and and Shaf'i mainly in India), mystic traditions.", "~ histories you will be studying ... "medieval" -> "medieval" You will find out", "~ 7. How were the affairs of regulated? -> 7. How were the affairs of f jatis regulated?"
- Images: p6 caption "The nastaliq style (on the left) is cursive ..." has no colon. p9: "(see Chapter 2 for an example of a prashasti)" with no stray full stop or second bracket, and the map caption "Masalik al-Absar fi Mamalik al-Amsar", no colon. "Gujarat – apparently fled" on the page (not Gujarati). p12: "(Hanafi and Shafi'i mainly in India), and in theology and mystic traditions." p13: ""medieval". You will find out more" in the page. p15: "7. How were the affairs of jatis regulated?" (no "f").
- Verdict: extraction fault (one-off) (the italics layer adds a stray mark: new faults not present in the committed text for some of them)
- Fix: overrides (snapshot "2024-05-24", chapter 1)
  - find "example of a . prashasti))" replace "example of a prashasti)" note "stray full stop and doubled bracket from italic word on page 9"
  - find "Masalik : al-Absar" replace "Masalik al-Absar" note "stray colon page 9"
  - find "Maharashtra and Gujarati apparently fled" replace "Maharashtra and Gujarat apparently fled" note "page 9 reads Gujarat"
  - find "(Hanafi and in theology and and Shaf'i mainly in India), mystic traditions." replace "(Hanafi and Shafi’i mainly in India), and in theology and mystic traditions." note "words reordered on page 12"
  - find "The : nastaliq style" replace "The nastaliq style" note "stray colon page 6"
  - find "How were the affairs of f jatis regulated?" replace "How were the affairs of jatis regulated?" note "stray f on page 15"
  - find "described as "medieval" You will find out" replace "described as “medieval”. You will find out" note "closing quotation mark and full stop lost page 13"

### our-pasts-2 2024-05-24, chapter 1, printed page 8, 13
- Hunk: "- As a result, significant economic and social differences emerged amongst peasants. others also Some possessed ..." and "- The histories you will be studying this You will find out year are often described as "medieval" ..." and "+ ..." 
- Images: both paragraphs now in order. 
- Verdict: matches the page

### our-pasts-2 2024-05-24, chapter 2, printed pages 17, 18
- Hunk: "- independence from their overlords." "+ Sometimes they asserted their independence from their overlords." "~ ... Prashastis and Land Grants Prashastis -> Prashastis and Land Grants" "- These resources were used to finance the king's establishment, as well as for the construction of temples and forts." and "+ These resources were used to finance the kings" "+ establishment, as well as for the construction of temples and forts."
- Images: p17 sentence is whole and right. p18: the sentence "These resources were used to finance the king's establishment, as well as ..." starts a paragraph below the "Four hundred taxes!" box. The new text makes the first words a heading ("### These resources were used to finance the kings") and loses the apostrophe.
- Verdict: extraction fault (one-off)
- Fix: override (snapshot "2024-05-24", chapter 2): find "### These resources were used to finance the kings\n\nestablishment, as well as for the construction of temples and forts." replace "These resources were used to finance the king’s establishment, as well as for the construction of temples and forts." note "paragraph opening misread as a heading on page 18". The line break between the two pieces must be taken from the file.

### our-pasts-2 2024-05-24, chapter 2, printed pages 20, 25, 26, 28
- Hunk: "~ ... prashastis,, he -> ... of : prashastis, he", "~ ... muvendavelan velan or peasant serving three kings), (a araiyar -> muvendavelan (a velan or peasant serving three kings), araiyar", "~ ... known as UT , became -> ur,", "~ Associations of traders known as Ma Claims also -> nagarams also", "~ Each brahmadeya ; was looked after -> Each brahmadeya was looked after", "~ way in was organised ... The sabha had which the sabha separate committees -> way in which the sabha was organised. The sabha had separate committees", "~ He can officers as finest, the tax let the taxes imposed by judi official of cool on betel-leaves ... -> He can collect the taxes imposed by judicial officers as fines, the tax on betel-leaves ...", "~ 2. Who were the parties involved in the "tripartite What were ... -> What were the qualifications ..." "+ 2. Who were the parties involved in the "tripartite struggle"?"
- Images: the page reads exactly the new text for each ("nagarams", "which the sabha was organised"). The "Unlike the writers of prashastis" has no colon on the page.
- Verdict: matches the page except one stray colon
- Fix: override (snapshot "2024-05-24", chapter 2): find "Unlike the writers of : prashastis, he" replace "Unlike the writers of prashastis, he" note "stray colon page 20"

### our-pasts-2 2024-05-24, chapter 3, printed pages 30, 31
- Hunk: "- Qutbuddin Aybak 1206 -1210 Shamsuddin Iltutmish Raziyya Ghiyasuddin Balban KHALJI DYNASTY Jalaluddin Khalji TUGHLUQ DYNASTY Ghiyasuddin Tughluq Muhammad Tughluq" and "+ KHALJI DYNASTY Jalaluddin Khalji", "+ Khizr Khan 1414 -1421", "+ Qutbuddin Aybak 1206 -1210 Shamsuddin Iltutmish Raziyya Ghiyasuddin Balban", "+ SAYYID DYNASTY", "+ TUGHLUQ DYNASTY Ghiyasuddin Tughluq Muhammad Tughluq Firuz Shah Tughluq"; "~ ... The Delhi Sultans built many cities in the area ... -> cities in the area ..." and "+ The Delhi Sultans built many"
- Images: p31 shows the table with a heading and one line per ruler with dates (for example "Shamsuddin Iltutmish 1210-1236"). Most of the dates are missing in the new text ("Tomaras Early twelfth century 1165 Ananga Pala"): rows are joined, dates and en dashes lost, only "1206 -1210" and "1414 -1421" kept. So the sentence-level list shows the rulers but the table is no longer a faithful copy of the page. The deleted line was equally poor. p30: "The Delhi Sultans built many cities in the area that we now know as Delhi." is a paragraph, now a "###" heading plus a fragment.
- Verdict: extraction fault (rule) (table panel with a gradient: the earlier review pattern, still present), p30 extraction fault (one-off)
- Fix: for p30 override (snapshot "2024-05-24", chapter 3): find "### The Delhi Sultans built many\n\ncities in the area that we now know as Delhi." replace "The Delhi Sultans built many cities in the area that we now know as Delhi." note "paragraph start misread as heading on page 30". Also the p30 line "Delhi first became the capital Take a look at Table 1. of a kingdom under the Tomara Rajputs" has the blue question spliced in: replace "Delhi first became the capital Take a look at Table 1. of a kingdom" with "Take a look at Table 1. Delhi first became the capital of a kingdom" (the page puts the "Take a look at Table 1." first). For p31, the panel needs a row-by-row reading, not an override (a full override of the table is possible, with the dates from the page).

### our-pasts-2 2024-05-24, chapter 3, printed pages 32 to 36
- Hunk: many: "~ Histories are known as tarikh (singular)/ 'tawarikh (plural) -> tawarikh", "- Wished men have said Aperienced slab" and "+ Wise men have said", "~ that a worthy and exp persistence slab slave ts better than a son -> that a worthy and experienced slave is better than a son", "~ ... playing zat was started by the crop he himself -> ... laying zakat ... the Prophet himself", "+ These lands were called iqta and their holder was called iqtadar or muqti.", "~ Thus essential zat -> Thus essentially zakat", "~ ... Firuz Shah Tughluq collected zat -> Tughlag collected zakat", "- Its several parts are so interacted that even fierce cannot y felt them ..." and "+ Its several parts are so intertwined that even fire cannot affect them, and they are on the whole very strong." "+ The chieftains live in these forests which serve them as ramparts, inside which are their cattle and their crops." "+ There is also water for them within, that is, rain water which collects there.", "~ In hindi fia the bamboo is pala places as well not holy low; it is big. -> In India the bamboo is not hollow; it is big.", "- Sher Shah Sur (1540." and "+ Sher Shah Sur (1540- 1545) started his career ..."
- Images: all of these readings are what the pages (34 to 37) show. A few are still not perfect: p35 "annual sayings to the needs and the travellers" (page: "annual savings to the needy and the travellers"), "Tughlag", "samanta: aristocrats" (stray colon), "1. Khums was Consisted of one-fifth of war booty and one-fifth / on mines and treasury trove." (the sentence is cut in two, the page has it in one box with a line break). On p34 the quote is cut by a "## that a worthy and experienced slave is better than a son" heading and p36 "## bamboos with specially prepared instruments." heading (the tail of the quote read as a heading).
- Verdict: matches the page for the listed sentences. Remaining faults: extraction fault (one-off) x5
- Fix: overrides (snapshot "2024-05-24", chapter 3): find "## that a worthy and experienced slave is better than a son" replace "that a worthy and experienced slave is better than a son …" note "quote tail misread as heading on page 34"; find "## bamboos with specially prepared instruments." replace "bamboos with specially prepared instruments." note "quote tail misread as heading on page 36"; find "annual sayings to the needs and the travellers" replace "annual savings to the needy and the travellers" note "page 35"; find "Tughlag collected zakat" replace "Tughlaq collected zakat" note "page 35 box"; find "the samanta: aristocrats" replace "the samanta aristocrats" note "stray colon page 35".

### our-pasts-2 2024-05-24, chapter 3, printed pages 37, 38
- Hunk: "~ (1540 -1555), it introduced an administration ... made Sher Shah's administr... -> ... made them more efficient. Sher Shahs administration became the model ...", "- 2. What was the language of administration under the Delhi Sultans In whose reign did the Sultanate reach its farthest extent?" and "+ 2. What was the language ..." "+ In whose reign ... extent?", "- 10." "- 5. According to the "circle of justice" ..." and "+ 5. According to the "circle of justice", why was it important" "+ for military commanders to keep the interests of the peasantry in mind?", "~ Why were the Delhi Sultans interested in cutting down forests? -> 10. Why were the Delhi Sultans interested in cutting"
- Images: p37 exercise (Let's recall) items 1 to 4: the question marks are dropped and the numbering of 1 and 3 is lost ("> [caption] Which ruler first established ..."). p38: numbering of 8 and 9 is lost, question marks dropped in 6, 7 and 11, and "(5)" is now a unit break. The wording is right. All questions are on the page. "Shahs administration" (apostrophe lost).
- Verdict: extraction fault (rule) (question mark and numbering of the exercises lost: the pattern "numbering of the exercises lost in the second pass" of the earlier review, not gone)
- Fix: pattern, in exercise lists the numbers ("1." "3." "8." "9.") and the "?" are lost in 2024 chapter 3 pages 37 and 38, chapter 4 p47 ("8.", "9."), chapter 5 p59 ("(d)"), chapter 7 p91 and others. Rule: take the exercise numbers and the "?" from the same layer as the rest of the line, or put them back by sequence.

### our-pasts-2 2024-05-24, chapter 4, printed pages 39, 40, 42, 43, 45
- Hunk: "- R extremely difficult task for any ruler to accomplish in" "~ uling as large a territory ... was an the Middle Age -> Ruling as large ... was an extremely difficult task ...", "~ the first Mughal emperor Babur, succeeded ... -> Babur, the first Mughal emperor succeeded to the throne of Ferghana in 1494 when", "~ But unlike mUuq list ;, most mansabdars ... -> But unlike muqtis, most mansabdars ... jagirs.", "~ ... called Jagirs which -> jagirs which", "~ ... zat.. -> zat.", "~ ... SQAUWAaT or cavalrymen -> sawar or cavalrymen", "+ Each province was divided into revenue circles with its own schedule of revenue rates for individual crops." (p43), "~ Jagirs : were carefully assessed -> In Akbar's reign, these jagirs were carefully assessed", "~ These and other factors created a shortage in the number of Jagirs.. -> jagirs."
- Images: p39 drop capital R is rebuilt ("Ruling as large ..."). p42 and p43 read as the new text (sawar, muqtis, jagirs). Double full stops are gone. The "Each province was divided into revenue circles" sentence is the p43 text. p40: the new text has the heading-level line "## Babur, the first Mughal emperor succeeded to the throne of Ferghana in 1494 when" and "(1526 –1530)," lost (the sentence is a paragraph in the page, "Babur, the first Mughal emperor (1526 –1530), succeeded to the throne of Ferghana in 1494 when he was only 12 years old."). p45 "Shah Jahans reign" apostrophe lost.
- Verdict: matches the page for the listed sentences. p40 and p45 extraction fault (one-off)
- Fix: overrides (snapshot "2024-05-24", chapter 4): find "## Babur, the first Mughal emperor succeeded to the throne of Ferghana in 1494 when\n\nhe was only 12 years old." replace "Babur, the first Mughal emperor (1526 –1530), succeeded to the throne of Ferghana in 1494 when he was only 12 years old." note "paragraph opening misread as heading on page 40, dates lost". And find "Shah Jahans reign" replace "Shah Jahan’s reign" note "apostrophe lost on page 45".

### our-pasts-2 2024-05-24, chapter 4, printed page 47
- Hunk: "~ (b) If zat determined a rank and salary, mansabdar's sawar indicated his -> (b) If zat determined a mansabdar's rank and salary, sawar indicated his", "~ 4 What was the relationship between the mansabdar : and the? -> ... the jagir:?", "- KEYWORDS" "- mansab jagir zat sawar sulh-i kul zabt" and "~ Mughal primogeniture coparcenary zamindar Like the Mughal Empire, ... -> Like the Mughal Empire, ..."
- Images: (b) now agrees with the page. The blanks in (b) and (c) ("____") are lost, "4 ... jagir:?" has a stray colon and a lost full stop (page: "4. What was the relationship between the mansabdar and the jagir?"). Let's discuss numbers 8 and 9 are lost. The Keywords column is complete.
- Verdict: matches the page for (b) and Keywords, extraction fault (rule) for the numbering, and one-off for "jagir:?"
- Fix: override (snapshot "2024-05-24", chapter 4): find "What was the relationship between the mansabdar and the jagir:?" replace "What was the relationship between the mansabdar and the jagir?" note "stray colon on page 47".

### our-pasts-2 2024-05-24, chapter 5, printed pages 49, 50, 53, 55
- Hunk: "- Y crafts and production activities flourished in towns" "~ ou saw in Chapters 2, 3 and 4 ... -> You saw in Chapters 2, 3 and 4 ...", "+ Even as this was happening, new arts, crafts and production activities flourished in towns and villages.", "~ ... forests, hills, Sometimes they deserts -> forests, hills, deserts", "~ This of conflict and dependence, relationship, gradually -> This relationship, of conflict and dependence, gradually", "~ ... ts a group of. families ... 'ancestor -> is a group of families ... ancestor", "- From there, they again reload their oxen ... roof profitably sold ld mn other pala In tanda fa there may places be ..." and "+ From there, they again reload their oxen with anything that can be profitably sold in other places." "+ In a tanda there may be as many as 6 or 7 hundred persons They do not travel more than 6 or 7 miles a day – that, too, in the cool weather.", "~ ... roam from one pastures to another with their Jlocks and herders -> roam from one pasture to another with their flocks and herds.", "~ ... travel room place to plates praising théir -> from place to place practising their", "~ Shifting cultivation streets and bushes in forest area are first cult and but. -> Shifting cultivation Trees and bushes in a forest area are first cut and burnt.", "~ The crop is shown in the cases. -> sown in the ashes.", "~ When this land loss its Jertility ... planned -> loses its fertility ... planted", "~ Many ... -> Jatis -> jatis, varna italics ..."
- Images: each new reading is what the page shows. "Beyond Big Cities" etc. unchanged.
- Verdict: matches the page

### our-pasts-2 2024-05-24, chapter 5, printed pages 56, 57, 58, 59
- Hunk: p56 "- Dalpat, however, died early." "~ Rani Durgawati was very capable, and started ruling on behalf of her five Bir Narain. -> capable, and started ruling on behalf of her five-year-old son, Bir Narain." "~ Under year-old son, her, the kingdom -> Under her, the kingdom" "+ Dalpat, however, died early. Rani Durgawati was very"; p57 "- Lachit Barphukan and the defeat of the Mughals in Assam" "- Lachit Barphukan, the Ahom his war skills and'excellent use battle." "~ Source: Janasanyog Assam, Decorated of I information ... Gujarati. -> Directorate of Information Public Relations, Government of Assam, Dispur, Guwahati." "+ Lachit Barphukan and the defeat of the Mughals in Assam Discuss why the Mughals were interested in the land of the Gonds." "+ Lachit Barphukan, the Ahom" "+ Mughal Emperor Aurangzeb in LI 1671 in the Battle of Saraighat, near Guwahati." "+ The Mughal army was consisted of 18,000 cavalry, ..." "+ The battle was mostly a naval war on the river Brahmaputra." "+ Now a memorial L1 stands on the site of this famous battle."; p58 "- Discuss why the Mughals were interested in the land of the Gonds." "~ Historical Chronicles ... -first the Ahom language -> ... written first in the Ahom language", "~ Varna -based society -> Varnas -based society"; p59 "~ (c) The -chaurasi in Gond states -> (c) The chaurasii in Gond states", "- Durgawati" "- Jati tanda garh chaurasi barhot bhuiyans paik khel" "- KEYWORDS" "- garh khel" "~ tanda chaurasi labourer caravan clan ... paik -> ... paik Durgawati" "+ Keywords" "+ barhot ..." "+ khel garh" "+ paik" "+ tanda"
- Images: p56: the heading "### Dalpat, however, died early. Rani Durgawati was very" is a normal paragraph (page: "Dalpat, however, died early. Rani Durgawati was very capable, and started ruling on behalf of her five-year-old son, Bir Narain."), so a heading is wrong but the words are right. The fixed "five-year-old son" is right. p57: the orange note "Lachit Barphukan, the Ahom General defeated the army of the Mughal Emperor Aurangzeb in 1671 in the Battle of Saraighat, near Guwahati. The Mughal army was consisted of 18,000 cavalry ..." — the new text has stray "LI" and "L1" marks (the little picture), "Lachit, with his war skills and excellent use of the terrain relentlessly fought LT JJ" tail noise, and the box title "Lachit Barphukan and the defeat of the Mughals in Assam" glued to "Discuss why the Mughals were interested in the land of the Gonds." which is the blue question on page 58. The Source line is right now (Guwahati). The words "Source: Janasanyog Assam, Directorate of Information Public Relations, Government of Assam, Dispur, Guwahati." are on the page (with "&" before Public). p58: "Varna-based society" on the page, new text "Varnas -based". p59: "The new castes emerging within varnas were called ____" loses "varnas". "(c) The chaurasi in Gond states", new "chaurasii". The match items are listed row by row but "Durgawati" is moved after "paik". The "Imagine" box (nomadic community) of this page is missing in the text of the page (I did not find "Imagine You are a member of a nomadic community" in the 2024 file), a lost paragraph. The keywords "buranji census" are joined and "khel garh" repeated ("khel garh" from the match list has leaked into the Keywords list).
- Verdict: p56, p57, p58, p59 extraction fault (one-off) for each listed item. "Imagine" on p59 not in the text: extraction fault (one-off), lost sentence that is on the page (the most serious kind, see Summary).
- Fix: overrides (snapshot "2024-05-24", chapter 5): find "Varnas -based society" replace "Varna-based society" note "page 58"; find "(c) The chaurasii in Gond states" replace "(c) The chaurasi in Gond states" note "page 59"; find "(a) The new castes emerging within were called" replace "(a) The new castes emerging within varnas were called" note "italic word lost on page 59"; find "### Dalpat, however, died early. Rani Durgawati was very\n\ncapable," replace "Dalpat, however, died early. Rani Durgawati was very capable," note "page 56 paragraph misread as heading"; find "Mughal Emperor Aurangzeb in LI 1671" replace "Mughal Emperor Aurangzeb in 1671" note "stray picture mark page 57"; find "Now a memorial L1 stands" replace "Now a memorial stands" note "stray picture mark page 57". The Imagine on page 59 needs an inserted paragraph: find "<!-- section: exercises -->\n\n### Let’s recall\n\n1. Match the following:" on page 59 and insert before it "Imagine\n\nYou are a member of a nomadic community that shifts residence every three months. How would this change your life?" The text of the Imagine is taken from the page image (and the 2014/2016/2019 pages of ch7 p101).

### our-pasts-2 2024-05-24, chapter 6, printed pages 63, 66, 67, 68, 69
- Hunk: p63 "- This is a composition of Manikkavasagar: flesh body Into my vile ... " and "+ This is a composition of Manikkavasagar: Into my vile body of flesh You came, as though it were a temple of gold, ..." "+ How does the poet describe his relationship with the deity?" "+ O Bliss O Light I have taken refuge in You, And never can I be parted from You."; "~ Hagiography Writing of saints lives. -> saints' lives.", p66 "~ ... He who wide titles fentif with the battered ... -> He who identifies ...", p67 "~ Fig. 3 A reside glaring of ascetics. -> A fireside gathering of ascetics.", "~ The Sufis often rej recited the elaborate rituals -> rejected", "~ 'Sufis were Muslim mystics. -> Sufis were Muslim mystics.", "+ Among the great Sufis of Central Asia were Ghazzali, Rumi and Sadi." p68: "- In Kashmir, the Rishi order of Su sufism flourished in the 15th and 16th centuries." and "+ In Kashmir, the Rishi order of Sufism flourished" "+ in the 15th and 16th centuries.", "- .", "- were Ghazzali, Rumi and Sadi."; p69 "~ Fig. 5 ... late eighteenth-century. -> late fifteenth century.", "~ Iqtadar long line of teachers like Khwaja Muinuddin Chishti -> It had a long line of teachers ...", "~ The Chishti was among the silsila most influential orders. -> The Chishti silsila was among the most influential orders."
- Images: all of these agree with the pages. On p68 the sentence "In Kashmir, the Rishi order ..." is a margin note and the two units of it are fine. The "( (tariqa)) of instruction and ritual practice." line is a stranded bit: the page has "(tariqa) of instruction and ritual practice." as the end of the text column above the picture, now preceded by stray bracket characters.
- Verdict: matches the page; one one-off fault: "( (tariqa)) of instruction and ritual practice."
- Fix: override (snapshot "2024-05-24", chapter 6): find "( (tariqa)) of instruction and ritual practice." replace "(tariqa) of instruction and ritual practice." note "stray brackets from italic word on page 68". The sentence is also on its own, apart from "Thus emerged the silsilas, a spiritual genealogy of Sufi teachers, each following a slightly different method" (the first half), check on the file whether the two are joined.

### our-pasts-2 2024-05-24, chapter 6, printed pages 61, 62, 64, 65, 70, 71, 72, 73, 74, 75, 76, 77
- Hunk: many reading fixes ("~ ... Mahar htra, such dnyaneshwar, Namdev -> Maharashtra, such as Jnaneshwar, Namadeva", "~ ... akbari set -> Varkari sect", "~ sakhis", "~ Avicenna the philosopher", "~ nam, dan, and isnan", "~ nam-japna, kirt-karna, and vand-chhakna", "- The teachings Q of Shankaradeva ... L. He also encouraged ..." and "+ The teachings of Shankaradeva were based on the" "+ Bhagavad Gita" "+ and Bhagavata Purana 1. He also encouraged the establishment" "+ fo satra monasteries for transmission of knowledge." "+ His major compositions included" "+ Kirtana-ghosha", "- important contributing Bhakti saints was towards ..." and "+ An important contribution of Bhakti saints was towards the development of music." "+ Jayadeva of Bengal composed the Gita Govinda in Sanskrit, each song composed in a particular raga and tala O significant impact that these saints had on music w..." (p72), "~ Muslim or weavers -> Muslim 1 julahas or weavers", "~ Shankara, one of the most influential philosophers -> Philosophy and Bhakti Shankara, one of ...")
- Images: viewed p71 only. p71's orange note about Shankaradeva is the text in the right margin ("The essence of Shankaradeva's devotion came to be known as Eka Sarana Nama Dharma (supreme surrender to the One). The teachings of Shankaradeva were based on the Bhagavad Gita and Bhagavata Purana. He also encouraged the establishment of satra monasteries for transmission of knowledge. His major compositions included Kirtana-ghosha."). The new text reads it in order but with stray "1." after Purana and "fo satra". The "The essence of Shankaradevas" lost its apostrophe. p72's note about music ("An important contribution of Bhakti saints was towards the development of music. Jayadeva of Bengal composed ...") was not viewed. p61, 62 (OCR'd letter-spacing "w or shi pped" "Shi va", "Vish n u" is still spaced), 64, 65, 67, 69, 70, 72 to 77 not viewed.
- Verdict: p71 matches the page except two one-off faults; the rest not viewed
- Fix: overrides (snapshot "2024-05-24", chapter 6): find "Bhagavata Purana 1. He also encouraged" replace "Bhagavata Purana. He also encouraged" note "stray picture mark on page 71"; find "fo satra monasteries" replace "of satra monasteries" note "OCR page 71". p62 letter-spacing: find "w or shi pped in different areas" replace "worshipped in different areas" and "Shi va, Vish n u or Dur ga" (the exact text in the Markdown must be copied) as the 2023 text got it right.

### our-pasts-2 2024-05-24, chapter 7, printed pages 80, 83, 84, 86, 87, 88, 89, 91
- Hunk: "~ T he first literary works -> The first literary works", "~ Subsequently, it developed in two: one in the courts of Rajasthan traditions or ; gharanas: (Jaipur) -> in two traditions or gharanas: one in the courts of Rajasthan (Jaipur)", "~ r "ASIA lila -> r casa lila", "~ CLASSICAL H pictorially, -> CLASSICAL Historically,", "~ History for Schools (Trilingual), 2017, INERT -> Sources Dictionary of History for Schools (Trilingual), 2017, NCERT" "- Source", "~ ... Athens to a pure cement position -> pre-eminent position", "- R e m e m b e r t h a t ordinary women ... cloth." "- works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries." and "+ Remember that ordinary women and men painted as well — on pots, walls, floors, cloth - works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries.", "~ Animism Attributed of living soul to plates, inanimate subjects -> Attribution of living soul to plants, inanimate objects", "~ ... as us . -> as pirs.", "~ Pir A Persian word meaning spiritual guide -> a spiritual guide", "~ Why do you think the second category of texts was not written down? -> Many of the modest brick Why do you think the second category ...", "~ ... modest brick and terracotta temples ... -> and terracotta temples ...", "~ Understandably, 'these two items -> these two items"
- Images: p80 the drop capital T is rebuilt, p84 the Classical note matches. p86: the two parts of "Remember that ordinary women and men painted as well – on pots, walls, floors, cloth – works of art that have occasionally survived, unlike the miniatures that were carefully preserved in palaces for centuries." are now one sentence (the page runs it across p86 and p87, with the two lines that sit above the picture in the page being one paragraph). Compared with 2023, the splice is cleared. Letter-spacing gone. p89: "Many of the modest brick" is the last text of the page, text of the paragraph "Bengal also witnessed a temple-building spree ... Many of the modest brick and terracotta temples" and "Why do you think the second category of texts was not written down?" is the blue margin question. The new text glues the sentence start "Many of the modest brick" to the question. The sentence "Many of the modest brick" in the main paragraph is also there (cut at the page edge, continues on p90). Dash-like "cloth - works" (a hyphen instead of an en dash) is a typographic mismatch, minor.
- Verdict: matches the page for the listed readings, one extraction fault (one-off) for the glued question on p89
- Fix: override (snapshot "2024-05-24", chapter 7): find "Many of the modest brick Why do you think the second category of texts was not written down?" replace "Why do you think the second category of texts was not written down?" note "the first words belong to the paragraph on page 89 (they continue on page 90)". The Markdown may need the orphan words to stay with the paragraph.

### our-pasts-2 2024-05-24, chapter 8, printed page 104
- Hunk: "~ 3. Why did the Marathas want to expand beyond the -> ... Deccan?" "- Deccan?" "- Keywords subadari dal khalsa misl faujdari ijaradari chauth sardeshmukhi" "+ Keywords ..." 
- Images: p104 shows Let's recall item 1 true/false (a to d) and Let's discuss items 2 to 5, Let's do item 6, and the Keywords column of six words ("chauth sardeshmukhi" is one line). The new text has all of them. Note the page numbers items 1 to 6 (the page has no "Match the following").
- Verdict: matches the page

### our-pasts-2 2024-05-24, prelims
- As 2023: Member-Coordinator and Reetu Singh match the credits. The price "₹ 65.00" matches. The Keywords box (p13) has the same interleaving fault as in 2016 (see the prelims override above). "Imagine" box on p13: text is present. The emblem line "VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND" persists (override above).

## 2018-partial

### our-pasts-2 2018-partial, chapters 1, 3, 4, 9, prelims (block "new file" in the change list)
- Hunk: all "+" lines.
- Images: not viewed. There are no texts of 2018-partial in the working tree or in HEAD to compare with the pages.
- Verdict: not viewed
- Fix: regenerate the change list. If the snapshot is meant to have texts, they must be produced first.

## Summary

Counts by entry (an entry that groups the same finding over several pages counts once, one entry per edition and finding):
- matches the page: 76
- extraction fault (rule): 27
- extraction fault (one-off): 41
- not viewed: 14 (2018-partial block, 2022 OCR ch7 p99, p100, p101 text, ch8 p105, p113, ch9 p131, ch4 p58, ch6 p87, 2024 ch6 p61, 62 text, 64, 65, 67, 70, 72 to 77, ch7 p83 to 85, 87, 88, 91 text, ch2 p25 text for the "UT" reading, ch3 p32 text, ch5 p50 and the 2024 ch1 p15)

Lost sentences (the most serious finding): one found. Edition 2024-05-24, chapter 5, printed page 59: the Imagine box "You are a member of a nomadic community that shifts residence every three months. How would this change your life?" is on the page but not in the text at all. No other "-" line was a loss: every deleted sentence was found again, joined to another sentence, split, moved to a note, or (2014 to 2019 keyword words) listed as a "### Keywords" list. Words that are on the page and missing from the new text in smaller ways: blanks in exercise lines (2022, 2024 ch4 p47 (b) and (c), ch5 p59 (a)), exercise numbers and question marks (2024 ch3 p37, p38, ch4 p47, "(1526 -1530)," in 2024 ch4 p40), and most of the dates of the Table 1 panel in 2024 ch3 p31.

Patterns of the earlier review that are now gone (or mostly gone):
- The margin KEYWORDS words glued into an exercise line (2014, 2016, 2019, 2023, 2024, and mostly 2022): gone except for the OCR edition p14 ch1, ch4 p58, ch9 p136.
- "Widely available." inserted after a box title glued to a sentence (2016 ch1 p4, 2024 ch1 p4): gone. Box titles glued to the next sentence in 2014/2016 chapters 4 and 6 (Nur Jahan, the bronze note): gone.
- Words moved to the line above in 2024 (the "study for and the nature" family) and the garbled italic words ("SQAUWAaT", "Ma Claims", "mUuq list ;", "VaTTlas", "hoc h cult"): almost all gone, thanks to Apple Vision. Remaining: stray colons and brackets next to italic words ("of : prashastis", "( (tariqa))", "example of a . prashasti))"), a few reordered phrases (ch1 p12 "Hanafi and in theology").
- Letter-spaced justified lines "c a m e t o b e" and "R e m e m b e r t h a t": gone in 2023. Still present in 2024 ch6 p62 ("w or shi pped", "Shi va").
- The drop capital cut from its word (2024 ch4, ch5, ch7): gone. Still present in 2022 ch1 p1 ("ake a look").
- Match-the-following tables spilling into the glossary (ch4 p57 and p58, ch7 p101): gone in 2014, 2016, 2019.
- The Table 1 panel, text box inside a wrapped paragraph for ch10 p147 in 2019 and 2022: gone ("Maratha campaigns into Rajasthan" rejoined). The 2023 splice of the Kangra paragraph and the Remember sentence in 2023 ch7 p86 is gone in 2024, not in 2023.
- The "duplicate garbled copies of the quotations in boxes" in 2024: gone on the pages viewed.
- Numbered exercises dropped in 2023 ch1 p14 (the "700." and "this period.") are fixed in 2023, not in 2024 (see below).

The three remaining patterns that matter most:
1. Text placed around pictures and boxes is cut and interleaved in the OCR edition 2022-08-04, and is spliced into the wrong paragraph (box title, margin note or caption words inside a sentence). Seen at ch2 p24, ch3 p32, p34, p35, p37, ch4 p48, p49, p50, p52, ch5 p63, p64, ch6 p82, p83, ch7 p95, p98, ch8 p119, ch9 p130, p135, p136. In 2016 and 2019 the same family is the box title "Importance of water" inside the sentence (ch5 p65) and the Fig. 4 caption cut by a question (ch5 p62). Rule: flow body text by column, give a caption, a note and a box title their own unit, and never let a unit continue after another block starts. Noise words from maps and pictures should never become headings or captions (ch3 p34, p35, ch4 p49, ch5 p62, ch8 p115, ch9 p125).
2. Exercises and structured lists lose structure in 2024 and the OCR edition: numbers and question marks dropped (2024 ch3 p37, p38, ch4 p47), blanks dropped (2022 everywhere, 2024 ch4 p47, ch5 p59), match rows joined or moved (2024 ch5 p59, 2022 ch4 p57, ch9 p136), Imagine paragraphs split at line ends or lost (2014 to 2019 and 2022 pages named above, and the lost Imagine on 2024 ch5 p59), and a Keywords box carrying free text (ch5 p73). Rule: read the exercise numbers and "?" from the same layer, keep blank runs as a "____" token, join consecutive lines of one coloured block, treat a Keywords box with sentences as a note.
3. Paragraph openings misread as headings or table panels in 2024 and the gradient Table 1 panels (2024 ch3 p31 dates lost, 2022 ch4 p48 and p49): lines like "### These resources were used to finance the kings", "### Dalpat, however, died early. Rani Durgawati was very", "## Babur, the first Mughal emperor ...", "### The Delhi Sultans built many", "## that a worthy and experienced slave is better than a son" are body text. Rule: a line is a heading only if it is short (fewer than about 12 words), has no sentence-final continuation across the break and its font matches the heading font. Table panels with a gradient need a row-by-row (by vertical position) reading with dates kept.

Smaller recurring faults for the fix pass: the OCR confusions k to R and l to 1 ("Rnowledge", "Rept", "1s", "Pulatyas") persist in the 2022 text, the emblem line "VATIONAL COUNCI OF EDUCATIONAL RESEARCH AND" in the prelims of four editions, the prelims "Keywords" box in every edition, and the 2014 chapter 5 clipped margin.
