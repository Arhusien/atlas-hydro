<template>
  <UButton
    icon="lucide-info"
    color="neutral"
    variant="solid"
    size="lg"
    square
    class="cursor-pointer"
  >
    <span class="sr-only">Informations sur ...</span>
  </UButton>
</template>

<script setup>
  defineProps({
    data: {
      type: Object,
      required: true,
    },
  });
</script>
