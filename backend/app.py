import sys

from flask import Flask

from db import db
from db.models import Installation, Releve
from scripts import sync_installations


def creer_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Si le fichier est chargé depuis la commande « sync »
        # et que la base de données est vide
        if ("sync" not in sys.argv) and (Installation.query.count() == 0):
            raise RuntimeError("Base de données vide. Exécutez 'python -m flask --app app.py sync' pour l'initialiser.")

    return app


app = creer_app()


# Définir la commande « sync » à utiliser avec le module flask
@app.cli.command("sync")
def sync_cmd():
    """
    Synchronise en base de données les installations d'Hydro-Québec.
    """

    resultat = sync_installations(app)

    print(f"Installations créées : {resultat['creees']}\nInstallations mises à jour : {resultat['mises_a_jour']}")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=5000)
