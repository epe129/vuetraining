import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Form from './components/Form.vue'

const app = createApp(App)

app.component('Form', Form)

app.mount('#app')

