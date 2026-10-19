# Recheck of social-political-life-3 after the rule change

Book: Social and Political Life III (Class 8 civics). Input: `review/changes-social-political-life-3.txt` (477 changed sentences). Every listed page was opened as a rendering of the edition's own PDF, and the new text was compared with it. The earlier review is `review/social-political-life-3.md` (Rules A to H).

How to read the entries. Each entry starts with a tag: [M] the new text matches the page, [R] extraction fault that a rule can fix, [O] one-off fault with a ready-to-paste override, [N] not viewed. The 2019, 2020, 2021 and 2022 printings share one layout and, for chapters 6 and 8 and 10, byte-identical text, so a fault seen in one is listed for all four. Editions are named by their folder (`2023-12-23-rationalised` is "2023", `2024-05-24` is "2024").

Page images were opened as follows. 2014: ch1 p10 p14, ch3 p33 p37 p38, ch4 p43, ch5 p55 p56 p58 p61, ch6 p70 p71 p72 p76, ch7 p89, ch9 p112, ch10 p124 p125. 2016: ch3 p33 p38, ch5 p56 p60 p63, ch6 p68 p70 to p76, ch7 p82 to p89, ch8 p101, ch10 p124 p125, prelims pdf pages 1 to 3. 2019: ch1 p14, ch5 p56 p61, ch6 p70 to p72, ch7 p89, ch8 p96 p101. 2021: ch1 p14 p17, ch9 p111 p112 p116, ch10 p123 p124 p134. 2022: ch2 p21, ch6 p71 p72, ch9 p114 p115. 2023: ch1 p14 p17, ch3 p33 p35, ch4 p52, ch5 p71, ch7 p91 p92, prelims pdf pages 5 and 14. 2024: ch4 p52, ch8 p103 p104, ch7 p91.

---

## Patterns (rules)

- Rule I, wrapped line of a boxed bullet or run-in bold heading becomes its own block. A bullet or heading that wraps onto a second line is cut after its first line and the second line is written as a separate `[table]` block (bullet case) or the first line becomes a `###` heading with the rest as a paragraph (heading case). The page shows one bullet or one run-in heading followed by its paragraph. Seen: ch1 p14 "- If a group of people are not given permission to open a" / "Telugu-medium school in Kerala." in 2014, 2019, 2020, 2021, 2022, 2023, 2024 (the 2016 file did not change and was not listed). Ch5 p55 "### Upholding the Law and Enforcing Fundamental" then "Rights: Every citizen ..." in 2014 only. Rule: a bold or box line that ends without terminal punctuation and is followed directly by a line starting in lower case or a capital with the same left edge and font belongs to the same block.
- Rule J, side question or wrapped table cell glued to the next item. The grey side question of a page is written inside the last row of the neighbouring table, and the wrapped second line of a table cell ("Subordinate Courts") is glued to the paragraph below. Seen: ch5 p56 "Laws that are in violation of the Constitution Do you think that any ordinary citizen stands a chance against a politician in this kind of judicial system? Why not?" in 2014, 2016, 2019, 2020, 2021, 2022 (ch4 p50 in 2023 and 2024). Ch5 p63 "C District and 19,421 15,039? Subordinate Courts However, inspite of this ..." in 2016, 2019, 2020, 2021, 2022 (new in 2016, unchanged in the later files). The page shows the side question alone in the margin and "However, inspite ..." as the paragraph under the table.
- Rule K, heading drawn twice with a clipped prefix. "Bhopal Gas T Bhopal Gas Tragedy" is the heading on the first Bhopal page in every edition (ch10 p124 in 2014, 2016, 2019 to 2022, ch8 p104 in 2023 and 2024). The page shows only "Bhopal Gas Tragedy". The trailing "ragedy" duplicate is gone now, the leading "Bhopal Gas T " is not.
- Rule E (still open), pie chart labels. Written one fragment per label. In 2021, 2022 and 2023 the label "9 p." of "Centrally Sponsored Scheme" is missing (the text has two "9 p." and the page has three, the 2019 and 2020 files still have all three). In 2024 the new chart (percentages) comes out scrambled: "Finance Commission / Central Sector Scheme and other Transfers", "(6%) States' share of / Subsidies taxes & duties", and only eight of the nine values are present (one "(8%)" for Defence is lost). Rule: join the labels of one figure into one block in reading order of the label positions, and check that the values add up to 100.
- Rule L, table cells from different tables or columns mixed. 2016 ch5 p60: the two columns of the criminal/civil law table are interleaved line by line ("1. Deals with conduct or acts that the Deals with any harm or injury to rights law defines as offences. For example, of individuals. For example, disputes theft, ..."). 2016 ch7 p88: the cells of the two p89 tables (literacy row and the employment header row) are written into the p88 "I. Basic Amenities, 1994" block. Rule: cells go into the block of the table whose bounding box contains them, and a cell is read column by column.
- Rule M, logo and watermark lettering read as text, preamble page garbled. Every prelims file with a logo has fragments of the NCERT logo or the diagonal watermark ("RUE.", "OF EDUCATIONAL RESEARCH AND TRAI", "VATIONAL COUNCI", in 2016, 2019 to 2023, and "uRt.", "le.f." in 2024). In 2023 and 2024 the Preamble page (pdf page 14) is an ornamental image page read with dropped letters ("VEREIGN CIALIST SECULAR DEM CRATIC", "ec mic", "pportunity", footnote "Forty-seco ocratic Republic"). Rule: drop caption blocks of three or fewer words that sit on the logo, and mark the Preamble as unreadable or OCR it with the vocabulary snap.

---

## 2014-07-28

- [M] ch1 p10 "Now let us try and understand ..." is on the page without the "Q" glyph. The new text matches.
- [R] ch1 p14. Page shows the bullet "If a group of people are not given permission to open a / Telugu-medium school in Kerala." as one bullet over two lines. New text has "- If a group ... to open a" and a separate block "Telugu-medium school in Kerala.". Old side matched the page. Verdict: extraction fault (rule I). Fix: rule I. Override:
  ```
  - snapshot: "2014-07-28"
    chapter: 1
    find: "> [table] - If a group of people are not given permission to open a\n\n> [table] Telugu-medium school in Kerala."
    replace: "> [table] - If a group of people are not given permission to open a Telugu-medium school in Kerala."
    note: "the bullet wraps onto a second line on page 14 and is one bullet"
  ```
  The same override (with the snapshot label changed) fits 2019-05-04, 2020-06-16, 2021-08-14, 2022-08-02 (chapter 1), and 2023-12-23 and 2024-05-24 (chapter 1, the `[table]` prefix is as in the file).
- [M] ch3 p33. "4. Fill in the blanks ..." is printed "4." on the page, the stray "Q4." is gone. Matches.
- [M] ch3 p37. The old sentence "B. To Control, Guide and Inform the Government The Parliament, while in session, ..." is now a heading and a paragraph. The page shows the bold heading on its own line. Nothing lost.
- [M] ch3 p38. "list two questions that you would like to ask." Page matches, the doubled "arliament (MP)" is gone.
- [M] ch4 p43. "The above is a clear case of the violation of law." Page has a Q watermark in the box, the sentence has no Q.
- [O] ch5 p55. Page shows one run-in heading "Upholding the Law and Enforcing Fundamental Rights:" followed by the paragraph. New text writes "### Upholding the Law and Enforcing Fundamental" then "Rights: Every citizen ...", old text had it whole. Verdict: extraction fault (one-off in this file, rule I). Override:
  ```
  - snapshot: "2014-07-28"
    chapter: 5
    find: "### Upholding the Law and Enforcing Fundamental\n\nRights: Every citizen"
    replace: "Upholding the Law and Enforcing Fundamental Rights: Every citizen"
    note: "bold run-in heading wraps onto the second line on page 55, the other editions read it as one paragraph"
  ```
- [M] ch5 p56 "Imagine a situation ..." (Q removed), p58 "Are these different levels of courts connected to each other?", p61 "In principle, all citizens of India ...". All on the pages without a Q. (The Rule J glue on p56 is listed under Patterns.)
- [M] ch6 p70 "From the above incident ..." without "Po". Page matches.
- [M] ch6 p71. The four old lumped sentences are now seven bullets, a lead sentence and four box bullets. All words are on the page in the page's order, and the memo-of-arrest bullet is one bullet with its two sentences, as printed. Nothing lost. The side question sits between bullets 1 and 2 as a caption.
- [M] ch6 p72. "2. Now let us take a slightly different scenario." The page prints "2." and the "Q2." is gone.
- [M] ch6 p76 "In a town called Peace Land ..." without "Q". Matches.
- [M] ch7 p89. The old split "25 per cent ... dropped out." plus "This percentage ... (page 58)." is now one bullet. The page prints one bullet in the margin box. Matches.
- [M] ch9 p112 "2. The government can get private companies ..." The page prints "2." (not "Q2."). Matches.
- [M] ch10 p124 and p125. "A child severely affected by the gas" (p124) and "The struggle for justice goes on…" (p125) are back and match the photo captions. The Bhopal captions fault of Rule B is fixed.
- [R] ch10 p124 heading "Bhopal Gas T Bhopal Gas Tragedy". Rule K. Override:
  ```
  - snapshot: "2014-07-28"
    chapter: 10
    find: "## Bhopal Gas T Bhopal Gas Tragedy"
    replace: "## Bhopal Gas Tragedy"
    note: "the page 124 heading is drawn twice and the first copy is clipped, the page shows Bhopal Gas Tragedy"
  ```
  The same override fits 2016-09-10 (chapter 10), 2019-05-04, 2020-06-16, 2021-08-14, 2022-08-02 (chapter 10), 2023-12-23 and 2024-05-24 (chapter 8).

## 2016-09-10

- [M] ch3 p33 ("4." printed, "Q4." gone), p38 (doubled "arliament (MP)" gone). Pages match.
- [M] ch4 p43, ch5 p58 ("Are these different levels ..."), ch9 p112 ("2."). Same as 2014. Matches. Ch5 p56 "Dispute between centre and the state" without "Q" matches the table row.
- [R] ch5 p56. Old text had the side question as its own sentence and "Laws that are in violation of the Constitution" as a table row. New text joins them: "Laws that are in violation of the Constitution Do you think that any ordinary citizen ...". Page shows the question alone in the margin. Verdict: extraction fault (rule J). Override:
  ```
  - snapshot: "2016-09-10"
    chapter: 5
    find: "> [caption] Laws that are in violation of the Constitution Do you think that any ordinary citizen stands a chance against a politician in this kind of judicial system? Why not?"
    replace: "> [caption] Laws that are in violation of the Constitution\n\n> [caption] Do you think that any ordinary citizen stands a chance against a politician in this kind of judicial system? Why not?"
    note: "the grey side question of page 56 stands alone in the margin, it is not part of the table"
  ```
  The same find and replace fit 2014-07-28, 2019-05-04, 2020-06-16, 2021-08-14, 2022-08-02 (chapter 5) and 2023-12-23, 2024-05-24 (chapter 4, p50).
- [R] ch5 p60. Page shows the criminal law table as two columns with three numbered rows and a fill-in table below. New text keeps all words (the "A group of girls ..." row is its own caption and the "Q" is gone, both correct) but writes the table cells by line across columns ("1. Deals with conduct or acts that the Deals with any harm or injury to rights law defines as offences. ..."). Verdict: extraction fault (rule L). Fix: rule L (old text had the same interleaving in the deleted lines).
- [R] ch5 p63. The new text glues "Subordinate Courts" to the next paragraph ("... Subordinate Courts However, inspite of this ..."). The page shows the table cell "District and Subordinate Courts" and the paragraph "However, inspite ..." below the footnote. Old side had the paragraph apart. Verdict: extraction fault (rule J). Override:
  ```
  - snapshot: "2016-09-10"
    chapter: 5
    find: "15,039? Subordinate Courts However, inspite of this"
    replace: "15,039? Subordinate Courts\n\nHowever, inspite of this"
    note: "the wrapped second line of the table cell is glued to the paragraph under the table on page 63"
  ```
  The same fits 2019-05-04, 2020-06-16, 2021-08-14, 2022-08-02 (chapter 5, p63, text unchanged there).
- [M] ch6 p66. The "-" line "I plead not guilty. And I claim trial." is not lost. The speech bubble is on the page (bottom, courtroom drawing) and the sentence is still in the 2016 text as a caption on p66 (it also appears once more under p69, an older duplicate). The change list shows it as removed only because one copy was dropped.
- [M] ch6 p68 "Mr Shinde returns with Sub Inspector Rao." Page prints exactly this, "Po" gone.
- [M] ch6 p70 and p71. The paragraph "As stated at the beginning of this chapter, it is not the job of the police to decide whether a person is guilty or innocent, that is for the judge to decide." is now whole (it runs across p70 to p71 on the page) and the sub-heading and the side question are no longer inside it. Rule C is gone here.
- [M] ch6 p71 the seven bullets, same as 2014. Matches.
- [M] ch6 p72. "a) When Shanti was arrested ... Does it violate the D.K. Basu guidelines?" and "b) Did S.I. Rao do enough ... investigation?" are each one block now and the "Qb)" is gone. The page shows the box with items 1 a, 1 b and 2. Matches.
- [M] ch6 p73. "What if the court did not give a copy of the chargesheet and statements of witnesses to Shanti?" is whole, and "What did the judge say in Shanti’s case after hearing the testimony of all the witnesses?" is its own caption (the page shows it in the margin). Fixed. The ready-to-paste override of the first review is no longer needed.
- [M] ch6 p74. "Advocate Roy was given an opportunity to cross-examine all the prosecution witnesses. Advocate Roy was given an opportunity to present witnesses in Shanti’s defence." The doubled "rosecution rosecution" and "itnesses" are gone. Rule H is fixed. The tail "statements of witnesses to Shanti?" is joined to its sentence.
- [M] ch6 p75. "All of the processes, written in bold on page 74, ..." is now the first line of the box (the page shows it there). "a. Open Court: b. Basis of Evidence: c. Cross-examination of Prosecution Witnesses:" and "a. If she were not defended by a lawyer. b. If the court had not assumed her to be innocent." match, the stray "Qa." is gone.
- [M] ch6 p76. "1. Police 2. Public Prosecutor 3. Defence lawyer 4. Judge", "The column on the right provides a list of functions." and "Now take the same situation ..." are separate sentences as on the page.
- [M] ch7 p82. All the old speech bubbles ("After a few years ...", "The money hardly lasted ...", "I never saw most of my friends again.") are on the page and in the new text, the bubble sentences are only counted one by one now. Nothing lost.
- [M] ch7 p83 and p84. "Simultaneously, Adivasi religions themselves have influenced dominant religions of the empires around them, for example, the Jagannath cult of Orissa and Shakti and Tantric traditions in Bengal and Assam." is whole across the page break, and "Explain at least three different reasons why groups may be marginalised." is its own caption. Rule C is gone.
- [O] ch7 p85 and p86. The page 86 paragraph "Forest lands have been cleared for timber and to get land for agriculture and industry. Adivasis have also lived in areas ... termed encroachers." is written into the p85 pink box paragraph after the first poem line: "... the reality they faced in Assam. Come Mini, let’s go to Assam Forest lands have been cleared ...". The page shows the song lines in the box on p85 and the "Forest lands ..." paragraph at the top of the right column on p86. Old side had the poem line in a caption with the other lines. Verdict: extraction fault (one-off). Override (the paragraph stays under the p85 marker, which is still wrong by one page, but the poem line is back in its place):
  ```
  - snapshot: "2016-09-10"
    chapter: 7
    find: "reality they faced in Assam. Come Mini, let’s go to Assam Forest lands have been cleared"
    replace: "reality they faced in Assam.\n\n> [caption] Come Mini, let’s go to Assam\n\nForest lands have been cleared"
    note: "the first poem line of the box on page 85 was written in front of the page 86 paragraph, page 86 starts with Forest lands have been cleared"
  ```
- [M] ch7 p86 and p87. "Adivasis use around 10,000 plant species ..." is its own caption and "They, thus, get caught in a cycle of poverty and deprivation." is whole. "Given certain conditions, communities that are small in number relative to the rest of society may feel insecure about their lives, assets and well-being." is whole over p87 to p88 and the side question "In your opinion, why is it important ..." is separate. Rule C is gone.
- [M] ch7 p85 caption "Source: Basu, S. Jharkhand Movement: Ethnicity and Culture of Silence What metals are important in present-day India? Why? ..." The page shows the source line and the side question apart. Words are right but two items are glued (minor, same family as rule J). Not a loss.
- [R] ch7 p88. The new "I. Basic Amenities, 1994" block holds "Kutcha houses ... Piped water ..." and also "All Hindus Muslims Christians Sikhs Buddhists Jains 65% 65% 59% 80% 70% 73% 94% Population IAS IPS IFS Central Public State PSU Banks & RBI Sector Unit (PSU)". The page puts the first line (literacy cells) in table II on p89 and the second (employment header) in table III on p89. Verdict: extraction fault (rule L). Overrides:
  ```
  - snapshot: "2016-09-10"
    chapter: 7
    find: "25.3% of Hindus have access to piped water All Hindus Muslims Christians Sikhs Buddhists Jains 65% 65% 59% 80% 70% 73% 94% Population IAS IPS IFS Central Public State PSU Banks & RBI Sector Unit (PSU)"
    replace: "25.3% of Hindus have access to piped water"
    note: "cells of the two tables of page 89 were written into the page 88 table"
  - snapshot: "2016-09-10"
    chapter: 7
    find: "> [table] II. Literacy Rate by Religion, 2001"
    replace: "> [table] II. Literacy Rate by Religion, 2001\n\nAll Hindus Muslims Christians Sikhs Buddhists Jains 65% 65% 59% 80% 70% 73% 94%"
    note: "literacy cells belong to table II on page 89"
  - snapshot: "2016-09-10"
    chapter: 7
    find: "> [table] III. Public Employment of Muslims (percentages)"
    replace: "> [table] III. Public Employment of Muslims (percentages)\n\nPopulation IAS IPS IFS Central Public Sector Unit (PSU) State PSU Banks & RBI"
    note: "header cells belong to table III on page 89"
  ```
- [M] ch7 p88 "I. Basic Amenities, 1994", p89 "II. Literacy Rate by Religion, 2001", "III. Public Employment of Muslims (percentages)". The page prints the roman numerals. The three separate lines and "25 per cent of Muslim children ..." (one bullet) match.
- [M] ch8 p101. "Why did the Safai Karamchari Andolan file a PIL in 2003? What did they complain about in their petition?" is one margin block on the page. Matches.
- [M] ch10 p124 and p125. Bhopal captions back and right. Heading fault is rule K (see 2014 entry).
- [M] prelims. "` 50.00" is "₹ 50.00" on the page.
- [R] prelims pdf page 2. All words of the credits are on the page, but "Cover and Layout Storyboards CMAC Dipankar Bhattacharya" now carries the whole "Reprinted January 2009 ... December 2014 Pausha 1936" list, the copyright line and the "Printed on 80 GSM ... Published at ..." lines, which sit in other places on the page (Reprinted list top left, copyright below it, printing note at the bottom left). Verdict: extraction fault (order and grouping, one-off). Override:
  ```
  - snapshot: "2016-09-10"
    chapter: "prelims"
    find: "> [caption] Cover and Layout Storyboards CMAC Dipankar Bhattacharya Reprinted January 2009"
    replace: "> [caption] Cover and Layout Storyboards CMAC Dipankar Bhattacharya\n\n> [caption] Reprinted January 2009"
    note: "the credits box and the reprint list are separate blocks on pdf page 2"
  ```
- [R] prelims pdf page 1. "RUE. OF EDUCATIONAL RESEARCH AND TRAI" and "VATIONAL COUNCI" are the logo lettering and watermark. The page prints "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING" in the logo. Verdict: extraction fault (rule M).

## 2019-05-04

- [M] ch1 p14 (rule I, see 2014), ch3 p33 and p38, ch4 p43, ch5 p56 p58 p61 (Q removed), ch6 p70 p71 p72 p76, ch7 p89. Same as 2014, matches. The 2019 page of ch6 p71 shows the seven bullets as in the text.
- [R] ch1 p14. Rule I. The page shows "If a group of people are not given permission to open a / Telugu-medium school in Kerala." as one bullet. "armed forces for being a woman." was already whole here.
- [M] ch8 p96. "Promoting Social Justice" is a bold sub-heading on its own line and "As part of their effort ..." a paragraph. The page shows exactly this. Matches.
- [M] ch8 p101. "₹ 200 per day" The page prints the rupee sign. Matches.
- [M] ch9 p112 ("2." printed), p116 ("₹2 is charged ..." printed with the rupee sign). Match.
- [M] ch10 p123 "fine of ₹20,000 to ₹50,000". Page shows the rupee sign. Match. P124 and p125, the Bhopal captions are back. Heading fault is rule K.
- [R] prelims logo fragments. Rule M. "₹ 60.00" matches the page.
- [N] ch5 p63 text is unchanged here and the page was not opened (rule J glue is in the file, see 2016).

## 2020-06-16

- [M] ch1 p14 (rule I), ch3 p33 p38, ch4 p43, ch5 p56 p58 p61, ch6 p70 to p76, ch7 p89, ch8 p96 p101, ch9 p112 p116, ch10 p123 p124 p125. The text of these chapters equals the 2019 text (same hash for ch6, ch8 and ch10) and the 2020 pages 71 and 72 of chapter 6 were rendered but I opened only the 2019 and 2022 renderings of the same pages. Verdict: matches the page, by the 2019 and 2022 pages. Counted as one [M] entry. Rules I, J and K apply as in 2019.
- [R] prelims logo fragments, rule M. "₹ 65.00" matches.

## 2021-08-14

- [M] ch1 p14. "- If the government decides not to promote an officer of the armed forces for being a woman." is whole again and matches the page. The Rule B loss is fixed here. The wrapped Telugu bullet is rule I.
- [M] ch1 p17. "Tyranny: The cruel and unjust use of power or authority." is back and matches the glossary line on the page.
- [M] ch3 p33 p38, ch4 p43, ch5 p56 p58 p61, ch6 p70 to p72 p76, ch7 p89, ch8 p96 p101, ch9 p112 p116, ch10 p123 p124 p125. Same as 2019 and the pages I opened (ch9 p112 and p116, ch10 p123 and p124) match.
- [M] ch9 p111. The new pie caption block has "Scheme / Central Sector Scheme / 10 p." back (rule B fix). The old text stopped at "Centrally Sponsored". Matches the page for those labels.
- [O] ch9 p111. The page shows "Centrally Sponsored Scheme 9p." as a label of the pie. The text has two "9 p." (Subsidies and Defence) and the third is missing (the 2019 and 2020 files have three). Verdict: extraction fault (one-off, rule E). Override:
  ```
  - snapshot: "2021-08-14"
    chapter: 9
    find: "> [caption] Centrally Sponsored\n\n> [caption] Scheme\n\n> [caption] Central Sector Scheme"
    replace: "> [caption] Centrally Sponsored\n\n> [caption] Scheme\n\n> [caption] 9 p.\n\n> [caption] Central Sector Scheme"
    note: "the page 111 pie chart gives 9p. for Centrally Sponsored Scheme, the label was lost"
  ```
  The same override fits 2022-08-02 (chapter 9) and 2023-12-23 (chapter 7).
- [M] ch10 p134. "Sustainable Development Goals (SDGs), www.in.undp.org" is back and is the last line of the reference list on the page. The list entries are glued into one caption and "(Accessed on 24 October 2017)" and "2 January 2008)" stay separate, as before, so no words are lost, but the reading order is broken (existing).
- [R] prelims logo fragments, rule M.

## 2022-08-02

- [M] ch2 p21. "1. that one religious community does not dominate another;" and items 2 and 3. The page prints "1. that" with a space. Rule F is fixed.
- [M] ch9 p114 and p115. "1. Throughout the world ...", "2. There are areas ...", "3. In a few cases ...", "4. Within India ..." all printed with a space after the number. Fixed.
- [M] ch1 p14 p17 (Tyranny and "for being a woman." back, rule I applies), ch3, ch4, ch5, ch6 p71 p72 (page opened, bullets match), ch7, ch8, ch9 p111 (pie, see 2021), ch10 p134. Same texts as 2021 where checked. Matches.
- [R] prelims logo fragments, rule M.

## 2023-12-23-rationalised

- [M] ch1 p14 (armed forces line whole, Telugu bullet is rule I) and p17 (Tyranny back). Pages opened and match.
- [M] ch3 p33 ("4." printed, "Q4." gone).
- [M] ch3 p35. The old sentence "d. Which party do you think will form the government? Give reasons why. Source: http://loksabha.nic.in" is now three items "d.", "Which party do you think will form the government?", "Give reasons why." plus the source line as its own caption. The page shows "d. Which party do you think will form the government? Give reasons why." in the margin and "Source: http://loksabha.nic.in" under the table. Nothing lost. Table of the 17th Lok Sabha has all rows to "Grand Total 543".
- [M] ch4 p50 p52 p55 ("Imagine a situation ...", "Are these different levels ...", "In principle ..." without "Q").
- [M] ch4 p52. "High Court of Karnataka http://karnatakajudiciary.kar.nic.in" is back, joined to the Patna caption ("High Court of Patna http://patnahighcourt.gov.in High Court of Karnataka ...") whereas the page shows two photo captions. Words right, order right. Counted as matching, minor glue.
- [M] ch5 p71. "25 per cent of Muslim children ... (page 58)." is one bullet. Matches.
- [M] ch6 p76 and p81 ("Promoting Social Justice" heading, "₹ 200 per day"), ch7 p92 ("2." printed), p96, ch8 p103 p104 p105, p114 (references). Same as 2021, matches. Chapter 7 p91 pie: "9 p." for Centrally Sponsored is missing, see 2021 entry.
- [M] prelims pdf page 5. The five rationalisation bullets are now "- " items and the closing "This present edition, is a reformatted version ..." is its own paragraph. The page shows five bullets and the paragraph. Matches.
- [O] prelims pdf page 14 (Preamble). The page shows the full Preamble clearly. The text reads "WE, solemnly resolved to constitute India into VEREIGN CIALIST SECULAR DEM CRATIC REPUBLIC and to secure all its citizens cial, ec mic and political; ..." and several leftover fragments. It does not match the page (letters dropped, "Forty-seco ocratic Republic" in the footnote). Verdict: extraction fault (one-off, rule M). Override:
  ```
  - snapshot: "2023-12-23"
    chapter: "prelims"
    find: "THE C NSTITUTI INDIA\n\nPREAMBLE\n\n> [caption] WE, solemnly resolved to constitute India into VEREIGN CIALIST SECULAR DEM CRATIC REPUBLIC and to secure all its citizens cial, ec mic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and pportunity; and to promote among them all FRATERNITY assuring the dignity the individual and the unity and integrity of the Nation IN DUR NSTITUENT ASSEMBLY this twenty-sixth day of November, 1949 d HEREBY AD PT, ENACT AND GIVE TO OURSELVES THIS CO ONSTITUTI THE PEO PLE JUSTICE,\n\n> [caption] (Forty-seco ocratic Republic\" (Forty-seco.e.f. 3.1.1977)\n\n> [caption] re.f. 3.1.1977)\n\n> [caption] vereign Den Subs. by the Co\n\n> [caption] INDIA, having"
    replace: "THE CONSTITUTION OF INDIA\n\nPREAMBLE\n\nWE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a 1[SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC] and to secure to all its citizens:\n\nJUSTICE, social, economic and political;\n\nLIBERTY of thought, expression, belief, faith and worship;\n\nEQUALITY of status and of opportunity;\n\nand to promote among them all\n\nFRATERNITY assuring the dignity of the individual and the 2[unity and integrity of the Nation];\n\nIN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949 do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION.\n\n1. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Sovereign Democratic Republic\" (w.e.f. 3.1.1977)\n\n2. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Unity of the Nation\" (w.e.f. 3.1.1977)"
    note: "ornamental Preamble page on pdf page 14 read with dropped letters, the page image gives the full text"
  ```
  The exact find text must be copied from the file. If the lines differ by a character, replace by line number of the block between "PREAMBLE" and the next page marker.
- [R] prelims logo fragments ("RUE.", "OF EDUCATIONAL RESEARCH AND TRAI", "VATIONAL COUNCI"), rule M. "₹ 65.00" matches.

## 2024-05-24

- [M] ch1 p14 and p17 (same as 2023, rule I for the Telugu bullet), ch3 p33 and p35, ch4 p52 (Karnataka caption back, as 2023), ch5 p71, ch6 p76 p81, ch8 p103 p104 p105 (opened, Bhopal captions back and right, "₹20,000 to ₹50,000" on the page), ch8 p114.
- [R] ch7 p91. The new pie chart (Union Budget 2024-25, nine labels with percentages) is written as "Finance Commission / Central Sector Scheme and other Transfers / (8%) / (16%) / (6%) States’ share of / Subsidies taxes & duties / (20%)" and only eight of the nine percentages are present (Defence "(8%)" is lost). The page shows each label with its percentage. Verdict: extraction fault (rule E). Fix: rule E.
- [M] prelims pdf page 5 (bullets) as in 2023.
- [O] prelims pdf page 14. The Preamble is garbled in the same way as in 2023 with slightly different fragments ("WE. solemnly ...", "(Forty-seco 10'.e.f. 3.1.1977)", "Subs. by the Co J 7 J", "le.f. 3.1.1977)"). Does not match the page. Use the replacement text of the 2023 override with `snapshot: "2024-05-24"` and a find that spans the lines from "THE C NSTITUTI INDIA" to "> [caption] INDIA, having".
- [R] prelims logo fragments ("OF EDUCATIONAL RESEARCH AND TRAI", "VATIONAL COUNCI", "uRt."), rule M. "₹ 65.00" matches.

---

## Summary

Counts (entries as tagged above, one line per finding):
- Matches the page: 56
- Extraction fault, rule: 16
- Extraction fault, one-off: 5 (plus the override-ready rule entries for ch1 p14, ch5 p56, ch5 p63, ch7 p88, prelims p2 and the Bhopal heading)
- Not viewed: 1 (2020 pages of chapters 3, 4, 5, 7 and 8, judged from text identical to 2019 and the 2019 and 2021 renderings, and ch5 p63 of 2019 to 2022)

Earlier rules. Gone: Rule A (no "Q", "Po", "Q2." glyph is left in any text, all removals match the pages), Rule B (the "armed forces for being a woman.", "Tyranny", "Central Sector Scheme", "Sustainable Development Goals", the "High Court of Karnataka" caption and both Bhopal captions are back and right), Rule C (the side question no longer splits a sentence at a page break in 2016 ch6 p70, p73 and ch7 p83, p86, p87), Rule F (list labels "1. that" and "1. Throughout" are spaced in 2022), Rule H (2016 ch6 p74 reads once and correctly). Still open: Rule D (a diff engine matter, extraction now gives the page's order in most places but a few caption orders differ), Rule E (pie labels, now also losing a value), Rule G (the 2022 to 2023 chapter pairing, not touched by this recheck).

The three remaining patterns that matter most:
1. Rule I, a wrapped bullet or run-in heading cut into two blocks ("open a" / "Telugu-medium school in Kerala." in seven editions, and the 2014 "Upholding the Law ... Fundamental" heading). It is new with this rule change.
2. Rules J and L together, text from one page object written into the neighbouring one: the side question in the table row (ch5 p56 in every edition), "Subordinate Courts" glued to the paragraph (ch5 p63 in 2016 and 2019 to 2022), the interleaved law table (2016 ch5 p60), tables II and III cells in table I (2016 ch7 p88) and the poem line glued to the next page's paragraph (2016 ch7 p85/86).
3. Rule M and Rule K, the front and heading noise: the logo and watermark fragments and the garbled Preamble in every prelims, and the doubled heading "Bhopal Gas T Bhopal Gas Tragedy" in every edition. The pie charts of ch9/7 (rule E) come right behind, with a lost label value in 2021 to 2023 and in 2024.
