import os
import sys

from flask import Flask

from db import db
from db.models import Installation
from pipeline import demarrer_cron_etl, executer_etl
from services.installations_service import associer_sondes_aux_centrales, synchroniser_installations

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

with app.app_context():
    db.create_all()

    # Si le fichier est chargé depuis la commande "sync_installations"
    # et que la base de données est vide
    if ("sync_installations" not in sys.argv) and (Installation.query.count() == 0):
        raise RuntimeError(
            "Base de données vide. Exécutez 'python -m flask --app app.py sync_installations' pour l'initialiser."
        )

# En mode développement, lancer l'exécution de l'ETL seulement sur le processus principale
# En production, il n'y a qu'un seul processus qui exécute le code
if (os.environ.get("WERKZEUG_RUN_MAIN") == "true") or (not app.config["DEBUG"]):
    demarrer_cron_etl(app)


# Définir la commande "sync_installations" à utiliser avec le module flask
@app.cli.command("sync_installations")
def sync_installations_cmd():
    """
    Synchronise en base de données les installations d'Hydro-Québec.
    """

    resultat = synchroniser_installations(app)
    nb_associations = associer_sondes_aux_centrales(app)

    print(
        f"Installations créées : {resultat['creees']}\n"
        + f"Installations mises à jour : {resultat['mises_a_jour']}\n"
        + f"Nombre d'associations : {nb_associations}\n"
        + f"Temps d'exécution : {round(resultat['temps'], 2)} s",
    )


@app.cli.command("executer_etl")
def executer_etl_cmd():
    """
    Exécute la pipeline ETL.
    """

    executer_etl(app)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=5000)
