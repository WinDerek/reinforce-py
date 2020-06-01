<template>
  <div class="grid" :class="{ wall: gridData.wall, goal: gridData.goal }" :style="{ backgroundColor: backgroundColor }">
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
      arrowWidth: 10,
      zeroColor: "#ececec",
      positiveColor: "#00ff00",
      negativeColor: "#ff0000",
      wallColor: "#6c7a89",
      stateValueUpperBound: 3.0
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
    },
    backgroundColor () {
      var stateValue = this.gridData.stateValue;
      var wall = this.gridData.wall;
      
      if (wall) {
        return this.wallColor;
      }

      if (stateValue == 0.0) {
        return this.zeroColor;
      } else if (stateValue > 0.0) {
        stateValue = Math.min(stateValue, this.stateValueUpperBound);
        var ratio = stateValue / this.stateValueUpperBound;
        var aStr = Math.round(ratio * 255).toString(16);
        return this.positiveColor + aStr;
      } else {
        stateValue = Math.max(stateValue, -this.stateValueUpperBound);
        var ratio = -stateValue / this.stateValueUpperBound;
        var aStr = Math.round(ratio * 255).toString(16);
        return this.negativeColor + aStr;
      }
    }
  },
  methods: {
    onGridClicked: function (index) {
      this.$emit('onGridClicked', index)
    },
    rgbToHex: function (r, g, b) {
      r = r.toString(16);
      g = g.toString(16);
      b = b.toString(16);

      if (r.length == 1) {
        r = "0" + r;
      }
      if (g.length == 1) {
        g = "0" + g;
      }
      if (b.length == 1) {
        b = "0" + b;
      }

      return "#" + r + g + b;
    },
    pixColor: function (colorFrom, colorTo, ratio) {
      var rgbFrom = [
        parseInt(colorFrom[2] + colorFrom[3], 16),
        parseInt(colorFrom[4] + colorFrom[5], 16),
        parseInt(colorFrom[6] + colorFrom[7], 16)
      ];
      var rgbTo = [
        parseInt(colorTo[2] + colorTo[3], 16),
        parseInt(colorTo[4] + colorTo[5], 16),
        parseInt(colorTo[6] + colorTo[7], 16)
      ];

      var w1 = 1 - ratio;
      var w2 = ratio;
      var rgb = [Math.round(rgbFrom[0] * w1 + rgbTo[0] * w2),
        Math.round(rgbFrom[1] * w1 + rgbTo[1] * w2),
        Math.round(rgbFrom[2] * w1 + rgbTo[2] * w2)];
      return this.rgbToHex(rgb[0], rgb[1], rgb[2]);
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
}

.grid:hover {
  cursor: pointer;
}

.wall {
}

.goal {
  margin: 0px;
  border: 3px solid #33ee99;
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
