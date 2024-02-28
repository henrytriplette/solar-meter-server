import { createRouter, createWebHashHistory } from "vue-router";

const Home = () => import("@/views/Home.vue");
const Settings = () => import("@/views/Settings.vue");

const SettingsTriggers = () => import("@/views/SettingsTriggers.vue");


const base_url = "/";

const routes = [
  {
    path: base_url,
    name: "Home",
    component: Home,
    meta: {},
  },
  {
    path: base_url + 'settings',
    name: "Settings",
    component: Settings,
    children: [
      {
        path: "settings-triggers",
        name: "Settings Triggers",
        component: SettingsTriggers,
        meta: {},
      }
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;

