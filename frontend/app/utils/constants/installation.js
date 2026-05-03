import {
    DateTime,
} from "luxon";
import {
    TrendingUp,
    TrendingDown,
    Minus,
} from "@lucide/vue";
import {
    calculateDifference,
} from "~/utils/calculations.js";
import {
    formatToLocalDate,
} from "~/utils/formatting.js";

export const excludedDataTypesForStats = [
    "DIRECTION_VENT",
];

export const installationTabs = [
    {
        label: "Informations",
        // icon: "lucide:info",
        slot: "infos",
    },
    {
        label: "Mesures",
        // icon: "lucide:activity",
        slot: "data",

    },
    {
        label: "Graphiques",
        // icon: "lucide:satellite-dish",
        slot: "stats",
    },
];

export function buildRelevesTableColumns(releves, timezone) {
    return [
        {
            id: "date",
            accessorKey: "date",
            header: "Date",
            cell: ({ row }) => {
                return row.getValue("date")
                    ? formatToLocalDate(row.getValue("date"), timezone)
                    : "Inconnu";
            },
        },
        {
            id: "difference",
            header: "Différence",
            cell: ({ row }) => {
                const delta = calculateDifference(row.original, releves);

                if (excludedDataTypesForStats.includes(row.original.type_donnee) || delta === null) {
                    return h("div", {
                        class: "flex items-center gap-2",
                    }, [
                        h(Minus, {
                            class: "size-4.5 text-toned",
                        }),
                        h("span", {
                            class: "text-toned",
                        }, "S. O."),
                    ]);
                }

                return h("div", {
                    class: "flex items-center gap-2",
                }, [
                    delta > 0 && h(TrendingUp, {
                        class: "size-4.5 text-green-500",
                    }),
                    delta < 0 && h(TrendingDown, {
                        class: "size-4.5 text-red-500",
                    }),
                    delta === 0 && h(Minus, {
                        class: "size-4.5 text-toned",
                    }),
                    h("span", {
                        class: "text-toned",
                    }, `${Math.abs(delta).toFixed(2)} ${row.original.unite_valeur}`),
                ]);
            },
        },
        {
            id: "valeur",
            accessorKey: "valeur",
            header: "Valeur",
            cell: ({ row }) => {
                return `${row.getValue("valeur").toFixed(2)} ${row.original.unite_valeur}`;
            },
            meta: {
                class: {
                    td: "text-toned",
                },
            },
        },
    ];
}

export function shouldDisplayMeasureAlert(date) {
    const releveHour = DateTime.fromISO(date.split(":")[0]).setZone("UTC"),
        thresholdHour = DateTime.fromISO(
            DateTime.now().minus({ hours: 3 }).setZone("UTC").toISO().split(":")[0],
        );

    return releveHour <= thresholdHour;
}
