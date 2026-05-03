<template>
  <UModal
    v-model:open="open"
    :title="dataTypeReleveMapping[relevesType] || 'Inconnu'"
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
        v-if="points.length > 0"
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
            :data="buildChartData(points, relevesType)"
            :options="buildChartOptions(releves, timezone, stats, true)"
          />
        </UCard>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 sm:my-1.5">
          <UILabeledNumber
            v-for="([key, value]) in Object.entries(stats).filter(([_, value]) => typeof value === 'number')"
            :key="key"
            :label="detailedChartStatsMapping[key] || key"
            :value="Number(value.toFixed(2)).toLocaleString()"
            :unit="unit || ''"
          />
        </div>
        <div class="h-px bg-border w-full" />
        <div class="flex items-center justify-between text-[13px] text-muted leading-tight sm:leading-none">
          <span class="text-left">Sur {{ points.length }} mesures</span>
          <span class="text-right">Du {{ stats.dateRange[0] }} au {{ stats.dateRange[1] }}</span>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup>
  import {
    dataTypeReleveMapping,
    detailedChartStatsMapping,
  } from "~/utils/constants/mapping.js";
  import {
    Line,
  } from "vue-chartjs";
  import {
    buildChartData,
    buildChartOptions,
  } from "~/utils/chart.js";

  const props = defineProps({
    modelValue: {
      type: Boolean,
      required: true,
    },
    relevesType: {
      type: String,
      default: "",
    },
    releves: {
      type: Object,
      default: () => ({}),
    },
    points: {
      type: Array,
      default: () => [],
    },
    stats: {
      type: Object,
      default: () => ({}),
    },
    timezone: {
      type: String,
      required: true,
    },
    unit: {
      type: String,
      default: "",
    },
  });

  const open = ref(props.modelValue);

  const emit = defineEmits([
    "update:modelValue",
  ]);

  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, (newValue) => {
    emit("update:modelValue", newValue);
  });
</script>
