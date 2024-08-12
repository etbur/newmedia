<script setup>
import { Icon } from "@iconify/vue";
import { ref } from "vue";

const showSidebar = ref(false);
</script>

<template>
  <header class="sm:flex flex-col fixed top-0 w-full z-20 mb-10 sm:mb-0">
    <!-- Header Section -->
    <div class="flex flex-col py-2 sm:py-6 lg:py-0 bg-[#008A8A] shadow-md px-[3vw]">
      <div class="flex justify-between px-4 md:py-2 items-center">
        <img
          src="../assets/logo.jpg"
          class="w-12 h-12 sm:w-8 sm:h-8"
          alt="Logo"
        />
        <p class="text-white text-sm sm:text-lg md:text-xl hidden sm:block">
          Connect, Share and Engage with friends
        </p>
        <div class="flex items-center gap-3">
          <button
            class="bg-[#F4F4F4] border-2 border-[#4267B2] border-opacity-10 text-blue-800 px-4 py-2 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-500 hover:text-[#ffffff] block sm:hidden"
          >
            Logout
            <Icon icon="mdi:logout" class="inline-block ml-2 rotate-180" />
          </button>
          <Icon
            class="w-8 h-8 sm:w-6 sm:h-6"
            icon="mdi:account"
          />
        </div>
      </div>
      <p class="text-white text-lg text-center sm:hidden">
        Connect, Share and Engage with friends
      </p>
    </div>

    <!-- Main Navigation -->
    <nav class="flex flex-col gap-4 sm:flex-row sm:gap-8 bg-[#F1F1F1] justify-between items-center  py-2 shadow-md px-[4vw]">
      <div class="flex gap-4 sm:gap-8">
        <RouterLink to="/app/friends">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:account-plus"
          />
        </RouterLink>
        <RouterLink to="/app/group">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:account-group"
          />
        </RouterLink>
        <RouterLink to="/app/chat">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:chat"
          />
        </RouterLink>
        <RouterLink to="/app/notfication">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:bell"
          />
        </RouterLink>
        <RouterLink to="/app/marketplace">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:chart-line"
          />
        </RouterLink>
        <RouterLink to="/app/videochat">
          <Icon
            class="w-6 h-6 transition-transform duration-300 transform hover:scale-110 hover:text-[#C59728] router-link-active:text-[#008a8a]"
            icon="mdi:video"
          />
        </RouterLink>
        <button @click="showSidebar = !showSidebar" class="md:hidden">
          <Icon class="w-8 h-8" icon="mdi:menu" />
        </button>
      </div>

      <div class="relative w-full sm:w-auto">
        <input
          type="text"
          class="px-4 py-3 w-full sm:w-64 rounded-xl border-2 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
          placeholder="Search"
        />
        <button class="absolute inset-y-0 right-0 px-4 text-teal-600">
          <svg class="h-5 w-5" fill="none" stroke="black" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </button>
      </div>
    </nav>

    <!-- Sidebar -->
    <div
      v-if="showSidebar"
      class="fixed top-0 left-0 w-full h-full bg-gray-800 bg-opacity-50 z-10 md:hidden"
    >
      <div
        class="bg-white w-full mt-[9vh] p-6 overflow-y-auto transition-transform duration-300 ease-in-out transform translate-x-0"
        :class="{ '-translate-x-full': !showSidebar }"
      >
        <button @click="showSidebar = false" class="absolute top-4 right-4">
          <Icon class="w-8 h-8" icon="mdi:close" />
        </button>
        <div class="flex flex-col items-start gap-4">
          <router-link
            @click="showSidebar = false"
            to="/app/newpost"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:post-outline" class="w-6 h-6" />
            <span class="text-blue-800">New Post</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/design"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:design" class="w-6 h-6" />
            <span class="text-blue-800">Design</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/game"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:gamepad-variant" class="w-6 h-6" />
            <span class="text-blue-800">Game</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/voicetotext"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:voice" class="w-6 h-6" />
            <span class="text-blue-800">Voice to Text</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/market"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:chart-line" class="w-6 h-6" />
            <span class="text-blue-800">Marketing</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/job"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:briefcase" class="w-6 h-6" />
            <span class="text-blue-800">Job</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/ad"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2] transition-colors"
          >
            <Icon icon="mdi:announcement" class="w-6 h-6" />
            <span class="text-blue-800">Ad</span>
          </router-link>
          <router-link
            @click="showSidebar = false"
            to="/signlanguage"
            class="flex items-center gap-2 p-3 rounded-md hover:bg-[#E2E2E2]  transition-colors"
          >
            <Icon icon="mdi:language" class="w-6 h-6" />
            <span class="text-blue-800">Sign Language</span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>

</style>
