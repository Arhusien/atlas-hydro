from enum import Enum


class TypeInstallation(Enum):
    CENTRALE = "centrale"
    SONDE = "sonde"


class TypeReleve(Enum):
    HYDROMETEOROLOGIQUE = "hydrometeorologique"
    HYDROMETRIQUE = "hydrometrique"


class TypeDonnee(Enum):
    # Données hydrométriques
    DEBIT_TURBINE = "Débit turbiné"
    DEBIT_DEVERSE = "Débit déversé"
    DEBIT_TOTAL = "Débit total"
    APPORT_FILTRE = "Apport filtré"

    # Données hydrométéorologiques
    TEMPERATURE_EAU = "Température de l'eau"
    TEMPERATURE_MIN = "Température Minimum"
    TEMPERATURE_MAX = "Température Maximum"
    VITESSE_VENT = "Vitesse du vent"
    DIRECTION_VENT = "Direction du vent"
    PRECIPITATION = "Précipitation"
    EPAISSEUR_NEIGE = "Épaisseur de neige"
    EQUIVALENT_EAU_NEIGE = "Équivalent en eau de la neige"
    HUMIDITE_RELATIVE = "Humidité relative"
    DEBIT_FLUVIAL = "Débit"
    NIVEAU_EAU = "Niveau"

    INCONNU = "Inconnu"

    @property
    def type_releve(self):
        # Les types possibles des données des relevés hydrométriques
        types_donnees_releves_hydrometriques = {
            TypeDonnee.DEBIT_TURBINE,
            TypeDonnee.DEBIT_DEVERSE,
            TypeDonnee.DEBIT_TOTAL,
            TypeDonnee.APPORT_FILTRE,
        }

        if self == TypeDonnee.INCONNU:
            return None
        elif self in types_donnees_releves_hydrometriques:
            return TypeReleve.HYDROMETRIQUE

        return TypeReleve.HYDROMETEOROLOGIQUE

    @classmethod
    def _missing_(cls, valeur):
        return cls.INCONNU


class TypeValeur(Enum):
    INSTANTANE = "Instantanée"
    MAXIMUM = "Maximum"
    MINIMUM = "Minimum"
    MOYENNE = "Moyenne"
    SOMME = "Somme"

    INCONNU = "Inconnu"

    @classmethod
    def _missing_(cls, valeur):
        return cls.INCONNU


class JeuDonnees(Enum):
    HYDROMETEOROLOGIQUES = "donnees-hydrometeorologiques"
    HYDROMETRIQUES = "donnees-hydrometriques"
