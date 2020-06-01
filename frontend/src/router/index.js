import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import GridWorldDp from '../views/GridWorldDp.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/grid_world/dp',
    name: 'GridWorldDp',
    component: GridWorldDp,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
