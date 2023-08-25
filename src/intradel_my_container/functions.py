"""Centralize helper functions."""
import re
from datetime import datetime
from typing import Dict, List

from bs4 import Tag


def cleanup(string: str) -> str:
    """
    Clean up the input string by removing extra whitespace, tabs, and newlines.

    Parameters:
    ----------
    string : str
        The input string to be cleaned up.

    Returns:
    -------
    str
        The cleaned up string.
    """
    to_return: str = re.sub("\t+|\n+|\r+", " ", string.strip())
    to_return = re.sub(r"\s+", " ", to_return.strip())
    to_return = re.sub(" , ", ", ", to_return.strip())
    return to_return


def find_date(string: str) -> datetime:
    """
    Find a date string in the input using regular expressions and return it as a datetime object.

    Parameters:
    ----------
    string : str
        The input string where the date is to be found.

    Returns:
    -------
    datetime
        A datetime object representing the extracted date.
        If no date is found, returns January 1, 1970.
    """

    search = re.search(r"(\d\d-\d\d-\d\d\d\d)", string)
    if search is None:
        print("Cannot extract date. Return 01-01-1970")
        return datetime.strptime("01-01-1970", "%d-%m-%Y")
    else:
        return datetime.strptime(search.group(1), "%d-%m-%Y")


def extract_number(string: str) -> int:
    """
    Extract an integer from the input string using regular expressions.

    Parameters:
    ----------
    string : str
        The input string from which the integer is to be extracted.

    Returns:
    -------
    int
        The extracted integer. If no integer is found, returns -10000.
    """

    search = re.search(r"(\d+)", string)

    if search is None:
        print("Cannot extract value. Return -10000")
        return -10_000
    else:
        result = search.group(1)
        return int(result)


def p_to_dictionary(content: Tag) -> Dict[str, str]:
    """
    Convert the content of HTML 'p' tags into a dictionary of key-value pairs.

    Parameters:
    ----------
    content : Tag
        The HTML 'Tag' object containing the 'p' tags to be processed.

    Returns:
    -------
    Dict[str, str]
        A dictionary containing key-value pairs extracted from the 'p' tags.
        Keys are cleaned up and values are cleaned up and stored as strings.
    """

    p_dic: Dict[str, str] = {}

    for p_tag in content.find_all("p"):
        splitted_text: List[str] = p_tag.text.split(":")
        if len(splitted_text) == 2:
            key = cleanup(splitted_text[0])
            value = cleanup(splitted_text[1])
            p_dic[key] = value

    return p_dic
