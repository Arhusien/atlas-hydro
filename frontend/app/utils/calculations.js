/**
 * Calcul la différence de la valeur d'un relevé et le relevé précédent.
 * @param {Object} releve - Le relevé pour lequel calculer la différence.
 * @param {Array} releves - La liste des relevés à laquelle appartient le relevé.
 * @returns {number | null} La différence calculée ou une valeur nulle.
*/
export function calculateDifference(releve, releves) {
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

/**
 * Calcule les statistiques de base et la plage de dates d'un ensemble de points de données d'un graphique.
 * @param {Array} chartPoints - Les points (x; y) de données du graphique.
 * @param {string} timezone - Le fuseau horaire cible.
 * @returns {Object} Un objet contenant les statistiques calculées et la plage de dates.
 */
export function calculateChartStats(chartPoints, timezone) {
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

    // Trier les dates par ordre croissant
    const dates = chartPoints.map(p => new Date(p.x)).sort((a, b) => a - b),
        dateRange = [
            formatToLocalDate(dates[0].toISOString(), timezone, {
                month: "2-digit",
                day: "2-digit",
                year: "numeric",
            }),
            formatToLocalDate(dates[dates.length - 1].toISOString(), timezone, {
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
