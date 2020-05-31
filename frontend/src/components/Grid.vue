<template>
  <div class="grid">
    {{gridData.gridIndex}}
  </div>
</template>

<script>
export default {
  name: 'Grid',
  model: {
    prop: 'gridData',
    event: 'onGridClicked'
  },
  props: {
    gridData: {
      type: Object, // gridIndex: 99, actionArray: [ 0, 1, 2, 3 ]
      required: true
    }
  },
  data: function () {
    return {}
  },
  methods: {
    onGridClicked: function (index) {
      this.$emit('onGridClicked', index)
    }
  }
}
</script>

<style scoped>
.grid {
  align-self: stretch;
  flex-grow: 1;
}
</style>
