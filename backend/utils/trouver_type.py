import re

from enums import TypeInstallation
from utils import simplifier_texte

# ex. (CQVI, 092725)
REGEX_CODE_SONDE = re.compile(r"\([A-Z0-9, ]+\)")


def trouver_type(nom: str) -> TypeInstallation:
    """
    Détermine le type d'une installation.

    Parameters:
        nom (str): Le nom de l'installation.

    Returns:
        (TypeInstallation): Le type de l'installation.
    """

    if not nom:
        return TypeInstallation.SONDE

    # Rechercher si le nom de l'installation contient un code de sonde
    if REGEX_CODE_SONDE.search(nom):
        return TypeInstallation.SONDE

    nom_simplifie = simplifier_texte(nom)

    if "centrale" in nom_simplifie:
        return TypeInstallation.CENTRALE

    if "barrage" in nom_simplifie:
        return TypeInstallation.BARRAGE

    return TypeInstallation.SONDE
