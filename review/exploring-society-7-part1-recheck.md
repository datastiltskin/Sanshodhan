# exploring-society-7, part 1: recheck after the rule change

Edition live-2026-10-18 (one edition only). Each entry says what the page image shows.
Patterns referred to below:

- P1 (photo number badges): the numbered badges on a photo collage come out as stray one-line paragraphs.
- P2 (caption merge/split): captions of side-by-side photos are merged line by line into one caption, or one caption is cut into several blocks.
- P3 (map/diagram labels): axis ticks, legends and place names on maps come out as stray paragraphs or fragments.
- P4 (noodles pages): blank "Noodles" pages give nothing, only the heading, or only the footnote, depending on the page.

## Chapter 1, Geographical Diversity of India

### exploring-society-7 live-2026-10-18, chapter 1, printed page 3
- Page shows: caption "Fig. 1.2. These are satellite images of the Himalayan range. Note that the length of the range is about 2500 km."
- Verdict: matches the page. The "- Note that the" fragment is now joined into the caption.

### chapter 1, printed page 6
- Page shows: caption "Fig. 1.6. Kath-kuni House, Himachal Pradesh" in one block under the photo.
- Text: caption cut in two blocks ("Fig. 1.6. Kath-kuni House," and "Himachal Pradesh"). Words are right, structure is not (P2).
- Verdict: extraction fault (one-off).
- Fix:
  - snapshot: "live-2026-10-18", chapter: 1
  - find: "> [caption] Fig. 1.6. Kath-kuni House,\n\n> [caption] Himachal Pradesh"
  - replace: "> [caption] Fig. 1.6. Kath-kuni House, Himachal Pradesh"
  - note: "caption under the photo on page 6 is one two-line caption"

### chapter 1, printed page 7
- Page shows: DON'T MISS OUT box, the paragraph runs behind the photo collage but the words "a World Heritage Site by UNESCO" are in the page text layer. Badges 1 to 7 sit on the photos. Caption "Fig. 1.7. ... 7. Rhododendron — a type of sherbet is made out of this flower."
- "~ The park has been declared 1 2 4 5 6 a World Heritage Site": new side matches the page (the stray digits are gone).
- "- 7. Rhododendron — a" / "+ 7. Rhododendron — a type of sherbet...": the caption is now whole, matches the page.
- "+ 1", "+ 2", "+ 4 5", "+ 6" (and the earlier "[note] 3", "[note] 7"): the photo badges, not text of the book (P1). Verdict: extraction fault (rule). Fix: drop one-to-two-digit lines that sit alone in the badge position of a picture block, or at least digits-only paragraphs on a page with a photo collage. Seen: ch1 p7.

### chapter 1, printed page 10
- Page shows: Fig. 1.11, 1.12, 1.13, 1.14 as four captions under four photos, and Fig. 1.15 under the pair of transport photos.
- "+ Fig. 1.15. Modes of transport in the Gangetic plains": matches the page.
- Not in the change list but seen: Fig. 1.11 to 1.14 are merged and interleaved into two caption blocks ("Fig. 1.12. Aerial view of Delhi with the in the plains river Yamuna on top right Fig. 1.13. ..."), so the words of Fig. 1.11 and Fig. 1.12 are mixed (P2). Verdict: extraction fault (rule, P2).
- Fix: see the one-off below, but the pattern is the point.
  - snapshot: "live-2026-10-18", chapter: 1
  - find: "> [caption] Fig. 1.11. Modern agricultural practices\n\n> [caption] Fig. 1.12. Aerial view of Delhi with the in the plains river Yamuna on top right Fig. 1.13. Multi-cropping in Uttar Pradesh Fig. 1.14. Rural women working in a paddy field in West Bengal"
  - replace: "> [caption] Fig. 1.11. Modern agricultural practices in the plains\n\n> [caption] Fig. 1.12. Aerial view of Delhi with the river Yamuna on top right\n\n> [caption] Fig. 1.13. Multi-cropping in Uttar Pradesh\n\n> [caption] Fig. 1.14. Rural women working in a paddy field in West Bengal"
  - note: "four captions of the photo grid on page 10, each under its own photo"

### chapter 1, printed page 11
- Page shows: Fig. 1.17 "The Northern plains grey langur sits on a wooden beam in Bandhavgarh National Park, Madhya Pradesh" and Fig. 1.18 "The majestic tiger that was on the verge of extinction. Project Tiger has supported the return of the tiger to its habitats."
- "- Project Tiger has sits on a wooden beam in Bandhavgarh..." / "+ same sentence": the scrambled interleaving of two side-by-side captions is still there (P2). Verdict: extraction fault (one-off here, rule P2 overall).
- Fix:
  - snapshot: "live-2026-10-18", chapter: 1
  - find: "Fig. 1.17. The Northern plains grey langur Fig. 1.18. The majestic tiger that was on the verge of extinction. Project Tiger has sits on a wooden beam in Bandhavgarh National Park, Madhya Pradesh supported the return of the tiger to its habitats."
  - replace: "Fig. 1.17. The Northern plains grey langur sits on a wooden beam in Bandhavgarh National Park, Madhya Pradesh\n\n> [caption] Fig. 1.18. The majestic tiger that was on the verge of extinction. Project Tiger has supported the return of the tiger to its habitats."
  - note: "two side-by-side captions on page 11 interleaved by line"
  - (the "Fig. 1.16 ... Fig. 1.17" part of the same caption line starts the block, so check the line before pasting: Fig. 1.16 must be its own caption too.)

### chapter 1, printed page 13
- Page shows: Fig. 1.23 caption "Camel vendor at the Pushkar Mela (at the edge of the Thar Desert)" as one right-aligned caption.
- "~ Mela (at the edge of -> Mela (at the edge of the Thar" and "+ Desert)": text is split into four blocks (Fig. 1.23. / Camel vendor at the Pushkar / Mela (at the edge of the Thar / Desert)). Words are all there, order right (P2). Verdict: extraction fault (one-off).
- Fix:
  - snapshot: "live-2026-10-18", chapter: 1
  - find: "> [caption] Fig. 1.23.\n\n> [caption] Camel vendor at the Pushkar\n\n> [caption] Mela (at the edge of the Thar\n\n> [caption] Desert)"
  - replace: "> [caption] Fig. 1.23. Camel vendor at the Pushkar Mela (at the edge of the Thar Desert)"
  - note: "caption narrow column on page 13 wrapped into four lines"

### chapter 1, printed page 15
- Page shows: Fig. 1.26 "...proved to be an excellent deterrent to the enemy."
- "~ Fig. 1.26 ... this location in the hills -> ... proved to be an excellent deterrent": matches the page (the tail "to the enemy." is cut off by the changes file, present in the text).

### chapter 1, printed page 18
- Page shows: Fig. 1.28 to 1.32, each under its photo. Fig. 1.32 reads "Coal mines in the plateau; an important resource, especially in the production of electricity. Coal is a fossil fuel, the use of which contributes to global warming."
- "~ Coal is a fossil fuel, the use of which contributes -> ... to global warming.": new side matches the page. But Fig. 1.29, 1.30, 1.31 and 1.32 are one merged caption, and the tail of Fig. 1.31 ("small insects in sticky traps and digests them!") sits in a separate block (P2). Verdict: extraction fault (rule P2).
- Fix: see P2. One-off:
  - snapshot: "live-2026-10-18", chapter: 1
  - find: "> [caption] Fig. 1.28. Powerhouse Waterfalls at Periyakanal, near Munnar, Kerala Fig. 1.29. Lion-tailed macaque Fig. 1.30. King cobra of the in the Western Ghats Western Ghats Fig. 1.31. This is an insectivorous plant, meaning it feeds on insects, found in the Western Ghats. It catches Fig. 1.32. Coal mines in the plateau; an important resource, especially in the production of electricity.\n\n> [caption] small insects in sticky traps and digests them!\n\n> [caption] Coal is a fossil fuel, the use of which contributes to global warming."
  - replace: "> [caption] Fig. 1.28. Powerhouse Waterfalls at Periyakanal, near Munnar, Kerala\n\n> [caption] Fig. 1.29. Lion-tailed macaque in the Western Ghats\n\n> [caption] Fig. 1.30. King cobra of the Western Ghats\n\n> [caption] Fig. 1.31. This is an insectivorous plant, meaning it feeds on insects, found in the Western Ghats. It catches small insects in sticky traps and digests them!\n\n> [caption] Fig. 1.32. Coal mines in the plateau; an important resource, especially in the production of electricity. Coal is a fossil fuel, the use of which contributes to global warming."
  - note: "five captions of page 18 each under its own photo"
  - (the exact leading text of the first caption block was cut off in the change list. Check the line in the Markdown before pasting.)

### chapter 1, printed page 26
- Page shows: a blank "Noodles" page with the footnote "*'Noodles' is our abbreviation for 'Notes and Doodles'!" and a pencil.
- "- XN aN yN": OCR of the pencil doodle, rightly gone. But the page now has no text at all (heading and footnote both missing) (P4). Verdict: matches the page for the removed garbage, extraction fault (rule P4) for the missing heading and footnote.

## Chapter 2, Understanding the Weather

### chapter 2, printed page 28
- Page shows: "In simple terms, it is the layer of gases..." and the diagram labels Stratosphere, Tropopause, Ozone Layer, Troposphere, and caption "Fig. 2.2".
- "~ In simple ld terms -> In simple terms": new matches.
- "- Ozone Layer Tropopause oo ve" / "+ Tropopause Ozone Layer": new matches the labels. Verdict: matches the page.

### chapter 2, printed page 31
- Page shows: four captions under the four drawings: Fig. 2.4.1 "Snow melts quickly when it's warm.", Fig. 2.4.2 "Cloudy weather —it's getting cold.", Fig. 2.4.3 "In winter, coconut oil turns solid.", Fig. 2.4.4 "Curd takes longer to set in cold weather."
- "+ to set in cold weather.": a fragment of Fig. 2.4.4 only. The captions of Fig. 2.4.3 and the first half of 2.4.4 are LOST from the text (they were not in the committed text either, nothing in the file matches "coconut" or "Curd"). Verdict: extraction fault (one-off), the most serious finding of this chapter.
- Fix:
  - snapshot: "live-2026-10-18", chapter: 2
  - find: "> [caption] to set in cold weather."
  - replace: "> [caption] Fig. 2.4.3. In winter, coconut oil turns solid.\n\n> [caption] Fig. 2.4.4. Curd takes longer to set in cold weather."
  - note: "captions of the two lower drawings on page 31 are not in the text layer, read from the page image"

### chapter 2, printed page 40
- Page shows: weather warning map with legend. "- en aap": garbage from the map, rightly gone. Legend items are separate caption blocks (P3). Verdict: matches the page.

### chapter 2, printed page 44
- Noodles page (same layout as p26). "- XN aN yN" is the pencil doodle. Not viewed individually. Text has only the footnote (P4).

## Chapter 3, Climates of India

### chapter 3, printed page 52
- Page shows: "We will soon see the case of the monsoon winds." and the map Fig. 3.7 with labels wind and cyclonic circulation, and tick labels.
- "~ monsoon oy winds -> monsoon winds": new matches.
- "- cyclonic circulation LZ Ay es ve any LF we, Cs", "- oR ot", "- ye Ly):" / "+ cyclonic circulation": map noise gone, label kept. Verdict: matches the page. Note: the Topography margin definition is split into three caption blocks ("wind", "Topography:", "The totality of ...") with a stray "wind" caption that is the map label (P2/P3).

### chapter 3, printed page 59
- Page shows: "Fig. 3.13. Cyclone Fani" under the satellite image, labels clouds formed, low pressure centre, winds bringing moist air from sea.
- "+ Fig. 3.13. Cyclone Fani": matches.

## Chapter 4, New Beginnings: Cities and States

### chapter 4, printed page 82
- "- XN aN yN": pencil doodle on a Noodles page. Not viewed individually, the page text is empty (P4). Garbage correctly gone.

## Chapter 5, The Rise of Empires

### chapter 5, printed page 88
- Page shows: six hexagons. 01 "Maintains an army to keep the tributary states under control, expand the empire or protect it from outside aggression". 02 "Designs and maintains an administration, with officials to manage the territories, collect taxes, maintain law and order, etc." 03 "Makes laws, issues currencies, weights and measures, regulates trade". 04 "Controls and regulates access to resources (mines, forest and agricultural produce, manpower)". 05 "Encourages art, literature, religions, schools of thought, centres of learning". 06 "Maintains communication networks (roads, river and sea navigation) and other infrastructure for administration, trade and people's welfare". Centre: "Emperor exerts central authority over the empire's tributary territories and kings".
- "~ ... under control, le 2 an or protect it -> ... under control, 02 or protect it", "- Makes laws ... ja Controls ...", "- trade and people's welfare a sae ...", and the "+" versions: the OCR noise (le 2 an, ja, a sae) is gone, but the hexagon text is still interleaved by line across the six boxes (01 loses "expand the empire", which sits in the 02 line followed by "06 02"). Words are all present, boxes are scrambled. Verdict: extraction fault (one-off), P3.
- Fix (override entries, snapshot "live-2026-10-18", chapter 5, note "hexagon diagram on page 88, text of the six boxes read in line order across boxes"). Replace the five table lines that carry the text:
  - find: "> [table] Maintains an army to keep the tributary states under control, 02 or protect it from outside aggression Designs and maintains an administration, with expand the empire 06 02" replace: "> [table] 01 Maintains an army to keep the tributary states under control, expand the empire or protect it from outside aggression\n\n> [table] 02 Designs and maintains an administration, with officials to manage the territories, collect taxes, maintain law and order, etc."
  - find: "> [table] Maintains communication networks (roads, river and sea navigation) and officials to manage the territories, collect other infrastructure taxes, maintain law for administration," replace: "> [table] 06 Maintains communication networks (roads, river and sea navigation) and other infrastructure for administration, trade and people's welfare"
  - find: "> [table] and order, etc." replace: "" and find: "> [table] trade and people’s welfare" replace: ""
  - find: "> [table] 05 Encourages art, literature, religions, 05 03" replace: "> [table] 05 Encourages art, literature, religions, schools of thought, centres of learning"
  - find: "> [table] Makes laws, issues currencies, weights and measures, regulates trade 04 Controls and regulates access schools of thought, 04 centres of learning to resources (mines, forest and agricultural produce, manpower)" replace: "> [table] 03 Makes laws, issues currencies, weights and measures, regulates trade\n\n> [table] 04 Controls and regulates access to resources (mines, forest and agricultural produce, manpower)"
  - (the lone "> [table] 01" line before them must then go too: find "> [table] 01\n\n" replace "").

### chapter 5, printed page 96
- Page shows: Fig. 5.9 two maps with labels (Granicus, Guagamela, Pella, Issus, Susa, Alexandria, Persepolis, Babylon, Memphis, Hydaspes, Indus, Jhelum (Hydaspes), Sindh), caption "Fig. 5.9", and the timeline "334-331 BCE:" with the paragraph about Alexander.
- "- if": stray fragment, gone, nothing on the page. Matches.
- "+ Indus Jhelum Hydaspes) Jhelum (Hydaspes) Indus", "+ Sindh": map labels (P3), not prose, harmless but unreadable. Verdict: extraction fault (rule P3), cosmetic. The paragraph "Alexander, a young and powerful Greek king..." is typed as a caption, though it is the body of the 334-331 BCE timeline entry. Cosmetic.

### chapter 5, printed page 98
- Page shows: the yellow box with the bold heading "Alexander's dialogue with the Gymnosophists", then the story.
- "~ Alexander's dialogue with the Gymnosophists Alexander heard ... -> Alexander heard ..." and "+ Alexander's dialogue with the Gymnosophists": heading now separate from the paragraph. Matches the page.
- Not in the change list: Fig. 5.11 caption "A Greek coin probably showing Alexander on horseback attacking Porus on his elephant." is cut in two with the sentence "Historians view such exchanges ..." between the halves. Words all present, the caption is broken (P2). Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 5
  - find: "> [caption] Fig. 5.11. A Greek coin\n\nHistorians view such exchanges as a meeting of two great traditions — Greek and Indian philosophies.\n\n> [caption] probably showing Alexander on horseback attacking Porus on his elephant."
  - replace: "> [caption] Fig. 5.11. A Greek coin probably showing Alexander on horseback attacking Porus on his elephant.\n\nHistorians view such exchanges as a meeting of two great traditions — Greek and Indian philosophies."
  - note: "caption of the coin photo on page 98 is one caption, the paragraph runs beside it"

### chapter 5, printed page 109
- Page shows: Fig. 5.20 caption "The Mauryas were renowned for their highly polished stone pillars, as can be seen in this capital of the Sarnath pillar."
- "~ ... as can -> ... as can be seen in this capital of the": more complete, but the last words "Sarnath pillar." are LOST (nothing in the file matches "Sarnath pillar"). A lost caption tail that is on the page. Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 5
  - find: "as can be seen in this capital of the\n"
  - replace: "as can be seen in this capital of the Sarnath pillar.\n"
  - note: "last line of the Fig. 5.20 caption on page 109 is missing from the text layer"

### chapter 5, printed page 110
- Page shows: Fig. 5.24 "Terracotta of Saptamātrikās or seven mother goddesses (a continuing tradition)." and Fig. 5.25 "Head of a terracotta horse (notice the elaborate design of the bridle)." side by side.
- "+ Fig. 5.24. ... seven Fig. 5.25. Head of a terracotta mother goddesses ..." and "+ horse (notice ...)": the two captions interleaved (P2). Verdict: extraction fault (one-off, rule P2).
  - snapshot: "live-2026-10-18", chapter: 5
  - find: "> [caption] Fig. 5.24. Terracotta of Saptamātrikās or seven Fig. 5.25. Head of a terracotta mother goddesses (a continuing tradition).\n\n> [caption] horse (notice the elaborate design of the bridle)."
  - replace: "> [caption] Fig. 5.24. Terracotta of Saptamātrikās or seven mother goddesses (a continuing tradition).\n\n> [caption] Fig. 5.25. Head of a terracotta horse (notice the elaborate design of the bridle)."
  - note: "two side-by-side captions on page 110 interleaved by line"

### chapter 5, printed page 116
- "- XN aN yN": pencil doodle on a Noodles page. Not viewed individually (page text is empty, P4). Garbage correctly gone.

## Chapter 6, The Age of Reorganisation

### chapter 6, printed page 119
- Page shows: Fig. 6.2 map with axis ticks 60E to 90E, labels (Indo-Greeks, Kuṣhāṇas, Śhakas (Indo-Scythians), Śhungas, Sātavāhanas, Chedis, Cholas, Pāṇḍyas, Cheras, Arabian Sea, Bay of Bengal), scale 0/500/1,000 km, caption "Fig. 6.2. Prominent dynasties of India during the age of reorganisation".
- "~ Fig. 6.2 ... -> 70E 80E 90E Fig. 6.2 ... 60E": worse. The axis ticks are now glued into the caption, while the same ticks also appear as four separate captions ("+ 60E", "+ 70E", "+ 80E", "+ 90E") and "+ 500". Verdict: extraction fault (rule P3). The "- Ś h u n g a s" removal is fine, but the map labels are now headings ("### Śhakas", "### Śhungas", "## Arabian", "## Bay of Bengal", "## Sea").
- Fix: rule P3, drop axis-tick-only blocks (digits plus E/N/W/S) and never append them to a "Fig." caption, and do not promote map labels to headings. One-off override:
  - snapshot: "live-2026-10-18", chapter: 6
  - find: "> [caption] 70E 80E 90E Fig. 6.2. Prominent dynasties of India during the age of reorganisation 60E"
  - replace: "> [caption] Fig. 6.2. Prominent dynasties of India during the age of reorganisation"
  - note: "axis tick labels of the map on page 119 were glued into the caption"

### chapter 6, printed page 120
- Page shows: the half-circle diagram Fig. 6.3: left "Dynasties from within the Subcontinent: Śhungas, Chedis, Sātavāhanas, Cholas, Cheras, Pāṇḍyas", right "Dynasties from outside the Subcontinent: Indo-Greeks, Śhakas, Kuṣhāṇas", centre "Prominent dynasties of the Subcontinent".
- "+ Fig. 6.3": matches the page. But the diagram text is jumbled in the body ("Dynasties from outside the Subcontinent within the Subcontinent Śhungas, Chedis, Sātavāhanas, Indo-Greeks, Śhakas, Kuṣhāṇ as Cholas, Cheras, Pānḍyas", with "Kuṣhāṇ as" broken, and the centre text as two headings). Verdict: extraction fault (one-off, P3).
  - snapshot: "live-2026-10-18", chapter: 6
  - find: "Dynasties from outside the Subcontinent within the Subcontinent Śhungas, Chedis, Sātavāhanas, Indo-Greeks, Śhakas, Kuṣhāṇ as Cholas, Cheras, Pānḍyas"
  - replace: "Dynasties from within the Subcontinent: Śhungas, Chedis, Sātavāhanas, Cholas, Cheras, Pānḍyas. Dynasties from outside the Subcontinent: Indo-Greeks, Śhakas, Kuṣhāṇas."
  - note: "Fig. 6.3 half-circle diagram on page 120, left and right halves read line by line"
  - (the lines "Dynasties from" just before it and the headings "Prominent dynasties of the / Subcontinent" go with it. Check the lines in the Markdown before pasting.)

### chapter 6, printed page 130
- Page shows: Fig. 6.14 map with ticks 76E 78E 80E and 12N 10N 8N, labels (Chola, Chera, Pandya, Kaveri R., Uraiyur, Vanji (Karur), Madurai, Arabian sea, Bay of Bengal), the legend box and scale (0 100 200 km), caption "Fig. 6.14. Kingdoms in the South (note that borders are approximate and fluctuated in time)."
- "- 200 km", "- Capital Cities Rivers.", "- LEGEND South Indian Kingdoms": the pieces of the legend are gone from their old places and now sit in one block "+ LEGEND South Indian Kingdoms Chola Chera Pandya Capital Cities Rivers 200 km 100". The "+ 76E", "+ 78E", "+ N.8", "+ No8" blocks are axis ticks (the "N.8" and "No8" are OCR of "8°N", twice). Verdict: extraction fault (rule P3), cosmetic. The caption itself matches the page.

### chapter 6, printed page 136
- Page shows: Fig. 6.22 "Headless statue of King Kaṇiṣhka" (two lines under the statue) and Fig. 6.23 "Coins of Kaṇiṣhka".
- "- of King Kaṇiṣhka" / "+ Fig. 6.23. Coins of Kaṇiṣhka of King Kaṇiṣhka": the tail of the Fig. 6.22 caption has moved onto the Fig. 6.23 caption. Page text is wrong on both captions. Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 6
  - find: "> [caption] Fig. 6.22. Headless statue\n"
  - replace: "> [caption] Fig. 6.22. Headless statue of King Kaṇiṣhka\n"
  - note: "caption continues on a second line under the statue on page 136"
  - and a second entry: find "Fig. 6.23. Coins of Kaṇiṣhka of King Kaṇiṣhka" replace "Fig. 6.23. Coins of Kaṇiṣhka", note "tail of the Fig. 6.22 caption landed on the coin caption"

### chapter 6, printed page 137
- Page shows: "THINK ABOUT IT: Do you know where Gāndhāra is? ..." with no other words in front.
- "~ Ce Do you know where Gāndhāra is? -> Do you know ...": new matches the page.
- Not in the change list: Fig. 6.24 caption is cut in two blocks (P2), words complete.

### chapter 6, printed page 138
- Page shows: map Fig. 6.25 (left half) with ticks 10E to 70E, labels (Rome, Byzantium, Antioch, Alexandria, Damascus, Samarkand, Balkh, Qumis- Iran, Black Sea, Mediterranean Sea, Caspian Sea, Persian Gulf, Gulf of Oman, Gulf of Aden, Red Sea, SCYTHIA, PERSIA, ARABIA, EGYPT), scale 0/1,000/2,000 km, caption "Fig. 6.25. Some of the trade routes of the ancient world. The network marked in green shows the Silk Route connecting China with the Mediterranean world and passing through central Asia, Persia, etc."
- "~ Black Sea -> Błack Sea": the old side was right. The new text has an OCR/glyph error (a stray "ł"). Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 6, find: "Błack Sea", replace: "Black Sea", note: "map label on page 138 misread"
- "~ Fig. 6.25 ... -> 10E 20E 30E 40E 50E 60E Fig. 6.25 ...": the axis ticks are now glued to the front of the caption (regression, P3).
  - snapshot: "live-2026-10-18", chapter: 6, find: "10E 20E 30E 40E 50E 60E Fig. 6.25.", replace: "Fig. 6.25.", note: "axis ticks glued to the caption"
- "- The network marked in green ... Byzantium Rome Samarkand Balkh Qumis- Iran Damascus Alexandria" / "+ The network marked in green shows the Silk Route ... etc.": the caption sentence is now clean and matches the page. The place names are in their own caption blocks (P3).
- Stray: "+ 1,000", "+ 10E N.09", "+ 20E n", "+ 40N Mediterranean Sea 30N", "+ 70", "+ 70 w-Rome", "+ Qumis- Iran Persian n n Gult Gulf of Oman Damascus" ("Gult" misread of Gulf): extraction fault (rule P3), cosmetic, no prose lost.

### chapter 6, printed page 139
- Page shows: the right half of the map: ticks 80E to 120E, legend (Main Route of Silk Road, Other Caravan Routes, Important Centres), labels (Takṣhaśhilā, Mathura, Pāṭaliputra, Tāmralipti, Luoyang, CHINA, INDIA, Bay of Bengal, South China Sea, East China Sea, Yellow Sea, Celebes Sea, Andaman Sea, Gulf of Thailand, Indian Ocean).
- "~ Fast China -> East China", "~ 'Celebes Sea -> Celebes Sea": new matches the page.
- "~ Main Route of Silk Road Other Caravan Routes Important Centres: -> ... Important Centres Luoyang Yellow Sea 30N Sea Takṣhaśhilā": labels now glued into the legend caption (P3, cosmetic). "+ E", "+ E", ticks repeated twice, "+ South China Sea".
- "- Bay", "- Bengal", "- Luoyang", "- Takṣhaśhilā", "- Yellow", "- ‘China": single-word label fragments, moved into the legend block or ("Bay of Bengal") a separate caption. Nothing prose lost.

### chapter 6, printed page 144
- "- SN aN yN": pencil doodle on a Noodles page. Not viewed individually (page text is empty, P4).

## Chapter 7, The Gupta Era: An Age of Tireless Creativity

### chapter 7, printed page 146
- Page shows: "Dhruv and Bhavisha had just returned from their journey to the Pānḍya kingdom." (italic intro) and the Fig. 7.2 map with ticks 70E 80E 90E, the compass, and five call-out boxes with labels (Gupta Empire, Kāmarūpa Kingdom, Vākāṭaka Kingdom, Pallava Kingdom).
- "~ EDhruv -> Dhruv": new matches the page.
- "+ 70E", "+ 80E", "+ 90E", "+ E", "+ W": axis ticks and compass letters as paragraphs (P3), cosmetic. Also the tick block "80E" appears twice but the page has 70E, 80E, 90E. The Gupta call-out is jumbled: "The Gupta Empire was the most powerful and flourished from the 3rd to Kāmarūpa Kingdom the 6th century CE, with its capital at Pāṭaliputra" (a map label inside the sentence). Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 7
  - find: "flourished from the 3rd to Kāmarūpa Kingdom the 6th century CE"
  - replace: "flourished from the 3rd to the 6th century CE"
  - note: "map label Kāmarūpa Kingdom sits between two lines of the Gupta call-out on page 146"

### chapter 7, printed page 152
- Page shows: Fig. 7.8 map, caption "The Gupta Empire's extent. Note that the Vākāṭakas were the allies of the Guptas. The Guptas claim to have conquered parts of the east coast, down to the Pallavas, whom they may have briefly subdued."
- "~ ... down to the -> ... down to the Pallavas, whom they may have briefly subdued.": new side matches the page (the old sentence was cut).
- "~ Fig. 7.8 ... -> 70E 80E 90E Fig. 7.8 ...": axis ticks glued onto the caption front (regression, P3).
  - snapshot: "live-2026-10-18", chapter: 7, find: "70E 80E 90E Fig. 7.8.", replace: "Fig. 7.8.", note: "axis ticks glued to the caption"

### chapter 7, printed page 163
- Page shows: Fig. 7.18.1 to 7.18.3 caption ending "...A sculpted depiction from the Mahābhārata".
- "~ Arjuna and Karṇa in battle — A sculpted depiction from -> ... from the Mahābhārata": new matches the page.

## Chapter 8, How the Land Becomes Sacred

### chapter 8, printed page 169
- Page shows: "In Sikhism, takhts are seats or centres of spiritual a u t h o r i t y — f o r example..." in a narrow justified column (letters spread out in the printing, the word is "authority").
- "~ spiritual a u t h o r i t y   —   f o r example -> spiritual authority   —   for example": the new text reads the words right (matches the page). Only the triple spaces round the dash remain, cosmetic.
  - snapshot: "live-2026-10-18", chapter: 8, find: "authority   —   for example", replace: "authority — for example", note: "justified narrow column on page 169 spread the dash with spaces"
- Fig. 8.3 caption and the margin glossary (Pilgrimage, Shrine, Relic) are separate blocks, as printed.

### chapter 8, printed page 171
- Page shows: Fig. 8.4 caption "Pandharpur wārī, an 800-year-old tradition in Maharashtra. Warī means a pilgrimage that is held regularly, in this case annually. Pilgrims walk in large groups for 21 days to the famous Vithoba temple in Pandharpur." and, in the margin, the glossary entry "Tīrthankara: Literally, someone who makes a tīrtha, ...".
- "~ Pilgrims walk ... Vithoba temple in Tīrthankara: Literally ... -> Tīrthankara: Literally ..." and "+ Pilgrims walk in large groups for 21 days to the famous Vithoba temple in Pandharpur.": the margin note is no longer glued into the caption and the caption is whole. Matches the page.

## Chapter 9, From the Rulers to the Ruled: Types of Government

Pattern P5 (flattened tables): table cells come out as loose paragraphs in column order, row labels are separated from their rows, and part of the text of a neighbouring box can be pulled into the table. Seen: ch9 p195 (Table 9.1), p205 (Table 9.2), p208 (the two exercise tables), and ch12 p257.

### chapter 9, printed page 187
- Page shows: the THINK ABOUT IT box in the right margin, and "Fig. 9.3" under the classroom drawing.
- "- Vl THINK ABOUT IT": the OCR of the box heading is gone, and "> [caption] THINK ABOUT IT" is now a separate caption block followed by the box text. "+ Fig. 9.3": matches. Verdict: matches the page (box heading typed as a caption, cosmetic).

### chapter 9, printed page 191
- Page shows: the green margin pull-out "What is the government working for? What goals is it trying to achieve?" next to item 4.
- "- NS es e SI", "- we": noise, nothing on the page. Matches. The pull-out is a "[note]" block with the right words.

### chapter 9, printed page 192
- Page shows: the icon list (Universal adult franchise, Fundamental rights with a "RIGHTS" icon, Independent judiciary).
- "- GY OE;", "- is": noise, gone, matches.
- "+ RIGHTS": the word on the icon, now a "## RIGHTS" heading in the text. Not book text. Verdict: extraction fault (one-off, P1).
  - snapshot: "live-2026-10-18", chapter: 9, find: "## RIGHTS\n\n", replace: "", note: "word printed on the rights icon on page 192, not a heading"

### chapter 9, printed page 195
- Page shows: Table 9.1 with rows India (prime minister and the council of ministers / Lower House (Lok Sabha) is more powerful than Upper House (Rajya Sabha) / independent from executive and legislature (separation of power)), USA (president / equal power between Upper House (Senate) and Lower House (House of Representatives) / independent ...), South Korea (president / single house (National Assembly) / independent ...), Australia (prime minister and the council of ministers / equal power ... / independent ...), then two blank rows A and B. Caption "Table 9.1 Different forms of democratic government". Then the bullet "Legislature: The legislature is the body of the government which is responsible for making laws. ..."
- "~ Institution Executive Legislature Judiciary Lower House ... -> Lower House ..." and "~ South Korea president single house (National Assembly) -> president single house (National Assembly)", "- USA president independent from ...", "~ prime minister ... Australia A B Legislature: ... -> Legislature: ...", "- prime minister and the council of ministers India equal power between ...": the sentence "Legislature: The legislature is the body..." is now clean (matches the page), and A and B are separate. But Table 9.1 is flattened: cells are in column order, so "equal power ..." sits under India's rows, and "India" follows the first cell of its own row. All words are present, row membership is lost (P5). Verdict: extraction fault (one-off).
- Fix:
  - snapshot: "live-2026-10-18", chapter: 9
  - find: from "Institution Executive Legislature Judiciary" to the line "B" (the whole block, 28 lines in the Markdown just before "> [caption] Table 9.1 ...")
  - replace: "Institution | Executive | Legislature | Judiciary\n\nIndia | prime minister and the council of ministers | Lower House (Lok Sabha) is more powerful than Upper House (Rajya Sabha) | independent from executive and legislature (separation of power)\n\nUSA | president | equal power between Upper House (Senate) and Lower House (House of Representatives) | independent from executive and legislature (separation of power)\n\nSouth Korea | president | single house (National Assembly) | independent from executive and legislature (separation of power)\n\nAustralia | prime minister and the council of ministers | equal power between Upper House (Senate) and Lower House (House of Representatives) | independent from executive and legislature (separation of power)\n\nA | | |\n\nB | | |"
  - note: "Table 9.1 on page 195, rows rebuilt from the page image"

### chapter 9, printed page 197
- Page shows: Fig. 9.6 "Chola period inscriptions on the walls of Vaikuntha Perumal temple, Uttaramerur, Tamil Nadu".
- "~ ... temple, -> ... temple, Uttaramerur, Tamil Nadu": new matches the page.

### chapter 9, printed page 198
- Page shows: margin glossary "Slave: A person who is forced to work for and obey another and is considered to be their property." and "Subjugate: To take control of people or a place by using force and make the people obey." Fig. 9.7 caption "Adoration of the pillar of Sanchi Stūpa" (two lines, under the relief).
- "- Fig. 9.7. Adoration of the pillar" and "~ Slave: A person ... -> Fig. 9.7. Adoration of the pillar of Sanchi Stūpa Slave: A person ...": the caption is now complete, but the margin entry "Slave" is glued to the end of the caption (regression, page shows them far apart). Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 9
  - find: "Fig. 9.7. Adoration of the pillar of Sanchi Stūpa Slave: A person"
  - replace: "Fig. 9.7. Adoration of the pillar of Sanchi Stūpa\n\n> [caption] Slave: A person"
  - note: "margin glossary entry Slave landed on the Fig. 9.7 caption on page 198"
- Also "> [caption] Subjugate:" and its definition are two blocks, cosmetic (P2).

### chapter 9, printed page 205
- Page shows: LET'S EXPLORE, "Why Democracy Matters", then Table 9.2 with header Characteristics / Democracy / Dictatorship / Absolute Monarchy / Oligarchy, first row "Universal Adult Franchise: Yes, No, No, No", then four blank rows (Equality amongst citizens, Freedom of speech, Separation of powers, Wellbeing and Prosperity of all citizens). The sentence "You have learnt the basic characteristics ... role play ... in your classroom:" is NOT on this page, it starts the LET'S EXPLORE box at the top of printed page 206 (opened).
- "~ Characteristics Democracy Dictatorship Absolute Monarchy Oligarchy Universal Adult Franchise Yes No Equality ... -> ... Oligarchy Yes No Equality amongst citizens ... You have learnt ... role play ... classroom:" and "+ Universal Adult Franchise": the first-row label has been lifted out of the table into a "### Universal Adult Franchise" heading after the table, and the first lines of page 206's box are glued to the table text. The new text is worse than the old one. Verdict: extraction fault (one-off, P5).
  - snapshot: "live-2026-10-18", chapter: 9
  - find: "Characteristics Democracy Dictatorship Absolute Monarchy Oligarchy Yes No Equality amongst citizens Freedom of speech Separation of powers Wellbeing and Prosperity of all citizens You have learnt the basic characteristics of various forms of governments. Do a small role play of the various forms in your classroom:\n\n### Universal Adult Franchise"
  - replace: "Characteristics | Democracy | Dictatorship | Absolute Monarchy | Oligarchy\n\nUniversal Adult Franchise | Yes | No | No | No\n\nEquality amongst citizens | | | |\n\nFreedom of speech | | | |\n\nSeparation of powers | | | |\n\nWellbeing and Prosperity of all citizens | | | |\n\nYou have learnt the basic characteristics of various forms of governments. Do a small role play of the various forms in your classroom:"
  - note: "Table 9.2 on page 205 rebuilt, the box sentence belongs to the top of page 206 and stays below the table"
  - (the caption "Table 9.2 Characteristics of different forms of government" is under the table and must stay in place. Check where it falls in the Markdown.)

### chapter 9, printed page 208
- Page shows: exercise 5 table (S. No / Practice in the country / Type of Government): I. All citizens are treated equally before law, Dictatorship. II. The government refers to the religious leader for each and every decision it takes, Monarchy. III. After the queen's death, her son became the new king, Democracy. IV. The ruler is not bound to follow any Constitution. He makes all the decisions as per his choice, Theocracy. Exercise 6 table with Bhutan, Nepal, Bangladesh, South Africa, Brazil and an empty column.
- "~ S. No Practice in the country Type of Government I. -> S. No Practice in the country Type of Government", "+ I.", "- All citizens ... Dictatorship The government refers to the religious leader ...", "+ All citizens are treated equally before law Dictatorship", "+ The government refers to ...", "~ Democracy The ruler is not bound ... -> The ruler is not bound ...": all words are present and the OCR noise is gone, but the rows are in a scrambled order (the text of II and IV precedes its numeral, and "Dictatorship", "Monarchy", "Democracy", "Theocracy" are tied to neighbouring cells). Verdict: extraction fault (one-off, P5). The old text was no better. Exercise 6 table header became "### S. No Country Type of Government" (heading from a table header, cosmetic).
  - snapshot: "live-2026-10-18", chapter: 9
  - find: the block from "S. No Practice in the country Type of Government" down to "Theocracy" (about 14 lines)
  - replace: "S. No | Practice in the country | Type of Government\n\nI. | All citizens are treated equally before law | Dictatorship\n\nII. | The government refers to the religious leader for each and every decision it takes. | Monarchy\n\nIII. | After the queen’s death, her son became the new king. | Democracy\n\nIV. | The ruler is not bound to follow any Constitution. He makes all the decisions as per his choice. | Theocracy"
  - note: "exercise table on page 208, rows rebuilt from the page image (the printed pairing is as shown, not a correct matching)"

## Chapter 10, The Constitution of India: An Introduction

### chapter 10, printed page 215
- Page shows: caption "Fig. 10.4.1. Workings of the Constituent Assembly" under the photo.
- "+ Fig. 10.4.1. Workings of the Constituent Assembly": matches the page (it was missing before).

### chapter 10, printed page 217
- Page shows: caption "Fig. 10.5. This 'Declaration of the Rights of Man and of the Citizen', which focused on equality, liberty and justice for all, was formulated during the 1789 French Revolution. It helped the spread of such ideals in many parts of the world; many constitutions (including the French one) adopted or adapted its values and principles."
- "+ adopted or adapted its values and principles.": the text is all present, but the caption is cut into three blocks (P2). Verdict: extraction fault (one-off, cosmetic).
  - snapshot: "live-2026-10-18", chapter: 10
  - find: "in many parts of the world;\n\n> [caption] many constitutions (including the French one)\n\n> [caption] adopted or adapted its values and principles."
  - replace: "in many parts of the world; many constitutions (including the French one) adopted or adapted its values and principles."
  - note: "Fig. 10.5 caption wrapped around the photo on page 217"

### chapter 10, printed page 222
- Page shows: Fig. 10.14 diagram. Top, Fundamental Rights: four bullets (Right to Equality (Article 14. Equality before law), Right to Freedom (Article 21. Protection of life and personal liberty), Right against Exploitation, Article 21-A. (Right to education)). Left, Directive Principles of State Policy: bullets Article 41, 44, 38, 48-A, 49, 47. Right, Fundamental Duties: a. to f. Caption "Fig 10.14. A glimpse of how the parts of the Constitution are organised".
- "~ Fig 10.14 ... are -> ... are organised": matches the page (caption complete).
- "~ • Article ... -> - Article ...", and the five other "•" to "-" pairs: the bullet sign is now a hyphen. Matches the page (bullets), cosmetic.
- Not fixed: the Directive Principles bullets and the Fundamental Duties list a. to f. are interleaved line by line ("- Article 38: Social, Political, and Economic Justice a. to abide by the Constitution and respect", "- Article 48-A: ... its ideals and institutions, the National Flag, and the National Anthem;", and so on), and the headings "Fundamental" / "Rights" / "Directive Principles of" / "State Policy" / "Fundamental" / "Duties" are split over separate headings. Verdict: extraction fault (one-off, P5).
  - snapshot: "live-2026-10-18", chapter: 10
  - find: the table blocks from "> [table] - Article 41: Welfare Government" to "> [table] f. if a parent or guardian, ..." (every block that holds an "Article" line or an "a." to "f." item)
  - replace: "- Article 41: Welfare Government\n\n- Article 44: Uniform Civil Code\n\n- Article 38: Social, Political, and Economic Justice\n\n- Article 48-A: Environment and Wildlife Protection\n\n- Article 49: Protection of monuments, places, and objects of national importance\n\n- Article 47: Nutrition, standard of living, and public health\n\nFundamental Duties\n\na. to abide by the Constitution and respect its ideals and institutions, the National Flag, and the National Anthem;\n\nb. to defend the country and render national service when called upon to do so;\n\nc. to value and preserve the rich heritage of our composite culture;\n\nd. to protect and improve the natural environment including forests, lakes, rivers and wild life, and to have compassion for living creatures;\n\ne. to strive towards excellence in all spheres of individual and collective activity so that the nation constantly rises to higher levels of endeavour and achievement;\n\nf. if a parent or guardian, to provide opportunities for education to his or her child or, as the case may be, ward between the age of six and fourteen years;"
  - note: "Fig. 10.14 on page 222, left and right columns had been read line by line across each other"

### chapter 10, printed page 225
- Page shows: the Preamble scroll, in a framed box "THE CONSTITUTION OF INDIA / PREAMBLE / WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a [SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC] and to secure to all its citizens: JUSTICE, social, economic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and of opportunity; and to promote among them all FRATERNITY assuring the dignity of the individual and the [unity and integrity of the Nation]; IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949 do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION." with two footnotes (Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for "Sovereign Democratic Republic" (w.e.f. 3.1.1977) and for "Unity of the Nation" (w.e.f. 3.1.1977)). Left and right margins carry the notes WE THE PEOPLE OF INDIA, SOVEREIGN, SOCIALIST, SECULAR, REPUBLIC, JUSTICE, LIBERTY, EQUALITY, DEMOCRATIC, FRATERNITY. Caption "Fig. 10.16. Preamble of the Indian Constitution".
- "~ JPLE constitute India intc CIALIST SECULAR INDIA, WE, ... -> WE, solemnly resolved to o constitute India into os!, OVEREIGN SO OCIALIST SECULAR DEMO OCRATIC REPUBLIC and to to all i...", "- INSTITUTIC INDIA", "- THE C", "- PEC", "- and", "- PREAMBLE having", "+ THE CO ONSTITUTIC NC INDIA", "+ THE PEO OPLE", "+ OF", "+ OF INDIA, having", "+ PREAMBLE", "+ SECULAR Subs. by the Con for ...": the page is still not right. The new text is a little closer, but the Preamble is OCR noise ("o constitute", "os!, OVEREIGN SO OCIALIST", "DEMO OCRATIC", "ADO OPT", "CO ONSTITUTIO ON", "to to all its citizens" with "secure" lost), it is run together with the LIBERTY, SECULAR and FRATERNITY margin notes, and the two footnotes are garbled ("Subs. by the Con for "Covereion De n (Forty-se in Denhlir ..."). The caption "Fig. 10.16. Preamble of the Indian Constitution" is LOST (nothing in the file matches it). The Preamble words ARE on the page. Verdict: extraction fault (one-off, most serious in the chapter, OCR of outlined type, P6).
- Fix: replace the three caption blocks "THE CO ONSTITUTIC NC INDIA" / "OF" / "PREAMBLE" / "OF INDIA, having" / "THE PEO OPLE" and the big "WE, solemnly resolved ..." block with:
  - snapshot: "live-2026-10-18", chapter: 10
  - replace: "THE CONSTITUTION OF INDIA\n\nPREAMBLE\n\nWE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a [SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC] and to secure to all its citizens: JUSTICE, social, economic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and of opportunity; and to promote among them all FRATERNITY assuring the dignity of the individual and the [unity and integrity of the Nation]; IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949 do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION.\n\n1. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Sovereign Democratic Republic\" (w.e.f. 3.1.1977)\n\n2. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Unity of the Nation\" (w.e.f. 3.1.1977)\n\nLIBERTY There are no unreasonable restrictions on the citizens in what they think, how they wish to express their thoughts and the way they wish follow up their thoughts in action.\n\nSECULAR Citizens have complete freedom to follow any religion. But there is no official religion. Government treats all religious beliefs and practices with equal respect.\n\nFRATERNITY All of us should behave as if we are members of the same family. No one should treat a fellow citizen as inferior.\n\n> [caption] Fig. 10.16. Preamble of the Indian Constitution"
  - note: "Preamble box on page 225 read from the page image, the outlined type was OCR noise and the margin notes were run into it"
  - (the "freedom to follow any religion..." caption at the end of the page belongs to SECULAR and should be removed in the same entry. Write the find against the exact blocks of the Markdown.)
- Pattern P6 (outlined/bold display type OCR noise): ch10 p225, and the same Preamble page in the prelims (see Prelims).

## Chapter 11, From Barter to Money

### chapter 11, printed page 246
- "- XN aN yN": pencil doodle on a Noodles page. Not viewed individually. The text of the page is only the heading "## Noodles" (P4). Garbage correctly gone.

## Chapter 12, Understanding Markets

### chapter 12, printed page 256
- Page shows: Fig. 12.10, a world map with two call-out lists (India's exports 1 to 5, India's imports 1 to 6), country and ocean labels (North America, South America, Europe, West Asia, Africa, India, South East Asia, Atlantic, Pacific and Indian Ocean), scale bar 0/1,400/2,800/5,600 K.M., and the side tags "India's exports and imports around the world", "India's exports:", "India's imports:".
- "- ef 8 CREE tf : Atlantic Ocean iy CT ...", "- eal": OCR noise from the map, gone. Verdict: matches (nothing lost).
- "+ Eur ica Atlantic Ocean West Asia Soutl outn An 5.", "+ Eurc Europe", "+ Europe", "+ Middle-East", "+ West", "+ West Asia Ind sia South East Asia Indian Ocean ... 6.": map label noise in caption blocks (P3). "Middle-East" is not on the page. The call-out lists are interleaved with their numbers ("North America: Outsourced services like software 1.", "South America: Chemical products 2.") and the numbers are repeated as separate "1." to "6." blocks. All words of the lists are present (matches the page, order messy). Verdict: extraction fault (rule P3), cosmetic.
- Fix: P3. One-off deletions:
  - snapshot: "live-2026-10-18", chapter: 12, find: "> [caption] Eurc Europe\n\n", replace: "", note: "map label noise on page 256"
  - same for "> [caption] Eur ica Atlantic Ocean West Asia Soutl outn An 5.\n\n" and "> [caption] Middle-East\n\n" (not printed on the map).

### chapter 12, printed page 257
- Page shows: the flow diagram Fig. 12.11 "Movement of Physical Goods in Markets": Inputs/Raw Materials, purchased by, Producers, manufacture & converted into, Finished Goods, go to, Wholesalers, reach, Warehouses & Distributors, send to, Mandis / Wholesale Markets, Retailers, Consumers. Then LET'S EXPLORE "Observe the diagram and describe the flow of goods from the manufacturer / producer to the consumer. What is the role of the wholesaler and the retailer in the flow?", then the paragraph that wraps round the Fig. 12.12 photo ("... In the case of perishables, the warehouses [may also have cold storage facilities. They are then brought to markets called mandīs.]"). Caption "Fig. 12.12. Cold storage facility for vegetables".
- "~ Movement of Physical Goods in Markets TT cum ff) Finished -> Movement of Physical Goods in Markets", "~ La send to -> send to", "~ Mandis / Se Wholesale -> Mandis / Wholesale", "- Warehouses & Se Sy Wholesalers", "- com", "~ ehObserve the diagram -> Observe the diagram": all the OCR noise is gone and the words match the page. Matches.
- "~ In the case of perishables, the warehouses Fig. 12.12. Cold storage facility for vegetables may also have cold s torage facilities. -> In the case of perishables, the warehouses may also have cold s torage facilities." and "+ Fig. 12.12. Cold storage facility for vegetables": the caption is no longer in the middle of the sentence. Matches the page. The words "cold s torage" carry a stray gap (not visible on the page image because the rest of the line sits beyond the photo), cosmetic, probably a hidden space character.
- "+ Finished", "+ Wholesalers Warehouses &": the boxes of Fig. 12.11 are loose table blocks in the wrong order (P5, cosmetic). All words of the diagram are present.

### chapter 12, printed page 261
- Page shows: the sentence "This helps maintain the stock of products with the manufacturers and ensures an uninterrupted supply of products to the end consumers." as the end of the first paragraph, then Fig. 12.23 (cotton map: Surendranagar, Jamnagar, Bhavnagar, Amreli, Surat, Amravati, Akola, Nagpur, Wardha, Yavatmal, Adilabad, scale, legend "Production By District 2017-2020 Metric tons: <10,000 Low, 10,000-75,000 Medium, >75,000 High") and Fig. 12.24 "Surat City Map" (legend Port, Airport, Railway, Road, River, Surat City, Textile Market).
- "- This helps maintain the stock ... vs Cc, er, pes pe fos ' a" / "+ This helps maintain the stock ... end consumers.": the paragraph end is clean now. Matches the page.
- "- Adilabad", "- Akola", "- Amreli Surat Amravati", "- Bhavnagar", "- Jamnagar", "- Nagpur Wardha", "- Yavatmal", "- Surendranagar", "- 0 100 200 50 km", "- Production By District 2017 -2020 Metric tons" and "+ Surendranagar Surend gal jar Bha Ar Surat Jamnagar Bhavnagar our Amreli ...": the district labels moved into one jumbled block (P3, contains noise like "Surend gal jar Bha Ar", "AkolaAmrava Akola"). No prose lost.
- "~ Fig. 12.23. Supply of raw cotton ... Surat Port River Surat City Textile Market Railway ... -> 80E Fig. 12.23. Supply of raw cotton from surrounding cotton clusters to Surat 70°E 75°E 80°E Port River Surat City Textile Market Railway Road Airport 0 5 10 2.5 km": the caption is now glued with the axis ticks and the legend of the next map (regression, P3). The caption of Fig. 12.24, "Fig. 12.24. Surat City Map", is LOST (no line in the file, nor in the committed text). Verdict: extraction fault (one-off).
  - snapshot: "live-2026-10-18", chapter: 12
  - find: "> [caption] 80E Fig. 12.23. Supply of raw cotton from surrounding cotton clusters to Surat 70°E 75°E 80°E Port River Surat City Textile Market Railway Road Airport 0 5 10 2.5 km"
  - replace: "> [caption] Fig. 12.23. Supply of raw cotton from surrounding cotton clusters to Surat\n\n> [caption] Fig. 12.24. Surat City Map"
  - note: "axis ticks and legend of Fig. 12.24 were glued into the Fig. 12.23 caption on page 261, and the Fig. 12.24 caption is missing from the text layer"

### chapter 12, printed page 262
- Page shows: the LET'S EXPLORE box "Ask your nearest retailer about a product, its place of origin, and the chain of suppliers in the process of the product reaching the shop. Trace this using a flow chart like Fig. 12.11 and share it in class." and caption "Fig. 12.25. A wholesaler's warehouse of fabric".
- "+ Ask your nearest retailer ... reaching the shop.": the first sentence of the box is now its own block, followed by the sentence "Trace this using ...". Matches the page (it was missing before, the box now reads in full).

### chapter 12, printed page 264
- Page shows: caption "Fig. 12.26. Ima Keithal of Imphal" under the two photos.
- "+ Fig. 12.26. Ima Keithal of Imphal": the page has "Ima Keithal" and the text agrees (an earlier "Ima" fault is fixed). The change list line shows "Fig. 12.26. Ima Keithal of Imphal" with "Ima", matches the page.

## Prelims (part1-prelims.md, no printed pages, pdf pages cited)

### prelims, pdf page 1 (title page)
- Page shows: the title, "Social Science Textbook for Grade 7 | Part 1", a QR code, the NCERT logo, and the line "NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING" (plus its Hindi version) printed as clean type.
- "- sta 3far fae sq sine atest fstatorT IONAL COUNCI EDUCAI IONAL RESEARCH AND ...", "- Uke Rave" / "+ TRUE TRAIN", "+ NATI TIONAL COUNCIL", "+ F EDUCATI TIONAL RESEARCH AND T", "+ OF" (and "+ T"): the Devanagari line is gone but the English line is still OCR noise in three captions, plus the stray "TRUE TRAIN". Verdict: extraction fault (one-off), P6.
  - snapshot: "live-2026-10-18", chapter: (prelims, use the chapter value the override file uses for part 1 prelims, i.e. 0)
  - find: "> [caption] TRUE TRAIN\n\n> [caption] NATI TIONAL COUNCIL\n\n> [caption] F EDUCATI TIONAL RESEARCH AND T"
  - replace: "> [caption] NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING"
  - note: "title page footer line read from the page image, the extractor read noise"
  - (the exact text of the third caption is cut in the change list. Check the Markdown before pasting, and the "OF" block that is placed later in the file.)

### prelims, pdf page 12 (Fundamental Rights list)
- Page shows: "CONSTITUTION OF INDIA / Part III (Articles 12 - 35) / guarantees these Fundamental Rights", six groups each with a bold group title and bullets (Right to Equality, Right to Freedom, Right against Exploitation, Right to Freedom of Religion, Cultural and Educational Rights, Right to Constitutional Remedies).
- "- before law and equal protection of laws; ...", "+ before law and equal protection of laws;" and the matching pairs for irrespective..., by abolition..., for prohibition..., freedom ..., of expression..., of certain protections..., of protection..., of free and compulsory education..., for protection of interests..., for minorities..., "~ • by issuance ... -> by issuance ...", "- (Forty-seco ef.", "- CCl ...": each bullet is now its own line ("- ..." list item) and reads the same as the page. The old text had several bullets run together. Matches the page.

### prelims, pdf pages 15 and 16 (Textbook Development Team)
- Page 15 shows the names from Michel Danino to Pawan Kumar (heading "Contributors"). Page 16 shows Payel Mukherjee to Surendra C Thakurdesai, then "Member Coordinators" (Seema Shukla Ojha, M V Srinivasan), then "Reviewers" (Aditi Mishra, ..., Aparna Pandey, and more on the following page).
- "~ Mrinmoyee Ray, ... Nabajyoti Deka ... -> same with a heading change" and "~ Aditi Mishra, Director Principal, Delhi Public School, Gurgaon; and Teachers: ... ": the names are the same as the page. The change is the "Member Coordinators" heading now being a "###" heading placed before M V Srinivasan. But page 15 of the text carries the names of page 16 as well, and "Seema Shukla Ojha, Professor of History, ... CAG (Social Science)" ends the Contributors block (before the Member Coordinators heading), while on the page she is the first Member Coordinator. Verdict: extraction fault (one-off), the sentence is on the page under a different heading.
  - snapshot: "live-2026-10-18", chapter: prelims
  - find: " Seema Shukla Ojha, Professor of History, Department of Education in Social Science, NCERT; CAG (Social Science)\n\n<!-- pdf page 16 -->\n\n### Member Coordinators\n\n"
  - replace: "\n\n<!-- pdf page 16 -->\n\n### Member Coordinators\n\nSeema Shukla Ojha, Professor of History, Department of Education in Social Science, NCERT; CAG (Social Science)\n\n"
  - note: "Seema Shukla Ojha is the first Member Coordinator on page 16"
  - (the page marker positions between 15 and 16 are also off by one block. The names Payel Mukherjee to Surendra C Thakurdesai are on page 16 of the PDF.)

### prelims, pdf page 18 (Preamble)
- Page shows: the Preamble in a framed box: "THE CONSTITUTION OF INDIA / PREAMBLE / WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a [SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC] and to secure to all its citizens: JUSTICE, social, economic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and of opportunity; and to promote among them all FRATERNITY assuring the dignity of the individual and the [unity and integrity of the Nation]; IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949 do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION." and two footnotes.
- "- INSTITUTI INDIA THE Ct having", "- PE(", "- PLE constitute India intc ICIALIST SECULAR ...", "- CCl political; ...", "- Co", "- Subs. by the Cc "Unity of the Natio ef.", "- IN", "+ THE CO ONSTITUTIO ON INDIA", "+ PREAMBLE" (table), "+ OF INDIA, having", "+ THE PEC OPLE", "+ WE, solemnly resolved to constitute India into 'ISC OVEREIGN SC OCIALIST SECULAR DEMC OCRATIC REPUBLIC ...", "+ JUSTICE,", "+ SO", "+ J overeign Dem O. Subs. by the Cor n (Forty-secor D nocratic Republic" ( n (Forty-secor w.e.f. 3.1.1977)", "+ w.e.f. 3.1.1977)", "+ OF": the new text is closer than the old one (the words "to secure" and "JUSTICE" are back) but is still OCR noise of the outlined type ("DEMC OCRATIC", "ADO OPT", "CO ONSTITUTIC ON", "ocial, eco ono omic"), with "JUSTICE," split from "social, economic and political" and "SO" a stray. The footnotes are garbled. Verdict: extraction fault (one-off, P6). The words are on the page.
  - snapshot: "live-2026-10-18", chapter: prelims
  - replace: the same clean Preamble block as under chapter 10 page 225 (without the margin notes), as one block, with the footnotes "1. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Sovereign Democratic Republic\" (w.e.f. 3.1.1977)" and "2. Subs. by the Constitution (Forty-second Amendment) Act, 1976, Sec. 2, for \"Unity of the Nation\" (w.e.f. 3.1.1977)".
  - note: "Preamble on the pdf page 18 of the prelims read from the page image"

## Summary

Part 1 of exploring-society-7, edition live-2026-10-18, 57 page entries across the 12 chapters and the prelims. Counts are per page entry, and an entry with both a fault and a correct part is counted under the fault.

- Matches the page (every changed sentence there is now right): 16. Pages 3, 15 (ch1), 28, 40 (ch2), 52, 59 (ch3), 163 (ch7), 169, 171 (ch8), 187, 191, 197 (ch9), 215 (ch10), 262, 264 (ch12), and prelims pdf page 12.
- Extraction fault, rule (a pattern, cosmetic or low risk, no lost words): 14. Pages ch1 7, 10, 18, 26, ch3 (map labels on 52), ch6 119, 130, 139, ch7 146, 152, ch12 256, 257, 261.
- Extraction fault, one-off (needs an override): 22. ch1 6, 11, 13, ch2 31, ch5 88, 98, 109, 110, ch6 120, 136, 138, ch8 169 (spaces only), ch9 192, 195, 198, 205, 208, ch10 217, 222, 225, prelims pdf 1, 15 and 16, 18.
- Not viewed individually: 5, the Noodles pages 44, 82, 116, 144 and 246 (judged by the Noodles page 26 that was opened, the removed lines are the pencil doodle). Page 26 and page 40 and all other pages were opened.

Lost text that is on the page (the most serious findings): ch2 p31 captions of Fig. 2.4.3 "In winter, coconut oil turns solid." and Fig. 2.4.4 "Curd takes longer" (only "to set in cold weather." is left), ch5 p109 "Sarnath pillar." at the end of the Fig. 5.20 caption, ch6 p136 "of King Kaṇiṣhka" attached to the wrong caption, ch10 p225 caption "Fig. 10.16. Preamble of the Indian Constitution", ch12 p261 caption "Fig. 12.24. Surat City Map", prelims Seema Shukla Ojha under the wrong heading. Overrides for all of them are in the entries above.

Regressions caused by the new rules (worse than the committed text): axis tick labels glued to the front of a Fig. caption (ch6 p119, 138, ch7 p152, ch12 p261), "Błack Sea" (ch6 p138), "Slave:" glued to the Fig. 9.7 caption (ch9 p198), "Universal Adult Franchise" pulled out of Table 9.2 and the first lines of the next page's box glued to it (ch9 p205), the margin-note glue of "of King Kaṇiṣhka" (ch6 p136).

The three remaining patterns that matter most:
1. P3, map and diagram labels (ch6 p119/130/138/139, ch7 p146/152, ch12 p256/261, ch5 p88/96, ch6 p120): axis ticks (60E, 8°N and the like) come out as stray paragraphs, get glued to the front of the "Fig." caption, and label words are interleaved line by line across boxes. Fix in the extractor: drop tick-only blocks and never merge them into a caption, and read call-out boxes one box at a time.
2. P5 flattened tables and diagrams (ch9 p195/205/208, ch10 p222, ch12 p257): cells are listed in column order, row labels are separated from their rows, and a neighbouring box can be glued to the table. Words are present, but a reader cannot tell which row a cell belongs to.
3. P2/P1 captions and badges next to photos (ch1 p6/7/10/11/13/18, ch5 p98/110, ch6 p137, ch10 p217, ch8 p169): the captions of side-by-side photos are merged and interleaved by line, a caption is split into several blocks, and the photo number badges 1 to 7 become stray one-line paragraphs. Fix by grouping lines per caption block by x-position, and by dropping badge digits placed on a picture.
Next in line, P6 outlined or display type (ch10 p225, prelims pdf 1 and 18) still reads as OCR noise and needs the override rebuild, and P4 blank Noodles pages give inconsistent text (nothing, the heading only, or the footnote only).
