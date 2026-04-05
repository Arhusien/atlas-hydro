import time
import urllib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from flask import Flask

from db import db
from enums import JeuDonnees, TypeReleve
from models import Releve
from utils import constantes

QUERY_PAR_DEFAUT = (
    f"?lang=fr&timezone={urllib.parse.quote(constantes.FUSEAU_HORAIRE)}" + f"&limit={constantes.LIMITE_ELEMENTS_API}"
)

JEUX_DONNEES = [
    JeuDonnees.HYDROMETEOROLOGIQUES,
    JeuDonnees.HYDROMETRIQUES,
]

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def _construire_filtre_date(cle_date: str, date_inferieure: datetime, date_superieure: datetime) -> str:
    """
    Construit un filtre par rapport à un intervalle de temps.

    Parameters:
        cle_date (str): La clé JSON de la valeur de la date.
        date_inferieure (datetime): La borne inférieure de l'intervalle de temps (exclue).
        date_superieure (datetime): La borne supérieure de l'intervalle de temps (incluse).

    Returns:
        (str): Le filtre de l'intervalle de temps.
    """

    nb_heures = int((date_superieure - date_inferieure).total_seconds() / 3600)

    conditions_date = []
    # La date de début n'est pas incluse dans l'itération
    for i in range(nb_heures):
        date_iteration = date_superieure - timedelta(hours=i)

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
            if jeu_donnees == JeuDonnees.HYDROMETEOROLOGIQUES
            else TypeReleve.HYDROMETRIQUE
        )

        with app.app_context():
            date_dernier_releve = (
                db.session.query(db.func.max(Releve.date)).filter(Releve.type_releve == type_releve).scalar()
            )

        if not date_dernier_releve:
            date_dernier_releve = date - timedelta(hours=24)

        date_dernier_releve = date_dernier_releve.replace(tzinfo=FUSEAU_HORAIRE)

        nb_heures_retard = int((date - date_dernier_releve).total_seconds() / 3600)
        if nb_heures_retard > 24:
            nb_heures_retard = 24
            date_dernier_releve = date - timedelta(hours=24)

        releves_jeu_donnees = []

        for i in range(0, nb_heures_retard, 3):
            nb_heures_intervalle = min(3, nb_heures_retard - i)

            date_debut_intervalle = date_dernier_releve + timedelta(hours=i)
            date_fin_intervalle = date_debut_intervalle + timedelta(hours=nb_heures_intervalle)

            cle_date = "date" if jeu_donnees == JeuDonnees.HYDROMETEOROLOGIQUES else "split_date"

            filtre_date = _construire_filtre_date(
                cle_date,
                date_inferieure=date_debut_intervalle,
                date_superieure=date_fin_intervalle,
            )

            url_api = f"{constantes.URL_API_DONNEES_HQ}/{jeu_donnees.value}/records{QUERY_PAR_DEFAUT}&where={urllib.parse.quote(filtre_date)}"  # noqa: E501

            decalage = 0
            total_elements = float("inf")  # Utiliser "inf" pour forcer la première itération

            print(
                "Extraction des données dans l'intervalle de temps :"
                + f"]{date_debut_intervalle.isoformat()}; {date_fin_intervalle.isoformat()}]"
            )

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

    return releves_extraits
