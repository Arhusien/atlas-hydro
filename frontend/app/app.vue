<template>
  <UApp>
    <TooltipProvider>
      <UMain>
        <NuxtPage />
      </UMain>
    </TooltipProvider>
  </UApp>
</template>

<script setup>
  import {
    TooltipProvider,
  } from "reka-ui";
</script>
