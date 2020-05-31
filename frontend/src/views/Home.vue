<template>
  <div class="home">
    <h1>Welcome to Grid World !</h1>

    <el-button
      @click="hello"
      style="font-family: 'monaco';">
      GET
    </el-button>

    <GridWorld />
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
