<template>
  <USlideover
    v-model:open="open"
    side="right"
    inset
    dismissible
    :overlay="$device.isMobile"
    modal
    :ui="{
      overlay: 'sm:bg-transparent',
      header: 'px-5',
      content: 'ring-0 sm:ring-0',
      body: 'flex-1 overflow-hidden p-0 sm:p-0',
      footer: 'px-4 sm:px-4 min-h-16',
    }"
  >
    <template #header="{ close }">
      <div class="flex w-full items-center gap-2">
        <div class="flex w-full min-w-0 items-center gap-2">
          <h2 class="truncate text-highlighted font-medium">
            {{ title }}
          </h2>
          <UBadge
            v-if="badge"
            color="neutral"
            variant="soft"
            class="rounded"
          >
            {{ badge }}
          </UBadge>
        </div>
        <UButton
          icon="lucide:x"
          color="neutral"
          variant="ghost"
          square
          class="cursor-pointer rounded -mr-2"
          @click="close"
        >
          <span class="sr-only">Fermer</span>
        </UButton>
      </div>
    </template>
    <template #body>
      <div
        v-if="isLoading"
        class="flex items-center justify-center h-full"
      >
        <UIcon
          name="lucide:loader-circle"
          class="animate-spin size-6"
        />
      </div>
      <slot
        v-else
      />
    </template>
    <template
      v-if="$slots.footer"
      #footer
    >
      <slot
        name="footer"
      />
    </template>
  </USlideover>
</template>

<script setup>
  const props = defineProps({
    modelValue: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    badge: {
      type: String,
      required: false,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
  });

  const emit = defineEmits([
    "update:modelValue",
  ]);

  const open = ref(props.modelValue);
  watch(() => props.modelValue, (newValue) => {
    open.value = newValue;
  });

  watch(open, (newValue) => {
    emit("update:modelValue", newValue);
  });
</script>
