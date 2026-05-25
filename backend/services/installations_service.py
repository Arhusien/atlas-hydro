from typing import Optional

from db import db
from models import Installation


def obtenir_installation(id_installation: str) -> Optional[dict]:
    """
    Récupère les données d'une installation en base de données.

    Parameters:
        id_installation (str): L'identifiant de l'installation.

    Returns:
        (dict | None): Les données de l'installation ou une valeur nulle.
    """

    installation = db.session.get(Installation, id_installation)
    if not installation:
        return None

    return installation.serialiser(avec_releves=True)
