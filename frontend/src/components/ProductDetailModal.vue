<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md relative">
      <button @click="close" class="absolute top-2 right-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <h2 class="text-xl font-semibold mb-4 text-[#008a8a]">{{ product.name }}</h2>
      <img
        :src="`http://localhost:8000${product.image}`"
        alt="Product Image"
        class="w-full h-48 object-cover mb-4"
      />
      <p class="text-sm mb-2">Seller: {{ product.seller_profile_name }}</p>
      <p class="text-sm">{{ product.description }}</p>
      <div class="flex justify-between py-2">
        <p class="text-sm mb-4">Price: {{ product.price }} Br</p>
        <p class="text-sm mb-4">Rating: {{ product.rating }}</p>
        <p class="text-sm mb-4">Views: {{ product.views }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  product: Object
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<style scoped>
/* Add your styles here */
</style>
