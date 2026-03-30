from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from enums import JeuxDonnees, TypeReleve
from utils import constantes

from .extraction import extraire_releves
from .traitement import supprimer_anciens_releves, traiter_releves


def executer_pipeline(app: Flask):
    """
    Exécute la pipeline ETL (Extract-transform-load).

    Cette pipeline extrait les données des jeux de données d'Hydro-Québec, les traite et les charge en base de données.

    Parameters:
        app (Flask): L'application Flask.
    """

    print("Exécution de la pipeline ETL.")

    supprimer_anciens_releves(app)

    donnees_extraites = extraire_releves()
    for jeu_donnees, donnees in donnees_extraites.items():
        jeu_donnees = JeuxDonnees(jeu_donnees)

        match jeu_donnees:
            case JeuxDonnees.HYDROMETEOROLOGIQUES:
                traiter_releves(app, lst_releves=donnees, type_releves=TypeReleve.HYDROMETEOROLOGIQUE)
            case JeuxDonnees.HYDROMETRIQUES:
                traiter_releves(app, lst_releves=donnees, type_releves=TypeReleve.HYDROMETRIQUE)

    print("Pipeline ETL exécutée. Exécution à suivre dans 1 heure.")


def demarrer_cron_pipeline(app: Flask):
    """
    Démarre la cron job de la pipeline ETL.

    La pipeline s'exécutera automatiquement toutes les heures à la 10ème minute.

    Parameters:
        app (Flask): L'application Flask.
    """

    scheduler = BackgroundScheduler(timezone=constantes.FUSEAU_HORAIRE)

    scheduler.add_job(
        func=executer_pipeline,
        trigger="cron",
        minute=10,
        hour="*",
        args=[app],
        id="job_pipeline_etl",
        replace_existing=True,
    )

    scheduler.start()
