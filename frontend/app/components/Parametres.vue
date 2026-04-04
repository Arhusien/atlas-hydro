<template>
  <UTooltip
    :delay-duration="0"
    text="Paramètres"
    :content="{
      side: 'left',
      sideOffset: 10,
      updatePositionStrategy: 'always',
    }"
  >
    <UButton
      icon="lucide-settings"
      color="neutral"
      variant="solid"
      size="lg"
      square
      class="cursor-pointer"
    >
      <span class="sr-only">Paramètres</span>
    </UButton>
  </UTooltip>
</template>
