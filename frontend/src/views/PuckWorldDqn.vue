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

      if (!this.running) {
        return;
      }

      var viewModel = this;
      setTimeout(function () { viewModel.tick() }, viewModel.tickInterval);
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
