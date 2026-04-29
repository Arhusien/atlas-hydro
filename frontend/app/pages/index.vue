<template>
  <div
    class="w-svw h-svh relative"
    style="contain: layout paint;"
  >
    <div class="flex flex-col items-center justify-center gap-2.5 absolute top-4 left-4 z-1000">
      <ControleZoom
        @zoom-in="map.leafletObject.zoomIn()"
        @zoom-out="map.leafletObject.zoomOut()"
      />
    </div>
    <div class="flex flex-col items-center justify-center gap-2.5 absolute bottom-4 left-4 z-1000">
      <ControleCouches
        v-model="layerStates"
      />
      <CentrerQuebec
        @center="centerOnQuebec()"
      />
    </div>
    <div class="flex flex-col items-center justify-center gap-2.5 absolute top-4 right-4 z-1000">
      <InfosCredits />
    </div>
    <div class="flex items-center justify-center gap-2.5 absolute top-4 left-1/2 -translate-x-1/2 z-1000">
      <UTabs
        v-model="mapMode"
        color="neutral"
        variant="pill"
        :content="false"
        :items="mapModeTabs"
        :ui="{
          list: 'bg-default',
          trigger: 'cursor-pointer',
        }"
      />
    </div>
    <LMap
      ref="map"
      class="isolate"
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
      <LGeoJson
        ref="regionLayers"
        :geojson="geojsonRegions"
        :options="regionsLayerOptions"
        :options-style="regionsStyle"
        :visible="mapMode === 'regions'"
      />
      <div v-if="displayedGeojson">
        <LGeoJson
          v-for="([layerName, features]) in Object.entries(displayedGeojson)"
          :key="layerName"
          :geojson="features"
          :options="mapLayerOptions"
          :visible="layerStates[layerName] && mapMode === 'installations'"
        />
      </div>
    </LMap>
    <InstallationPanel
      v-model="installationPanelOpen"
      :default-data="installationPanelData"
    />
    <ElectricityPanel
      v-model="electricityPanelOpen"
      :region="activeRegion"
      :data="elecricityData"
    />
  </div>
</template>

<script setup>
  import L from "leaflet";
  import satellitePin from "~/assets/img/pins/satellitePin.svg?url";
  import satellitePinActive from "~/assets/img/pins/satellitePinActive.svg?url";
  import factoryPin from "~/assets/img/pins/factoryPin.svg?url";
  import factoryPinActive from "~/assets/img/pins/factoryPinActive.svg?url";
  import damPin from "~/assets/img/pins/damPin.svg?url";
  import damPinActive from "~/assets/img/pins/damPinActive.svg?url";
  import pinShadow from "~/assets/img/pins/pinShadow.svg?url";

  const validMapModes = [
    "installations",
    "regions",
  ];

  const route = useRoute(),
        router = useRouter(),
        installationId = route.query.installation,
        installationType = route.query.type,
        regionId = route.query.region;

  const installationPanelOpen = ref(false),
        installationPanelData = ref({}),
        electricityPanelOpen = ref(false);

  const elecricityData = ref(null);

  const activeMarker = ref(null),
        activeRegion = ref(null),
        activeRegionLayer = ref(null);

  const mapMode = computed({
    get() {
      return validMapModes.includes(route.query.map) ? route.query.map : "installations";
    },
    set(tab) {
      router.replace({
        query: {
          map: tab,
        },
      });
    },
  });

  const mapModeTabs = [
    {
      label: "Installations",
      value: "installations",
    },
    {
      label: "Régions",
      value: "regions",
    },
  ];

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

  watch(installationPanelOpen, (newValue) => {
    if (newValue === false) {
      if (activeMarker.value) {
        const marker = activeMarker.value.feature,
              markerType = marker.properties.type.toLowerCase();

        activeMarker.value.setIcon(markerIcons[markerType].default);
        activeMarker.value = null;
      }
    }
  });

  watch(electricityPanelOpen, (newValue) => {
    if (newValue === false) {
      if (activeRegionLayer.value) {
        resetRegionStyle(activeRegionLayer.value);
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
        regionLayers = ref(null);

  const mapRes = await $fetch("/api/carte/installations");
  if (mapRes.status !== 200) {
    throw createError({
      statusCode: mapRes.status,
      message: mapRes.message,
    });
  }

  const regionsRes = await $fetch("/api/carte/regions");
  if (regionsRes.status !== 200) {
    throw createError({
      statusCode: regionsRes.status,
      message: regionsRes.message,
    });
  }

  // Empêcher la réactivité du GeoJSON et ainsi éviter des problèmes de performance
  const geojsonMap = markRaw(mapRes.data),
        geojsonRegions = markRaw(regionsRes.data);
  const displayedGeojson = markRaw(
    Object.fromEntries(
      Object.entries(geojsonMap).map(([layerName, featureCollection]) => [
        layerName,
        {
          ...featureCollection,
          // Conserver seulement les installations indépendantes d'un ouvrage
          features: featureCollection.features.filter(feature => !feature.properties.ouvrage_id),
        },
      ]),
    ),
  );

  const mapLayerOptions = {
    pointToLayer: function (feature, latlng) {
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

  const regionsLayerOptions = {
    onEachFeature: function (feature, layer) {
      layer.on({
        mouseover: (e) => {
          highlightRegion(e.target);
        },
        mouseout: () => {
          const layers = regionLayers.value?.leafletObject;
          if (!layers) return;

          layers.eachLayer((l) => {
            if (!electricityPanelOpen.value || activeRegionLayer.value?._leaflet_id !== l._leaflet_id) {
              resetRegionStyle(l);
            }
          });
        },
        click: async (e) => {
          await openRegion(feature, e.target);
        },
      });
    },
  };

  async function openInstallation(marker, feature) {
    if (electricityPanelOpen.value) {
      electricityPanelOpen.value = false;
      await nextTick();
    }

    if (installationPanelOpen.value) {
      installationPanelOpen.value = false;
      await nextTick();
    }

    const markerType = feature.properties.type.toLowerCase();

    marker.setIcon(markerIcons[markerType].active);
    activeMarker.value = marker;

    installationPanelData.value = feature.properties;
    installationPanelOpen.value = true;
  }

  async function openRegion(feature, layer) {
    if (installationPanelOpen.value) {
      installationPanelOpen.value = false;
      await nextTick();
    }

    if (activeRegionLayer.value && activeRegionLayer.value !== layer) {
      resetRegionStyle(activeRegionLayer.value);
    }

    activeRegion.value = feature.properties.region;
    activeRegionLayer.value = layer;

    electricityPanelOpen.value = true;
    highlightRegion(layer);
  }

  function regionsStyle() {
    return {
      fillColor: "var(--ui-color-neutral-500)",
      fillOpacity: 0.2,
      color: "var(--ui-color-neutral-600)",
      opacity: 0.8,
      weight: 1,
    };
  }

  function highlightRegion(layer) {
    layer.setStyle({
      fillOpacity: 0.35,
      opacity: 0.75,
    });
    layer.bringToFront();
  }

  function resetRegionStyle(layer) {
    layer.setStyle(regionsStyle());
  }

  function onMapReady() {
    centerOnQuebec();

    if (mapMode.value === "installations" && (installationId && installationType)) {
      if (!geojsonMap[installationType]) return;

      const selectedFeature = geojsonMap[installationType].features.find((feature) => {
        return feature.properties.objectid === installationId;
      });

      if (selectedFeature) {
        installationPanelData.value = selectedFeature.properties;
        installationPanelOpen.value = true;
      }
    }

    if (mapMode.value === "regions" && regionId) {
      const layers = regionLayers.value?.leafletObject;
      if (!layers) return;

      layers.eachLayer((layer) => {
        if (layer.feature.properties.region === regionId) {
          openRegion(layer.feature, layer);
        }
      });
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
