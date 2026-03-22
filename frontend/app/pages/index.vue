<template>
  <div style="height:100vh; width:100vw">
    <LMap
      ref="map"
      :zoom="zoom"
      :center="[50.0, -73.0]"
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
        test
      </LControl>
    </LMap>
  </div>
</template>

<script setup>
  import L from "leaflet";
  import {
    MapPin,
    createElement,
  } from "lucide";

  const mapPinSvg = createElement(MapPin, {
    width: 32,
    height: 32,
    stroke: "white",
    fill: "royalblue",
  }).outerHTML;

  const zoom = ref(6),
        map = ref(null);

  const {
    data: geojson,
  } = await useFetch("https://cartes.shawinigan.ca/server/rest/services/Infrastructures_sportives/FeatureServer/0/query?where=1=1&outFields=*&returnGeometry=true&f=geojson");

  const onMapReady = () => {
    // Ajouter le GeoJSON à la carte
    L.geoJSON(geojson.value, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {
          title: feature.properties.nom || "Inconnu",
          icon: L.divIcon({
            html: mapPinSvg,
            className: "marker-icon",
            iconSize: [32, 32],
            iconAnchor: [12, 32],
            popupAnchor: [0, -32],
          }),
        });
      },
      onEachFeature: function (feature, layer) {
        if (feature.properties) {
          const htmlContent = `
              <div class="modern-popup">
                <h3>${feature.properties.nom || "Inconnu"}</h3>
                <p>${feature.properties.sport || ""}</p>
              </div>
            `;
          layer.bindPopup(htmlContent, { maxWidth: 300 });
        }
      },
    }).addTo(map.value.leafletObject);
  };
</script>
