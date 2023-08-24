"""The core of the package. Provide the functionality to parse Intradel's website"""
import re
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from intradel_my_container.const import *
from intradel_my_container.functions import (
    cleanup,
    extract_number,
    find_date,
    p_to_dictionary,
)

from . import const


@dataclass
class Pickup:
    """
    Represents a pickup event.

    Attributes:
    ----------
    date : datetime
        The date of the pickup event.
    kilograms : float
        The weight of materials collected in kilograms.
    """

    date: datetime
    kilograms: float


@dataclass
class Material:
    """
    Represents a material with quantity and unit.

    Attributes:
    ----------
    name : str
        The name of the material.
    quantity : float
        The quantity of the material.
    unit : str
        The unit of measurement for the material's quantity.
    """

    name: str
    quantity: float
    unit: str

    def __post_init__(self):
        """
        Ensure strings are stripped a Material instance.
        """
        self.name = self.name.strip()
        self.unit = self.unit.strip()


class Dropout:
    """
    Represents a dropout event.

    Attributes:
    ----------
    date : datetime
        The date of the dropout event.
    parc : str
        The name of the parc associated with the dropout event.
    materials : List[Material]
        A list of Material instances representing the materials in the dropout event.
    _raw_materials : str
        The raw string of materials before processing.
    """

    date: datetime
    parc: str
    materials: List[Material]
    _raw_materials: str

    def _create_material(self, raw_material: str) -> List[Material]:
        """
        Parse a string to create a list of materials.

        Parameters:
        ----------
        raw_material : str
            The raw material string to parse.
        """
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
        """
        Initialize a Dropout instance.

        Parameters:
        ----------
        date : datetime
            The date of the dropout event.
        parc : str
            The name of the parc associated with the dropout event.
        materials : str
            A string containing materials data.
        """

        self.date = date
        self.parc = parc
        self.materials = self._create_material(raw_material=materials)
        self._raw_materials = materials


class Informations:
    """
    Represents information about an Intradel user.

    Attributes:
    ----------
    name : str
        The name of the Intradel user.
    category : str
        The category of the user.
    address : str
        The address of the user.
    actif : datetime
        The active date of the user.
    """

    name: str
    category: str
    address: str
    actif: datetime

    def __init__(self, content: Tag) -> None:
        """
        Initialize an Informations instance.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing information content.
        """

        dict_my_informations: Dict[str, str] = p_to_dictionary(content)

        self.name = dict_my_informations[INTRADEL_INFO_NAME]
        self.category = dict_my_informations[INTRADEL_INFO_CATEGORY]
        self.address = dict_my_informations[INTRADEL_INFO_ADDRESS]
        self.actif = find_date(dict_my_informations[INTRADEL_INFO_ACTIF])


class TrashBin(ABC):
    """
    Abstract base class representing a trash bin.

    Attributes:
    ----------
    volume : int
        The volume of the trash bin.
    chip_number : str
        The chip number of the trash bin.
    status : str
        The status of the trash bin.
    since : datetime
        The starting date of the trash bin's usage.
    pickups : List[Pickup]
        A list of Pickup instances representing pickup events associated with the trash bin.
    """

    volume: int
    chip_number: str
    status: str
    since: datetime
    pickups: List[Pickup]

    def get_pickups(self, content: Tag) -> List[Pickup]:
        """
        Retrieve a list of pickup events associated with the trash bin.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing trash bin content.

        Returns:
        -------
        List[Pickup]
            A list of Pickup instances representing pickup events associated with the trash bin.
        """

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
        """
        Calculate the total number of pickup events.

        Returns:
        -------
        int
            The total number of pickup events.
        """
        return len(self.pickups)

    def total_collects_per_year(self) -> Dict[str, int]:
        """
        Calculate the total number of pickup events per year.

        Returns:
        -------
        Dict[str, int]
            A dictionary with years as keys and the corresponding total pickup events as values.
        """

        per_year_dict: Dict[str, int] = {}
        for pickup in self.pickups:
            year: str = str(pickup.date.year)
            if year in per_year_dict:
                per_year_dict[year] = per_year_dict[year] + 1
            else:
                per_year_dict[year] = 1
        return per_year_dict

    def total_kilograms(self) -> float:
        """
        Calculate the total weight of materials collected.

        Returns:
        -------
        float
            The total weight of materials collected in kilograms.
        """

        total: float = 0
        for pickup in self.pickups:
            total = total + pickup.kilograms
        return total

    def total_kilograms_per_year(self) -> Dict[str, float]:
        """
        Calculate the total weight of materials collected per year.

        Returns:
        -------
        Dict[str, float]
            A dictionary with years as keys and the corresponding total weight of materials
            collected as values.
        """

        per_year_dict: Dict[str, float] = {}
        for pickup in self.pickups:
            year: str = str(pickup.date.year)
            if year in per_year_dict:
                per_year_dict[year] = per_year_dict[year] + pickup.kilograms
            else:
                per_year_dict[year] = pickup.kilograms
        return per_year_dict


class Organic(TrashBin):
    """
    Represents an organic waste trash bin.

    Inherits from TrashBin.

    Attributes:
    ----------
    (inherits attributes from TrashBin)
    """

    def __init__(self, content: Tag) -> None:
        """
        Initialize an Organic instance.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing organic waste content.
        """

        dict_organic: Dict[str, str] = p_to_dictionary(content)

        self.volume = extract_number(dict_organic[INTRADEL_ORGANIC_VOLUME])
        self.chip_number = dict_organic[INTRADEL_ORGANIC_CHIP_NUMBER]
        self.status = dict_organic[INTRADEL_ORGANIC_STATUS]
        self.since = find_date(dict_organic[INTRADEL_ORGANIC_SINCE])
        self.pickups = self.get_pickups(content)


class Residual(TrashBin):
    """
    Represents a residual waste trash bin.

    Inherits from TrashBin.

    Attributes:
    ----------
    (inherits attributes from TrashBin)
    """

    def __init__(self, content: Tag) -> None:
        """
        Initialize a Residual instance.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing residual waste content.
        """

        dict_residual: Dict[str, str] = p_to_dictionary(content)

        self.volume = extract_number(dict_residual[INTRADEL_RESIDUAL_VOLUME])
        self.chip_number = dict_residual[INTRADEL_RESIDUAL_CHIP_NUMBER]
        self.status = dict_residual[INTRADEL_RESIDUAL_STATUS]
        self.since = find_date(dict_residual[INTRADEL_RESIDUAL_SINCE])
        self.pickups = []

        self.pickups = self.get_pickups(content)


class Recyparc:
    """
    Represents the recyparc visits.

    Attributes:
    ----------
    since : datetime
        The starting date of the recyparc's operation.
    dropout : List[Dropout]
        A list of Dropout instances representing dropout events associated with the recyparc.
    """

    since: datetime
    dropout: List[Dropout]

    def get_dropouts(self, content: Tag) -> List[Dropout]:
        """
        Retrieve a list of dropout events associated with the recyparc.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing recyparc content.

        Returns:
        -------
        List[Dropout]
            A list of Dropout instances representing dropout events associated with the recyparc.
        """

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
        """
        Initialize a Recyparc instance.

        Parameters:
        ----------
        content : Tag
            The HTML 'Tag' object containing recyparc content.
        """

        dict_recyparc: Dict[str, str] = p_to_dictionary(content)

        self.since = find_date(dict_recyparc[INTRADEL_RESIDUAL_SINCE])
        self.dropout = self.get_dropouts(content)


class IntradelMyContainer:
    """
    Represents an IntradelMyContainer instance for retrieving waste management data.

    Attributes:
    ----------
    _login : str
        The login credential.
    _password : str
        The password credential.
    _municipality_id : str
        The id of the municipality.
    my_informations : Informations
        An Informations instance containing location information.
    organic : Organic
        An Organic instance containing organic waste bin information.
    residual : Residual
        A Residual instance containing residual waste bin information.
    recyparc : Recyparc
        A Recyparc instance containing recyparc information.
    start_date : datetime
        The start date for data retrieval.
    end_date : datetime
        The end date for data retrieval.
    _start_date_str : str
        The formatted start date string.
    _end_date_str : str
        The formatted end date string.
    """

    _login: str
    _password: str
    _municipality_id: str
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
        start_date: Union[None, datetime] = None,
        end_date: Union[None, datetime] = None,
    ) -> bytes:
        """
        Retrieve the page content using provided credentials and parameters.

        Parameters:
        ----------
        login : str
            The login credential.
        password : str
            The password credential.
        municipality_id : str
            The id of the municipality.
        start_date : Union[None, datetime], optional
            The start date for data retrieval, by default None.
        end_date : Union[None, datetime], optional
            The end date for data retrieval, by default None.

        Returns:
        -------
        bytes
            The page content as bytes.
        """

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
            "login": self._login,
            "pass": self._password,
            "commune": self._municipality_id,
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
        municipality_id: str,
        start_date: Union[None, datetime] = None,
        end_date: Union[None, datetime] = None,
    ) -> None:
        """
        Initialize an IntradelMyContainer instance.

        Parameters:
        ----------
        login : str
            The login credential.
        password : str
            The password credential.
        municipality_id : str
            The id of the municipality.
        start_date : Union[None, datetime], optional
            The start date for data retrieval, by default None.
        end_date : Union[None, datetime], optional
            The end date for data retrieval, by default None.
        """

        self._login = login
        self._password = password
        self._municipality_id = municipality_id

        page_content: bytes = self._get_page_content(
            start_date=start_date,
            end_date=end_date,
        )

        soup: BeautifulSoup = BeautifulSoup(page_content, "html.parser")
        all_post__content: ResultSet[Any] = soup.find_all("div", class_="post__content")

        for content in all_post__content:
            if isinstance(content, Tag):
                h3_tag = content.find_next("h3")
                if h3_tag is not None:
                    match h3_tag.text:
                        case const.INTRADEL_INFO_TITLE:
                            self.my_informations = Informations(content)
                        case const.INTRADEL_ORGANIC_TITLE:
                            self.organic = Organic(content)
                        case const.INTRADEL_RESIDUAL_TITLE:
                            self.residual = Residual(content)
                        case const.INTRADEL_RECYPARC_TITLE:
                            self.recyparc = Recyparc(content)
