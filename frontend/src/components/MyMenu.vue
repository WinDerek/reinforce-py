<template>
  <div class="my-menu">
    <div class="menu-item left">
      <div
        class="white organization-label"
        style="position: absolute;top: 50%;transform: translateY(-50%);">REINFORCEpy</div>
    </div>

    <router-link to="/water-world/dqn" class="menu-item right white link-label" :class="{ selected: selectedIndex === 5 }" v-on:click.native="selectedIndex = 5">
      <div class="link-text">Water World: DQN</div>
    </router-link>
    <router-link to="/puck-world/dqn" class="menu-item right white link-label" :class="{ selected: selectedIndex === 4 }" v-on:click.native="selectedIndex = 4">
      <div class="link-text">Puck World: DQN</div>
    </router-link>
    <router-link to="/grid-world/dbs" class="menu-item right white link-label" :class="{ selected: selectedIndex === 3 }" v-on:click.native="selectedIndex = 3">
      <div class="link-text">Grid World: DBS</div>
    </router-link>
    <router-link to="/grid-world/td" class="menu-item right white link-label" :class="{ selected: selectedIndex === 2 }" v-on:click.native="selectedIndex = 2">
      <div class="link-text">Grid World: TD</div>
    </router-link>
    <router-link to="/grid-world/dp" class="menu-item right white link-label" :class="{ selected: selectedIndex === 1 }" v-on:click.native="selectedIndex = 1">
      <div class="link-text">Grid World: DP</div>
    </router-link>
    <router-link to="/home" class="menu-item right white link-label" :class="{ selected: selectedIndex === 0 }" v-on:click.native="selectedIndex = 0">
      <div class="link-text">Home</div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'MyMenu',
  props: {
    selectedIndex: {
      type: Number,
      required: false,
      default: 0
    },
  },
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

.link-text:hover {
  background-color: #2574a9;
}

.selected {
  border: 1px solid #ffffff;
  background-color: #2574a9;
  transition: border-color 0.1s;
}
</style>
