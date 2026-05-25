import signal
import sys
import threading

from app import app
from pipeline import demarrer_cron_pipeline

if __name__ == "__main__":
    est_arrete = threading.Event()
    planificateur = None

    def gerer_arret(*args):
        print("Arrêt en cours...")

        # Si le planificateur a été initialisé
        if planificateur is not None:
            planificateur.shutdown(wait=False)

        # Arrêter le bloquage du processus
        est_arrete.set()

    # Quitter le processus si le terminal en envoie l'évènement
    signal.signal(signal.SIGTERM, gerer_arret)
    signal.signal(signal.SIGINT, gerer_arret)

    planificateur = demarrer_cron_pipeline(app)

    # Bloquer le processus pour "garder en vie" le conteneur Docker
    while not est_arrete.is_set():
        est_arrete.wait(timeout=1)

    # Lorsque le processus est débloqué, arrêter l'exécution
    sys.exit(0)
