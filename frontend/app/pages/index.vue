<template>
  <div class="w-svw h-svh relative">
    <div
      class="absolute py-4 left-4 z-1000 flex flex-col items-center justify-between h-full"
    >
      <ControleZoom
        @zoom-in="map.leafletObject.zoomIn()"
        @zoom-out="map.leafletObject.zoomOut()"
      />
      <div class="flex flex-col items-center justify-center gap-2.5">
        <ControleCouches
          v-model="layerStates"
        />
        <CentrerQuebec
          @center="centerOnQuebec()"
        />
      </div>
    </div>
    <div class="flex flex-col items-center justify-center gap-2.5 absolute top-4 right-4 z-1000">
      <InfosCredits />
    </div>
    <div class="flex items-center justify-center gap-2.5 absolute top-4 left-1/2 -translate-x-1/2 z-1000 w-full pointer-events-none">
      <DonneesElectricite
        :data="elecricityData"
        :disabled="!elecricityData"
        :dragging="dragging"
      />
    </div>
    <LMap
      ref="map"
      :zoom="zoom"
      :center="[0, 0]"
      :options="mapOptions"
      @ready="onMapReady"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/copyright&quot; target=&quot;_blank&quot;>OpenStreetMap</a> contributors</a>"
        layer-type="base"
        name="OpenStreetMap"
        no-wrap
      />
      <div
        v-if="geojson"
      >
        <LGeoJson
          v-for="([layerName, features]) in Object.entries(geojson)"
          :key="layerName"
          :geojson="features"
          :options="layerOptions"
          :visible="layerStates[layerName]"
        />
      </div>
    </LMap>
    <PanelInstallation
      v-model="panelInstallationOpen"
      :default-data="panelInstallationData"
    />
  </div>
</template>

<script setup>
  import L from "leaflet";
  import satellitePin from "~/assets/img/satellitePin.svg?url";
  import satellitePinActive from "~/assets/img/satellitePinActive.svg?url";
  import factoryPin from "~/assets/img/factoryPin.svg?url";
  import factoryPinActive from "~/assets/img/factoryPinActive.svg?url";
  import damPin from "~/assets/img/damPin.svg?url";
  import damPinActive from "~/assets/img/damPinActive.svg?url";
  import pinShadow from "~/assets/img/pinShadow.svg?url";

  const route = useRoute(),
        installationId = route.query.installation,
        installationType = route.query.type;

  const panelInstallationOpen = ref(false),
        panelInstallationData = ref({});

  const activeMarker = ref(null);

  const elecricityData = ref(null);

  const layerStates = ref({
    centrale: true,
    barrage: true,
    sonde: true,
  });

  const markerIconOptions = {
    className: "marker-icon",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
    shadowUrl: pinShadow,
    shadowSize: [32, 36],
    shadowAnchor: [16, 32],
  };

  const markerIcons = {
    centrale: {
      default: L.icon({
        ...markerIconOptions,
        iconUrl: factoryPin,
      }),
      active: L.icon({
        ...markerIconOptions,
        iconUrl: factoryPinActive,
      }),
    },
    barrage: {
      default: L.icon({
        ...markerIconOptions,
        iconUrl: damPin,
      }),
      active: L.icon({
        ...markerIconOptions,
        iconUrl: damPinActive,
      }),
    },
    sonde: {
      default: L.icon({
        ...markerIconOptions,
        iconUrl: satellitePin,
      }),
      active: L.icon({
        ...markerIconOptions,
        iconUrl: satellitePinActive,
      }),
    },
  };

  const markerZIndex = {
    centrale: 9999,
    barrage: 4999,
    sonde: 0,
  };

  watch(panelInstallationOpen, (newValue) => {
    if (newValue === false) {
      if (activeMarker.value) {
        const marker = activeMarker.value.feature,
              markerType = marker.properties.type.toLowerCase();

        activeMarker.value.setIcon(markerIcons[markerType].default);
        activeMarker.value = null;
      }
    }
  });

  const quebecBounds = L.latLngBounds(
          L.latLng(45.0, -80.0), // Gatineau/Abitibi
          L.latLng(62.5, -57.0), // Nunavik/Blanc-Sablon
        ),
        worldBounds = L.latLngBounds(
          L.latLng(-90, -180), // Sud-Ouest
          L.latLng(90, 180), // Nord-Est
        );

  const mapOptions = {
    zoomControl: false,
    minZoom: 3,
    maxBounds: worldBounds,
    maxBoundsViscosity: 1.0,
  };

  const map = ref(null),
        zoom = ref(5),
        dragging = ref(false);

  const mapRes = await $fetch("/api/carte/installations");
  if (mapRes.status !== 200) {
    throw createError({
      statusCode: mapRes.status,
      message: mapRes.message,
    });
  }

  // Empêcher la réactivité du GeoJSON et ainsi éviter des problèmes de performance
  const geojson = markRaw(mapRes.data);

  const layerOptions = {
    pointToLayer: function (feature, latlng) {
      // Ne pas afficher les installations associées à un ouvrage
      if (feature.properties.ouvrage_id) return;

      const markerType = feature.properties.type.toLowerCase();

      return L.marker(latlng, {
        title: feature.properties?.nom || "Inconnu",
        icon: markerIcons[markerType].default,
        zIndexOffset: markerZIndex[markerType] || 0,
      }).on("click", async function () {
        await openInstallation(this, feature);
      });
    },
  };

  async function openInstallation(marker, feature) {
    if (panelInstallationOpen.value) {
      panelInstallationOpen.value = false;
      await nextTick();
    }

    const markerType = feature.properties.type.toLowerCase();

    marker.setIcon(markerIcons[markerType].active);
    activeMarker.value = marker;

    panelInstallationData.value = feature.properties;
    panelInstallationOpen.value = true;
  }

  function onMapReady() {
    centerOnQuebec();

    map.value.leafletObject.on("dragstart", () => {
      dragging.value = true;
    });

    map.value.leafletObject.on("dragend", () => {
      dragging.value = false;
    });

    if (installationId && installationType) {
      if (!geojson[installationType]) return;

      const selectedFeature = geojson[installationType].features.find((feature) => {
        return feature.properties.objectid === installationId;
      });

      if (selectedFeature) {
        panelInstallationData.value = selectedFeature.properties;
        panelInstallationOpen.value = true;
      }
    }
  };

  function centerOnQuebec() {
    map.value.leafletObject.flyToBounds(quebecBounds, {
      animate: false,
      padding: [50, 50],
    });
  };

  onMounted(async () => {
    const storedLayerStates = localStorage.getItem("layerStates");
    if (storedLayerStates) {
      layerStates.value = JSON.parse(storedLayerStates);
    }

    const elecricityRes = await $fetch("/api/electricite");
    if (elecricityRes.status !== 200) {
      throw createError({
        statusCode: elecricityRes.status,
        message: elecricityRes.message,
      });
    }

    elecricityData.value = elecricityRes.data;
  });

  watch(layerStates, (newValue) => {
    localStorage.setItem("layerStates", JSON.stringify(newValue));
  }, {
    deep: true,
  });
</script>
