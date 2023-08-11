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
