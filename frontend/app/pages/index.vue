<template>
  <div style="height:100vh; width:100vw; position: relative;">
    <LMap
      ref="map"
      :zoom="5"
      :center="[53.5, -71.5]"
      :options="{
        zoomControl: false,
      }"
      @ready="onMapReady"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors"
        layer-type="base"
        name="OpenStreetMap"
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

  const map = ref(null);

  const {
    data: geojson,
  } = await useFetch("https://cartes.shawinigan.ca/server/rest/services/Infrastructures_sportives/FeatureServer/0/query?where=1=1&outFields=*&returnGeometry=true&f=geojson", {
    // Empêcher la réactivité du GeoJSON et ainsi éviter les problèmes de performance
    transform: rawData => markRaw(rawData),
  });

  const onMapReady = () => {
    // Ajouter le GeoJSON à la carte
    L.geoJSON(geojson.value, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {
          title: feature.properties.nom || "Inconnu",
          icon: markerIcon,
        }).on("click", function () {
          infosInstallationOpen.value = true;
          infosInstallationData.value = feature.properties;

          const zoom = map.value.leafletObject.getZoom(),
                animationDuration = zoom < 15 ? (zoom > 10 ? 1 : 1.5) : 0.5;

          map.value.leafletObject.flyTo(latlng, 15, {
            animate: true,
            duration: animationDuration,
          });
        });
      },
    }).addTo(map.value.leafletObject);
  };
</script>
