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
      </div>
    </div>

    <div class="puck-world-container">
      <PuckWorld :puck-world-data="puckWorldData" />
    </div>
  </div>
</template>

<script>
import PuckWorld from '@/components/PuckWorld.vue';
import { AXIOS } from '../util/http-common.js';
import axios from 'axios';

export default {
  name: 'PuckWorldDqn',
  components: {
    PuckWorld
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
      puckAcceleration: 0.002,
      puckVelocityX: 0.0,
      puckVelocityY: 0.0,
      puckDampingFactor: 0.95,
      redTargetVelocityX: 0.0,
      redTargetVelocityY: 0.0,
      redTargetVelocity: 0.001,
      bounceFactor: -0.5,

      running: false,
      toggleRunningButtonText: "Start DQN",
      tickInterval: 20,
      tickCount: 0,
      greenTargetResetIntervalInTicks: 100,
      epsilon: 0.1, // For $\epsilon$-greedy
      gamma: 0.9, // The discount factor
      tdErrorClamp: 1.0,
      experience: [],
      transitionIndex: 0,
      transitionMemoryIntervalInTicks: 25,
      experienceMaxSize: 3000,
      replayMaxSize: 16,
      currentTransition: [ null, null, null, null ], // [ s0, a0, r1, s1 ]
      currentTdError: null, // TODO
      hiddenSize: 64,
      w1: null,
      b1: null,
      w2: null,
      b2: null,
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
    state () {
      return [
        this.puckWorldData.puckX, this.puckWorldData.puckY,
        this.puckVelocityX, this.puckVelocityY,
        this.puckWorldData.greenTargetX, this.puckWorldData.greenTargetY,
        this.puckWorldData.redTargetX, this.puckWorldData.redTargetY ];
    },
    reward () {
      reward = 0.0;

      var badRadius = this.puckWorldData.badRadius;

      // The closer to the green target, the better
      var dxGreen = this.puckWorldData.puckX - this.puckWorldData.greenTargetX;
      var dyGreen = this.puckWorldData.puckY - this.puckWorldData.greenTargetY;
      var distanceGreen = Math.sqrt(dxGreen * dxGreen + dyGreen * dyGreen);
      reward += -distanceGreen;

      // If the puck is in the bad area
      var dxRed = this.puckWorldData.puckX - this.puckWorldData.redTargetX;
      var dyRed = this.puckWorldData.puckY - this.puckWorldData.redTargetY;
      var distanceRed = Math.sqrt(dxRed * dxRed + dyRed * dyRed);
      if (distanceRed < badRadius) {
        // The closer to the red taget, the worse
        reward += 2 * (distanceRed - badRadius) / badRadius;
      }
    },
  },
  created () {
    this.currentTransition[0] = this.state;
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
      if (Math.random() < this.epsilon) {
        this.puckWorldData.action = Math.floor(Math.random() * 5.0);
      } else {
        // Compute forward


        // Find the max Q index
        var maxQIndex = -1;
        var maxQ = 0.0;
        

        this.puckWorldData.action = maxQIndex;
      }

      // Update the data in puck world and UI will be updated automatically
      this.updatePuckWorldData();

      // Reset the position of the green target if necessary
      if (this.tickCount % this.greenTargetResetIntervalInTicks === 0) {
        this.puckWorldData.greenTargetX = Math.random();
        this.puckWorldData.greenTargetY = Math.random();
      }

      // Update the transition
      var firstTick = false;
      if (this.currentTransition[2] != null) {
        firstTick = true;
        this.currentTransition[0] = this.currentTransition[3];
      }
      this.currentTransition[1] = this.puckWorldData.action;
      this.currentTransition[2] = this.reward;
      this.currentTransition[3] = this.state;

      // Store the transition in the experience if necessary
      if (this.tickCount % this.transitionMemoryIntervalInTicks == 0) {
        if (this.transitionIndex + 1 > this.experience.length) {
          this.experience.push(this.currentTransition);
        } else {
          this.experience[this.transitionIndex] = this.currentTransition;
        }

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
      AXIOS.post("/puckworld/learn_from_transitions", { weights: weights, hideenSize: viewModel.hideenSize, transitions: transitions, clamp: viewModel.tdErrorClamp, gamma: viewModel.gamma })
      .then(response => {
        var weights = response.data;
        viewModel.w1 = weights.w1;
        viewModel.b1 = weights.b1;
        viewModel.w2 = weights.w2;
        viewModel.b2 = weights.b2;

        // Loop
        if (!this.running) {
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
        var index = this.randomInt(0, this.experience.length);
        transitions.push(this.experience[index]);
      }
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
</style>
