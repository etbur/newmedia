<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavbarView from "./components/NavbarView.vue";
import Sidebar from "./components/Sidebar.vue";
</script>

<template>
  <div>
    <header>
      <div class="wrapper">
        <NavbarView />
      </div>
    </header>
    <main class=" mt-[22vh] hidden md:block">
      <Sidebar class="md:fixed left-[7vw]" />
    </main>
    <div class="mt-[30vh] sm:mt-[25vh] md:ml-[20vw] lg:ml-[19vw] md:mr-[4vw]">
      <RouterView />
    </div>
  </div>
</template>
