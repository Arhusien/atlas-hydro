from datetime import datetime, timedelta
from numbers import Number
from zoneinfo import ZoneInfo

import requests

import constantes

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)

nom_region_cle = {
    "new_york": "NewYork",
    "nouveau_brunswick": "NewBrunswick",
    "nouvelle_angleterre": "NewEngland",
    "ontario": "Ontario",
    "quebec": "Quebec",
}

nom_energie_cle = {
    "Biomasse - solide": "biomasse_solide",
    "Nucléaire": "nucleaire",
    "Autres fossiles": "autres_fossiles",
    "Hydro": "hydraulique",
    "Solaire": "solaire",
    "Géothermique": "geothermique",
    "Biomasse - biocarburant gazeux": "biomasse_gazeux",
    "Charbon": "charbon",
    "Électricité": "electricite",
    "Autres": "autres",
    "Biomasse - biocarburant liquide": "biomasse_liquide",
    "Pétrole": "petrole",
    "Gaz naturel": "gaz_naturel",
    "Éolien": "eolien",
}


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
            # Si l'entrée n'existe pas dans le cumulatif
            if not isinstance(base, dict):
                base = {}

            cumulatif[cle] = _cumuler_donnees_cycles(base, valeur)
        elif isinstance(valeur, Number):
            cumulatif[cle] = cumulatif.get(cle, 0) + valeur

    return cumulatif


def obtenir_donnees_electricite() -> dict:
    """
    Récupère des données concernant l'électricité du réseau d'Hydro-Québec.

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

    cumul_donnees = {}
    for cycle_donnees in donnees_electricite.get("details", []):
        date_brute = cycle_donnees.get("date")
        if not date_brute:
            continue

        date = datetime.fromisoformat(date_brute).replace(tzinfo=FUSEAU_HORAIRE)

        if date < date_hier:
            continue

        # Supprimer la date du dictionnaire avant de calculer le cumul
        if "date" in cycle_donnees:
            del cycle_donnees["date"]

        cumul_donnees = _cumuler_donnees_cycles(cumul_donnees, cycle_donnees)

    return {
        "exportation": cumul_donnees.get("Exportations", {}),
        "importation": cumul_donnees.get("Importations_Sources", {}),
        "consommation": cumul_donnees.get("Quebec_Consommation_Sources", {}),
        "production": cumul_donnees.get("Quebec_Production_Sources", {}),
        "estimation_ges": cumul_donnees.get("Quebec_Estimation_Consommation_GES"),
    }


def obtenir_emissions_ges() -> dict:
    """
    Récupère les facteurs d'émission (en tCO2eq/MWh) des diverses sources d'énergie du réseau d'Hydro-Québec.

    Returns:
        (dict): Un dictionnaire contenant les facteurs d'émission.
    """

    reponse = requests.get(
        constantes.URL_GES_HQ,
        headers=constantes.HEADERS,
        timeout=constantes.ATTENTE_REQUETE_SECONDES,
    )
    reponse.encoding = "UTF-8"
    reponse.raise_for_status()

    facteurs_ges = reponse.json()

    donnees_facteurs_ges_regions = {
        cle: {} for cle in nom_region_cle.values()
    }  # fmt: off
    for regions in facteurs_ges.get("results", []):
        nom_energie = regions.get("sources_d_energie")
        if nom_energie not in nom_energie_cle:
            continue

        for nom_region, facteur_ges in regions.items():
            if nom_region not in nom_region_cle:
                continue

            cle_region = nom_region_cle[nom_region]
            cle_energie = nom_energie_cle[nom_energie]

            donnees_facteurs_ges_regions[cle_region].update(
                {
                    cle_energie: facteur_ges,
                }
            )

    return donnees_facteurs_ges_regions
