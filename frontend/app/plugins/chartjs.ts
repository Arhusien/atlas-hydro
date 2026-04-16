import {
    Chart,
    registerables,
} from "chart.js";
import "chartjs-adapter-date-fns";

let isChartRegistered = false;

export default defineNuxtPlugin(() => {
    if (isChartRegistered) return;

    Chart.register(...registerables);
    Chart.defaults.font.family = "'Inter', sans-serif";

    isChartRegistered = true;
});
