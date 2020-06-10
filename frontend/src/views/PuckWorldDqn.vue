<template>
  <div class="puck-world-dqn">
    <div class="control-panel-container">
      <div class="control-panel">
        <h1>Puck World: Deep Q-Learning</h1>

        <el-row style="padding: 12px;">
          <el-button
            @click="toggleRunning">
            {{toggleRunningButtonText}}
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          Tick count: <code>{{tickCount}}</code>
        </el-row>

        <el-row style="padding: 12px;">
          Experience count: <code>{{this.experience.length}}</code>
        </el-row>

        <el-row style="padding: 12px;">
          <v-chart :options="chartOptions" />
        </el-row>
      </div>
    </div>

    <div class="puck-world-container">
      <puck-world :puck-world-data="puckWorldData" />
    </div>
  </div>
</template>

<script>
import PuckWorld from '@/components/PuckWorld.vue';
import { AXIOS } from '../util/http-common.js';
import axios from 'axios';
import LineChart from '@/components/LineChart.vue';
import ECharts from 'vue-echarts';
import 'echarts/lib/chart/line';

export default {
  name: 'PuckWorldDqn',
  components: {
    'puck-world': PuckWorld, 'v-chart': ECharts
  },
  data: function () {
    return {
      puckWorldData: {
        puckX: 0.05,
        puckY: 0.3,
        puckRadius: 0.05,
        greenTargetX: 0.7,
        greenTargetY: 0.8,
        greenTargetRadius: 0.015,
        redTargetX: 0.45,
        redTargetY: 0.55,
        redTargetRadius: 0.015,
        badRadius: 0.25,
        action: 3
      },
      puckAcceleration: 0.005,
      puckVelocityX: 0.0,
      puckVelocityY: 0.0,
      puckDampingFactor: 0.95,
      redTargetVelocityX: 0.0,
      redTargetVelocityY: 0.0,
      redTargetVelocity: 0.001,
      bounceFactor: -0.5,

      running: false,
      toggleRunningButtonText: "Start DQN",
      tickInterval: 10,
      tickCount: 0,
      greenTargetResetIntervalInTicks: 100,
      epsilon: 0.2, // For $\epsilon$-greedy
      gamma: 0.9, // The discount factor
      tdErrorClamp: 1.0,
      experience: [],
      transitionIndex: 0,
      transitionMemoryIntervalInTicks: 4,
      experienceMaxSize: 3000,
      replayMaxSize: 16,
      currentTransition: [ null, null, null, null ], // [ s0, a0, r1, s1 ]
      currentTdError: null, // TODO
      hiddenSize: 100,
      w1: null,
      b1: null,
      w2: null,
      b2: null,

      // chartData: {
      //   labels: [],
      //   datasets: [ {
      //     label: "Latest TD error",
      //     backgroundColor: "#e0828366",
      //     borderColor: "#ff0000",
      //     lineTension: 0.1,
      //     borderWidth: 1,
      //     fill: true,
      //     pointRadius: 2,
      //     data: [ ]
      //   } ]
      // },
      chartOptions: {
        title: {
          text: "Latest TD Error v.s. Tick Index"
        },
        xAxis: {
          type: 'value',
          splitLine: {
            show: false
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            params = params[0];
            return params.name + ': ' + params.value[1];
          },
          axisPointer: {
            animation: false
          }
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '100%'],
          splitLine: {
            show: false
          }
        },
        series: [{
          name: 'latest td error',
          type: 'line',
          showSymbol: false,
          hoverAnimation: false,
          data: []
        }],
      },
    }
  },
  watch: {
    running: {
      handler: function () {
        if (this.running) {
          this.tick();
        }
      },
    },
  },
  computed: {
  },
  created () {
    this.currentTransition[0] = this.state();
    this.currentTransition[1] = Math.floor(Math.random() * 5.0);
  },
  methods: {
    toggleRunning: function () {
      this.running = !this.running;

      if (this.running) {
        this.toggleRunningButtonText = "Stop DQN";
      } else {
        this.toggleRunningButtonText = "Start DQN";
      }
    },
    tick: function () {
      // Increment the tick count by one
      this.tickCount += 1;

      // Take action
      // if (Math.random() < this.epsilon) {
      //   this.puckWorldData.action = Math.floor(Math.random() * 5.0);
      //   this.currentTransition[1] = this.puckWorldData.action;
      // } else {
      //   // // Compute forward


      //   // // Find the max Q index
      //   // var maxQIndex = -1;
      //   // var maxQ = 0.0;
        

      //   // this.puckWorldData.action = maxQIndex;
      //   this.puckWorldData.action = this.currentTransition[1];
      // }
      // Already done on POST response

      // Update the data in puck world and UI will be updated automatically
      this.updatePuckWorldData();

      // Update the transition
      var firstTick = true;
      if (this.currentTransition[3] != null) {
        firstTick = false;
        this.currentTransition[0] = this.currentTransition[3];
      }
      this.currentTransition[1] = this.puckWorldData.action;
      this.currentTransition[2] = this.reward();
      // var state = this.state;
      // console.log("Got u state!");
      // console.log(state);
      this.currentTransition[3] = this.state();

      // // todo
      // console.log(this.currentTransition);
      // console.log(this.currentTransition[3]);
      // console.log(this.state());

      // Store the transition in the experience if necessary
      if (this.tickCount % this.transitionMemoryIntervalInTicks == 0) {
        // Deep copy the current transition, or you will only playing the reference to this.currentTransition!
        var transitionCopy = JSON.parse(JSON.stringify(this.currentTransition));
        // console.log(this.transitionIndex);
        // console.log(this.currentTransition);
        if (this.transitionIndex + 1 > this.experience.length) {
          this.experience.push(transitionCopy);
        } else {
          this.experience[this.transitionIndex] = transitionCopy;
        }
        // console.log(this.experience);
        // console.log(this.experience[this.experience.length - 1]);

        // Increment the transition index
        this.transitionIndex += 1;
        if (this.transitionIndex >= this.experienceMaxSize) {
          this.transitionIndex = 0;
        }
      }

      // Experience replay
      var transitions = this.sampleTransitions();
      var viewModel = this;
      var weights = null;
      if (!firstTick) {
        weights = { w1: viewModel.w1, b1: viewModel.b1, w2: viewModel.w2, b2: viewModel.b2 };
      }
      // console.log(weights);
      AXIOS.post("/puckworld/learn_from_transitions", { weights: weights, hiddenSize: viewModel.hiddenSize, transitions: transitions, clamp: viewModel.tdErrorClamp, gamma: viewModel.gamma })
      .then(response => {
        var weights = response.data.weights;
        viewModel.w1 = weights.w1;
        viewModel.b1 = weights.b1;
        viewModel.w2 = weights.w2;
        viewModel.b2 = weights.b2;

        // Update the action
        if (Math.random() < viewModel.epsilon) {
          viewModel.puckWorldData.action = response.data.a1;
        } else {
          viewModel.puckWorldData.action = Math.floor(Math.random() * 5.0);
        }
        // viewModel.currentTransition[1] = viewModel.puckWorldData.action;

        // Display the latest TD error
        // viewModel.chartData.datasets[0].data.push(response.data.latestTdError);
        // viewModel.chartData.labels.push(viewModel.chartData.datasets[0].data.length);
        viewModel.chartOptions.series[0].data.push({
          name: viewModel.tickCount,
          value: [ viewModel.tickCount, response.data.latestTdError ]
        });
        // console.log(viewModel.chartData);

        // Loop
        if (!viewModel.running) {
          return;
        }
        setTimeout(function () { viewModel.tick() }, viewModel.tickInterval);
      })
      .catch(e => {
        console.log(e);
        // TODO: stop the button and make alerts
      });
    },
    sampleTransitions: function () {
      var transitions = [ this.currentTransition ];
      for (var i = 0; i < this.replayMaxSize; i++) {
        // Stop sampling if there is no experience at all
        if (this.experience.length == 0) {
          break;
        }

        var index = this.randomInt(0, this.experience.length);
        // console.log(index);
        // console.log(this.experience[index]);
        transitions.push(this.experience[index]);
      }
      return transitions;
    },
    randomInt: function(a, b) {
      return Math.floor(Math.random() * (b - a) + a);
    },
    updatePuckWorldData: function () {
      // Update the velocity of the puck
      // Damping
      this.puckVelocityX *= this.puckDampingFactor;
      this.puckVelocityY *= this.puckDampingFactor;
      // Acceleration
      if (this.puckWorldData.action === 1) {
        this.puckVelocityY -= this.puckAcceleration;
      } else if (this.puckWorldData.action === 2) {
        this.puckVelocityX += this.puckAcceleration;
      } else if (this.puckWorldData.action === 3) {
        this.puckVelocityY += this.puckAcceleration;
      } else if (this.puckWorldData.action === 4) {
        this.puckVelocityX -= this.puckAcceleration;
      }

      // Update the velocity of the red target
      var dxRed = this.puckWorldData.puckX - this.puckWorldData.redTargetX;
      var dyRed = this.puckWorldData.puckY - this.puckWorldData.redTargetY;
      var distanceRed = Math.sqrt(dxRed * dxRed + dyRed * dyRed);
      this.redTargetVelocityX = dxRed * this.redTargetVelocity / distanceRed;
      this.redTargetVelocityY = dyRed * this.redTargetVelocity / distanceRed;

      // Update the position of the puck
      this.puckWorldData.puckX += this.puckVelocityX;
      this.puckWorldData.puckY += this.puckVelocityY;

      // Boundary detection for the puck
      if (this.puckWorldData.puckX <= this.puckWorldData.puckRadius) {
        this.puckVelocityX *= this.bounceFactor;
        this.puckWorldData.puckX = this.puckWorldData.puckRadius;
      } else if (this.puckWorldData.puckX >= 1.0 - this.puckWorldData.puckRadius) {
        this.puckVelocityX *= this.bounceFactor;
        this.puckWorldData.puckX = 1.0 - this.puckWorldData.puckRadius;
      }
      if (this.puckWorldData.puckY <= this.puckWorldData.puckRadius) {
        this.puckVelocityY *= this.bounceFactor;
        this.puckWorldData.puckY = this.puckWorldData.puckRadius;
      } else if (this.puckWorldData.puckY >= 1.0 - this.puckWorldData.puckRadius) {
        this.puckVelocityY *= this.bounceFactor;
        this.puckWorldData.puckY = 1.0 - this.puckWorldData.puckRadius;
      }
      
      // Update the position of the red target
      this.puckWorldData.redTargetX += this.redTargetVelocityX;
      this.puckWorldData.redTargetY += this.redTargetVelocityY;

      // Reset the position of the green target if necessary
      if (this.tickCount % this.greenTargetResetIntervalInTicks === 0) {
        this.puckWorldData.greenTargetX = Math.random();
        this.puckWorldData.greenTargetY = Math.random();
      }
    },

    state: function () {
      return [
        this.puckWorldData.puckX, this.puckWorldData.puckY,
        this.puckVelocityX, this.puckVelocityY,
        this.puckWorldData.greenTargetX, this.puckWorldData.greenTargetY,
        this.puckWorldData.redTargetX, this.puckWorldData.redTargetY ];
    },

    reward: function () {
      var r = 0.0;

      // The closer to the green target, the better
      var dxGreen = this.puckWorldData.puckX - this.puckWorldData.greenTargetX;
      var dyGreen = this.puckWorldData.puckY - this.puckWorldData.greenTargetY;
      var distanceGreen = Math.sqrt(dxGreen * dxGreen + dyGreen * dyGreen);
      r += -distanceGreen;

      // If the puck is in the bad area
      var badRadius = this.puckWorldData.badRadius;
      var dxRed = this.puckWorldData.puckX - this.puckWorldData.redTargetX;
      var dyRed = this.puckWorldData.puckY - this.puckWorldData.redTargetY;
      var distanceRed = Math.sqrt(dxRed * dxRed + dyRed * dyRed);
      if (distanceRed < badRadius) {
        // The closer to the red taget, the worse
        r += 2 * (distanceRed - badRadius) / badRadius;
      }

      return r;
    },
  },
};
</script>

<style scoped>
* {
  font-family: "roboto";
}

code {
  font-family: "monaco";
}

.puck-world-dqn {
  flex-grow: 1;

  display: flex;
  flex-direction: row;
  align-items: stretch;
}

.control-panel-container {
  flex-grow: 0;
}

.control-panel {
  margin: 12px;
  padding: 12px;
}

.puck-world-container {
  flex-grow: 1;

  background-color: #f3f1ef;
}

.echarts {
  width: 90%;
  height: 200px;
}
</style>
