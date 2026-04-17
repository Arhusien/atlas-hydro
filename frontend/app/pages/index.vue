<template>
  <div class="w-svw h-svh">
    <LMap
      ref="map"
      :zoom="5"
      :center="[0, 0]"
      :options="mapOptions"
      @ready="onMapReady"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/copyright&quot; target=&quot;_blank&quot;>OpenStreetMap</a> contributors &amp;copy; <a href=&quot;https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/licence.html&quot; target=&quot;_blank&quot;>Hydro-Québec</a>"
        layer-type="base"
        name="OpenStreetMap"
        no-wrap
      />
      <div
        v-if="geojson.data"
      >
        <LGeoJson
          v-for="([layerName, features]) in Object.entries(geojson.data)"
          :key="layerName"
          :geojson="features"
          :options="layerOptions"
          :visible="layerStates[layerName]"
        />
      </div>
      <LControl position="topleft">
        <ControleZoom
          @zoom-in="map.leafletObject.zoomIn()"
          @zoom-out="map.leafletObject.zoomOut()"
        />
        <div class="flex flex-col items-center justify-center gap-2.5 mt-2.5">
          <SourceProductionElectricite />
          <DemandeElectricite />
          <ExportationElectricite />
        </div>
      </LControl>
      <LControl position="bottomleft">
        <div class="flex flex-col items-center justify-center gap-2.5 mb-4.25 sm:mb-0">
          <ControleCouches
            v-model="layerStates"
          />
          <CentrerQuebec
            @center="centerOnQuebec()"
          />
        </div>
      </LControl>
      <LControl position="topright">
        <div class="flex flex-col items-center justify-center gap-2.5">
          <InfosCredits />
        </div>
      </LControl>
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
        const currentMarker = activeMarker.value.feature,
              currentType = currentMarker.properties.type.toLowerCase();

        activeMarker.value.setIcon(markerIcons[currentType].default);
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

  const map = ref(null);

  const {
    data: geojson,
  } = await useFetch("/api/carte/installations", {
    // Empêcher la réactivité du GeoJSON et ainsi éviter des problèmes de performance
    transform: rawData => markRaw(rawData),
  });

  const layerOptions = {
    pointToLayer: function (feature, latlng) {
      // Ne pas afficher les installations associées à un ouvrage
      if (feature.properties.ouvrage_id) return;

      const markerType = feature.properties.type.toLowerCase();

      return L.marker(latlng, {
        title: feature.properties?.nom || "Inconnu",
        icon: markerIcons[markerType].default,
        zIndexOffset: markerZIndex[markerType] || 0,
      }).on("click", function () {
        if (activeMarker.value) {
          const previousMarker = activeMarker.value.feature,
                previousMarkerType = previousMarker.properties.type.toLowerCase();

          activeMarker.value.setIcon(markerIcons[previousMarkerType].default);
        }

        this.setIcon(markerIcons[markerType].active);
        activeMarker.value = this;

        panelInstallationOpen.value = true;
        panelInstallationData.value = feature.properties;
      });
    },
  };

  function onMapReady() {
    centerOnQuebec();

    if (installationId && installationType) {
      if (!geojson.value.data[installationType]) return;

      const selectedFeature = geojson.value.data[installationType].features.find((feature) => {
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

  onMounted(() => {
    const storedLayerStates = localStorage.getItem("layerStates");
    if (storedLayerStates) {
      layerStates.value = JSON.parse(storedLayerStates);
    }
  });

  watch(layerStates, (newValue) => {
    localStorage.setItem("layerStates", JSON.stringify(newValue));
  }, {
    deep: true,
  });
</script>
