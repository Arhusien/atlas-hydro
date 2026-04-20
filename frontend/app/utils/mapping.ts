export const installationTypeMapping = {
    CENTRALE: "Centrale",
    BARRAGE: "Barrage",
    SONDE: "Sonde",
};

export const releveTypeMapping = {
    HYDROMETEOROLOGIQUE: "Hydrométéorologique",
    HYDROMETRIQUE: "Hydrométrique",
};

export const dataTypeReleveMapping = {
    DEBIT_TURBINE: "Débit turbiné",
    DEBIT_DEVERSE: "Débit déversé",
    DEBIT_TOTAL: "Débit total",
    APPORT_FILTRE: "Apports filtrés",
    TEMPERATURE_EAU: "Température de l'eau",
    TEMPERATURE_MIN: "Température minimale",
    TEMPERATURE_MAX: "Température maximale",
    VITESSE_VENT: "Vitesse du vent",
    DIRECTION_VENT: "Direction du vent",
    PRECIPITATION: "Précipitations",
    EPAISSEUR_NEIGE: "Épaisseur du manteau neigeux",
    EQUIVALENT_EAU_NEIGE: "Équivalent en eau de la neige",
    HUMIDITE_RELATIVE: "Humidité relative",
    DEBIT_FLUVIAL: "Débit en rivière",
    NIVEAU_EAU: "Niveau de l'eau",
};

export const valueTypeMapping = {
    INSTANTANE: "Valeurs instantanées",
    MAXIMUM: "Valeurs maximales",
    MINIMUM: "Valeurs minimales",
    MOYENNE: "Valeurs moyennes",
    SOMME: "Sommations",
};

export const bigChartStatsMapping = {
    average: "Moyenne",
    minimum: "Minimum",
    maximum: "Maximum",
    standardDeviation: "Écart-type",
};

export const electicityTypeMapping = {
    hydraulique: "Hydraulique",
    hydro: "Hydraulique",
    wind: "Éolien",
    eolien: "Éolien",
    nucleaire: "Nucléaire",
    nuclear: "Nucléaire",
    solaire: "Solaire",
    solar: "Solaire",
    thermique: "Thermique",
    geothermique: "Géothermique",
    biomasse: "Biomasse",
    biomass: "Biomasse",
    autres: "Autres",
    gas: "Gaz",
    oil: "Pétrole",
    other: "Autres",
    unknown: "Inconnu",
};

export const renewableElectricityTypes = [
    "hydraulique",
    "hydro",
    "wind",
    "eolien",
    "solaire",
    "solar",
    "geothermique",
    "biomasse",
    "biomass",
];
