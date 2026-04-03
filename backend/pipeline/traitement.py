from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from flask import Flask

from db import db
from enums import TypeDonnee, TypeReleve
from models import Releve
from utils import constantes, convertir_valeur, simplifier_texte

FUSEAU_HORAIRE = ZoneInfo(constantes.FUSEAU_HORAIRE)


def _determiner_type_donnee(donnee: str, type_releve: TypeReleve) -> TypeDonnee:
    """
    Détermine le type de la donnée d'un relevé.

    Parameters:
        donnee (str): Le nom de la donnée.
        type_releve (TypeReleve): Le type du relevé.

    Returns:
        (TypeDonnee): Le type de la donnée du relevé.
    """

    if not donnee:
        return TypeDonnee.INCONNU

    # Filtrer la liste des types de données pour n'y inclure que ceux du type du relevé
    types_donnees_releve = list(filter(lambda t: t.type_releve == type_releve, TypeDonnee))

    for type_donnee in types_donnees_releve:
        if simplifier_texte(type_donnee.value) in simplifier_texte(donnee):
            return type_donnee

    return TypeDonnee.INCONNU


def traiter_releves(app: Flask, lst_releves: list[dict], type_releves: TypeReleve) -> int:
    """
    Traite et charge les relevés en base de données.

    Parameters:
        app (Flask): L'application Flask.
        lst_releves (list[dict]): La liste des relevés extraits.
        type_releves (TypeReleve): Le type de relevés.

    Returns:
        (int): Le nombre de relevés créés.
    """

    nb_releves_crees = 0

    with app.app_context():
        try:
            for donees_releve in lst_releves:
                id_installation = donees_releve.get("identifiant")
                if not id_installation:
                    continue

                valeur = None
                if type_releves == TypeReleve.HYDROMETEOROLOGIQUE:
                    valeur = donees_releve.get("valeur")
                elif type_releves == TypeReleve.HYDROMETRIQUE:
                    valeur = donees_releve.get("split_value")

                valeur = convertir_valeur(valeur, type_cible=float)
                # Si la valeur n'a pas pu être convertie
                if valeur is None:
                    continue

                date = None
                if type_releves == TypeReleve.HYDROMETEOROLOGIQUE:
                    date = donees_releve.get("date")
                elif type_releves == TypeReleve.HYDROMETRIQUE:
                    date = donees_releve.get("split_date")

                if not date:
                    continue

                date = date.replace(" ", "T")
                date = datetime.strptime(date, "%Y/%m/%dT%H:%M:%SZ")

                releve = {
                    "installation_id": id_installation,
                    "date": date,
                    "valeur_donnee": valeur,
                    "type_releve": type_releves,
                }
                if type_releves == TypeReleve.HYDROMETEOROLOGIQUE:
                    donnee = donees_releve.get("composition_depil_type_point_donnee")

                    releve.update(
                        {
                            "methode_mesure": donees_releve.get("composition_depil_type_mesure"),
                            "unite_donnee": donees_releve.get("composition_depil_nom_unite_mesure"),
                            "nom_donnee": donnee,
                            "type_donnee": _determiner_type_donnee(donnee, type_releve=type_releves),
                        }
                    )
                elif type_releves == TypeReleve.HYDROMETRIQUE:
                    donnee = donees_releve.get("depil_json_type_point_donnee")

                    releve.update(
                        {
                            "methode_mesure": donees_releve.get("depil_json_type_mesure"),
                            "unite_donnee": donees_releve.get("depil_json_nom_unite_mesure"),
                            "nom_donnee": donees_releve.get("depil_json_type_point_donnee"),
                            "type_donnee": _determiner_type_donnee(donnee, type_releve=type_releves),
                        }
                    )

                db.session.add(Releve(**releve))

                nb_releves_crees += 1

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

    return nb_releves_crees


def supprimer_anciens_releves(app: Flask) -> int:
    """
    Supprime tous les relevés vieux de plus de 24 heures.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (int): Le nombre de relevés supprimés.
    """

    nb_releves_supprimes = 0

    with app.app_context():
        date_jour_precedent = datetime.now(FUSEAU_HORAIRE) - timedelta(hours=24)

        try:
            nb_releves_supprimes = db.session.query(Releve).filter(Releve.date < date_jour_precedent).delete()

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

    return nb_releves_supprimes
