"""Constants"""

from typing import Dict, Final, List

# Website
INTRADEL_URL_LOGIN: Final[str] = "https://www.intradel.be/particulier/"
INTRADEL_URL_DATA: Final[str] = "https://www.intradel.be/particulier/data.php"

# Mes informations

INTRADEL_INFO_TITLE: Final[str] = "Mes informations"
INTRADEL_INFO_NAME: Final[str] = "Nom"
INTRADEL_INFO_CATEGORY: Final[str] = "Catégorie"
INTRADEL_INFO_ADDRESS: Final[str] = "Adresse"
INTRADEL_INFO_ACTIF: Final[str] = "Actif"

INTRADEL_ORGANIC_TITLE: Final[str] = "ORGANIQUE"
INTRADEL_ORGANIC_VOLUME: Final[str] = "Volume"
INTRADEL_ORGANIC_CHIP_NUMBER: Final[str] = "Nr. Puce"
INTRADEL_ORGANIC_STATUS: Final[str] = "Statut"
INTRADEL_ORGANIC_SINCE: Final[str] = "Depuis"

INTRADEL_RESIDUAL_TITLE: Final[str] = "RESIDUEL"
INTRADEL_RESIDUAL_VOLUME: Final[str] = "Volume"
INTRADEL_RESIDUAL_CHIP_NUMBER: Final[str] = "Nr. Puce"
INTRADEL_RESIDUAL_STATUS: Final[str] = "Statut"
INTRADEL_RESIDUAL_SINCE: Final[str] = "Depuis"

INTRADEL_RECYPARC_TITLE: Final[str] = "RECYPARC"
INTRADEL_RECYPARC_SINCE: Final[str] = "Depuis"

INTRADEL_QUOTAS: Final[Dict[str, int]] = {
    "ENCOMBRANTS": 4,
    "BOIS": 3,
    "FRIGOLITE": 1,
    "INERTES": 5,
    "AMIANTE": 3,
    "VERTS": 8,
    "MATELAS": 4,
    "PNEUS": 5,
}

INTRADEL_QUOTAS_MAPPING: Final[Dict[str, List[str]]] = {
    "ENCOMBRANTS": ["Encombrants", "Enc.valorisables"],
    "BOIS": ["Bois"],
    "FRIGOLITE": ["Frigolite"],
    "INERTES": ["Inertes recyclés"],
    "AMIANTE": ["unknown"],
    "VERTS": ["Déchets verts"],
    "MATELAS": ["unknown"],
    "PNEUS": ["unknown"],
}

INTRADEL_MUNICIPALITIES: Final[Dict[str, int]] = {
    "AMAY": 26,
    "ANS": 590,
    "ANTHISNES": 3,
    "AUBEL": 589,
    "AWANS": 8,
    "AYWAILLE": 9,
    "BAELEN": 588,
    "BASSENGE": 591,
    "BERLOZ": 2,
    "BEYNE": 592,
    "BLEGNY": 581,
    "BRAIVES": 10,
    "BURDINNE": 577,
    "CHAUDFONTAINE": 584,
    "CLAVIER": 27,
    "COMBLAIN-AU-PONT": 30,
    "CRISNÉE": 593,
    "DALHEM": 594,
    "DEMO_BERLOZ": 580,
    "DISON": 595,
    "DONCEEL": 596,
    "ENGIS": 7,
    "ESNEUX": 6,
    "EUPEN": 597,
    "FAIMES": 4,
    "FERRIÈRES": 583,
    "FEXHE": 11,
    "FLEMALLE": 36,
    "FLERON": 21,
    "GEER": 29,
    "GRACE-HOLLOGNE": 32,
    "HAMOIR": 5,
    "HANNUT": 12,
    "HERSTAL": 38,
    "HERVE": 13,
    "HUY": 598,
    "JALHAY": 599,
    "JUPRELLE": 600,
    "KELMIS": 601,
    "LIEGE": 576,
    "LIMBOURG": 602,
    "LINCENT": 28,
    "LONTZEN": 603,
    "MARCHIN": 14,
    "MODAVE": 15,
    "NANDRIN": 35,
    "NEUPRÉ": 604,
    "OLNE": 587,
    "OREYE": 16,
    "OUFFET": 582,
    "OUPEYE": 579,
    "PEPINSTER": 22,
    "PLOMBIÈRES": 586,
    "RAEREN": 605,
    "REMICOURT": 17,
    "SAINT-GEORGES-SUR-MEUSE": 33,
    "SAINT-NICOLAS": 25,
    "SERAING": 24,
    "SOUMAGNE": 606,
    "SPA": 23,
    "SPRIMONT": 18,
    "THEUX": 607,
    "THIMISTER": 608,
    "TINLOT": 609,
    "TROOZ": 37,
    "VERLAINE": 610,
    "VERVIERS": 611,
    "VILLERS": 612,
    "VISÉ": 613,
    "WANZE": 19,
    "WAREMME": 20,
    "WASSEIGES": 1,
    "WELKENRAEDT": 585,
}
