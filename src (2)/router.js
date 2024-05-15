import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
import navbar from './components/navbar.vue'
import activity_create from './components/activity_create.vue'
import activity_manage from './components/activity_manage.vue'
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
    path:'/create',
    name:'activity_create',
    component:activity_create,
  },
  {
      path: '/manage',
      name: 'activity_manage',
      component: activity_manage,
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
