<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full h-full relative">
    <div class="flex flex-col items-center justify-center gap-2.5 absolute top-4 left-4 z-1000">
      <ControlZoom
        @zoom-in="map.leafletObject.zoomIn()"
        @zoom-out="map.leafletObject.zoomOut()"
      />
    </div>
    <div class="flex flex-col items-center justify-center gap-2.5 absolute bottom-4 left-4 z-1000">
      <ControlLayers
        v-if="activeMapView === 'installations'"
        v-model="installationLayerStates"
      />
      <ControlCenter
        @center="centerOnQuebec(map.leafletObject)"
      />
    </div>
    <div class="flex flex-col items-center justify-center gap-2.5 absolute top-4 right-4 z-1000">
      <ModalInformation />
    </div>
    <div class="flex items-center justify-center gap-2.5 absolute top-4 left-1/2 -translate-x-1/2 z-1000">
      <UTabs
        v-model="activeMapView"
        color="neutral"
        variant="pill"
        :content="false"
        :items="mapViewTabs"
        :ui="{
          list: 'bg-default',
          trigger: 'cursor-pointer select-none',
        }"
      />
    </div>
    <LMap
      ref="map"
      class="isolate"
      :zoom="initialZoom"
      :center="initialMapCenter"
      :options="mapOptions"
      @ready="onMapReady"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/copyright&quot; target=&quot;_blank&quot;>OpenStreetMap</a> &amp;copy; <a href=&quot;https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/licence.html&quot; target=&quot;_blank&quot;>Hydro-Québec</a>"
        layer-type="base"
        name="OpenStreetMap"
        no-wrap
      />
      <!-- Régions -->
      <LGeoJson
        ref="regionLayers"
        :geojson="geojsonRegions"
        :options="regionsLayerOptions"
        :options-style="regionDefaultStyle"
        :visible="activeMapView === 'territoires'"
      />
      <!-- Installations -->
      <LGeoJson
        v-for="([layerName, features]) in Object.entries(geojsonInstallations)"
        ref="installationLayers"
        :key="layerName"
        :geojson="features"
        :options="installationsLayerOptions"
        :visible="installationLayerStates[layerName] && activeMapView === 'installations'"
      />
    </LMap>
  </div>
</template>

<script setup>
  import L from "leaflet";
  import {
    markers,
  } from "~/utils/constants/markers";
  import {
    availableViews,
    mapViewTabs,
    initialMapCenter,
    initialZoom,
    mapOptions,
    setRegionActive,
    setRegionInactive,
    regionStyle,
    centerOnQuebec,
  } from "~/utils/constants/map.js";

  const props = defineProps({
    appReady: {
      type: Boolean,
      default: false,
    },
    installationOpen: {
      type: Boolean,
      default: false,
    },
    regionOpen: {
      type: Boolean,
      default: false,
    },
  });

  const emit = defineEmits([
    "open-installation",
    "open-region",
    "map-ready",
  ]);

  const route = useRoute(),
        router = useRouter(),
        queryInstallationId = route.query.installation,
        queryInstallationType = route.query.type,
        queryRegionId = route.query.territoire;

  const activeMarker = ref(null),
        activeRegionLayer = ref(null);

  // Carte affichée
  const activeMapView = computed({
    get() {
      return availableViews.includes(route.query.map) ? route.query.map : "installations";
    },
    set(tab) {
      router.replace({
        query: {
          map: tab,
        },
      });
    },
  });

  // États des couches de la carte installations
  const installationLayerStates = ref({
    centrale: true,
    barrage: true,
    sonde: true,
  });

  const map = ref(null),
        regionLayers = ref(null),
        installationLayers = ref(null);

  // Récupérer les cartes GeoJSON
  const [
    installationsResponse,
    regionsResponse,
  ] = await Promise.all([
    $fetch("/api/carte/installations"),
    $fetch("/api/carte/regions"),
  ]);

  for (const response of [installationsResponse, regionsResponse]) {
    if (response.status !== 200) {
      throw createError({
        statusCode: response.status,
        message: response.message,
      });
    }
  }

  watch(() => props.installationOpen, (newValue) => {
    // Réinitialiser le marqueur actif lors de la fermeture du panneau d'installation
    if (newValue === false) {
      resetActiveMarker();
    }
  });

  watch(() => props.regionOpen, (newValue) => {
    // Réinitialiser la région active lors de la fermeture du panneau de région
    if (newValue === false) {
      if (activeRegionLayer.value) {
        setRegionInactive(activeRegionLayer.value);
        activeRegionLayer.value = null;
      }
    }
  });

  // Empêcher la réactivité du GeoJSON pour éviter des problèmes de performance
  const geojsonInstallations = markRaw(installationsResponse.data),
        geojsonRegions = markRaw(regionsResponse.data);

  const installationsLayerOptions = {
    pointToLayer: function (feature, latlng) {
      // Conserver seulement les installations indépendantes d'un ouvrage
      if (feature.properties.ouvrage_id) return null;

      const installationType = feature.properties.type.toLowerCase(),
            markerTitle = feature.properties?.nom || "Inconnu",
            markerIcon = markers[installationType].default,
            markerZIndex = markerIcon.zIndex || 0;

      const marker = L.marker(latlng, {
        title: markerTitle,
        icon: markerIcon,
        zIndexOffset: markerZIndex,
      });

      // Ouvir le panneau d'installation au clic sur le marqueur
      marker.on("click", () => {
        openInstallation(marker, feature);
      });

      return marker;
    },
  };

  const regionsLayerOptions = {
    onEachFeature: function (feature, layer) {
      // Pour chaque région, écouter les événements d'interaction
      layer.on({
        mouseover: async (event) => {
          setRegionActive(event.target);
        },
        mouseout: async () => {
          const layers = regionLayers.value?.leafletObject,
                activeLayerId = activeRegionLayer.value?._leaflet_id;
          if (!layers) return;

          layers.eachLayer((l) => {
            if (activeLayerId !== l._leaflet_id) {
              setRegionInactive(l);
            }
          });
        },
        // Ouvrir le panneau région au clic sur la région
        click: (event) => {
          openRegion(feature, event.target);
        },
      });
    },
  };

  async function openInstallation(marker, feature) {
    const installationType = feature.properties.type.toLowerCase(),
          markerIcon = markers[installationType].active;

    resetActiveMarker();

    activeMarker.value = marker;
    marker.setIcon(markerIcon);

    emit("open-installation", feature.properties);
  }

  function openRegion(feature, layer) {
    // Si une autre région est active et qu'elle diffère de celle affichée, la réinitialiser
    if (activeRegionLayer.value && activeRegionLayer.value?._leaflet_id !== layer._leaflet_id) {
      setRegionInactive(activeRegionLayer.value);
    }

    activeRegionLayer.value = layer;
    setRegionActive(layer);

    emit("open-region", feature.properties.region);
  }

  function resetActiveMarker() {
    if (!activeMarker.value) return;

    const marker = activeMarker.value.feature,
          markerType = marker.properties.type.toLowerCase(),
          markerIcon = markers[markerType].default;

    activeMarker.value.setIcon(markerIcon);
    activeMarker.value = null;
  }

  function onMapReady() {
    centerOnQuebec(map.value.leafletObject);

    emit("map-ready");
  };

  function onAppReady() {
    // Si l'URL contient des paramètres d'installation
    if (activeMapView.value === "installations" && (queryInstallationId && queryInstallationType)) {
      // Si le type de l'installation n'existe pas dans les données de la carte, ignorer
      if (!geojsonInstallations[queryInstallationType]) return;

      // Trouver l'indice de la couche correspondante au type de l'installation
      const geojsonIndex = Object.keys(geojsonInstallations).findIndex(key => key === queryInstallationType);

      const layers = installationLayers.value[geojsonIndex]?.leafletObject;
      if (!layers) return;

      // Chercher le marqueur correspondant à l'installation
      const selectedFeature = geojsonInstallations[queryInstallationType].features.find((feature) => {
        return feature.properties.objectid === queryInstallationId;
      });

      // S'il existe, ouvrir le panneau d'installation correspondant
      if (selectedFeature) {
        layers.eachLayer((layer) => {
          if (layer.feature.properties.objectid === queryInstallationId) {
            openInstallation(layer, selectedFeature);
          }
        });
      }
    }

    // Si l'URL contient un paramètre de région
    if (activeMapView.value === "territoires" && queryRegionId) {
      const layers = regionLayers.value?.leafletObject;
      if (!layers) return;

      // Parcourir les régions pour trouver celle correspondante au nom de la région
      layers.eachLayer((layer) => {
        // Si elle existe, ouvrir le panneau de région correspondant
        if (layer.feature.properties.region === queryRegionId) {
          openRegion(layer.feature, layer);
        }
      });
    }
  }

  function regionDefaultStyle() {
    return regionStyle.default;
  }

  onMounted(async () => {
    // Récupérer et définir les états des couches de la carte installations
    const storedLayerStates = localStorage.getItem("layerStates");
    if (storedLayerStates) {
      installationLayerStates.value = JSON.parse(storedLayerStates);
    }
  });

  // Sauvegarder les états des couches de la carte installations lors d'un changement
  watch(installationLayerStates, (newValue) => {
    localStorage.setItem("layerStates", JSON.stringify(newValue));
  }, {
    deep: true,
  });

  watch(() => props.appReady, (newValue) => {
    if (newValue === true) {
      onAppReady();
    }
  });
</script>
