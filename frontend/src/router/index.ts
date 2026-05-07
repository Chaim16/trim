import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/weight",
    name: "weight",
    component: () => import("../views/WeightView.vue"),
  },
  {
    path: "/food",
    name: "food",
    component: () => import("../views/FoodView.vue"),
  },
  {
    path: "/exercise",
    name: "exercise",
    component: () => import("../views/ExerciseView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;
