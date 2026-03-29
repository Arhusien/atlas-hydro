from db import db


class Releve(db.Model):
    __tablename__ = "releves"

    id = db.Column(db.Integer, primary_key=True)

    installation_id = db.Column(db.String(20), db.ForeignKey("installations.id"), nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    type_mesure = db.Column(db.String)
    unite = db.Column(db.String)
    donnee = db.Column(db.Float)

    def serialiser(self) -> dict:
        return {
            "id": self.id,
            "installation_id": self.installation_id,
            "date": self.date.isoformat(),
            "type_mesure": self.type_mesure,
            "unite": self.unite,
            "donnee": self.donnee,
        }
