import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
const routes = [
  { 
    path: '/login', 
    component: login
  },
  {
    path: '/register', 
    component: register
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router