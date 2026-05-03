<template>
  <UModal
    title="Informations"
    close-icon="lucide:x"
  >
    <UTooltip
      :delay-duration="0"
      text="Informations"
      :content="{
        side: 'left',
        sideOffset: 10,
      }"
    >
      <UButton
        icon="lucide:info"
        color="neutral"
        variant="solid"
        size="lg"
        square
        class="cursor-pointer"
      >
        <span class="sr-only">Informations</span>
      </UButton>
    </UTooltip>
    <template #body>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    </template>
  </UModal>
</template>
