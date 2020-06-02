<template>
  <div class="home">
    <h1>REINFORCEpy</h1>

    <div class="introduction-container">
      REINFORCEpy is a reinforcement learning library that implements several common RL algorithms, all with web demos. In particular, the library currently supports:
      <ul>
        <li>Dynamic Programming methods</li>
        <li>Temporal-Difference Learning (SARSA / Q-Learning)</li>
        <li>(TODO) Deep Q-Learning for Q-Learning with function approximation with Neural Networks</li>
        <li>(TODO) Stochastic/Deterministic Policy Gradients and Actor Critic architectures for dealing with continuous action spaces</li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {
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
* {
  font-family: "roboto";
}

.home {
  flex-grow: 1;

  display: flex;
  flex-direction: column;
  align-items: start;

  padding: 12px 1.5rem;
}

.introduction-container {
}
</style>
