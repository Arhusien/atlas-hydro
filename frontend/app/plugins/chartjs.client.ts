import Zoom from "chartjs-plugin-zoom";
import "chartjs-adapter-date-fns";
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
        Zoom,
    );

    Chart.defaults.font.family = "'Inter', sans-serif";

    isChartRegistered = true;
});
