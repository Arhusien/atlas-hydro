<template>
  <div class="flex flex-col gap-0.5">
    <span
      v-if="label"
      class="text-sm text-muted"
    >
      <span>{{ label }}</span>
    </span>
    <div class="inline leading-none">
      <span
        class="text-default"
        :class="{
          'text-lg sm:text-xl font-medium': size === 'md',
          'text-xl sm:text-2xl font-semibold': size === 'lg',
          'text-2xl sm:text-3xl font-semibold': size === 'xl',
        }"
      >
        {{ value }}
      </span>
      <span
        v-if="unit"
        class=" text-muted"
        :class="{
          'font-normal text-xs sm:text-sm': size === 'md',
          'font-medium text-xs sm:text-sm': size === 'lg',
          'font-medium text-sm sm:text-base': size === 'xl',
        }"
      >
        <span>&nbsp;{{ unit }}</span>
      </span>
    </div>
  </div>
</template>

<script setup>
  defineProps({
    label: {
      type: String,
      default: "",
    },
    value: {
      type: [Number, String],
      required: true,
    },
    unit: {
      type: String,
      default: "",
    },
    size: {
      type: String,
      default: "md",
    },
  });
</script>
