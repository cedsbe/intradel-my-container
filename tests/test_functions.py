from datetime import datetime

from intradel_my_container.functions import cleanup, extract_number, find_date

# Cleanup Function
# region cleanup


def test_cleanup_one_word():
    clean: str = cleanup("oneword")
    assert clean == "oneword"


def test_cleanup_one_sentence():
    clean: str = cleanup("One sentence to clean.")
    assert clean == "One sentence to clean."


def test_cleanup_one_sentence_extra_spaces():
    clean: str = cleanup("   One   sentence   to  clean.   ")
    assert clean == "One sentence to clean."


def test_cleanup_one_sentence_extra_spaces_and_tabs():
    clean: str = cleanup("One\t \tsentence   to  clean.")
    assert clean == "One sentence to clean."


def test_cleanup_one_sentence_extra_spaces_tabs_and_lines():
    clean: str = cleanup("  \t  One\t \tsentence  \n\r to \r\n    clean.  \r\n  ")
    assert clean == "One sentence to clean."


# endregion cleanup

# find_date Function
# region find_date


def test_find_date():
    date: datetime = find_date("01-02-2022")
    assert date == datetime.strptime("01-02-2022", "%d-%m-%Y")


def test_find_date_in_string():
    date: datetime = find_date("Find this: 01-02-2022")
    assert date == datetime.strptime("01-02-2022", "%d-%m-%Y")


def test_find_date_cannot():
    date: datetime = find_date("Damn, there is no date here")
    assert date == datetime.strptime("01-01-1970", "%d-%m-%Y")


def test_find_date_wrong_format():
    date: datetime = find_date("Damn, wrong format: 2023-03-25")
    assert date == datetime.strptime("01-01-1970", "%d-%m-%Y")


# endregion find_date

# extract_number Function
# region extract_number


def test_extract_number():
    number: int = extract_number("123")
    assert number == 123


def test_extract_number_in_sentence():
    number: int = extract_number("Can you find 123 in this sentence?")
    assert number == 123


def test_extract_number_no_number():
    number: int = extract_number("There is no number in this sentence!")
    assert number == -10000


# endregion extract_number
