import chartOptionsDataset from "~/utils/constants/chartOptionsDataset.json";
import chartOptions from "~/utils/constants/chartOptions.json";
import merge from "lodash/merge";
import {
    dataTypeReleveMapping,
} from "~/utils/constants/mapping.js";
import {
    fr,
} from "date-fns/locale";

/**
 * Construit un objet de données pour un graphique Chart.js.
 * @param {Array} chartPoints - Les coordonnées (x; y) à inclure dans le graphique.
 * @param {string} type_releves - Le type de relevés pour lequel est construit le graphique.
 * @returns {Object} Un objet de données formaté pour Chart.js.
 */
export function buildChartData(chartPoints, type_releves) {
    return {
        datasets: [
            {
                ...chartOptionsDataset,
                label: dataTypeReleveMapping[type_releves] || "Inconnu",
                data: chartPoints,
            },
        ],
    };
}

/**
 * Construit un objet d'options pour un graphique Chart.js.
 * @param {Array} releves - Les relevés pour lesquels construire le graphique.
 * @param {string} timezone - Le fuseau horaire cible.
 * @param {Object} stats - Les statistiques des relevés.
 * @param {boolean} isDetailedChart - Si le graphique est sous sa forme détaillé.
 * @returns {Object} Un objet d'options formaté pour Chart.js.
 */
export function buildChartOptions(releves, timezone, stats, isDetailedChart = false) {
    return merge({}, chartOptions, {
        plugins: {
            tooltip: {
                callbacks: {
                    title: ctx => _createTooltipTitle(ctx, releves, timezone, isDetailedChart),
                    label: ctx => _createTooltipLabel(ctx, releves, timezone, isDetailedChart),
                    afterLabel: ctx => isDetailedChart ? _createTooltipAfterLabel(ctx, releves, stats) : undefined,
                },
            },
            zoom: isDetailedChart
                ? {
                    limits: {
                        x: {
                            min: "original",
                            max: "original",
                        },
                    },
                    pan: {
                        enabled: true,
                        mode: "x",
                        threshold: 8,
                    },
                    zoom: {
                        wheel: {
                            enabled: true,
                            // modifierKey: "ctrl",
                        },
                        pinch: {
                            enabled: true,
                        },
                        mode: "x",
                    },
                }
                : undefined,
        },
        scales: {
            x: {
                ticks: {
                    display: isDetailedChart,
                },
                adapters: {
                    date: {
                        locale: fr,
                    },
                },
            },
        },
    });
}

function _createTooltipTitle(ctx, releves, timezone, detailed = false) {
    const releve = releves[ctx[0].dataIndex];

    if (!detailed) {
        return releve ? formatToLocalDate(releve.date, timezone) : "";
    }

    return releve
        ? formatToLocalDate(releve.date, timezone, {
            year: "numeric",
            month: "long",
        })
        : "";
}

function _createTooltipLabel(ctx, releves, detailed = false) {
    const releve = releves[ctx.dataIndex];

    if (!detailed) {
        return releve ? `${ctx.parsed.y} ${releve.unite_valeur || ""}` : "";
    }

    return releve ? `${ctx.parsed.y.toFixed(2)} ${releve.unite_valeur || ""}` : "";
}

function _createTooltipAfterLabel(ctx, releves, stats) {
    const releve = releves[ctx.dataIndex];

    // Calcul des statistiques du relevé
    const difference = calculateDifference(releve, releves),
        zScore = (releve.valeur - stats.average) / (stats.standardDeviation || 1);

    let labels = [];
    if (difference !== null) {
        labels.push(`Différence : ${difference === 0 ? "" : difference > 0 ? "+" : "-"}${Math.abs(difference).toFixed(2)} ${releve.unite_valeur || ""}`);
    }
    if (isFinite(zScore)) {
        labels.push(`Cote Z : ${zScore === 0 ? "" : zScore > 0 ? "+" : "-"}${Math.abs(zScore).toFixed(2)}`);
    }

    return labels.length > 0 ? labels.join("\n") : "";
}
