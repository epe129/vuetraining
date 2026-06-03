import './assets/main.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import Rekisteröidy from './components/rekisteröidy.vue'
import Kirjaudu from './components/kirjaudu.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Rekisteröidy },
        { path: '/kirjaudu', component: Kirjaudu },
    ]
});


const app = createApp(App)

app.use(router);

app.mount('#app')

