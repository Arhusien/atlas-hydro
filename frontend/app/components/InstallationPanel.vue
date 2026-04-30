<template>
  <USlideover
    v-model:open="open"
    side="right"
    inset
    dismissible
    :overlay="$device.isMobile"
    :modal="$device.isMobile"
    :ui="{
      overlay: 'sm:bg-transparent',
      header: 'px-5',
      content: 'ring-0 sm:ring-0',
      body: 'flex-1 overflow-hidden p-0 sm:p-0',
      footer: 'px-4 sm:px-4 min-h-16',
    }"
  >
    <template #header="{ close }">
      <div class="flex w-full items-center gap-2">
        <div class="flex w-full min-w-0 items-center gap-2">
          <h2 class="truncate text-highlighted font-medium">
            {{ installationData?.nom || defaultData.nom || 'Inconnu' }}
          </h2>
          <UBadge
            color="neutral"
            variant="soft"
            class="rounded"
          >
            {{ installationTypeMapping[installationData?.type || defaultData.type] || 'Inconnu' }}
          </UBadge>
        </div>
        <UButton
          icon="lucide:x"
          color="neutral"
          variant="ghost"
          square
          class="cursor-pointer rounded -mr-2"
          @click="close"
        >
          <span class="sr-only">Fermer</span>
        </UButton>
      </div>
    </template>
    <template #body>
      <div
        v-if="isPending"
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
          :items="tabs"
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
          <template #infos>
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
                v-if="computedReleves.length > 0"
                class="flex flex-col gap-2.5 sm:gap-3"
              >
                <h3 class="text-highlighted font-medium">
                  Dernières mesures
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                  <UCard
                    v-for="({ type_releves, releves }) in computedReleves"
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
                        {{ `${releves[0].valeur.toFixed(2)} ${releves[0]?.unite_valeur || ''}` }}
                      </span>
                    </div>
                    <span class="text-sm text-muted text-center">{{ dataTypeReleveMapping[type_releves] || 'Inconnu' }}</span>
                  </UCard>
                </div>
              </div>
              <div
                v-if="installationData?.sondes && installationData.sondes.length > 0"
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
                  @click="updateData(sonde.id);"
                >
                  <span class="text-left text-default">{{ sonde.nom || 'Inconnu' }}</span>
                  <span class="text-muted text-right">{{ getDistance(
                    { latitude: installationData.y, longitude: installationData.x },
                    { latitude: sonde.y, longitude: sonde.x },
                  ) }} mètres</span>
                </UCard>
              </div>
            </div>
          </template>
          <template #data>
            <div
              v-if="computedReleves.length > 0"
              class="flex flex-col gap-2.5 sm:gap-3"
            >
              <h3 class="text-highlighted font-medium">
                Mesures
              </h3>
              <UAccordion
                v-for="({ type_releves, releves }) in computedReleves"
                :key="type_releves"
                :items="[
                  {
                    label: dataTypeReleveMapping[type_releves] || 'Inconnu',
                    content: releves,
                  },
                ]"
                :ui="{
                  trigger: 'p-4 bg-elevated/50 font-normal rounded-md cursor-pointer data-[state=open]:rounded-b-none transition hover:bg-elevated gap-2',
                  content: `bg-elevated/50 rounded-b-md data-[state=open]:animate-[accordion-down_var(--duration)_ease-out] data-[state=closed]:animate-[accordion-up_var(--duration)_ease-out]`,
                }"
                :style="{
                  '--duration': `${Math.min(150 + (releves.length * 10), 500)}ms`,
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
                    :data="item.content"
                    :columns="columns"
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
              class="flex flex-col items-center justify-center"
            >
              <UEmpty
                icon="lucide:circle-off"
                title="Aucune donnée"
                description="Atlas Hydro n'a pas pu récupérer de données liées à cette installation."
                variant="naked"
              />
            </div>
          </template>
          <template #stats>
            <div
              v-if="computedReleves.length > 0"
              class="flex flex-col gap-2.5 sm:gap-3"
            >
              <h3 class="text-highlighted font-medium">
                Graphiques
              </h3>
              <div class="flex flex-col gap-2.5 sm:gap-3">
                <UCard
                  v-for="({ type_releves, chartPoints }) in computedChartPoints.filter((e) => !excludedDataTypesForDifference.includes(e.type_releves))"
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
                        @click="zoomInChart(type_releves, chartPoints)"
                      />
                    </UTooltip>
                  </div>
                  <Line
                    :data="{
                      datasets: [
                        {
                          ...chartDefaultOptionsDataset,
                          label: dataTypeReleveMapping[type_releves] || 'Inconnu',
                          data: chartPoints,
                        },
                      ],
                    }"
                    :options="{
                      ...chartDefaultOptions,
                      plugins: {
                        ...chartDefaultOptions.plugins,
                        tooltip: {
                          ...chartDefaultOptions.plugins.tooltip,
                          callbacks: {
                            title: (ctx) => createTooltipTitle(ctx, type_releves),
                            label: (ctx) => createTooltipLabel(ctx, type_releves),
                          },
                        },
                      },
                      scales: {
                        ...chartDefaultOptions.scales,
                        x: {
                          ...chartDefaultOptions.scales.x,
                          ticks: {
                            ...chartDefaultOptions.scales.x.ticks,
                            display: false,
                          },
                          adapters: {
                            date: {
                              locale: fr,
                            },
                          },
                        },
                      },
                    }"
                  />
                </UCard>
              </div>
            </div>
            <div
              v-else
              class="flex flex-col items-center justify-center"
            >
              <UEmpty
                icon="lucide:circle-off"
                title="Aucune donnée"
                description="Atlas Hydro n'a pas pu récupérer de données liées à cette installation."
                variant="naked"
              />
            </div>
          </template>
        </UTabs>
      </div>
    </template>
    <template
      v-if="installationData && installationData.ouvrage_id"
      #footer
    >
      <UButton
        icon="lucide:arrow-left"
        color="neutral"
        variant="ghost"
        class="cursor-pointer rounded"
        @click="updateData(installationData.ouvrage_id);"
      >
        Retour
      </UButton>
    </template>
  </USlideover>
  <UModal
    v-model:open="bigChartModalOpen"
    :title="dataTypeReleveMapping[bigChartType] || 'Inconnu'"
    close-icon="lucide:x"
    :ui="{
      header: 'p-5',
      content: 'w-[calc(100vw-2rem)] max-w-xl ring-0',
      close: 'cursor-pointer rounded',
      body: 'p-5',
    }"
  >
    <template #body>
      <div
        v-if="bigChartPoints.length > 0"
        class="flex flex-col gap-2.5 sm:gap-3"
      >
        <UCard
          variant="soft"
          :ui="{
            root: 'rounded-md',
            body: 'sm:p-4 p-4 text-sm font-normal flex flex-col justify-center w-full h-full gap-4',
          }"
        >
          <Line
            :data="{
              datasets: [
                {
                  ...chartDefaultOptionsDataset,
                  label: dataTypeReleveMapping[bigChartType] || 'Inconnu',
                  data: bigChartPoints,
                },
              ],
            }"
            :options="{
              ...chartDefaultOptions,
              plugins: {
                ...chartDefaultOptions.plugins,
                tooltip: {
                  ...chartDefaultOptions.plugins.tooltip,
                  callbacks: {
                    title: (ctx) => createTooltipTitle(ctx, bigChartType, true),
                    label: (ctx) => createTooltipLabel(ctx, bigChartType, true),
                    afterLabel: (ctx) => createTooltipAfterLabel(ctx, bigChartType),
                  },
                },
              },
              scales: {
                ...chartDefaultOptions.scales,
                x: {
                  ...chartDefaultOptions.scales.x,
                  adapters: {
                    date: {
                      locale: fr,
                    },
                  },
                },
              },
            }"
          />
        </UCard>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 sm:my-1.5">
          <UILabeledNumber
            v-for="([key, value]) in Object.entries(chartStats).filter(([_, value]) => typeof value === 'number')"
            :key="key"
            :label="bigChartStatsMapping[key] || key"
            :value="Number(value.toFixed(2)).toLocaleString()"
            :unit="computedReleves.find(e => e.type_releves === bigChartType)?.relevesAscending?.[0]?.unite_valeur || ''"
          />
        </div>
        <div class="h-px bg-border w-full" />
        <div class="flex items-center justify-between text-[13px] text-muted leading-tight sm:leading-none">
          <span class="text-left">Sur {{ bigChartPoints.length }} mesures</span>
          <span class="text-right">Du {{ chartStats.dateRange[0] }} au {{ chartStats.dateRange[1] }}</span>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup>
  import chartDefaultOptionsDataset from "~/utils/chartDefaultOptionsDataset.json";
  import chartDefaultOptions from "~/utils/chartDefaultOptions.json";
  import {
    LoaderCircle,
    TrendingUp,
    TrendingDown,
    Minus,
  } from "@lucide/vue";
  import {
    getDistance,
  } from "geolib";
  import {
    DateTime,
  } from "luxon";
  import {
    installationTypeMapping,
    dataTypeReleveMapping,
    valueTypeMapping,
    bigChartStatsMapping,
  } from "~/utils/mapping.ts";
  import {
    calculateDifference,
    calculateChartStats,
  } from "~/utils/calculations.ts";
  import {
    convertToDMS,
    formatToLocalDate,
  } from "~/utils/formatting.ts";
  import {
    processReleves,
  } from "~/utils/processing.ts";
  import {
    Line,
  } from "vue-chartjs";
  import {
    fr,
  } from "date-fns/locale";

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
        bigChartType = ref(null),
        bigChartPoints = ref([]),
        bigChartModalOpen = ref(false);

  const excludedDataTypesForDifference = [
          "DIRECTION_VENT",
        ],
        localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone,
        installationCache = new Map();

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(installationData, (newData) => {
    if (newData) {
      const installationId = newData.id,
            installationType = newData.type.toLowerCase();

      router.replace({
        query: {
          ...route.query,
          installation: installationId,
          type: installationType,
          region: undefined,
        },
      });
    }
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);

    if (newValue === true) {
      const installationId = props.defaultData?.objectid;
      if (!installationId) {
        isPending.value = false;
        return;
      }

      if (installationData.value?.id === installationId && !isPending.value) {
        return;
      }

      installationData.value = null;

      await loadInstallation(installationId);
    }
    else {
      resetStates();
      isPending.value = false;

      router.replace({
        query: {
          ...route.query,
          installation: undefined,
          type: undefined,
          region: undefined,
        },
      });
    }
  });

  const tabs = [
    {
      label: "Informations",
      // icon: "lucide:info",
      slot: "infos",
    },
    {
      label: "Mesures",
      // icon: "lucide:activity",
      slot: "data",

    },
    {
      label: "Graphiques",
      // icon: "lucide:satellite-dish",
      slot: "stats",
    },
  ];

  const columns = [
    {
      id: "date",
      accessorKey: "date",
      header: "Date",
      cell: ({ row }) => {
        return row.getValue("date")
          ? formatToLocalDate(row.getValue("date"), localTimezone)
          : "Inconnu";
      },
    },
    {
      id: "difference",
      header: "Différence",
      cell: ({ row }) => {
        const relevesOfSameType = computedReleves.value.find(e => e.type_releves === row.original.type_donnee)?.relevesAscending || [],
              delta = calculateDifference(row.original, relevesOfSameType);

        if (excludedDataTypesForDifference.includes(row.original.type_donnee) || delta === null) {
          return h("div", {
            class: "flex items-center gap-2",
          }, [
            h(Minus, {
              class: "size-4.5 text-toned",
            }),
            h("span", {
              class: "text-toned",
            }, "S. O."),
          ]);
        }

        return h("div", {
          class: "flex items-center gap-2",
        }, [
          delta > 0 && h(TrendingUp, {
            class: "size-4.5 text-green-500",
          }),
          delta < 0 && h(TrendingDown, {
            class: "size-4.5 text-red-500",
          }),
          delta === 0 && h(Minus, {
            class: "size-4.5 text-toned",
          }),
          h("span", {
            class: "text-toned",
          }, `${Math.abs(delta).toFixed(2)} ${row.original.unite_valeur}`),
        ]);
      },
    },
    {
      id: "valeur",
      accessorKey: "valeur",
      header: "Valeur",
      cell: ({ row }) => {
        return `${row.getValue("valeur").toFixed(2)} ${row.original.unite_valeur}`;
      },
      meta: {
        class: {
          td: "text-toned",
        },
      },
    },
  ];

  const relevesByDataType = computed(() => {
    if (!installationData.value || !installationData.value.releves) return {};

    return processReleves(installationData.value.releves);
  });

  const computedReleves = computed(() => {
    return Object.entries(relevesByDataType.value)
      .map(([type_releves, releves]) => {
        const relevesAscending = [...releves].reverse();

        return {
          type_releves,
          releves,
          relevesAscending,
        };
      });
  });

  const computedChartPoints = computed(() => {
    return computedReleves.value.map(({ type_releves, relevesAscending }) => ({
      type_releves,
      chartPoints: markRaw(
        relevesAscending.map(releve => ({
          x: new Date(releve.date),
          y: releve.valeur,
        })),
      ),
    }));
  });

  const chartStats = computed(() => {
    return calculateChartStats(bigChartPoints.value, localTimezone);
  });

  async function fetchInstallation(id) {
    if (installationCache.has(id)) {
      return installationCache.get(id);
    }

    const response = await $fetch(`/api/installations/${id}`),
          installationData = markRaw(response.data);

    installationCache.set(id, installationData);

    return installationData;
  }

  function resetStates() {
    bigChartModalOpen.value = false;
    bigChartType.value = null;
    bigChartPoints.value = [];
    activeTab.value = "0";
  }

  async function loadInstallation(id) {
    isPending.value = true;
    resetStates();

    try {
      installationData.value = await fetchInstallation(id);
    }
    finally {
      isPending.value = false;
    }
  }

  async function updateData(id) {
    if (!id || !installationData.value || isPending.value) return;
    if (installationData.value.id === id) return;

    await loadInstallation(id);
  }

  function zoomInChart(type_releves, releves) {
    bigChartType.value = type_releves;
    bigChartPoints.value = releves;

    bigChartModalOpen.value = true;
  }

  function shouldDisplayMeasureAlert(releveDate) {
    const releveHour = DateTime.fromISO(releveDate.split(":")[0]).setZone("UTC"),
          thresholdHour = DateTime.fromISO(
            DateTime.now().minus({ hours: 3 }).setZone("UTC").toISO().split(":")[0],
          );

    return releveHour <= thresholdHour;
  }

  function createTooltipTitle(ctx, type_releves, detailed = false) {
    const relevesAscending = computedReleves.value.find(e => e.type_releves === type_releves)?.relevesAscending || [],
          releve = relevesAscending[ctx[0].dataIndex];

    if (!detailed) {
      return releve ? formatToLocalDate(releve.date, localTimezone) : "";
    }

    return releve
      ? formatToLocalDate(releve.date, localTimezone, {
        year: "numeric",
        month: "long",
      })
      : "";
  }

  function createTooltipLabel(ctx, type_releves, detailed = false) {
    const relevesAscending = computedReleves.value.find(e => e.type_releves === type_releves)?.relevesAscending || [],
          releve = relevesAscending[ctx.dataIndex];

    if (!detailed) {
      return releve ? `${ctx.parsed.y} ${releve.unite_valeur || ""}` : "";
    }

    return releve ? `${ctx.parsed.y.toFixed(2)} ${releve.unite_valeur || ""}` : "";
  }

  function createTooltipAfterLabel(ctx, type_releves) {
    const relevesAscending = computedReleves.value.find(e => e.type_releves === type_releves)?.relevesAscending || [],
          releve = relevesAscending[ctx.dataIndex];

    const difference = calculateDifference(releve, relevesAscending),
          zScore = (releve.valeur - chartStats.value.average) / (chartStats.value.standardDeviation || 1);

    let labels = [];
    if (difference !== null) {
      labels.push(`Différence : ${difference === 0 ? "" : difference > 0 ? "+" : "-"}${Math.abs(difference).toFixed(2)} ${releve.unite_valeur || ""}`);
    }
    if (isFinite(zScore)) {
      labels.push(`Cote Z : ${zScore === 0 ? "" : zScore > 0 ? "+" : "-"}${Math.abs(zScore).toFixed(2)}`);
    }

    return labels.length > 0 ? labels.join("\n") : "";
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
