import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
const routes = [
  { 
    path: '/login', 
    component: login
  },
  {
    path: '/register', 
    component: register
  },
  {
    path: '/forget_password', 
    component: forget_password
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router