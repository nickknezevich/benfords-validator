import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import './assets/admin.css'
import './assets/app.js'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const toastOptions = {
    timeout: 6000
};

app.use(createPinia())
app.use(router)
app.use(Toast, toastOptions);


app.mount('#app')
