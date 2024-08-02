import './assets/main.css'

import { createApp } from 'vue'
// import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router'
import store from "./store";

const app = createApp(App)
app.use(store)
app.use(router)

app.mount('#app')

// const pinia = createPinia();

new Vue({
  render: (h) => h(App),
  pinia,
}).$mount('#app');