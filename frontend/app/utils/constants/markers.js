import L from "leaflet";
import satellitePin from "~/assets/img/pins/satellitePin.svg?url";
import satellitePinActive from "~/assets/img/pins/satellitePinActive.svg?url";
import factoryPin from "~/assets/img/pins/factoryPin.svg?url";
import factoryPinActive from "~/assets/img/pins/factoryPinActive.svg?url";
import damPin from "~/assets/img/pins/damPin.svg?url";
import damPinActive from "~/assets/img/pins/damPinActive.svg?url";
import pinShadow from "~/assets/img/pins/pinShadow.svg?url";

const markerOptions = {
    className: "marker-icon",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
    shadowUrl: pinShadow,
    shadowSize: [32, 36],
    shadowAnchor: [16, 32],
};

export const markers = {
    centrale: {
        default: L.icon({
            ...markerOptions,
            iconUrl: factoryPin,
        }),
        active: L.icon({
            ...markerOptions,
            iconUrl: factoryPinActive,
        }),
        zIndex: 9999,
    },
    barrage: {
        default: L.icon({
            ...markerOptions,
            iconUrl: damPin,
        }),
        active: L.icon({
            ...markerOptions,
            iconUrl: damPinActive,
        }),
        zIndex: 4999,
    },
    sonde: {
        default: L.icon({
            ...markerOptions,
            iconUrl: satellitePin,
        }),
        active: L.icon({
            ...markerOptions,
            iconUrl: satellitePinActive,
        }),
        zIndex: 0,
    },
};
