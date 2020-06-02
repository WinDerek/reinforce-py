<template>
  <div class="grid-world">
    <div class="grid-container">
      <div class="grid-row" v-for="i in 10" v-bind:key="i">
        <grid
          v-for="j in 10" v-bind:key="j"
          v-model="gridDataArray[(i - 1) * 10 + j - 1]"
          :selected="selectedArray[(i - 1) * 10 + j - 1]"
          v-on:on-grid-clicked="onGridClicked"
          :current="(i - 1) * 10 + j - 1 == currentIndex" />
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
    selectedIndex: {
      type: Number,
      required: true
    },
    wallIndexArray: {
      type: Array,
      required: true
    },
    // The index of the current state
    currentIndex: {
      type: Number,
      required: false,
      default: -1
    }
  },
  components: { Grid },
  data: function () {
    return {
    }
  },
  computed: {
    selectedArray () {
      var array = [];
      for (var i = 0; i < 10 * 10; i++) {
        array.push(this.selectedIndex == i);
      }
      return array;
    }
  },
  created () {
  },
  methods: {
    onGridClicked: function (gridIndex, selected) {
      this.$emit('on-selected-index-updated', gridIndex, selected);
    }
  }
};
</script>

<style scoped>
.grid-world {
  font-family: "roboto";
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  margin: auto;
}

.grid-container {
  width: 65vh;
  height: 65vh;
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
