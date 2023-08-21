from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup, Tag

from intradel_my_container import (
    Dropout,
    Informations,
    Material,
    Organic,
    Pickup,
    Recyparc,
    Residual,
)


def test_pickup_date():
    pickup_date = datetime.today()
    pickup: Pickup = Pickup(pickup_date, 45.67)
    assert pickup.date == pickup_date


def test_pickup_kilograms():
    pickup_date = datetime.today()
    pickup: Pickup = Pickup(pickup_date, 45.67)
    assert pickup.kilograms == 45.67


def test_material_name():
    material: Material = Material("Wood", 2.7, "m³")
    assert material.name == "Wood"


def test_material_name_space():
    material: Material = Material("  Wood  ", 2.7, "m³")
    assert material.name == "Wood"


def test_material_unit():
    material: Material = Material("Wood", 2.7, "m³")
    assert material.unit == "m³"


def test_material_unit_space():
    material: Material = Material("Wood", 2.7, "   m³   ")
    assert material.unit == "m³"


def test_material_quantity():
    material: Material = Material("Wood", 2.7, "m³")
    assert material.quantity == 2.7


def test_dropout_date():
    today: datetime = datetime.today()
    dropout: Dropout = Dropout(
        today,
        "LIÈGE",
        "Bois (0.10 m³), DSM (Autre) (0.00 pièce), Encombrants (0.25 m³)",
    )
    assert dropout.date == today


def test_dropout_parc():
    today: datetime = datetime.today()
    dropout: Dropout = Dropout(
        today,
        "LIÈGE",
        "Bois (0.10 m³), DSM (Autre) (0.00 pièce), Encombrants (0.25 m³)",
    )
    assert dropout.parc == "LIÈGE"


def test_dropout_islist():
    today: datetime = datetime.today()
    dropout: Dropout = Dropout(
        today,
        "LIÈGE",
        "Bois (0.10 m³), DSM (Autre) (0.00 pièce), Encombrants (0.25 m³)",
    )
    assert isinstance(dropout.materials, List)


def test_dropout_materials():
    today: datetime = datetime.today()
    dropout: Dropout = Dropout(
        today,
        "LIÈGE",
        "Bois (0.10 m³), DSM (Autre) (0.00 pièce), Encombrants (0.25 m³)",
    )
    assert (
        dropout.materials[0].name == "Bois"
        and dropout.materials[0].quantity == 0.1
        and dropout.materials[0].unit == "m³"
        and dropout.materials[1].name == "DSM (Autre)"
        and dropout.materials[1].quantity == 0
        and dropout.materials[1].unit == "pièce"
        and dropout.materials[2].name == "Encombrants"
        and dropout.materials[2].quantity == 0.25
        and dropout.materials[2].unit == "m³"
    )


def test_informations_basic():
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
    info: Informations = Informations(content)
    assert (
        info.name == "John Doe"
        and info.category == "Ménages"
        and info.address == "RUE DES CHEVREUILS 10 C, 4540 Amay"
        and info.actif == datetime(2013, 2, 1, 0, 0)
    )


def test_organic_basic():
    tag_content = """<div class="post__content">
<h3 class="post__title">ORGANIQUE</h3>
<p><strong>Volume</strong> : 240 L</p>
<p><strong>Nr. Puce</strong> : 8573214986</p>
<p><strong>Statut</strong> : ACTIVE</p>
<p><strong>Depuis</strong> : 01-02-2013</p>
<table id="table_results">
<thead>
<tr>
<th style="background-color: #64b731">Date</th>
<th style="background-color: #64b731">
                                Vidanges
                              </th>
<th style="background-color: #64b731">Kilos</th>
</tr>
</thead>
<tbody>
<tr>
<td>02-03-2013</td>
<td>1</td>
<td>72.8</td>
</tr>
<tr>
<td>07-05-2013</td>
<td>1</td>
<td>54.3</td>
</tr>
<tr>
<td>16-06-2013</td>
<td>1</td>
<td>60.9</td>
</tr>
<tr>
<td>21-06-2013</td>
<td>1</td>
<td>28.4</td>
</tr>
<tr>
<td>14-08-2013</td>
<td>1</td>
<td>68.2</td>
</tr>
<tr>
<td>03-09-2013</td>
<td>1</td>
<td>57.7</td>
</tr>
<tr>
<td>23-10-2013</td>
<td>1</td>
<td>74.6</td>
</tr>
<tr>
<td>04-12-2013</td>
<td>1</td>
<td>88.1</td>
</tr>
<tr>
<td>29-12-2013</td>
<td>1</td>
<td>76.2</td>
</tr>
<tr>
<td>20-02-2014</td>
<td>1</td>
<td>45.3</td>
</tr>
<tr>
<td>12-03-2014</td>
<td>1</td>
<td>71.4</td>
</tr>
<tr>
<td>04-06-2014</td>
<td>1</td>
<td>42.8</td>
</tr>
<tr>
<td>23-07-2014</td>
<td>1</td>
<td>94.5</td>
</tr>
<tr>
<td>08-10-2014</td>
<td>1</td>
<td>35.7</td>
</tr>
<tr>
<td>11-11-2014</td>
<td>1</td>
<td>61.8</td>
</tr>
<tr>
<td>07-01-2015</td>
<td>1</td>
<td>87.3</td>
</tr>
<tr>
<td>14-03-2015</td>
<td>1</td>
<td>50.7</td>
</tr>
<tr>
<td>29-04-2015</td>
<td>1</td>
<td>33.9</td>
</tr>
<tr>
<td>14-06-2015</td>
<td>1</td>
<td>78.0</td>
</tr>
<tr>
<td>14-11-2015</td>
<td>1</td>
<td>65.1</td>
</tr>
<tr>
<td>08-01-2016</td>
<td>1</td>
<td>39.2</td>
</tr>
<tr>
<td>05-03-2016</td>
<td>1</td>
<td>80.5</td>
</tr>
<tr>
<td>31-07-2016</td>
<td>1</td>
<td>29.8</td>
</tr>
<tr>
<td>16-09-2016</td>
<td>1</td>
<td>70.3</td>
</tr>
<tr>
<td>23-11-2016</td>
<td>1</td>
<td>46.9</td>
</tr>
<tr>
<td>12-01-2017</td>
<td>1</td>
<td>90.4</td>
</tr>
<tr>
<td>05-03-2017</td>
<td>1</td>
<td>36.7</td>
</tr>
<tr>
<td>20-04-2017</td>
<td>1</td>
<td>57.8</td>
</tr>
<tr>
<td>15-06-2017</td>
<td>1</td>
<td>80.3</td>
</tr>
<tr>
<td>28-08-2017</td>
<td>1</td>
<td>40.6</td>
</tr>
<tr>
<td>11-10-2017</td>
<td>1</td>
<td>23.4</td>
</tr>
<tr>
<td>07-12-2017</td>
<td>1</td>
<td>94.8</td>
</tr>
<tr>
<td>19-01-2018</td>
<td>1</td>
<td>66.9</td>
</tr>
<tr>
<td>12-03-2018</td>
<td>1</td>
<td>75.5</td>
</tr>
<tr>
<td>04-05-2018</td>
<td>1</td>
<td>47.8</td>
</tr>
<tr>
<td>26-06-2018</td>
<td>1</td>
<td>58.9</td>
</tr>
<tr>
<td>18-08-2018</td>
<td>1</td>
<td>31.2</td>
</tr>
<tr>
<td>09-10-2018</td>
<td>1</td>
<td>82.7</td>
</tr>
<tr>
<td>01-12-2018</td>
<td>1</td>
<td>70.0</td>
</tr>
<tr>
<td>09-03-2019</td>
<td>1</td>
<td>61.7</td>
</tr>
<tr>
<td>28-04-2019</td>
<td>1</td>
<td>78.6</td>
</tr>
<tr>
<td>12-06-2019</td>
<td>1</td>
<td>53.9</td>
</tr>
<tr>
<td>04-08-2019</td>
<td>1</td>
<td>36.5</td>
</tr>
<tr>
<td>29-09-2019</td>
<td>1</td>
<td>87.7</td>
</tr>
<tr>
<td>20-11-2019</td>
<td>1</td>
<td>69.9</td>
</tr>
<tr>
<td>05-01-2020</td>
<td>1</td>
<td>43.7</td>
</tr>
<tr>
<td>26-02-2020</td>
<td>1</td>
<td>76.2</td>
</tr>
<tr>
<td>18-04-2020</td>
<td>1</td>
<td>50.9</td>
</tr>
<tr>
<td>09-06-2020</td>
<td>1</td>
<td>70.1</td>
</tr>
<tr>
<td>01-08-2020</td>
<td>1</td>
<td>27.3</td>
</tr>
<tr>
<td>23-09-2020</td>
<td>1</td>
<td>82.4</td>
</tr>
<tr>
<td>15-11-2020</td>
<td>1</td>
<td>47.8</td>
</tr>
<tr>
<td>05-01-2021</td>
<td>1</td>
<td>62.5</td>
</tr>
<tr>
<td>26-02-2021</td>
<td>1</td>
<td>36.3</td>
</tr>
<tr>
<td>18-04-2021</td>
<td>1</td>
<td>51.2</td>
</tr>
<tr>
<td>10-06-2021</td>
<td>1</td>
<td>77.4</td>
</tr>
<tr>
<td>02-08-2021</td>
<td>1</td>
<td>65.1</td>
</tr>
<tr>
<td>24-09-2021</td>
<td>1</td>
<td>39.8</td>
</tr>
<tr>
<td>16-11-2021</td>
<td>1</td>
<td>56.4</td>
</tr>
<tr>
<td>07-01-2022</td>
<td>1</td>
<td>73.9</td>
</tr>
<tr>
<td>29-03-2022</td>
<td>1</td>
<td>33.6</td>
</tr>
<tr>
<td>20-05-2022</td>
<td>1</td>
<td>67.5</td>
</tr>
<tr>
<td>12-07-2022</td>
<td>1</td>
<td>50.1</td>
</tr>
<tr>
<td>03-09-2022</td>
<td>1</td>
<td>83.0</td>
</tr>
<tr>
<td>26-10-2022</td>
<td>1</td>
<td>42.5</td>
</tr>
<tr>
<td>17-12-2022</td>
<td>1</td>
<td>58.3</td>
</tr>
<tr>
<td>09-03-2023</td>
<td>1</td>
<td>69.6</td>
</tr>
<tr>
<td>05-05-2023</td>
<td>1</td>
<td>44.9</td>
</tr>
<tr>
<td>28-06-2023</td>
<td>1</td>
<td>54.6</td>
</tr>
<tr>
<td>20-08-2023</td>
<td>1</td>
<td>46.7</td>
</tr>
</tbody>
<tfoot>
<tr class="last_row">
<td style="background-color: #64b731">TOTAL</td>
<td style="background-color: #64b731">35</td>
<td style="background-color: #64b731">
                                2066.9 Kg
                              </td>
</tr>
</tfoot>
</table>
</div>
"""
    soup: BeautifulSoup = BeautifulSoup(tag_content, "html.parser")
    content: Tag = soup.div
    organic: Organic = Organic(content)
    assert (
        organic.volume == 240
        and organic.chip_number == "8573214986"
        and organic.status == "ACTIVE"
        and organic.since == datetime(2013, 2, 1, 0, 0)
        and len(organic.pickups) == 70
        and (
            organic.pickups[0].date == datetime(2013, 3, 2, 0, 0)
            and organic.pickups[0].kilograms == 72.8
        )
    )


def test_residual_basic():
    tag_content = """<div class="post__content">
<h3 class="post__title">RESIDUEL</h3>
<p><strong>Volume</strong> : 240 L</p>
<p><strong>Nr. Puce</strong> : 6120938475</p>
<p><strong>Statut</strong> : ACTIVE</p>
<p><strong>Depuis</strong> : 01-02-2013</p>
<table id="table_results">
<thead>
<tr>
<th style="background-color: #64b731">Date</th>
<th style="background-color: #64b731">
                                Vidanges
                              </th>
<th style="background-color: #64b731">Kilos</th>
</tr>
</thead>
<tbody>
<tr>
<td>02-03-2013</td>
<td>1</td>
<td>72.8</td>
</tr>
<tr>
<td>07-05-2013</td>
<td>1</td>
<td>54.3</td>
</tr>
<tr>
<td>16-06-2013</td>
<td>1</td>
<td>60.9</td>
</tr>
<tr>
<td>21-06-2013</td>
<td>1</td>
<td>28.4</td>
</tr>
<tr>
<td>14-08-2013</td>
<td>1</td>
<td>68.2</td>
</tr>
<tr>
<td>03-09-2013</td>
<td>1</td>
<td>57.7</td>
</tr>
<tr>
<td>23-10-2013</td>
<td>1</td>
<td>74.6</td>
</tr>
<tr>
<td>04-12-2013</td>
<td>1</td>
<td>88.1</td>
</tr>
<tr>
<td>29-12-2013</td>
<td>1</td>
<td>76.2</td>
</tr>
<tr>
<td>20-02-2014</td>
<td>1</td>
<td>45.3</td>
</tr>
<tr>
<td>12-03-2014</td>
<td>1</td>
<td>71.4</td>
</tr>
<tr>
<td>04-06-2014</td>
<td>1</td>
<td>42.8</td>
</tr>
<tr>
<td>23-07-2014</td>
<td>1</td>
<td>94.5</td>
</tr>
<tr>
<td>08-10-2014</td>
<td>1</td>
<td>35.7</td>
</tr>
<tr>
<td>11-11-2014</td>
<td>1</td>
<td>61.8</td>
</tr>
<tr>
<td>07-01-2015</td>
<td>1</td>
<td>87.3</td>
</tr>
<tr>
<td>14-03-2015</td>
<td>1</td>
<td>50.7</td>
</tr>
<tr>
<td>29-04-2015</td>
<td>1</td>
<td>33.9</td>
</tr>
<tr>
<td>14-06-2015</td>
<td>1</td>
<td>78.0</td>
</tr>
<tr>
<td>14-11-2015</td>
<td>1</td>
<td>65.1</td>
</tr>
<tr>
<td>08-01-2016</td>
<td>1</td>
<td>39.2</td>
</tr>
<tr>
<td>05-03-2016</td>
<td>1</td>
<td>80.5</td>
</tr>
<tr>
<td>31-07-2016</td>
<td>1</td>
<td>29.8</td>
</tr>
<tr>
<td>16-09-2016</td>
<td>1</td>
<td>70.3</td>
</tr>
<tr>
<td>23-11-2016</td>
<td>1</td>
<td>46.9</td>
</tr>
<tr>
<td>12-01-2017</td>
<td>1</td>
<td>90.4</td>
</tr>
<tr>
<td>05-03-2017</td>
<td>1</td>
<td>36.7</td>
</tr>
<tr>
<td>20-04-2017</td>
<td>1</td>
<td>57.8</td>
</tr>
<tr>
<td>15-06-2017</td>
<td>1</td>
<td>80.3</td>
</tr>
<tr>
<td>28-08-2017</td>
<td>1</td>
<td>40.6</td>
</tr>
<tr>
<td>11-10-2017</td>
<td>1</td>
<td>23.4</td>
</tr>
<tr>
<td>07-12-2017</td>
<td>1</td>
<td>94.8</td>
</tr>
<tr>
<td>19-01-2018</td>
<td>1</td>
<td>66.9</td>
</tr>
<tr>
<td>12-03-2018</td>
<td>1</td>
<td>75.5</td>
</tr>
<tr>
<td>04-05-2018</td>
<td>1</td>
<td>47.8</td>
</tr>
<tr>
<td>26-06-2018</td>
<td>1</td>
<td>58.9</td>
</tr>
<tr>
<td>18-08-2018</td>
<td>1</td>
<td>31.2</td>
</tr>
<tr>
<td>09-10-2018</td>
<td>1</td>
<td>82.7</td>
</tr>
<tr>
<td>01-12-2018</td>
<td>1</td>
<td>70.0</td>
</tr>
<tr>
<td>09-03-2019</td>
<td>1</td>
<td>61.7</td>
</tr>
<tr>
<td>28-04-2019</td>
<td>1</td>
<td>78.6</td>
</tr>
<tr>
<td>12-06-2019</td>
<td>1</td>
<td>53.9</td>
</tr>
<tr>
<td>04-08-2019</td>
<td>1</td>
<td>36.5</td>
</tr>
<tr>
<td>29-09-2019</td>
<td>1</td>
<td>87.7</td>
</tr>
<tr>
<td>20-11-2019</td>
<td>1</td>
<td>69.9</td>
</tr>
<tr>
<td>05-01-2020</td>
<td>1</td>
<td>43.7</td>
</tr>
<tr>
<td>26-02-2020</td>
<td>1</td>
<td>76.2</td>
</tr>
<tr>
<td>18-04-2020</td>
<td>1</td>
<td>50.9</td>
</tr>
<tr>
<td>09-06-2020</td>
<td>1</td>
<td>70.1</td>
</tr>
<tr>
<td>01-08-2020</td>
<td>1</td>
<td>27.3</td>
</tr>
<tr>
<td>23-09-2020</td>
<td>1</td>
<td>82.4</td>
</tr>
<tr>
<td>15-11-2020</td>
<td>1</td>
<td>47.8</td>
</tr>
<tr>
<td>05-01-2021</td>
<td>1</td>
<td>62.5</td>
</tr>
<tr>
<td>26-02-2021</td>
<td>1</td>
<td>36.3</td>
</tr>
<tr>
<td>18-04-2021</td>
<td>1</td>
<td>51.2</td>
</tr>
<tr>
<td>10-06-2021</td>
<td>1</td>
<td>77.4</td>
</tr>
<tr>
<td>02-08-2021</td>
<td>1</td>
<td>65.1</td>
</tr>
<tr>
<td>24-09-2021</td>
<td>1</td>
<td>39.8</td>
</tr>
<tr>
<td>16-11-2021</td>
<td>1</td>
<td>56.4</td>
</tr>
<tr>
<td>07-01-2022</td>
<td>1</td>
<td>73.9</td>
</tr>
<tr>
<td>29-03-2022</td>
<td>1</td>
<td>33.6</td>
</tr>
<tr>
<td>20-05-2022</td>
<td>1</td>
<td>67.5</td>
</tr>
<tr>
<td>12-07-2022</td>
<td>1</td>
<td>50.1</td>
</tr>
<tr>
<td>03-09-2022</td>
<td>1</td>
<td>83.0</td>
</tr>
<tr>
<td>26-10-2022</td>
<td>1</td>
<td>42.5</td>
</tr>
<tr>
<td>17-12-2022</td>
<td>1</td>
<td>58.3</td>
</tr>
<tr>
<td>09-03-2023</td>
<td>1</td>
<td>69.6</td>
</tr>
<tr>
<td>05-05-2023</td>
<td>1</td>
<td>44.9</td>
</tr>
<tr>
<td>28-06-2023</td>
<td>1</td>
<td>54.6</td>
</tr>
<tr>
<td>20-08-2023</td>
<td>1</td>
<td>46.7</td>
</tr>
</tbody>
<tfoot>
<tr class="last_row">
<td style="background-color: #64b731">TOTAL</td>
<td style="background-color: #64b731">35</td>
<td style="background-color: #64b731">
                                2066.9 Kg
                              </td>
</tr>
</tfoot>
</table>
</div>
"""
    soup: BeautifulSoup = BeautifulSoup(tag_content, "html.parser")
    content: Tag = soup.div
    residual: Residual = Residual(content)
    assert (
        residual.volume == 240
        and residual.chip_number == "6120938475"
        and residual.status == "ACTIVE"
        and residual.since == datetime(2013, 2, 1, 0, 0)
        and len(residual.pickups) == 70
        and (
            residual.pickups[0].date == datetime(2013, 3, 2, 0, 0)
            and residual.pickups[0].kilograms == 72.8
        )
    )


def test_recyparc_basic():
    tag_content = """<div class="post__content">
<h3 class="post__title">RECYPARC</h3>
<p><strong>Depuis</strong> : 01-02-2013</p>
<table id="table_results">
<thead>
<tr>
<th style="background-color: #ffa64d">Date</th>
<th style="background-color: #ffa64d">Parc</th>
<th style="background-color: #ffa64d">Matière</th>
</tr>
</thead>
<tbody>
<tr>
<td>03-03-2018</td>
<td>ENGIS</td>
<td>
                                DSM (Autre) (1.00 pièce), <br/>Petits Bruns
                                (5.00 pièce)
                              </td>
</tr>
<tr>
<td>22-03-2018</td>
<td>AWAY</td>
<td>
                                Encombrants (0.15 m³), <br/>Petits Bruns (3.00
                                pièce)
                              </td>
</tr>
<tr>
<td>14-07-2018</td>
<td>HUY</td>
<td>Déchets verts (6.00 m³)</td>
</tr>
<tr>
<td>21-09-2018</td>
<td>ENGIS</td>
<td>
                                Bois (0.15 m³), <br/>DSM (Autre) (0.00 pièce),
                                <br/>Encombrants (0.35 m³)
                              </td>
</tr>
<tr>
<td>10-11-2018</td>
<td>WANZE</td>
<td>Encombrants (0.30 m³)</td>
</tr>
<tr>
<td>22-11-2018</td>
<td>LIÈGE</td>
<td>
                                Encombrants (0.15 m³), <br/>Piles (0.00 m³)
                              </td>
</tr>
<tr>
<td>08-12-2018</td>
<td>ENGIS</td>
<td>
                                Métaux (0.00 m³), <br/>Papiers_Cartons (0.00
                                m³), <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>18-02-2019</td>
<td>ENGIS</td>
<td>
                                DSM (Autre) (0.00 pièce), <br/>Petits Bruns
                                (0.00 pièce)
                              </td>
</tr>
<tr>
<td>15-04-2019</td>
<td>WANZE</td>
<td>
                                Encombrants (0.15 m³), <br/>Frigolite (0.15 m³)
                              </td>
</tr>
<tr>
<td>06-05-2019</td>
<td>ENGIS</td>
<td>DSM (Autre) (0.00 pièce)</td>
</tr>
<tr>
<td>04-08-2019</td>
<td>GLAIN</td>
<td>
                                Bois (0.02 m³), <br/>DSM (Autre) (0.00 pièce),
                                <br/>Enc.valorisables (0.50 m³),
                                <br/>Papiers_Cartons (0.00 m³)
                              </td>
</tr>
<tr>
<td>24-08-2019</td>
<td>ENGIS</td>
<td>
                                Bois (0.15 m³), <br/>Encombrants (0.10 m³),
                                <br/>Papiers_Cartons (0.00 m³), <br/>Petits
                                Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>20-01-2020</td>
<td>ENGIS</td>
<td>
                                Bois (0.30 m³), <br/>Encombrants (0.15 m³)
                              </td>
</tr>
<tr>
<td>25-05-2020</td>
<td>ENGIS</td>
<td>
                                Bois (0.30 m³), <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>31-05-2020</td>
<td>ENGIS</td>
<td>
                                Inertes recyclés (0.50 m³), <br/>Inertes
                                recyclés (0.75 m³)
                              </td>
</tr>
<tr>
<td>05-06-2020</td>
<td>ENGIS</td>
<td>Inertes recyclés (0.50 m³)</td>
</tr>
<tr>
<td>16-07-2020</td>
<td>ENGIS</td>
<td>
                                Bois (0.15 m³), <br/>Encombrants (0.30 m³),
                                <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>26-04-2021</td>
<td>ENGIS</td>
<td>
                                Encombrants (0.15 m³), <br/>Frigolite (0.05
                                m³), <br/>Métaux (0.00 m³)
                              </td>
</tr>
<tr>
<td>12-06-2021</td>
<td>ENGIS</td>
<td>
                                Bois (0.50 m³), <br/>DSM (Pot de peint.) (6.00
                                pièce), <br/>Huiles friture (0.00 m³),
                                <br/>Bois (0.20 m³), <br/>Déchets verts (0.15
                                m³), <br/>Frigolite (0.05 m³), <br/>Métaux
                                (0.00 m³), <br/>Papiers_Cartons (0.00 m³),
                                <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>30-06-2021</td>
<td>ENGIS</td>
<td>
                                Bois (0.15 m³), <br/>Encombrants (0.55 m³),
                                <br/>Métaux (0.00 m³), <br/>Petits Bruns (0.00
                                pièce)
                              </td>
</tr>
<tr>
<td>18-07-2021</td>
<td>ENGIS</td>
<td>Déchets verts (6.00 m³)</td>
</tr>
<tr>
<td>09-08-2021</td>
<td>LIÈGE</td>
<td>Déchets verts (0.75 m³)</td>
</tr>
<tr>
<td>13-03-2022</td>
<td>ENGIS</td>
<td>
                                Encombrants (0.20 m³), <br/>Frigolite (0.07
                                m³), <br/>Papiers_Cartons (0.00 m³)
                              </td>
</tr>
<tr>
<td>18-03-2022</td>
<td>ENGIS</td>
<td>
                                Ecrans (0.00 pièce), <br/>Encombrants (0.20
                                m³), <br/>EV (Plastiques) (1.00 pièce),
                                <br/>Frigolite (0.07 m³), <br/>Petits Bruns
                                (0.00 pièce)
                              </td>
</tr>
<tr>
<td>21-03-2022</td>
<td>ENGIS</td>
<td>
                                Encombrants (0.40 m³), <br/>Métaux (0.00 m³)
                              </td>
</tr>
<tr>
<td>21-05-2022</td>
<td>ENGIS</td>
<td>
                                Bois (0.20 m³), <br/>Encombrants (0.20 m³),
                                <br/>Métaux (0.00 m³), <br/>Métaux (0.00 m³)
                              </td>
</tr>
<tr>
<td>19-06-2022</td>
<td>ENGIS</td>
<td>Déchets verts (0.80 m³)</td>
</tr>
<tr>
<td>14-08-2022</td>
<td>LIÈGE</td>
<td>
                                Déchets verts (0.55 m³), <br/>Inertes recyclés
                                (0.55 m³)
                              </td>
</tr>
<tr>
<td>10-10-2022</td>
<td>ENGIS</td>
<td>
                                Encombrants (0.20 m³), <br/>Papiers_Cartons
                                (0.00 m³), <br/>Petits Bruns (0.00 pièce),
                                <br/>Verre blanc (0.00 m³), <br/>Verre coloré
                                (0.00 m³)
                              </td>
</tr>
<tr>
<td>02-12-2022</td>
<td>ENGIS</td>
<td>
                                Bois (0.06 m³), <br/>Encombrants (0.20 m³),
                                <br/>Papiers_Cartons (0.00 m³)
                              </td>
</tr>
<tr>
<td>15-02-2023</td>
<td>ENGIS</td>
<td>
                                DSM (Autre) (1.00 pièce), <br/>Encombrants
                                (0.03 m³), <br/>Frigolite (0.03 m³),
                                <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>03-04-2023</td>
<td>ENGIS</td>
<td>
                                Encombrants (0.09 m³), <br/>Métaux (0.00 m³),
                                <br/>Neons (0.00 pièce), <br/>Papiers_Cartons
                                (0.00 m³), <br/>Petits Bruns (0.00 pièce)
                              </td>
</tr>
<tr>
<td>15-06-2023</td>
<td>LIÈGE</td>
<td>Déchets verts (0.85 m³)</td>
</tr>
<tr>
<td>20-06-2023</td>
<td>ENGIS</td>
<td>
                                Bois (0.43 m³), <br/>Encombrants (0.08 m³)
                              </td>
</tr>
<tr>
<td>24-06-2023</td>
<td>LIÈGE</td>
<td>
                                Encombrants (0.03 m³), <br/>Papiers_Cartons
                                (0.00 m³)
                              </td>
</tr>
<tr>
<td>01-07-2023</td>
<td>LIÈGE</td>
<td>Déchets verts (1.00 m³)</td>
</tr>
<tr>
<td>27-08-2023</td>
<td>LIÈGE</td>
<td>Déchets verts (0.30 m³)</td>
</tr>
<tr>
<td>22-09-2023</td>
<td>LIÈGE</td>
<td>
                                Bois (0.18 m³), <br/>Déchets verts (1.00 m³),
                                <br/>Encombrants (0.20 m³)
                              </td>
</tr>
</tbody>
<tfoot>
<tr class="last_row">
<!--<td  style="background-color:#ffa64d;">TOTAL</td> -->
<!--<td  style="background-color:#ffa64d;"></td>
									  <td  style="background-color:#ffa64d;"></td> -->
<!--<td colspan="3" style="text-align:right; background-color:#ffa64d;"> M3</td> -->
</tr>
</tfoot>
</table>
</div>
"""
    soup: BeautifulSoup = BeautifulSoup(tag_content, "html.parser")
    content: Tag = soup.div
    recyparc: Recyparc = Recyparc(content)
    assert (
        recyparc.since == datetime(2013, 2, 1, 0, 0)
        and len(recyparc.dropout) == 38
        and (
            recyparc.dropout[0].date == datetime(2018, 3, 3, 0, 0)
            and recyparc.dropout[0].parc == "ENGIS"
            and (
                recyparc.dropout[0].materials[0].name == "DSM (Autre)"
                and recyparc.dropout[0].materials[0].quantity == 1.0
                and recyparc.dropout[0].materials[0].unit == "pièce"
            )
        )
    )
