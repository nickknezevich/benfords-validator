import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"
import "bootstrap"


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
