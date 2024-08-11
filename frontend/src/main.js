import './assets/main.css'

import { createApp } from 'vue'
// import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router'
import store from "./store";
import 'toastr/build/toastr.min.css'; // Import Toastr CSS
import toastr from 'toastr';
const app = createApp(App)
app.config.globalProperties.$toastr = toastr; 
app.use(store)
app.use(router)

app.mount('#app')

// const pinia = createPinia();

new Vue({
  render: (h) => h(App),
  pinia,
}).$mount('#app');