import './assets/main.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import Rekisteröidy from './components/rekisteröidy.vue'
import Kirjaudu from './components/kirjaudu.vue'
import Protected from './components/Protected.vue'
import axios from 'axios'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Rekisteröidy },
        { path: '/kirjaudu', component: Kirjaudu },
        { path: '/protected', component: Protected, meta: { requiresAuth: true } },
    ]
});

const app = createApp(App)

app.use(router);

router.beforeEach((to, from, next) => {
    // Quick guard: if route needs auth, call `/me` and proceed on success.
    if (!to.meta?.requiresAuth) return next()

    axios.get('http://127.0.0.1:5000/me', { withCredentials: true })
        .then(() => next())
        .catch(() => next('/'))
})

app.mount('#app')

