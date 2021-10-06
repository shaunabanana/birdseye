<template>
  <div class="app" @click.stop="mapping = false">
    <projection-mapper :focused="mapping" @click.stop="mapping = !mapping">
      <tweets ref="tweets" :robots="robots" :tweets="tweets" :selected="selectedTweets"/>

      <robot v-for="robot in robots" :key="robot.id"
        :x="robot.x" :y="robot.y" :angle="robot.angle" :keywords="robot.keywords"
        :locked="robot.locked" :expanded="robot.expanded"
        :style="{ opacity: robot.active ? 1 : 0 }"/>
      
    </projection-mapper>
  </div>
</template>

<script>
const Victor = require('victor');

import ProjectionMapper from "./components/ProjectionMapper";
import Tweets from "./components/Tweets";
import Robot from "./components/Robot";

import ToioConnector from "./toio";
import DataLoader from "./dataloader"
import Clusterer from "./clustering"

export default {
  name: "App",
  components: {
    ProjectionMapper,
    Tweets,
    Robot
  },

  data: () => ({
    debug: true,

    mapping: false,

    toio: null,
    loader: null,
    clusterer: null,

    robots: [
      { 
        id: '0', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 0,
        active: false, locked: false, expanded: false, keywords: []
      },
      {
        id: '1', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 1,
        active: false, locked: false, expanded: false, keywords: []
      },
      { 
        id: '2', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 2,
        active: false, locked: false, expanded: false, keywords: []
      },
      { 
        id: '3', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 3,
        active: false, locked: false, expanded: false, keywords: []
      },
    ],
    tweets: [],
    links: [],
    clusterLinks: [],

  }),

  mounted () {
    this.toio = new ToioConnector();
    this.toio.onConnect = this.onToioConnect.bind(this);
    this.toio.onActivate = this.onToioActivate.bind(this);
    this.toio.onDeactivate = this.onToioDeactivate.bind(this);
    this.toio.onMove = this.onToioMove.bind(this);
    this.toio.onExpand = this.onToioExpand.bind(this);
    this.toio.onDump = this.onToioDump.bind(this);

    this.loader = new DataLoader('./dataset');
    this.loader.loadData().then(tweets => {
      this.tweets = tweets;
    });

    this.clusterer = new Clusterer();
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
      // Find an empty spot for the robot
      for (let robot of this.robots) {
        if (robot.name === null) {
          robot.name = event.name;
          return;
        }
      }
    },

    onToioActivate (event) {
      console.log('Toio Acticated.', event);
      let robot = this.getRobotByName(event.cube);
      robot.active = true;
      this.clusterTweets();
    },

    onToioDeactivate (event) {
      let robot = this.getRobotByName(event.cube);
      robot.active = false;
      this.$refs.tweets.updateForces();
    },

    onToioMove (event) {
      let robot = this.getRobotByName(event.cube);
      if (this.debug) {
        event.x = (event.x - 347) / (649 - 347) * window.innerHeight * 1.414
        event.y = (event.y - 262) / (454 - 262) * window.innerHeight
      }
      robot.x = robot.fx = event.x;
      robot.y = robot.fy = event.y;
      robot.deltaAngle = event.angle - robot.angle;
      robot.angle = event.angle;
    },

    onToioExpand (event) {
      let robot = this.getRobotByName(event.cube);
      robot.expanded = !robot.expanded;
      console.log('Expand', robot);
    },

    onToioDump (event) {
      let from = this.getRobotByName(event.from);
      let to = this.getRobotByName(event.to);

      this.tweets.forEach(tweet => {
        if (tweet.cluster === from.cluster) {
          tweet.cluster = to.cluster;
        }
      });
      to.locked = true;
      this.$refs.tweets.updateForces();
    },

    // (Re)cluster tweets according to current number of active & unlocked robots
    clusterTweets () {
      this.clusterer.cluster(this.activeRobots, this.activeTweets, this.numClusters).then(result => {

        this.activeTweets.forEach((tweet, i) => {
          // labels start from zero, so we subtract one to get cluster index.
          // let robot = this.activeRobots[result.labels[i] - 1];
          tweet.cluster = result[i]; 
        })
        this.$refs.tweets.updateForces();

        this.clusterer.keyword(this.tweets).then(result => {
          for (let index of Object.keys(result)) {
            this.robots[index].keywords = result[index];
            this.unlockClusters();
          }

        })
      });
    },

    unlockClusters() {
      this.robots.forEach(robot => {
        if (robot.active) robot.locked = false;
      })
    }
  },

  computed: {
    numClusters () {
      let numClusters = 0;
      for (let robot of this.robots) {
        if (robot.active && !robot.locked) numClusters++;
      }
      return numClusters;
    },

    activeRobots () {
      return this.robots.filter( robot => robot.active && !robot.locked );
    },

    activeTweets () {
      return this.tweets.filter( tweet => 
        tweet.cluster === -1 || 
        (this.robots[tweet.cluster].active && !this.robots[tweet.cluster].locked) );
    },

    currentClustering () {
      let clustering = {};
      this.activeTweets.forEach( tweet => {
        if (!clustering[tweet.cluster]) clustering[tweet.cluster] = [];
        clustering[tweet.cluster].push(tweet.id);
      });
      return clustering;
    },

    selectedTweets () {
      let selected = [];
      this.robots.forEach( robot => {
        if (!robot.active || !robot.expanded) return;
        let tweets = this.tweets.filter( tweet => tweet.cluster === robot.cluster);
        let robotPos = Victor(robot.x, robot.y);
        let robotAngle = Victor(0, 1).rotateDeg(robot.angle).angleDeg();
        
        let angles = tweets.map(tweet => {
          let angle = Victor(tweet.x, tweet.y).subtract(robotPos).angleDeg();
          return Math.abs(angle - robotAngle);
        });
        
        let selectedIndex = angles.indexOf(Math.min(...angles));
        selected.push(tweets[selectedIndex].id);
      });
      return selected;
    }
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
  font-family: 'Open Sans', sans-serif;
}

.app {
  width: calc(1.414 * 100vh);
  height: 100vh;
}

</style>
