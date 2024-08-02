 <script setup>
 import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { format } from "date-fns";
import avatar from "../assets/avatar.png";

const store = useStore();
// Function to check if the user is authenticated
const isAuthenticated = () => {
  return !!store.state.activeUser; // Check the Vuex store for authentication status
};

const logCurrentUserInfo = () => {
  console.log("Current authenticated user info:", store.state.activeUser);
};
// Function to handle like toggling
const toggleLike = (postId) => {
  if (!isAuthenticated()) {
    showLoginModal.value = true; // Show login modal if not authenticated
    return;
  }

  const index = liked.value.indexOf(postId);
  if (index === -1) {
    liked.value.push(postId);
    sendLike(postId, true);
  } else {
    liked.value.splice(index, 1);
    sendLike(postId, false);
  }
};

// Function to send like action to WebSocket
const sendLike = (postId, liked) => {
  try {
    actionWebSocket.value.send(
      JSON.stringify({
        action: "like",
        post_id: postId,
        username: store.state.activeUser,
        liked,
      })
    );
  } catch (error) {
    console.error("Error sending like:", error);
  }
};

// Function to handle adding a comment
const addComment = (postId, content) => {
  if (!isAuthenticated()) {
    showLoginModal.value = true; // Show login modal if not authenticated
    return;
  }

  try {
    actionWebSocket.value.send(
      JSON.stringify({
        action: "comment",
        post_id: postId,
        username: store.state.activeUser,
        content,
      })
    );
    commentContent.value = ""; // Clear comment input after sending
    commentBoxVisible.value = null; // Hide comment box after sending
  } catch (error) {
    console.error("Error sending comment:", error);
  }
};

import { Icon } from "@iconify/vue";

const fetchWebSocket = ref(null);
const actionWebSocket = ref(null);
const posts = ref([]);
const liked = ref([]);
const currentUser = ref(null); // Initialize as null to represent unauthenticated

const router = useRouter();
const showLoginModal = ref(false); // State to control modal visibility

// State to manage which post is being commented on and visibility of comment box
const commentBoxVisible = ref(null);
const commentContent = ref("");

// State to manage which post's dropdown is visible
const dropdownVisible = ref(null);
const expandedPostId = ref(null); //close description


// Function to show comment box
const showCommentBox = (postId) => {
  commentBoxVisible.value = postId;
};

// Function to hide comment box
const hideCommentBox = () => {
  commentBoxVisible.value = null;
};

// Function to toggle dropdown visibility
const toggleDropdown = (postId) => {
  dropdownVisible.value = dropdownVisible.value === postId ? null : postId;
};

// Function to handle editing a post
const editPost = (postId) => {
  console.log("Editing post:", postId);
  // Implement the logic for editing a post
};

// Function to handle deleting a post
const deletePost = (postId) => {
  console.log("Deleting post:", postId);
  // Implement the logic for deleting a post
};

// Function to handle reporting a post
const reportPost = (postId) => {
  console.log("Reporting post:", postId);
  // Implement the logic for reporting a post
};

// Function to update like count locally
const updateLikeCount = (postId, delta) => {
  const post = posts.value.find((p) => p.id === postId);
  if (post) {
    post.count_like += delta;
  }
};

// Function to share post
const sharePost = (post) => {
  if (navigator.share) {
    navigator
      .share({
        title: post.title,
        text: post.description,
        url: `http://localhost:8000${post.media}`,
      })
      .then(() => {
        console.log("Thanks for sharing!");
      })
      .catch(console.error);
  } else {
    alert("Web Share API is not supported in your browser.");
  }
};

// Function to copy post link to clipboard
const copyLinkToClipboard = (post) => {
  const postUrl = `http://localhost:8000${post.media}`;
  navigator.clipboard.writeText(postUrl).then(
    () => {
      console.log("Link copied to clipboard!");
    },
    (err) => {
      console.error("Failed to copy the link: ", err);
    }
  );
};

// Function to download media
const downloadMedia = (post) => {
  const link = document.createElement("a");
  link.href = `http://localhost:8000${post.media}`;
  link.download = `${post.title}-${post.media.split("/").pop()}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Connect to WebSocket for fetching posts
const connectFetchWebSocket = () => {
  fetchWebSocket.value = new WebSocket("ws://localhost:8000/ws/posts/fetch");
  fetchWebSocket.value.onopen = onFetchWebSocketOpen;
  fetchWebSocket.value.onmessage = onFetchWebSocketMessage;
  fetchWebSocket.value.onerror = onWebSocketError;
  fetchWebSocket.value.onclose = onWebSocketClose;
};

// Connect to WebSocket for actions (like and comment)
const connectActionWebSocket = () => {
  actionWebSocket.value = new WebSocket(
    "ws://localhost:8000/ws/PostLikeCommentFollow"
  );
  actionWebSocket.value.onopen = onActionWebSocketOpen;
  actionWebSocket.value.onmessage = onActionWebSocketMessage;
  actionWebSocket.value.onerror = onWebSocketError;
  actionWebSocket.value.onclose = onWebSocketClose;
};

// Handle WebSocket open for fetching posts
const onFetchWebSocketOpen = () => {
  console.log("Fetch WebSocket connection opened");
  fetchPosts();
};

// Handle WebSocket open for actions
const onActionWebSocketOpen = () => {
  console.log("Action WebSocket connection opened");
};

// Handle incoming WebSocket messages for fetching posts
const onFetchWebSocketMessage = (event) => {
  try {
    const data = JSON.parse(event.data);

    if (!data.action) {
      console.error("Received message without action field:", data);
      return;
    }

    if (data.action === "fetch") {
      if (Array.isArray(data.posts)) {
        posts.value = data.posts;
      } else {
        console.error("Expected posts to be an array:", data.posts);
      }
    } else {
      console.error("Unexpected action:", data.action);
    }
  } catch (error) {
    console.error("Error handling WebSocket message:", error);
  }
};

const onActionWebSocketMessage=(event) =>{
        const data = JSON.parse(event.data);
        
        if (data.type === 'error') {
            console.error(`WebSocket error: ${data.error}`);
        } else if (data.type === 'comment') {
            handleCommentUpdate(data.comment);
        } else if (data.type === 'like') {
            handleLikeUpdate(data.like);
        } else {
            console.warn('Unknown WebSocket message type:', data);
        }
    }

// Handle WebSocket errors
const onWebSocketError = (error) => {
  console.error("WebSocket error:", error);
};

// Handle WebSocket closure
const onWebSocketClose = () => {
  console.log("WebSocket connection closed");
  setTimeout(() => {
    connectFetchWebSocket();
    connectActionWebSocket();
  }, 5000);
};

// Fetch posts from WebSocket
const fetchPosts = () => {
  try {
    fetchWebSocket.value.send(JSON.stringify({ action: "fetch" }));
  } catch (error) {
    console.error("Error sending fetch request:", error);
  }
};

// Handle comment updates
const handleCommentUpdate = (comment) => {
  const post = posts.value.find((p) => p.id === comment.post_id);
  if (post) {
    if (!post.comments) {
      post.comments = [];
    }
    post.comments.push(comment);
  }
};

// Handle like updates
const handleLikeUpdate = (like) => {
  const post = posts.value.find((p) => p.id === like.post_id);
  if (post) {
    if (like.liked) {
      post.count_like += 1;
    } else {
      post.count_like -= 1;
    }
  }
};

// Handle login button click in the modal
const handleLogin = () => {
  router.push("/login"); // Redirect to login page
  showLoginModal.value = false; // Hide modal after redirect
};
//format post date
const formattedPosts = computed(() => {
  return posts.value.map((post) => ({
    ...post,
    formatted_created_at: format(
      new Date(post.created_at),
      "MMMM d, yyyy, HH:mm"
    ),
  }));
});
//see description more

const toggleDescription = (postId) => {
  expandedPostId.value = expandedPostId.value === postId ? null : postId;
};

const isDescriptionExpanded = (postId) => {
  return expandedPostId.value === postId;
};
//close post
const closePost = (postId) => {
  posts.value = posts.value.filter((post) => post.id !== postId);
};
onMounted(() => {
  connectFetchWebSocket();
  connectActionWebSocket();
});

onUnmounted(() => {
  if (fetchWebSocket.value) {
    fetchWebSocket.value.close();
  }
  if (actionWebSocket.value) {
    actionWebSocket.value.close();
  }
});
</script> 
<template>
  <div
    class="flex flex-col lg:flex-row items-center md:items-start justify-evenly gap-[5vw] md:mx-[3vw]"
  >
    <!-- Posts Section -->
      <div class="flex flex-col gap-10 ">
        <div
          class="flex flex-col px-10 py-2  md:w-[60vw] lg:w-[40vw]  bg-[#f4f4f4] border-2 "
          v-for="post in formattedPosts"
          :key="post.id"
        >
          <div class="flex justify-end relative -right-6 py-4">
            <Icon
              icon="mdi:close"
              class="text-gray-800 w-6 h-6 hover:text-red-500 cursor-pointer"
              @click="closePost(post.id)"
            />
          </div>
          <div class="flex flex-col">
            <div
              class="flex flex-col  gap-2 lg:flex-row lg:justify-between lg:items-center mb-5"
            >
              <!-- User Info -->
              <div
                class="flex flex-col gap-2 lg:flex-row lg:justify-between lg:items-center mb-5"
              >
                <div class="flex gap-4 items-center">
                  <img
                    :src="post.user.profile_picture || avatar"
                    class="w-10 h-10 rounded-full"
                    alt="User profile picture"
                  />
                  <span class="text-[#C59728]">{{ post.user.username }}</span>
                </div>
              </div>
              <div>
                <!-- More Options Dropdown -->
                <div class="flex justify-between gap-2">
                  <h2 class="text-sm mb-4 text-black capitalize">
                    {{ post.formatted_created_at }}
                  </h2>

                  <div class="relative">
                    <Icon
                      icon="mdi:dots-vertical"
                      class="text-gray-800 hover:text-[#C59728] cursor-pointer text-sm w-10 h-5 sm:text-base"
                      @click="toggleDropdown(post.id)"
                    />
                    <div
                      v-if="dropdownVisible === post.id"
                      class="absolute -right-44 mt-3 w-48 bg-gray-50 border border-gray-300 rounded-md shadow-lg"
                    >
                      <ul>
                        <li
                          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                          @click="editPost(post.id)"
                        >
                          Edit Post
                        </li>
                        <li
                          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                          @click="deletePost(post.id)"
                        >
                          Delete Post
                        </li>
                        <li
                          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                          @click="reportPost(post.id)"
                        >
                          Report Post
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <h2 class="text-lg font-medium text-[#C59728] mb-4 capitalize">
              {{ post.title }}
            </h2>
            <img
              v-if="
                post.media &&
                (post.media.endsWith('.jpeg') ||
                  post.media.endsWith('.jpg') ||
                  post.media.endsWith('.png'))
              "
              :src="`http://localhost:8000${post.media}`"
              alt="post img"
              class="rounded-lg  object-cover"
              
            />
            <video
              v-else-if="
                post.media &&
                (post.media.endsWith('.mp4') ||
                  post.media.endsWith('.mov') ||
                  post.media.endsWith('.avi'))
              "
              :src="`http://localhost:8000${post.media}`"
              controls
              class="rounded-lg h-auto"
            >
              Your browser does not support the video tag.
            </video>
            <div
              v-else
              class="bg-gray-200 rounded-lg w-32 h-32 flex items-center justify-center"
            >
              <Icon icon="mdi:file" class=" w-12 h-12" />
            </div>
            <p class="text-gray-800 my-8">
              {{
                post.description.length > 100 && !isDescriptionExpanded(post.id)
                  ? post.description.substring(0, 100) + "..."
                  : post.description
              }}
              <button
                v-if="post.description.length > 100"
                @click="toggleDescription(post.id)"
                class="text-[#C59728] underline"
              >
                {{ isDescriptionExpanded(post.id) ? "Show less" : "Show more" }}
              </button>
            </p>
            <div
              class="flex  flex-wrap justify-between items-center text-gray-500 mb-6 bg-white  px-6 py-2 rounded-md"
            >
              <button @click="toggleLike(post.id)" class="flex flex-col gap-2">
                {{ post.count_like }} Likes

                <Icon
                  :icon="
                    liked.includes(post.id) ? 'mdi:heart' : 'mdi:heart-outline'
                  "
                />
              </button>
              <!-- Comment Button -->
              <button
                class="flex  flex-col  hover:text-[#C59728] gap-2 "
              >
              <span class="text-sm sm:text-base flex "
              >{{ post.count_comment }} comment</span>
                <Icon
                  v-if="isAuthenticated()"
                  icon="mdi:comment-outline"
                  class="cursor-pointer"
                  @click="showCommentBox(post.id)"
                />
                <Icon
                  v-else
                  icon="mdi:comment-outline"
                  class="cursor-pointer"
                  @click="showLoginModal = true"
                />
               
              </button>

              <button @click="sharePost(post)" class="flex flex-col gap-2">
                <Icon icon="mdi:share-outline" class="cursor-pointer" />
                Share
              </button>
              <button @click="copyLinkToClipboard(post)" class="flex flex-col gap-2">
                <Icon icon="mdi:content-copy" class="cursor-pointer" />
                Copy link
              </button>
              <button @click="downloadMedia(post)" class="flex flex-col gap-2">
                <Icon icon="mdi:download-outline"  class="cursor-pointer"/>
                Download
              </button>
            
            </div>
          </div>
        </div>
      </div>
    <!-- Sidebar Section -->
    <div class="grid grid-cols-2 md:grid-cols-1 gap-10 w-[25vw] h-auto">
      <div class="bg-[#edeaea] rounded-lg shadow-md p-6">
        <h2 class="text-lg font-medium text-gray-800 mb-4">
          People you may know
        </h2>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-lg font-medium text-gray-800 mb-4">Trends</h2>
      </div>
    </div>
  </div>

  <!-- Login Modal -->
  <div
    v-if="showLoginModal"
    class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-80">
      <h3 class="text-lg font-semibold mb-4">Please Log In</h3>
      <p class="mb-4">You need to be logged in to like or comment on posts.</p>
      <div class="flex justify-end gap-4">
        <button
          @click="handleLogin"
          class="bg-[#C59728] text-white px-4 py-2 rounded"
        >
          Log In
        </button>
        <button
          @click="showLoginModal = false"
          class="bg-gray-200 px-4 py-2 rounded"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>


