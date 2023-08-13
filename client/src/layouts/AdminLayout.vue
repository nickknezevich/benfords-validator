
<script start>
import MainSidebar from '../components/MainSidebar.vue';
import MainNavbar from '../components/MainNavbar.vue'

export default {
  components: { MainSidebar, MainNavbar }
}

</script>
<template>
  <div class="wrapper">
    <MainSidebar />
    <div class="main">
      <MainNavbar />
      <main class="content">
        <div class="container-fluid p-0">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>