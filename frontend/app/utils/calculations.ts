// @ts-nocheck
export function calculateDifference(releves: Array<object>, currentReleve: object, isChart: boolean = false): number | null {
    if (!releves || releves.length === 0) {
        return null;
    }

    const relevesOfSameType = isChart ? releves.toReversed() : releves[currentReleve.type_donnee].toReversed(),
        indexReleve = relevesOfSameType.findIndex(r => r.id === currentReleve.id);

    if (indexReleve <= 0) {
        return null;
    }

    const currentValue = currentReleve.valeur,
        previousValue = relevesOfSameType[indexReleve - 1].valeur;

    let delta = currentValue - previousValue;
    delta = Math.round(delta * 100) / 100;

    if (!isFinite(delta) || isNaN(delta)) {
        return null;
    }

    return delta;
}

export function calculateChartStats(data: Array<object>, localTimezone: string) {
    if (!data || data.length === 0) {
        return {
            minimum: 0,
            maximum: 0,
            average: 0,
            standardDeviation: 0,
            dateRange: [],
        };
    }

    // Calcul des statistiques de base
    const values = data.map(r => r.valeur),
        average = values.reduce((a, b) => a + b, 0) / values.length,
        minimum = Math.min(...values),
        maximum = Math.max(...values);

    // Calcul de l'écart-type
    const squaredDifferences = values.map(v => Math.pow(v - average, 2)),
        variance = squaredDifferences.reduce((a, b) => a + b, 0) / (values.length - 1),
        standardDeviation = Math.sqrt(variance);

    const dates = data.map(r => new Date(r.date)).sort((a, b) => a - b),
        dateRange = [
            formatToLocalDate(dates[0].toISOString(), localTimezone, {
                month: "2-digit",
                day: "2-digit",
                year: "numeric",
            }),
            formatToLocalDate(dates[dates.length - 1].toISOString(), localTimezone, {
                month: "2-digit",
                day: "2-digit",
                year: "numeric",
            }),
        ];

    return {
        minimum,
        maximum,
        average,
        standardDeviation,
        dateRange,
    };
}
