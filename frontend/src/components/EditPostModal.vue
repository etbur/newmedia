<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-[50vw]">
      <h3 class="text-lg font-semibold mb-4">Edit Post</h3>
      <form @submit.prevent="handleEdit">
        <!-- Form fields -->
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
        <div v-if="errorMessage" class="mb-4 text-red-500">{{ errorMessage }}</div>
        <div class="flex justify-end gap-4">
          <button type="submit" class="bg-[#C59728] text-white px-4 py-2 rounded">Save</button>
          <button @click.prevent="cancel" class="bg-gray-500 text-white px-4 py-2 rounded">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, onMounted } from 'vue';

const props = defineProps({
  post: Object,
  show: Boolean
});

const title = ref(props.post?.title || '');
const description = ref(props.post?.description || '');
const tags = ref(props.post?.tags || '');
const media = ref(null);
const mediaPreview = ref(props.post?.media || '');
const location = ref(props.post?.location || '');
const audience = ref(props.post?.audience || 'public');
const emit = defineEmits();

const socket = ref(null);
const errorMessage = ref('');

const openWebSocket = () => {
  socket.value = new WebSocket('ws://localhost:8000/ws/PostLikeComment'); 

  socket.value.onopen = () => {
    console.log('WebSocket connection established.');
    errorMessage.value = '';
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received message:', data);
    if (data.type === 'error') {
      errorMessage.value = data.error;
    } else {
      errorMessage.value = '';
    }
  };

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error);
    errorMessage.value = 'WebSocket error occurred. Please try again later.';
  };

  socket.value.onclose = (event) => {
    console.log('WebSocket connection closed.', event);
    if (event.wasClean) {
      console.log('Connection closed cleanly.');
    } else {
      console.error('Connection died.');
      errorMessage.value = 'WebSocket connection was closed unexpectedly. Please try again later.';
    }
  };
};

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

// const handleEdit = () => {
//   if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
//     errorMessage.value = 'WebSocket connection is not open. Please try again later.';
//     console.error('WebSocket connection is not open.');
//     return;
//   }

//   const data = {
//     action: 'edit_post',
//     post_id: props.post?.id, // Ensure post ID is included
//     data: {
//       title: title.value,
//       description: description.value,
//       tags: tags.value, // Ensure tags are formatted properly
//       media: media.value ? media.value.name : mediaPreview.value,
//       location: location.value,
//       audience: audience.value
//     }
//   };
  
//   try {
//     socket.value.send(JSON.stringify(data));
//     errorMessage.value = '';
//     cancel(); 
//   } catch (error) {
//     errorMessage.value = 'Failed to send data. Please try again.';
//     console.error('Failed to send data:', error);
//   }
// };

const handleEdit = () => {
  if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
    errorMessage.value = 'WebSocket connection is not open. Please try again later.';
    console.error('WebSocket connection is not open.');
    return;
  }

  const data = {
    action: 'edit_post',
    post_id: props.post?.id, // Ensure post ID is included
    data: {
      title: title.value,
      description: description.value,
      tags: tags.value, // Split and trim tags
      media: media.value ? mediaPreview.value : null, // Send base64 string or null
      location: location.value,
      audience: audience.value
    }
  };
  
  try {
    socket.value.send(JSON.stringify(data));
    errorMessage.value = '';
    console.log(data)
    cancel(); 
  } catch (error) {
    errorMessage.value = 'Failed to send data. Please try again.';
    console.error('Failed to send data:', error);
  }
};


const cancel = () => {
  emit('close');
};

onMounted(() => {
  openWebSocket();
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.close();
  }
});
</script>
