<template>
  <div>
    <Map
      :installation-open="installationPanelOpen"
      :region-open="regionPanelOpen"
      @open-installation="openInstallation"
      @open-region="openRegion"
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

  async function openInstallation(data) {
    if (regionPanelOpen.value) {
      regionPanelOpen.value = false;
      await nextTick();
    }

    if (installationPanelOpen.value) {
      installationPanelOpen.value = false;
      await nextTick();
    }

    installationPanelData.value = data;
    installationPanelOpen.value = true;
  }

  async function openRegion(region) {
    if (installationPanelOpen.value) {
      installationPanelOpen.value = false;
      await nextTick();
    }

    activeRegion.value = region;
    regionPanelOpen.value = true;
  }

  onMounted(async () => {
    const elecricityRes = await $fetch("/api/electricite");
    if (elecricityRes.status !== 200) {
      throw createError({
        statusCode: elecricityRes.status,
        message: elecricityRes.message,
      });
    }

    elecricityData.value = elecricityRes.data;
  });
</script>
