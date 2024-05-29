import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import mitt from 'mitt'
import axios from 'axios';

axios.defaults.withCredentials = true;

const app=createApp(App)
app.config.globalProperties.emitter = mitt()
app.use(router)
app.mount('#app')

