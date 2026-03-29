from db import db
from enums import TypeInstallation

from .Installation import Installation


class Sonde(Installation):
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.SONDE,
    }

    centrale_id = db.Column(db.String(20), db.ForeignKey("installations.id"), nullable=True)

    def serialiser(self, avec_releves: bool | None = False) -> dict:
        return {
            **super().serialiser(avec_releves),
            "centrale_id": self.centrale_id,
        }
