import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
import schedule from './components/calendar.vue'
import navbar from './components/navbar.vue'
import activity_create from './components/activity_create.vue'
import activity_manage from './components/activity_manage.vue'
import activity_person from './components/activity_person.vue'
import activity_resources from './components/activity_resources.vue'
import activity_goal from './components/activity_goal.vue'
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
    path: '/schedule', 
    name:'schedule',
    component:schedule,
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
  {
      path: '/person',
      name: 'activity_person',
      component: activity_person,
  },
  {
      path: '/resources',
      name: 'activity_resources',
      component: activity_resources,
  },
  {
      path: '/goal',
      name: 'activity_goal',
      component: activity_goal,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
