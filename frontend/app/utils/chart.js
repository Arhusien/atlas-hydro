import chartOptionsDataset from "~/utils/constants/chartOptionsDataset.json";
import chartOptions from "~/utils/constants/chartOptions.json";
import merge from "lodash/merge";
import {
    dataTypeReleveMapping,
} from "~/utils/constants/mapping.js";
import {
    fr,
} from "date-fns/locale";

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

export function buildChartOptions(releves, timezone, stats, isDetailedChart = false) {
    return merge({}, chartOptions, {
        plugins: {
            tooltip: {
                callbacks: {
                    title: ctx => createTooltipTitle(ctx, releves, timezone, isDetailedChart),
                    label: ctx => createTooltipLabel(ctx, releves, timezone, isDetailedChart),
                    afterLabel: ctx => isDetailedChart ? createTooltipAfterLabel(ctx, releves, stats) : undefined,
                },
            },
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

export function createTooltipTitle(ctx, releves, timezone, detailed = false) {
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

export function createTooltipLabel(ctx, releves, detailed = false) {
    const releve = releves[ctx.dataIndex];

    if (!detailed) {
        return releve ? `${ctx.parsed.y} ${releve.unite_valeur || ""}` : "";
    }

    return releve ? `${ctx.parsed.y.toFixed(2)} ${releve.unite_valeur || ""}` : "";
}

export function createTooltipAfterLabel(ctx, releves, stats) {
    const releve = releves[ctx.dataIndex];

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
