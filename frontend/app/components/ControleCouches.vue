<template>
  <UPopover
    :ui="{
      //content: 'rounded',
    }"
    :content="{
      side: 'right',
      sideOffset: 16,
    }"
  >
    <UTooltip
      :delay-duration="0"
      text="Couches"
      :content="{
        side: 'right',
        sideOffset: 10,
      }"
    >
      <UButton
        icon="lucide-layers"
        color="neutral"
        variant="solid"
        size="lg"
        square
        class="cursor-pointer"
      >
        <span class="sr-only">Couches</span>
      </UButton>
    </UTooltip>
    <template #content>
      <div class="flex flex-col items-start justify-center gap-2 py-2.5 px-3">
        <UCheckbox
          v-model="layerStates.centrale"
          label="Centrales"
          color="neutral"
        />
        <UCheckbox
          v-model="layerStates.barrage"
          label="Barrages"
          color="neutral"
        />
        <UCheckbox
          v-model="layerStates.sonde"
          label="Sondes"
          color="neutral"
        />
      </div>
    </template>
  </UPopover>
</template>

<script setup>
  const props = defineProps({
    modelValue: {
      type: Object,
      required: true,
    },
  });

  const emit = defineEmits([
    "update:modelValue",
  ]);

  const layerStates = ref(props.modelValue);

  watch(layerStates, (newValue) => {
    emit("update:modelValue", newValue);
  }, {
    deep: true,
  });
</script>
