
 <script setup>
 import { ref, onMounted, onUnmounted } from "vue";
 import avatar from "../assets/avatar.png";
 
 // State to store the product list
 const products = ref([]);
 
 // State to handle dropdowns
 const dropdowns = ref({
   sell: false,
   filter: false,
   category: false,
 });
 
 // Dropdown toggle function
 const toggleDropdown = (dropdown) => {
   dropdowns.value[dropdown] = !dropdowns.value[dropdown];
 };
 
 // Connect to WebSocket
 const connectWebSocket = () => {
   const webSocket = new WebSocket(`ws://localhost:8000/ws/products/fetch/`);
 
   webSocket.onopen = () => {
     console.log("WebSocket connection opened");
     // Request to fetch all products
     webSocket.send(JSON.stringify({ action: 'fetch_all_products' }));
   };
 
   webSocket.onmessage = (event) => {
     const data = JSON.parse(event.data);
     console.log("Received:", data);
 
     if (data.action === 'fetch_all_products_success') {
       products.value = data.products;
     } else if (data.action === 'fetch_all_products_error') {
       console.error('Error fetching products:', data.error);
     }
   };
 
   webSocket.onclose = () => {
     console.log("WebSocket connection closed");
   };
 };
 
 const sendMessage = () => {
  //  send message logic
};

const updateViewCount = () => {
  console.log("Update View Count");
  //  update view count logic
};

const addProduct = () => {
  console.log("Adding a new product");
  //  logic to add a product
};

const buyProduct = () => {
  console.log("Buying a product");
  //  logic to buy a product
};

const filterByRating = () => {
  console.log("Filtering by rating");
  //  logic to filter by rating
};

const filterByLocation = () => {
  console.log("Filtering by location");
  //  logic to filter by location
};

const filterByPrice = () => {
  console.log("Filtering by price");
  //  logic to filter by price
};

const showCategory = (category) => {
  console.log(`Showing products in the ${category} category`);
  //  logic to show products by category
};
 // Lifecycle hooks
 onMounted(() => {
   connectWebSocket();
 });
 
 onUnmounted(() => {
   // Ensure to close WebSocket connection if open
 });
 </script>
 
 <template >
  <div class="mx-[2vw]">
   <div class="flex justify-end gap-6 mb-3  ">
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

    <div class="relative inline-block text-left">
      <div>
        <button
          @click="toggleDropdown('filter')"
          class="inline-flex justify-center w-full rounded-md border border-[#D9D9D9] text-[#008A8A]  font-medium shadow-sm px-4 py-1 bg-white text-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-[#008A8A]"
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

    <div class="relative inline-block text-left">
      <div>
        <button
          @click="toggleDropdown('category')"
          class="inline-flex justify-center w-full rounded-md border border-[#D9D9D9] text-[#008A8A] font-medium shadow-sm px-4 py-1 bg-white text-sm outline-none hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-[#008A8A]"
          type="button"
        >
          Category
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
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            role="menuitem"
            @click.prevent="showCategory('Electronics')"
          >
            Electronics
          </a>
          <a
            href="#"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            role="menuitem"
            @click.prevent="showCategory('Clothing')"
          >
            Clothing
          </a>
          <a
            href="#"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            role="menuitem"
            @click.prevent="showCategory('Furniture')"
          >
            Furniture
          </a>
          <a
            href="#"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            role="menuitem"
            @click.prevent="showCategory('Books')"
          >
            Books
          </a>
        </div>
      </div>
    </div>
  </div>
 <div class="grid grid-cols-1 sm:grid-cols-2 lg:ml-0 lg:grid-cols-3 mx:ml-[10%] sm:ml-[5%]  gap-[5%]  mt-16  items-center">
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
 