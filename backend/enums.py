import enum


class TypeInstallation(enum.Enum):
    CENTRALE = "centrale"
    BARRAGE = "barrage"
    SONDE = "sonde"


class TypeReleve(enum.Enum):
    HYDROMETEOROLOGIQUE = "hydrometeorologique"
    HYDROMETRIQUE = "hydrometrique"


class JeuxDonnees(enum.Enum):
    HYDROMETEOROLOGIQUES = "donnees-hydrometeorologiques"
    HYDROMETRIQUES = "donnees-hydrometriques"
    DEMANDE_ELECTRICITE = "demande-electricite-quebec"
    PRODUCTION_ELECTRICITE = "production-electricite-quebec"
    EXPORTATIONS_ELECTRICITE = "importations-exportations-avec-transits"
