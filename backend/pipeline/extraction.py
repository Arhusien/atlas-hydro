import time
import urllib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from enums import JeuxDonnees
from utils import constantes

QUERY_PAR_DEFAUT = (
    f"?lang=fr&timezone={urllib.parse.quote(constantes.FUSEAU_HORAIRE)}" + f"&limit={constantes.LIMITE_ELEMENTS_API}"
)

JEUX_DONNEES = [
    JeuxDonnees.HYDROMETEOROLOGIQUES,
    JeuxDonnees.HYDROMETRIQUES,
]

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def extraire_releves() -> dict[str, list[dict]]:
    """
    Extrait les relevés hydrométéorologiques ainsi qu'hydrométriques des jeux de données d'Hydro-Québec.

    Returns:
        (dict[str, list[dict]]]): Un dictionnaire contenant, pour chaque jeu de données, les données extraites de celui-ci.
    """  # noqa: E501

    releves_extraits = {}

    session = requests.Session()
    session.headers.update({**constantes.HEADERS})

    date = datetime.now(FUSEAU_HORAIRE).replace(minute=0, second=0, microsecond=0)
    date_avancee = date + timedelta(hours=1)

    date_format_standard = date.strftime("%Y/%m/%d %H")
    date_format_iso = date.strftime("%Y/%m/%dT%H")

    for jeu_donnees in JEUX_DONNEES:
        # Filtrer à l'aide de "startsWith" car la date est une chaîne de caractères
        if jeu_donnees == JeuxDonnees.HYDROMETEOROLOGIQUES:
            filtre = f"startsWith(date, '{date_format_standard}') OR startsWith(date, '{date_format_iso}')"
        elif jeu_donnees == JeuxDonnees.HYDROMETRIQUES:
            filtre = f"startsWith(split_date, '{date_format_standard}') OR startsWith(split_date, '{date_format_iso}')"
        # Filtrer à l'aide d'opérateurs car la date est un objet
        else:
            filtre = f"date >= '{date.isoformat()}' AND date < '{date_avancee.isoformat()}'"

        url_api = f"{constantes.URL_API_DONNEES_HQ}/{jeu_donnees.value}/records{QUERY_PAR_DEFAUT}&where={urllib.parse.quote(filtre)}"  # noqa: E501

        releves_jeu_donnees = []
        decalage = 0
        total_elements = float("inf")  # Utiliser "inf" pour forcer la première itération

        while decalage < total_elements:
            print(f"Extraction des données du jeu {jeu_donnees.value} (decalage={decalage})")

            url_api_paginee = f"{url_api}&offset={decalage}"

            try:
                reponse = session.get(url_api_paginee, timeout=constantes.TIMEOUT_REQUETE_SECONDES)
                reponse.encoding = "UTF-8"
                reponse.raise_for_status()

                corps_reponse = reponse.json()

                # Mettre à jour le nombre total de relevés à extraire lors de première itération
                if decalage == 0:
                    total_elements = corps_reponse.get("total_count", 0)

                releves_jeu_donnees.extend(corps_reponse.get("results", []))

                decalage += constantes.LIMITE_ELEMENTS_API

                # Si une autre itération doit être faite, attendre 3 secondes
                if decalage < total_elements:
                    time.sleep(constantes.PAUSE_ENTRE_REQUETES_SECONDES)

            except requests.exceptions.RequestException:
                print(
                    f"Échec de la récupération des relevés d'Hydro-Québec pour le jeu {jeu_donnees.value} (decalage={decalage})."  # noqa: E501
                )
                # Arrêter l'extraction des relevés pour le jeu de l'itération
                break

        print(f"{len(releves_jeu_donnees)} relevés extraits du jeu {jeu_donnees.value}.")

        releves_extraits[jeu_donnees.value] = releves_jeu_donnees

        time.sleep(constantes.PAUSE_ENTRE_REQUETES_SECONDES)

    return releves_extraits
