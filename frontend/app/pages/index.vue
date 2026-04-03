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
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors"
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
          <Credits />
        </div>
      </LControl>
      <LControl position="bottomleft">
        <CentrerQuebec
          @center="centerOnQuebec()"
        />
      </LControl>
    </LMap>
    <InfosInstallation
      v-model="infosInstallationOpen"
      :data="infosInstallationData"
    />
  </div>
</template>

<script setup>
  import L from "leaflet";
  import {
    MapPin,
    createElement,
  } from "lucide";

  const infosInstallationOpen = ref(false),
        infosInstallationData = ref({});

  const mapPinSvg = createElement(MapPin, {
    width: 32,
    height: 32,
    stroke: "var(--ui-bg-inverted)",
    fill: "var(--ui-bg)",
  }).outerHTML;

  const markerIcon = L.divIcon({
    html: mapPinSvg,
    className: "marker-icon",
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
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

  const onMapReady = () => {
    centerOnQuebec();

    // Ajouter le GeoJSON à la carte
    L.geoJSON(geojson.value, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {
          title: feature.properties.nom || "Inconnu",
          icon: markerIcon,
        }).on("click", function () {
          infosInstallationOpen.value = true;
          infosInstallationData.value = feature.properties;
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
</script>
