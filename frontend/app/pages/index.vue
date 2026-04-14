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
        installationId = route.query.installation;

  const panelInstallationOpen = ref(false),
        panelInstallationData = ref({});

  const activeMarker = ref(null);

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
    CENTRALE: {
      default: L.icon({
        ...markerIconOptions,
        iconUrl: factoryPin,
      }),
      active: L.icon({
        ...markerIconOptions,
        iconUrl: factoryPinActive,
      }),
    },
    BARRAGE: {
      default: L.icon({
        ...markerIconOptions,
        iconUrl: damPin,
      }),
      active: L.icon({
        ...markerIconOptions,
        iconUrl: damPinActive,
      }),
    },
    SONDE: {
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

  watch(panelInstallationOpen, (newValue) => {
    if (newValue === false) {
      if (activeMarker.value) {
        const activeType = activeMarker.value.feature.properties.type;
        activeMarker.value.setIcon(markerIcons[activeType].default);
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

  const onMapReady = () => {
    centerOnQuebec();

    // Ajouter le GeoJSON à la carte
    L.geoJSON(geojson.value.data, {
      pointToLayer: function (feature, latlng) {
        if (feature.properties.ouvrage_id) return;

        return L.marker(latlng, {
          title: feature.properties.nom || "Inconnu",
          icon: markerIcons[feature.properties.type]?.default || markerIcons.SONDE.default,
          zIndexOffset: feature.properties.type === "CENTRALE" ? 9999 : feature.properties.type === "BARRAGE" ? 4999 : 0,
        }).on("click", function () {
          if (activeMarker.value) {
            const previousType = activeMarker.value.feature.properties.type;
            activeMarker.value.setIcon(markerIcons[previousType].default);
          }

          this.setIcon(markerIcons[feature.properties.type].active);
          activeMarker.value = this;

          panelInstallationOpen.value = true;
          panelInstallationData.value = feature.properties;
        });
      },
    }).addTo(map.value.leafletObject);

    if (installationId) {
      const selectedFeature = geojson.value.data.features.find((feature) => {
        return feature.properties.objectid === installationId;
      });

      if (selectedFeature) {
        panelInstallationData.value = selectedFeature.properties;
        panelInstallationOpen.value = true;
      }
    }
  };

  const centerOnQuebec = () => {
    map.value.leafletObject.flyToBounds(quebecBounds, {
      animate: false,
      padding: [50, 50],
    });
  };
</script>
