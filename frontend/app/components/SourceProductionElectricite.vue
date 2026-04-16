<template>
  <UTooltip
    :delay-duration="0"
    text="Sources de production d'électricité"
    :content="{
      side: 'right',
      sideOffset: 10,
    }"
  >
    <UButton
      icon="lucide-zap"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
    >
      <span class="sr-only">Sources de production d'électricité</span>
    </UButton>
  </UTooltip>
</template>
