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
                  <UCard
                    v-for="(sonde, index) in installationData.sondes"
                    :key="index"
                    as="button"
                    variant="soft"
                    :ui="{
                      root: 'rounded-md cursor-pointer bg-elevated/50 has-focus-visible:ring-2 transition hover:bg-elevated has-focus-visible:ring-inverted',
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
                  <UTable
                    :data="item.content"
                    :columns="tableColumns"
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
    TrendingUp,
    TrendingDown,
    Minus,
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

  const excludedDataTypesForDifference = [
    "DIRECTION_VENT",
  ];

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

  const tableColumns = [
    {
      id: "date",
      accessorKey: "date",
      header: "Date",
      cell: ({ row }) => {
        return row.getValue("date")
          ? Intl.DateTimeFormat("fr-FR", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(new Date(row.getValue("date")))
          : "Inconnu";
      },
    },
    {
      id: "difference",
      header: "Différence",
      cell: ({ row }) => {
        const delta = caclculateDifference(row.original);

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

  function caclculateDifference(currentReleve) {
    const releves = relevesByDataType.value[currentReleve.type_donnee].toReversed(),
          indexReleve = releves.findIndex(r => r.id === currentReleve.id);

    if (indexReleve <= 0) {
      return null;
    }

    const currentValue = currentReleve.valeur,
          previousValue = releves[indexReleve - 1].valeur;

    let delta = currentValue - previousValue;
    delta = Math.round(delta * 100) / 100;

    if (!isFinite(delta) || isNaN(delta)) {
      return null;
    }

    return delta;
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
