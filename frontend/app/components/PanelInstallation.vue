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
          class="rounded"
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
          :items="tabs"
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
                    <div class="flex items-center justify-end gap-2">
                      <span>{{ installationData?.nom_region || 'Inconnu' }}</span>
                      <span class="text-muted">{{ installationData?.code_region || 'Inconnu' }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Latitude</span>
                    <div class="flex items-center justify-end gap-2">
                      <span>{{ convertToDMS(installationData?.y, true) || 'Inconnu' }}</span>
                      <span class="text-muted">{{ installationData?.y || 'Inconnu' }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between text-sm">
                    <span>Longitude</span>
                    <div class="flex items-center justify-end gap-2">
                      <span>{{ convertToDMS(installationData?.x, false) || 'Inconnu' }}</span>
                      <span class="text-muted">{{ installationData?.x || 'Inconnu' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div
                v-if="Object.keys(relevesByDataType)?.length > 0"
                class="flex flex-col gap-2 sm:gap-3"
              >
                <h2 class="text-highlighted font-medium">
                  Dernières mesures
                </h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                  <UCard
                    v-for="([type_releves, releves]) in Object.entries(relevesByDataType)"
                    :key="type_releves"
                    variant="soft"
                    :ui="{
                      root: 'rounded-md ',
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
                          updatePositionStrategy: 'always',
                        }"
                      >
                        <UIcon
                          v-if="shouldDisplayMeasureAlert(releves[0].date)"
                          name="i-lucide-triangle-alert"
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
                v-if="installationData.type === 'CENTRALE' && installationData?.sondes?.length > 0"
                class="flex flex-col gap-2 sm:gap-3"
              >
                <h2 class="text-highlighted font-medium">
                  Sondes à proximité
                </h2>
                <div class="flex flex-col gap-2 sm:gap-3">
                  <UCard
                    v-for="(sonde, index) in installationData.sondes"
                    :key="index"
                    as="button"
                    variant="soft"
                    :ui="{
                      root: 'rounded-md cursor-pointer has-focus-visible:ring-2 transition hover:bg-elevated has-focus-visible:ring-inverted',
                      body: 'sm:p-4 text-sm font-normal flex items-center justify-between w-full',
                    }"
                    @click="updateData(sonde);"
                  >
                    <span class="text-left text-default">{{ sonde.nom || 'Inconnu' }}</span>
                    <span class="text-muted text-right">{{ getDistance(
                      { latitude: installationData.y, longitude: installationData.x },
                      { latitude: sonde.y, longitude: sonde.x },
                    ) }} mètres</span>
                  </UCard>
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
                Mesures
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
                  content: 'bg-elevated/50 rounded-b-md data-[state=open]:animate-none data-[state=closed]:animate-none',
                }"
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
                  <UTable
                    :data="item.content"
                    :columns="columns"
                    :ui="{
                      thead: 'hidden',
                    }"
                  >
                    <template #body-top>
                      <div class="h-px w-full">
                        <div class="absolute left-0 w-full h-px bg-(--ui-border-accented)" />
                      </div>
                    </template>
                  </UTable>
                </template>
              </UAccordion>
            </div>
          </template>
          <template #stats>
            <div
              v-if="Object.keys(relevesByDataType)?.length > 0"
              class="flex flex-col gap-2 sm:gap-3"
            >
              <h2 class="text-highlighted font-medium">
                Graphiques
              </h2>
              <div class="flex flex-col gap-2 sm:gap-3">
                <UCard
                  v-for="([type_releves, releves]) in Object.entries(relevesByDataType).filter(([type, _]) => !excludedDataTypesForDifference.includes(type))"
                  :key="type_releves"
                  variant="soft"
                  :ui="{
                    root: 'rounded-md ',
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
                        updatePositionStrategy: 'always',
                      }"
                    >
                      <UIcon
                        name="i-lucide-zoom-in"
                        class="size-4.5 cursor-pointer"
                        @click="zoomInChart(type_releves, releves)"
                      />
                    </UTooltip>
                  </div>
                  <Line
                    :data="{
                      datasets: [
                        {
                          label: dataTypeReleveMapping[type_releves] || 'Inconnu',
                          data: releves.toReversed().map(r => ({
                            x: new Date(r.date),
                            y: r.valeur,
                          })),
                          fill: false,
                          borderColor: 'rgb(161 161 161)',
                          tension: 0.1,
                        },
                      ],
                    }"
                    :options="{
                      plugins: {
                        legend: {
                          display: false,
                        },
                        tooltip: {
                          backgroundColor: 'rgba(23, 23, 23, 0.95)',
                          displayColors: false,
                          caretPadding: 4,
                          titleFont: {
                            weight: '500',
                          },
                          bodyFont: {
                            weight: '400',
                          },
                          callbacks: {
                            title: function(context) {
                              const index = context[0].dataIndex,
                                    releve = releves.toReversed()[index];

                              return formatToLocalDate(releve.date, localTimezone);
                            },
                            label: function(context) {
                              const index = context.dataIndex,
                                    releve = releves.toReversed()[index];

                              return `${context.parsed.y} ${releve.unite_valeur || ''}`;
                            },
                          },
                        },
                      },
                      scales: {
                        x: {
                          ticks: {
                            display: false,
                            autoSkip: true,
                            maxTicksLimit: 10,
                          },
                          grid: {
                            color: 'rgba(38, 38, 38)',
                            drawTicks: false,
                          },
                          type: 'time',
                          adapters: {
                            date: {
                              locale: fr,
                            },
                          },
                          time: {
                            unit: 'day',
                            displayFormats: {
                              day: 'd MMM',
                            },
                          },
                        },
                        y: {
                          ticks: {
                            color: 'rgba(115 115 115)',
                          },
                          grid: {
                            color: 'rgba(38, 38, 38)',
                          },
                        },
                      },
                    }"
                  />
                </UCard>
              </div>
            </div>
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
  <UModal
    v-model:open="bigChartModalOpen"
    :title="dataTypeReleveMapping[bigChartType] || 'Inconnu'"
    close-icon="i-lucide-x"
    :ui="{
      content: 'w-[calc(100vw-2rem)] max-w-xl data-[state=open]:animate-[slide-in-from-bottom-and-fade_200ms_ease-out] data-[state=closed]:animate-[slide-out-to-bottom-and-fade_200ms_ease-in]',
      close: 'cursor-pointer',
    }"
  >
    <template #body>
      <div
        v-if="bigChartData.length > 0"
        class="flex flex-col gap-2 sm:gap-3"
      >
        <UCard
          variant="soft"
          :ui="{
            root: 'rounded-md ',
            body: 'sm:p-4 p-4 text-sm font-normal flex flex-col justify-center w-full h-full gap-4',
          }"
        >
          <Line
            :data="{
              datasets: [
                {
                  label: dataTypeReleveMapping[bigChartType] || 'Inconnu',
                  data: bigChartData.toReversed().map(r => ({
                    x: new Date(r.date),
                    y: r.valeur,
                  })),
                  fill: false,
                  borderColor: 'rgb(161 161 161)',
                  tension: 0.1,
                },
              ],
            }"
            :options="{
              animation: {
                duration: 0,
              },
              plugins: {
                legend: {
                  display: false,
                },
                tooltip: {
                  backgroundColor: 'rgba(23, 23, 23, 0.95)',
                  displayColors: false,
                  caretPadding: 4,
                  titleFont: {
                    weight: '500',
                  },
                  bodyFont: {
                    weight: '400',
                  },
                  callbacks: {
                    title: function(context) {
                      const index = context[0].dataIndex,
                            releve = bigChartData.toReversed()[index];

                      return formatToLocalDate(releve.date, localTimezone, {
                        year: 'numeric',
                        month: 'long',
                      });
                    },
                    label: function(context) {
                      const index = context.dataIndex,
                            releve = bigChartData.toReversed()[index];

                      return `${context.parsed.y.toFixed(2)} ${releve.unite_valeur || ''}`;
                    },
                    afterLabel: function(context) {
                      const index = context.dataIndex,
                            releve = bigChartData.toReversed()[index],
                            difference = calculateDifference(bigChartData, releve, true),
                            zScore = (releve.valeur - chartStats.average) / (chartStats.standardDeviation || 1);

                      let labels = [];
                      if (difference !== null) {
                        labels.push(`Différence : ${difference === 0 ? '' : difference > 0 ? '+' : '-'}${Math.abs(difference).toFixed(2)} ${releve.unite_valeur || ''}`);
                      }
                      if (zScore !== null && isFinite(zScore)) {
                        labels.push(`Cote Z : ${zScore === 0 ? '' : zScore > 0 ? '+' : '-'}${Math.abs(zScore).toFixed(2)}`);
                      }

                      return labels.length > 0 ? labels.join('\n') : '';
                    },
                  },
                },
              },
              scales: {
                x: {
                  ticks: {
                    autoSkip: true,
                    maxTicksLimit: 12,
                  },
                  grid: {
                    color: 'rgba(38, 38, 38)',
                    drawTicks: false,
                  },
                  type: 'time',
                  adapters: {
                    date: {
                      locale: fr,
                    },
                  },
                  time: {
                    unit: 'day',
                    displayFormats: {
                      day: 'd MMM',
                    },
                  },
                },
                y: {
                  ticks: {
                    color: 'rgba(115 115 115)',
                  },
                  grid: {
                    color: 'rgba(38, 38, 38)',
                  },
                },
              },
            }"
          />
        </UCard>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <UCard
            v-for="([key, value]) in Object.entries(chartStats).filter(([_, value]) => typeof value === 'number')"
            :key="key"
            variant="soft"
            :ui="{
              root: 'rounded-md',
              body: 'sm:p-4 text-sm font-normal flex flex-col items-center justify-center w-full h-full gap-0.25',
            }"
          >
            <span class="text-muted text-xs">{{ bigChartStatsMapping[key] || key }}</span>
            <span class="text-lg font-medium text-default text-center">{{ value.toFixed(2) }}</span>
            <span class="text-xs text-muted text-center">{{ bigChartData[0]?.unite_valeur || '' }}</span>
          </UCard>
        </div>
        <div class="flex items-center justify-between text-[13px] text-muted leading-none">
          <span class="text-left">Sur {{ bigChartData.length }} mesures</span>
          <span class="text-right">Du {{ chartStats.dateRange[0] }} au {{ chartStats.dateRange[1] }}</span>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup>
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

  const open = ref(props.modelValue),
        installationData = ref(null),
        pendingData = ref(true),
        installationHistoryData = ref([]),
        activeTab = ref("0"),
        bigChartType = ref(null),
        bigChartData = ref([]),
        bigChartModalOpen = ref(false);

  const excludedDataTypesForDifference = [
          "DIRECTION_VENT",
        ],
        localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

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

  const tabs = [
    {
      label: "Informations",
      // icon: "i-lucide-info",
      slot: "infos",
    },
    {
      label: "Mesures",
      // icon: "i-lucide-activity",
      slot: "data",
    },
    {
      label: "Graphiques",
      // icon: "i-lucide-satellite-dish",
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
        const delta = calculateDifference(relevesByDataType.value, row.original);

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
    if (!installationData.value || !installationData.value.releves) return [];

    return processReleves(installationData.value.releves);
  });

  const chartStats = computed(() => {
    return calculateChartStats(bigChartData.value);
  });

  function updateData(sonde) {
    installationHistoryData.value.push(installationData.value);
    installationData.value = sonde;
  }

  function zoomInChart(type_releves, releves) {
    bigChartType.value = type_releves;
    bigChartData.value = releves;

    bigChartModalOpen.value = true;
  }

  function goToPreviousInstallation() {
    if (installationHistoryData.value.length === 0) return;

    installationData.value = installationHistoryData.value.pop();

    activeTab.value = "0";
  }

  function shouldDisplayMeasureAlert(releveDate) {
    const releveHour = DateTime.fromISO(releveDate.split(":")[0]).setZone("UTC"),
          thresholdHour = DateTime.fromISO(
            DateTime.now().minus({ hours: 3 }).setZone("UTC").toISO().split(":")[0],
          );

    return releveHour <= thresholdHour;
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
