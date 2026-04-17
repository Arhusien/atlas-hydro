<template>
  <UTooltip
    :delay-duration="0"
    text="Exportations d'électricité"
    :content="{
      side: 'top',
      sideOffset: 10,
    }"
  >
    <UButton
      icon="lucide:utility-pole"
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
