<template>
  <USlideover
    v-model:open="open"
    side="right"
    inset
    :overlay="false"
    close-icon="lucide-x"
    title="Slideover with inset"
  >
    <template #body>
      {{ data }}
    </template>
  </USlideover>
</template>

<script setup>
  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    data: {
      type: Object,
      required: true,
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
