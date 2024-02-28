import { createRouter, createWebHashHistory } from "vue-router";

const Home = () => import("@/views/Home.vue");

const HomeContent = () => import("@/views/HomeContent.vue");


const base_url = "/";

const routes = [
  {
    path: base_url,
    name: "Home",
    component: Home,
    children: [
      {
        path: "homecontent",
        name: "Home Content",
        component: HomeContent,
        meta: {},
      }
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(), // createWebHistory(base_url_env_history),
  // base: base_url_env_history,
  routes,
});

export default router;

