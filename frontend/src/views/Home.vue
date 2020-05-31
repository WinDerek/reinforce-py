<template>
  <div class="home">
    <GridWorld />
  </div>
</template>

<script>
// @ is an alias to /src
import GridWorld from '@/components/GridWorld.vue';

export default {
  name: 'Home',
  components: {
    GridWorld,
  },
};
</script>
