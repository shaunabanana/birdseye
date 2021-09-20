<template>
  <div class="app" @click.stop="mapping = false">
    <projection-mapper :focused="mapping" @click.stop="mapping = !mapping">
      <tweets />
    </projection-mapper>
  </div>
</template>

<script>
import ProjectionMapper from "./components/ProjectionMapper";
import Tweets from "./components/Tweets";

export default {
  name: "App",
  components: {
    ProjectionMapper,
    Tweets,
  },


  data: () => ({
    mapping: false
  }),

  mounted () {
  },

  methods: {
  },

  watch: {
  }
};
</script>


<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;

  background: black;
  color: white;
}

.app {
  width: 100%;
  height: 100%;
}

</style>
