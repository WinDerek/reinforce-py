<template>
  <div class="grid">
    <div class="state-value">{{gridData.stateValue.toFixed(2)}}</div>

    <svg class="arrow" height="80%" width="80%" :view-box.camel="viewBoxStr">
        <line
          fill="none"
          stroke="#336e7b"
          stroke-width="4"
          stroke-linecap="round"
          stroke-linejoin="round"
          :x1="pointArray[0][0]"
          :y1="pointArray[0][1]"
          :x2="pointArray[2][0]"
          :y2="pointArray[2][1]" />
        <line
          fill="none"
          stroke="#336e7b"
          stroke-width="4"
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
      type: Object, // gridIndex: 99, stateValue: 0.0, policy: [ 0.25, 0.25, 0.25, 0.25]
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
  flex-grow: 1;

  border-radius: 4px;
  border: 2px solid #000000;
  margin: 2px;
}

.state-value {
  position: relative;
  top: 2px;
  left: 2px;
  font-family: "monaco";
  font-size: 0.8em;
}

.arrow {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translateX(-50%);
}
</style>
