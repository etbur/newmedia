<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import avatar from "../assets/avatar.png";

const products = ref([]);
let productWebSocket = null;

const connectProductWebSocket = () => {
  productWebSocket = new WebSocket("ws://localhost:8000/ws/products/fetch/");

  productWebSocket.onopen = () => {
    console.log("Buying product WebSocket connection opened");
    if (products.value) {
      productWebSocket.send(JSON.stringify({ action: "fetch_all_products" }));
    }
  };
  productWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received Product Data:", data);
    if (data.action === "fetch_all_products_success") {
      products.value = data.products;
    } else if (data.action === "fetch_all_products_error") {
      console.error("Error fetching products:", data.error);
    }
  };

  productWebSocket.onclose = () => {
    console.log("Buying product WebSocket connection closed");
  };
};
onMounted(() => {
  connectProductWebSocket();
});

onUnmounted(() => {
  if (productWebSocket) {
    productWebSocket.close();
  }
});
</script>

<template>
  <h1 class="text-[#008a8a] font-medium mb-8">Buy product</h1>
  <!-- Display Product List -->
  <div v-if="products.length > 0" class="flex flex-col gap-10">
    <div v-for="product in products" :key="product.id" class="border  p-6 rounded-md">
      <div class="flex gap-[20%]">
        <div class="bg-[#f4f4f4] p-8">
           <img
          :src="`http://localhost:8000${product.image}`"
          alt="Product Image"
          class="w-[12vw] h-[12vw] inset-0 rounded-lg text-center"
        />
        </div>
       
        <div class="flex flex-col  ">
          <h3 class="font-medium capitalize">{{ product.name }}</h3>
          <p class="text-gray-900">{{ product.description }}</p>
          <div class="flex gap-3 items-center justify-between">
            <p class="text-gray-900">{{ product.price }} Br</p>
            <router-link class="text-white bg-[#008a8a] px-4 py-1 rounded-md">
              Buy Now
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>