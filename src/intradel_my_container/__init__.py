import re
from abc import ABC
from datetime import datetime
from typing import Any, Dict, List, Union

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from intradel_my_container.const import *
from intradel_my_container.functions import cleanup, extract_number, find_date

from . import const


class Pickup:
    date: datetime
    kilograms: float

    def __init__(self, date: datetime, kilograms: float) -> None:
        self.date = date
        self.kilograms = kilograms


class Material:
    name: str
    quantity: float
    unit: str

    def __init__(self, name: str, quantity: float, unit: str) -> None:
        self.name = name.removesuffix(" ")
        self.quantity = quantity
        self.unit = unit.removesuffix(" ")


class Dropout:
    date: datetime
    parc: str
    materials: List[Material]
    _raw_materials: str

    def _create_material(self, raw_material: str) -> List[Material]:
        raw_material = cleanup(raw_material)
        split_materials = raw_material.split(",")
        list_material: List[Material] = []
        for material in split_materials:
            search = re.search(r"(.*)\((\d+\.\d+)\s(.*)\)", material)
            if search is not None:
                list_material.append(
                    Material(
                        name=search.group(1),
                        quantity=float(search.group(2)),
                        unit=search.group(3),
                    )
                )
        return list_material

    def __init__(self, date: datetime, parc: str, materials: str) -> None:
        self.date = date
        self.parc = parc
        self.materials = self._create_material(raw_material=materials)
        self._raw_materials = materials


def p_to_dictionnary(content: Tag) -> Dict[str, str]:
    p_dic: Dict[str, str] = {}

    for p in content.find_all("p"):
        splitted_text: List = p.text.split(":")
        if len(splitted_text) == 2:
            key = cleanup(splitted_text[0])
            value = cleanup(splitted_text[1])
            p_dic[key] = value

    return p_dic


class Informations:
    name: str
    category: str
    address: str
    actif: datetime

    def __init__(self, content: Tag) -> None:
        dict_my_informations: Dict[str, str] = p_to_dictionnary(content)

        self.name = dict_my_informations[INTRADEL_INFO_NAME]
        self.category = dict_my_informations[INTRADEL_INFO_CATEGORY]
        self.address = dict_my_informations[INTRADEL_INFO_ADDRESS]
        self.actif = find_date(dict_my_informations[INTRADEL_INFO_ACTIF])


class TrashBin(ABC):
    volume: int
    chip_number: str
    status: str
    since: datetime
    pickups: List[Pickup]

    def get_pickups(self, content: Tag) -> List[Pickup]:
        pickup_list: List[Pickup] = []
        all_tr_in_tbody_table: Any = []

        next_table_results = content.find_next("table", id="table_results")
        if isinstance(next_table_results, Tag):
            next_tbody = next_table_results.find_next("tbody")
        if isinstance(next_tbody, Tag):
            all_tr_in_tbody_table = next_tbody.find_all("tr")

        for table_line in all_tr_in_tbody_table:
            pickup_entry = table_line.find_all("td")
            pickup_list.append(
                Pickup(
                    date=find_date(pickup_entry[0].text),
                    kilograms=float(pickup_entry[2].text),
                )
            )

        return pickup_list

    def total_collects(self) -> int:
        return len(self.pickups)

    def total_collects_per_year(self) -> Dict[str, int]:
        per_year_dict: Dict[str, int] = {}
        for pickup in self.pickups:
            year: str = str(pickup.date.year)
            if year in per_year_dict.keys():
                per_year_dict[year] = per_year_dict[year] + 1
            else:
                per_year_dict[year] = 1
        return per_year_dict

    def total_kilograms(self) -> float:
        total: float = 0
        for pickup in self.pickups:
            total = total + pickup.kilograms
        return total

    def total_kilograms_per_year(self) -> Dict[str, float]:
        per_year_dict: Dict[str, float] = {}
        for pickup in self.pickups:
            year: str = str(pickup.date.year)
            if year in per_year_dict.keys():
                per_year_dict[year] = per_year_dict[year] + pickup.kilograms
            else:
                per_year_dict[year] = pickup.kilograms
        return per_year_dict


class Organic(TrashBin):
    def __init__(self, content: Tag) -> None:
        dict_organic: Dict[str, str] = p_to_dictionnary(content)

        self.volume = extract_number(dict_organic[INTRADEL_ORGANIC_VOLUME])
        self.chip_number = dict_organic[INTRADEL_ORGANIC_CHIP_NUMBER]
        self.status = dict_organic[INTRADEL_ORGANIC_STATUS]
        self.since = find_date(dict_organic[INTRADEL_ORGANIC_SINCE])
        self.pickups = self.get_pickups(content)


class Residual(TrashBin):
    def __init__(self, content: Tag) -> None:
        dict_residual: Dict[str, str] = p_to_dictionnary(content)

        self.volume = extract_number(dict_residual[INTRADEL_RESIDUAL_VOLUME])
        self.chip_number = dict_residual[INTRADEL_RESIDUAL_CHIP_NUMBER]
        self.status = dict_residual[INTRADEL_RESIDUAL_STATUS]
        self.since = find_date(dict_residual[INTRADEL_RESIDUAL_SINCE])
        self.pickups = []

        self.pickups = self.get_pickups(content)


class Recyparc:
    since: datetime
    dropout: List[Dropout]

    def get_dropouts(self, content: Tag) -> List[Dropout]:
        dropout_list: List[Dropout] = []
        all_tr_in_tbody_table: Any = []

        next_table_results = content.find_next("table", id="table_results")
        if isinstance(next_table_results, Tag):
            next_tbody = next_table_results.find_next("tbody")
        if isinstance(next_tbody, Tag):
            all_tr_in_tbody_table = next_tbody.find_all("tr")

        for table_line in all_tr_in_tbody_table:
            dropout_entry = table_line.find_all("td")
            dropout_list.append(
                Dropout(
                    date=find_date(dropout_entry[0].text),
                    parc=dropout_entry[1].text,
                    materials=dropout_entry[2].text,
                )
            )

        return dropout_list

    def __init__(self, content: Tag) -> None:
        dict_recyparc: Dict[str, str] = p_to_dictionnary(content)

        self.since = find_date(dict_recyparc[INTRADEL_RESIDUAL_SINCE])
        self.dropout = self.get_dropouts(content)


class IntradelMyContainer:
    _login: str
    _password: str
    _municipality: str
    my_informations: Informations
    organic: Organic
    residual: Residual
    recyparc: Recyparc
    start_date: datetime
    end_date: datetime
    _start_date_str: str
    _end_date_str: str

    def _get_page_content(
        self,
        login: str,
        password: str,
        municipality: str,
        start_date: Union[None, datetime] = None,
        end_date: Union[None, datetime] = None,
    ) -> bytes:
        if start_date is None:
            self.start_date = datetime.today().replace(month=1, day=1)
            self._start_date_str = self.start_date.strftime("%d-%m-%Y")
        else:
            self.start_date = start_date
            self._start_date_str = start_date.strftime("%d-%m-%Y")

        if end_date is None:
            self.end_date = datetime.today()
            self._end_date_str = self.end_date.strftime("%d-%m-%Y")
        else:
            self.end_date = end_date
            self._end_date_str = end_date.strftime("%d-%m-%Y")

        post_login: dict[str, str] = {
            "llogin": "YES",
            "login": login,
            "pass": password,
            "commune": municipality,
        }

        post_data: dict[str, str] = {
            "sdate": self._start_date_str,
            "edate": self._end_date_str,
        }

        session = requests.session()
        page = session.post(url=INTRADEL_URL_LOGIN, data=post_login)
        page = session.post(url=INTRADEL_URL_DATA, data=post_data)

        return page.content

    def __init__(
        self,
        login: str,
        password: str,
        municipality: str,
        start_date: Union[None, datetime] = None,
        end_date: Union[None, datetime] = None,
    ) -> None:
        self._login = login
        self._password = password
        self._municipality = municipality

        page_content: bytes = self._get_page_content(
            login=login,
            password=password,
            municipality=municipality,
            start_date=start_date,
            end_date=end_date,
        )

        soup: BeautifulSoup = BeautifulSoup(page_content, "html.parser")
        all_post__content: ResultSet[Any] = soup.find_all("div", class_="post__content")

        for content in all_post__content:
            if isinstance(content, Tag):
                h3 = content.find_next("h3")
                if h3 is not None:
                    match h3.text:
                        case const.INTRADEL_INFO_TITLE:
                            self.my_informations = Informations(content)
                        case const.INTRADEL_ORGANIC_TITLE:
                            self.organic = Organic(content)
                        case const.INTRADEL_RESIDUAL_TITLE:
                            self.residual = Residual(content)
                        case const.INTRADEL_RECYPARC_TITLE:
                            self.recyparc = Recyparc(content)
