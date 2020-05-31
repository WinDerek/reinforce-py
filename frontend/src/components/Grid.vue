<template>
  <div class="grid" v-bind:class="{ wall: gridData.wall, goal: gridData.goal }">
    <div v-if="!gridData.wall" class="state-value">{{gridData.stateValue.toFixed(2)}}</div>

    <div v-if="!gridData.wall && (gridData.reward != 0.0)" class="reward">R={{gridData.reward.toFixed(1)}}</div>

    <svg v-if="!gridData.wall" class="arrow" height="80%" width="80%" :view-box.camel="viewBoxStr">
        <line
          fill="none"
          stroke="#2e3131"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
          :x1="pointArray[0][0]"
          :y1="pointArray[0][1]"
          :x2="pointArray[2][0]"
          :y2="pointArray[2][1]" />
        <line
          fill="none"
          stroke="#2e3131"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
          :x1="pointArray[1][0]"
          :y1="pointArray[1][1]"
          :x2="pointArray[3][0]"
          :y2="pointArray[3][1]" />
        <circle :cx="borderLength / 2.0" :cy="borderLength / 2.0" r="4" stroke="#ffffff" fill="#ffffff" />
        Sorry, your browser does not support inline SVG.
    </svg>
  </div>
</template>

<script>
export default {
  name: 'Grid',
  model: {
    prop: 'gridData',
    event: 'onGridClicked'
  },
  props: {
    gridData: {
      type: Object, // gridIndex: 99, wall: false, goal: false, stateValue: 0.0, reward: 1.0, policy: [ 0.25, 0.25, 0.25, 0.25]
      required: true
    }
  },
  data: function () {
    return {
      borderLength: 100,
      arrowWidth: 10
    }
  },
  computed: {
    viewBoxStr () {
        return `0 0 ${this.borderLength} ${this.borderLength}`;
    },
    pointArray () {
      var pointArr = [];

      var a = this.borderLength / 2.0;

      pointArr.push([a, a - a * this.gridData.policy[0]])
      pointArr.push([a + a * this.gridData.policy[1], a])
      pointArr.push([a, a + a * this.gridData.policy[2]])
      pointArr.push([a - a * this.gridData.policy[3], a])

      return pointArr;
    }
  },
  methods: {
    onGridClicked: function (index) {
      this.$emit('onGridClicked', index)
    }
  }
}
</script>

<style scoped>
.grid {
  align-self: stretch;
  width: 10%;
  position: relative;

  border-radius: 6px;
  border: 1px solid #6c7a89;
  margin: 2px;
  background-color: #ececec;
}

.grid:hover {
  cursor: pointer;
}

.wall {
  background-color: #6c7a89;
}

.goal {
  background-color: #7befb2;
}

.state-value {
  position: absolute;
  top: 2px;
  left: 2px;
  font-family: "monaco";
  font-size: 0.8em;
}

.reward {
  position: absolute;
  bottom: 2px;
  right: 2px;
  font-family: "monaco";
  font-size: 0.4em;
  color: #f15a22;
}

.arrow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}
</style>
