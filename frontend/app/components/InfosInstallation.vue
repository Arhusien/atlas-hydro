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
          {{ installationTypeMapping[installationData?.type || defaultData.type] || 'Inconnu' }}
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
          v-model="activeTab"
          :items="configTabs"
          color="neutral"
          variant="link"
          class="h-full min-h-0 flex flex-col"
          :ui="{
            root: 'gap-0',
            list: 'px-4 sm:px-6 shrink-0',
            content: 'flex-1 min-h-0 h-full overflow-y-auto py-4 sm:py-6 pl-4 sm:pl-6 pr-[11px] sm:pr-[19px] mt-px content-scrollbar',
            trigger: 'w-full px-0 cursor-pointer',
          }"
        >
          <template #infos>
            <div class="flex-col gap-4 sm:gap-6 flex">
              <div class="flex flex-col gap-2 sm:gap-3">
                <h2 class="text-highlighted font-medium">
                  Détails de l'installation
                </h2>
                <div class="flex flex-col justify-center gap-2 sm:gap-3">
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
                    <span>{{ installationTypeMapping[installationData?.type] || 'Inconnu' }}</span>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Région</span>
                    <div class="flex items-center justify-end">
                      <span>{{ installationData?.nom_region || 'Inconnu' }}</span>
                      <UIcon
                        name="i-lucide-dot"
                        class="size-4 text-dimmed"
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
                class="flex flex-col gap-2 sm:gap-3"
              >
                <h2 class="text-highlighted font-medium">
                  En direct
                  <!-- pour les trucs pas à jour mettre un triangle warning à côté du label de la data -->
                </h2>
              </div>
              <div
                v-if="installationData.type === 'CENTRALE' && installationData?.sondes?.length > 0"
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
                      container: 'p-4 sm:p-4',
                      body: 'w-full',
                      description: 'text-sm font-normal',
                    }"
                    @click="updateData(sonde);"
                  >
                    <template #description>
                      <div class="flex items-center justify-between w-full">
                        <span class="text-left text-default">{{ sonde.nom || 'Inconnu' }}</span>
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
          <template #data>
            <div
              v-if="Object.keys(relevesByDataType)?.length > 0"
              class="flex flex-col gap-2 sm:gap-3"
            >
              <h2 class="text-highlighted font-medium">
                Relevés
              </h2>
              <UAccordion
                v-for="([type_releves, releves]) in Object.entries(relevesByDataType)"
                :key="type_releves"
                :items="[
                  {
                    label: dataTypeReleveMapping[type_releves] || 'Inconnu',
                    content: releves,
                  },
                ]"
                :ui="{
                  trigger: 'p-4 bg-elevated/50 font-normal rounded-md cursor-pointer data-[state=open]:rounded-b-none transition hover:bg-elevated gap-2',
                  content: 'bg-elevated/50 rounded-b-md',
                }"
              >
                <template
                  v-if="(releves[0]?.type_valeur !== 'INCONNU') && valueTypeMapping[releves[0].type_valeur]"
                  #leading
                >
                  <UTooltip
                    :delay-duration="0"
                    :text="valueTypeMapping[releves[0].type_valeur]"
                    :content="{
                      side: 'left',
                      sideOffset: 10,
                      updatePositionStrategy: 'always',
                    }"
                  >
                    <UIcon
                      name="i-lucide-info"
                      class="size-4.5"
                    />
                  </UTooltip>
                </template>
                <template #content="{ item }">
                  <!-- ajouter une table!!! -->
                  <div class="flex flex-col justify-center items-center">
                    <div
                      v-for="(releve, index) in item.content"
                      :key="index"
                      class="px-4 w-full even:bg-elevated py-1"
                    >
                      <div class="flex items-center justify-between w-full text-sm text-pretty">
                        <span class="text-muted text-left">
                          {{ releve.date ? Intl.DateTimeFormat("fr-FR", { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(releve.date)) : 'Inconnu' }}
                        </span>
                        <span class="text-right">
                          {{ releve.valeur?.toFixed(2) ?? 'Inconnu' }} {{ releve.unite_valeur ?? 'Inconnu' }}
                        </span>
                      </div>
                    </div>
                  </div>
                </template>
                <!-- <h2 class="text-highlighted font-medium">
                  {{ dataTypeReleveMapping[type_releves] || 'Inconnu' }}
                </h2>
                <div class="flex flex-col gap-2 sm:gap-3">
                  <UPageCard
                    v-for="(releve, index) in releves"
                    :key="index"
                    variant="soft"
                    :ui="{
                      root: 'rounded-md',
                      container: 'p-2 sm:p-4',
                      body: 'w-full',
                      description: 'text-sm text-highlighted font-normal',
                    }"
                  >
                    <template #description>
                      <div class="flex items-center justify-between w-full">
                        <span class="text-left">{{ releve.valeur ?? 'Inconnu' }}</span>
                        <span class="text-muted text-right">{{ releve.date ? new Date(releve.date).toLocaleString() : 'Inconnu' }}</span>
                      </div>
                    </template>
                  </UPageCard>
                </div> -->
              </UAccordion>
            </div>
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
  import {
    installationTypeMapping,
    dataTypeReleveMapping,
    valueTypeMapping,
  } from "~/utils/mapping.ts";

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
        installationHistoryData = ref([]),
        activeTab = ref("0");

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);

    if (newValue === true) {
      installationData.value = null;
      pendingData.value = true;
      activeTab.value = "0";

      const {
        data,
        pending,
      } = await useFetch(`/api/installations/${props.defaultData.objectid}`);

      installationData.value = data.value.data;
      pendingData.value = pending.value;
    }
    else {
      installationHistoryData.value = [];
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
      slot: "data",
    },
    {
      label: "Statistiques",
      // icon: "i-lucide-satellite-dish",
      slot: "stats",
    },
  ];

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

    activeTab.value = "0";
  }

  function processReleves(releves) {
    let relevesByDataType = {};

    for (const releve of releves) {
      if (!relevesByDataType[releve.type_donnee]) {
        relevesByDataType[releve.type_donnee] = [];
      }
      relevesByDataType[releve.type_donnee].push(releve);
    }

    if (relevesByDataType["INCONNU"]) {
      delete relevesByDataType["INCONNU"];
    }

    relevesByDataType = Object.keys(relevesByDataType).sort().reduce((acc, key) => {
      acc[key] = relevesByDataType[key].sort((a, b) => new Date(b.date) - new Date(a.date));

      return acc;
    }, {});

    return relevesByDataType;
  }

  const relevesByDataType = computed(() => {
    if (!installationData.value || !installationData.value.releves) return [];

    return processReleves(installationData.value.releves);
  });
</script>

<style>
  .content-scrollbar {
    scrollbar-gutter: stable;

    &::-webkit-scrollbar {
      height: 5px;
      width: 5px
    }

    &::-webkit-scrollbar-corner {
      background: 0 0
    }

    &::-webkit-scrollbar-thumb {
      background: var(--ui-bg-accented);
      border-radius: 9999px
    }

    &::-webkit-scrollbar-track {
      background: 0 0
    }
  }
</style>
