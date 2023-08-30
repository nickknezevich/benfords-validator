import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { VDataTable } from 'vuetify/labs/VDataTable'
import '@vuepic/vue-datepicker/dist/main.css'
import VueDatePicker from '@vuepic/vue-datepicker'

const customDarkheme = {
    dark: true,
    colors: {
      background: '#292626',
      surface: '#292626',
      primary: '#fff',
      'primary-darken-1': '#3700B3',
      secondary: '#03DAC6',
      'secondary-darken-1': '#018786',
      error: '#B00020',
      info: '#2196F3',
      success: '#4CAF50',
      warning: '#FB8C00',
      anchor: '#8c9eff'
    },
  }

const vuetify = createVuetify({
  components: {
    ...components,
    VDataTable
  },
  directives,
  theme: {
    defaultTheme: 'customDarkheme',
    themes: {
        customDarkheme,
    },
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.component('VueDatePicker', VueDatePicker);

app.mount('#app')
