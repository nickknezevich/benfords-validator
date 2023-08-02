<script setup>
import ValidationEntries from '../components/ValidationEntries.vue'
import { useAuthStore } from '../stores/auth.store';

const authStore = useAuthStore();

const logout = () => {
  authStore.logout();
}
</script>

<template>
  <main>
    <div class="container">
      <header
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-5 border-bottom">
        <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
          <img class="me-2" src="@/assets/logo.svg" alt="" width="40" height="57">
          <span class="fs-4">Benford's Validator</span>
        </a>

        <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
          <li><a href="/" class="nav-link px-2 link-secondary active">Home</a></li>
          <li><a href="#" class="nav-link px-2 link-dark">Add New Entry</a></li>
          <li><a href="#" class="nav-link px-2 link-dark">Users</a></li>
        </ul>

        <div class="col-md-3 text-end">
          <button type="button" class="btn btn-outline-primary me-2" @click="logout()">Log out</button>
        </div>

      </header>
      <ValidationEntries />




      
    </div>



  </main>
</template>
