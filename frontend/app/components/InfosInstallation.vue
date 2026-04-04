<template>
  <USlideover
    v-model:open="open"
    side="right"
    inset
    :overlay="false"
    close-icon="lucide-x"
    :ui="{
      content: 'ring-0 sm:ring-0',
      body: 'flex-1 overflow-hidden p-0 sm:p-0',
      footer: 'p-2 sm:p-4',
      close: 'cursor-pointer',
    }"
  >
    <template #title>
      <div class="flex items-center gap-2">
        <h2>{{ installationData?.nom || defaultData.nom || 'Inconnu' }}</h2>
        <UBadge
          color="neutral"
          variant="soft"
        >
          {{ typeMapping[installationData?.type || defaultData.type] || 'Inconnu' }}
        </UBadge>
      </div>
    </template>
    <template #body>
      <div
        v-if="pendingData"
        class="flex items-center justify-center h-full"
      >
        <LoaderCircle class="animate-spin" />
      </div>
      <div
        v-else
        class="h-full min-h-0 flex flex-col"
      >
        <UTabs
          :items="configTabs"
          color="neutral"
          variant="link"
          class="h-full min-h-0 flex flex-col"
          :ui="{
            root: 'gap-0',
            list: 'px-4 sm:px-6 shrink-0',
            content: 'flex-1 min-h-0 h-full overflow-y-auto p-4 sm:p-6',
            trigger: 'w-full px-0 cursor-pointer',
          }"
        >
          <template #infos>
            <div class="flex-col gap-4 sm:gap-6 flex">
              <div class="flex flex-col gap-2 sm:gap-3">
                <h2 class="text-highlighted font-medium">
                  Détails de l'installation
                </h2>
                <div class="flex flex-col justify-center gap-2 sm:gap-4">
                  <div class="flex items-center justify-between text-sm">
                    <span>Identifiant</span>
                    <span>{{ installationData?.id || 'Inconnu' }}</span>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Nom</span>
                    <span>{{ installationData?.nom || 'Inconnu' }}</span>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Type</span>
                    <span>{{ typeMapping[installationData?.type] || 'Inconnu' }}</span>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Région</span>
                    <div class="flex items-center justify-end">
                      <span>{{ installationData?.nom_region || 'Inconnu' }}</span>
                      <UIcon
                        name="i-lucide-dot"
                        class="size-4 text-muted"
                      />
                      <span class="text-muted">{{ installationData?.code_region || 'Inconnu' }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Latitude</span>
                    <div class="flex items-center justify-end">
                      <span>{{ convertToDMS(installationData?.y, true) || 'Inconnu' }}</span>
                      <UIcon
                        name="i-lucide-dot"
                        class="size-4 text-dimmed"
                      />
                      <span class="text-muted">{{ installationData?.y || 'Inconnu' }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Longitude</span>
                    <div class="flex items-center justify-end">
                      <span>{{ convertToDMS(installationData?.x, false) || 'Inconnu' }}</span>
                      <UIcon
                        name="i-lucide-dot"
                        class="size-4 text-dimmed"
                      />
                      <span class="text-muted">{{ installationData?.x || 'Inconnu' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div
                v-if="installationData.type === 'centrale'"
                class="flex flex-col gap-2 sm:gap-3"
              >
                <h2 class="text-highlighted font-medium">
                  Sondes à proximité
                </h2>
                <div class="flex flex-col gap-2 sm:gap-3">
                  <UPageCard
                    v-for="(sonde, index) in installationData.sondes"
                    :key="index"
                    as="button"
                    variant="soft"
                    :ui="{
                      root: 'rounded-md has-focus-visible:ring-inverted cursor-pointer',
                      container: 'p-2 sm:p-4',
                      body: 'w-full',
                      description: 'text-sm text-highlighted font-normal',
                    }"
                    @click="updateData(sonde);"
                  >
                    <template #description>
                      <div class="flex items-center justify-between w-full">
                        <span class="text-left">{{ sonde.nom || 'Inconnu' }}</span>
                        <span class="text-muted text-right">{{ getDistance(
                          { latitude: installationData.y, longitude: installationData.x },
                          { latitude: sonde.y, longitude: sonde.x },
                        ) }} mètres</span>
                      </div>
                    </template>
                  </UPageCard>
                </div>
              </div>
            </div>
          </template>
          <template #releves>
            <span>Relevés</span>
          </template>
          <template #stats>
            <span>Statistiques</span>
          </template>
        </UTabs>
      </div>
    </template>
    <template
      v-if="installationHistoryData.length > 0"
      #footer
    >
      <UButton
        icon="i-lucide-arrow-left"
        color="neutral"
        variant="ghost"
        class="cursor-pointer"
        @click="(installationHistoryData.length > 0) ? goToPreviousInstallation() : null"
      >
        Retour
      </UButton>
    </template>
  </USlideover>
</template>

<script setup>
  import {
    LoaderCircle,
  } from "@lucide/vue";
  import {
    decimalToSexagesimal,
    getDistance,
  } from "geolib";

  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    defaultData: {
      type: Object,
      required: true,
    },
  });

  const emit = defineEmits([
    "update:modelValue",
  ]);

  const open = ref(props.modelValue),
        installationData = ref(null),
        pendingData = ref(true),
        installationHistoryData = ref([]);

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);

    if (newValue === true) {
      installationData.value = null;
      pendingData.value = true;

      const {
        data,
        pending,
      } = await useFetch(`/api/installations/${props.defaultData.objectid}`);

      installationData.value = data.value.data;
      pendingData.value = pending.value;
    }
  });

  const configTabs = [
    {
      label: "Informations",
      // icon: "i-lucide-info",
      slot: "infos",
    },
    {
      label: "Relevés",
      // icon: "i-lucide-activity",
      slot: "releves",
    },
    {
      label: "Statistiques",
      // icon: "i-lucide-satellite-dish",
      slot: "stats",
    },
  ];

  const typeMapping = {
    centrale: "Centrale",
    sonde: "Sonde",
  };

  function convertToDMS(coord, isLat = true) {
    if (typeof coord !== "number") return null;

    const dms = decimalToSexagesimal(Math.abs(coord)).replace(/\s/g, ""),
          direction = isLat
            ? (coord >= 0 ? "N" : "S")
            : (coord >= 0 ? "E" : "W");

    return `${dms}${direction}`;
  }

  function updateData(sonde) {
    installationHistoryData.value.push(installationData.value);
    installationData.value = sonde;
  }

  function goToPreviousInstallation() {
    if (installationHistoryData.value.length === 0) return;

    installationData.value = installationHistoryData.value.pop();
  }
</script>
