from db import db
from enums import TypeDonnee, TypeReleve
from utils import generer_snowflake


class Releve(db.Model):
    __tablename__ = "releves"

    id = db.Column(db.BigInteger, primary_key=True, default=generer_snowflake)

    installation_id = db.Column(db.String(20), db.ForeignKey("installations.id"), nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    type_releve = db.Column(db.Enum(TypeReleve), nullable=False)

    methode_mesure = db.Column(db.String)
    unite_donnee = db.Column(db.String)
    nom_donnee = db.Column(db.String)
    type_donnee = db.Column(db.Enum(TypeDonnee), nullable=False)

    valeur_donnee = db.Column(db.Float)

    def serialiser(self) -> dict:
        return {
            "id": self.id,
            "installation_id": self.installation_id,
            "date": self.date.isoformat(),
            "methode_mesure": self.methode_mesure,
            "unite_donnee": self.unite_donnee,
            "nom_donnee": self.nom_donnee,
            "type_donnee": self.type_donnee,
            "valeur_donnee": self.valeur_donnee,
        }
