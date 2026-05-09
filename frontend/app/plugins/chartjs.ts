import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    TimeScale,
    CategoryScale,
    Tooltip,
    Filler,

} from "chart.js";
import "chartjs-adapter-date-fns";

let isChartRegistered = false;

export default defineNuxtPlugin(() => {
    if (isChartRegistered) return;

    // Charger les composants utilisés
    Chart.register(
        LineController,
        LineElement,
        PointElement,
        LinearScale,
        TimeScale,
        CategoryScale,
        Tooltip,
        Filler,
    );

    Chart.defaults.font.family = "'Inter', sans-serif";

    isChartRegistered = true;
});
