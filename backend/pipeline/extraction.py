from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import constantes
from enums import JeuDonnees

JEUX_DONNEES = [
    JeuDonnees.HYDROMETEOROLOGIQUES,
    JeuDonnees.HYDROMETRIQUES,
]

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def _convertir_date(date_brute: str) -> datetime | None:
    """
    Convertit une date brute en objet datetime.

    Parameters:
        date_brute (str): La date brute.

    Returns:
        (datetime | None): La date convertie ou une valeur nulle.
    """

    if not isinstance(date_brute, str):
        return None

    # Pour chaque format de date possible
    for format_date in constantes.FORMATS_DATE:
        # Essayer de convertir (puis retourner) la date dans le format de l'itération
        # Si la conversion échoue, passer à l'itération suivante
        try:
            return datetime.strptime(date_brute, format_date).replace(tzinfo=FUSEAU_HORAIRE)

        except ValueError:
            continue

    return None


def _formatter_donnees_extraites(
    donnees_extraites: dict,
    jeu_donnees: JeuDonnees,
):
    """
    Formatte les données d'un jeu pour les convertir en une liste de relevés.

    Parameters:
        donnees_extraites (dict): Les données extraites du jeu.
        jeu_donnees (JeuDonnees): Le jeu de données extrait.
        date_minimale (datetime): La date minimale de conservation des données.
        date_maximale (datetime): La date maximale de conservation des données.

    Returns:
        (list[dict]): Une liste de relevés.
    """

    lst_releves: list[dict] = []

    cle_installations = "Station" if jeu_donnees == JeuDonnees.HYDROMETEOROLOGIQUES else "Site"

    for installation in donnees_extraites.get(cle_installations, []):
        id_installation = installation.get("identifiant")
        if not id_installation:
            continue

        for composition in installation.get("Composition", []):
            donnees_releve = composition.get("Donnees", {})

            for date_brute, valeur in donnees_releve.items():
                date = _convertir_date(date_brute)
                if date is None:  # or not (date_min < date <= date_max):
                    continue

                lst_releves.append(
                    {
                        "id": id_installation,
                        "date": date.isoformat(),
                        "type_valeur": composition.get("type_mesure"),
                        "unite_valeur": composition.get("nom_unite_mesure"),
                        "nom_donnee": composition.get("type_point_donnee"),
                        "valeur": valeur,
                    }
                )

    return lst_releves


def extraire_releves() -> dict[str, list[dict]]:
    """
    Extrait les relevés hydrométéorologiques ainsi qu'hydrométriques des jeux de données d'Hydro-Québec.

    Returns:
        (dict[str, list[dict]]]): Un dictionnaire contenant, pour chaque jeu de données, les relevés extraits de celui-ci.
    """  # noqa: E501

    releves_extraits = {}

    session = requests.Session()
    session.headers.update(constantes.HEADERS)

    for jeu_donnees in JEUX_DONNEES:
        releves_jeu_donnees = []
        try:
            url_jeu_donnees = (
                constantes.URL_SONDES_HQ
                if jeu_donnees == JeuDonnees.HYDROMETEOROLOGIQUES
                else constantes.URL_CENTRALES_HQ
            )

            reponse = session.get(
                url_jeu_donnees,
                timeout=constantes.ATTENTE_REQUETE_SECONDES,
            )
            reponse.encoding = "UTF-8"
            reponse.raise_for_status()

            donnees_jeu = reponse.json()

            releves_jeu_donnees = _formatter_donnees_extraites(
                donnees_jeu,
                jeu_donnees,
            )

        except requests.exceptions.RequestException:
            print(f"Échec de la récupération des relevés du jeu {jeu_donnees.value}.")
            # Arrêter l'extraction des relevés pour ce jeu
            continue

        print(f"{len(releves_jeu_donnees)} relevés extraits du jeu {jeu_donnees.value}.")

        releves_extraits[jeu_donnees.value] = releves_jeu_donnees

    return releves_extraits
