from enums import TypeInstallation

from .Installation import Installation


class Barrage(Installation):
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.BARRAGE,
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
