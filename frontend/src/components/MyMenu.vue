<template>
  <div class="my-menu">
    <div class="menu-item left">
      <div
        class="white organization-label"
        style="position: absolute;top: 50%;transform: translateY(-50%);">REINFORCEpy</div>
    </div>

    <router-link to="/water_world/dqn" class="menu-item right white link-label">
      <div class="link-text">Water World: DQN</div>
    </router-link>
    <router-link to="/puck_world/dqn" class="menu-item right white link-label">
      <div class="link-text">Puck World: DQN</div>
    </router-link>
    <router-link to="/grid_world/td" class="menu-item right white link-label">
      <div class="link-text">Grid World: TD</div>
    </router-link>
    <router-link to="/grid_world/dp" class="menu-item right white link-label">
      <div class="link-text">Grid World: DP</div>
    </router-link>
    <router-link to="/home" class="menu-item right white link-label">
      <div class="link-text">Home</div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'MyMenu',
  props: {},
  data: function () {
    return {}
  },
  methods: {}
}
</script>

<style scoped>
.my-menu {
  padding: 0;
  margin: 0;
  overflow: hidden;
  width: 100%;
  position: relative;
  background-color: #1e8bc3;
}

.white {
  color: white;
}

.left {
  float: left;
}

.organization-label {
  font-size: 1.0rem;
  font-family: "roboto" !important;
  margin-left: 1rem;
  user-select: none;
  padding: 0.3rem;
  border: #ffffff solid 1px;
  border-radius: 1000rem;
}

.right {
  float: right;
}

.menu-item {
  margin: 8px;
}

.link-label {
  text-align: center;
  text-decoration: none;
  display: inline-block;
  border: 1px solid transparent;
}

.link-text {
  font-size: 1.0rem;
  font-family: "roboto";
  padding: 6px 10px;
}

.link-label:hover {
  border: 1px solid #ffffff;
  background-color: #2574a9;
  transition: border-color 0.1s;
}
</style>
