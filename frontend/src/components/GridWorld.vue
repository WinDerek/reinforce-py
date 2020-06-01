<template>
  <div class="grid-world">
    <div class="grid-container">
      <div class="grid-row" v-for="i in 10" v-bind:key="i">
        <grid v-for="j in 10" v-bind:key="j" v-model="gridDataArray[(i - 1) * 10 + j - 1]" />
      </div>
    </div>
  </div>
</template>

<script>
import Grid from './Grid';

export default {
  name: 'GridWorld',
  model: {
    prop: "gridDataArray"
  },
  props: {
    gridDataArray: {
      type: Array,
      required: true
    },
    wallIndexArray: {
      type: Array,
      required: true
    }
  },
  components: { Grid },
  data: function () {
    return {
    }
  },
  created () {
  }
};
</script>

<style scoped>
.grid-world {
  font-family: "roboto";
  box-sizing: border-box;
  height: 80%;
  margin: 0 auto;
}

.grid-container {
  width: 75vh;
  height: 75vh;
  padding: 12px;
  background-color: #ffffff;
  border: 6px solid #2c3e50;

  margin: auto;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}

.grid-row {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  width: 100%;
  height: 10%;
}
</style>
