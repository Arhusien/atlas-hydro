from db import db
from enums import TypeInstallation

from .Installation import Installation


class Centrale(Installation):
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.CENTRALE,
    }

    def serialiser(
        self,
        avec_releves: bool | None = False,
        avec_releves_sondes: bool | None = False,
    ):
        return {
            **super().serialiser(avec_releves),
            "sondes": [sonde.serialiser(avec_releves_sondes) for sonde in self.sondes],
        }
