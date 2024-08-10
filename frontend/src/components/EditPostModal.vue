<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[50vw]">
      <h3 class="text-lg font-semibold mb-4">Edit Post</h3>
      <form @submit.prevent="handleEdit">
        <div class="mb-4">
          <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
          <input v-model="title" id="title" type="text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" required />
        </div>
        <div class="mb-4">
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea v-model="description" id="description" rows="4" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" required></textarea>
        </div>
        <div class="mb-4">
          <label for="tags" class="block text-sm font-medium text-gray-700">Tags (comma-separated)</label>
          <input v-model="tags" id="tags" type="text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
        </div>
        <div class="mb-4">
          <label for="media" class="block text-sm font-medium text-gray-700">Media</label>
          <input type="file" id="media" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" @change="handleMediaUpload" />
          <div v-if="mediaPreview" class="mt-2">
            <img :src="mediaPreview" alt="Preview" class="rounded-lg w-16" />
          </div>
        </div>
        <div class="mb-4">
          <label for="location" class="block text-sm font-medium text-gray-700">Location</label>
          <input v-model="location" id="location" type="text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
        </div>
        <div class="mb-4">
          <label for="audience" class="block text-sm font-medium text-gray-700">Audience</label>
          <select v-model="audience" id="audience" class="mt-1 block w-full p-2 border border-gray-300 rounded-md">
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
        <div class="flex justify-end gap-4">
          <button type="submit" class="bg-[#C59728] text-white px-4 py-2 rounded">Save</button>
          <button @click="cancel" class="bg-gray-500 text-white px-4 py-2 rounded">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
  post: Object,
  show: Boolean
});

const emit = defineEmits(['close', 'edit']);

const title = ref('');
const description = ref('');
const tags = ref('');
const media = ref(null);
const location = ref('');
const audience = ref('public');
const mediaPreview = ref('');

const store = useStore();

watch(() => props.post, (newPost) => {
  if (newPost) {
    title.value = newPost.title;
    description.value = newPost.description;
    tags.value = newPost.tags;
    location.value = newPost.location;
    audience.value = newPost.audience;
    mediaPreview.value = newPost.media ? `http://localhost:8000${newPost.media}` : '';
  }
}, { immediate: true });

const handleMediaUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      mediaPreview.value = reader.result;
      media.value = file;
    };
    reader.readAsDataURL(file);
  }
};

const handleEdit = async () => {
  try {
    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('description', description.value);
    formData.append('tags', tags.value);
    formData.append('location', location.value);
    formData.append('audience', audience.value);
    if (media.value) {
      formData.append('media', media.value);
    }

    await store.dispatch('updatePost', { id: props.post.id, data: formData });
    emit('edit', { id: props.post.id, data: formData });
    cancel();
  } catch (error) {
    console.error('Error editing post:', error);
  }
};

const cancel = () => {
  emit('close');
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
