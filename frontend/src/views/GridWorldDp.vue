<template>
  <div class="grid-world-dp">
    <h1>Grid World: Dynamic Programming</h1>

    <el-row>
      <el-col :span="6" class="control-panel">
        <el-row style="padding: 12px;">
          <el-button
            @click="reset"
            :disabled="valueIterationRunning">
            Reset Grid World
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="evaluatePolicy"
            :disabled="valueIterationRunning"
            :loading="policyEvaluationLoading">
            Policy evaluation (1 sweep)
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="improvePolicy"
            :disabled="valueIterationRunning"
            :loading="policyImprovementLoading">
            Policy improvement
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          <el-button
            @click="toggleValueIteration">
            {{toggleValueIterationButtonText}}
          </el-button>
        </el-row>

        <el-row style="padding: 12px;">
          Iteration interval (0.1s ~ 1.0s)
          <el-slider
            v-model="interval"
            :min="10"
            :max="100"
            :step="10"
            :format-tooltip="formatTooltip">
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
      </el-col>

      <el-col :span="18">
        <GridWorld
          :grid-data-array="gridDataArray"
          :wall-index-array="wallIndexArray"
          :selectedIndex="selectedIndex"
          v-on:on-selected-index-updated="onSelectedIndexUpdated" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
// @ is an alias to /src
import GridWorld from '@/components/GridWorld.vue';
import { AXIOS } from '../util/http-common.js';
import axios from 'axios';
import MyMenu from '@/components/MyMenu.vue';
// import _ from 'lodash';

export default {
  name: 'GridWorldDp',
  components: {
    GridWorld, MyMenu
  },
  data: function () {
    return {
      initialGridDataArray: [],
      gridDataArray: [],
      wallIndexArray: [ 21, 22, 23, 24, 26, 27, 28, 34, 44, 54, 64, 74 ],
      initialMinusRewardIndexArray: [ 33, 45, 46, 56, 58, 68, 73, 75, 76 ],
      policyEvaluationLoading: false,
      policyImprovementLoading: false,
      valueIterationRunning: false,
      interval: 10,
      selectedIndex: -1,
      rewardSliderValue: 0,
      minReward: -1.0,
      maxReward: 1.0,
      toggleValueIterationButtonText: "Start value iteration"
    }
  },
  computed: {
    valueIterationIntervalInMillis () {
      return this.interval * 10;
    },
    selectedReward () {
      if (this.selectedIndex != -1) {
        return this.gridDataArray[this.selectedIndex].reward.toFixed(2);
      }
      return null;
    }
  },
  watch: {
    valueIterationRunning: {
      handler: function () {
        var viewModel = this;

        function _evaluatePolicy () {
          AXIOS.post("/dynamic_programming/policy_evaluation", viewModel.gridDataArray)
            .then(response => {
              var stateValueArray = response.data;
              // console.log(response.data);

              for (var i = 0; i < viewModel.gridDataArray.length; i++) {
                viewModel.gridDataArray[i].stateValue = stateValueArray[i];
              }

              if (!viewModel.valueIterationRunning) {
                return;
              }
              setTimeout(function () { _improvePolicy() }, viewModel.valueIterationIntervalInMillis);
            }).catch(e => {
              console.log(e);
            });
        }

        function _improvePolicy () {
          AXIOS.post("/dynamic_programming/policy_improvement", viewModel.gridDataArray)
            .then(response => {
              var policyArray = response.data;
              // console.log(response.data);

              for (var i = 0; i < viewModel.gridDataArray.length; i++) {
                viewModel.gridDataArray[i].policy = policyArray[i];
              }

              if (!viewModel.valueIterationRunning) {
                return;
              }

              setTimeout(function () { _evaluatePolicy() }, viewModel.valueIterationIntervalInMillis);
            }).catch(e => {
              console.log(e);
            });
        }

        if (viewModel.valueIterationRunning) {
          _evaluatePolicy();
        }
      }
    }
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
            policy: policyArray
          }
        );
      }
    }



    // Set the walls
    this.wallIndexArray.forEach(wallIndex => this.initialGridDataArray[wallIndex].wall = true);

    // Set special reward
    this.initialGridDataArray[55].reward = 1.0;

    // Set the goal
    this.initialGridDataArray[55].goal = true;

    // Set the initial -1 reward
    this.initialMinusRewardIndexArray.forEach(index => this.initialGridDataArray[index].reward = -1.0)

    this.gridDataArray = JSON.parse(JSON.stringify(this.initialGridDataArray));
  },
  methods: {
    hello () {

      AXIOS.get('/hello')
        .then(response => {
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        })
    },
    evaluatePolicy () {
      if (this.policyEvaluationLoading) {
        return;
      }

      this.policyEvaluationLoading = true;

      AXIOS.post("/dynamic_programming/policy_evaluation", this.gridDataArray)
      .then(response => {
        var stateValueArray = response.data;
        // console.log(response.data);

        for (var i = 0; i < this.gridDataArray.length; i++) {
          this.gridDataArray[i].stateValue = stateValueArray[i];
        }

        this.policyEvaluationLoading = false;
      }).catch(e => {
        console.log(e);

        this.policyEvaluationLoading = false;
      })
    },
    improvePolicy () {
      if (this.policyImproveLoading) {
        return;
      }

      this.policyImprovementLoading = true;

      AXIOS.post("/dynamic_programming/policy_improvement", this.gridDataArray)
      .then(response => {
        var policyArray = response.data;
        // console.log(response.data);

        for (var i = 0; i < this.gridDataArray.length; i++) {
          this.gridDataArray[i].policy = policyArray[i];
        }

        this.policyImprovementLoading = false;
      }).catch(e => {
        console.log(e);

        this.policyImprovementLoading = false;
      })
    },
    formatTooltip: function (value) {
      var seconds = value * 10 / 1000.0;
      return seconds.toFixed(1) + "s";
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
    toggleValueIteration: function () {
      this.valueIterationRunning = !this.valueIterationRunning;

      if (this.valueIterationRunning) {
        this.toggleValueIterationButtonText = "Stop value iteration";
      } else {
        this.toggleValueIterationButtonText = "Start value iteration";
      }
    },
    reset: function () {
      this.gridDataArray = JSON.parse(JSON.stringify(this.initialGridDataArray));
      this.selectedIndex = -1;
      this.valueIterationRunning = false;
    }
  }
};
</script>

<style scoped>
* {
  font-family: "roboto";
}

.grid-world-dp {
  flex-grow: 1;
}

.control-panel {
  padding: 12px;
  border: 2px solid #2c3e50;
  border-radius: 4px;
}

code {
  font-family: "monaco";
}
</style>
