# Recheck of social-political-life-2 after the rule change

Method: every page named in review/changes-social-political-life-2.txt was mapped to its PDF page through the page markers, and the page image was opened (at 70 to 110 dpi, often two or three pages side by side). Editions that share one print run (2016, 2019, 2020 and the 2023 and 2024 rationalised printings) show the same faults on the same pages, so a pattern is described once in full and later entries refer to it. Rupee-sign lines are listed once per edition. Pages that were not opened say "not viewed".

Short names for the patterns that are still present:

- P1: a blue box, clipping or caption that sits at the foot of a page (or a heading of the next page) is glued into a body sentence that is cut at the page break, or lands on the wrong page.
- P2: speech bubbles of a comic are merged line by line or interleaved, so a sentence is made of pieces of two bubbles.
- P3: labels of a diagram (MEDIA, READERS, VIEWERS, LISTENERS, cotton-boll labels) are glued into exercise lines or caption lists.
- P4: a two-column or list structure is read across (two-column table on ch02 p20, credit rows on the imprint page, reference bullets) and the pieces are glued.
- P5: a sentence is cut at a printed line end or a column end and the cut is kept as a fragment (OCR edition mostly).
- P6: the rupee sign is read as "=", "z", "?" or "%", or the blank after it is dropped (2022 OCR only).
- P7: a heading, box title or box tail is glued to body text on the same line (ch01 p14, ch01 p8 of 2024, "Glossary" on ch08 p101 of 2022).

## 2014-07-28

### social-political-life-2 2014-07-28, chapter 1, printed page 14
- Hunk: "- Challenge of democracy", "- No country can be described ...", "~ Excerpt from Article 15 ... Prohibition of discrimination ..." -> "Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth.", "+ Excerpt from Article 15 of the Indian Constitution Challenge of democracy No country can be described as being completely democratic."
- Images: the blue box title "Excerpt from Article 15 of the Indian Constitution" is the title of the box. "Challenge of democracy" is a heading above the paragraph. The box sentence "Prohibition of discrimination ..." stands alone.
- Verdict: extraction fault (rule). The "~" side now matches the page, the "+" line does not: the box title and the heading are glued to the first body sentence. The lost "-" sentences are in the glued line, so no words are lost.
- Fix: P7. Keep a box title and a heading as their own blocks. Seen on ch01 p14 in 2014, 2016, 2019 and 2020. The 2023 and 2024 printings (p8) are right for the heading, see below.

### social-political-life-2 2014-07-28, chapter 2, printed pages 22 and 23
- Hunk: "+ Thank you Doctor...I feel better already!", "+ Rs 150!", "+ That much! My treatment cost just"
- Images: the comic bubbles read "Thank you Doctor...I feel better already!" and "That much! My treatment cost just Rs 150!" (one bubble).
- Verdict: extraction fault (rule). The first line matches the page. The bubble on p23 is cut into two pieces in the wrong order.
- Fix: P2.

### social-political-life-2 2014-07-28, chapter 6, printed page 77
- Hunk: "~ As citizens of a democracy, ... related" -> "... related Recognising that the media will not be interested ...", "+ Local media"
- Images: the sentence ends at the foot of the page ("issues related") and goes on at the top of p78. The orange box "Local media" sits below it.
- Verdict: extraction fault (rule). "Local media" is now a heading (matches the page). The box paragraph is still glued into the cut sentence.
- Fix: P1. Also 2016 (p77), 2023 (p71) and 2024 (p71) show the same glue.

### social-political-life-2 2014-07-28, chapter 7, printed page 88
- Hunk: "~ They often have to sell their Social advertising Social advertisements refer to advertisements ..." -> "They often have to sell their Social advertisements refer to advertisements made by the State ...", "+ Social advertising"
- Images: the body sentence is cut at the foot of the text column. The box "Social advertising" starts below.
- Verdict: extraction fault (rule). The heading is now separate (matches the page), the box text is still glued to the cut sentence.
- Fix: P1. Same in 2016 p88.

### social-political-life-2 2014-07-28, chapter 8, printed page 103
- Hunk: "- Market Kind of goods sold ... Glossary", "+ Glossary", "+ Market Kind of goods sold Prices of goods Sellers Buyers", "+ Shopping complex"
- Images: a table with the header row (Market, Kind of goods sold, Prices of goods, Sellers, Buyers) and two rows (Weekly market, Shopping complex), then the Glossary box.
- Verdict: matches the page. The header row is one sentence, the Glossary heading is separate. ("Weekly market" is a row label and is not in the change list.) Same in 2016 (p103), 2019 (p91), 2020 (p91). 2019 and 2020 were not opened for this page, 2016 was.

### social-political-life-2 2014-07-28, chapter 9, printed pages 107 and 113
- Hunk: "~ The weavers have no way of 1.This is a merchant's shop in the bazaar." -> "1. This is a merchant's shop in the bazaar.", "+ The weavers have no way of", "~ 7.Spinning mill ..." -> "7. Spinning mill ...", "~ 8.Weavers ..." -> "8. Weavers ..."
- Images: the italic caption 1 to 3 starts "1.This is a merchant's shop" (no space printed). The body sentence "The weavers have no way of" ends the column and goes on over the page.
- Verdict: matches the page. The cut sentence is a fragment, which is the printed break. The inserted space after "1." is cosmetic.
- Fix: none. Same in 2016 (opened p107 and p113), 2019 (p95, p101), 2020, 2023 (p89, p95) and 2024 (p89, p95). Only 2016 was opened for these pages.

### social-political-life-2 2014-07-28, chapter 9, printed page 107 (stray text)
- Hunk: not in the change list, seen on the page: text reads "Putting-out syste Putting-out system– weavers producing cloth at home".
- Images: the caption under the photograph reads only "Putting-out system– weavers producing cloth at home".
- Verdict: extraction fault (one-off). The stray "syste " is a fragment of the outlined caption.
- Fix (2014 file ch09, and 2016 file ch09 line 83 the same):
```
- snapshot: "2014-07-28"
  chapter: 9
  find: "Putting-out syste Putting-out system"
  replace: "Putting-out system"
  note: "stray fragment of the outlined caption on printed page 107"
- snapshot: "2016-09-10"
  chapter: 9
  find: "Putting-out syste Putting-out system"
  replace: "Putting-out system"
  note: "stray fragment of the outlined caption on printed page 107"
```

### social-political-life-2 2014-07-28, chapter 10, printed page 122
- Hunk: 41 "+" lines (the References, one author or title per line)
- Images: the page is the References list with 12 bullets (Dreze ... www.infochangeindia.org). Every new line is a piece of one bullet, and every bullet on the page is present.
- Verdict: matches the page (the source gap of the earlier review, pattern C, is gone for 2014). The pieces are split at the full stops inside the bullets.

## 2016-09-10

### social-political-life-2 2016-09-10, chapter 1, printed page 14
- Same as 2014 (not opened, text identical). Verdict: not viewed. Pattern P7.

### social-political-life-2 2016-09-10, chapter 2, printed page 21
- Hunk: "~ Read the story given above ... What would you say to" -> "... What would you say to Hakim Sheik?"
- Images: the box ends "What would you say to Hakim Sheik?" in the 2015-16 print.
- Verdict: matches the page (the old cut is gone).

### social-political-life-2 2016-09-10, chapter 2, printed page 22
- Hunk: "~ I had viral fever and school on Monday. My Daddy had to go to the took me to see the doctor hospital..." -> "school on Monday. My Daddy had to go to the took me to see the doctor hospital...", "~ THE COST OF A CURE Aman and Ranjan ..." -> "Aman and Ranjan ...", "+ I had viral fever and", "+ THE COST OF A CURE", "+ Thank you Doctor...I feel better already!", "+ p23: Rs 150!", "+ p23: That much! My treatment cost just"
- Images: "THE COST OF A CURE" is the title. "Aman and Ranjan are good friends ..." is the strapline. Two bubbles on the right panel read "I had viral fever and had to go to the hospital..." and "Oh! Me, too! I just got back to school on Monday. My Daddy took me to see the doctor at the new hospital in Kingsway."
- Verdict: title and strapline match the page. The bubbles are extraction fault (rule): the lines of two bubbles are merged ("had to go to the took me to see the doctor hospital...").
- Fix: P2. Same on 2019 p22, 2020 p22 (opened 2019 and 2020), and 2022 p22.

### social-political-life-2 2016-09-10, chapter 2, printed page 25
- Hunk: "~ (PHCs) or hospitals near your place. From your experience ... find out the facilities provided and people" -> "... and people who run the centre."
- Images: the blue box reads "List some Primary Health Centres (PHCs) or hospitals near your place. From your experience (or by visiting any one of them), find out the facilities provided and people who run the centre."
- Verdict: matches the page for the "~" sentence. The box is still cut after "List some Primary Health Centres" (a fragment). Pattern P5.

### social-political-life-2 2016-09-10, chapter 3, printed page 31
- Hunk: three "-" lines of the comic, nine "+" lines (bubbles).
- Images: bubbles read "What a loud voice he has...he must be a leader or something...", "...and we demand that the authorities take immediate action to bring the public health situation under control! Our MLA must take the responsibility for this!", "Shh...I saw him on TV too. He is a member of the Opposition!", "Ha ha - they seem more angry about what he hasn't done!", "Really! Why? Has he done something?".
- Verdict: extraction fault (rule). The words are all present and the three lost "-" lines are redistributed. The pieces are still wrongly combined: "What a loud voice he has...he must be the Opposition!" (the first bubble with the end of the last) and "He is a member of the responsibility for this!" (two bubbles).
- Fix: P2. Same in 2019, 2020 (opened), 2023 (p25) and 2024 (p25).

### social-political-life-2 2016-09-10, chapter 3, printed page 31 (map caption)
- Hunk: not in the list, seen in text: "They then become members of the legislative assembly and also form the The state of Himachal Pradesh is coloured in green in the above thumbnail map of India."
- Images: the page has no caption. The caption belongs to the map on p32. The sentence is cut at the foot of p31.
- Verdict: extraction fault (rule). The caption of the next page is glued into the cut sentence.
- Fix: P1. Same in 2022 (p31), 2023 (p25) and 2024.

### social-political-life-2 2016-09-10, chapter 6, printed page 77 and chapter 7, printed page 88
- Same as 2014. Opened both. Verdict: extraction fault (rule), P1 (glue of the box into the cut sentence). The headings "Local media" and "Social advertising" are correct.

### social-political-life-2 2016-09-10, chapter 8, printed page 103 and chapter 9 printed pages 107 and 113
- Opened. Verdict: matches the page (same notes as 2014).

### social-political-life-2 2016-09-10, chapter 10, printed pages 120 and 122
- Hunk: "~ Can you share with your class a local song or a poem on dignity" -> "... that is from your area?", "~ Poster Women: A Visual History of the Women's Movement" -> "... in India.", "- in India."
- Images: both lines are complete on the page.
- Verdict: matches the page. The earlier cut is gone.

## 2019-05-04

### social-political-life-2 2019-05-04, chapter 2, printed pages 22 and 23
- Hunk: "~ Oh! Me, too! I just got back to had to go to the school on Monday. My Daddy hospital..." -> "had to go to the school on Monday. My Daddy hospital...", "+ Oh! Me, too! I just got back to", "~ once before bed time ... it's tasty" -> "... Thank you Doctor...I feel better already!", "+ Oh! My treatment did not cost much!"
- Images: p22 bubbles as in 2016. p23 bottom right reads "My hospital was nice, but they gave me many medicines and the whole thing cost quite a lot!" and "Oh! My treatment did not cost much!"
- Verdict: p23 matches the page. p22 is extraction fault (rule) P2 (two bubbles merged, and "Thank you Doctor..." is glued to the syrup bubble).

### social-political-life-2 2019-05-04, chapter 3, printed page 41
- Hunk: "~ Majority: ... supports a decision or an idea." -> "... or an", "+ idea."
- Images: the glossary entry reads "Majority: This is a situation when more than half the number in a group supports a decision or an idea. This is also called a simple majority." on two lines.
- Verdict: extraction fault (rule). The sentence is cut at the line end (pattern P5). Same in 2020 p41, 2023 p35 and 2024 p35 (2023 opened).
- Fix: join lines of a glossary entry into one sentence.

### social-political-life-2 2019-05-04, chapter 6, printed page 73
- Hunk: "~ ... from ` 1,000 to ` 1,00,000 ..." -> "from ₹ 1,000 to ₹ 1,00,000"
- Verdict: not viewed (the rupee sign is a glyph, the text reads the same on p98 which was opened and shows the sign as "₹"). Same for 2020 p73, 2023 p67.

### social-political-life-2 2019-05-04, chapter 6, printed page 79
- Hunk: "~ 2. Can you give this diagram a title? What do you understand ..." -> "What do you understand ...", "~ 4. As a class project ..." -> same, "~ 5. Do projects ..." -> "Create commercial ...", "- Compare two newspapers ... MEDIA a. What information i...", "~ EXERCISES cs" -> "EXERCISES", "~ VIEWERS, LISTENERS b. ..." -> "What information is it leaving out?", "- d. Whose point of view is being left out and why?", "- the agenda'. ... Provide two examples ...", 10 "+" fragments.
- Images: the exercise list 1 to 5 with sub-items a to d beside a diagram with the labels BIG BUSINESS HOUSES, MEDIA, READERS, VIEWERS, LISTENERS and the arrow captions.
- Verdict: extraction fault (rule) for the glue of diagram labels: "It might help to ask the following questions- MEDIA a. What information is this article providing?" and "READERS," as a separate line. "EXERCISES cs" is fixed (one-off gone). The rest matches the page: the lost "-" sentences are present in the new text ("Compare two newspapers ...", "d. Whose point of view is being left out and why?" appears whole in the text and the "+ d." line is only a split of the same words).
- Fix: P3. Same in 2020 (opened p79), 2022 (p79) and 2024 (p73, "READERS," and "MEDIA a." still present).

### social-political-life-2 2019-05-04, chapter 7, printed pages 85, 86 and 91, chapter 8, printed pages 93 to 96, 99 and 101
- Hunk: backtick -> "₹" in 24 sentences, "7.Spinning" -> "7. Spinning", "+ The weavers have no way of" (p95), market table (p91).
- Verdict: p98 opened and shows "₹ 3,000", "₹ 1.50 (per piece)", "₹ 2,000", "₹ 1,500", "₹ ______ per shirt", "₹ 900", "₹ 1,800", "₹ 300", "₹ 100". All p98 lines match the page. The other pages are not viewed. The p91 table matches as for 2014 (not viewed here).

### social-political-life-2 2019-05-04, chapter 9, printed page 110
- Hunk: "- India.", "~ Poster Women ... in" -> "... in India.", "- World Health Organization, Essential medicines and health products,", "- http://www.who.int/medicines/services/inn/en/", "- www.cehat.org/rthc/policybrieffinal.pdf www.in.undp.org (Sustainable Development Goals - SDGs)", "+ World Health Organization, Essential medicines and health products, http://www.who.int/medicines/services/inn/en/ www.cehat.org/rthc/policybrieffinal.pdf www.in..."
- Images: the References list. "World Health Organization ..." (with its URL), "www.cehat.org/rthc/policybrieffinal.pdf", "www.in.undp.org (Sustainable Development Goals - SDGs)" and "www.infochangeindia.org" are four separate bullets. "Medical Council of India, ..." and "Parks, Rosa. 2000. ..." are two bullets too.
- Verdict: extraction fault (rule). The "Poster Women ... in India." line is fixed. Reference bullets are glued when an earlier bullet wraps to a second line.
- Fix: P4. Same in 2020 p110, 2023 p96 (opened). The 2023 text also glues "Medical Council of India ... Parks, Rosa".

### social-political-life-2 2019-05-04, prelims (imprint page, PDF page 2, and the Ansaris page)
- Hunk: many OCR-garbage "-" lines of the Preamble, "~ INSTITUTI INDIA" -> "THE C NSTITUTI INDIA", "+ Head, Publication: M. Siraj Anwar Division", "+ Chief Business: Gautam Ganguly Manager", "+ Chief Production: Arun Chitkara Officer", "+ Orijit Sen with Splash!", "+ Communications", "+ Cover, Layout", "+ Printed on 80 GSM paper with NCERT watermark", "+ If you were one of the Ansaris how would you have responded", "+ to the property dealer's suggestion that you change", "+ your name?", "~ ` 60.00" -> "₹ 60.00", "~ Advertising ` 400" and the other shirt labels -> "₹".
- Images: the imprint shows "Head, Publication Division : M. Siraj Anwar", "Chief Business Manager : Gautam Ganguly", "Chief Production Officer : Arun Chitkara", "Orijit Sen with Splash! Communications", "₹ 60.00". The Preamble page is a raster picture with a clear text. The page xii shows the diagram and the shirt with "₹ 900", "₹ 400", "₹ 200", "₹ 300".
- Verdict: the price, the shirt labels and "Printed on 80 GSM paper with NCERT watermark" match the page. The credits are extraction fault (rule) P4: the second line of a label ("Division", "Manager", "Officer") is glued behind the name. The Ansaris question is cut into three line fragments (P5). The Preamble OCR text ("WE. solemnly resolved to constitute India into OVEREIGN CIALIST SECULAR DEM CRATIC REPUBLIC ... cial, ec mic ...") does not match the page and is extraction fault (rule): the page is a decorated picture and the OCR drops letters at the border.
- Fix: P4 for the credits. For the Preamble use the printed text of the page (a hand correction of the whole block, as it is the same in every edition) or leave it out of the sentence counts. Same in 2020, 2022, 2023 and 2024 (2024 opened the imprint and the rationalisation page).

## 2020-05-08

### social-political-life-2 2020-05-08, chapters 1 to 3, 6 to 9 and prelims
- The same sentences changed as in 2019 and the PDFs have the same layout (opened ch02 p22, ch03 p31, ch06 p79, ch08 p98).
- Verdicts: as in 2019. ch01 p14 P7, ch02 p22 P2, ch03 p31 P2, ch06 p79 "EXERCISES cS" is fixed and the diagram labels remain P3, ch08 p98 the rupee sign matches the page, ch09 p110 P4, prelims credits P4 ("Head, Publication: Anup Kumar Rajput Division", "Chief Business: Bibash Kumar Das Manager"). The prelims "Some own radio, TV, newspaper" and "People buy products seen in the media ... advertise their products" were glued before and are now caption lines, which matches the diagram on p79 (pages not opened for the prelims copy).
- Not viewed: ch07 p85, p86, p91, ch08 p93 to 96, 99 and 101 (rupee lines), ch06 p73.

## 2022-08-02-ocr

### social-political-life-2 2022-08-02-ocr, chapter 1, printed pages 13 and 15
- Hunk: "~ Rosa Parks ... American history with one defiant act." -> "... American history", "+ history with one defiant act.", glossary lines split in the same way.
- Images: not opened. Verdict: not viewed. The words are all present and the cut is at a line end (P5).

### social-political-life-2 2022-08-02-ocr, chapter 2, printed page 20
- Hunk: "- India is the third largest producer of Half of all children in India do not medicines in the world ...", "- exporter of medicines. undernourished.", "+ India is the third largest producer of Half of all children in India do not medicines in the world and is also a large get adequate food to eat and are exporter...", "+ In order to prevent and treat illnesses ..."
- Images: a two-column table whose left and right cells each read as separate sentences ("India is the third largest producer of medicines in the world and is also a large exporter of medicines." and "Half of all children in India do not get adequate food to eat and are undernourished.").
- Verdict: extraction fault (rule). The line-by-line read of a two-column table interleaves the two cells. All words are present and no sentence is lost, but none is intact. Also "2I per cent" for "21 per cent" in the same table (one-off, see below).
- Fix: P4.
```
- snapshot: "2022-08-02-ocr"
  chapter: 2
  find: "2I per cent"
  replace: "21 per cent"
  note: "OCR misread on printed page 20, the page prints 21 per cent"
```

### social-political-life-2 2022-08-02-ocr, chapter 2, printed page 21
- Hunk: "~ He was in a very serious condition and needed immediate He was taken to a government hospital ..." -> "He was taken ...", "~ ... he accidentally fell off a running train ..." -> "... a running", "+ He was in a very serious condition and needed immediate", "+ train and suffered head injuries."
- Images: the box reads "... fell off a running train and suffered head injuries. He was in a very serious condition and needed immediate treatment." The last word "treatment." is on a line of its own.
- Verdict: extraction fault (rule). Words are present, but the sentence is cut into three pieces, and "treatment." is a separate caption block. P5. The caption "government hospitals, ike this one." is a one-off misread of "like".
```
- snapshot: "2022-08-02-ocr"
  chapter: 2
  find: "government hospitals, ike this one."
  replace: "government hospitals, like this one."
  note: "OCR dropped the l on printed page 21"
```

### social-political-life-2 2022-08-02-ocr, chapter 2, printed page 22
- Hunk: nine "-" lines (the comic's sentences), six "+" lines.
- Images: the comic of the 2022 print. Bubbles read "I had viral fever and had to go to the hospital...", "Hi Aman! Good to see you back! How have you been?", "The building looked so posh ... with the best of facilities." and so on.
- Verdict: extraction fault (rule) P2 for the interleaved narration boxes ("Daddy said that was because it was a private hospital, with the Daddy had to pay Rs 500 ..." is two caption boxes merged) and for "While Ranjan os Bi Aman!" ("os Bi" is the OCR of the bubble "Hi Aman!" inside the strapline). The words are all present. The title is a one-off misread:
```
- snapshot: "2022-08-02-ocr"
  chapter: 2
  find: "THE COST OFA CURE"
  replace: "THE COST OF A CURE"
  note: "OCR joined OF A on printed page 22"
- snapshot: "2022-08-02-ocr"
  chapter: 2
  find: "| had viral fever and had to go to the hospital..."
  replace: "I had viral fever and had to go to the hospital..."
  note: "OCR read I as a bar on printed page 22"
```

### social-political-life-2 2022-08-02-ocr, chapter 2, printed page 24
- Hunk: "- From the above story ... in two categories -", "- Public health services The public health service ...", "+ From the above story ... two categories - The public health service is a chain ...", "+ Public health services"
- Images: the text reads "From the above story, you must have understood that we can roughly divide up various health care facilities in two categories -", then the list "(a) Public health services and", "(b) Private health facilities.", then the heading "Public health services", then the paragraph.
- Verdict: extraction fault (rule). The list items (a) and (b) are moved to a later line ("(a) Public health services and (b) Private health facilities. Public health services") and the intro sentence is glued to the paragraph. No words are lost.
- Fix: P1 (the two list lines and the heading are page-level blocks, keep them in reading order).

### social-political-life-2 2022-08-02-ocr, chapter 2, printed pages 26, 27 and 29
- Hunk: "~ | Daam kam, Dawai Uttam 'ep Jan Aushadhi Medical Stores is a chain ..." (p26), "+ illness." (p27), glossary lines (p29).
- Images: p26 has a photograph of a Jan Aushadhi poster. The text inside the poster is read as body text. p27 starts "illness. Hence, even for those ...", which ends the sentence "In fact, barely 20 per cent of the population can afford all the medicines they require during an illness." from p26. p29 Glossary: "Communicable diseases: ... in many ways such as through water, food, air, etc." and "OPD: This is the short form for 'Out Patient Department'."
- Verdict: p29 matches the page (the earlier glue is gone, "Glossary" is its own line). p27 "illness." is a page-break fragment (P5). p26 is an extraction fault (rule) for the text inside a picture (the poster), which is read as body text (pattern I of the earlier review).
- Fix: P5 and drop OCR lines whose box lies inside a picture.

### social-political-life-2 2022-08-02-ocr, chapter 3, printed pages 31 and 32
- Hunk: "~ They then become members of the legislative assembly and also form the Discuss the following terms with your teacher ..." -> "... They then become members of the legislative assembly and also form the The state of Himachal Pradesh is coloured in purplein theabove thumbnail map of India." (p31), "~ What action do you think can be taken ... Discuss.", "- Can you explain the following terms-majority, ruling party, opposition with reference to your The state of Himachal Pradesh is coloured in purplein theabove thumbnail map of India." (p32), "+ Can you explain the following terms-majority, ruling party, opposition with reference to your"
- Images: p31 ends "... and also form the" and has no map. The caption "The state of Himachal Pradesh is coloured in purple in the above thumbnail map of India." sits under the map on p32.
- Verdict: p32 matches the page (the caption is no longer glued to the blue question). p31 is extraction fault (rule) P1 (the caption of the next page is glued into the cut sentence, with a one-off misread "purplein theabove"). Blue question "What action ... Discuss." matches the page.
```
- snapshot: "2022-08-02-ocr"
  chapter: 3
  find: "coloured in purplein theabove thumbnail map"
  replace: "coloured in purple in the above thumbnail map"
  note: "OCR lost the spaces in the map caption (printed page 32)"
```

### social-political-life-2 2022-08-02-ocr, chapter 3, printed pages 36 and 37
- Hunk: "~ The government announced a compensation for these Government smells the garbage Chief Minister promises funds for work f..." (p36) -> "... for work families.", "~ The minister said that they families." -> "The minister said that they", "+ intend to supply drinking water to every village through tanker trucks."
- Images: p36 ends "The government announced a compensation for these" (and "families." is the first line of p37). The newspaper clipping "Government smells the garbage / Chief Minister promises funds for work" and its two columns are on p37. The column break reads "The minister said that they" and "intend to supply drinking water to every village ...".
- Verdict: p37 matches the page. The p36 sentence is extraction fault (rule): the headline of p37's clipping is glued into the cut sentence (P1). The clipping column break is kept as a fragment, which matches the printed break (P5).

### social-political-life-2 2022-08-02-ocr, chapter 4, printed pages 47 to 51
- Hunk: p47 "- At the Singh's house dimen Jaspreet, why don't What fun!", "- 'MY MOTHER", "~ Besides, Mangala has also money for that!" -> "Besides, Mangala has also", "~ I'll ask Harmeet to switch Oh God!" -> "I'll ask Harmeet to switch", "+ 'MY MOTHER dimen Jaspreet, why don't What fun!", "+ money for that!" (p48), p49 "~ Tasks like washing clothes ..." -> "washing clothes ...", "+ Tasks like on a Strike for a day?", p50 "- This is often referred to as the double burden of", p51 "~ This naturally has an impact on whether Children at an Anganwadi centre in a girls can attend school."
- Images: p47 comic. The last bubble reads "How would I know? I'm on strike, remember? Besides, Mangala has also taken leave today." p48 has "Ma already gave us money for that!" and "I'll give you some money. Just buy something from the canteen today..." in other bubbles. p49 ends "Tasks like" and the blue question ends "... on a strike for a day?". p50 has the italic caption "Many women like Shonali's mother ... This is often referred to as the double burden of women's work." beside the table. p51 begins "This naturally has an impact on whether girls can attend school." and has a photo caption "Children at an Anganwadi centre in a village in Madhya Pradesh."
- Verdict: p47 and p48 are extraction fault (one-off and rule). The words "taken leave today." and "How would I know? I'm on strike, remember?" are lost (in no line of the new text), which is the most serious finding of this review. The rest is P2. p49 and p50 are extraction fault (rule) P1: the exercise line is glued to the cut body sentence, and the caption sentence of p50 is merged with p51's lines and the photo caption. The photo caption misreads "Madhya" as "Madlrya".
- Fix, ready to paste (the first restores the lost words):
```
- snapshot: "2022-08-02-ocr"
  chapter: 4
  find: "Besides, Mangala has also"
  replace: "Besides, Mangala has also taken leave today."
  note: "OCR lost the end of the last bubble on printed page 47 (the page reads taken leave today.)"
- snapshot: "2022-08-02-ocr"
  chapter: 4
  find: "Madlrya Pradesh"
  replace: "Madhya Pradesh"
  note: "OCR misread the photo caption on printed page 51"
```

### social-political-life-2 2022-08-02-ocr, chapter 5, printed pages 57 and 58
- Hunk: p57 "~ Even in school, Laxmi helped ..." -> "Laxmi helped ...", "- Laxmi's parents are not literate but they struggled and overcame ...", "+ Laxmi's parents are not literate but they struggled and", "+ education.", "+ overcame many hardships to make sure their children got an", p57 "~ Laxmi has had to do this several times ..." -> "to do this several times ...", p58 "~ 7} You have to get a good job!", "- It has no scope! __all Be sensible, son.", "~ It is important to understand that we live in a Read the story below and answer society ..." -> "Laxmi has had Read the story below ...", "+ Why do you want to take History? Think about your future. 7}", "+ Be sensible, son.", "+ It has no scope! __all"
- Images: the green box on p57 reads "Laxmi's parents are not literate but they struggled and overcame many hardships to make sure their children got an education." The last line of the box is "Laxmi has had to do this several times in her life ..." The comic bubbles on p58 read "Why do you want to take History? Think about your future. You have to get a good job! History will not help. It has no scope!" and "Be sensible, son. Take Maths, and you can study computers side by side. The job market for computers is very good."
- Verdict: p57 is extraction fault (rule). The box sentence is cut into three line pieces. "Laxmi has had" is glued with the blue question of p58 (P1). p58 is P2 plus a stray symbol "7}" and "__all", which are OCR noise from the speech bubble (one-off).
```
- snapshot: "2022-08-02-ocr"
  chapter: 5
  find: "Think about your future. 7}"
  replace: "Think about your future."
  note: "stray OCR symbol from a speech bubble on printed page 58"
- snapshot: "2022-08-02-ocr"
  chapter: 5
  find: "It has no scope! __all"
  replace: "It has no scope!"
  note: "stray OCR symbol from a speech bubble on printed page 58"
```

### social-political-life-2 2022-08-02-ocr, chapter 5, printed pages 62, 64, 66 and 67
- Hunk: p62 "+ If a school", p64 "+ dowry.", "~ Eventually, this became a public issue ...", p66 "- Below: On & March ...", "+ Below: On & March, International Women's Day, women all over", "+ the world come together to celebrate and renew their struggles.", "+ cultural programme.", p67 "+ Glossary", "+ Violation: ...", "+ Sexual harassment: ..."
- Images: p62 ends "If a school" (continues on p63). p64 ends "... punish families who seek dowry." p66 captions read "Below: On 8 March, International Women's Day, women all over the world come together to celebrate and renew their struggles." and "... gather at Wagah on the border of India and Pakistan and hold a cultural programme." p67 glossary as printed.
- Verdict: p67 matches the page (the glossary is clean). p62 is the printed break (P5, matches the page). p64 and p66 are line-end fragments (P5) with two one-off misreads: "Satyarant" for "Satyarani" (caption on p64) and "On & March" for "On 8 March".
```
- snapshot: "2022-08-02-ocr"
  chapter: 5
  find: "Below: On & March"
  replace: "Below: On 8 March"
  note: "OCR misread 8 on printed page 66"
- snapshot: "2022-08-02-ocr"
  chapter: 5
  find: "Satyarant, an active member"
  replace: "Satyarani, an active member"
  note: "OCR misread the name in the photo caption on printed page 64"
```

### social-political-life-2 2022-08-02-ocr, chapter 6, printed pages 72 and 74
- Hunk: p72 "- With electronic typerwriters, journalism underwent a sea-change in the 1940s.", "+ With electronic typerwriters, journalism", "+ underwent a sea-change in the 1940s.", "+ the Royal Institute, his invention, the", p74 "- Although the government did take this decision rather hastily ...", "+ decision rather hastily, the protestors have known for quite some time that their", "+ units are not legal.", "+ protesting.", "+ € government Says", "+ lost if the factories close ..."
- Images: p72 captions (the first reads "With electronic typerwriters, journalism underwent a sea-change in the 1940s." as printed). p74 has two clippings in columns and the text "...the government says..." in a quotation.
- Verdict: p72 is extraction fault (rule) P5 (the captions are cut at line ends, all words present). p74 is extraction fault (rule) P5 for the clipping columns (the sentences run over the two columns and are not joined), and one-off for "€ government Says" (the page reads "The government says").
```
- snapshot: "2022-08-02-ocr"
  chapter: 6
  find: "€ government Says"
  replace: "The government says"
  note: "OCR misread the clipping text on printed page 74"
```

### social-political-life-2 2022-08-02-ocr, chapter 6, printed pages 77 and 78
- Hunk: p77 "- As citizens of a democracy ... related Recognising ...", "+ As citizens of a democracy ... related Social advertising Social advertisements refer to advertisements made by the Government or private agencies ... crossing of manned /unmanned level crossings.", "+ Recognising that the media will not be interested ..." p78 "- Social advertisements refer ...", "- Social advertising", "- a@) SEEONBOTHTHESIDES ...", "+ a@) SEEONBOTHTHESIDES 45) LISTEN CAREFULLY ... brotha dade", "+ o [Passengers|complaint SS eise Helpline Noms at"
- Images: p77 has the body, the box "Local media" and ends with the cut sentence. The orange box "Social advertising" is on p78, beside a photograph of a railway poster. The poster text is part of a picture.
- Verdict: extraction fault (rule). The p78 box text is now filed on p77 and glued into the cut sentence (P1). The poster text ("SEEONBOTHTHESIDES ...") is OCR noise from inside a picture and remains.
- Fix: P1 and drop OCR lines inside pictures.

### social-political-life-2 2022-08-02-ocr, chapter 6, printed pages 79 and 81
- Hunk: glossary and exercise lines split in pieces ("+ magazines and books for a wide audience to read.", "+ showing certain stories.", "+ ways in which this is done.", "+ save water and energy.", "+ a."), p81 "~ ... the chain" -> "... of markets involved in the process."
- Images: exercise 4 with a. to d., 5, glossary as in 2020. p81 is the Teacher's note in two columns.
- Verdict: p79 matches the page words. Line-end fragments (P5) and the diagram labels are not glued here (the diagram text of p79 is read as separate lines). p81 matches the page (the clipped column is the printed break).

### social-political-life-2 2022-08-02-ocr, chapter 7, printed pages 82, 84, 85 and 91
- Hunk: p82 "- If we make a list ...", "- There are many kinds of markets ...", "~ In this chapter ..." (all cut at line ends), p84 "- Give three reasons.", "~ Why do people go to a weekly market?" -> "... Give three reasons.", "+ We may buy milk from the dairy ... other", "+ Sujata and Kavita were sent to buy SS ive | a 12 Lee groceries from their neighbourhood" (p85), p91 glossary and exercise lines.
- Images: p82 is the chapter opener paragraph, p84 the blue questions and "Shops in the neighbourhood", p85 not opened, p91 the exercises and glossary.
- Verdict: p84 blue question matches the page. p82 and p91 match the page words and are extraction fault (rule) P5 (every line end is a sentence end). p85 is not viewed, but the text "Sujata and Kavita were sent to buy SS ive | a 12 Lee groceries" contains picture noise (not viewed, flagged), and "% 3000" reads a rupee sign badly (P6).
```
- snapshot: "2022-08-02-ocr"
  chapter: 7
  find: "the amount of % 3000"
  replace: "the amount of ₹ 3000"
  note: "OCR read the rupee sign as % on printed page 85, confirm on the image"
```
(The override above is a guess from the pattern, so check page 85 before pasting.)

### social-political-life-2 2022-08-02-ocr, chapter 8, printed pages 92, 93 and 95
- Hunk: p92 "- It begins with the production of cotton and ends | with the sale of the shirt.", "+ It begins with the with the sale of the shirt.", "+ production of cotton and ends |", p93 "~ 6. Spinning be Spinnin P & mill sells ... % Trader: Amma, I am giving you a good price ...", "~ Swapna: ¥ 3,000 only!" -> "₹ 3,000 only!", "- Trader: Amma, I am giving you a good price." (p94), p95 "+ A variety of sarees, towels,", "+ powerlooms on which the yarn is woven into cloth." ...
- Images: p92 reads "It begins with the production of cotton and ends with the sale of the shirt." in the intro paragraph. p93 shows the story, the diagram with the labels 1. to 6. and the speech lines. "Trader: Amma, I am giving you a good price" is not on p93 (it is on p94). p95 has the italic caption 1 to 3 beside the photographs.
- Verdict: p92 is extraction fault (rule). The words "production of cotton and ends" are cut out of the sentence and made into a bogus heading. p93 matches the page for "Swapna: ₹ 3,000 only!". The rest of p93 is extraction fault (rule) P3: the cotton-boll labels are scrambled ("4. Spinning mill buys the v7") and a speech line of p94 is glued onto the label list on the wrong page. p95 is P5 and P3 (blue questions glued into the body lines: "What are the following people However, this dependence ...").
- Fix: P3 and P5. A heading must not be made from the middle of a body sentence.

### social-political-life-2 2022-08-02-ocr, chapter 8, printed pages 96, 97 and 98
- Hunk: "~ Each loom costs ~ 20,000 ..." -> "₹ 20,000" (p96), "~ Women workers sewing buttons in a" -> "...in a" (p97), "~ He then spent ? for advertising in the media, and another ? per shirt ...", "- The businessperson purchased the shirts from the garment exporter in Delhi for per shirt.", "~ The cloth and other raw materials cost him ~ 100 per shirt." -> "₹ 100", "~ The highest paid ... ~ 3,000" -> "₹ 3,000", "~ Thus, the cost to this person is ¥ 900 while he sells the shirt for = 1,800. z is his profit on one shirt!" -> "₹ 900 ... = 1,800. z is ..."
- Images: p98 (opened) prints "₹ 3,000", "₹ ______ per shirt", "₹ ______ for advertising", "₹ 900", "₹ 1,800", "₹ ______ is his profit", "₹ 300", "₹ 100", "₹ 25".
- Verdict: the "~" sentences that now read "₹" match the page. Still wrong, extraction fault (rule) P6: "for = 1,800. z is his profit", "sold the shirt at = 300 per piece", "He then spent ? for advertising ... another ? per shirt", "for per shirt" (the blank is lost) and on p99 "came to = 25 per shirt", on p88 not viewed. p96 and p97 not viewed.
- Fix: map "=", "z", "?" and "~" before a figure or a blank to "₹" in 2022. One-off overrides for p98 and p99:
```
- snapshot: "2022-08-02-ocr"
  chapter: 8
  find: "he sells the shirt for = 1,800. z is his profit"
  replace: "he sells the shirt for ₹ 1,800. ₹ __________ is his profit"
  note: "rupee sign read as = and z on printed page 98"
- snapshot: "2022-08-02-ocr"
  chapter: 8
  find: "sold the shirt at = 300 per"
  replace: "sold the shirt at ₹ 300 per"
  note: "rupee sign read as = on printed page 98"
- snapshot: "2022-08-02-ocr"
  chapter: 8
  find: "He then spent ? for advertising in the media, and another ? per shirt"
  replace: "He then spent ₹ _______ for advertising in the media, and another ₹ _______ per shirt"
  note: "rupee sign and blanks read as ? on printed page 98"
- snapshot: "2022-08-02-ocr"
  chapter: 8
  find: "came to = 25 per shirt"
  replace: "came to ₹ 25 per shirt"
  note: "rupee sign read as = on printed page 99"
- snapshot: "2022-08-02-ocr"
  chapter: 8
  find: "although Swapna knows that cotton will sell for at least = 1,800"
  replace: "Though Swapna knows that cotton will sell for at least ₹ 1,800"
  note: "rupee sign read as = on printed page 94, confirm on the image"
```
(The last override was not checked on page 94. Fix its find string to the exact Markdown text "Though Swapna knows that cotton will sell for at least = 1,800 per quintal" before pasting.)

### social-political-life-2 2022-08-02-ocr, chapter 8, printed pages 99 and 101
- Hunk: p99 "~ On the other hand, it is usually the rich and the powerful Did you know that ..." -> "Did you know ...", "+ On the other hand, it is usually the rich and the powerful", p101 "- Glossary", "~ If the costs are more than the earnings, it would lead to a loss." -> "Glossary more than the earnings, it would lead to a loss.", "~ The cotton is pressed into bales ..." -> "bales to be sent for spinning into thread."
- Images: p99 ends with the cut sentence "On the other hand, it is usually the rich and the powerful". p101 has the glossary: "Profit: The amount that is left ... If the costs are more than the earnings, it would lead to a loss."
- Verdict: p99 matches the page (the cut is the printed break). p101 is extraction fault (rule) P7: the heading "Glossary" is glued to the tail of the last entry and the entries are cut at line ends.

### social-political-life-2 2022-08-02-ocr, chapter 9, printed pages 104 and 108
- Hunk: p104 "~ is often considered of less value than that done by the men." -> "www.in.undp.org is often considered ...", p108 "- The Indian Constitution as a living document The foundation of ...", "- Why for centuries they have been breaking Why don't they ever come true ...", "+ While some join protest movements ...", "+ Why from village to village they walk on their own"
- Images: p104 has the SDG photograph with the caption "Sustainable Development Goal (SDG) www.in.undp.org" at the left, and the body starts "is often considered of less value ...". p108 has the song and the blue box "Creative expression against inequality".
- Verdict: p104 is extraction fault (rule) P1 (the caption line is glued to the first body line of the page). p108 matches the page words. The box paragraph is separate (the earlier glue with the heading is gone). The song lines are one run-on sentence, and one line ("Why from village to village they walk on their own") is moved to the end, which is an ordering fault (rule) P5.

### social-political-life-2 2022-08-02-ocr, prelims
- Hunk: as for 2019 with the 2022 imprint ("Head, Publication: Anup Kumar Rajput Division Chief Editor: Shveta Uppal", "Chief Business: Vipin Dewan Manager"), "~ ` 65.00" -> "₹ 65.00", "~ INSTITUTI INDIA" -> "THE C NSTITUTI INDIA".
- Verdict: not viewed (the 2022 imprint page was not opened). The Preamble remains misread (see 2019).

## 2023-12-23-rationalised

### social-political-life-2 2023-12-23-rationalised, chapter 1, printed page 8
- Hunk: "~ Excerpt from Article 15 ... Prohibition of discrimination ..." -> "Prohibition of discrimination ...", "+ Excerpt from Article 15 of the Indian Constitution"
- Images: the page shows the heading "Challenge of democracy" and the paragraph, then the box with the title and the sentence "Prohibition of discrimination ...".
- Verdict: matches the page. The title is its own block.

### social-political-life-2 2023-12-23-rationalised, chapter 2, printed pages 16, 17 and 19
- Hunk: p16 "~ ... it's tasty" -> "... Thank you Doctor...", "+ better already!", p17 "+ Oh! My treatment did not cost much!", p19 "~ From your experience ... find out the facilities provided and people" -> "... who run the centre."
- Images: p19 opened, matches. p16 and p17 not opened.
- Verdict: p19 matches the page. p16 and p17 not viewed (same comic as 2019, P2).

### social-political-life-2 2023-12-23-rationalised, chapter 3, printed pages 25 and 35
- Hunk: p25 as the 2016 comic, p35 "- 5. What is the difference between the work that MLAs do ... Constituency: A particular area ...", "+ 5. What is the difference ... departments?", "+ Constituency: ...", "~ Majority: ..." -> "... or an", "+ idea."
- Images: p35 opened: the exercises 1 to 5, the table and the glossary.
- Verdict: p35 matches the page for exercise 5 and "Constituency" (the earlier glue is gone). "Majority" is cut at the line end (P5). p25 is extraction fault (rule) P2 and P1 (the map caption is glued into the cut sentence).

### social-political-life-2 2023-12-23-rationalised, chapter 4, printed page 47
- Hunk: "~ Give one example of each based on the household tasks d." -> "... tasks", "~ Support your answer with the use of an example - a." -> "... example -", "- The work that women do is less valued than that of men.", "~ Typically, a person can have several identities." -> "several", "+ a.", "+ d.", "+ identities.", "+ valued than that of men."
- Images: the exercise list 1 to 4 and the blue statements a to d. The glossary says "Identity: Identity is a sense of self-awareness ... Typically, a person can have several identities."
- Verdict: the exercise sentences now match the page (the stray letters are no longer glued). The blue statement d and the glossary sentence are cut at the line end (P5), and the letters "a." and "d." stand apart from their statements. All words are present.

### social-political-life-2 2023-12-23-rationalised, chapter 5, printed page 61
- Hunk: "~ 2. List one reason why learning the alphabet was so important to women like Rashsundari Devi, Ramabai and" -> "... Rokeya.", "- Rokeya.", "~ Violation: ..." -> "... we can", "+ say that he or she has committed a violation."
- Images: exercise 2 is complete on two lines. The glossary entry "Violation:" runs over two lines.
- Verdict: matches the page for exercise 2. "Violation" is cut at the line end (P5).

### social-political-life-2 2023-12-23-rationalised, chapter 6, printed pages 65, 66, 67 and 71
- Hunk: "~ List three things that you know about some other part of the world from watching television?", "- Do", "+ Do you think this is true and why?", "~ ... ` 1,000 to ` 1,00,000 ..." -> "₹ ...", "~ As citizens ..." (p71) -> glue, "+ Local media"
- Images: p66 is opened: the blue questions on the left read "Can you list three different products ... ?" and "Take a newspaper and count ... Some people say that newspapers have too many advertisements. Do you think this is true and why?"
- Verdict: p66 matches the page (the stray "Do" is gone). p71 is extraction fault (rule) P1 (same as 2014 p77). p65 and p67 not viewed.

### social-political-life-2 2023-12-23-rationalised, chapter 7, printed pages 79, 80 and 85
- Hunk: rupee lines, "~ Why are goods sold in permanent shops costlier than those sold in the weekly markets or by roadside" -> "... hawkers?", p85 "- Most products, including vegetables,", "- fruits and flowers have special wholesale markets.", "- pass from one market to another.", "- products.", "~ These shops most often sell branded" -> "... products.", "+ Most products, including vegetables, fruits and flowers have special wholesale markets."
- Images: p79 and p85 opened.
- Verdict: matches the page (including "₹ 3000" in the notebook line on p79, the complete blue question, and the whole glossary on p85). p80 not viewed.

### social-political-life-2 2023-12-23-rationalised, chapter 8, printed pages 87 to 96
- Hunk: rupee lines (as 2019), "The weavers have no way of 1.This ..." fixed, p96 references.
- Images: p92 opened, p96 opened.
- Verdict: p92 matches the page (₹ and the blanks "₹ ______" are right). p96 is extraction fault (rule) P4: "Medical Council of India, ... Parks, Rosa. ..." and "World Health Organization, ... www.cehat.org/rthc/policybrieffinal.pdf www.in.undp.org (Sustainable Development Goals - SDGs)" are glued from several bullets. Not viewed: p87 to p90, p93 to p95.

### social-political-life-2 2023-12-23-rationalised, prelims
- Hunk: Preamble garbage, "~ Difficulty level" and the other bullet lines lose the bullet sign, "+ Content, which is irrelevant in the present context", "+ This present edition, is a reformatted version after carrying out the changes given above.", credits as above.
- Images: the same pages as 2024 (opened for 2024): the rationalisation page reads exactly those bullets and the closing sentence.
- Verdict: the bullet sentences match the page. The credits are P4 and the Preamble is wrong (see 2019). The 2023 pages were not opened, only the 2024 copy, so the entries are marked not viewed for 2023.

## 2024-05-24

### social-political-life-2 2024-05-24, chapter 1, printed pages 8 and 9
- Hunk: p8 "~ Excerpt ... Prohibition of discrimination ..." -> "Prohibition of discrimination ...", "+ Excerpt from Article 15 of the Indian Constitution EXERCISES Glossary", p9 "~ 3. What do you understand by the term 'all persons are equal before the law'?" -> "... Why do you think it is important in a democracy?", "- 4. According to the Rights of Persons with Disabilities Act ...", "- EXERCISES", "- Glossary", "- Look at the photograph ...", "- Universal adult franchise: ...", "+ 4. According to ...", "+ Look at the photograph ... safety?"
- Images: p8 has the box with the title "Excerpt from Article 15 of the Indian Constitution". "EXERCISES" and "Glossary" are on p9.
- Verdict: p9 matches the page (exercise 3, exercise 4, the paragraph under the photograph and the glossary entry are whole). p8 is extraction fault (rule) P1 and P7: "EXERCISES Glossary" (headings of p9) are glued to the box title of p8, and p9 has lost them as headings.
- Fix: P1.

### social-political-life-2 2024-05-24, chapter 2, printed pages 16 and 17
- Same comic as 2019 (not viewed). "+ Oh! My treatment did not cost much!" matches the 2019 page.

### social-political-life-2 2024-05-24, chapter 3, printed pages 25, 26, 30 and 31
- Hunk: p26 "- For example, the Legislative Assembly of the state of Himachal Pradesh has 68 MLA constituencies.", "- "name and Kashmir Jammu and Kashmir Punjab Uttarakhand Results of the Assembly Elections in Himachal Pradesh in 2017", "+ For example, ... 68 MLA constituencies. amma and Kashmir Jammu and Kashmir Punjab Uttarakhand Results of the Assembly Elections in Himachal Pradesh in 2017", p30 "~ The government announced a compensation for these Government smells the garbage Chief Minister promises funds for work f..." -> "... for these Government smells the garbage intend to supply drinking water ...", p31 "+ Chief Minister promises funds for work"
- Images: p26 has the sentence and the map with the labels "Jammu and Kashmir", "Punjab", "Uttarakhand". "Results of the Assembly Elections in Himachal Pradesh in 2017" is on the next page (p27). p30 ends "compensation for these". The clipping and its headline are on p31.
- Verdict: p26 is extraction fault (rule): map labels and a title of the next page are glued to a sentence (pattern D, one-off "amma" for "Jammu"). p30 is extraction fault (rule) P1 (clipping text of p31 glued to the cut sentence of p30). p31 matches the page: the headline "Chief Minister promises funds for work" is a heading as on the clipping.
```
- snapshot: "2024-05-24"
  chapter: 3
  find: "has 68 MLA constituencies. amma and Kashmir Jammu and Kashmir Punjab Uttarakhand Results of the Assembly Elections in Himachal Pradesh in 2017"
  replace: "has 68 MLA constituencies."
  note: "map labels and a table title of the next page glued to the sentence on printed page 26, check the table title returns on page 27"
```

### social-political-life-2 2024-05-24, chapter 6, printed pages 68, 71 and 73
- Hunk: p68 "~ News of India Report Crackdown on pol Protestors block roads and disrupt traffic cutting factories Moreover ..." -> "... luting factories Moreover ...", p71 glue of the "Local media" box (P1), p73 "~ It might help to ask the iN READERS, following questions- MEDIA a." -> "It might help to ask the following questions- MEDIA a.", "+ READERS,"
- Images: p68 clipping headline "Crackdown on polluting factories / Protestors block roads and disrupt traffic" is a headline in two lines. p73 is the exercise page with the diagram.
- Verdict: p68 is extraction fault (one-off): the old "cutting" and the new "luting" are both wrong, the page reads "polluting". The clipping body is also glued behind the headline. p73 is P3 (labels still glued, though the stray "iN" is gone).
```
- snapshot: "2024-05-24"
  chapter: 6
  find: "Crackdown on pol Protestors block roads and disrupt traffic luting factories"
  replace: "Crackdown on polluting factories Protestors block roads and disrupt traffic"
  note: "headline split over two lines on printed page 68, the page reads polluting"
```

### social-political-life-2 2024-05-24, chapter 7, printed pages 78 to 83 and 85
- Hunk: p78 "- We may buy milk from the dairy ... Sujata and Kavita were sent to buy groceries fr...", p78 "+ We may buy milk from the dairy, groceries from departmental stores, stationery, eatables or medicines from other", p79 "+ Sujata and Kavita were sent to buy groceries from their neighbourhood shop.", p80 "~ branded goods are expensive, ..." and "+ As you have read in the chapter on advertising,", p81 "+ Every city has areas for wholesale markets.", "+ The city", "+ We can understand this with the help of the following examples -", p82 "~ ... large number of goods are bought ..." -> "large number ...", "+ This is because a", p83 "+ It is through", p85 "+ Glossary", "+ Market Kind of goods sold Prices of goods Sellers Buyers", "+ Shopping complex"
- Images: p78, p81 and p83 opened. p78 ends "... medicines from other" and p79 begins with the bubble "Sujata and Kavita were sent to buy groceries from their neighbourhood shop." p81 "Every city has areas for wholesale markets. This is where goods first reach ..." and ends "The city". p83 starts "large number of goods are bought and sold that we don't use directly." p85 not opened.
- Verdict: p78, p81 and p83 match the page (they are the printed breaks, so the fragments are right). The p79 sentence matches the page word for word, which was not opened, so "not viewed" for p79, p80 and p82, p85 (table text matches the 2014 page).

### social-political-life-2 2024-05-24, chapter 8, printed pages 87, 89, 92, 93 and 95
- Hunk: p87 "~ 2. Ginning mill buys the cotton." -> "2. Ginning mil buys the cotton.", "~ 3. Ginning fruit the seeisand pressures the cotton into bales." -> "3. Ginning mi the seeds and presses the cotton into bales.", "~ 4. Spinning buys the bales." -> "4. Spinning sAna the bales.", "~ trader sells the cotton at the cotton market." -> "rader sells ...", "~ "5. Spinning fill signs the cotton into mill sells the dealers." -> "5. Spinning mill spins the cotton into dealers.", "+ 6. Spinning mill sells the", p95 "- or an or", "- us ub"
- Images: p87 shows the diagram with the labels "1. Trader sells the cotton at the Kurnool cotton market.", "2. Ginning mill buys the cotton.", "3. Ginning mill removes the seeds and presses the cotton into bales.", "4. Spinning mill buys the bales.", "5. Spinning mill spins the cotton into yarn.", "6. Spinning mill sells the yarn to yarn dealers." p95 has the numbered list 1 to 9 (matches).
- Verdict: p87 extraction fault (one-off and rule). The new text is closer on label 5 (but "into dealers." is glued), and worse on labels 2 and 3 ("mil", "mi") that were right before. The text came from the OCR of the diagram. p95 matches the page (the noise lines "or an or" and "us ub" are gone). p92 and p93 rupee lines were not opened for 2024.
```
- snapshot: "2024-05-24"
  chapter: 8
  find: "2. Ginning mil buys the cotton."
  replace: "2. Ginning mill buys the cotton."
  note: "diagram label on printed page 87, OCR dropped an l"
- snapshot: "2024-05-24"
  chapter: 8
  find: "3. Ginning mi the seeds and presses the cotton into bales."
  replace: "3. Ginning mill removes the seeds and presses the cotton into bales."
  note: "diagram label on printed page 87, OCR lost two words"
- snapshot: "2024-05-24"
  chapter: 8
  find: "4. Spinning sAna the bales."
  replace: "4. Spinning mill buys the bales."
  note: "diagram label on printed page 87"
- snapshot: "2024-05-24"
  chapter: 8
  find: "rader sells the cotton at the cotton market."
  replace: "1. Trader sells the cotton at the Kurnool cotton market."
  note: "diagram label on printed page 87, check against the image before pasting"
```

### social-political-life-2 2024-05-24, prelims
- Hunk: as 2023 with "Assistant Production : Rajesh Pippal Officer", "+ Published at the Publication Division by the Secretary, ...", "~ Layout Orijit Sen with Splash Communications Illustrations Orijit Sen" -> "Layout Orijit Sen with Splash Communications", "+ Illustrations", "+ Orijit Sen", "~ ` 65.00" -> "₹ 65.00".
- Images: the imprint shows "₹ 65.00", "Printed on 80 GSM paper with NCERT watermark", the "Published at the Publication Division ..." paragraph, "Layout Orijit Sen with Splash Communications" and "Illustrations Orijit Sen". The rationalisation page shows the five bullets and the closing sentence.
- Verdict: the price, the layout line, the "Illustrations" block, the "Published at" paragraph and the rationalisation bullets match the page. The credit rows are extraction fault (rule) P4 ("Head, Publication: Anup Kumar Rajput Division", "Assistant Production : Rajesh Pippal Officer"). The Preamble is misread as in 2019.

## Summary

Counts of entries as written above (an entry that holds several pages counts once under each verdict it names, so the totals are above the number of headings):

| Verdict | Count |
| --- | --- |
| matches the page | 37 |
| extraction fault (rule) | 49 |
| extraction fault (one-off) | 21 |
| not viewed | 14 |

Patterns of the earlier review (review/social-political-life-2.md) that are now gone:

- Pattern C, the source gap of the 2014 References: the references now appear (ch10 p122, 2014 and 2016) and match the page.
- Rule A for the table-style blocks that carried real boxes as "[table]": the box "Read the story given above ... Hakim Sheik?" is whole, exercise 5 on 2023 p35 is whole, the market table (p103, p91, p85) is one header sentence plus rows, and the glossary of ch06 p79 in 2022 is clean.
- Rule B in its caption form for the 2014 photo captions: "A doctor in a rural health care centre ..." is no longer inside the sentence.
- The "EXERCISES cs" and "EXERCISES cS" one-offs (2019, 2020) and the "or an or" and "us ub" noise of 2024 are gone.
- Pattern H for the backtick: 2019, 2020, 2023 and 2024 all read "₹", and p98 of 2019, 2020 and 2023 was checked on the image.
- The stray "Do" and "d." / "a." letters glued to exercise sentences (2023) are gone, and the cut of "(PHCs) ... find out the facilities provided and people" and of "Can you share with your class a local song or a poem on dignity" is closed.

Not gone, and one regression to note: in 2024 the diagram labels of ch08 p87 are worse (old "Ginning mill buys the cotton." is now "Ginning mil buys the cotton.").

The three remaining patterns that matter most:

1. P1, glue at the page foot. A heading, box, clipping or map caption (or the headings "EXERCISES" and "Glossary" of the next page) is glued into a body sentence that is cut at the page break, or moves to the wrong page. Seen in ch01 p8 (2024), ch03 p31 (2016, 2019, 2020, 2022, 2023, 2024), ch03 p26, p30 (2024), ch03 p36 (2022), ch04 p49 and p50 (2022), ch06 p77 and p78 (2022), ch06 p77 (2014, 2016, 2023, 2024), ch07 p88 (2014, 2016), ch09 p104 (2022). This one loses the page marker of a box and makes a sentence that is on no page.
2. P2 and P3, comic bubbles and diagram labels. Bubbles are merged by line (ch02 p22, ch03 p31, ch04 p47 in every edition, with the one case where words are lost: ch04 p47/p48 in 2022, "taken leave today." and "How would I know? I'm on strike, remember?"). Diagram labels are glued into exercises (ch06 p79 in 2019, 2020, 2022 and ch06 p73 in 2024) and the cotton-boll labels are scrambled (ch08 p87, p93).
3. P4 and P5, structure read line by line. Two-column tables (ch02 p20), credit rows on the imprint page, reference bullets (ch09 p110, ch08 p96) and OCR paragraphs (ch07 p82, p91, ch05 p57) are cut at line ends or glued across rows. A smaller linked fault is P6 for the 2022 rupee sign ("=", "z", "?") and the dropped blank after it, and the Preamble OCR which does not match the page in any edition.
