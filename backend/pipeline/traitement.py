from datetime import datetime, timedelta, timezone

from flask import Flask

from db import db
from db.models import Releve
from enums import TypeReleve
from utils import convertir_valeur


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
        date_jour_precedent = datetime.now(timezone.utc) - timedelta(hours=24)

        nb_releves_supprimes = db.session.query(Releve).filter(Releve.date < date_jour_precedent).delete()

    return nb_releves_supprimes


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
                    if date:
                        date = datetime.strptime(date, "%Y/%m/%d %H:%M:%SZ")
                elif type_releves == TypeReleve.HYDROMETRIQUE:
                    date = donees_releve.get("split_date")
                    if date:
                        date = datetime.strptime(date, "%Y/%m/%dT%H:%M:%SZ")

                if not date:
                    continue

                releve = {
                    "installation_id": id_installation,
                    "date": date,
                    "valeur": valeur,
                }
                if type_releves == TypeReleve.HYDROMETEOROLOGIQUE:
                    releve.update(
                        {
                            "type_mesure": donees_releve.get("composition_depil_type_mesure"),
                            "unite": donees_releve.get("composition_depil_nom_unite_mesure"),
                            "donnee": donees_releve.get("composition_depil_type_point_donnee"),
                        }
                    )
                elif type_releves == TypeReleve.HYDROMETRIQUE:
                    releve.update(
                        {
                            "type_mesure": donees_releve.get("depil_json_type_mesure"),
                            "unite": donees_releve.get("depil_json_nom_unite_mesure"),
                            "donnee": donees_releve.get("depil_json_type_point_donnee"),
                        }
                    )

                db.session.add(Releve(**releve))

                nb_releves_crees += 1

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

    return nb_releves_crees
