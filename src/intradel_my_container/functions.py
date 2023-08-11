import re
from datetime import datetime


def cleanup(string: str) -> str:
    to_return: str = re.sub(r"\s+", " ", string.strip())
    to_return = re.sub(" , ", ", ", to_return)
    return to_return


def find_date(string: str) -> datetime:
    search = re.search(r"(\d\d-\d\d-\d\d\d\d)", string)
    return datetime.strptime(search.group(1), "%d-%m-%Y")


def extract_number(string: str) -> int:
    search = re.search(r"(\d*)", string)
    return int(search.group(1))
