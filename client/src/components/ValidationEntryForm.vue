<script setup lang="ts">
import { Form, useField, useForm } from "vee-validate";
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useValidationsStore } from "@/stores/validations.store";
const validationsStore = useValidationsStore();
const emit = defineEmits<{
  (e: "close-dialog", value: boolean): void;
}>();

const { handleSubmit } = useForm({
  validationSchema: {
    title(value: string) {
      if (value) return true;
      return "Title is required.";
    },
    reference_column(value: string) {
      if (value) return true;
      return "Reference column is required.";
    },
    file(value: any) {
      if (value) return true;
      return "Required!";
    },
  },
});

const title = useField("title");
const reference_column = useField("reference_column");
const separator = useField("separator");
const file = useField("file");
const validationError = ref();
const { isSubmiting, isSubmited, errors } = storeToRefs(validationsStore);
const snackbar = ref(false);

const submit = handleSubmit((values: any) => {
  const { title, reference_column, file, separator } = values;
  validationsStore.add(title, file, reference_column, separator);
  emit("close-dialog", false);
  if (isSubmited.value === true) {
    emit("close-dialog", false);
    snackbar.value = true;
  }
});
</script>

<template>
  <form @submit.prevent="submit">
    <v-text-field
      v-model="title.value.value"
      variant="outlined"
      :error-messages="title.errorMessage.value"
      label="Title"
      class="mb-2"
    ></v-text-field>
    <v-text-field
      v-model="reference_column.value.value"
      :error-messages="reference_column.errorMessage.value"
      label="Reference Column"
      variant="outlined"
      class="mb-2"
    ></v-text-field>
    <v-text-field
      v-model="separator.value.value"
      :error-messages="separator.errorMessage.value"
      label="Separator"
      variant="outlined"
      class="mb-2"
    ></v-text-field>
    <v-file-input
      placeholder="Click here to select your file"
      v-model="file.value"
      :error-messages="file.errorMessage.value"
      accept=".xlsx, .txt, .csv"
      variant="outlined"
      class="mb-2"
      label="File input"
    >
    </v-file-input>
    <v-btn
      :disabled="isSubmiting"
      :loading="isSubmiting"
      block
      class="text-none mb-1"
      color="light-green-darken-1"
      size="x-large"
      variant="flat"
      @click="submit"
    >
      Save
    </v-btn>
  </form>

  <v-snackbar
    v-model="snackbar"
    :timeout="2000"
    color="success"
    variant="outlined"
  >
    Validation has been successfuly Added!
  </v-snackbar>
</template>

<style>
.form-signin {
  max-width: 330px;
  padding: 15px;
}

.w-100 {
  width: 100% !important;
}

.v-card {
  overflow-y: none !important;
}
</style>
