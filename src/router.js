import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
import calendar from './components/calendar.vue'
const routes = [
  { 
    path: '/login', 
    name:'login',
    component:login, 
  },
  {
    path: '/register', 
    name:'register',
    component:register,
  },
  {
    path: '/forget_password', 
    name:'forget_password',
    component:forget_password,
  },
  {
    path: '/calendar', 
    name:'calendar',
    component:calendar,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
