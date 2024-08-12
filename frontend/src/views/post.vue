
<template>
  <main
    class="flex flex-col gap-10 mx-10 md:mx-0 px-4 sm:px-8 md:px-12 lg:px-16 xl:px-20 mt-8 sm:mt-12 md:mt-16 lg:mt-20 xl:mt-24"
  >
    <h1 class="text-xl font-semibold">New Post</h1>
    <div>
      <h2 class="text-[#C59728] text-lg">Author Name | Published Date</h2>
      <p>Please fill the content of the new post...</p>
    </div>
    <Form :validation-schema="validationSchema" @submit="onSubmit">
      <div class="flex flex-col gap-5">
        <div class="flex flex-col sm:flex-row gap-5">
          <div class="flex flex-col gap-2 flex-1">
            <Field
              type="text"
              class="px-4 py-3 border-2 rounded-lg outline-none w-full"
              placeholder="Title (Optional)"
              id="title"
              name="title"
              :value="formInput.title"
              @input="formInput.title = $event.target.value"
            />
            <ErrorMessage name="title" class="text-red-500" />
          </div>
          <div class="flex flex-col gap-2 flex-1">
            <Field
              type="text"
              class="px-4 py-3 border-2 rounded-lg outline-none w-full"
              placeholder="What's happening?"
              id="description"
              name="description"
              :value="formInput.description"
              @input="formInput.description = $event.target.value"
            />
            <ErrorMessage name="description" class="text-red-500" />
          </div>
        </div>
        <div class="flex flex-col sm:flex-row gap-5">
          <div class="flex flex-col gap-2 flex-1">
            <Field
              type="text"
              class="px-4 py-3 border-2 rounded-lg outline-none w-full"
              placeholder="Tags (comma separated)"
              id="tags"
              name="tags"
              :value="formInput.tags"
              @input="formInput.tags = $event.target.value"
            />
            <ErrorMessage name="tags" class="text-red-500" />
          </div>
          <div class="flex flex-col gap-2 flex-1">
            <div class="relative flex gap-2">
              <Field
                type="file"
                class="px-4 py-3 border-2 rounded-lg outline-none w-full"
                id="media"
                name="media"
                @change="handleMediaUpload"
              />
              <ErrorMessage name="media" class="text-red-500" />
              <div v-if="previewUrl">
                <img :src="previewUrl" class="max-h-21 w-full object-contain" />
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row gap-5">
          <div class="flex flex-col gap-2 flex-1">
            <Field
              type="text"
              class="px-4 py-3 border-2 rounded-lg outline-none w-full"
              placeholder="Location (Optional)"
              id="location"
              name="location"
              :value="formInput.location"
              @input="formInput.location = $event.target.value"
            />
          </div>
          <div class="flex flex-col gap-2 w-full sm:w-[10rem]">
            <select
              class="px-4 py-3 border-2 rounded-lg outline-none w-full"
              :value="formInput.audience"
              @change="formInput.audience = $event.target.value"
            >
              <option value="public">Public</option>
              <option value="friends">Friends</option>
              <option value="group">Group</option>
            </select>
          </div>
        </div>
      </div>
      <div class="flex justify-end mt-6">
        <button
          type="submit"
          class="px-8 py-2 rounded-xl border-gray-300 bg-[#008A8A] text-white w-fit"
        >
          Post
        </button>
      </div>
    </Form>
  </main>
</template>

<script setup>
import { reactive, ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as Yup from 'yup';

const router = useRouter();

const previewUrl = ref(null);
const formInput = reactive({
  title: '',
  description: '',
  tags: '',
  media: '',
  location: '',
  audience: 'public',
});

let websocket;

const connectWebSocket = () => {
  websocket = new WebSocket('ws://localhost:8000/ws/posts/');
  websocket.onopen = () => {
    console.log('WebSocket connection established');
  };
  websocket.onmessage = (message) => {
    console.log('Message from server:', message.data);
  };
  websocket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  websocket.onclose = () => {
    console.log('WebSocket connection closed');
  };
};

const validationSchema = Yup.object({
  title: Yup.string().max(100, 'Title must be less than 100 characters'),
  description: Yup.string().max(500, 'Description must be less than 500 characters').required('Description is required!'),
  tags: Yup.string().max(100, 'Tags must be less than 100 characters'),
  media: Yup.mixed().required('Media is required!'),
});

const onSubmit = async (values) => {
  const data = {
    action: 'create',
    post: {
      title: values.title,
      description: values.description,
      tags: values.tags.split(',').map((tag) => tag.trim()),
      media: formInput.media,
      location: values.location,
      audience: values.audience,
    },
  };

  try {
    console.log('Submitting form with data:', data);
    websocket.send(JSON.stringify(data));
    console.log('Data sent to WebSocket');

    // Reset form input after sending data
    Object.keys(formInput).forEach((key) => {
      formInput[key] = '';
    });

    // Optionally, navigate after submission
    await router.push('/');
  } catch (error) {
    console.error('Error sending data:', error);
    alert('An error occurred. Please try again later.');
  }
};

const handleMediaUpload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
    formInput.media = reader.result;
    previewUrl.value = reader.result;
  };
  reader.onerror = (error) => {
    console.error('Error reading file:', error);
  };
};

// Set up and clean up WebSocket connection
onMounted(connectWebSocket);
onBeforeUnmount(() => {
  if (websocket) {
    websocket.close();
  }
});
</script>
