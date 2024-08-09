<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50 ">
    <div class="bg-white p-16 rounded-lg shadow-lg w-[50vw]">
      <h3 class="text-lg font-semibold mb-4">Edit Post</h3>
      <form @submit.prevent="submitEdit">
        <div class="mb-4">
          <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
          <input v-model="title" id="title" type="text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md"/>
        </div>
        <div class="mb-4">
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea v-model="description" id="description" rows="4" class="mt-1 block w-full p-2 border border-gray-300 rounded-md"></textarea>
        </div>
        <div class="mb-4">
          <label for="tags" class="block text-sm font-medium text-gray-700">Tags (comma-separated)</label>
          <input v-model="tags" id="tags" type="text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
        </div>
        <div class="mb-4">
          <label for="media" class="block text-sm font-medium text-gray-700">Media URLs </label>
          <input type="file" id="media" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" @change="handleMediaUpload" />
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
          <button type="submit" class="bg-[#C59728] text-white px-4 py-2 rounded" @click="handleEdit">Save</button>
          <button @click="cancel" class="bg-gray-500 text-white px-4 py-2 rounded">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import { ref, watch } from 'vue';
import store from '../store';

const props = defineProps({
  post: Object,
  show: Boolean
});

const emit = defineEmits(['close', 'edit']);

const title = ref(props.post ? props.post.title : '');
const description = ref(props.post ? props.post.description : '');
const tags = ref(props.post ? props.post.tags : '');
const media = ref(props.post ? props.post.media : '');
const location = ref(props.post ? props.post.location : '');
const audience = ref(props.post ? props.post.audience : 'public');
const error = ref(''); // For displaying errors

// Watch for changes to props.post and update local state accordingly
watch(() => props.post, (newPost) => {
  if (newPost) {
    title.value = newPost.title;
    description.value = newPost.description;
    tags.value = newPost.tags;
    location.value = newPost.location;
    audience.value = newPost.audience;
  }
});

const handleMediaUpload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
  };
  reader.onerror = (error) => {
    console.error("Error reading file:", error);
  };
};

const submitEdit = async () => {
  const userId = store.state.activeUser?.id;
  if (!props.post || props.post.user_id !== userId) {
    error.value = 'Unauthorized user or post data missing.';
    console.error(error.value);
    return;
  }

  const updatedPost = {
    title: title.value,
    description: description.value,
    media: media.value, // Array of file URLs
    tags: tags.value, // Convert comma-separated tags to an array
    location: location.value,
    audience: audience.value
  };

  try {
    // Assuming you have an API method to handle the update, replace `apiUpdatePost` with actual API call
    await apiUpdatePost(updatedPost); 
    emit('edit', updatedPost);
    emit('close');
  } catch (err) {
    error.value = 'Failed to update the post. Please try again.';
    console.error(err);
  }
};

const cancel = () => {
  emit('close');
};

const apiUpdatePost = async (post) => {
  // Replace with actual API call logic
  return new Promise((resolve, reject) => {
    // Simulate API call
    setTimeout(() => {
      if (Math.random() > 0.1) {
        resolve();
      } else {
        reject(new Error('Simulated API error'));
      }
    }, 1000);
  });
};
</script>

