<script setup lang="ts">
import { Form, Field, useField, useForm } from "vee-validate";
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "../stores/auth.store";

const { handleSubmit, handleReset } = useForm({
  validationSchema: {
    username(value: string) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true;
      return "Must be a valid e-mail.";
    },
    password(value: string) {
      if (value) return true;
      return "Name needs to be at least 2 characters.";
    }
  },
});

const username = useField("username");
const password = useField("password");
const validationError = ref();
const authStore = useAuthStore();
const { isLoading } = storeToRefs(authStore);

const submit = handleSubmit(
  (values: { username: string; password: string }) => {
    try {
      authStore.login(values.username, values.password);
    } catch (error: any) {
      validationError.value = error.response.data.errors.message;
    }
  }
);
</script>

<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <!-- <v-sheet class="mx-auto login-form" max-width="344"> -->
      <div class="text-center mt-4">
        <img
          src="@/assets/img/logo-larger-white.png"
          height="32"
          class="mb-3"
        />
        <p class="lead">Sign in to your account to continue</p>
        <v-sheet class="mt-5 pt-5 pl-5 pb-5 pr-5" :width="330" rounded>
          <form @submit.prevent="submit">
            <v-text-field
              v-model="username.value.value"
              variant="outlined"
              :error-messages="username.errorMessage.value"
              label="Email"
              class="mb-2"
            ></v-text-field>
            <v-text-field
              v-model="password.value.value"
              :error-messages="password.errorMessage.value"
              label="Password"
              variant="outlined"
              class="mb-2"
              type="password"
            ></v-text-field>
            <v-btn
              :disabled="isLoading"
              :loading="isLoading"
              block
              class="text-none mb-1"
              color="light-green-darken-1"
              size="x-large"
              variant="flat"
              @click="submit"
            >
              Sign In
            </v-btn>
          </form>
        </v-sheet>
      </div>
    </v-row>
  </v-container>
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
