import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; 
import './style.css';
import flag_plugin from './plugins/flags';

const app = createApp(App);
app.use(router); 
app.use(flag_plugin);

app.mount('#app');
