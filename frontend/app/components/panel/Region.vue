<template>
  <UIPanel
    v-model="open"
    :title="regionName"
    :is-loading="!data"
  >
    <div
      v-if="regionHasData"
      class="h-full min-h-0 flex flex-col"
    >
      <UTabs
        v-model="activeTab"
        :items="regionData"
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
      class="flex h-full justify-center items-center"
    >
      <UEmpty
        icon="lucide:circle-off"
        title="Aucune donnée"
        description="Atlas Hydro n'a pas pu récupérer de données liées à cette région."
        variant="naked"
        class="sm:absolute sm:-translate-y-1/2 sm:top-1/2"
      />
    </div>
  </UIpanel>
</template>

<script setup>
  import {
    electricityTypeMapping,
    ghgEnergySourceNamesMapping,
    regionNameMapping,
  } from "~/utils/constants/mapping.js";

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

  const route = useRoute(),
        router = useRouter();

  const open = ref(props.modelValue),
        activeTab = ref("0");

  const regionName = computed(() => {
    return regionNameMapping[props.region] || props.region || "Inconnu";
  });

  const data = computed(() => {
    return {
      consommation: filterData(props.data.consommation || {}, electricityTypeMapping),
      production: filterData(props.data.production || {}, electricityTypeMapping),
      facteurs_ges: filterData(props.data.facteurs_ges?.[props.region] || {}, ghgEnergySourceNamesMapping, true),
      importation: filterData(props.data.importation?.[props.region] || {}, electricityTypeMapping),
    };
  });

  const total = computed(() => {
    return {
      facteurs_ges: Number(props.data?.facteurs_ges?.[props.region]?.electricite ?? 0),
      importation: Number(props.data?.importation?.[props.region]?.total ?? 0),
      exportation: Number(props.data?.exportation?.[props.region] ?? 0),
    };
  });

  const regionData = computed(() => {
    const chunks = [];

    if (total.value.exportation > 0) {
      chunks.push({
        type: "export",
        label: "Exportation",
        description: "Quantité d'électricité exportée vers la région par Hydro-Québec au cours des dernières 24 heures.",
        total: total.value.exportation,
        data: [],
      });
    }

    if (total.value.importation > 0) {
      chunks.push({
        type: "import",
        label: "Importation",
        description: "Quantité d'électricité importée au Québec par Hydro-Québec au cours des dernières 24 heures.",
        total: total.value.importation,
        data: data.value.importation,
      });
    }

    if (props.region === "Quebec") {
      chunks.push({
        type: "production",
        label: "Production",
        description: "Quantité d'électricité produite au Québec par Hydro-Québec au cours des dernières 24 heures.",
        total: props.data?.production?.total ?? 0,
        data: data.value.production,
      }, {
        type: "usage",
        label: "Consommation",
        description: "Quantité d'électricité produite par Hydro-Québec et consommée au Québec au cours des dernières 24 heures.",
        total: props.data?.consommation?.total ?? 0,
        data: data.value.consommation,
      });
    }

    if (total.value.facteurs_ges > 0) {
      chunks.push({
        type: "ghg",
        label: "Émissions",
        description: "Quantité d'émissions directes de gaz à effet de serre générée pour chaque kilowattheure d'électricité produit.",
        total: total.value.facteurs_ges,
        data: data.value.facteurs_ges,
      });
    }

    return chunks;
  });

  const regionHasData = computed(() => {
    return regionData.value.length > 0;
  });

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, async (newValue) => {
    emit("update:modelValue", newValue);

    if (!newValue) {
      router.replace({
        query: {
          ...route.query,
          territoire: undefined,
          installation: undefined,
          type: undefined,
        },
      });

      activeTab.value = "0";
    }
    else {
      router.replace({
        query: {
          ...route.query,
          territoire: props.region,
          installation: undefined,
          type: undefined,
        },
      });
    }
  });

  function filterData(data, mapping, isGhg = false) {
    return Object.entries(data)
      .filter(([key, value]) => key !== "total" && Number(value) > 0 && (!isGhg || (key !== "electricite" && Number(value) > 0.005)))
      .sort((a, b) => b[1] - a[1])
      .map(([key, value]) => ({
        key,
        label: mapping[key] || key,
        value,
      }));
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
