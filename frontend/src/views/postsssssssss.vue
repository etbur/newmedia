<template>
  <div id="app">
    <header>
      <nav>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Profile</a></li>
          <li><a href="#">Logout</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <div class="post-form">
        <textarea v-model="newPostContent" placeholder="What's on your mind?"></textarea>
        <button @click="createPost">Post</button>
      </div>

      <div class="posts">
        <div class="post" v-for="post in posts" :key="post.id">
          <div class="post-header">
            <img :src="post.user.avatar" alt="User Avatar" class="avatar">
            <h3>{{ post.user.username }}</h3>
            <p>{{ post.created_at }}</p>
          </div>
          <p class="post-content">{{ post.content }}</p>
          <div class="comments">
            <div class="comment" v-for="comment in post.comments" :key="comment.id">
              <img :src="comment.user.avatar" alt="User Avatar" class="avatar">
              <div>
                <h4>{{ comment.user.username }}</h4>
                <p>{{ comment.content }}</p>
              </div>
            </div>
            <div class="comment-form">
              <textarea v-model="newCommentContent" placeholder="Add a comment..."></textarea>
              <button @click="createComment(post.id)">Comment</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
      newPostContent: '',
      newCommentContent: ''
    }
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      axios.get('/api/posts/')
        .then(response => {
          this.posts = response.data;
        })
        .catch(error => {
          console.error('Error fetching posts:', error);
        });
    },
    createPost() {
      axios.post('/api/posts/', { content: this.newPostContent })
        .then(response => {
          this.posts.unshift(response.data);
          this.newPostContent = '';
        })
        .catch(error => {
          console.error('Error creating post:', error);
        });
    },
    createComment(postId) {
      axios.post(`/api/comments/`, { post: postId, content: this.newCommentContent })
        .then(response => {
          const post = this.posts.find(p => p.id === postId);
          post.comments.push(response.data);
          this.newCommentContent = '';
        })
        .catch(error => {
          console.error('Error creating comment:', error);
        });
    }
  }
}
</script>

<style>
/* Add your CSS styles here */
</style>