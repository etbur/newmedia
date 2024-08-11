<template>
  <form @submit.prevent="submitPost">
    <div class="form-head">
      <a href="index.html" class="logo">
        <img
          src="http://themesbox.in/admin-templates/gappa/html/light/assets/images/logo.svg"
          class="img-fluid"
          alt="logo"
        />
      </a>
    </div>
    <h4 class="text-primary my-4">Create an Account</h4>

    <div class="form-floating mb-3">
      <input
        type="text"
        class="form-control"
        v-model="post.user"
        placeholder="Username"
      />
      <label>Username</label>
    </div>

    <div class="form-floating mb-3">
      <input
        type="text"
        class="form-control"
        v-model="post.content"
        placeholder="Post Content"
      />
      <label>Post Content</label>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <div class="d-grid gap-2">
      <button class="btn btn-success btn-lg btn-block font-18" type="submit">
        Post
      </button>
    </div>
  </form>
</template>

<script>
import axios from "../../axios";
import toastr from "toastr";

export default {
  name: "PostPage",
  data() {
    return {
      post: {
        user: "",
        content: "",
      },
      errorMessage: null,
    };
  },
  methods: {
    async submitPost() {
      try {
        const response = await axios.post("/postfile/", this.post);
        console.log(response);
        toastr.success(response.data.message, "Success");
        this.$router.replace("/postfile/");
      } catch (error) {
        console.log(error.response);
        this.errorMessage = "An error occurred while submitting the post.";
      }
    },
  },
};
</script>

<style scoped></style>