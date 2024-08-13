
<template>
  <div class="flex hover:cursor-pointer fill-gray-300">
    <span v-for="star in maxStars" :key="star" @click="setRating(star)" class="star">
      <svg
        :class="{'filled ': star <= rating}"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        width="14"
        height="14"
      >
        <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
      </svg>
    </span>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  productId: Number,
  userId: Number,
  maxStars: {
    type: Number,
    default: 5
  }
});

const emit = defineEmits(['rating-changed']);
const rating = ref(0);

const getStorageKey = () => `rating-${props.userId}-${props.productId}`;

onMounted(() => {
  // Retrieve rating from local storage on component mount
  const savedRating = localStorage.getItem(getStorageKey());
  if (savedRating) {
    rating.value = parseFloat(savedRating);
  }
});

const setRating = (star) => {
  rating.value = star;
  // Save rating to local storage
  localStorage.setItem(getStorageKey(), star);
  emit('rating-changed', { productId: props.productId, userId: props.userId, rating: star });
};
</script>

<style scoped>
.star {
  cursor: pointer;
  display: inline-block;
  margin-right: 2px;
}
.filled {
  fill: gold;
}
</style>
