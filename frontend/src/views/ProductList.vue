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
  <div class="md:mx-[2vw]">
    <div class="flex flex-wrap ml-[8vw] md:mx-0 md:justify-end gap-6 mb-3">
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
              to="/app/buyproduct"
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
              @click.prevent="applyFilters"
            >
              Rating
              <input
                type="number"
                v-model.number="minRating"
                placeholder="min"
                class="w-16 py-1 px-2 ml-2 border"
                min="0"
                max="5"
                step="0.1"
              />
              <input
                type="number"
                v-model.number="maxRating"
                placeholder="max"
                class="w-16 border py-1 px-2"
                min="0"
                max="5"
                step="0.1"
              />
            </a>
            <a
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="applyFilters"
            >
              Location
              <input
                type="text"
                v-model="location"
                placeholder="location"
                class="border py-1 px-2 ml-2"
              />
            </a>
            <a
              href="#"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
              @click.prevent="applyFilters"
            >
              Price
              <input
                type="number"
                v-model.number="minPrice"
                placeholder="min"
                class="w-16 py-1 px-2 ml-2 border"
                min="0"
              />
              <input
                type="number"
                v-model.number="maxPrice"
                placeholder="max"
                class="w-16 border py-1 px-2"
                min="0"
              />
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
          class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
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
    <div
      v-if="products.length > 0"
      class="grid items-center mx-[8%] sm:mx-[6%] md:mx-6 lg:mx-8 xl:mx-12  sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-16 mt-8 sm:mt-12 lg:mt-16"
    >
      <div
        v-for="(product, index) in products.slice(0, displayedProductsCount)"
        :key="product.id"
        class="bg-white flex flex-col gap-4 rounded-lg shadow-lg p-4 sm:p-6 transition-transform transform hover:scale-105  w-[80%] sm:w-full"
      >
        <!-- Seller Info -->
        <div class="flex flex-col gap-2">
          
          <div class="flex items-center gap-3 sm:gap-4">
            <img
              :src="product.seller_profile_picture || avatar"
              v-bind:alt="alt"
              class="w-6 h-6 rounded-full "
            />
            <p class="sm:text-base text-sm">
              {{ product.seller_profile_name }}
            </p>
          </div>
          <p class="text-gray-600 text-sm">
            {{ product.created_at }}
          </p>
        </div>
        <h3 class="sm:text-lg font-medium capitalize">
            {{ product.name }}
          </h3>
        <!-- Product Image -->
        <div class="flex ">
          <img
            :src="`http://localhost:8000${product.image}`"
            alt="Product Image"
            class="  w-full h-60 sm:h-48 object-cover rounded-lg transition-transform transform  "
          />
        </div>

        <!-- Product Details -->
        <div class="flex flex-col gap-3 sm:gap-4">
         
          <p class="text-[#008a8a] text-base ">
            {{ product.price }} Br
          </p>
          <div
            class="flex flex-wrap sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-4"
          >
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
    <div v-else class="text-xl font-medium mt-[2vh]  text-[#008a8a] ">
      No products available !
    </div>

    <!-- Product Detail Modal -->
    <ProductDetailModal
      :isOpen="showModal"
      :product="selectedProduct"
      @close="closeModal"
    />
  </div>

    <!-- Load More / Show Less Buttons -->
    <div class="flex justify-center mt-8 pb-4" >
      <button
        v-if="displayedProductsCount < products.length"
        @click="loadMore"
        class="px-4 py-2 bg-[#008a8a] text-white rounded-lg hover:bg-[#C59728]"
      >
        Load More
      </button>
      <button
        v-if="displayedProductsCount > initialProductsCount"
        @click="showLess"
        class="px-4 py-2 bg-[#008a8a] text-white rounded-lg hover:bg-[#C59728] ml-2"
      >
        Show Less
      </button>
    </div>
</template>

