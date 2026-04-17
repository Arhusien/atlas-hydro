from datetime import datetime, timedelta
from numbers import Number
from zoneinfo import ZoneInfo

import requests

from utils import constantes

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def _cumuler_donnees_cycles(cumulatif: dict, initial: dict) -> dict:
    """
    Cumule les données des cycles.

    Parameters:
        cumulatif (dict): Le dictionnaire contenant les données cumulées.
        initial (dict): Le dictionnaire contenant les données à additionner.

    Returns:
        (dict): Un dictionnaire contenant le cumule des données.
    """

    for cle, valeur in initial.items():
        if isinstance(valeur, dict):
            base = cumulatif.get(cle, {})
            print(base)
            # Si l'entrée n'existe pas dans le cumulatif
            if not isinstance(base, dict):
                base = {}

            cumulatif[cle] = _cumuler_donnees_cycles(base, valeur)
        elif isinstance(valeur, Number):
            cumulatif[cle] = cumulatif.get(cle, 0) + valeur

    return cumulatif


def obtenir_donnees_electricite() -> dict:
    """
    Récupère des données concernant l'électricité produite par dHydro-Québec.

    Returns:
        (dict): Un dictionnaire contenant les données.
    """

    reponse = requests.get(
        constantes.URL_ELECTRICITE_HQ,
        headers=constantes.HEADERS,
        timeout=constantes.ATTENTE_REQUETE_SECONDES,
    )
    reponse.encoding = "UTF-8"
    reponse.raise_for_status()

    donnees_electricite = reponse.json()

    date_hier = datetime.now(FUSEAU_HORAIRE).replace(minute=0, second=0, microsecond=0) - timedelta(hours=24)

    cumule_donnees = {}
    for cycle_donnees in donnees_electricite.get("details", []):
        date_brute = cycle_donnees.get("date")
        if not date_brute:
            continue

        date = datetime.fromisoformat(date_brute).replace(tzinfo=FUSEAU_HORAIRE)

        if date < date_hier:
            continue

        if "date" in cycle_donnees:
            del cycle_donnees["date"]

        cumule_donnees = _cumuler_donnees_cycles(cumule_donnees, cycle_donnees)

    return cumule_donnees
