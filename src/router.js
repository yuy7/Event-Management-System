import { createRouter, createWebHistory } from 'vue-router'
import login from './components/login.vue'
import register from './components/register.vue'
import forget_password from './components/forget_password.vue'
import budget from './components/budget.vue'
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
import activity_member from './components/activity_member.vue'
import activity_history from './components/activity_history.vue'
import activity_final from './components/activity_final.vue'
import class_manage from './components/class_manage.vue'
const routes = [
	{
		path:'/',
		redirect:'/login'
	},
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
  // {
  //   path: '/chat-room',
  //   name: 'chat-room',
  //   component: chat_room
  // },
  {
    path:'/budget',
    name:'budget',
    component: budget,
  },
  {
    path:'/member',
    name:'member',
    component: activity_member,
  },
  {
    path:'/history',
    name:'history',
    component: activity_history,
  },
  {
    path:'/final',
    name:'final',
    component: activity_final,
  },
  {
    path:'/class',
    name:'class_manage',
    component: class_manage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
