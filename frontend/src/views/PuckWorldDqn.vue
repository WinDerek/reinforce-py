<template>
  <div class="puck-world-dqn">
    <div class="control-panel-container">
      <div class="control-panel">
        <h1>Puck World: Deep Q-Learning</h1>
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
      }
    }
  },
  created () {
  },
  methods: {
  }
};
</script>

<style scoped>
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
