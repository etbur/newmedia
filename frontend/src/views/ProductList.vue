<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import avatar from "../assets/avatar.png";
import ProductDetailModal from "../components/ProductDetailModal.vue";
import StarRating from "../components/StarRating.vue";

const products = ref([]);
const minRating = ref(null);
const maxRating = ref(null);
const minPrice = ref(null);
const maxPrice = ref(null);
const location = ref("");
const categories = ref([]);
const displayedProductsCount = ref(6);
const initialProductsCount = 6;
const alt = ref("seller profile");
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
  productWebSocket = new WebSocket("ws://localhost:8000/ws/products/fetch/");

  productWebSocket.onopen = () => {
    console.log("Product WebSocket connection opened");
    if (selectedCategory.value) {
      productWebSocket.send(
        JSON.stringify({
          action: "filter_by_category",
          category: selectedCategory.value,
        })
      );
    } else {
      productWebSocket.send(JSON.stringify({ action: "fetch_all_products" }));
    }
  };

  productWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received Product Data:", data);

    if (data.action === "fetch_all_products_success") {
      products.value = data.products;
    } else if (data.action === "filter_by_category_success") {
      products.value = data.products;
    } else if (
      data.action === "fetch_all_products_error" ||
      data.action === "filter_by_category_error"
    ) {
      console.error("Error fetching products:", data.error);
    }
  };

  productWebSocket.onclose = () => {
    console.log("Product WebSocket connection closed");
  };
};

const applyFilters = () => {
  if (productWebSocket) {
    productWebSocket.send(
      JSON.stringify({
        action: "filter_products",
        category: selectedCategory.value,
        min_rating: minRating.value,
        max_rating: maxRating.value,
        min_price: minPrice.value,
        max_price: maxPrice.value,
        location: location.value,
      })
    );
  }
};

const connectCategoryWebSocket = () => {
  categoryWebSocket = new WebSocket(
    "ws://localhost:8000/ws/products/categories/"
  );

  categoryWebSocket.onopen = () => {
    console.log("Category WebSocket connection opened");
    categoryWebSocket.send(JSON.stringify({ action: "fetch_categories" }));
  };

  categoryWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received Category Data:", data);

    if (data.action === "fetch_categories_success") {
      categories.value = data.categories;
    } else if (data.action === "fetch_categories_error") {
      console.error("Error fetching categories:", data.error);
    }
  };

  categoryWebSocket.onclose = () => {
    console.log("Category WebSocket connection closed");
  };
};

const showCategory = (category) => {
  console.log(`Showing products in the ${category} category`);
  selectedCategory.value = category;
  if (productWebSocket) {
    productWebSocket.send(
      JSON.stringify({
        action: "filter_by_category",
        category: category,
      })
    );
  }
};

const updateViewCount = (productId) => {
  const updateViewWebSocket = new WebSocket(
    `ws://localhost:8000/ws/products/update/${productId}/`
  );
  updateViewWebSocket.onopen = () => {
    updateViewWebSocket.send(JSON.stringify({ action: "update_product_view" }));
  };

  updateViewWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.action === "update_product_view_success") {
      console.log("Product view updated successfully:", data.num_views);
    } else if (data.action === "update_product_view_error") {
      console.error("Error updating product view:", data.error);
    }
  };

  updateViewWebSocket.onclose = () => {
    console.log("Update View WebSocket connection closed");
  };
};

const updateProductRating = (productId, rating) => {
  const updateRatingWebSocket = new WebSocket(
    `ws://localhost:8000/ws/products/update/${productId}/`
  );
  updateRatingWebSocket.onopen = () => {
    updateRatingWebSocket.send(
      JSON.stringify({
        action: "update_product_rating",
        rating: rating,
      })
    );
  };

  updateRatingWebSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.action === "update_product_rating_success") {
      console.log("Product rating updated successfully:", data.rating);
      // Optionally update the product rating locally
      const product = products.value.find((p) => p.id === productId);
      if (product) {
        product.rating = data.rating;
      }
    } else if (data.action === "update_product_rating_error") {
      console.error("Error updating product rating:", data.error);
    }
  };

  updateRatingWebSocket.onclose = () => {
    console.log("Update Rating WebSocket connection closed");
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
  router.push("/app/newproduct");
};
const filterByRating = () => {
  // Example: Prompt user for min and max rating
  const minRating = prompt("Enter minimum rating:");
  const maxRating = prompt("Enter maximum rating:");

  if (minRating !== null && maxRating !== null) {
    if (productWebSocket) {
      productWebSocket.send(
        JSON.stringify({
          action: "filter_by_rating",
          min_rating: parseFloat(minRating),
          max_rating: parseFloat(maxRating),
        })
      );
    }
  }
};

const filterByLocation = () => {
  // Example: Prompt user for location
  const location = prompt("Enter location:");

  if (location) {
    if (productWebSocket) {
      productWebSocket.send(
        JSON.stringify({
          action: "filter_by_location",
          location: location,
        })
      );
    }
  }
};

const filterByPrice = () => {
  // Example: Prompt user for min and max price
  const minPrice = prompt("Enter minimum price:");
  const maxPrice = prompt("Enter maximum price:");

  if (minPrice !== null && maxPrice !== null) {
    if (productWebSocket) {
      productWebSocket.send(
        JSON.stringify({
          action: "filter_by_price",
          min_price: parseFloat(minPrice),
          max_price: parseFloat(maxPrice),
        })
      );
    }
  }
};

const loadMore = () => {
  displayedProductsCount.value = Math.min(
    displayedProductsCount.value + 6,
    products.value.length
  );
};

const showLess = () => {
  displayedProductsCount.value = Math.max(
    initialProductsCount,
    displayedProductsCount.value - 6
  );
};
</script>
<template>
  <div class="flex flex-col  ">
    <!-- Filter Sidebar -->
    <!-- Sidebar for Extra Small Screens -->
    <div class="block  mx-[10vw] sm:hidden">
      <div class="flex gap-4">
        <!-- Filter Dropdown -->
        <div class="flex flex-col">
          <button
            @click="toggleDropdown('filter')"
            class="px-4 py-1 rounded-sm font-medium text-sm text-[#008A8A] flex gap-2 items-center border"
          >
            Filter
            <svg
              class="w-4 h-4 ml-2 transform transition-transform duration-200"
              :class="{ 'rotate-180': dropdowns.filter }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </button>
          <div v-show="dropdowns.filter" class="p-4">
            <div class="py-2">
              <div class="flex flex-col gap-2 py-1">
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-700">Rating</span>
                  <input
                    type="number"
                    v-model.number="minRating"
                    placeholder="min"
                    class="w-16 py-1 px-2 border rounded-sm"
                    min="0"
                    max="5"
                    step="0.1"
                  />
                  <input
                    type="number"
                    v-model.number="maxRating"
                    placeholder="max"
                    class="w-16 border py-1 px-2 rounded-sm"
                    min="0"
                    max="5"
                    step="0.1"
                  />
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-700">Location</span>
                  <input
                    type="text"
                    v-model="location"
                    placeholder="location"
                    class="border py-1 px-2 rounded-sm"
                  />
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-700">Price</span>
                  <input
                    type="number"
                    v-model.number="minPrice"
                    placeholder="min"
                    class="w-16 py-1 px-2 border rounded-sm"
                    min="0"
                  />
                  <input
                    type="number"
                    v-model.number="maxPrice"
                    placeholder="max"
                    class="w-16 border py-1 px-2 rounded-sm"
                    min="0"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sell Dropdown -->
        <div>
          <button
            @click="toggleDropdown('sell')"
            class="px-4 py-1 border rounded-sm text-sm font-medium text-[#008A8A] flex gap-2 items-center"
          >
            Sell
            <svg
              class="w-4 h-4 ml-2 transform transition-transform duration-200"
              :class="{ 'rotate-180': dropdowns.sell }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </button>
          <div v-show="dropdowns.sell" class="p-4">
            <router-link
              to="/app/newproduct"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 rounded-sm"
              role="menuitem"
              @click.prevent="addProduct"
            >
              Add New Product
            </router-link>
            <router-link
              to="/app/buyproduct"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 rounded-sm"
              role="menuitem"
            >
              Buy Product
            </router-link>
          </div>
        </div>

        <!-- Categories Dropdown -->
        <div>
          <button
            @click="toggleDropdown('categories')"
            class="px-4 py-1 rounded-sm  border text-sm font-medium text-[#008A8A] flex gap-2 items-center"
          >
            Categories
            <svg
              class="w-4 h-4 ml-2 transform transition-transform duration-200"
              :class="{ 'rotate-180': dropdowns.categories }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </button>
          <div v-show="dropdowns.categories" class="p-4">
            <a
              v-for="category in categories"
              :key="category.id"
              class="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-gray-100 hover:text-gray-900 rounded-sm"
              role="menuitem"
              @click.prevent="showCategory(category.name)"
            >
              {{ category.name }}
            </a>
          </div>
        </div>
      </div>
    </div>
 <div class="hidden sm:block">
  <div
      class="px-4 h-[500px] pb-20 flex  flex-col gap-6 overflow-y-scroll fixed left-[3vw] bg-white z-10 w-full sm:w-64 lg:w-80"
    >
      <!-- Filter -->
      <div class=" py-2">
        <h1 class="text-[#008A8A] font-semibold ">Filter</h1>
        <div class="py-2" role="none">
          <div class="flex flex-col gap-2 py-1">
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-700">Rating</span>
              <input
                type="number"
                v-model.number="minRating"
                placeholder="min"
                class="w-16 py-1 px-2 border rounded-sm"
                min="0"
                max="5"
                step="0.1"
              />
              <input
                type="number"
                v-model.number="maxRating"
                placeholder="max"
                class="w-16 border py-1 px-2 rounded-sm"
                min="0"
                max="5"
                step="0.1"
              />
            </div>
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-700">Location</span>
              <input
                type="text"
                v-model="location"
                placeholder="location"
                class="border py-1 px-2 rounded-sm"
              />
            </div>
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-700">Price</span>
              <input
                type="number"
                v-model.number="minPrice"
                placeholder="min"
                class="w-16 py-1 px-2 border rounded-sm"
                min="0"
              />
              <input
                type="number"
                v-model.number="maxPrice"
                placeholder="max"
                class="w-16 border py-1 px-2 rounded-sm"
                min="0"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Sell Action -->
      <div class="border-t py-2">
        <h1 class="text-[#008a8a] font-semibold ">Sell</h1>
        <div class="py-2" role="none">
          <router-link
            to="/app/newproduct"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 rounded-sm"
            role="menuitem"
            @click.prevent="addProduct"
          >
            Add New Product
          </router-link>
          <router-link
            to="/app/buyproduct"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 rounded-sm"
            role="menuitem"
          >
            Buy Product
          </router-link>
        </div>
      </div>

      <!-- Categories -->
      <div class="border-t py-2">
        <h1 class="text-[#008a8a] font-semibold ">Categories</h1>
        <div class="py-2" role="none">
          <a
            v-for="category in categories"
            :key="category.id"
            class="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-gray-100 hover:text-gray-900 rounded-sm"
            role="menuitem"
            @click.prevent="showCategory(category.name)"
          >
            {{ category.name }}
          </a>
        </div>
      </div>
    </div>

 </div>

    <!-- Product  -->
    <div class="flex-1 ml-0 sm:ml-64 lg:ml-80 p-4">
      <div
        v-if="products.length > 0"
        class="grid gap-8 md:grid-cols-2 lg:grid-cols-3 ml-[10vw] mr-[3vw]"
      >
        <div
          v-for="(product, index) in products.slice(0, displayedProductsCount)"
          :key="product.id"
          class="bg-white flex flex-col gap-4 rounded-lg shadow-lg p-4 transition-transform transform hover:scale-105"
        >
          <!-- Seller Info -->
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-2 sm:gap-4">
              <img
                :src="product.seller_profile_picture || avatar"
                v-bind:alt="alt"
                class="w-8 h-8 rounded-full"
              />
              <p class="text-sm sm:text-base">
                {{ product.seller_profile_name }}
              </p>
            </div>
            <p class="text-gray-600 text-sm">
              {{ product.created_at }}
            </p>
          </div>
          <h3 class="text-base sm:text-lg font-medium capitalize">
            {{ product.name }}
          </h3>
          <!-- Product Image -->
          <div class="flex">
            <img
              :src="`http://localhost:8000${product.image}`"
              alt="Product Image"
              class="w-full h-48 sm:h-60 object-cover rounded-lg"
            />
          </div>

          <!-- Product Details -->
          <div class="flex flex-col gap-3">
            <p class="text-gray-900 text-base">{{ product.price }} Br</p>
            <div class="flex flex-wrap items-start justify-between gap-3">
              <StarRating
                :rating="product.rating"
                @rating-changed="updateProductRating(product.id, $event)"
              />
              <router-link
                class="text-teal-500 hover:underline px-2 py-1 rounded-md flex gap-2"
                @click.prevent="updateViewCount(product.id)"
              >
                {{ product.views }} <span>Views</span>
              </router-link>
              <button
                class="text-teal-500 hover:underline px-2 py-1 rounded-md"
                @click="openModal(product)"
              >
                Detail
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Products Available -->
      <div
        v-else
        class="flex justify-center items-center text-xl font-medium mt-8 text-[#008a8a]"
      >
        No products available!
      </div>

      <!-- Load More / Show Less Buttons -->
      <div class="flex justify-end mt-8 pb-4 mr-[4vw]">
        <button
          v-if="displayedProductsCount < products.length"
          @click="loadMore"
          class="px-4 py-2 bg-[#008a8a] text-white rounded-lg hover:bg-[#C59728]"
        >
          Load More...
        </button>
        <button
          v-if="displayedProductsCount > initialProductsCount"
          @click="showLess"
          class="px-4 py-2 bg-[#008a8a] text-white rounded-lg hover:bg-[#C59728] ml-2"
        >
          Show Less
        </button>
      </div>
    </div>
  </div>

  <!-- Product Detail Modal -->
  <ProductDetailModal
    :isOpen="showModal"
    :product="selectedProduct"
    @close="closeModal"
  />
</template>


