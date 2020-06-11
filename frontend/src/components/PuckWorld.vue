<template>
  <div class="puck-world">
    <div class="container">
      <svg viewBox="0 0 1 1" style="background-color:white">
        <!-- The puck -->
        <circle :cx="puckWorldData.puckX" :cy="puckWorldData.puckY" :r="puckWorldData.puckRadius" stroke="#34495e" stroke-width="0.0012" fill="transparent" />
        <line
          fill="none"
          stroke="#2e3131"
          stroke-width="0.003"
          stroke-linecap="round"
          stroke-linejoin="round"
          :x1="puckWorldData.puckX"
          :y1="puckWorldData.puckY"
          :x2="arrowHeadX"
          :y2="arrowHeadY" />

        <!-- The red target -->
        <circle :cx="puckWorldData.redTargetX" :cy="puckWorldData.redTargetY" :r="puckWorldData.badRadius" fill="#f1a9a066" stroke="#96281b" stroke-width="0.0012" />
        <circle :cx="puckWorldData.redTargetX" :cy="puckWorldData.redTargetY" :r="puckWorldData.redTargetRadius" fill="#cf000f" />

        <!-- The green target -->
        <circle :cx="puckWorldData.greenTargetX" :cy="puckWorldData.greenTargetY" :r="puckWorldData.greenTargetRadius" fill="#00e640" />
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PuckWorld',
  model: {
    prop: 'puckWorldData'
  },
  props: {
    puckWorldData: {
      type: Object, // puckX: 0.5, puckY: 0.5, puckRadius: 0.05, greenTargetX: 0.5, greenTargetY: 0.5, greenTargetRadius: 0.01, redTargetX: 0.5, redTargetY: 0.5, redTargetRadius: 0.01, badRadius: 0.25, action: 4
      required: true
    }
  },
  data: function () {
    return {
      arrowRatio: 0.618
    }
  },
  created: function () {
  },
  watch: {
  },
  computed: {
    arrowHeadX () {
      if ((this.puckWorldData.action == 1) || (this.puckWorldData.action == 3) || (this.puckWorldData.action == 0)) {
          return this.puckWorldData.puckX;
      } else if (this.puckWorldData.action == 2) {
          return this.puckWorldData.puckX + this.arrowRatio * this.puckWorldData.puckRadius;
      } else if (this.puckWorldData.action == 4) {
          return this.puckWorldData.puckX - this.arrowRatio * this.puckWorldData.puckRadius;
      }
    },
    arrowHeadY () {
      if ((this.puckWorldData.action == 2) || (this.puckWorldData.action == 4) || (this.puckWorldData.action == 0)) {
          return this.puckWorldData.puckY;
      } else if (this.puckWorldData.action == 1) {
          return this.puckWorldData.puckY - this.arrowRatio * this.puckWorldData.puckRadius;
      } else if (this.puckWorldData.action == 3) {
          return this.puckWorldData.puckY + this.arrowRatio * this.puckWorldData.puckRadius;
      }
    }
  },
  methods: {
  }
}
</script>

<style scoped>
* {
  -webkit-user-select: none;  /* Chrome all / Safari all */
  -moz-user-select: none;     /* Firefox all */
  -ms-user-select: none;      /* IE 10+ */
  user-select: none;          /* Likely future */  
}

.puck-world {
  width: 100%;
  height: 100%;
  margin: auto;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.container {
  width: min(80vw, 80vh);
  height: min(80vw, 80vh);
  padding: 12px;
  background-color: #ececec;
  border: 6px solid #2c3e50;
  box-shadow: 0 3px 12px rgba(37, 34, 67, 0.9);

  margin: auto;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}
</style>
