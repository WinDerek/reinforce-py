<template>
  <div class="grid-world">
    <div class="grid-container">
      <div class="grid-row" v-for="i in 10">
        <div class="grid" v-for="i in 10">{{ i }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GridWorld',
  props: {
  },
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
