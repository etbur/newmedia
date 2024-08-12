<template>
  <section v-if="selected_user">
    <active-user :user="selected_user"></active-user>
    <router-link to="/app/postlist">post</router-link>
    <div class="chat-body" ref="chatBody">
      <div v-for="message in selected_user.messages" class="chat-message" :class="message.sender !== selected_user.username ? 'right': 'left'">
        <div class="actions">
          <span class="dropdown">
            <a href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              ...
            </a>

            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuLink">
              <a class="dropdown-item" href="#" @click="deleteMessage(message)">Delete</a>
              <a class="dropdown-item" href="#" @click="editMessage(message)">Edit</a>
              <a class="dropdown-item" href="#" @click="replyToMessage(message)">Reply</a>
              <a class="dropdown-item" href="#" @click="forwardMessage(message)">Forward</a>
            </div>
          </span>
        </div>
        <div class="text">
          <span>{{ message.text }}</span>
        </div>
        <div class="meta">
          <span>{{ dateHumanize(message.date_time) }}</span>
          <i class="feather icon-check ml-2"></i>
        </div>
      </div>
    </div>

    <div class="chat-bottom">
      <div class="chat-messagebar">
        <form @submit.prevent="sendMessage">
          <div class="input-group">
            <div class="input-group-prepend">
              <a href="#" id="button-addonmic"><i class="feather icon-mic"></i></a>
            </div>
            <div class="input-group-prepend">
              <label for="fileInput" id="button-addonfile" class="file-input-label">
                <i class="feather icon-file"></i> Choose File
              </label>
            </div>
            <input type="file" class="file-input" id="fileInput">
            <input v-model="message" type="text" class="form-control" placeholder="Type a message..." aria-label="Text">
            <div class="input-group-append">
              <a href="#" class="mr-3" id="button-addonlink"><i class="feather icon-paperclip"></i></a>
              <a href="#" id="button-addonsend"><i class="feather icon-send"></i></a>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>

  <section v-else>
    <default-message-window></default-message-window>
  </section>
</template>

<script>
import ActiveUser from "./ActiveUser.vue";
import axios from "../../../../../axios";
import moment from "moment";
import DefaultMessageWindow from "../../../../../components/DefaultMessageWindow.vue";

export default {
  name: "MessageWindow",
  props: ['selected_user'],
  components: {
    'active-user': ActiveUser,
    'default-message-window': DefaultMessageWindow
  },
  data() {
    return {
      message: ''
    }
  },
  data(){
    return {
      postLink: "#",
      yourLink: "https://www.example.com"
    }
  },
  watch: {
    'selected_user.messages': {
      deep: true,
      handler() {
        if (this.$refs.hasOwnProperty('chatBody')) {
          this.scrollDown()
        }
      }
    }
  },
  methods: {
    sendMessage() {
      this.selected_user.messages.push({
        text: this.message,
        read: true,
        date_time: moment().format(),
        sender_id: 'me'
      });
      axios.post('message/', {
        text: this.message,
        receiver: this.selected_user.username
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      }).finally(() => {
        this.message = '';
      });
    },

    dateHumanize(date) {
      return moment(date).fromNow();
    },

    scrollDown() {
      this.$refs.chatBody.scrollTop = this.$refs.chatBody.scrollHeight;
    },

    deleteMessage(message) {
      const index = this.selected_user.messages.indexOf(message);
      if (index !== -1) {
        this.selected_user.messages.splice(index, 1);
      }
    },

    editMessage(message) {
      // Implement the logic to open an edit form for the message
      console.log('Edit message:', message);
    },

    replyToMessage(message) {
      // Implement the logic to initiate a reply to the message
      console.log('Reply to message:', message);
    },

    forwardMessage(message) {
      // Implement the logic to initiate forwarding of the message
      console.log('Forward message:', message);
    }
  }
};
</script>
<style scoped>
.chat-body {
  overflow-y: auto;
}

.chat-message {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.chat-message.right .text {
  align-self: flex-end;
}

.text {
  background-color: #f3f3f3;
  padding: 10px;
  border-radius: 10px;
  max-width: 70%;
  align-self: flex-start;
}

.meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 5px;
  color: #999;
  font-size: 12px;
}

.actions {
  margin-top: 5px;
}

.dropdown-menu {
  min-width: 100px;
}

.dropdown-item {
  display: flex;
  align-items: center;
}

.dropdown-item i {
  margin-right: 5px;
}

.chat-bottom {
  padding: 15px;
  background-color: #f9f9f9;
  border-top: 1px solid #ddd;
}

.chat-messagebar {
  display: flex;
  align-items: center;
}

.input-group {
  width: 100%;
}

.form-control {
  border-radius: 30px;
  border: 1px solid #ddd;
}

#button-addonmic,
#button-addonfile,
#button-addonlink,
#button-addonsend {
  color: #999;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
}

.file-input-label {
  cursor: pointer;
}

.file-input {
  display: none;
}



</style>