from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from enums import JeuDonnees, TypeReleve

from .extraction import extraire_releves
from .traitement import traiter_releves


def executer_pipeline(app: Flask):
    """
    Exécute la pipeline ETL (Extract-transform-load).

    Cette pipeline extrait les données des jeux de données d'Hydro-Québec, les traite et les charge en base de données.

    Parameters:
        app (Flask): L'application Flask.
    """

    print("Exécution de la pipeline ETL.")

    donnees_extraites = extraire_releves()

    est_premiere_iteration = True
    for jeu_donnees, donnees in donnees_extraites.items():
        jeu_donnees = JeuDonnees(jeu_donnees)
        type_releves = (
            TypeReleve.HYDROMETEOROLOGIQUE
            if jeu_donnees == JeuDonnees.HYDROMETEOROLOGIQUES
            else TypeReleve.HYDROMETRIQUE
        )

        traiter_releves(
            app,
            lst_releves=donnees,
            type_releves=type_releves,
            reconstruire_table=est_premiere_iteration,
        )

        est_premiere_iteration = False

    print("Pipeline ETL exécutée. Exécution à suivre dans 1 heure.")


def demarrer_cron_pipeline(app: Flask):
    """
    Démarre la cron job de la pipeline ETL.

    La pipeline s'exécutera automatiquement toutes les heures à la 10ème minute.

    Parameters:
        app (Flask): L'application Flask.

    Returns:
        (BackgroundScheduler): Le planificateur de la cron job.
    """

    planificateur = BackgroundScheduler(timezone="America/Toronto")

    planificateur.add_job(
        func=executer_pipeline,
        trigger="cron",
        minute=10,
        hour="*",
        args=[app],
        id="job_pipeline_etl",
        replace_existing=True,
    )

    print("La pipeline ETL s'exécutera automatiquement toutes les heures à la 10ème minute.")

    planificateur.start()

    return planificateur
