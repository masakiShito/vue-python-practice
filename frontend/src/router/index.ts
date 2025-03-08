import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import RoomPage from "../pages/room.vue"; // 追加

const routes = [
  { path: "/", component: HomePage },
  { path: "/room", component: RoomPage } // 追加
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
