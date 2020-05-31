<template>
  <div class="home">
    <h1>Welcome to Grid World !</h1>

    <el-button
      @click="hello"
      style="font-family: 'monaco';">
      Policy evaluation (1 sweep)
    </el-button>

    <GridWorld
      :grid-data-array="gridDataArray"
      :wall-index-array="wallIndexArray" />
  </div>
</template>

<script>
// @ is an alias to /src
import GridWorld from '@/components/GridWorld.vue';
import { AXIOS } from '../util/http-common.js';

export default {
  name: 'Home',
  components: {
    GridWorld,
  },
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
            goal: false,
            gridIndex: i * 10 + j,
            stateValue: 0.0,
            reward: 0.0,
            policy: [ 0.25, 0.25, 0.25, 0.25 ]
          }
        );
      }
    }

    // Set the walls
    this.wallIndexArray.forEach(wallIndex => this.gridDataArray[wallIndex].wall = true);

    // Set special reward
    this.gridDataArray[55].reward = 1.0;

    // Set the goal
    this.gridDataArray[55].goal = true;
  },
  methods: {
    hello() {
      AXIOS.get('/hello')
        .then(response => {
          console.log(response.data)

          // this.loading = false

          // MyNoty.success('查询成功！')
        })
        .catch(e => {
          console.log(e)

          // this.loading = false

          // MyNoty.error('查询失败，请检查重试')
        })
    }
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>
