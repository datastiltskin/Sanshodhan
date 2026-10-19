# Recheck of our-pasts-3 after the rule change

Scope: `review/changes-our-pasts-3.txt` (1007 changed sentences, 7 editions). Pages were rendered at 110 dpi from the source PDFs and opened. The 2019-03-12 "[unreadable]" fonts are not logged.

How this pass worked, stated plainly so the fix pass can trust the verdicts. The image viewer dropped many page renders part way through (request limit), so a verdict "matches the page" or "fault" below rests on a page image that opened. Where an image did not open the entry says "not viewed" and gives only what the extracted text shows, as a hint and not as a verdict. Pages whose image opened:

- 2019-03-12: ch1 p3, p6. ch2 p16. ch5 p56. ch6 p66, p67, p70. ch7 p88, p89. ch8 p95, p99. ch10 p130, p134, p135. ch11 p146, p148, p150, p151, p155, p158. ch12 p168.
- 2014-07-28: ch1 p3. ch2 p22, p24.
- 2020-10-15: prelims pdf page 1. 2021-08-14: ch5 p54, ch10 p135. 2022-08-02: ch3 p27.
- 2023-12-23-rationalised: prelims pdf page 5, ch1 p3, ch3 p32, ch5 p55, p59, ch8 p96. The 2024-08-04 PDF has the same layout and the same text, but no 2024 page image was opened.

Verdict tags used on each entry: [M] matches the page, [R] extraction fault (rule), [O] extraction fault (one-off), [N] not viewed.

The KEYWORDS check: no `### Keywords` heading or "- term" list exists in any our-pasts-3 text or in the change list (they appear only in our-pasts-2). Nothing to check against the page for this book.

Entry format is the one in `review/README.md`. Entries for matching text are one line.

## Patterns (rules), with every place seen

P1. Margin box emitted inside a running sentence. An Activity box or glossary box that sits in the margin beside the text is emitted in the middle of the sentence it is next to, so the sentence is broken, the box words are glued to the sentence, and the continuation on the next page is cut off. Rule: a box (Activity, glossary, Source) must be its own block, and a sentence broken at a page turn must be rejoined over the box.
Seen: 2014 ch1 p3 "dominated Interview your mother ...". 2019/2020/2021/2022 ch1 p3 (same words). 2023 and 2024 ch1 p3 "To do Interview your mother ...". 2023 and 2024 ch5 p59 "white people, Make a list of places ...". 2023 and 2024 ch5 p51 "Nana Saheb, the adopted son of Imagine you are a sepoy ...", and p57 "In Jhansi, Rani Lakshmibai joined the rebel sepoys and" (the Activity word is gone but the sentence still stops at the box, the 2024 break moved two words). 2023 and 2024 ch8 p99 "His earliest Find out about the Jallianwala Bagh massacre ...". 2023 and 2024 ch7 p87 "Phule dedicated his book to all Carefully read Source 3 ...". 2023 and 2024 ch3 p30 "should act as paternal father figures" (Activity box separate but sentence starts mid-page). 2019 to 2022 ch12 p164/165 (and ch10 p132 in 2020 to 2022) "In politics Activity Discuss in your class ..." then "we will be recognising ...". 2019 to 2022 ch10 p137 "the ancient art of mural Look at Fig.25 ...". 2019 ch6 p67 (and 2014 ch6 p65/66) "Mir Taqi Mir said, “The Dargah – ... Cul-de-sac – ...". 2019 ch10 p133 "The characteristic elements Life study – ... of these pictures came into being". 2019 to 2022 ch11/ch9 p149/117 "Picket – ... Illegal eviction – ... had restricted their use of forest resources". 2019 ch11 p148 "Knighthood – ... interventions were in local movements".

P2. Glossary or margin entries glued to the next paragraph, or split and promoted to the wrong type. Rule: each "Term – definition" entry in a margin box is a glossary item, never a heading, never glued to a body sentence.
Seen: 2019 to 2022 ch7/6 p88 "Smelting – ... By 1900, over 84 mills". 2019 ch8 p95 "grammar and Linguist – Someone who knows ... poetry." (all 2019 to 2024). 2019 to 2024 ch5/ch6 p55 "Mutiny – ... Firangis – Foreigners ..." (Firangis belongs to p56). 2019 ch2 p21 and 2014 to 2022 "Mufti – ... Impeachment – ...". 2019 ch11 p157 "“General”constituencies ... After the failure of the Cabinet Mission" (all editions, glossary from p157, sentence from p158). 2014 ch2 p22 "### Sawar – Men on horses" and 2014 ch2 p24 "### Rani Channamma criminal court" (promoted to headings). 2014 ch4 p40 "### Sal – A tree". 2014 ch6 p66 "### Dargah – The tomb of a Sufi saint". 2019 to 2024 "### Provincial autonomy" then "Capacity of the provinces ... federation Peasants, tribals and women participated" (ch11 p154, ch9 p122, ch8 p106 in 2023/24). 2019 to 2022 ch7/6 p83 "Activity Why do you think the Act was called ...".

P3. Caption title glued to its description with no full stop, and caption blocks emitted in a different order from the page. Words are right, only the sentence boundary is wrong. Seen: ch3 p32 (Fig. 7), ch5 p64 (Fig. 17), ch7/6 p79, p83, p88 (Fig. 1, 7, 11), ch8/7/6 p97 (Fig. 3), ch9/8/7 p115 (Fig. 10), ch10 p133, p135, p136 (Fig. 15, 21, and Fig. 22/23 emitted as "Fig. 23 ... Fig. 22 ..." in reverse order), ch11/9/8 p148, p150, p155 (Fig. 7, 8, 14), ch12/10 p168, p170 (Fig. 6, 7, 9). Not a fault the diff cares about unless one edition splits and another glues, which now happens between 2014 (glued) and 2019 (glued) less than before.

P4. Numbered Activity items split at line wraps. Seen: 2019 ch10 p128 (and 2014 p128 text is whole): "2. What are the ways in which the artist has depicted" | "the victory of the British?" | "3. Notice the position of the British flag (the Union" | "Jack) in Figs. 7 and 8. Why is it placed there?". Rule: join continuation lines of an Activity item until the next numeral.

P5. Page-turn rejoin blocked by a caption. Seen: 2014 and 2019 ch10 p127/128 "One of the first of these history paintings was produced" | "by Francis Hayman in 1762 ...". The old text had it whole, so this one is a regression.

P6. Bullet list glued into one sentence, last item left as "- ". Seen: 2014 and 2019 ch11 p141, and 2020/2021/2022 ch9 p109 (the "In the previous chapters we have looked at:" list). The 2023/2024 texts are right (one item per line).

P7. Two-column "Match the following" exercise read down the page, mixing the columns. Seen: 2014 ch2 p24 (also a candidate for the diff-noise cleanup, since it is an exercise).

P8. Cover and licence page fragments. Seen: 2020, 2021, 2022 prelims "EDUCAT IONAL RESEARCH AND" and "IONAL COUNCI".

## Patterns from the earlier review that are now gone

Activity arrow "†" and "\x86" and the square bullet "¢" (removed from every list). Backtick rupee sign now "₹" (ch4 p46 in 2023/2024, all prelims). Letter-spaced "I n t h e B o m b a y", "e d u c a t i o n w h i c h", "a n d o f f i c i a l s", "P h e r o z e s h a h", "r i c h e n o u g h". "1.In" and "2.Notice" spacing now "1. In" and "2. Notice". Captions swallowed in the middle of a sentence ("He also established a close Fig. 8 – Tipu Sultan relationship", "Fig. 10 – Lord Hastings In the late 1830s", "There is one thing common in the Fig. 5 ... two prints", "Fig. 12 – Shri Narayana Guru Gulamgiri"). "More Azad was born" (the "More" belonged to the next sentence, now "More importantly" is whole). Plain-paragraph page turns are rejoined ("relationship with the French", "They tell us what the officials thought ... preserve for posterity", "The liquid was drained off ...", "Of these, the most important are", "Others travelled around the country"). Run-in headings "Revenue for the Company", "Derozio and Young Bengal", "The Brahmo Samaj", "The Prarthana Samaj", "The Aligarh Movement", "The Singh Sabha Movement", "Early years of industrialisation in Japan" are now separate lines (2019 to 2022, see P2 for the editions that still glue "Gulamgiri").

## 2014-07-28

### our-pasts-3 2014-07-28, chapter 1, printed page 3
- Hunk: "Religious intolerance ... dominated" and "Interview your mother ..." were two sentences, now one: "... dominated Interview your mother or another member of your family to find out about their life."
- Images: p3 shows the Activity box in the right margin and the body paragraph ending "dominated" at the foot of the page. "social life." is the first line of p4.
- Verdict: [R] extraction fault (rule), P1. The old text was better here (box separate).
- Fix: P1. Box as its own block, sentence rejoined over the page turn to "dominated social life."

### our-pasts-3 2014-07-28, chapter 2, printed page 22
- Hunk: "Dharmashastras – ... Sawar – Men on horses Musket – ..." became "Dharmashastras – ... Musket – ... Matchlock – ..." plus a new heading "### Sawar – Men on horses".
- Images: the margin box lists Dharmashastras, Sawar, Musket, Matchlock in that order, all glossary entries.
- Verdict: [R] extraction fault (rule), P2. Sawar is not a heading.
- Fix: P2. Override if one-off: snapshot "2014-07-28", chapter 2, find "### Sawar – Men on horses", replace "Sawar – Men on horses", note "glossary entry in the margin box on p22, not a heading". The entry order of the glued line (Sawar second) is still wrong.

### our-pasts-3 2014-07-28, chapter 2, printed page 24
- Hunk: "“Tiger of Mysore” right to collect land revenue faujdari adalat Sepoy Rani Channamma criminal court sipahi led an anti-British movement in Kitoor" became the same without "Rani Channamma criminal court", which is now "### Rani Channamma criminal court".
- Images: the page shows the "Match the following" exercise in two columns (Diwani | Tipu Sultan, “Tiger of Mysore” | right to collect land revenue, faujdari adalat | Sepoy, Rani Channamma | criminal court, sipahi | led an anti-British movement in Kitoor).
- Verdict: [R] extraction fault (rule), P7.
- Fix: P7. Read the two columns as pairs, or drop the exercise from the diff as noise.

### our-pasts-3 2014-07-28, chapter 2, printed pages 16, 18 and 20
- Hunk: "He also established a close Fig. 7 – Tipu Sultan relationship ..." now whole. "Fig. 10 – Lord Hastings In the late 1830s ..." now whole. New "Fig. 7 – Tipu Sultan", "Fig. 10 – Lord Hastings", "Fig. 11 c".
- Images: not viewed for 2014. The same sentence is on the 2019 p16 image (viewed), where "He also established a close" ends the page and "relationship with the French in India" starts p17, and the Tipu Sultan caption sits left of the text.
- Verdict: [N] not viewed. Text change looks right.
- Fix: none until opened.

### our-pasts-3 2014-07-28, chapters 1, 2, 3, 4, 5, printed pages 1, 15, 28, 42, 55
- Hunk: " Activity" or "Activity " changes only by trailing space, or a lone "Activity" line now carried by "### Activity".
- Images: not viewed. No word differs.
- Verdict: [N] not viewed. Whitespace only.
- Fix: none.

### our-pasts-3 2014-07-28, chapter 4 p40, chapter 5 p53 and p54, chapter 6 p65 and p66
- Hunk: "Sal – A tree" became "### Sal – A tree" (p40). "Vishnubhatt Godse, Majha Pravaas, pp. 23-24." and "Source 2" are new separate lines (p53, p54). "Dargah – The tomb of a Sufi saint" became "### Dargah ..." (p66).
- Images: not viewed. The text shows a glossary entry promoted to a heading (P2), and the Source 2 label removed from the Fig. 3 caption (good).
- Verdict: [N] not viewed. Sal and Dargah headings look like P2 faults.
- Fix: P2, confirm on the page first.

### our-pasts-3 2014-07-28, chapters 7 to 12, printed pages 79 to 170 (the "-" captions that reappear glued to their description)
- Hunk: 2014 ch7 p79, p83, p84, p85, p88, p89, ch8 p95 to p97, ch9 p114 to p116, ch10 p125 to p137, ch11 p141 to p158, ch12 p164 to p170. Every "-" line is on the page in some other sentence (checked against the new text, all words present). Examples: "Fig. 1 – Trading ships ..." and "Surat in Gujarat ..." are now one caption sentence.
- Images: not viewed for 2014 (the 2019 pages with the same text were viewed, see 2019 entries).
- Verdict: [N] not viewed. No sentence was lost in the text (every "-" line has its words in the new file), but P1, P2, P3 and P5 apply as listed above.
- Fix: P1, P2, P3, P5, P6.

## 2019-03-12

### our-pasts-3 2019-03-12, chapter 1, printed page 3
- Hunk: "... dominated Activity Interview your mother ..." became "... dominated Interview your mother ...".
- Images: the Activity box is in the right margin. The body sentence stops at "dominated". "social life." is on p4.
- Verdict: [R] extraction fault (rule), P1. The word "Activity" was dropped, the glue remains.
- Fix: P1.

### our-pasts-3 2019-03-12, chapter 1, printed pages 5, 6, 7
- Hunk: "Fig. 4 – The National Archives of India came up in the 1920s" now glued to "When New Delhi was built ..." (p5). "They tell us what the officials thought, what" (p6) is now joined with "they were interested in, and what they wished to preserve for posterity" (p7). The caption "Images need to be carefully studied for they project the viewpoint of those who create them." is now its own sentence.
- Images: p6 viewed. The body ends "They tell us what the officials thought, what", the Fig. 5 caption sits in the left margin. The joined sentence matches. p5 and p7 not viewed.
- Verdict: p6 [M] matches the page. p5 and p7 [N] not viewed.
- Fix: none for p6.

### our-pasts-3 2019-03-12, chapter 1, printed pages 1 and 2
- Hunk: "Look carefully at Fig.1 and write a paragraph ... † Activity All such historical questions ..." became two clean sentences: "Look carefully at Fig.1 ..." and "All such historical questions refer us back to notions of time."
- Images: not viewed.
- Verdict: [N] not viewed. The "†" is gone and no word was lost. The "### Activity" heading now follows the Activity text instead of preceding it (the box heading is above its text on the page).
- Fix: P1 for the order of heading and text, after viewing.

### our-pasts-3 2019-03-12, chapter 2, printed page 16
- Hunk: "He also established a close Fig. 8 – Tipu Sultan relationship with the French in India, and modernised his army with the" now "He also established a close relationship with the French in India, and modernised his army with their help." New "Fig. 8 – Tipu Sultan". The long caption sentence is split into "The treaties that followed ..." and "Here, however, he poses in regal splendour, towering over the Resident."
- Images: p16 shows the body ending "He also established a close" at the foot and the Fig. 7 caption (Nawab Shujauddaulah) and the Fig. 8 portrait caption in the left column. The new text matches. p17 not viewed (the continuation).
- Verdict: [M] matches the page.
- Fix: none.

### our-pasts-3 2019-03-12, chapter 2, printed pages 20 and 21
- Hunk: "Fig. 11 a, b, c – Expansion ..." now glued to "Look at these maps ..." (p20). "From 1772 a new system of justice was established." now its own sentence (p21). "Mufti – ... Impeachment – ..." changed in a few characters.
- Images: not viewed.
- Verdict: [N] not viewed. Text looks right for p20. Mufti and Impeachment are two margin entries run together (P2).
- Fix: P2.

### our-pasts-3 2019-03-12, chapter 3, printed pages 28, 32, 34
- Hunk: "Activity †" now "Activity" (p28). Fig. 7 caption glued to its first sentence (p32). "Gradually the indigo separated out ... a clear liquid rose to the surface." and "The liquid was drained off ..." rejoined over the page turn (p34).
- Images: not viewed for 2019. The 2023 p32 image (viewed) shows the same caption beside the picture and the page 34 sentence is split between the two figure captions on the 2023 layout.
- Verdict: [N] not viewed. Text changes look right (P3 only).
- Fix: P3.

### our-pasts-3 2019-03-12, chapter 4, printed page 49
- Hunk: "Why do we need cash!" became "### Why do we" and "> [note] need cash!".
- Images: not viewed.
- Verdict: [N] not viewed. Every other edition prints "### Why do we need cash!" as one heading, so this one is probably an extraction split (O).
- Fix: after viewing the page, snapshot "2019-03-12", chapter 4, find "### Why do we\n\n> [note] need cash!", replace "### Why do we need cash!", note "box title split over two lines on p49".

### our-pasts-3 2019-03-12, chapter 5, printed pages 55, 56, 64
- Hunk: "Mutiny – ... Firangis – Foreigners The term reflects an attitude of contempt." (p55) now "Mutiny – When soldiers as a group disobey their officers in the army" (p55) and "Firangis – Foreigners The term reflects an attitude of contempt." (p56). "On 29 March 1857, a young soldier, Mangal Pandey, ..." no longer carries the Mutiny entry. New "The battle continued all through the night." (p56). Fig. 17 caption glued (p64).
- Images: p56 viewed. The Firangis entry is in the left margin of p56, the Fig. 4 caption ends "The battle continued all through the night.", "From Meerut to Delhi" opens with "On 29 March 1857 ...". The new text matches p56. The Mutiny entry on p55 not viewed.
- Verdict: p56 [M] matches the page. p55 and p64 [N] not viewed.
- Fix: none for p56.

### our-pasts-3 2019-03-12, chapter 6, printed pages 66, 67, 70
- Hunk: p66 "Of these, the most" now rejoined as "Of these, the most important are the capital cities built between the twelfth and seventeenth centuries." The Bombay port caption glued to its description. p67 "Delhi during Shah Jahan's time was also an important centre of Sufi culture." is now clean. "No wonder the poet Mir Taqi Mir said, “The Dargah – ... Khanqah – ... Idgah – ... Cul-de-sac – ..." contains the four glossary entries. p70 "Notice the buildings all around the Masjid." and "They were cleared after the Revolt of 1857." are caption text.
- Images: p66 and p67 viewed. p66 ends "Of these, the most" and p67 starts "important are the capital cities ..." under the Fig. 3 caption, so the rejoin is right. On p67 the body ends the page with “The" (the quotation continues on p68) and the four glossary entries (Dargah, Khanqah, Idgah, Cul-de-sac) are in the right margin box. p70 shows the Fig. 7 caption "Notice the buildings all around the Masjid. They were cleared after the Revolt of 1857." and the Activity box in the left margin.
- Verdict: p66 rejoin [M] matches. p67 "Delhi during Shah Jahan's time ..." [M] matches. p67 "Mir Taqi Mir said, “The Dargah – ..." [R] extraction fault (rule), P1. p70 [M] matches.
- Fix: P1 for p67. The quoted couplet on p68 ("streets of Delhi aren't mere streets ...") is the continuation.

### our-pasts-3 2019-03-12, chapter 7, printed pages 79, 83, 84, 85, 88, 89, 93
- Hunk: Fig. 1, Fig. 7 and Fig. 9 captions glued to their descriptions (P3). "It was famous for its mulmul and jamdani weaving." (p84) now a separate sentence. "Do you know what a pit loom is?" separate (p85). "Smelting – ... By 1900, over 84 mills started operating in Bombay." (p88). "Fig. 11 – Tipu's sword ..." caption (p88). "Bellows – A device or equipment that can pump air" now separate (p89), "Some communities like the Agarias specialised in the craft of iron smelting." is the Fig. 13 caption on p90. "Early years of industrialisation in Japan" now a separate heading (p93).
- Images: p88 and p89 viewed. On p88 the Smelting entry is the left margin box at the top and "By 1900, over 84 mills started operating in Bombay." opens the body column, so the glued sentence "Smelting – ... By 1900 ..." joins a glossary entry to a body sentence. The Fig. 11 caption sits at the lower left. On p89 the Activity box (Why would the iron and steel making industry ...) and the Bellows entry are right-margin boxes and Fig. 12 is a caption, so the separate "Bellows" line matches. p79, p83, p84, p85, p93 not viewed.
- Verdict: p88 "By 1900" glued to Smelting [R] extraction fault (rule), P2. p88 Fig. 11 caption [M] matches. p89 Bellows [M] matches. p79, p83, p84, p85, p93 [N] not viewed.
- Fix: P2 for p88.

### our-pasts-3 2019-03-12, chapter 8, printed pages 95, 96, 97, 99
- Hunk: p95 "At Calcutta, he began spending many hours a day with pandits who taught him the subtleties of Sanskrit language, grammar and Linguist – Someone who knows and studies several languages poetry." (the Madrasa entry that used to be inside has moved to p96). p96 "Madrasa – ... Not all officials shared these views." p97 "Fig. 3 – Monument ..." glued to "This image represents how Orientalists thought of British power in India." p99 "Write about your reactions. " now "Write about your reactions."
- Images: p95 and p99 viewed. On p95 the sentence "... grammar and" ends the page and "poetry." starts p96, and the Linguist entry is a margin box at the right, so the glued Linguist words are a fault. The Fig. 1 caption is at the lower right. On p99 the Activity box reads "Imagine you are living in the 1850s. You hear of Wood's Despatch. Write about your reactions." so the new line matches. p96 and p97 not viewed.
- Verdict: p95 [R] extraction fault (rule), P2. p99 [M] matches. p96 and p97 [N] not viewed. Text of p96 still glues the Madrasa entry to "Not all officials shared these views." which is the first line of the body on p97.
- Fix: P2 (p95, p96).

### our-pasts-3 2019-03-12, chapter 9, printed pages 114, 115, 116, 120, 121
- Hunk: p114 and p115 captions glued to their descriptions. p116 "I n t h e B o m b a y Presidency ..." now "In the Bombay Presidency ...", "Fig. 12 – Shri Narayana Guru" separate from "One of the most vocal amongst ...". p120 and p121 headings "Derozio and Young Bengal", "The Brahmo Samaj", "The Prarthana Samaj", "The Aligarh Movement", "The Singh Sabha Movement" are now separate lines.
- Images: not viewed (the p116, p120, p121 renders did not open).
- Verdict: [N] not viewed. Text changes look right (spaced letters gone, headings separate, no word lost).
- Fix: none until opened. The 2014, 2023 and 2024 texts still glue "Gulamgiri One of the most vocal ..." (P2, "run-in heading glued") while 2019 to 2022 split it.

### our-pasts-3 2019-03-12, chapter 10, printed pages 125 to 137
- Hunk: p125 "Portrait – ... Portraiture – ... Commission – ..." now glued to "As portrait painting became popular ...". p126 "1.In" to "1. In" and "2.Notice" to "2. Notice". p127 "One of the first of these history paintings was produced" and p128 "by Francis Hayman ... (Fig. 7)." p128 Activity items split into fragments. p130 Activity items "2. If you were a nawab ...", "3. Do you think ..." now spaced. p131 Perspective entry. p132 "Notice how the artists have modernised traditional images. Hanuman is wearing footwear ..." caption. p133 "Life study ..." glued into "The characteristic elements ... of these pictures came into being in the late nineteenth century." and Fig. 15 caption glued. p134 Fig. 18 caption. p135 "Others travelled around the country searching ..." joined. Fig. 21 caption glued. p136 "Fig. 23 – ... Fig. 22 – ... The railway station was built between 1878 and 1887." p137 "... the ancient art of mural Look at Fig.25 ...".
- Images: p130, p134, p135 viewed. p130: the Activity box (Compare Figs. 8 and 10, items 1 to 3) is in the body column below the mural, the Mural entry is in the left margin. The spaced numerals match. p134: "of these pictures came into being in the late nineteenth century." is the first body line over the Fig. 16 picture, and Figs. 16, 17, 18 have their own captions. p135: "Others travelled around the country searching for ruined buildings ..." is one run of body text wrapped around the Fig. 19 picture, and the Fig. 21 caption is "A nationlist demonstration in a Bombay street, photograph by Vikar" followed by "By the late nineteenth century Indian photographers ..." and "They recorded the nationalist marches and meetings ..." (the print has "nationlist"). p125 to p128, p131 to p133, p136, p137 not viewed (those renders did not open).
- Verdict: p130 [M] matches. p134 Fig. 18 caption [M] matches. p135 joined sentence [M] matches, Fig. 21 caption [M] matches (title glued to description, P3). p133 "The characteristic elements Life study – ... of these pictures came into being" [R] extraction fault (rule), P1 (the p133 half not viewed, the p134 half viewed). p127/128 split and p128 fragments [R] extraction fault (rule), P5 and P4, from the text and from the p128 sentence layout (not viewed). p125 to p128, p131, p132, p136, p137 otherwise [N] not viewed.
- Fix: P1, P3, P4, P5. One-off, p127: the stray token "fghsdtysd" (in the committed text too, not part of this change) is hidden text on p127. Override: snapshot "2019-03-12", chapter 10, find "fghsdtysd", replace "", note "stray hidden text on p127 between the nawab paragraph and the heading Painting history". Same text in 2014 ch10. Not viewed.

### our-pasts-3 2019-03-12, chapter 11, printed pages 141 to 158
- Hunk: p141 the seven "¢ ..." lines are gone and the bullet list is now one sentence "The British conquest of territories, and takeover of kingdoms Introduction of new laws ... The revolt of 1857 and its aftermath" plus a lone "- The decline of crafts and growth of industries". p146 "He was also an active member of the Arya Samaj." p148 Fig. 7 caption now glued to "The people are pointing to the bullet marks on the wall." p149 Picket, Mahants, Illegal eviction entries inside a sentence. p150 Fig. 8 caption glued. p151 "A major figure in the freedom movement, Das was a lawyer from East Bengal." and "He was especially active in the Non-Cooperation Movement." p153 "Women in the freedom struggle: Ambabai from Karnataka" now a separate line and "Provincial autonomy" (p154) a heading with "Capacity of the provinces ... federation Peasants, tribals and women participated ..." glued. p154 "Active in the national movement since the early 1920s, Naidu was a significant leader of the Dandi March." and "She was the first Indian woman to become President of the Indian National Congress (1925)." p155 "More Azad was born ..." now "Azad was born ..." and Fig. 14 caption as one sentence. p156 Patel caption split in two. p157 "More importantly, ..." whole. p158 "“General”constituencies ... After the failure of the Cabinet Mission ...".
- Images: p146, p148, p150, p151, p155 and p158 viewed. p146: the Fig. 5 caption (Lala Lajpat Rai, "He was also an active member of the Arya Samaj."), then two margin boxes (Revolutionary violence, Council) and the Activity box (Find out which countries fought the First World War). p148: the Activity box (Find out about the Jallianwala Bagh massacre ...) and the Knighthood entry are left-margin boxes, the body starts "interventions were in local movements in Champaran" (continuing from p147), the Fig. 7 caption reads "The people are pointing to the bullet marks on the wall." p150: the Mahants and Illegal eviction entries are the left-margin box at the top, the body starts "had restricted their use of forest resources in various ways.", the Fig. 8 caption "In popular images too Mahatma Gandhi ..." is in the left column. p151: Fig. 9 caption "A major figure in the freedom movement, Das was a lawyer from East Bengal. He was especially active in the Non-Cooperation Movement." p155: the Fig. 14 caption is at the top right and the body ends "More" with "importantly" on the next page. p158: the para "After the failure of the Cabinet Mission ..." is the first text, beside the Fig. 22 picture. p141, p149, p153, p154, p156, p157 not viewed.
- Verdict: p146 "He was also an active member of the Arya Samaj." [M] matches. p146 Revolutionary violence, Council and Activity glued into one block [R] extraction fault (rule), P2. p148 Fig. 7 caption [M] matches. p148 "Knighthood – ... interventions were in local movements" [R] extraction fault (rule), P1. p150 Fig. 8 caption [M] matches. p149/150 "Picket – ... had restricted their use of forest resources in various ways." [R] extraction fault (rule), P1 (the sentence is whole on the page, p149 end and p150 start, the entries are in two different margin boxes). p151 [M] matches. p155 "Azad was born ..." and Fig. 14 caption [M] matches (words), "More importantly" rejoin [M] matches. p158 "“General”constituencies ... After the failure of the Cabinet Mission ..." [R] extraction fault (rule), P2 (the entry is on p157, the sentence is on p158, so the sentence is credited to the wrong page and carries the entry). p141 [R] extraction fault (rule), P6 (from the text, the p141 image did not open). p153, p154, p156, p157 [N] not viewed. The "-" lines on p141, p149, p150, p151, p154, p155, p157, p158 are all in the new text (checked word by word), so no sentence is lost.
- Fix: P1, P2, P6.

### our-pasts-3 2019-03-12, chapter 12, printed pages 164, 168, 170
- Hunk: p164 "A lawyer and economist, he is best known ... the father of the Indian Constitution Activity Discuss in your class, one advantage and one disadvantage today of the decision to keep English as a language of India." was split in two, and "In politics we will be recognising the principle of one man one vote and one value." (p164/165) is now "In politics Activity Discuss in your class ..." on p164 and "we will be recognising ..." on p165. p168 Fig. 6 and Fig. 7 captions glued to their descriptions, "It was completed in 1960." separate. p170 "The search for an independent foreign policy" now a separate heading, Fig. 9 caption glued to "Krishna Menon led the Indian delegation ...".
- Images: p168 viewed. The Fig. 6 caption "Bridges and dams became the symbol of development in independent India." and the Fig. 7 caption "This was the first of the four dams built on the Chambal river in Madhya Pradesh. It was completed in 1960." match, and the State entry is a margin box. p164 and p170 not viewed.
- Verdict: p168 [M] matches. p164 "In politics Activity Discuss ..." and "we will be recognising ..." [R] extraction fault (rule), P1. This is a regression (the committed text joined "In politics we will be recognising ..."). p170 [N] not viewed.
- Fix: P1.

### our-pasts-3 2019-03-12, part1-prelims and part2-prelims
- Hunk: "1.How, When and Where 1" now "1. How, When and Where 1" (and 2 to 6). "` 50.00" now "₹ 50.00".
- Images: pdf pages 8 and 9 of part1-prelims did not open.
- Verdict: [N] not viewed. The "1." spacing and rupee fix are the same as elsewhere. The new "## 1. How, When and Where 1" is a heading while "2." to "6." are plain lines (heading level changes, minor).
- Fix: none.

## 2020-10-15

### our-pasts-3 2020-10-15, chapters 1, 2, 3, 5, 6, 7, 8, 9, 10
- Hunk: same sentences as 2019 (chapter numbers shift: ch6 weavers, ch7 civilising, ch8 women, ch9 national movement, ch10 India after independence). ch10 p132, ch9 p117, ch8 p103 and p102, ch5 p55 and p56 did not open for 2020.
- Images: not viewed for 2020. The sentences and the changes are identical to those in 2019 which were viewed.
- Verdict: [N] not viewed for each page, with the same hint as the 2019 entry: P1 in ch10 p132 "In politics Activity ...", ch9 p117 "Picket – ...", P2 in ch6 p74 "Smelting ...", ch5 p55 "Mutiny ...", P6 in ch9 p109, P3 captions, and the matching changes (ch6 p70 "It was famous for its mulmul ...", ch8 p102 "In the Bombay Presidency ...", ch8 p103 "### Gulamgiri" as its own heading, ch9 p114 "He was also an active member ...") look right.
- Fix: P1, P2, P3, P6.

### our-pasts-3 2020-10-15, prelims
- Hunk: "Raq" is gone. "Saas SNe TART cla srfer fsTaror fap sy IONAL RESEARCH AND EDUCAT ONAL COUNCI Published at the Publication Division ..." became "Published at the Publication Division ...". New "EDUCAT IONAL RESEARCH AND" and "IONAL COUNCI". "` 65.00" now "₹ 65.00".
- Images: the cover (pdf page 1) shows "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING" in one line and the Hindi line above it. There are no fragments on the page.
- Verdict: the removal of "Raq" and the garbage run [M] matches the page. "EDUCAT IONAL RESEARCH AND" and "IONAL COUNCI" [O] extraction fault (one-off), P8: fragments of the cover line. "₹ 65.00" [N] not viewed (pdf page 2 did not open for 2020, the 2021 render did not open either).
- Fix: three snapshots, same text. Override 1: snapshot "2020-10-15", chapter "*", find "EDUCAT IONAL RESEARCH AND", replace "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING", note "cover line on pdf page 1, split into fragments by the font". Override 2: snapshot "2020-10-15", chapter "*", find "> [caption] IONAL COUNCI\n\n", replace "", note "second fragment of the same cover line". Repeat both for snapshots "2021-08-14" and "2022-08-02" (their prelims carry the same two fragments).

## 2021-08-14

### our-pasts-3 2021-08-14, chapter 5, printed page 54
- Hunk: "Fig. 3 – Rebel sepoys at Meerut attack officers, enter their homes and set fire to buildings Source 2" became the caption alone, and "Source 2" is a separate line.
- Images: p54 viewed. "Source 2" is the label at the top left of the pink box, the Fig. 3 caption is at the bottom, and "Source 2 contd." is a label at the bottom right.
- Verdict: [M] matches the page.
- Fix: none.

### our-pasts-3 2021-08-14, chapter 5 p56 and chapter 6 (weavers) p71
- Hunk: ch5 p56 "On 8 April 1857, a young soldier, Mangal Pandey ..." no longer carries the Mutiny entry. ch6 p71 "Proceedings of the Board of Trade, 3 February 1824" is a new line.
- Images: not viewed.
- Verdict: [N] not viewed. Note the 2021 edition prints "8 April 1857" where 2019 prints "29 March 1857", a real change in the book.
- Fix: none.

### our-pasts-3 2021-08-14, chapter 10, printed page 135
- Hunk: new "Fig. 5 (c) – Indian States in 1975".
- Images: p135 viewed. The caption "Fig. 5 (c) – Indian States in 1975" is under the second map, beside the Activity box.
- Verdict: [M] matches the page.
- Fix: none.

### our-pasts-3 2021-08-14, chapters 1, 2, 3, 7, 8, 9, 10 and prelims
- Hunk: identical to 2019 and 2020 (see those entries), plus the prelims lines "Printed on 80 GSM paper with NCERT watermark Cover and Layout Arrt Creations Cartography Cartographic Designs Agency" now split into "Printed on 80 GSM paper ...", "Cover and Layout", "Arrt Creations", "Cartography Cartographic Designs Agency".
- Images: not viewed.
- Verdict: [N] not viewed. The prelims credit lines are now separate, which looks right (the credits are separate boxes), the "Arrt" spelling is the print's.
- Fix: P1, P2, P3, P6 as for 2019, and the cover override for 2021 (see 2020).

## 2022-08-02

### our-pasts-3 2022-08-02, chapter 3, printed page 27
- Hunk: "Revenue for the Company The Company had become the Diwan ..." became "The Company had become the Diwan, but it still saw itself primarily as a trader." and a new heading "Revenue for the Company".
- Images: p27 viewed. "Revenue for the Company" is a bold sub-heading and the next paragraph begins "The Company had become the Diwan ...".
- Verdict: [M] matches the page.
- Fix: none.

### our-pasts-3 2022-08-02, chapter 5 p54, p55, p56 and every other chapter
- Hunk: same as 2021 and 2019 (ch5 p54 Source 2, p55 Mutiny entry still glued to the 8 April paragraph, p56 Firangis, ch10 p135 Fig. 5 (c), and so on) and the prelims fragments "EDUCAT IONAL RESEARCH AND", "IONAL COUNCI".
- Images: not viewed (the 2022 p55 and p56 renders did not open).
- Verdict: [N] not viewed. Hints as in 2019 and 2021. Note: 2022 ch5 p55 text still puts "Mutiny – ... On 8 April 1857, ..." together in one sentence, so the paragraph is credited to p55 while on the page it opens p56 under "From Meerut to Delhi" (P2, from the 2021 p55/56 pair shown by the 2023 p55 image).
- Fix: P1, P2, P3, P6, P8.

## 2023-12-23-rationalised

### our-pasts-3 2023-12-23-rationalised, chapter 1, printed pages 3 and 4
- Hunk: "To do Activity Interview your mother ..." became "To do Interview your mother or another member of your family to find out about their life."
- Images: p3 viewed. The Activity box is in the right margin and the body ends "... British rule, Mill felt, could civilise India. To do" with "this, it was necessary to introduce ..." on p4.
- Verdict: [R] extraction fault (rule), P1. The words "To do" belong to "To do this, ..." on p4.
- Fix: P1. (The same text and fault in 2024.)

### our-pasts-3 2023-12-23-rationalised, chapter 1, printed pages 5, 6, 7
- Hunk: same as 2019 ch1 p5, p6, p7.
- Images: not viewed for 2023 (the same sentences were viewed on 2019 p6, matching).
- Verdict: [N] not viewed.
- Fix: none.

### our-pasts-3 2023-12-23-rationalised, chapter 2, printed pages 16, 20, 21
- Hunk: same as 2019 ch2. New "Fig. 14 c – India, 1857" (p20).
- Images: not viewed. The 2019 p16 image matches the p16 rejoin.
- Verdict: [N] not viewed.
- Fix: none.

### our-pasts-3 2023-12-23-rationalised, chapter 3, printed pages 30 and 32
- Hunk: p30 "There is one thing common in the Fig. 5 – A kalamkari print, twentieth-century India two prints: both use a rich blue colour – commonly called indigo." now "There is one thing common in the two prints: both use a rich blue colour – commonly called indigo." and a separate caption line. p32 "commercial agents a n d o f f i c i a l s o f t h e Company" now "commercial agents and officials of the Company". Fig. 7 caption glued to its first description sentence.
- Images: p32 viewed. The body reads "As the indigo trade grew, commercial agents and officials of the Company began investing in indigo production." (widely spaced in the print) and the Fig. 7 caption "In the eighteenth century, French planters produced indigo and sugar in the French colony of St Domingue in the Caribbean islands." is in the left column, and the print has "Scuhodolski". p30 not viewed.
- Verdict: p32 [M] matches the page. p30 [N] not viewed.
- Fix: none.

### our-pasts-3 2023-12-23-rationalised, chapter 4, printed pages 43, 44, 46
- Hunk: new "The entire village helps when log huts are built." (p43). Fig. 7 caption glued to "Note the difference between rice cultivation ..." (p44). "` 3 to ` 4" now "₹ 3 to ₹ 4" (p46).
- Images: not viewed (p43, p44, p46 did not open).
- Verdict: [N] not viewed. The ₹ change is the same fix as elsewhere.
- Fix: none.

### our-pasts-3 2023-12-23-rationalised, chapter 5, printed pages 51, 55, 56, 57, 59
- Hunk: p51 "Nana Saheb, the adopted son of Activity Imagine you are a sepoy ..." now without "Activity". p54 "Source 2" separate. p55 "Mutiny – When soldiers ..." and "On 8 April 1857, a young soldier, Mangal Pandey ..." now separate, "Firangis – Foreigners The term reflects an attitude of contempt." is now glued to the Mutiny entry on p55. p57 "In Jhansi, Rani Lakshmibai joined the rebel sepoys and" (Activity word gone). p59 "... if they had not killed any white people, Make a list of places where the uprising took place in May, June and July 1857."
- Images: p55 and p59 viewed. p55: the Mutiny entry is a right-margin box, the Activity box (two numbered questions) is above it, and the body ends the page. The 8 April paragraph is not on p55, it opens p56 under "From Meerut to Delhi", so separating it is right. p59: the Activity box is a right-margin box "Make a list of places where the uprising took place in May, June and July 1857." and the body ends "... and if they had not killed any white people," with "they would remain safe" on p60. p51, p57 not viewed.
- Verdict: p55 "On 8 April 1857 ..." separated from the Mutiny entry [M] matches. p55 "Firangis – Foreigners ..." joined to the Mutiny entry on p55 [R] extraction fault (rule), P2 (Firangis is on p56). p59 [R] extraction fault (rule), P1. p51 and p57 [N] not viewed (the text still shows P1 glue at "Nana Saheb, the adopted son of Imagine you are ..." and the break at "and").
- Fix: P1, P2.

### our-pasts-3 2023-12-23-rationalised, chapter 6, printed pages 65, 66, 67, 69
- Hunk: same as 2019 ch8 for p65 and p67. p69 "We must emphatically declare that the e d u c a t i o n w h i c h we desire ..." now "... the education which we desire ...".
- Images: not viewed (p69 did not open).
- Verdict: [N] not viewed. Letter-spacing gone (good), same as the 2023 ch3 p32 fix that was viewed.
- Fix: none.

### our-pasts-3 2023-12-23-rationalised, chapter 7, printed pages 84, 85, 86, 87
- Hunk: p84, p85 captions glued (P3). p86 "Fig. 12 – Shri Narayana Guru" now separate and "Gulamgiri One of the most vocal amongst ..." (heading glued to the paragraph, unlike 2019 to 2022). p86 "I n t h e B o m b a y Presidency" now "In the Bombay Presidency". p87 "Phule dedicated his book to all Activity Carefully read Source 3 ..." without "Activity".
- Images: not viewed.
- Verdict: [N] not viewed. P1 remains in p87, P2 (heading glued, Rule B) at p86.
- Fix: P1, P2.

### our-pasts-3 2023-12-23-rationalised, chapter 8, printed pages 93, 95, 96, 98, 99, 100, 102, 105, 106, 108, 109
- Hunk: p93 the bullets are now one item per line (good) and "On the basis of what you have read about these issues ..." is separate. p95 "The demand for Indianisation ..." changed a few characters. p96 "P h e r o z e s h a h i s nowadays too busy with his personal work … They are already r i c h e n o u g h … M r ." became "Pherozeshah is nowadays too busy with his personal work … They are already rich enough … Mr. Telang too r em ains busy." and the lone "T e l a n g t o o r em ains busy." is gone. p99 "His earliest Activity Find out about the Jallianwala Bagh massacre." now without "Activity". p100 Fig. 7 caption glued to "The people are pointing to the bullet marks on the wall." p101 Picket and Mahants entries glued. p102 Fig. 8 caption glued. p103 and p106 "Das" and "Naidu" captions. p105 "Women in the freedom struggle: Ambabai from Karnataka" separate. p106 "### Provincial autonomy". p108 "Patel hailed from ..." caption. p109 "“General”constituencies ..." now a lone line and "Fig. 21 – Khan Abdul Ghaffar Khan ... Also known as Badshah Khan ..." as one sentence.
- Images: p96 viewed. The Source 2 box shows "Pherozeshah is nowadays too busy with his personal work ... They are already rich enough ... Mr. Telang too remains busy. I wonder how if all remain busy in the pursuit of gold can the progress of the country be advanced?" (widely spaced in print, spelt normally). The Repeal entry is the left-margin box and the Activity box is below the Source box. p93, p99, p100, p101, p102, p105, p106, p108, p109 not viewed.
- Verdict: p96 "Pherozeshah is nowadays too busy ... rich enough ..." [M] matches. p96 "Mr. Telang too r em ains busy." [O] extraction fault (one-off), P-spacing (Rule C remnant). p96 "-" line "T e l a n g t o o r em ains busy." is not lost, its words are in the new sentence. p93 bullets [N] not viewed (text looks right). p99, p100, p101, p102, p105, p106, p108, p109 [N] not viewed. Text shows P1 at p99 and p101, P3 at p100, p102, P2 at p106 ("### Provincial autonomy" plus the entry glued to "Peasants, tribals and women participated"), P2 at p109 ("“General”constituencies" apart from the sentence, which is right for 2023 because p109 holds both).
- Fix: override for p96: snapshot "2023-12-23-rationalised", chapter 8, find "Mr. Telang too r em ains busy.", replace "Mr. Telang too remains busy.", note "wide word spacing in the Source 2 box on p96, the print reads remains".

### our-pasts-3 2023-12-23-rationalised, prelims
- Hunk: "Printed on 80 GSM paper with NCERT watermark" now glued to the front of "Published at the Publication Division ...". "` 65.00" now "₹ 65.00". The five "• ..." lines are now "- " list items, "This present edition, is a reformatted version after carrying out the changes given above." is its own sentence, and "Content, which is irrelevant in the present context" is a list item.
- Images: the Rationalisation page (pdf page 5) viewed. It lists the five bullet items and the closing sentence "This present edition, is a reformatted version after carrying out the changes given above."
- Verdict: the bullet list and the closing sentence [M] matches the page. "Printed on 80 GSM paper ..." glued to "Published at ..." and "₹ 65.00" [N] not viewed (pdf page 2 did not open). The "Director New Delhi ... 30 November 2007" line changed in a few characters, not viewed.
- Fix: none.

## 2024-08-04

### our-pasts-3 2024-08-04, all chapters and prelims
- Hunk: the changes in ch1 to ch8 repeat the 2023 list (same layout and same words), with these differences. ch5 p57 "In Jhansi, Rani Lakshmibai joined the rebel sepoys and fought the British along with Tantia Tope, the" now breaks after "the" (not "and"), and the next sentence starts "general of Nana Saheb." (2023 breaks after "and"). ch8 p96 "Mr. Telang too r em ain s busy." (2023 has "r em ains"). ch8 p96 "P h e r o z e s h a h" and "r i c h e n o u g h" are fixed as in 2023. prelims "Printed on 80 GSM paper ... Cover and Layout Arrt Creations Published at the Publication Division ..." glued.
- Images: not viewed for 2024 (no 2024 page was opened, the 2023 images were viewed because the layout is the same).
- Verdict: [N] not viewed for each 2024 page. Hints: the Telang line is the same one-off as 2023 (the page prints "remains"), and the Jhansi break is the same P1 as in 2023, only the break moved.
- Fix: override: snapshot "2024-08-04", chapter 8, find "Mr. Telang too r em ain s busy.", replace "Mr. Telang too remains busy.", note "wide word spacing in the Source 2 box on p96, the print reads remains". P1 for Jhansi (box glued after "and" in 2023 and after "the" in 2024).

## Summary

Counts of verdict tags in this file (an entry with several page verdicts counts once per page verdict): matches the page 28, extraction fault (rule) 18, extraction fault (one-off) 2, not viewed 33. The one-offs are the Telang line spacing (2023 and 2024 share one count) and the 2020 to 2022 cover fragments. Many of the "not viewed" pages are in editions whose layout is identical to a viewed 2019 or 2023 page, so the hints carry over, but they are not verdicts.

Patterns from the earlier review that are now gone: the Activity arrow and square bullet glyphs ("†", "\x86", "¢" and the lone leading space), the backtick rupee sign (now "₹"), letter-spaced words inside body text ("I n t h e B o m b a y", "e d u c a t i o n w h i c h", "a n d o f f i c i a l s", "P h e r o z e s h a h", "r i c h e n o u g h"), "1.In" and "2.Notice", captions swallowed in the middle of a sentence at a page turn, the "More Azad" leak, and run-in headings glued to the next paragraph in 2019 to 2022 ("Revenue for the Company", the five reform-movement headings, "Early years of industrialisation in Japan"). Plain paragraphs are now rejoined over page turns. No lost sentence was found: every "-" line in the change list has its words in the new text (checked by a word-run comparison for every edition), the faults are about where the words sit, not about missing words.

The three remaining patterns that matter most:

1. P1/P2. Margin boxes (Activity boxes and glossary entries) are still emitted inside running sentences and still pull a page-turn sentence apart, or glue a glossary entry to the next paragraph. It touches every edition and about 60 sentences: ch1 p3 (all editions), ch5 p51, p57, p59 (2023, 2024), ch8 p95, p99, p101, ch10 p133, p137, ch11 p146, p148, p149, p157/158, ch12 p164/165 (a regression, the committed text joined it), ch6 p67 "Mir Taqi Mir said, “The ...". The page shows the box in the margin and the sentence running on.
2. P2 inconsistencies between editions. Glossary entries promoted to headings (2014 "Sawar", "Sal", "Dargah", "Rani Channamma criminal court", 2019 to 2024 "Provincial autonomy") and run-in headings glued in some editions and split in others ("Gulamgiri" glued in 2014, 2023, 2024 and split in 2019 to 2022). These create diff hunks that are not edits.
3. P4/P5/P6 list and page-turn structure. Numbered Activity items split at line wraps (ch10 p128, a regression), the p127/128 page-turn sentence not rejoined over a caption (a regression), the bullet list on ch11 p141 and ch9 p109 glued into one sentence, the two-column match exercise on 2014 ch2 p24, and the cover fragments on the 2020 to 2022 prelims. A rule for list-item continuation and a rule for caption-aware page-turn rejoin would clear the rest.
