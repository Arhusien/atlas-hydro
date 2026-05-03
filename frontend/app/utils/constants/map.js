import L from "leaflet";

export const mapViewTabs = [
    {
        label: "Installations",
        value: "installations",
    },
    {
        label: "Territoires",
        value: "territoires",
    },
];

export const availableViews = [
    "installations",
    "territoires",
];

export const quebecBounds = L.latLngBounds(
    L.latLng(45.0, -80.0), // Gatineau/Abitibi
    L.latLng(62.5, -57.0), // Nunavik/Blanc-Sablon
);

export const worldBounds = L.latLngBounds(
    L.latLng(-90, -180), // Sud-Ouest
    L.latLng(90, 180), // Nord-Est
);

export const mapOptions = {
    zoomControl: false,
    minZoom: 3,
    maxBounds: worldBounds,
    maxBoundsViscosity: 1.0,
};

export const initialMapCenter = [0, 0];

export const initialZoom = 5;

export const regionStyle = {
    default: {
        fillColor: "var(--ui-color-neutral-500)",
        fillOpacity: 0.2,
        color: "var(--ui-color-neutral-600)",
        opacity: 0.8,
        weight: 1,
    },
    active: {
        fillOpacity: 0.35,
        opacity: 0.75,
    },
};

export function setRegionInactive(layer) {
    layer.setStyle(regionStyle.default);
}

export function setRegionActive(layer) {
    layer.setStyle(regionStyle.active);
    layer.bringToFront();
}

export function centerOnQuebec(map) {
    map.flyToBounds(quebecBounds, {
        animate: false,
        padding: [50, 50],
    });
};
