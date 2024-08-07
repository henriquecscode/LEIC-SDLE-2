import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('../views/Home.vue')
        },
        {
            path: '/timeline/:user/:port',
            name: 'Timeline',
            component: () => import('../views/Timeline.vue'),
        },
    ]
})

export default router