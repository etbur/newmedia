<template>
  <div class="chat-head">
    <div class="row justify-content-between">
      <div class="col-6">
        <ul class="list-unstyled mb-0">
          <li class="media">
            <div v-if="user.online" class="user-status"></div>
            <img src="/src/assets/icons/girl.svg" alt="">
            <div class="media-body">
              <h5>{{ user.name }}</h5>
              <p class="mb-0">{{ user.online ? 'Online' : 'Offline' }}</p>
            </div>
          </li>
        </ul>
      </div>
      <div class="col-6">
        <ul class="list-inline float-end mb-0">
          <li class="list-inline-item">
            <button @click="makeCall" type="button" class="">
              <img src="/src/assets/icons/phone.svg" alt="">
            </button>
          </li>

          <li class="list-inline-item">
            <button @click="makeCall" type="button" class="">
              <img src="/src/assets/icons/video.svg" alt="">
            </button>
          </li>

          <li class="list-inline-item dropdown">
            <button type="button" class="dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <img src="/src/assets/icons/more-vertical.svg" alt="">
            </button>
            <div class="dropdown-menu">
              <!-- Dropdown menu items -->
              <a class="dropdown-item" href="#">View Profile</a>
              <a class="dropdown-item" href="#">Download Report History</a>
              <a class="dropdown-item" href="#">Block User</a>
              <a class="dropdown-item" href="#">Clear History</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ActiveUser",
  props: ['user'],
  methods: {
    makeCall() {
      let routeData = this.$router.resolve({
        name: 'callerView',
        params: {
          username: this.$store.state.activeUser.username,
          receiver: this.user.username,
        },
        query: {
          display: JSON.stringify({
            username: this.user.username,
            photo: this.user.photo,
            name: this.user.name,
            online: this.user.online
          })
        }
      });
      window.open(routeData.href, '_blank', 'popup,height=650,width=550,resizable=0,location=no,toolbar=no,menubar=no,resizable=no')
      // window.open(routeData.href, '_blank')
    }
  }
}
</script>

<style scoped>
.dropdown-menu {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-menu a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-menu a:hover {
  background-color: #f1f1f1;
}

.dropdown:hover .dropdown-menu {
  display: block;
}
</style>