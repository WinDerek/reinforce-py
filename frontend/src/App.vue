<template>
  <div id="app">
    <my-menu></my-menu>
    <router-view/>
  </div>
</template>

<script>
import MyMenu from '@/components/MyMenu.vue';

export default {
  name: 'App',
  components: {
    MyMenu
  },
  data: function () {
    return {
    }
  },
  created () {
  }
};
</script>

<style>
@font-face {
  font-family: "monaco";
  src: url("./assets/fonts/monaco.ttf");
}

@font-face {
  font-family: "roboto";
  src: url("./assets/fonts/roboto.ttf");
}

h1 {
  font-family: "roboto";
  font-size: 2.0rem;
  text-align: center;
  text-shadow: 0 1px 1px #000;
  color: #6c7a89;
}

p {
  font-family: "roboto";
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  width: 100vw;
  height: 100vh;

  display: flex;
  flex-direction: column;
  align-items: stretch;
}
</style>
