<template>
  <UTooltip
    :delay-duration="0"
    text="Exportations d'électricité"
    :content="{
      side: 'left',
      sideOffset: 10,
      updatePositionStrategy: 'always',
    }"
  >
    <UButton
      icon="lucide-truck-electric"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
    >
      <span class="sr-only">Exportations d'électricité</span>
    </UButton>
  </UTooltip>
</template>
