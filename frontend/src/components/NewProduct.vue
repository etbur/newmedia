
<script setup>
import { reactive, onMounted, onBeforeUnmount, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const productData = reactive({
  name: '',
  price: '',
  description: '',
  image: null,
  category: '',
});

const fileInput = ref(null);

let productSocket;
let categorySocket;

onMounted(() => {
  // Create WebSocket connection for product creation
  productSocket = new WebSocket(`ws://localhost:8000/ws/products/create/`);

  productSocket.onopen = () => {
    console.log('Product WebSocket connection opened');
  };

  productSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Product WebSocket message:', data);
    if (data.action === 'create_product_success') {
      router.push('/marketplace');
    } else if (data.action === 'create_product_error') {
      console.error('Error creating product:', data.error);
    }
  };

  productSocket.onerror = (error) => {
    console.error('Product WebSocket error:', error);
  };

  productSocket.onclose = () => {
    console.log('Product WebSocket connection closed');
  };

  // Create WebSocket connection for fetching categories
  categorySocket = new WebSocket(`ws://localhost:8000/ws/products/categories/`);

  categorySocket.onopen = () => {
    console.log('Category WebSocket connection opened');
    categorySocket.send(JSON.stringify({ action: 'fetch_categories' }));
  };

  categorySocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Category WebSocket message:', data);
    if (data.action === 'fetch_categories_success') {
      categories.value = data.categories;
    } else if (data.action === 'fetch_categories_error') {
      console.error('Error fetching categories:', data.error);
    }
  };

  categorySocket.onerror = (error) => {
    console.error('Category WebSocket error:', error);
  };

  categorySocket.onclose = () => {
    console.log('Category WebSocket connection closed');
  };
});

onBeforeUnmount(() => {
  if (productSocket) {
    productSocket.close();
  }
  if (categorySocket) {
    categorySocket.close();
  }
});

const createProduct = async () => {
  const sellerProfileName = store.state.activeUser?.name || '';
  const sellerProfilePicture = store.state.activeUser?.profilePicture || '';

  let imageBase64 = '';
  if (productData.image) {
    const reader = new FileReader();
    reader.onloadend = () => {
      imageBase64 = reader.result;
      sendProductData();
    };
    reader.readAsDataURL(productData.image);
  } else {
    sendProductData();
  }

  function sendProductData() {
    productSocket.send(
      JSON.stringify({
        action: 'create_product',
        product_data: {
          name: productData.name,
          price: productData.price,
          description: productData.description,
          image: imageBase64,
          seller_profile_name: sellerProfileName,
          seller_profile_picture: sellerProfilePicture,
          category: productData.category,
        },
      })
    );

    Object.assign(productData, {
      name: '',
      price: '',
      description: '',
      image: null,
      category: '',
    });

    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};

const categories = ref([]);
</script>

<template>
  <div class="flex flex-col gap-16">
    <h2 class="text-[#008a8a] font-medium text-xl">Add New Product</h2>
    <form @submit.prevent="createProduct" class="flex flex-col gap-7">
      <div class="flex gap-[5%]">
        <input
          type="text"
          id="name"
          v-model="productData.name"
          required
          placeholder="Enter Product name?"
          class="py-4 px-4 border border-[#008A8A] border-opacity-20 w-[30vw] outline-none rounded-md"
        />
        <input
          type="number"
          id="price"
          v-model="productData.price"
          step="0.01"
          required
          placeholder="Price Br"
          class="py-4 px-4 border border-[#008A8A] border-opacity-20 w-[8vw] outline-none rounded-md"
        />
      </div>
      <div>
        <input
          type="file"
          id="image"
          ref="fileInput"
          @change="productData.image = $event.target.files[0]"
          required
          placeholder="Choose image?"
          class="py-4 px-4 border border-[#008A8A] border-opacity-20 w-[42vw] outline-none rounded-md"
        />
      </div>
      <div>
        <textarea
          id="description"
          v-model="productData.description"
          required
          class="w-[42vw] h-[20vh] border border-[#008a8a] border-opacity-20 outline-none px-4 py-4"
          placeholder="Description ..."
        ></textarea>
      </div>
      <div>
        <select
          id="category"
          v-model="productData.category"
          required
          class="py-4 px-4 border border-[#008A8A] border-opacity-20 w-[42vw] outline-none rounded-md"
        >
          <option value="" disabled>Select a category</option>
          <option v-for="category in categories" :key="category.id" :value="category.name">
            {{ category.name }}
          </option>
        </select>
      </div>
      <button
        type="submit"
        class="py-4 px-6 border border-[#008a8a] font-medium border-opacity-20 rounded-md w-fit text-[#008a8a]"
      >
        Create Product
      </button>
    </form>
  </div>
</template>
