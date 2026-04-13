import time

import requests
from flask import Flask
from geopy.distance import geodesic

from db import db
from enums import TypeInstallation
from models import Barrage, Centrale, Installation, Sonde
from utils import constantes, simplifier_texte


def synchroniser_installations(app: Flask) -> dict[str, int | float]:
    """
    Extrait et charge en base de données les installations d'Hydro-Québec.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (dict[str, int | float]): Un dictionnaire contenant les statistiques de la synchronisation.
    """

    debut_execution = time.perf_counter()

    session = requests.Session()
    session.headers.update({**constantes.HEADERS})

    try:
        reponse_centrales = session.get(
            constantes.URL_CENTRALES_HQ,
            timeout=constantes.ATTENTE_REQUETE_SECONDES,
        )
        reponse_centrales.encoding = "UTF-8"
        reponse_centrales.raise_for_status()

        reponse_sondes = session.get(
            constantes.URL_SONDES_HQ,
            timeout=constantes.ATTENTE_REQUETE_SECONDES,
        )
        reponse_sondes.encoding = "UTF-8"
        reponse_sondes.raise_for_status()

    except requests.exceptions.RequestException:
        raise RuntimeError("Echec de la recuperation des donnees Hydro-Quebec des installations.")

    donnees_centrales = reponse_centrales.json()
    donnees_sondes = reponse_sondes.json()

    nb_creees = 0
    nb_mises_a_jour = 0

    with app.app_context():
        try:
            lst_installations = donnees_centrales.get("Site", [])
            lst_installations.extend(donnees_sondes.get("Station", []))

            for donnees_installation in lst_installations:
                id_installation = donnees_installation.get("identifiant")
                if not id_installation:
                    continue

                type_installation = TypeInstallation.SONDE
                # Si la liste des données comprend une donnée "Débit turbiné", il s'agit d'une centrale
                if any(
                    simplifier_texte("Débit turbiné") in simplifier_texte(donnee.get("type_point_donnee", ""))
                    for donnee in donnees_installation.get("Composition", [])
                ):
                    type_installation = TypeInstallation.CENTRALE
                # S'il ne s'agit pas d'une centrale et que l'identifiant de l'installation est présent
                # dans la liste des barrages et centrales, il s'agit alors d'un barrage
                elif id_installation.startswith("3-"):
                    type_installation = TypeInstallation.BARRAGE

                installation = {
                    "id": id_installation,
                    "nom": donnees_installation.get("nom"),
                    "code_region": donnees_installation.get("CodeRegionQC"),
                    "nom_region": donnees_installation.get("RegionQC"),
                    "type": type_installation,
                    "x": donnees_installation.get("xcoord"),
                    "y": donnees_installation.get("ycoord"),
                    "z": donnees_installation.get("zcoord"),
                }

                installation_existante = db.session.get(Installation, id_installation)
                if not installation_existante:
                    if type_installation == TypeInstallation.CENTRALE:
                        nouvelle_installation = Centrale(**installation)
                    elif type_installation == TypeInstallation.BARRAGE:
                        nouvelle_installation = Barrage(**installation)
                    elif type_installation == TypeInstallation.SONDE:
                        nouvelle_installation = Sonde(**installation)

                    db.session.add(nouvelle_installation)

                    nb_creees += 1
                else:
                    for cle, valeur in installation.items():
                        setattr(installation_existante, cle, valeur)

                    nb_mises_a_jour += 1

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

    fin_execution = time.perf_counter()
    temps_execution = fin_execution - debut_execution

    return {
        "creees": nb_creees,
        "mises_a_jour": nb_mises_a_jour,
        "temps": temps_execution,
    }


def associer_sondes_centrales(app: Flask) -> int:
    """
    Associe les sondes à proximité d'une centrale à cette même centrale.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (int): Le nombre d'associations créées.
    """

    with app.app_context():
        lst_ouvrages: list[Centrale | Barrage] = Installation.query.filter(
            Installation.type.in_([TypeInstallation.BARRAGE, TypeInstallation.CENTRALE])
        ).all()

        associations_creees = 0

        for ouvrage in lst_ouvrages:
            if (ouvrage.y is None) or (ouvrage.x is None):
                continue

            point_centrale = (ouvrage.y, ouvrage.x)
            distance = geodesic(kilometers=constantes.DISTANCE_ASSOCIATION_CENTRALE_KM)

            # Calculer les 4 points de la zone de recherche
            nord = distance.destination(point=point_centrale, bearing=0).latitude
            sud = distance.destination(point=point_centrale, bearing=180).latitude
            est = distance.destination(point=point_centrale, bearing=90).longitude
            ouest = distance.destination(point=point_centrale, bearing=270).longitude

            sondes_a_proximite: list[Sonde] = Sonde.query.filter(
                Sonde.ouvrage_id == None,  # noqa: E711
                Sonde.y >= sud,  # Plus grand (ou égal) que 5 km au sud de la centrale
                Sonde.y <= nord,  # Plus petit (ou égal) que 5 km au nord de la centrale
                Sonde.x >= ouest,  # Plus grand (ou égal) que 5 km a l'ouest de la centrale
                Sonde.x <= est,  # Plus petit (ou égal) que 5 km a l'est de la centrale
            ).all()

            for sonde in sondes_a_proximite:
                if (
                    ouvrage.type == TypeInstallation.BARRAGE
                    and simplifier_texte("Barrage") in simplifier_texte(sonde.nom)
                ) or (ouvrage.type == TypeInstallation.CENTRALE):
                    sonde.ouvrage_id = ouvrage.id

        db.session.commit()

        return associations_creees
