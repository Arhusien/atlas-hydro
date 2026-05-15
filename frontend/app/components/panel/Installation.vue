<template>
  <UIPanel
    v-model="open"
    :title="installationName"
    :badge="installationType"
    :is-loading="isPending"
  >
    <UTabs
      v-model="activeTab"
      :items="installationTabs"
      color="neutral"
      variant="link"
      class="h-full min-h-0 flex flex-col"
      :ui="{
        root: 'gap-0',
        list: 'px-5 sm:px-6 shrink-0',
        content: 'flex-1 min-h-0 h-full overflow-y-auto py-5 sm:py-6 pl-5 sm:pl-6 pr-3.75 sm:pr-4.75 mt-px content-scrollbar',
        trigger: 'w-full cursor-pointer',
      }"
    >
      <template #informations>
        <div class="flex-col gap-5 sm:gap-6 flex">
          <div class="flex flex-col gap-2.5 sm:gap-3">
            <h3 class="text-highlighted font-medium">
              Détails de l'installation
            </h3>
            <div class="flex flex-col justify-center gap-2.5 sm:gap-3">
              <div class="flex items-center justify-between text-sm">
                <span>Identifiant</span>
                <span>{{ installationData?.id || 'Inconnu' }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span>Nom</span>
                <span>{{ installationName }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span>Type</span>
                <span>{{ installationType }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span>Région</span>
                <div class="flex items-center justify-end">
                  <span>{{ installationData?.nom_region || 'Inconnu' }}</span>
                  <span class="text-muted select-none">&nbsp;&middot;&nbsp;</span>
                  <span class="text-muted">{{ installationData?.code_region || 'Inconnu' }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span>Latitude</span>
                <div class="flex items-center justify-end">
                  <span>{{ convertToDMS(installationData?.y, true) || 'Inconnu' }}</span>
                  <span class="text-muted select-none">&nbsp;&middot;&nbsp;</span>
                  <span class="text-muted">{{ installationData?.y || 'Inconnu' }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span>Longitude</span>
                <div class="flex items-center justify-end">
                  <span>{{ convertToDMS(installationData?.x, false) || 'Inconnu' }}</span>
                  <span class="text-muted select-none">&nbsp;&middot;&nbsp;</span>
                  <span class="text-muted">{{ installationData?.x || 'Inconnu' }}</span>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="installationHasData"
            class="flex flex-col gap-2.5 sm:gap-3"
          >
            <h3 class="text-highlighted font-medium">
              Dernières mesures
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
              <UCard
                v-for="[type_releves, { releves }] in Object.entries(groupedReleves)"
                :key="type_releves"
                variant="soft"
                :ui="{
                  root: 'rounded-md',
                  body: 'sm:p-4 text-sm font-normal flex flex-col items-center justify-center w-full h-full gap-0.25',
                }"
              >
                <div class="flex items-center justify-center gap-1.5">
                  <UTooltip
                    :delay-duration="0"
                    text="Mesure ancienne"
                    :content="{
                      side: 'top',
                      sideOffset: 5,
                    }"
                  >
                    <UIcon
                      v-if="shouldDisplayMeasureAlert(releves[0].date)"
                      name="lucide:triangle-alert"
                      class="size-4.5 text-warning-500 cursor-pointer"
                    />
                  </UTooltip>
                  <span class="text-lg font-medium text-default text-center">
                    {{ `${releves[0].valeur.toFixed(2)} ${releves[0].unite_valeur || ''}` }}
                  </span>
                </div>
                <span class="text-sm text-muted text-center">{{ dataTypeReleveMapping[type_releves] || 'Inconnu' }}</span>
              </UCard>
            </div>
          </div>
          <div
            v-if="installationHasSondes"
            class="flex flex-col gap-2.5 sm:gap-3"
          >
            <h3 class="text-highlighted font-medium">
              Sondes associées
            </h3>
            <UCard
              v-for="(sonde, index) in installationData.sondes"
              :key="index"
              as="button"
              variant="soft"
              :ui="{
                root: 'rounded-md cursor-pointer has-focus-visible:ring-2 transition hover:bg-elevated has-focus-visible:ring-inverted',
                body: 'sm:p-4 text-sm font-normal flex items-center justify-between w-full',
              }"
              @click="updateInstallation(sonde.id);"
            >
              <span class="text-left text-default">{{ sonde.nom || 'Inconnu' }}</span>
              <span class="text-muted text-right">{{
                getDistance(
                  { latitude: installationData.y, longitude: installationData.x },
                  { latitude: sonde.y, longitude: sonde.x },
                )
              }} mètres</span>
            </UCard>
          </div>
        </div>
      </template>
      <template #mesures>
        <div
          v-if="installationHasData"
          class="flex flex-col gap-2.5 sm:gap-3"
        >
          <h3 class="text-highlighted font-medium">
            Mesures
          </h3>
          <UAccordion
            v-for="[type_releves, { chartReleves, releves }] in Object.entries(groupedReleves)"
            :key="type_releves"
            :items="[
              {
                label: dataTypeReleveMapping[type_releves] || 'Inconnu',
                releves,
                chartReleves,
              },
            ]"
            :ui="{
              trigger: 'p-4 bg-elevated/50 font-normal rounded-md cursor-pointer data-[state=open]:rounded-b-none transition hover:bg-elevated gap-2',
              content: `bg-elevated/50 rounded-b-md data-[state=open]:animate-none data-[state=closed]:animate-none`,
            }"
            trailing-icon="lucide:chevron-down"
          >
            <template
              v-if="valueTypeMapping[releves[0].type_valeur]"
              #leading
            >
              <UTooltip
                :delay-duration="0"
                :text="valueTypeMapping[releves[0].type_valeur]"
                :content="{
                  side: 'top',
                  sideOffset: 5,
                }"
              >
                <UIcon
                  name="lucide:info"
                  class="size-4.5"
                />
              </UTooltip>
            </template>
            <template #content="{ item }">
              <UTable
                :data="item.releves"
                :columns="buildRelevesTableColumns(item.releves, item.chartReleves, localTimezone)"
                :ui="{
                  base: 'border-t border-(--ui-border-accented)',
                  thead: 'hidden',
                }"
              />
            </template>
          </UAccordion>
        </div>
        <div
          v-else
          class="flex h-full justify-center items-center"
        >
          <UEmpty
            icon="lucide:circle-off"
            title="Aucune donnée"
            description="Atlas Hydro n'a pas pu récupérer de données liées à cette installation."
            variant="naked"
            class="sm:absolute sm:-translate-y-1/2 sm:top-1/2"
          />
        </div>
      </template>
      <template #graphiques>
        <div
          v-if="installationHasData"
          class="flex flex-col gap-2.5 sm:gap-3"
        >
          <h3 class="text-highlighted font-medium">
            Graphiques
          </h3>
          <div class="flex flex-col gap-2.5 sm:gap-3">
            <UCard
              v-for="[type_releves, { chartPoints }] in Object.entries(groupedReleves).filter(([type_releves]) => !excludedDataTypesForStats.includes(type_releves))"
              :key="type_releves"
              variant="soft"
              :ui="{
                root: 'rounded-md',
                body: 'sm:p-4 p-4 text-sm font-normal flex flex-col justify-center w-full h-full gap-4',
              }"
            >
              <div class="flex items-center gap-2">
                <span class="text-left text-default">{{ dataTypeReleveMapping[type_releves] || 'Inconnu' }}</span>
                <UTooltip
                  :delay-duration="0"
                  text="Afficher en vue détaillée"
                  :content="{
                    side: 'top',
                    sideOffset: 5,
                  }"
                >
                  <UIcon
                    name="lucide:zoom-in"
                    class="size-4.5 cursor-pointer"
                    @click="openDetailedChart(type_releves, chartPoints)"
                  />
                </UTooltip>
              </div>
              <Line
                :data="buildChartData(chartPoints, type_releves)"
                :options="buildChartOptions(groupedReleves[type_releves].chartReleves, localTimezone, chartStats[type_releves])"
              />
            </UCard>
          </div>
        </div>
        <div
          v-else
          class="flex h-full justify-center items-center"
        >
          <UEmpty
            icon="lucide:circle-off"
            title="Aucune donnée"
            description="Atlas Hydro n'a pas pu récupérer de données liées à cette installation."
            variant="naked"
            class="sm:absolute sm:-translate-y-1/2 sm:top-1/2"
          />
        </div>
      </template>
    </UTabs>
    <template
      v-if="installationHasOuvrage"
      #footer
    >
      <UButton
        icon="lucide:arrow-left"
        color="neutral"
        variant="ghost"
        class="cursor-pointer rounded"
        @click="updateInstallation(installationData.ouvrage_id)"
      >
        Retour
      </UButton>
    </template>
  </UIPanel>
  <ModalDetailedChart
    v-model="detailedChartModalOpen"
    :releves-type="detailedChartType"
    :releves="groupedReleves[detailedChartType]?.chartReleves"
    :points="detailedChartPoints"
    :stats="chartStats"
    :timezone="localTimezone"
    :unit="groupedReleves[detailedChartType]?.unit || ''"
  />
</template>

<script setup>
  import {
    getDistance,
  } from "geolib";
  import {
    installationTypeMapping,
    dataTypeReleveMapping,
    valueTypeMapping,
  } from "~/utils/constants/mapping.js";
  import {
    calculateChartStats,
  } from "~/utils/calculations.js";
  import {
    convertToDMS,
  } from "~/utils/formatting.js";
  import {
    processReleves,
  } from "~/utils/processing.js";
  import {
    Line,
  } from "vue-chartjs";
  import {
    buildChartData,
    buildChartOptions,
  } from "~/utils/chart.js";
  import {
    buildRelevesTableColumns,
    shouldDisplayMeasureAlert,
    excludedDataTypesForStats,
    installationTabs,
  } from "~/utils/constants/installation.js";

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

  const route = useRoute(),
        router = useRouter();

  const open = ref(props.modelValue),
        installationData = ref(null),
        isPending = ref(true),
        activeTab = ref("0"),
        detailedChartType = ref(null),
        detailedChartPoints = ref([]),
        detailedChartModalOpen = ref(false);

  const localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone,
        installationCache = new Map();

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);

    // Si le panneau est ouvert
    if (newValue === true) {
      const installationId = props.defaultData?.objectid,
            installationType = props.defaultData?.type?.toLowerCase();
      if (!installationId) {
        isPending.value = false;
        return;
      }

      // Si l'installation est différente de celle déjà chargée
      if (installationData.value?.id !== installationId) {
        installationData.value = null;

        await loadInstallation(installationId);
      }

      // Mettre à jour les paramètres de l'URL d'après l'installation sélectionnée
      router.replace({
        query: {
          ...route.query,
          installation: installationId,
          type: installationType,
          territoire: undefined,
        },
      });
    }
    // Si le panneau est fermé
    else {
      isPending.value = false;
      activeTab.value = "0";

      // Réinitialiser les paramètres de l'URL
      router.replace({
        query: {
          ...route.query,
          installation: undefined,
          type: undefined,
          territoire: undefined,
        },
      });
    }
  });

  const installationName = computed(() => {
    if (!installationData.value) {
      return props.defaultData.nom || "Inconnu";
    }

    return installationData.value.nom;
  });

  const installationType = computed(() => {
    if (!installationData.value) {
      return installationTypeMapping[props.defaultData.type] || "Inconnu";
    }

    return installationTypeMapping[installationData.value.type];
  });

  const installationHasData = computed(() => {
          return installationData.value && installationData.value.releves && installationData.value.releves.length > 0;
        }),
        installationHasSondes = computed(() => {
          return installationData.value && installationData.value.sondes && installationData.value.sondes.length > 0;
        }),
        installationHasOuvrage = computed(() => {
          return installationData.value && installationData.value.ouvrage_id;
        });

  const relevesByDataType = computed(() => {
    if (!installationData.value || !installationData.value.releves) return {};

    return processReleves(installationData.value.releves);
  });

  const groupedReleves = computed(() => {
    return Object.fromEntries(
      // Définir un ensemble d'objets pour chaque groupe de relevés
      Object.entries(relevesByDataType.value)
        .map(([type_releves, releves]) => {
          // Inverser l'ordre des relevés
          const chartReleves = [...releves].reverse(),
                firstReleve = releves[0];

          return [
            type_releves,
            {
              type_releves,
              releves,
              chartReleves,
              chartPoints: chartReleves.map(releve => ({
                x: new Date(releve.date),
                y: releve.valeur,
              })),
              unit: firstReleve?.unite_valeur || "",
            },
          ];
        }),
    );
  });

  const chartStats = computed(() => {
    return calculateChartStats(detailedChartPoints.value, localTimezone);
  });

  async function fetchInstallation(id) {
    if (installationCache.has(id)) {
      return installationCache.get(id);
    }

    // Récupérer les données de l'installation
    const response = await $fetch(`/api/installations/${id}`),
          installationData = markRaw(response.data);

    installationCache.set(id, installationData);

    return installationData;
  }

  async function loadInstallation(id) {
    isPending.value = true;

    try {
      installationData.value = await fetchInstallation(id);
    }
    finally {
      isPending.value = false;
    }
  }

  async function updateInstallation(id) {
    if (!id || !installationData.value || isPending.value) return;
    if (installationData.value.id === id) return;

    await loadInstallation(id);
  }

  function openDetailedChart(type_releves, releves) {
    // Ouvrir le graphique détaillé
    detailedChartType.value = type_releves;
    detailedChartPoints.value = releves;

    detailedChartModalOpen.value = true;
  }
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
