import requests
from flask import Flask

from db import db
from db.models import Installation
from utils import trouver_type

URL_INSTALLATIONS = (
    "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/Donnees_VUE_STATIONS_ET_TARAGES.json"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",  # noqa: E501
}


def sync_installations(app: Flask) -> dict:
    try:
        reponse = requests.get(
            url=URL_INSTALLATIONS,
            headers=HEADERS,
            timeout=10,
        )
        reponse.encoding = "UTF-8"
        reponse.raise_for_status()
    except requests.exceptions.RequestException:
        raise RuntimeError("Échec de la récupération des données Hydro-Québec.")

    corps_reponse = reponse.json()

    creees = 0
    mises_a_jour = 0

    with app.app_context():
        try:
            for donnees_installation in corps_reponse.get("Station", []):
                id_installation = donnees_installation.get("identifiant")
                if not id_installation:
                    continue

                nom_installation = donnees_installation.get("nom")
                type_installation = trouver_type(nom_installation)
                installation = {
                    "id": id_installation,
                    "nom": nom_installation,
                    "code_region": donnees_installation.get("CodeRegionQC"),
                    "nom_region": donnees_installation.get("RegionQC"),
                    "type": type_installation,
                    "x": donnees_installation.get("xcoord"),
                    "y": donnees_installation.get("ycoord"),
                    "z": donnees_installation.get("zcoord"),
                }

                installation_existante = db.session.get(Installation, id_installation)
                if not installation_existante:
                    db.session.add(Installation(**installation))
                    creees += 1
                    continue

                for cle, valeur in installation.items():
                    setattr(installation_existante, cle, valeur)
                mises_a_jour += 1

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    return {
        "creees": creees,
        "mises_a_jour": mises_a_jour,
    }
