<template>
  <USlideover
    v-model:open="open"
    side="right"
    inset
    dismissible
    overlay
    modal
    :ui="{
      overlay: 'md:bg-transparent',
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
            {{ regionTitle }}
          </h2>
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
        v-if="hasData"
        class="h-full min-h-0 flex flex-col"
      >
        <UTabs
          :items="regionData"
          color="neutral"
          variant="link"
          class="h-full min-h-0 flex flex-col"
          :ui="{
            root: 'gap-0',
            list: 'px-5 sm:px-6 shrink-0',
            content: 'flex-1 min-h-0 h-full overflow-y-auto py-5 sm:py-6 pl-5 sm:pl-6 pr-3.75 sm:pr-4.75 mt-px content-scrollbar',
            trigger: 'w-full px-0 cursor-pointer',
          }"
        >
          <template #content="{ item }">
            <div class="flex flex-col gap-2.5 sm:gap-3">
              <div class="flex flex-col gap-1.5">
                <span class="text-highlighted font-medium">
                  {{ item.label }}
                </span>
                <p class="text-sm">
                  {{ item.description }}
                </p>
              </div>
              <UILabeledNumber
                :value="formatValue(item.total, item.type === 'ghg')"
                :label="item.type === 'ghg' ? 'Moyenne réseau' : 'Total'"
                :unit="item.type === 'ghg' ? 'gCO2eq/kWh' : 'MW'"
                size="lg"
              />
              <div class="grid grid-cols-2 gap-2.5 sm:gap-3">
                <UILabeledNumber
                  v-for="value in item.data"
                  :key="value.key"
                  :label="value.label"
                  :value="formatValue(value.value, item.type === 'ghg')"
                  :unit="item.type === 'ghg' ? 'gCO2eq/kWh' : 'MW'"
                />
              </div>
            </div>
          </template>
        </UTabs>
      </div>
      <div
        v-else
        class="flex h-full items-center justify-center"
      >
        <UEmpty
          icon="lucide:circle-off"
          title="Aucune donnée"
          description="Atlas Hydro n'a pas pu récupérer de données électriques pour cette région."
          variant="naked"
        />
      </div>
    </template>
    <template
      v-if="hasData"
      #footer
    >
      <div class="flex w-full items-center justify-end text-[13px] text-muted leading-tight sm:leading-none">
        <span class="text-right">Sur les dernières 24 heures</span>
      </div>
    </template>
  </USlideover>
</template>

<script setup>
  import {
    electricityTypeMapping,
    ghgEnergySourceNamesMapping,
    regionNameMapping,
    regionNameToIdMapping,
  } from "~/utils/mapping.ts";

  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    region: {
      type: String,
      default: null,
    },
    data: {
      type: Object,
      default: null,
    },
  });

  const emit = defineEmits([
    "update:modelValue",
  ]);

  const open = ref(false);

  const regionId = computed(() => {
    return regionNameToIdMapping[props.region] || props.region;
  });

  const regionTitle = computed(() => {
    return regionNameMapping[regionId.value] || props.region || "Inconnu";
  });

  const usageData = computed(() => {
    return filterEntries(props.data?.consommation || {}).map(([key, value]) => ({
      key,
      label: electricityTypeMapping[key] || key,
      value,
    }));
  });

  const productionData = computed(() => {
    return filterEntries(props.data?.production || {}).map(([key, value]) => ({
      key,
      label: electricityTypeMapping[key] || key,
      value,
    }));
  });

  const ghgData = computed(() => {
    return filterEntries(props.data?.facteurs_ges?.[regionId.value] || {}, true).map(([key, value]) => ({
      key,
      label: ghgEnergySourceNamesMapping[key] || key,
      value,
    }));
  });

  const ghgTotal = computed(() => {
    return Number(props.data?.facteurs_ges?.[regionId.value]?.electricite ?? 0);
  });

  const importData = computed(() => {
    return filterEntries(props.data?.importation?.[regionId.value] || {}).map(([key, value]) => ({
      key,
      label: electricityTypeMapping[key] || key,
      value,
    }));
  });

  const importTotal = computed(() => {
    return Number(props.data?.importation?.[regionId.value]?.total ?? 0);
  });

  const exportTotal = computed(() => {
    const value = Number(props.data?.exportation?.[regionId.value] ?? 0);

    return value > 0 ? value : 0;
  });

  const regionData = computed(() => {
    const allData = [];

    if (exportTotal.value > 0) {
      allData.push({
        type: "export",
        label: "Exportation",
        description: "Quantité d'électricité exportée vers la région par Hydro-Québec.",
        total: exportTotal.value,
        data: [],
      });
    }

    if (importTotal.value > 0) {
      allData.push({
        type: "import",
        label: "Importation",
        description: "Quantité d'électricité importée au Québec par Hydro-Québec.",
        total: importTotal.value,
        data: importData.value,
      });
    }

    if (regionId.value === "Quebec") {
      allData.push({
        type: "production",
        label: "Production",
        description: "Quantité d'électricité produite au Québec par Hydro-Québec.",
        total: props.data?.production?.total ?? 0,
        data: productionData.value,
      }, {
        type: "usage",
        label: "Consommation",
        description: "Quantité d'électricité produite par Hydro-Québec et consommée au Québec.",
        total: props.data?.consommation?.total ?? 0,
        data: usageData.value,
      });
    }

    if (ghgTotal.value > 0) {
      allData.push({
        type: "ghg",
        label: "Émissions",
        description: "Quantité d'émissions directes de gaz à effet de serre générée pour chaque kilowattheure d'électricité produit.",
        total: ghgTotal.value,
        data: ghgData.value,
      });
    }

    return allData;
  });

  const hasData = computed(() => {
    return regionData.value.length > 0;
  });

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);
  });

  function filterEntries(data, isGhg = false) {
    return Object.entries(data)
      .filter(([key, value]) => key !== "total" && (!isGhg || key !== "electricite") && Number(value) > 0.005)
      .sort((a, b) => b[1] - a[1]);
  }

  function formatValue(value, isGhg = false) {
    if (isGhg) {
      return (Number(value ?? 0) * 1000).toFixed(2).toLocaleString();
    }

    return Math.round(Number(value ?? 0)).toLocaleString();
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
