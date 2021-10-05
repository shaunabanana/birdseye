<template>
  <div class="app" @click.stop="mapping = false">
    <projection-mapper :focused="mapping" @click.stop="mapping = !mapping">
      <tweets :robots="robots" ref="tweets"/>
    </projection-mapper>
  </div>
</template>

<script>
import ProjectionMapper from "./components/ProjectionMapper";
import Tweets from "./components/Tweets";

import ToioConnector from "./toio";

export default {
  name: "App",
  components: {
    ProjectionMapper,
    Tweets,
  },


  data: () => ({
    mapping: false,

    robots: [
      { id: '0', type: 'robot', name: null, linked: [], x: 0, y: 0, fx: 100, fy: 100 },
      { id: '1', type: 'robot', name: null, linked: [], x: 0, y: 0, fx: 100, fy: 100 },
      { id: '2', type: 'robot', name: null, linked: [], x: 0, y: 0, fx: 100, fy: 100 },
      { id: '3', type: 'robot', name: null, linked: [], x: 0, y: 0, fx: 100, fy: 100 },
    ],

  }),

  mounted () {
    this.toio = new ToioConnector();
    this.toio.onConnect = this.onToioConnect.bind(this);
    this.toio.onMove = this.onToioMove.bind(this);
  },

  methods: {
    getRobotByName(name) {
      for (let robot of this.robots) {
        if (robot.name === name) {
          return robot;
        }
      }
      return null;
    },

    onToioConnect (event) {
      for (let robot of this.robots) {
        if (robot.name === null) {
          robot.name = event.name;
          console.log('Robot', robot.id, robot.name);
          break;
        }
      }
    },

    onToioMove (event) {
      let robot = this.getRobotByName(event.cube);
      robot.x = robot.fx = event.x;
      robot.y = robot.fy = event.y;
      robot.angle = event.angle;
    }
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
