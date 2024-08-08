<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <div
      class="bg-white rounded-lg shadow-lg p-6 w-[40vw] relative flex gap-[25%] px-[2%]"
    >
      <button @click="close" class="absolute top-2 right-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <div class="bg-[#f4f4f4] px-8 py-1 rounded-sm">
        <img
          :src="`http://localhost:8000${product.image}`"
          alt="Product Image"
          class="w-full h-48 object-cover mb-4"
        />
        <router-link class="text-[#008a8a] flex justify-end text-sm"
          >Review</router-link
        >
      </div>
      <div>
        <div class="flex gap-3">
          <img
            :src="product.seller_profile_picture || avatar"
            v-bind:alt="alt"
            class="w-6 h-6"
          />
          <p class="text-sm mb-2 text-[#008a8a]">
           {{ product.seller_profile_name }}
          </p>
        </div>
        <h2 class="text-xl font-semibold mb-4 capitalize">
          {{ product.name }}
        </h2>
        <p class="text-gray-800 mb-4 mt-1">
          {{
            product.description.length > 100 && !isDescriptionExpanded(product.id)
              ? product.description.substring(0, 100) + "..."
              : product.description
          }}
          <button
            v-if="product.description.length > 100"
            @click="toggleDescription(product.id)"
            class="text-[#008a8a] underline"
          >
            {{ isDescriptionExpanded(product.id) ? "Show less" : "Show more" }}
          </button>
        </p>
        <div class="flex gap-6 py-2">
          <p class="text-sm mb-4">Price: {{ product.price }} Br</p>
          <p class="text-sm mb-4">Rating: {{ product.rating }}</p>
          <p class="text-sm mb-4">Views: {{ product.views }}</p>
        </div>
        <router-link
          to="/app/buyproduct"
          class="bg-[#008a8a] px-4 py-2 rounded-md text-white text-sm"
        >
          Buy Now
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import avatar from '../assets/avatar.png';

const expandedProductId = ref(null);

const props = defineProps({
  isOpen: Boolean,
  product: Object,
});

const emit = defineEmits(["close"]);

const close = () => {
  emit("close");
};

const toggleDescription = (productId) => {
  expandedProductId.value = expandedProductId.value === productId ? null : productId;
};

const isDescriptionExpanded = (productId) => {
  return expandedProductId.value === productId;
};
</script>


