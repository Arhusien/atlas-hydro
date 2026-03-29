from db import db
from enums import TypeInstallation

from .Installation import Installation


class Centrale(Installation):
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.CENTRALE,
    }

    sondes = db.relationship(
        "Sonde",
        backref=db.backref("centrale_parente", remote_side="Installation.id"),
        foreign_keys="Sonde.centrale_id",
        lazy=True,
    )

    def serialiser(self, avec_releves: bool | None = False):
        return {
            **super().serialiser(avec_releves),
            "sondes": [sonde.serialiser(avec_releves) for sonde in self.sondes],
        }
