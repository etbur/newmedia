<template>
  <div class="facebook-layout">
    <div class="header">
      <h1>Header</h1>
      <div class="header-icons">
        <router-link to="/app"><a href="#"><i class="fas fa-envelope"></i></a></router-link>
        <a href="#"><i class="fas fa-bell"></i></a>
        <a href="#"><i class="fas fa-user-friends"></i></a>
        <a href="#"><i class="fas fa-users"></i></a>
        <a href="#"><i class="fas fa-user-circle"></i></a>
      </div>
    </div>

    <div class="main-container">
      <div class="sidebar">
        <button class="menu-toggle-btn" @click="toggleMenu">
          <i class="fas fa-bars"></i>
        </button><br><br><br><br>
        <ul class="menu-items" :class="{ 'show-menu': showMenu }">
        <router-link to="/friends"><li class="menu-item"><i class="fas fa-user-friends"></i> Add Friend</li></router-link>
          <router-link to="/app"><li class="menu-item"><i class="fas fa-envelope"></i> Message</li></router-link>
          <router-link to="/gruop"><li class="menu-item"><i class="fas fa-users"></i> Group</li></router-link>
          <router-link to="/markat"><li class="menu-item"><i class="fas fa-bullhorn"></i> Marketing</li></router-link>
          <router-link to="/game"><li class="menu-item"><i class="fas fa-gamepad"></i> Game</li></router-link>
          <router-link to="/event"><li class="menu-item"><i class="fas fa-calendar-alt"></i> Event</li></router-link>
          <router-link to="/job"><li class="menu-item"><i class="fas fa-briefcase"></i> Job</li></router-link>
          <router-link to="/design"><li class="menu-item"><i class="fas fa-paint-brush"></i> Design</li></router-link>
          <router-link to="/signlng"><li class="menu-item"><i class="fas fa-sign-language"></i> Sign Language</li></router-link>
          <router-link to="/vtt"><li class="menu-item"><i class="fas fa-microphone"></i> Voice to Text</li></router-link>
          <router-link to="/advert"><li class="menu-item"><i class="fas fa-microphone"></i> Advert Here</li></router-link>
          <li class="menu-item"><i class="fas fa-ellipsis-h"></i> Other</li>
        <router-link to="/faq"><li class="menu-item"><i class="fas fa-users"></i> FAQ</li></router-link>
        <router-link to="/new"><li class="menu-item"><i class="fas fa-bullhorn"></i> New</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
        <router-link to="/privacy"><li class="menu-item"><i class="fas fa-lock"></i> Privacy Policy</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
         
          
          <!-- Sidebar menu items -->
        </ul>
      </div>

      <div class="jop-list">
        <h2>Job Openings</h2>
        <div class="job-item" v-for="job in jobs" :key="job.id">
          <h3>{{ job.title }}</h3>
          <p>{{ job.description }}</p>
          <p>{{ job.company }}</p>
          <p>{{ job.location }}</p>
          <p>{{ job.salary }}</p>
          <button>Apply</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMenu: false,
      jobs: [
        {
          id: 1,
          title: 'Software Engineer',
          description: 'Develop and maintain web applications.',
          company: 'ABC Inc.',
          location: 'New York, NY',
          salary: '$80,000 - $100,000'
        },
        {
          id: 2,
          title: 'Marketing Manager',
          description: 'Develop and execute marketing strategies.',
          company: 'XYZ Corp.',
          location: 'Los Angeles, CA',
          salary: '$60,000 - $80,000'
        },
        {
          id: 3,
          title: 'UX Designer',
          description: 'Design user-friendly interfaces.',
          company: 'EFG LLC',
          location: 'Chicago, IL',
          salary: '$70,000 - $90,000'
        }
      ]
    }
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
    }
  }
}
</script>

<style scoped>
/* Add your custom styles here */
</style>