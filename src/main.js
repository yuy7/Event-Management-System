import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import mitt from 'mitt'
import axios from 'axios';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

axios.defaults.withCredentials = true;

const app=createApp(App)
app.config.globalProperties.emitter = mitt()
app.use(ElementPlus)
app.use(router)
app.mount('#app')
