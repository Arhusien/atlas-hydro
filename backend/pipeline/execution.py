from apscheduler.schedulers.background import BackgroundScheduler

from enums import JeuxDonnees
from utils import constantes

from .extraction import extraire_donnees
from .traitement import (
    traiter_hydrometeorologie,
    traiter_hydrometrie,
)


def executer_etl(app):
    print("Exécution de la pipeline ETL.")

    donnees_extraites = extraire_donnees()
    for jeu_donnees, donnees in donnees_extraites.items():
        jeu_donnees = JeuxDonnees(jeu_donnees)

        match jeu_donnees:
            case JeuxDonnees.HYDROMETEOROLOGIQUES:
                traiter_hydrometeorologie(app, donnees)
            case JeuxDonnees.HYDROMETRIQUES:
                traiter_hydrometrie(app, donnees)

    print("Pipeline ETL exécutée. Exécution à suivre dans 1 heure.")


def demarrer_cron_etl(app):
    scheduler = BackgroundScheduler(timezone=constantes.FUSEAU_HORAIRE)

    scheduler.add_job(
        func=executer_etl,
        trigger="cron",
        minute=50,
        hour="*",
        args=[app],
        id="job_pipeline_etl",
        replace_existing=True,
    )

    scheduler.start()
