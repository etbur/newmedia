  <script setup>
  import { ref, onMounted, onUnmounted } from "vue";
  import avatar from "../assets/avatar.png";
  
  // State to store the product list and categories
  const products = ref([]);
  const categories = ref([]);
  const dropdowns = ref({
    sell: false,
    filter: false,
    category: false,
  });
  
  // Dropdown toggle function
  const toggleDropdown = (dropdown) => {
    dropdowns.value[dropdown] = !dropdowns.value[dropdown];
  };
  
  // WebSocket connection for products
  const connectProductWebSocket = () => {
    const productWebSocket = new WebSocket(`ws://localhost:8000/ws/products/fetch/`);
    
    productWebSocket.onopen = () => {
      console.log("Product WebSocket connection opened");
      productWebSocket.send(JSON.stringify({ action: 'fetch_all_products' }));
    };
  
    productWebSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received Product Data:", data);
      
      if (data.action === 'fetch_all_products_success') {
        products.value = data.products;
      } else if (data.action === 'fetch_all_products_error') {
        console.error('Error fetching products:', data.error);
      }
    };
  
    productWebSocket.onclose = () => {
      console.log("Product WebSocket connection closed");
    };
  };
  
  // WebSocket connection for categories
  const connectCategoryWebSocket = () => {
    const categoryWebSocket = new WebSocket(`ws://localhost:8000/ws/products/categories/`);
    
    categoryWebSocket.onopen = () => {
      console.log("Category WebSocket connection opened");
      categoryWebSocket.send(JSON.stringify({ action: 'fetch_categories' }));
    };
  
    categoryWebSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received Category Data:", data);
      
      if (data.action === 'fetch_categories_success') {
        categories.value = data.categories;
      } else if (data.action === 'fetch_categories_error') {
        console.error('Error fetching categories:', data.error);
      }
    };
  
    categoryWebSocket.onclose = () => {
      console.log("Category WebSocket connection closed");
    };
  };
  
  // Send a message to update the view count
  const updateViewCount = (productId) => {
    console.log("Updating view count for product:", productId);
    const viewWebSocket = new WebSocket(`ws://localhost:8000/ws/products/${productId}/update/`);
    
    viewWebSocket.onopen = () => {
      viewWebSocket.send(JSON.stringify({ action: 'update_product_view' }));
    };
  
    viewWebSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("View Count Update Data:", data);
      
      if (data.action === 'update_product_view_success') {
        console.log('Updated view count:', data.num_views);
        // Update the local product list if necessary
      } else if (data.action === 'update_product_view_error') {
        console.error('Error updating view count:', data.error);
      }
    };
  };
  
  // Send a message to add a product
  const addProduct = () => {
    console.log("Adding a new product");
    // Logic to add a product
  };
  
  // Send a message to buy a product
  const buyProduct = () => {
    console.log("Buying a product");
    // Logic to buy a product
  };
  
  // Filter products by rating, location, or price
  const filterByRating = () => {
    console.log("Filtering by rating");
    // Logic to filter by rating
  };
  
  const filterByLocation = () => {
    console.log("Filtering by location");
    // Logic to filter by location
  };
  
  const filterByPrice = () => {
    console.log("Filtering by price");
    // Logic to filter by price
  };
  
  // Show products by category
  const showCategory = (category) => {
    console.log(`Showing products in the ${category} category`);
    // Logic to show products by category
  };
  
  // Lifecycle hooks
  onMounted(() => {
    connectProductWebSocket();
    connectCategoryWebSocket();
  });
  
  onUnmounted(() => {
    // Ensure to close WebSocket connections if open
  });
  </script>
  
  <template>
    <div class=" md:mx-[2vw]">
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
                to="/newproduct"
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
    
    <div class="grid  items-center mx-[8vw]  sm:mx-0 sm:grid-cols-2 lg:ml-0 lg:grid-cols-3 mx:ml-[10%] sm:ml-[5%]  gap-[5%]  mt-16  ">
   <div v-for="product in products" :key="product.id" class="  bg-[#F4F4F4] flex flex-col gap-3 rounded-md shadow-md p-8">
     <div class="flex flex-col gap-2">
       <div class="flex items-center gap-4">
         <img :src="avatar" alt="seller profile" class="w-6 h-6" />
         <p class="text-sm capitalize text-[#]">{{ product.seller_profile_name }}</p>
       </div>
       <p class="text-sm">{{ product.created_at }}</p>
     </div>
 
     <div class="flex flex-col gap-4">
       <h3 class="font-medium  capitalize">{{ product.name }}</h3>
       <img :src="`http://localhost:8000${product.image}`" alt="Product Image" class="w-[25vw] h-[16vw] rounded-lg" />
       <div class="flex justify-between items-center">
         <p class="text-gray-900">{{ product.price }} Br</p>
         <div class="flex gap-3 items-center justify-end">
           <p class="text-gray-600">Rating: {{ product.rating }}</p>
           <p class="text-[#00b4b4] flex gap-2">
             {{ product.views }}<span>Views</span>
           </p>
           <router-link class="text-[#00b4b4] px-4 py-2 rounded-md" @click="updateViewCount">
             Detail
           </router-link>
         </div>
       </div>
     </div>
   </div>
 </div>
 </div>
  </template>
  
  <style scoped>
  /* Add your styles here */
  </style>
  