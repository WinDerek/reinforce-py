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
    path: '/grid-world/dp',
    name: 'GridWorldDp',
    component: GridWorldDp,
  },
  {
    path: '/grid-world/td',
    name: 'GridWorldTd',
    component: GridWorldTd,
  },
  {
    path: '/puck-world/dqn',
    name: 'PuckWorldDqn',
    component: PuckWorldDqn
  },
  {
    path: '/water-world/dqn',
    name: 'WaterWorldDqn',
    component: WaterWorldDqn
  },
];

const router = new VueRouter({
  routes,
});

export default router;
