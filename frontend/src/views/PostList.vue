<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import EditPostModal from "../components/EditPostModal.vue";
import { useRouter } from "vue-router";
import { format } from "date-fns";
import avatar from "../assets/avatar.png";
import { Icon } from "@iconify/vue";
import store from "@/store";

const router = useRouter();

const fetchWebSocket = ref(null);
const actionWebSocket = ref(null);
const posts = ref([]);
const liked = ref([]);
const showLoginModal = ref(false);
const commentBoxVisible = ref(null);
const commentContent = ref("");
const dropdownVisible = ref(null);
const expandedPostId = ref(null);
const showEditModal = ref(null);
const selectedPost = ref(null);
const isOwner = (post) => store.state.activeUser.id === post.user_id;
const isAuthenticated = () => !!store.state.activeUser;
console.log(store.state.activeUser);

const sendLike = (postId, liked) => {
  if (!postId || !store.state.activeUser) {
    console.error("Invalid post ID or user not authenticated");
    return;
  }
  try {
    actionWebSocket.value.send(
      JSON.stringify({
        action: "like",
        post_id: postId,
        username: store.state.activeUser.username,
        liked,
      })
    );
  } catch (error) {
    console.error("Error sending like:", error);
  }
};

const handleCommentUpdate = (comment) => {
  const post = posts.value.find((p) => p.id === comment.post_id);
  if (post) {
    if (!post.comments) {
      post.comments = [];
    }
    post.comments.push(comment);
    post.count_comment += 1;
  }
};

const addComment = (postId, content) => {
  if (!postId || !store.state.activeUser) {
    console.error("Invalid post ID or user not authenticated");
    return;
  }
  try {
    actionWebSocket.value.send(
      JSON.stringify({
        action: "comment",
        post_id: postId,
        username: store.state.activeUser.username,
        content,
      })
    );
    commentContent.value = "";
    commentBoxVisible.value = null;
  } catch (error) {
    console.error("Error sending comment:", error);
  }
};

const connectFetchWebSocket = () => {
  fetchWebSocket.value = new WebSocket("ws://localhost:8000/ws/posts/fetch");
  fetchWebSocket.value.onopen = onFetchWebSocketOpen;
  fetchWebSocket.value.onmessage = onFetchWebSocketMessage;
  fetchWebSocket.value.onerror = onWebSocketError;
  fetchWebSocket.value.onclose = onWebSocketClose;
};

const connectActionWebSocket = () => {
  actionWebSocket.value = new WebSocket(
    "ws://localhost:8000/ws/PostLikeComment"
  );
  actionWebSocket.value.onopen = onActionWebSocketOpen;
  actionWebSocket.value.onmessage = onActionWebSocketMessage;
  actionWebSocket.value.onerror = onWebSocketError;
  actionWebSocket.value.onclose = onWebSocketClose;
};

const updateLikeCount = (postId, liked) => {
  const post = posts.value.find((p) => p.id === postId);
  if (post) {
    console.log(
      `Updating like count for post ${postId}: ${post.count_like} -> ${
        post.count_like + (liked ? 1 : -1)
      }`
    );
    post.count_like += liked ? 1 : -1;
  }
};

const toggleLike = (postId) => {
  if (!isAuthenticated()) {
    showLoginModal.value = true;
    return;
  }

  const index = liked.value.indexOf(postId);
  if (index === -1) {
    liked.value.push(postId);
    updateLikeCount(postId, true);
    sendLike(postId, true);
  } else {
    liked.value.splice(index, 1);
    updateLikeCount(postId, false);
    sendLike(postId, false);
  }
};

const showCommentBox = (postId) => {
  if (!isAuthenticated()) {
    showLoginModal.value = true;
    return;
  }

  commentBoxVisible.value = commentBoxVisible.value === postId ? null : postId;
  if (commentBoxVisible.value === postId) {
    fetchComments(postId); // Fetch comments when the box is shown
  }
};

const fetchComments = (postId) => {
  try {
    actionWebSocket.value.send(
      JSON.stringify({
        action: "fetch_comments",
        post_id: postId,
      })
    );
  } catch (error) {
    console.error("Error sending fetch comments request:", error);
  }
};

const onFetchWebSocketOpen = () => {
  console.log("Fetch WebSocket connection opened on post");
  fetchPosts();
};

const onActionWebSocketOpen = () => {
  console.log("Action WebSocket connection opened on post");
};

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

const onActionWebSocketMessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    if (data.type === "error") {
      console.error(`WebSocket error: ${data.error}`);
    } else if (data.type === "comment") {
      handleCommentUpdate(data.comment);
    } else if (data.type === "comments") {
      updatePostComments(data.post_id, data.comments);
    } else if (data.action === "edit_post") {
      const updatedPost = data.post;
      const index = posts.value.findIndex((p) => p.id === updatedPost.id);
      if (index !== -1) {
        posts.value[index] = updatedPost;
      }
    } else if (data.action === "delete_post") {
      const postId = data.post_id;
      posts.value = posts.value.filter((post) => post.id !== postId);
    } else {
      console.warn("Unknown WebSocket message type:", data);
    }
  } catch (error) {
    console.error("Error handling WebSocket message:", error);
  }
};

const updatePostComments = (postId, comments) => {
  const post = posts.value.find((p) => p.id === postId);
  if (post) {
    post.comments = comments;
  } else {
    console.warn("Post not found for comments update:", postId);
  }
};

const onWebSocketError = (error) => {
  console.error("WebSocket error:", error);
};

const copyLinkToClipboard = (post) => {
  const url = `http://localhost:8000/posts/${post.id}`;
  navigator.clipboard
    .writeText(url)
    .then(() => {
      console.log("Link copied to clipboard");
    })
    .catch((err) => {
      console.error("Error copying link:", err);
    });
};
const sharePost = async (post) => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: post.title,
        text: post.description,
        url: `http://localhost:8000/posts/${post.id}`,
      });
      console.log("Post shared successfully");
    } catch (error) {
      console.error("Error sharing post:", error);
    }
  } else {
    console.warn("Web Share API is not supported in this browser.");
    // Fallback to other sharing methods or show a message
  }
};

const onWebSocketClose = () => {
  console.log("WebSocket connection closed");
  setTimeout(() => {
    connectFetchWebSocket();
    connectActionWebSocket();
  }, 5000);
};

const fetchPosts = () => {
  try {
    fetchWebSocket.value.send(JSON.stringify({ action: "fetch" }));
  } catch (error) {
    console.error("Error sending fetch request:", error);
  }
};

const handleLogin = () => {
  router.push("/login");
  showLoginModal.value = false;
};

const formattedPosts = computed(() => {
  return posts.value.map((post) => ({
    ...post,
    formatted_created_at: format(
      new Date(post.created_at),
      "MMMM d, yyyy, HH:mm"
    ),
  }));
});

const toggleDescription = (postId) => {
  expandedPostId.value = expandedPostId.value === postId ? null : postId;
};

const isDescriptionExpanded = (postId) => {
  return expandedPostId.value === postId;
};

const closePost = (postId) => {
  posts.value = posts.value.filter((post) => post.id !== postId);
};

const toggleDropdown = (postId) => {
  dropdownVisible.value = dropdownVisible.value === postId ? null : postId;
};

const handleEdit = (updatedPost) => {
  if (selectedPost.value && selectedPost.value.id) {
    console.log("Editing post with ID:", selectedPost.value.id);
    console.log("Updated data:", updatedPost);
    try {
      actionWebSocket.value.send(
        JSON.stringify({
          action: "edit_post",
          post_id: selectedPost.value.id,
          new_data: updatedPost,
        })
      );
    } catch (error) {
      console.error("Error sending edit request:", error);
    }
    showEditModal.value = false;
    selectedPost.value = null;
  } else {
    console.error("No selected post or post ID is missing.");
  }
};


const editPost = (post) => {
  if (post && isOwner(post)) {
    selectedPost.value = post;
    showEditModal.value = true;
  } else {
    console.error("Post is null or you are not authorized to edit this post");
  }
};

const deletePost = (postId) => {
  if (isOwner(posts.value.find((p) => p.id === postId))) {
    if (confirm("Are you sure you want to delete this post?")) {
      try {
        actionWebSocket.value.send(
          JSON.stringify({
            action: "delete_post",
            post_id: postId,
          })
        );
        // alert('post Successfull deleted!')
        connectFetchWebSocket();
      } catch (error) {
        console.error("Error sending delete request:", error);
      }
    }
  } else {
    console.error("You are not authorized to delete this post");
  }
};

const downloadMedia = (post) => {
  const mediaUrl = `http://localhost:8000${post.media}`;
  const link = document.createElement("a");
  link.href = mediaUrl;
  link.download = post.media.split("/").pop(); // Filename
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  // Show a confirmation message
  alert("Download started");
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
    <div class="grid grid-col-2 sm:grid-cols-1 gap-8 bg-[#f4f4f4] py-6">
      <div
        class="bg-[#ffffff] grid grid-cols-1 mx-8 px-6 shadow-sm w-full sm:w-[35vw]"
        v-for="post in formattedPosts"
        :key="post.id"
      >
        <div class="flex justify-end relative right-3 pt-5 mb-2">
          <Icon
            icon="mdi:close"
            class="text-gray-800 w-5 h-5 hover:text-red-600 cursor-pointer"
            @click="closePost(post.id)"
          />
        </div>
        <div class="flex flex-col">
          <div
            class="flex flex-col gap-2 lg:flex-row lg:justify-between lg:items-center mb-5"
          >
            <!-- User Info -->
            <div class="flex gap-4 items-center">
              <img
                :src="post.profile_picture || avatar"
                class="w-10 h-10 rounded-full"
                alt="User profile picture"
              />
              <span class="text-[#C59728] text-sm">{{ post.username }}</span>
            </div>
            <div>
              <!-- More Options Dropdown -->
        
              <div class="relative flex gap-2">
                {{ post.formatted_created_at }}
                <Icon
                  icon="mdi:dots-vertical"
                  class="text-gray-800 hover:text-[#C59728] cursor-pointer text-sm w-10 h-5 sm:text-base"
                  @click="toggleDropdown(post.id)"
                />
                <div
                  v-if="dropdownVisible === post.id && isOwner(post)"
                  class="absolute -right-44 mt-3 w-48 bg-gray-50 border border-gray-300 rounded-md shadow-lg z-30"
                >
                  <ul>
                    <li
                      class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                      @click="editPost(post)"
                    >
                      Edit Post
                    </li>
                    <li
                      class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                      @click="deletePost(post.id)"
                    >
                      Delete Post
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <h2 class="text-lg font-medium text-[#C59728] capitalize mt-1">
            {{ post.title }}
          </h2>
          <p class="text-gray-800 mb-4 mt-1">
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
          <img
            v-if="
              post.media &&
              (post.media.endsWith('.jpeg') ||
                post.media.endsWith('.jpg') ||
                post.media.endsWith('.png'))
            "
            :src="`http://localhost:8000${post.media}`"
            alt="post img"
            class="rounded-lg object-cover h-[45vh]"
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
            <Icon icon="mdi:file" class="w-12 h-12" />
          </div>

          <div
            class="py-2 flex flex-wrap gap-[4vw] items-center text-gray-500 my-4 px-6 rounded-md"
          >
            <button
              @click="toggleLike(post.id)"
              class="flex flex-col gap-2 text-sm hover:text-[#C59728]"
            >
              {{ post.count_like }} Likes
              <Icon
                :icon="
                  liked.includes(post.id) ? 'mdi:like' : 'mdi:like-outline'
                "
                class="text-red-500"
              />
            </button>
            <!-- Comment Button -->
            <button class="flex flex-col gap-2">
              <span class="text-sm sm:text-base flex hover:text-[#C59728]">
                {{ post.count_comment }} comment
              </span>
              <Icon
                :icon="
                  isAuthenticated() ? 'mdi:chat-outline' : 'mdi:chat-outline'
                "
                class="cursor-pointer"
                @click="
                  isAuthenticated()
                    ? showCommentBox(post.id)
                    : (showLoginModal = true)
                "
              />
            </button>

            <button @click="sharePost(post)" class="flex flex-col gap-2">
              <Icon
                icon="mdi:share-outline"
                class="cursor-pointer"
                title="Share"
              />
            </button>
            <button
              @click="copyLinkToClipboard(post)"
              class="flex flex-col gap-2"
            >
              <Icon
                icon="mdi:content-copy"
                class="cursor-pointer"
                title="copyLink"
              />
            </button>
            <button @click="downloadMedia(post)" class="flex flex-col gap-2">
              <Icon
                icon="mdi:download-outline"
                class="cursor-pointer"
                title="Download"
              />
            </button>
          </div>
        </div>

        <div
          v-if="commentBoxVisible === post.id"
          class="border-t-2 border-gray-200 py-3"
        >
          <div class="flex flex-col gap-2">
            <!-- Comment Box Header -->
            <div class="flex items-center gap-4 mb-2">
              <img
                :src="store.state.activeUser?.profile_picture || avatar"
                class="w-8 h-8 rounded-full"
                alt="User profile picture"
              />
              <input
                v-model="commentContent"
                type="text"
                placeholder="Add a comment..."
                class="w-full p-2 border border-gray-300 rounded-md"
              />
              <button
                @click="addComment(post.id, commentContent)"
                class="bg-[#C59728] text-white p-2 rounded-md"
              >
                Submit
              </button>
            </div>

            <!-- Display Comments -->
            <div v-if="post.comments && post.comments.length" class="space-y-2">
              <div
                v-for="comment in post.comments"
                :key="comment.created_at"
                class="flex items-start gap-2"
              >
                <img
                  :src="comment.profile_picture || avatar"
                  class="w-8 h-8 rounded-full"
                  alt="User profile picture"
                />
                <div class="flex flex-col">
                  <span class="font-semibold">{{ comment.username }}</span>
                  <p class="text-gray-800">{{ comment.content }}</p>
                  <span class="text-gray-500 text-xs">{{
                    format(new Date(comment.created_at), "MMMM d, yyyy, HH:mm")
                  }}</span>
                </div>
              </div>
            </div>
            <div v-else>
              <p class="text-gray-500">No comments yet.</p>
            </div>
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
          class="bg-gray-500 text-white px-4 py-2 rounded"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
  <EditPostModal
    v-if="showEditModal"
    :post="selectedPost"
    :show="showEditModal"
    @close="showEditModal = false"
    @edit="handleEdit"
  />
</template>
