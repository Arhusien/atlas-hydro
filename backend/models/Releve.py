from db import db
from enums import TypeDonnee, TypeReleve, TypeValeur
from utils import generer_snowflake


class Releve(db.Model):
    __tablename__ = "releves"

    id = db.Column(db.BigInteger, primary_key=True, default=generer_snowflake)

    installation_id = db.Column(db.String(20), db.ForeignKey("installations.id"), nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    type_releve = db.Column(db.Enum(TypeReleve), nullable=False)

    unite_valeur = db.Column(db.String)
    nom_donnee = db.Column(db.String)
    type_donnee = db.Column(db.Enum(TypeDonnee), nullable=False)

    type_valeur = db.Column(db.Enum(TypeValeur), nullable=False)
    valeur = db.Column(db.Float)

    def serialiser(self) -> dict:
        return {
            "id": str(self.id),
            "installation_id": self.installation_id,
            "date": self.date.isoformat(),
            "type_releve": self.type_releve.name,
            "unite_valeur": self.unite_valeur,
            "nom_donnee": self.nom_donnee,
            "type_donnee": self.type_donnee.name,
            "type_valeur": self.type_valeur.name,
            "valeur": self.valeur,
        }
