<template>
  <div class="water-world">
    <div class="container">
      <svg></svg>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WaterWorld',
  model: {
    prop: 'waterWorldData'
  },
  props: {
    puckWorldData: {
      type: Object, // 
      required: true
    }
  },
  data: function () {
    return {
      
    }
  },
  created: function () {
  },
  watch: {
  },
  computed: {
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

.water-world {
  width: 100%;
  height: 100%;
  margin: auto;

  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.container {
  width: 80vh;
  height: 80vh;
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
