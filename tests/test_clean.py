from ncert_diff import clean


def test_join_lines_keeps_real_hyphens():
    # The PDFs carry no automatic hyphenation, so a line-end hyphen is part of the word.
    assert clean.join_lines(["great-great-", "grandfather of Babur"]) == "great-great-grandfather of Babur"
    assert clean.join_lines(["modern-", "day Jaipur"]) == "modern-day Jaipur"
    assert clean.join_lines(["(1526-", "1530)"]) == "(1526-1530)"


def test_join_lines_en_dash_keeps_spaces():
    assert clean.join_lines(["a system of ethics –", "honesty, justice"]) == "a system of ethics – honesty, justice"


def test_broken_hyphen_inside_a_line_is_closed():
    assert clean.join_lines(["modern- day Jaipur"]) == "modern-day Jaipur"


def test_collapse_repeats_handles_shadow_headings():
    assert clean.collapse_repeats("Let’s recall Let’s recall Let’s recall Let’s recall") == "Let’s recall"
    assert clean.collapse_repeats("Let’s recall Let’s recall") == "Let’s recall Let’s recall"  # twice is not a shadow
    assert clean.collapse_repeats("a normal sentence") == "a normal sentence"


def test_continues():
    assert clean.continues("On the other hand, the Mughals were", "proud of their Timurid ancestry.")
    assert clean.continues("Mughal intervention in the succession of the Rathor Rajputs of", "Marwar led to rebellion.")
    assert not clean.continues("This sentence ends here.", "Another begins.")
    assert not clean.continues("Table 1", "Major campaigns")  # short label, capitalised follower
    assert clean.continues("areas cultivated for a 10-year period, 1570-", "1580. On the basis of this data")
    assert not clean.continues("Rathor Rajput Mewar Nur Jahan rank subadar Jahangir", "2. Fill in the blanks:")
    assert not clean.continues("Rathor Rajput Mewar Nur Jahan rank subadar Jahangir", "(a) The capital of Mirza Hakim")
    assert not clean.continues("", "x")


def test_merge_paragraphs():
    assert clean.merge_paragraphs("great-", "grandfather") == "great-grandfather"
    assert clean.merge_paragraphs("ethics –", "honesty") == "ethics – honesty"
    assert clean.merge_paragraphs("were", "proud") == "were proud"


def test_slugify():
    assert clean.slugify("THE CREATION OF AN EMPIRE: The Mughal Dynasty") == "the-creation-of-an-empire-the-mughal-dynasty"
    assert clean.slugify("the mughals (16th TO 17th CENTURY)") == "the-mughals-16th-to-17th-century"
    assert clean.slugify("") == "untitled"


def test_paragraph_does_not_continue_after_a_bare_number():
    from ncert_diff.clean import continues
    assert not continues("Registered Unrecognised Parties 16 Independents 3 Grand Total 543", "Once elected, these candidates become MPs.")
    assert continues("The Lok Sabha has 543 members, of whom a majority must", "support the government.")
    assert continues("The empire was founded in the year 1526 by a prince named", "Babur, who came from Central Asia.")
    assert continues("The empire was founded in 1526", "by a prince from Central Asia.")


def test_glued_list_label_gets_its_space():
    assert clean.join_lines(["1.that one religious community", "does not dominate another;"]) == "1. that one religious community does not dominate another;"
    assert clean.join_lines(["4.Within the city"]) == "4. Within the city"
    assert clean.join_lines(["1.5 million people"]) == "1.5 million people"


def test_rupee_backtick_becomes_the_rupee_sign():
    assert clean.join_lines(["fine of `20,000 to `50,000 and", "he spent ` _______ for"]) == "fine of ₹20,000 to ₹50,000 and he spent ₹ _______ for"


def test_list_item_does_not_run_into_the_next_paragraph():
    assert not clean.continues("- The decline of crafts and growth of industries", "On the basis of what you have read")
    assert clean.continues("- The decline of crafts and growth of", "industries in the nineteenth century")


def test_no_space_before_a_closing_bracket():
    from ncert_diff.clean import normalise_text
    assert normalise_text("an example of a prashasti ) praising the") == "an example of a prashasti) praising the"
    assert normalise_text("(see Chapter 2)") == "(see Chapter 2)"
    assert normalise_text("a criminal court ( faujdari adalat ) and") == "a criminal court (faujdari adalat) and"
