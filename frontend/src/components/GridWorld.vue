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
  props: {
  },
  components: { Grid },
  data: function () {
    return {
      gridDataArray: [],
      wallIndexArray: [ 21, 22, 23, 24, 26, 27, 28, 34, 44, 54, 64, 74 ]
    }
  },
  created () {
    for (var i = 0; i < 10; i++) {
      for (var j = 0; j < 10; j++) {
        this.gridDataArray.push(
          {
            wall: false,
            gridIndex: i * 10 + j,
            stateValue: 0.0,
            policy: [ 0.25, 0.25, 0.25, 0.25 ]
          }
        );
      }
    }

    this.wallIndexArray.forEach(wallIndex => this.gridDataArray[wallIndex].wall = true);
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
  width: 80vh;
  height: 80vh;
  padding: 12px;
  background-color: #ececec;
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
