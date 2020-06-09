<template>
  <div class="water-world-dqn">
    <div class="control-panel-container">
      <div class="control-panel">
        <h1>Water World: Deep Q-Learning</h1>
      </div>
    </div>

    <div class="water-world-container">
      <WaterWorld />
    </div>
  </div>
</template>

<script>
import WaterWorld from '@/components/WaterWorld.vue';

export default {
  name: 'WaterWorldDqn',
  components: {
    WaterWorld
  },
  data: function () {
    return {
    }
  },
  created () {
  },
  methods: {
  }
};
</script>

<style scoped>
.water-world-dqn {
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

.water-world-container {
  flex-grow: 1;

  background-color: #f3f1ef;
}
</style>
