<template>
  <UTooltip
    :delay-duration="0"
    text="Utiliser la localisation"
    :content="{
      side: 'left',
      sideOffset: 10,
      updatePositionStrategy: 'always',
    }"
  >
    <UButton
      icon="lucide-locate-fixed"
      color="neutral"
      variant="solid"
      size="lg"
      square
      :disabled="disabled"
      class="cursor-pointer"
      @click="emit('locate')"
    >
      <span class="sr-only">Utiliser la localisation</span>
    </UButton>
  </UTooltip>
</template>

<script setup>
  defineProps({
    disabled: {
      type: Boolean,
      default: false,
    },
  });

  const emit = defineEmits([
    "locate",
  ]);
</script>
