from db.db import db
from enums import TypeInstallation


class Installation(db.Model):
    __tablename__ = "installations"

    id = db.Column(db.String(20), primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(TypeInstallation), nullable=False)

    code_region = db.Column(db.String(2), nullable=False)
    nom_region = db.Column(db.String(100), nullable=False)

    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)

    releves = db.relationship("Releve", backref="installation", lazy=True)

    def serialiser(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "type": self.type.value,
            "code_region": self.code_region,
            "nom_region": self.nom_region,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }
