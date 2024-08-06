<script setup>
import { Icon } from "@iconify/vue";
import { ref } from "vue";

const showSidebar = ref(false);
</script>

<template>
  <header class="sm:flex flex-col fixed top-0 w-full z-10 mb-10 sm:mb-0">
    <div class="flex flex-col py-2 sm:py-4 bg-[#008A8A]">
      <div
        class="flex justify-between px-[6vw] md:py-0 items-center bg-[#008A8A]"
      >
        <img
          src="../assets/logo.jpg"
          class="w-[6vw] h-[6vw] sm:w-[3vw] sm:h-[3vw]"
          alt="Logo"
        />
        <p
          class="text-white text-sm sm:text-lg md:text-xl  hidden sm:block"
        >
          Connect, Share and Engage with friends
        </p>
        <div class="flex items-center gap-3">
          <div>
            <button
              class="bg-[#F4F4F4] border-2 border-[#4267B2] border-opacity-10 text-blue-800 px-4 rounded-lg md:hidden hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent hover:text-white"
            >
              Logout
              <Icon icon="mdi:logout" class="inline-block ml-2 rotate-180" />
            </button>
          </div>

          <Icon
            class="w-[5vw] h-[5vw] sm:w-[3vw] sm:h-[3vw]"
            icon="mdi:account"
          />
        </div>
      </div>
      <p class="text-white text-lg text-center sm:hidden">
        Connect, Share and Engage with friends
      </p>
    </div>

    <!-- Main Navigation -->
    <nav
      class="flex flex-col gap-5 sm:flex-row sm:gap-10  bg-[#F1F1F1] justify-between items-center px-[7vw] shadow-md"
    >
      <div class="flex gap-6 sm:gap-11">
        <RouterLink to="/app/friends" >
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:account-plus"
          />
        </RouterLink>
        <RouterLink to="/app/group">
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:account-group"
          />
        </RouterLink>
        <RouterLink to="app/message">
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:chat"
          />
        </RouterLink>
        <RouterLink to="/app/notfication">
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:bell"
          />
        </RouterLink>
        <RouterLink to="/app/marketplace">
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:chart-line"
          />
        </RouterLink>
        <RouterLink to="/app/videochat">
          <Icon
            class="w-4 h-4 sm:w-6 sm:h-6 transition-transform duration-300 ease-in-out transform hover:scale-125 hover:rotate-12 hover:text-[#C/59728] router-link-active:scale-125 router-link-active:rotate-12 router-link-active:text-[#008a8a]"
            icon="mdi:video"
          />
        </RouterLink>
        <button @click="showSidebar = !showSidebar" class="md:hidden">
          <Icon class="w-[4vw] h-[4vh]sm:w-[2vw] sm:h-[2vw]" icon="mdi:menu" />
        </button>
      </div>

      <div class="relative">
        <input
          type="text"
          class="px-4 py-3 w-[80vw] sm:w-[30vw] lg:w-[30vw] rounded-xl border-2 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          placeholder="Search"
        />
        <button class="absolute inset-y-0 right-0 px-4 text-teal-600">
          <svg
            class="h-5 w-5"
            fill="none"
            stroke="black"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            ></path>
          </svg>
        </button>
      </div>
    </nav>

    <!-- Sidebar -->
    <div
      v-if="showSidebar"
      class="fixed top-0 left-0 w-full h-full bg-gray-800 bg-opacity-50 z-10 md:hidden "
    >
      <div
        class="bg-white w-full mt-[9vh] p-6 overflow-y-auto transition-transform duration-300 ease-in-out"
        :class="{ '-translate-x-full': !showSidebar }"
      >
        <button @click="showSidebar = false" class="absolute top-20 right-4">
          <Icon class="w-6 h-6" icon="mdi:close" />
        </button>
        <div class="flex  items-center gap-6 space-y-4">
          <router-link
            @click="showSidebar = false"
            to="/app/newpost"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1 mt-4"
            exact-active-class="bg-[#E2E2E2] text-[#C59728] py-1"
          >
            <Icon icon="mdi:post-outline" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">New Post</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/design"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:design" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Design</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/game"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:gamepad-variant" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Game</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/voicetotext"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:voice" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]"
              >Voice to Text</span
            >
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/market"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:chart-line" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Marketing</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/job"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2]text-[#C59728]"
          >
            <Icon icon="mdi:briefcase" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Job</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/ad"
            active-class="bg-[#E2E2E2]text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2]text-[#C59728]"
          >
            <Icon icon="mdi:announcement" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Ad</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/signlanguage"
            active-class="bg-[#E2E2E2]text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2]text-[#C59728]"
          >
            <Icon icon="mdi:language" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]"
              >Sign Language</span
            >
          </router-link>

          <h1 class="font-semibold text-xl">Other</h1>

          <router-link
            @click="showSidebar = false"
            to="/follower"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:account-multiple" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Follower</span>
          </router-link>

          <router-link
            @click="showSidebar = false"
            to="/student"
            active-class="bg-[#E2E2E2] text-[#C59728]"
            class="flex items-center gap-1 min-w-fit border-2 border-[#008a8a] border-opacity-10 rounded-md px-4 py-1"
            exact-active-class="py-1  bg-[#E2E2E2] text-[#C59728]"
          >
            <Icon icon="mdi:school" class="inline-block mr-2" />
            <span class="text-blue-800 hover:text-[#C59728]">Student</span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>
<style scoped>
</style>

