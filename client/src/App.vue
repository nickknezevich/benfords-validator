<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth.store';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();

const { isAuthenticated } = authStore;
console.log("IS_AUTHENTICATED", isAuthenticated)
if(authStore.isAuthenticated === true){
  const { user } = authStore.user;
}

const user = authStore.user

const logout = () => {
  authStore.logout();
}
</script>

<template>
  <div class="container">
    <header
      class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-5 border-bottom app-header" v-if="user">
      <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
        <img class="me-2" src="@/assets/logo.svg" alt="" width="40" height="57">
        <span class="fs-4">Benford's Validator</span>
      </a>

      <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <li><router-link to="/" class="nav-link px-2 link-secondary">Home</router-link></li>
        <li><router-link to="/examples" class="nav-link px-2 link-secondary active">Examples</router-link></li>
      </ul>
      <div class="col-md-3 text-end" v-if="user">
        <span class="me-3 current-user" v-if="user">{{ user.user.first_name }} {{ user.user.last_name }}</span>
        <button type="button" class="btn btn-outline-primary me-2" @click="logout()">Log out</button>
      </div>
    </header>
    <RouterView />
  </div>
</template>

<style scoped></style>
