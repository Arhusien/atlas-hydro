<template>
  <div class="w-screen h-screen">
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
      <LControl position="topleft">
        <ControleZoom
          @zoom-in="map.leafletObject.zoomIn()"
          @zoom-out="map.leafletObject.zoomOut()"
        />
        <div class="flex flex-col items-center justify-center gap-2.5 mt-2.5">
          <SourceProductionElectricite />
          <DemandeElectricite />
          <ExportationElectricite />
          <InfosCredits />
        </div>
      </LControl>
      <LControl position="bottomleft">
        <div class="flex flex-col items-center justify-center gap-2.5 mt-2.5">
          <Parametres />
          <LocaliserPosition
            @locate="null"
          />
          <CentrerQuebec
            @center="centerOnQuebec()"
          />
        </div>
      </LControl>
    </LMap>
    <PanelInstallation
      v-model="PanelInstallationOpen"
      :default-data="PanelInstallationData"
    />
  </div>
</template>

<script setup>
  import L from "leaflet";
  import satellitePin from "~/assets/img/satellitePin.svg?raw";
  import factoryPin from "~/assets/img/factoryPin.svg?raw";

  const PanelInstallationOpen = ref(false),
        PanelInstallationData = ref({});

  const activeMarkers = ref([]);

  const markerIconOptions = {
    className: "marker-icon",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  };

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

  const onMapReady = () => {
    centerOnQuebec();

    // Ajouter le GeoJSON à la carte
    L.geoJSON(geojson.value.data, {
      pointToLayer: function (feature, latlng) {
        if (feature.properties.centrale_id) return;

        return L.marker(latlng, {
          title: feature.properties.nom || "Inconnu",
          icon: L.divIcon({
            ...markerIconOptions,
            html: feature.properties.type === "CENTRALE" ? factoryPin : satellitePin,
          }),
          zIndexOffset: feature.properties.type === "CENTRALE" ? 1000 : 0,
        }).on("click", function (event) {
          PanelInstallationOpen.value = true;
          PanelInstallationData.value = feature.properties;

          const target = event.originalEvent.target,
                svgMarkerIcon = target.closest("svg");

          svgMarkerIcon.style.setProperty("--ui-marker", "var(--ui-bg-inverted)");
          svgMarkerIcon.style.setProperty("--ui-marker-inverted", "var(--ui-bg)");

          activeMarkers.value.push(svgMarkerIcon);
        });
      },
    }).addTo(map.value.leafletObject);
  };

  const centerOnQuebec = () => {
    map.value.leafletObject.flyToBounds(quebecBounds, {
      animate: false,
      padding: [50, 50],
    });
  };

  watch(PanelInstallationOpen, (newValue) => {
    if (newValue === false) {
      activeMarkers.value.forEach((marker) => {
        marker.style.setProperty("--ui-marker", "var(--ui-bg)");
        marker.style.setProperty("--ui-marker-inverted", "var(--ui-bg-inverted)");
      });
      activeMarkers.value = [];
    }
  });
</script>
