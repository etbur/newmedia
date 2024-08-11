<template>
  <div class="facebook-layout">
    <div class="header">
      <h1>Header</h1>
      <div class="header-icons">
        <router-link to="/app"><a href="#"><i class="fas fa-envelope"></i></a></router-link>
        <a href="#"><i class="fas fa-bell"></i></a>
        <a href="#"><i class="fas fa-user-friends"></i></a>
        <a href="#"><i class="fas fa-users"></i></a>
        <a href="#"><i class="fas fa-user-circle"></i></a>
      </div>
    </div>

    <div class="main-container">
      <div class="sidebar">
        <button class="menu-toggle-btn" @click="toggleMenu">
          <i class="fas fa-bars"></i>
        </button><br><br><br><br>
        <ul class="menu-items" :class="{ 'show-menu': showMenu }">
          <router-link to="/friends"><li class="menu-item"><i class="fas fa-user-friends"></i> Add Friend</li></router-link>
          <router-link to="/app"><li class="menu-item"><i class="fas fa-envelope"></i> Message</li></router-link>
          <router-link to="/gruop"><li class="menu-item"><i class="fas fa-users"></i> Group</li></router-link>
          <router-link to="/markat"><li class="menu-item"><i class="fas fa-bullhorn"></i> Marketing</li></router-link>
          <router-link to="/game"><li class="menu-item"><i class="fas fa-gamepad"></i> Game</li></router-link>
          <router-link to="/event"><li class="menu-item"><i class="fas fa-calendar-alt"></i> Event</li></router-link>
          <router-link to="/job"><li class="menu-item"><i class="fas fa-briefcase"></i> Job</li></router-link>
          <router-link to="/design"><li class="menu-item"><i class="fas fa-paint-brush"></i> Design</li></router-link>
          <router-link to="/signlng"><li class="menu-item"><i class="fas fa-sign-language"></i> Sign Language</li></router-link>
          <router-link to="/vtt"><li class="menu-item"><i class="fas fa-microphone"></i> Voice to Text</li></router-link>
          <router-link to="/advert"><li class="menu-item"><i class="fas fa-microphone"></i> Advert Here</li></router-link>
          <li class="menu-item"><i class="fas fa-ellipsis-h"></i> Other</li>
        <router-link to="/faq"><li class="menu-item"><i class="fas fa-users"></i> FAQ</li></router-link>
        <router-link to="/new"><li class="menu-item"><i class="fas fa-bullhorn"></i> New</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
        <router-link to="/privacy"><li class="menu-item"><i class="fas fa-lock"></i> Privacy Policy</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
        </ul>
      </div>
      <h2 class = "">Marketplace</h2>
    <div class="product-list">
      <div v-for="product in products" :key="product.id" class="product">
        <img :src="product.image" :alt="product.title" class="product-image">
        <div class="product-details">
          <h3 class="product-title">{{ product.title }}</h3>
          <p class="product-price">{{ product.price }}</p>
          <button class="product-button" @click="addToCart(product)">Add to Cart</button>
        </div>
      </div>  
    </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      products: [
        {
          id: 1,
          title: 'Product 1',
          price: '$10.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 2,
          title: 'Product 2',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 3,
          title: 'Product 3',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 4,
          title: 'Product 4',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 5,
          title: 'Product 5',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 6,
          title: 'Product 6',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 7,
          title: 'Product 7',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 8,
          title: 'Product 8',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        {
          id: 9,
          title: 'Product 9',
          price: '$19.99',
          image: '/src/assets/logo.png'
        },
        // Add more products as needed
      ],
      cart: []
    };
  },
  methods: {
    addToCart(product) {
      this.cart.push(product);
      // You can perform additional logic here, such as updating the cart count or making API calls
    }
  }
};
</script>

<style>
.facebook-layout {
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #4267B2;
  color: #fff;
  padding: 20px;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;

}

.header-icons a {
  color: #fff;
  margin-left: 10px;
  text-decoration: none;
}

.main-container {
  display: flex;
}

.sidebar {
  background-color: #f0f2f5;
  width: 300px;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
    overflow-y: auto;
}

.post-list {
  margin-left: 320px; /* Adjust according to sidebar width */
  padding: 20px;
}

.post {
  background-color: #ffffff;
  padding: 10px;
  margin-bottom: 20px;
}

.post p {
  margin: 0;
}

/* Media Query for Small Devices */
@media (max-width: 768px) {
  .header {
    padding: 10px;
     position: sticky;
  top: 0;
  z-index: 100;
  }

  .header h1 {
    font-size: 16px;
  }

  

  .main-container {
    flex-direction: column;
    align-items: center;
  }

  .sidebar {
    width: 100%;
    max-width: 50px;
    padding: 10px;
  }

  .post-list {
    padding: 1px;
    margin-left:0;
  }
}

sidebar {
  background-color: #f0f2f5;
  width: 300px;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
}

.menu-items {
  list-style-type: none;
  padding: 0;
}

.menu-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.menu-item i {
  margin-right: 5px;
}

.show-menu .menu-items {
  display: block;
}

.product-list {
    margin-left: 150px;
   margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* Adjust layout for small devices */
@media (max-width: 768px) {
  .product-list {
    grid-template-columns: repeat(2, 1fr);
    margin-left:100px

  }
}

/* Adjust layout for extra small devices */
@media (max-width: 480px) {
  .product-list {
    grid-template-columns: repeat(1, 1fr);
     margin-left:100px
  }
}

.product {
  
  background-color: #ffffff;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column; /* Added to stack image and details vertically */
  align-items: center; /* Added to center align items horizontally */
  text-align: center; /* Added to center align text */
}

.product-image-container {
  margin-bottom: 10px; /* Added to create space between image and details */
}

.product-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
}

.product-details {
  flex: 1;
}

.product-title {
  
  font-size: 18px;
}

.product-price {
  margin: 0;
  color: #888888;
}
.product-button {
  padding: 5px 10px;
  background-color: #4267B2;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
</style>