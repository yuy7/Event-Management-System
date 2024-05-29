import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
import chat_room from "./components/chat_room.vue";
import schedule from './components/calendar.vue'
import navbar from './components/navbar.vue'
import activity_create from './components/activity_create.vue'
import activity_manage from './components/activity_manage.vue'
import activity_person from './components/activity_person.vue'
import activity_resources from './components/activity_resources.vue'
import activity_goal from './components/activity_goal.vue'
import activity_detail from './components/activity_detail.vue'
import activity_invite from './components/activity_invite.vue'
import activity_notifications from './components/activity_notifications.vue'
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
  {
	  path: '/detail',
	  name: 'activity_detail',
	  component: activity_detail,
  },
  {
  	  path: '/invite',
  	  name: 'activity_invite',
  	  component: activity_invite,
  },
  {
  	  path: '/notifications',
  	  name: 'activity_notifications',
  	  component: activity_notifications,
  },
  {
    path:'/budget',
    name:'budget',
    component: ()=>import('./components/budget.vue'),
  },
  {
    path: '/chat-room',
    name: 'chat-room',
    component: chat_room
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
