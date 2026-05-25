from enums import TypeInstallation

from .Installation import Installation


class Barrage(Installation):
    # Associer le type Barrage au modèle
    __mapper_args__ = {
        "polymorphic_identity": TypeInstallation.BARRAGE,
    }

    def serialiser(
        self,
        avec_releves: bool | None = False,
        avec_releves_sondes: bool | None = False,
    ):
        """
        Transforme les données de l'installation en objet JSON.

        Parameters:
            avec_releves (bool, optionel): Si l'objet doit inclure tous les relevés de l'installation.
            avec_releves_sondes (bool, optionel): Si l'objet doit inclure tous les relevés des sondes associées.

        Returns:
            (dict): Les données de l'installation en objet JSON.
        """

        return {
            **super().serialiser(avec_releves),
            "sondes": [sonde.serialiser(avec_releves_sondes) for sonde in self.sondes],
        }
