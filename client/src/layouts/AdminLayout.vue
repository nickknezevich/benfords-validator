<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "../stores/auth.store";
const authStore = useAuthStore();
const user = JSON.parse(localStorage.getItem("user") as string);
const logout = () => {
  authStore.logout();
};
</script>

<template>
  <v-app id="app-scraper">
    <v-navigation-drawer
      model-value
      class="pt-4"
      color="grey-darken-3"
      rail
      permanent
    >
      <img
        src="@/assets/img/logo.png"
        height="32"
        class="d-block text-center mx-auto mb-9"
      />
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            v-bind="props"
            class="d-block text-center mx-auto mb-9"
            variant="text"
          >
            <v-avatar class="" size="32" :image="user.user.picture"></v-avatar>
          </v-btn>
        </template>
        <v-list density="compact">
          <v-list-item value="1">
            <template v-slot:prepend>
              <v-icon icon="mdi-cogs" style="margin-right: -15px"></v-icon>
            </template>
            <v-list-item-title text="Settings">Settings</v-list-item-title>
          </v-list-item>
          <v-list-item value="2" @click="logout">
            <template v-slot:prepend>
              <v-icon
                icon="mdi-logout-variant"
                style="margin-right: -15px"
              ></v-icon>
            </template>
            <v-list-item-title text="Sign Out">Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <router-link to="/" class="navbar-link">
        <v-btn
          size="small"
          class="d-block text-center mx-auto"
          density="comfortable"
          icon="mdi-home"
          variant="text"
        ></v-btn>
      </router-link>
    </v-navigation-drawer>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<style>
.navbar-link {
  text-decoration: none !important;
  color: #fff;
}
</style>
