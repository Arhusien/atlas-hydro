<template>
  <UFieldGroup orientation="vertical">
    <UButton
      icon="lucide-plus"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
      @click="emit('zoom-in')"
    >
      <span class="sr-only">Zoom avant</span>
    </UButton>
    <UButton
      icon="lucide-minus"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
      @click="emit('zoom-out')"
    >
      <span class="sr-only">Zoom arrière</span>
    </UButton>
  </UFieldGroup>
</template>

<script setup>
  const emit = defineEmits([
    "zoom-in",
    "zoom-out",
  ]);
</script>
