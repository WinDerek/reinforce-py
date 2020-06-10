import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import GridWorldDp from '../views/GridWorldDp.vue';
import GridWorldTd from '../views/GridWorldTd.vue';
import PuckWorldDqn from '../views/PuckWorldDqn.vue';
import WaterWorldDqn from '../views/WaterWorldDqn.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Home,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/grid_world/dp',
    name: 'GridWorldDp',
    component: GridWorldDp,
  },
  {
    path: '/grid_world/td',
    name: 'GridWorldTd',
    component: GridWorldTd,
  },
  {
    path: '/puck_world/dqn',
    name: 'PuckWorldDqn',
    component: PuckWorldDqn
  },
  {
    path: '/water_world/dqn',
    name: 'WaterWorldDqn',
    component: WaterWorldDqn
  },
];

const router = new VueRouter({
  routes,
});

export default router;
