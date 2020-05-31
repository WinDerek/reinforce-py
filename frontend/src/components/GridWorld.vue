<template>
  <div class="grid-world">
    <div class="grid-container">
      <div class="grid-row" v-for="i in 10">
        <grid v-for="j in 10" v-model="gridDataArray[(i - 1) * 10 + j - 1]" />
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
    }
  },
  created () {
    for (var i = 0; i < 10; i++) {
      for (var j = 0; j < 10; j++) {
        this.gridDataArray.push(
          {
            gridIndex: i * 10 + j,
            actionArray: [ 0, 1, 2, 3 ]
          }
        );
      }
    }
  }
};
</script>

<style scoped>
.grid-world {
  font-family: "roboto";
  box-sizing: border-box;
  width: 40%;
  margin: 0 auto;
}

.grid-container {
  width: 40vw;
  height: 40vw;
  background-color: #2980b9;

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

  background-color: #f62459;
}

.grid {
  align-self: stretch;
  flex-grow: 1;
}
</style>
