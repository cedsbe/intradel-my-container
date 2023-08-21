import re
from datetime import datetime
from typing import Dict, List

from bs4 import Tag


def cleanup(string: str) -> str:
    to_return: str = re.sub("\t|\n|\r", "", string.strip())
    to_return = re.sub(r"\s+", " ", to_return.strip())
    to_return = re.sub(" , ", ", ", to_return.strip())
    return to_return


def find_date(string: str) -> datetime:
    search = re.search(r"(\d\d-\d\d-\d\d\d\d)", string)
    if search is None:
        print("Cannot extract date. Return 01-01-1970")
        return datetime.strptime("01-01-1970", "%d-%m-%Y")
    else:
        return datetime.strptime(search.group(1), "%d-%m-%Y")


def extract_number(string: str) -> int:
    search = re.search(r"(\d+)", string)

    if search is None:
        print("Cannot extract value. Return -10000")
        return -10_000
    else:
        result = search.group(1)
        return int(result)


def p_to_dictionnary(content: Tag) -> Dict[str, str]:
    p_dic: Dict[str, str] = {}

    for p in content.find_all("p"):
        splitted_text: List = p.text.split(":")
        if len(splitted_text) == 2:
            key = cleanup(splitted_text[0])
            value = cleanup(splitted_text[1])
            p_dic[key] = value

    return p_dic
