import time
import urllib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from flask import Flask

from db import db
from enums import JeuxDonnees, TypeReleve
from models import Releve
from utils import constantes

QUERY_PAR_DEFAUT = (
    f"?lang=fr&timezone={urllib.parse.quote(constantes.FUSEAU_HORAIRE)}" + f"&limit={constantes.LIMITE_ELEMENTS_API}"
)

JEUX_DONNEES = [
    JeuxDonnees.HYDROMETEOROLOGIQUES,
    JeuxDonnees.HYDROMETRIQUES,
]

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def _construire_filtre_date(cle_date: str, date_limite: datetime, date_fin: datetime) -> str:
    """
    Construit un filtre par rapport à un intervalle de temps.

    Parameters:
        cle_date (str): La clé JSON de la valeur de la date.
        date_limite (datetime): La borne inférieure de l'intervalle de temps (exclue).
        date_fin (datetime): La borne supérieure de l'intervalle de temps (incluse).

    Returns:
        (str): Le filtre de l'intervalle de temps.
    """

    nb_heures = int((date_fin - date_limite).total_seconds() / 3600)

    # Si le nombre d'heures est supérieur à 6
    if nb_heures > 6:
        nb_heures = 6
        # Avancer la date de début à la date de fin moins 6 heures
        date_limite = date_fin - timedelta(hours=6)

    conditions_date = []
    # La date de début n'est pas incluse dans l'itération
    for i in range(nb_heures):
        date_iteration = date_fin - timedelta(hours=i)

        conditions_date.extend(
            [
                f"startsWith({cle_date}, '{date_iteration.strftime('%Y/%m/%d %H')}')",
                f"startsWith({cle_date}, '{date_iteration.strftime('%Y/%m/%dT%H')}')",
            ]
        )

    return " OR ".join(conditions_date)


def extraire_releves(app: Flask) -> dict[str, list[dict]]:
    """
    Extrait les relevés hydrométéorologiques ainsi qu'hydrométriques des jeux de données d'Hydro-Québec.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (dict[str, list[dict]]]): Un dictionnaire contenant, pour chaque jeu de données, les données extraites de celui-ci.
    """  # noqa: E501

    releves_extraits = {}

    session = requests.Session()
    session.headers.update({**constantes.HEADERS})

    date = datetime.now(FUSEAU_HORAIRE).replace(minute=0, second=0, microsecond=0)

    for jeu_donnees in JEUX_DONNEES:
        type_releve = (
            TypeReleve.HYDROMETEOROLOGIQUE
            if jeu_donnees == JeuxDonnees.HYDROMETEOROLOGIQUES
            else TypeReleve.HYDROMETRIQUE
        )

        with app.app_context():
            derniere_date = (
                db.session.query(db.func.max(Releve.date)).filter(Releve.type_releve == type_releve).scalar()
            )

        if derniere_date:
            derniere_date = derniere_date.replace(tzinfo=FUSEAU_HORAIRE)
        else:
            derniere_date = date - timedelta(hours=6)

        if jeu_donnees == JeuxDonnees.HYDROMETEOROLOGIQUES:
            filtre_date = _construire_filtre_date("date", derniere_date, date)
        elif jeu_donnees == JeuxDonnees.HYDROMETRIQUES:
            filtre_date = _construire_filtre_date("split_date", derniere_date, date)

        # S'il n'y a pas de filtre par rapport à la date, alors tous les relevés sont à jour en base de données
        if not filtre_date:
            continue

        url_api = f"{constantes.URL_API_DONNEES_HQ}/{jeu_donnees.value}/records{QUERY_PAR_DEFAUT}&where={urllib.parse.quote(filtre_date)}"  # noqa: E501

        releves_jeu_donnees = []
        decalage = 0
        total_elements = float("inf")  # Utiliser "inf" pour forcer la première itération

        print(f"Extraction des données dans l'intervalle de temps : ]{derniere_date.isoformat()}; {date.isoformat()}].")

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
