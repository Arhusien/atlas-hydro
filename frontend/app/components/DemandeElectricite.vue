<template>
  <UTooltip
    :delay-duration="0"
    text="Demande d'électricité"
    :content="{
      side: 'left',
      sideOffset: 10,
      updatePositionStrategy: 'always',
    }"
  >
    <UButton
      icon="lucide-plug"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
    >
      <span class="sr-only">Demande d'électricité</span>
    </UButton>
  </UTooltip>
</template>
