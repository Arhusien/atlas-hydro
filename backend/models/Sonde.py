from db import db
from enums import TypeInstallation

from .Installation import Installation


class Sonde(Installation):
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.SONDE,
    }

    ouvrage_id = db.Column(db.String(20), db.ForeignKey("installations.id"), nullable=True)

    ouvrage = db.relationship(
        "Installation",
        remote_side=[Installation.id],
        foreign_keys=[ouvrage_id],
        back_populates="sondes",
        lazy=True,
    )

    def serialiser(self, avec_releves: bool | None = False) -> dict:
        return {
            **super().serialiser(avec_releves),
            "ouvrage_id": self.ouvrage_id,
        }
