import time

import requests
import spacy
from flask import Flask
from geopy.distance import geodesic
from spacy.lang.fr.stop_words import STOP_WORDS
from spacy.language import Language
from spacy.tokens import Doc

from db import db
from enums import TypeInstallation
from models import Barrage, Centrale, Installation, Sonde
from utils import constantes, simplifier_texte

noms_syonymes = {
    "Grande-2": "Robert-Bourassa",
    "Hart-Jaune Supérieur": "Petit Lac Manicouagan",
    "Rapide Sept": "Rapide-7",
}

# Ajouter quelques mots génériques aux mots vides par défaut de Spacy
STOP_WORDS.update(["barrage", "centrale", "digue", "bief", "aval", "amont"])

tal = spacy.load("fr_core_news_sm")


def _traiter_nom_installation(modele_tal: Language, nom: str) -> str:
    """
    Traite le nom d'une installation à l'aide d'un modèle de traitement automatique des langages.

    Parameters:
        modele_tal (Language): Un modèle de traitement Spacy.
        nom (str): Le nom de l'installation.

    Reuturns:
        (str): Le nom traité.
    """

    nom_traite = nom
    # Remplacer certains mots contenus dans le nom de l'installation par un synonyme
    # afin de faciliter l'assocition des sondes aux ouvrages
    for mot, synonyme in noms_syonymes.items():
        nom_traite = nom_traite.replace(mot, synonyme)

    if not isinstance(modele_tal, Language):
        return simplifier_texte(nom_traite)

    doc: Doc = modele_tal(nom_traite)

    mots_traites = []
    for token in doc:
        if not (token.is_stop or token.is_punct):
            mots_traites.append(token.text)

    nom_traite = " ".join(mots_traites).strip()

    return simplifier_texte(nom_traite)


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


def associer_sondes_ouvrages(app: Flask) -> int:
    """
    Associe à un ouvrage les sondes à proximité qui lui correspondent.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (int): Le nombre d'associations créées.
    """

    with app.app_context():
        lst_ouvrages: list[Centrale | Barrage] = Installation.query.filter(
            Installation.type.in_([TypeInstallation.BARRAGE, TypeInstallation.CENTRALE])
        ).all()

        # Trier la liste de manière à ce que les barrages soient placés devant les centrales
        lst_ouvrages = sorted(lst_ouvrages, key=lambda o: o.type.value)

        associations_creees = 0
        distance = geodesic(kilometers=constantes.DISTANCE_ASSOCIATION_CENTRALE_KM)

        for ouvrage in lst_ouvrages:
            if (ouvrage.y is None) or (ouvrage.x is None):
                continue

            point_centrale = (ouvrage.y, ouvrage.x)

            # Calculer les 4 sommets du carré de la zone de proximité
            nord = distance.destination(point=point_centrale, bearing=0).latitude
            sud = distance.destination(point=point_centrale, bearing=180).latitude
            est = distance.destination(point=point_centrale, bearing=90).longitude
            ouest = distance.destination(point=point_centrale, bearing=270).longitude

            sondes_a_proximite: list[Sonde] = Sonde.query.filter(
                Sonde.ouvrage_id.is_(None),
                Sonde.y >= sud,  # Plus grand (ou égal) que 5 km au sud de la centrale
                Sonde.y <= nord,  # Plus petit (ou égal) que 5 km au nord de la centrale
                Sonde.x >= ouest,  # Plus grand (ou égal) que 5 km a l'ouest de la centrale
                Sonde.x <= est,  # Plus petit (ou égal) que 5 km a l'est de la centrale
            ).all()

            for sonde in sondes_a_proximite:
                # Associer seulement si le nom de l'ouvrage est contenu dans le nom de la sonde
                if _traiter_nom_installation(tal, ouvrage.nom) in _traiter_nom_installation(tal, sonde.nom):
                    sonde.ouvrage_id = ouvrage.id
                    associations_creees += 1

        db.session.commit()

        return associations_creees
