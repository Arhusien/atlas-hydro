<template>
  <div class="w-svw h-svh relative">
    <!-- Écran de chargement -->
    <Teleport
      to="body"
    >
      <Transition
        enter-active-class="transition-opacity duration-500"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-500"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        @after-leave="appReady = true"
      >
        <div
          v-if="!mapReady"
          class="h-full w-full fixed bg-default z-9999 top-0 left-0 flex items-center justify-center will-change-[opacity]"
        >
          <div class="flex flex-col gap-6 items-center justify-center">
            <BrandLogoType class="w-48 sm:w-56 lg:w-64 h-auto text-highlighted animate-pulse" />
          </div>
        </div>
      </Transition>
    </Teleport>
    <Map
      :app-ready="appReady"
      :installation-open="installationPanelOpen"
      :region-open="regionPanelOpen"
      @open-installation="openPanel('installation', $event)"
      @open-region="openPanel('region', $event)"
      @map-ready="onMapReady"
    />
    <PanelInstallation
      v-model="installationPanelOpen"
      :default-data="installationPanelData"
    />
    <PanelRegion
      v-model="regionPanelOpen"
      :region="activeRegion"
      :data="elecricityData"
    />
  </div>
</template>

<script setup>
  const installationPanelOpen = ref(false),
        installationPanelData = ref({}),
        regionPanelOpen = ref(false);

  const elecricityData = ref({}),
        activeRegion = ref(null);

  const mapReady = ref(false),
        appReady = ref(false);

  async function openPanel(type, data) {
    // Si un panneau est déjà ouvert,
    // le fermer, attendre la fin de l'animation,
    // puis ouvrir le nouveau panneau
    if (regionPanelOpen.value) {
      regionPanelOpen.value = false;
      await nextTick();
    }

    if (installationPanelOpen.value) {
      installationPanelOpen.value = false;
      await nextTick();
    }

    /* eslint-disable vue/script-indent */
    switch (type) {
      case "installation":
        installationPanelData.value = data;
        installationPanelOpen.value = true;

        break;
      case "region":
        activeRegion.value = data;
        regionPanelOpen.value = true;

        break;
      default:
        break;
    }
  }

  async function onMapReady() {
    setTimeout(() => {
      mapReady.value = true;
    }, 500);
  }

  onMounted(async () => {
    // Récupérer les données des régions
    const elecricityResponse = await $fetch("/api/electricite");
    if (elecricityResponse.status !== 200) {
      throw createError({
        statusCode: elecricityResponse.status,
        message: elecricityResponse.message,
      });
    }

    elecricityData.value = elecricityResponse.data;
  });
</script>
