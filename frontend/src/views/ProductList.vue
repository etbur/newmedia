<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import avatar from '../assets/avatar.png';
import ProductDetailModal from '../components/ProductDetailModal.vue'

const products = ref([]);
const categories = ref([]);
const dropdowns = ref({
  sell: false,
  filter: false,
  category: false,
});

const selectedCategory = ref(null);
const selectedProduct = ref(null); 
const showModal = ref(false);
const router = useRouter();

const toggleDropdown = (dropdown) => {
  dropdowns.value[dropdown] = !dropdowns.value[dropdown];
};

let productWebSocket = null;
let categoryWebSocket = null;

const connectProductWebSocket = () => {
  productWebSocket = new WebSocket('ws://localhost:8000/ws/products/fetch/');

  productWebSocket.onopen = () => {
    console.log('Product WebSocket connection opened');
    if (selectedCategory.value) {
      productWebSocket.send(JSON.stringify({ action: 'filter_by_category', category: selectedCategory.value }));
    } else {
      productWebSocket.send(JSON.stringify({ action: 'fetch_all_products' }));
    }
  };

  productWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received Product Data:', data);

    if (data.action === 'fetch_all_products_success') {
      products.value = data.products;
    } else if (data.action === 'filter_by_category_success') {
      products.value = data.products;
    } else if (data.action === 'fetch_all_products_error' || data.action === 'filter_by_category_error') {
      console.error('Error fetching products:', data.error);
    }
  };

  productWebSocket.onclose = () => {
    console.log('Product WebSocket connection closed');
  };
};

const connectCategoryWebSocket = () => {
  categoryWebSocket = new WebSocket('ws://localhost:8000/ws/products/categories/');

  categoryWebSocket.onopen = () => {
    console.log('Category WebSocket connection opened');
    categoryWebSocket.send(JSON.stringify({ action: 'fetch_categories' }));
  };

  categoryWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received Category Data:', data);

    if (data.action === 'fetch_categories_success') {
      categories.value = data.categories;
    } else if (data.action === 'fetch_categories_error') {
      console.error('Error fetching categories:', data.error);
    }
  };

  categoryWebSocket.onclose = () => {
    console.log('Category WebSocket connection closed');
  };
};

const showCategory = (category) => {
  console.log(`Showing products in the ${category} category`);
  selectedCategory.value = category;
  if (productWebSocket) {
    productWebSocket.send(JSON.stringify({
      action: 'filter_by_category',
      category: category
    }));
  }
};

const updateViewCount = (productId) => {
  const updateViewWebSocket = new WebSocket(`ws://localhost:8000/ws/products/update/${productId}/`);
  updateViewWebSocket.onopen = () => {
    updateViewWebSocket.send(JSON.stringify({ action: 'update_product_view' }));
  };

  updateViewWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.action === 'update_product_view_success') {
      console.log('Product view updated successfully:', data.num_views);
    } else if (data.action === 'update_product_view_error') {
      console.error('Error updating product view:', data.error);
    }
  };

  updateViewWebSocket.onclose = () => {
    console.log('Update View WebSocket connection closed');
  };
};


const openModal = (product) => {
  selectedProduct.value = product;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

onMounted(() => {
  connectProductWebSocket();
  connectCategoryWebSocket();
});

onUnmounted(() => {
  if (productWebSocket) {
    productWebSocket.close();
  }
  if (categoryWebSocket) {
    categoryWebSocket.close();
  }
});

const addProduct = () => {
  router.push('/app/newproduct');
};

const buyProduct = () => {
  // Implement the logic for buying a product here
};

const filterByRating = () => {
  // Implement the logic for filtering by rating
};

const filterByLocation = () => {
  // Implement the logic for filtering by location
};

const filterByPrice = () => {
  // Implement the logic for filtering by price
};
</script>

<template>
  <div class="md:mx-[2vw]">
    <div class="flex flex-wrap ml-[8vw] md:mx-0 md:justify-end gap-6 mb-3 ">
      <!-- Dropdowns for actions -->
      <div class="relative inline-block text-left">
        <div>
          <button
            @click="toggleDropdown('sell')"
            class="inline-flex justify-center w-full rounded-md border border-[#D9D9D9] text-[#008A8A] font-medium shadow-sm px-4 py-1 bg-white text-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-[#D9D9D9]"
            type="button"
          >
            Sell
            <svg
              class="-mr-1 ml-2 h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <div
          v-show="dropdowns.sell"
          class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
          role="menu"
          aria-orientation="vertical"
          aria-labelledby="menu-button"
        >
          <div class="py-1" role="none">
            <router-link
              to="/app/newproduct"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="addProduct"
            >
              Add New Product
            </router-link>
            <router-link
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="buyProduct"
            >
              Buy Product
            </router-link>
          </div>
        </div>
      </div>

      <!-- Filter Dropdown -->
      <div class="relative inline-block text-left">
        <div>
          <button
            @click="toggleDropdown('filter')"
            class="inline-flex justify-center w-full rounded-md border border-[#D9D9D9] text-[#008A8A] font-medium shadow-sm px-4 py-1 bg-white text-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-[#008A8A]"
            type="button"
          >
            Filter
            <svg
              class="-mr-1 ml-2 h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <div
          v-show="dropdowns.filter"
          class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
          role="menu"
          aria-orientation="vertical"
          aria-labelledby="menu-button"
        >
          <div class="py-1" role="none">
            <a
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="filterByRating"
            >
              Filter by Rating
            </a>
            <a
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="filterByLocation"
            >
              Filter by Location
            </a>
            <a
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="filterByPrice"
            >
              Filter by Price
            </a>
          </div>
        </div>
      </div>

      <!-- Category Dropdown -->
      <div class="relative inline-block text-left">
        <div>
          <button
            @click="toggleDropdown('category')"
            class="inline-flex justify-center w-full rounded-md border border-[#D9D9D9] text-[#008A8A] font-medium shadow-sm px-4 py-1 bg-white text-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-[#008A8A]"
            type="button"
          >
            Categories
            <svg
              class="-mr-1 ml-2 h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <div
          v-show="dropdowns.category"
          class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
          role="menu"
          aria-orientation="vertical"
          aria-labelledby="menu-button"
        >
          <div class="py-1" role="none">
            <a
              href="#"
              v-for="category in categories"
              :key="category.id"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="showCategory(category.name)"
            >
              {{ category.name }}
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Display Product List -->
    <div v-if="products.length > 0" class="grid items-center mx-[8vw] sm:mx-0 sm:grid-cols-2 lg:ml-0 lg:grid-cols-3 mx:ml-[10%] sm:ml-[5%] gap-[5%] mt-16">
      <div v-for="product in products" :key="product.id" class="bg-[#F4F4F4] flex flex-col gap-3 rounded-md shadow-md p-8">
        <div class="flex flex-col gap-2">
          <div class="flex items-center gap-4">
            <img :src="avatar" alt="seller profile" class="w-6 h-6" />
            <p class="text-sm capitalize">{{ product.seller_profile_name }}</p>
          </div>
          <p class="text-sm">{{ product.created_at }}</p>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="font-medium capitalize">{{ product.name }}</h3>
          <img :src="`http://localhost:8000${product.image}`" alt="Product Image" class="w-[25vw] h-[16vw] rounded-lg" />
          <div class="flex justify-between items-center">
            <p class="text-gray-900">{{ product.price }} Br</p>
            <div class="flex gap-3 items-center justify-end">
              <p class="text-gray-600">Rating: {{ product.rating }}</p>
              <router-link class="text-[#00b4b4] px-4 py-2 rounded-md flex gap-2" @click.prevent="updateViewCount(product.id)">
                {{ product.views }}<span>Views</span>
              </router-link>
              <button class="text-[#00b4b4] px-4 py-2 rounded-md" @click="openModal(product)">
                Detail
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center mt-16 text-gray-500">
      No products available.
    </div>
  
    <!-- Product Detail Modal -->
    <ProductDetailModal :isOpen="showModal" :product="selectedProduct" @close="closeModal" />
  </div>

  
</template>

