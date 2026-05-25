from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask

import constants
from db import db
from enums import TypeDonnee, TypeReleve, TypeValeur
from models import Releve
from utils import convertir_valeur, simplifier_texte

FUSEAU_HORAIRE = ZoneInfo(constants.FUSEAU_HORAIRE)


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

    # Filtrer la liste des types de donnée pour n'y inclure que ceux du type du relevé
    types_donnees_releve = list(filter(lambda t: t.type_releve == type_releve, TypeDonnee))

    for type_donnee in types_donnees_releve:
        if simplifier_texte(type_donnee.value) in simplifier_texte(donnee):
            return type_donnee

    return TypeDonnee.INCONNU


def traiter_releves(
    app: Flask,
    lst_releves: list[dict],
    type_releves: TypeReleve,
    reconstruire_table: bool | None = False,
) -> int:
    """
    Traite et charge les relevés en base de données.

    Parameters:
        app (Flask): L'application Flask.
        lst_releves (list[dict]): La liste des relevés extraits.
        type_releves (TypeReleve): Le type de relevés.
        reconstruire_table (bool): Si la table des relevés doit être reconstruite.

    Returns:
        (int): Le nombre de relevés créés.
    """

    nb_releves_crees = 0

    with app.app_context():
        try:
            if reconstruire_table:
                # Supprimer tous les relevés pour simuler une reconstruction de la table
                db.session.query(Releve).delete()

            for releve in lst_releves:
                id_installation = releve.get("id")
                if not id_installation:
                    continue

                valeur = releve.get("valeur")
                if not valeur:
                    continue

                valeur = convertir_valeur(valeur, type_cible=float)
                # Si la valeur n'a pas pu être convertie
                if valeur is None:
                    continue

                date = releve.get("date")
                if not date:
                    continue

                date = datetime.fromisoformat(date)

                nom_donnee = releve.get("nom_donnee")
                if not nom_donnee:
                    continue

                nouveau_releve = {
                    "installation_id": id_installation,
                    "date": date,
                    "valeur": valeur,
                    "type_releve": type_releves,
                    "type_valeur": TypeValeur(releve.get("type_valeur")),
                    "unite_valeur": releve.get("unite_valeur"),
                    "nom_donnee": nom_donnee,
                    "type_donnee": _determiner_type_donnee(nom_donnee, type_releve=type_releves),
                }

                db.session.add(Releve(**nouveau_releve))

                nb_releves_crees += 1

            db.session.commit()

        except Exception:
            # Annuler les modifications faites durant l'exécution de la boucle
            db.session.rollback()
            raise

    return nb_releves_crees
