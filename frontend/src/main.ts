import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from "../src/plugins/vuetify.ts"; // Vuetify をインポート
import './assets/tailwind.css'
import '@mdi/font/css/materialdesignicons.css'

const app = createApp(App);

app.use(router);
app.mount('#app');
app.use(vuetify); // Vuetify を適用

