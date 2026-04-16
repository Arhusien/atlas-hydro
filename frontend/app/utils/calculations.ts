// @ts-nocheck
export function calculateDifference(releve: object, releves: Array<object>): number | null {
    if (!releves || releves.length === 0) {
        return null;
    }

    const indexReleve = releves.findIndex(r => r.id === releve.id);

    if (indexReleve <= 0) {
        return null;
    }

    const currentValue = releve.valeur,
        previousValue = releves[indexReleve - 1].valeur;

    let delta = currentValue - previousValue;
    delta = Math.round(delta * 100) / 100;

    if (!isFinite(delta) || isNaN(delta)) {
        return null;
    }

    return delta;
}

export function calculateChartStats(chartPoints: Array<object>, localTimezone: string) {
    if (!chartPoints || chartPoints.length === 0) {
        return {
            minimum: 0,
            maximum: 0,
            average: 0,
            standardDeviation: 0,
            dateRange: [],
        };
    }

    // Calcul des statistiques de base
    const values = chartPoints.map(p => p.y),
        average = values.reduce((a, b) => a + b, 0) / values.length,
        minimum = Math.min(...values),
        maximum = Math.max(...values);

    // Calcul de l'écart-type
    const squaredDifferences = values.map(v => Math.pow(v - average, 2)),
        variance = squaredDifferences.reduce((a, b) => a + b, 0) / (values.length - 1),
        standardDeviation = Math.sqrt(variance);

    const dates = chartPoints.map(p => new Date(p.x)).sort((a, b) => a - b),
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
