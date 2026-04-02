import os
import sys

from flask import Flask

from db import db
from models import Installation
from pipeline import demarrer_cron_pipeline, executer_pipeline
from services.synchronisation_service import associer_sondes_centrales, synchroniser_installations

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

with app.app_context():
    db.create_all()

    # Si le fichier n'est pas chargé depuis la commande "synchroniser_installations"
    # et que la base de données est vide
    if ("synchroniser_installations" not in sys.argv) and (Installation.query.count() == 0):
        raise RuntimeError(
            "Base de données vide. Exécutez 'python -m flask --app app.py synchroniser_installations' pour l'initialiser."
        )

# En mode développement, lancer l'exécution de l'ETL seulement sur le processus principale
# En production, il n'y a qu'un seul processus qui exécute le code
if (os.environ.get("WERKZEUG_RUN_MAIN") == "true") or (not app.config["DEBUG"]):
    demarrer_cron_pipeline(app)


# Définir la commande "synchroniser_installations" à utiliser avec le module flask
@app.cli.command("synchroniser_installations")
def synchroniser_installations_cmd():
    stats_synchronisation = synchroniser_installations(app)
    nb_associations = associer_sondes_centrales(app)

    print(
        f"Installations créées : {stats_synchronisation['creees']}\n"
        + f"Installations mises à jour : {stats_synchronisation['mises_a_jour']}\n"
        + f"Nombre d'associations : {nb_associations}\n"
        + f"Temps d'exécution : {round(stats_synchronisation['temps'], 2)} s",
    )


@app.cli.command("executer_pipeline")
def executer_pipeline_cmd():
    executer_pipeline(app)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=5000)
