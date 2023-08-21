from datetime import datetime
from typing import Dict

from bs4 import BeautifulSoup, Tag

from intradel_my_container.functions import (
    cleanup,
    extract_number,
    find_date,
    p_to_dictionnary,
)

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


# p_to_dictionnary Function
# region p_to_dictionnary


def test_p_to_dictionnary_basic():
    tag_content = """<div class="post__content">
<h3 class="post__title">Mes informations</h3>
<p><strong>Nom</strong> : John Doe</p>
<p><strong>Catégorie</strong> : Ménages</p>
<p>
<strong>Adresse</strong> : RUE DES CHEVREUILS 10 C ,
                        4540 Amay
                      </p>
<!-- <p>
									<strong>Composition de m&eacute;nage</strong> : 4								</p> -->
<p><strong>Actif</strong> : Depuis le 01-02-2013</p>
<!--<p>
									<strong>Login</strong> : 								</p>
								<p>
									<strong>Mot de passe</strong> : 								</p>-->
<p style="text-align: right">
<strong><a href="logout.php">Déconnexion</a></strong>
</p>
</div>
"""
    soup: BeautifulSoup = BeautifulSoup(tag_content, "html.parser")
    content: Tag = soup.div
    p_dic: Dict[str, str] = p_to_dictionnary(content)
    assert (
        p_dic["Nom"] == "John Doe"
        and p_dic["Catégorie"] == "Ménages"
        and p_dic["Adresse"] == "RUE DES CHEVREUILS 10 C, 4540 Amay"
        and p_dic["Actif"] == "Depuis le 01-02-2013"
    )


# endregion p_to_dictionnary
