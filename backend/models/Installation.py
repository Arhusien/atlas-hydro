from db import db
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

    sondes = db.relationship(
        "Sonde",
        back_populates="ouvrage",
        foreign_keys="Sonde.ouvrage_id",
        lazy=True,
    )

    # Baser l'héritage des modèles sur le type de l'installation
    __mapper_args__ = {
        "polymorphic_on": type,
    }

    def serialiser(self, avec_releves: bool | None = False) -> dict:
        """
        Transforme les données de l'installation en objet JSON.

        Parameters:
            avec_releves (bool, optionel): Si l'objet doit inclure tous les relevés de l'installation.

        Returns:
            (dict): Les données de l'installation en objet JSON.
        """

        donnees = {
            "id": self.id,
            "nom": self.nom,
            "type": self.type.name,
            "code_region": self.code_region,
            "nom_region": self.nom_region,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

        if avec_releves:
            donnees.update(
                {
                    "releves": [releve.serialiser() for releve in self.releves],
                }
            )

        return donnees
