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
          <router-link to="/postfile"><li class="menu-item"><i class="fas fa-user-friends"></i>post file</li></router-link>  
          <router-link to="/app"><li class="menu-item"><i class="fas fa-envelope"></i> Message</li></router-link>
          <router-link to="/group"><li class="menu-item"><i class="fas fa-users"></i> Group</li></router-link>
          <router-link to="/markat"><li class="menu-item"><i class="fas fa-bullhorn"></i> Marketing</li></router-link>
          <router-link to="/game"><li class="menu-item"><i class="fas fa-gamepad"></i> Game</li></router-link>
          <router-link to="/event"><li class="menu-item"><i class="fas fa-calendar-alt"></i> Event</li></router-link>
          <router-link to="/job"><li class="menu-item"><i class="fas fa-briefcase"></i> Job</li></router-link>
          <router-link to="/design"><li class="menu-item"><i class="fas fa-paint-brush"></i> Design</li></router-link>
          <router-link to="/signlng"><li class="menu-item"><i class="fas fa-sign-language"></i> Sign Language</li></router-link>
          <router-link to="/vtt"><li class="menu-item"><i class="fas fa-microphone"></i> Voice to Text</li></router-link>
          <router-link to="/advert"><li class="menu-item"><i class="fas fa-microphone"></i> Advert Here</li></router-link>
          <li class="menu-item"><i class="fas fa-ellipsis-h"></i> Other</li>
        <router-link to="/yourfollowers"><li class="menu-item"><i class="fas fa-users"></i> you Followers</li></router-link> 

        <router-link to="/student"><li class="menu-item"><i class="fas fa-users"></i>student</li></router-link> 

<router-link to="/std"><li class="menu-item"><i class="fas fa-users"></i>std</li></router-link> 

        <router-link to="/faq"><li class="menu-item"><i class="fas fa-users"></i> FAQ</li></router-link>
        <router-link to="/new"><li class="menu-item"><i class="fas fa-bullhorn"></i> New</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
        <router-link to="/privacy"><li class="menu-item"><i class="fas fa-lock"></i> Privacy Policy</li></router-link>
        <router-link to="/help"><li class="menu-item"><i class="fas fa-gamepad"></i> Help</li></router-link>
         
          
        </ul>
      </div>


       <div class="post-list">
      <div class="post">
        <img src="/src/assets/logo.png" alt="Image Post 1">
        <div class="post-actions">
          <span class="action"><i class="far fa-thumbs-up"></i> Like</span>
          <span class="action"><i class="far fa-comment"></i> Comment</span>
          <span class="action"><i class="far fa-share-square"></i> Share</span>
          <span class="action"><i class="far fa-bookmark"></i> Save</span>
          <span class="action"><i class="fas fa-ellipsis-h"></i></span>
        </div>
      </div>
      <div class="post">
        <img src="/src/assets/logo.png  " alt="Image Post 2">
        <div class="post-actions">
          <span class="action"><i class="far fa-thumbs-up"></i> Like</span>
          <span class="action"><i class="far fa-comment"></i> Comment</span>
          <span class="action"><i class="far fa-share-square"></i> Share</span>
          <span class="action"><i class="far fa-bookmark"></i> Save</span>
          <span class="action"><i class="fas fa-ellipsis-h"></i></span>
        </div>
      </div>
      <!-- Add more post items as needed -->
    </div>
    
    <div class="sponsored">
      <div class="sponsored-content">
        <h3 class="sponsored-title">Sponsored Ad</h3>
        <img src="/src/assets/icons/girl.svg" alt="Sponsored Ad">
      </div>
    </div>

    </div>
    
  </div>
</template>

<style>
.facebook-layout {
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #4267B2;
  color: #fff;
  padding: 20px;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;

}

.header-icons a {
  color: #fff;
  margin-left: 10px;
  text-decoration: none;
}

.main-container {
  display: flex;
}

.sidebar {
  background-color: #f0f2f5;
  width: 300px;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
    overflow-y: auto;
}

.collapsed .menu-item {
  display: none;
}

.post-list {
  margin-left: 320px;
  padding: 20px;
}

.post {
  background-color: #ffffff;
  padding: 10px;
  margin-bottom: 20px;
}

.post img {
  width: 100%;
  height: auto;
}

.post-actions {
  margin-top: 10px;
}

.action {
  display: inline-block;
  margin-right: 10px;
  color: #606770;
  font-size: 14px;
}

.action i {
  margin-right: 5px;
}

/* sponserd*/
/* Existing styles */

.sponsored {
  position: sticky;
  top: 0;
  width: 400px;
  margin-left: 250px;
}

.sponsored-content {
  background-color: #f0f2f5;
  padding: 10px;
  font-size: 14px;
}

.sponsored-title {
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: bold;
}

.sponsored-content img {
  width: 100%;
  height: auto;
}
/* Media Query for Small Devices */
@media (max-width: 768px) {
  .header {
    padding: 10px;
     position: sticky;
  top: 0;
  z-index: 100;
  }

  .header h1 {
    font-size: 16px;
  }

  

  .main-container {
    flex-direction: column;
    align-items: center;
  }

  .sidebar {
    width: 100%;
    max-width: 50px;
    padding: 10px;
  }

  .post-list {
    padding: 1px;
    margin-left:0;
  }
}

sidebar {
  background-color: #f0f2f5;
  width: 300px;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
}

.menu-items {
  list-style-type: none;
  padding: 0;
}

.menu-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.menu-item i {
  margin-right: 5px;
}

.show-menu .menu-items {
  display: block;
}
</style>