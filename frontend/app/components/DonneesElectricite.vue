<template>
  <UNavigationMenu
    as="div"
    :items="items"
    :ui="{
      viewport: 'w-full sm:w-(--reka-navigation-menu-viewport-width) max-w-[calc(100svw-2rem)] ring-0',
      content: 'w-auto pointer-events-auto',
      item: 'py-0',
      link: 'p-0 before:hidden hover:text-inherit data-[state=open]:text-inherit',
      list: 'gap-2.5',
    }"
    class="w-full justify-center flex items-center"
    color="neutral"
    :unmount-on-hide="false"
  >
    <template
      v-for="item in items"
      :key="item.slot"
      #[item.slot]
    >
      <UButton
        as="span"
        :icon="item.icon"
        color="neutral"
        variant="solid"
        size="lg"
        class="cursor-pointer mb-2.5"
        :label="item.label"
        :disabled="disabled"
        :ui="{
          base: 'p-2 md:px-3 md:py-2',
          label: 'sr-only md:not-sr-only',
        }"
        :class="{
          'pointer-events-none': dragging,
          'pointer-events-auto': !dragging,
        }"
      />
    </template>
    <template
      v-for="item in items.filter(i => ['prod', 'usage'].includes(i.slot))"
      :key="item.slot"
      #[`${item.slot}-content`]
    >
      <div class="flex flex-col gap-2.5 sm:gap-3 p-5 sm:p-6">
        <div class="flex flex-col gap-1.25 sm:gap-1.5">
          <h3 class="text-highlighted font-medium">
            {{ item.label }}
          </h3>
          <span class="text-sm">
            {{ item.description }}
          </span>
        </div>
        <div class="flex flex-col gap-2">
          <div class="inline leading-none">
            <span class="text-2xl sm:text-3xl text-default font-semibold">
              {{ Math.round(Number(item.total ?? 0)).toLocaleString() }}
            </span>
            <span class="text-muted font-medium text-sm sm:text-base">&nbsp;MW</span>
          </div>
        </div>
        <div class="h-px bg-border w-full" />
        <div class="gap-2.5 sm:gap-6 grid grid-cols-2 sm:grid-cols-4 sm:w-xl">
          <div
            v-for="([source, valeur]) in item.data"
            :key="source"
            class="flex flex-col gap-0.5"
          >
            <span class="text-sm text-muted">{{ electicityTypeMapping[source] || "Inconnu" }}</span>
            <div class="inline leading-none">
              <span class="text-lg sm:text-2xl text-default font-semibold">
                {{ Math.round(Number(valeur)).toLocaleString() }}
              </span>
              <span class="text-xs sm:text-sm text-muted font-medium">&nbsp;MW</span>
            </div>
            <!-- TODO: Ajouter ce que représente la valeur par rapport au total (proportion)? -->
          </div>
        </div>
      </div>
    </template>
  </UNavigationMenu>
</template>

<script setup>
  import {
    electicityTypeMapping,
    // renewableElectricityTypes,
  } from "~/utils/mapping.ts";

  const props = defineProps({
    disabled: {
      type: Boolean,
      default: false,
    },
    dragging: {
      type: Boolean,
      default: false,
    },
    data: {
      type: Object,
      default: () => ({}),
    },
  });

  const productionEntries = computed(() => {
    const production = props.data?.production ?? {};

    return Object.entries(production).filter(([s, v]) => s !== "total" && v > 0).sort((a, b) => b[1] - a[1]);
  });

  const usageEntries = computed(() => {
    const usage = props.data?.consommation ?? {};

    return Object.entries(usage).filter(([s, v]) => s !== "total" && v > 0).sort((a, b) => b[1] - a[1]);
  });

  const items = computed(() => [
    {
      label: "Production",
      description: "Quantité d'électricité produite au Québec au cours des dernières 24 heures.",
      icon: "lucide:zap",
      slot: "prod",
      type: "trigger",
      total: props.data?.production?.total ?? 0,
      data: productionEntries.value,
    },
    {
      label: "Consommation",
      description: "Quantité d'électricité consommée au Québec au cours des dernières 24 heures.",
      icon: "lucide:plug",
      slot: "usage",
      type: "trigger",
      total: props.data?.consommation?.total ?? 0,
      data: usageEntries.value,
    },
    {
      label: "Exportation",
      icon: "lucide:arrow-up-from-dot",
      slot: "export",
      type: "trigger",
    },
    {
      label: "Importation",
      icon: "lucide:arrow-down-to-dot",
      slot: "import",
      type: "trigger",
    },
  ]);
</script>
