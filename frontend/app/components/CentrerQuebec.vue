<template>
  <UTooltip
    :delay-duration="0"
    text="Centrer sur le Québec"
    :content="{
      side: 'right',
      sideOffset: 10,
    }"
  >
    <UButton
      icon="lucide-house"
      color="neutral"
      variant="solid"
      size="lg"
      square
      :disabled="disabled"
      class="cursor-pointer"
      @click="emit('center')"
    >
      <span class="sr-only">Centrer sur le Québec</span>
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
    "center",
  ]);
</script>
