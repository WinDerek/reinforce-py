<template>
  <div class="grid-world-dbs">
    <div class="control-panel-container">
      <div class="control-panel">
        <h1>Grid World: DBS Updates</h1>
        
        <el-row style="padding: 12px;">
          <el-button
            @click="reset"
            :disabled="sarsaRunning">
            Reset Grid World
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="sarsaOneStep"
            :disabled="sarsaOneStepPending || sarsaRunning">
            Sarsa 1 step
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="toggleSarsa">
            {{toggleSarsaButtonText}}
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="qLearningOneStep"
            :disabled="qLearningOneStepPending || qLearningRunning">
            Q-Learning 1 step
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="toggleQLearning">
            {{toggleQLearningButtonText}}
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          Total steps: <code>{{totalSteps}}</code>
        </el-row>

        <el-row style="padding: 12px;">
          Iteration interval (0.1s ~ 1.0s)
          <el-slider
            v-model="interval"
            :min="5"
            :max="100"
            :step="5"
            :format-tooltip="formatTooltip">
          </el-slider>
        </el-row>

        <el-row style="padding: 12px;">
          Deviation probability
          <el-slider
            v-model="deviationProbability"
            :min="0"
            :max="100"
            :step="5"
            :format-tooltip="formatDeviationProbabilityTooltip">
          </el-slider>
        </el-row>

        <el-row style="padding: 12px;" v-if="selectedIndex != -1">
          Min: <code>{{minReward.toFixed(2)}}</code>
          Max: <code>{{maxReward.toFixed(2)}}</code>
          Reward: <code>{{selectedReward}}</code>
          <el-slider
            v-model="rewardSliderValue"
            :min="0"
            :max="100"
            :step="5"
            :format-tooltip="formatRewardTooltip"
            v-on:change="onRewardSliderValueChanged">
          </el-slider>
        </el-row>
      </div>
    </div>

    <div class="grid-world-container">
      <GridWorld
        :grid-data-array="gridDataArray"
        :wall-index-array="wallIndexArray"
        :selectedIndex="selectedIndex"
        v-on:on-selected-index-updated="onSelectedIndexUpdated"
        :currentIndex="currentIndex" />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import GridWorld from '@/components/GridWorld.vue';
import { AXIOS } from '../util/http-common.js';
// import axios from 'axios';

export default {
  name: 'grid-world-dbs',
  components: {
    GridWorld
  },
  data: function () {
    return {
      initialGridDataArray: [],
      gridDataArray: [],
      wallIndexArray: [ 1, 7, 11, 17, 21, 27, 31, 37, 41, 47, 51, 57, 61, 67, 81, 87, 88, 91, 97 ],
      goalIndex: 98,
      initialMinusRewardIndexArray: [],
      interval: 5,
      deviationProbability: 0,
      selectedIndex: -1,
      rewardSliderValue: 0,
      minReward: 0.0,
      maxReward: 1.0,
      currentIndex: 0,
      currentAction: 1,
      toggleSarsaButtonText: "start DBS value iteration",
      dbsValueIterationRunning: false,
      dbsValueIterationOneStepPending: false,
      totalSteps: 0
    }
  },
  computed: {
    iterationIntervalInMillis () {
      // return this.interval * 10;
      return 1;
    },
    selectedReward () {
      if (this.selectedIndex != -1) {
        return this.gridDataArray[this.selectedIndex].reward.toFixed(2);
      }
      return null;
    }
  },
  watch: {
    dbsValueIterationRunning: {
      handler: function () {
        var viewModel = this;

        function _dbsValueIterationOneStep () {
          AXIOS.post("/dynamic_programming/dbs-value-iteration-one-step", { gridDataArray: viewModel.gridDataArray, currentState: viewModel.currentIndex, currentAction: viewModel.currentAction, epsilon: 0.15, alpha: 0.2, deviationProbability: viewModel.deviationProbability / 100.0 })
            .then(response => {
              viewModel.totalSteps++;

              var newQ = response.data.newQ;
              var newPolicy = response.data.newPolicy;
              var stateValueFrom = response.data.stateValueFrom;
              var stateValueTo = response.data.stateValueTo;
              var stateTo = response.data.stateTo;
              var actionTo = response.data.actionTo;

              viewModel.gridDataArray[viewModel.currentIndex].q[viewModel.currentAction] = newQ;

              viewModel.gridDataArray[stateTo].policy = newPolicy;

              viewModel.gridDataArray[viewModel.currentIndex].stateValue = stateValueFrom;
              viewModel.gridDataArray[stateTo].stateValue = stateValueTo;

              viewModel.currentIndex = stateTo;
              viewModel.currentAction = actionTo;

              if (!viewModel.dbsValueIterationRunning) {
                return;
              }

              setTimeout(function () { _dbsValueIterationOneStep() }, viewModel.iterationIntervalInMillis);
            }).catch(e => {
              console.log(e);
            });
        }

        if (viewModel.dbsValueIterationRunning) {
          _dbsValueIterationOneStep();
        }
      }
    },
  },
  created () {
    for (var i = 0; i < 10; i++) {
      for (var j = 0; j < 10; j++) {
        var count = 0 + (i == 0) + (j == 9) + (i == 9) + (j == 0);
        var prob = 1.0 / (4 - count);
        var policyArray = [];
        policyArray.push(i == 0 ? 0.0 : prob);
        policyArray.push(j == 9 ? 0.0 : prob);
        policyArray.push(i == 9 ? 0.0 : prob);
        policyArray.push(j == 0 ? 0.0 : prob);

        this.initialGridDataArray.push(
          {
            wall: false,
            goal: false,
            gridIndex: i * 10 + j,
            stateValue: 0.0,
            reward: 0.0,
            policy: policyArray,
            q: [ 0.0, 0.0, 0.0, 0.0 ]
          }
        );
      }
    }

    // Set the walls
    this.wallIndexArray.forEach(wallIndex => this.initialGridDataArray[wallIndex].wall = true);

    // Set special reward
    this.initialGridDataArray[this.goalIndex].reward = 1.0;

    // Set the goal
    this.initialGridDataArray[this.goalIndex].goal = true;

    // Set the initial -1 reward
    this.initialMinusRewardIndexArray.forEach(index => this.initialGridDataArray[index].reward = -1.0);

    this.gridDataArray = JSON.parse(JSON.stringify(this.initialGridDataArray));
  },
  methods: {
    formatTooltip: function (value) {
      var seconds = value * 10 / 1000.0;
      return seconds.toFixed(1) + "s";
    },
    formatDeviationProbabilityTooltip: function (value) {
      return value / 100.0;
    },
    onSelectedIndexUpdated: function (gridIndex, selected) {
      if (selected) {
        this.selectedIndex = -1;
      } else {
        if (this.selectedIndex == -1) {
          this.selectedIndex = gridIndex;

          this.rewardSliderValue = Math.round((this.gridDataArray[this.selectedIndex].reward - this.minReward) * 100.0 / (this.maxReward - this.minReward));
        } else {
          console.log("Cannot select multiple grids!");
        }
      }
    },
    onRewardSliderValueChanged: function (sliderValue) {
      this.gridDataArray[this.selectedIndex].reward = (100 - sliderValue) * this.minReward / 100.0 + sliderValue * this.maxReward / 100.0;
    },
    formatRewardTooltip: function (value) {
      return this.gridDataArray[this.selectedIndex].reward.toFixed(2);
    },
    reset: function () {
      this.gridDataArray = JSON.parse(JSON.stringify(this.initialGridDataArray));
      this.selectedIndex = -1;
      this.sarsaRunning = false;
    },
    toggleSarsa: function () {
      this.sarsaRunning = !this.sarsaRunning;

      if (this.sarsaRunning) {
        this.toggleSarsaButtonText = "Stop sarsa";
      } else {
        this.toggleSarsaButtonText = "Start sarsa";
      }
    },
    dbsValueIterationOneStep() {
      if (this.dbsValueIterationOneStepPending) {
        return;
      }

      this.dbsValueIterationOneStepPending = true;

      let viewModel = this;

      AXIOS.post("/dynamic_programming/sarsa_one_step", { gridDataArray: this.gridDataArray, currentState: this.currentIndex, currentAction: this.currentAction, epsilon: 0.2, alpha: 0.1, deviationProbability: viewModel.deviationProbability / 100.0 })
            .then(response => {
              this.totalSteps++;

              var newQ = response.data.newQ;
              var newPolicy = response.data.newPolicy;
              var stateValueFrom = response.data.stateValueFrom;
              var stateValueTo = response.data.stateValueTo;
              var stateTo = response.data.stateTo;
              var actionTo = response.data.actionTo;

              this.gridDataArray[this.currentIndex].q[this.currentAction] = newQ;

              this.gridDataArray[stateTo].policy = newPolicy;

              this.gridDataArray[this.currentIndex].stateValue = stateValueFrom;
              this.gridDataArray[stateTo].stateValue = stateValueTo;

              this.currentIndex = stateTo;
              this.currentAction = actionTo;

              this.sarsaOneStepPending = false;
            }).catch(e => {
              console.log(e);

              this.sarsaOneStepPending = false;
            });
    },
  }
};
</script>

<style scoped>
* {
  font-family: "roboto";
}

.grid-world-dbs {
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

.grid-world-container {
  flex-grow: 1;

  background-color: #f3f1ef;
}

code {
  font-family: "monaco";
}
</style>
