<template>
  <div class="app" @click.stop="mapping = false">
    <projection-mapper :focused="mapping" @click.stop="mapping = !mapping">
      <div class="title">
        <div class="main">Covid Vaccination</div>
        <div class="sub">tweets in a week</div>
      </div>
      <links :replies="replies" :links="links"/>

      <tweets ref="tweets" :robots="robots" :tweets="tweets" :selected="selectedTweets" />

      <robot v-for="robot in robots" :key="robot.id" :ref="'robot' + robot.id" :name="robot.name"
        :x="robot.x" :y="robot.y" :angle="robot.angle" :keywords="robot.keywords"
        :locked="robot.locked" :expanded="robot.expanded" :linked="robot.linked"
        :selection="robot.selected" :automatic="robot.automatic && robot.linked.length > 0" :related="robot.related"
        :moving="robot.moving"
        :style="{ opacity: robot.active ? 1 : 0 }"
        @browse="onBrowse"
        @browse-linked="onBrowseLinked"
        @rotate="rotateRobot" />
      
    </projection-mapper>
  </div>
</template>

<script>
const Vector = require('victor');

import ProjectionMapper from "./components/ProjectionMapper";
import Tweets from "./components/Tweets";
import Robot from "./components/Robot";
import Links from "./components/Links";

import ToioConnector from "./toio";
import DataLoader from "./dataloader"
import Clusterer from "./clustering"

export default {
  name: "App",
  components: {
    ProjectionMapper,
    Tweets,
    Robot,
    Links
  },

  data: () => ({
    debug: false,

    mapping: false,

    toio: null,
    loader: null,
    clusterer: null,

    robots: [
      { 
        id: '0', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 0,
        active: false, locked: false, expanded: false, keywords: [], linked: [], selected: null,
        related: [], automatic: false, moving: false,
      },
      {
        id: '1', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 1,
        active: false, locked: false, expanded: false, keywords: [], linked: [], selected: null,
        related: [], automatic: false, moving: false,
      },
      { 
        id: '2', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 2,
        active: false, locked: false, expanded: false, keywords: [], linked: [], selected: null,
        related: [], automatic: false, moving: false,
      },
      { 
        id: '3', type: 'robot', name: null, x: 0, y: 0, fx: -200, fy: -200, angle: 0, cluster: 3,
        active: false, locked: false, expanded: false, keywords: [], linked: [], selected: null,
        related: [], automatic: false, moving: false,
      },
    ],
    tweets: [],
    replies: [],

    focus: null,
  }),

  mounted () {
    this.toio = new ToioConnector();
    this.toio.onConnect = this.onToioConnect.bind(this);
    this.toio.onActivate = this.onToioActivate.bind(this);
    this.toio.onDeactivate = this.onToioDeactivate.bind(this);
    this.toio.onMove = this.onToioMove.bind(this);
    this.toio.onExpand = this.onToioExpand.bind(this);
    this.toio.onDump = this.onToioDump.bind(this);
    this.toio.onLink = this.onToioLink.bind(this);

    this.loader = new DataLoader('./dataset');
    this.loader.loadData().then(tweets => {
      console.log(tweets);
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

    getTweetById(id) {
      for (let tweet of this.tweets) {
        if (tweet.id === id) {
          return tweet;
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
      else {
        event.x = (event.x - 52) / (625 - 52) * window.innerHeight * 1.414
        event.y = (event.y - 479) / (886 - 479) * window.innerHeight
      }
      
      robot.x = robot.fx = event.x;
      robot.y = robot.fy = event.y;
      robot.deltaAngle = event.angle - robot.angle;
      robot.angle = event.angle;
      robot.moving = event.moving;
    },

    onToioExpand (event) {
      let robot = this.getRobotByName(event.cube);
      if (robot.linked.length > 0) return;
      robot.expanded = !robot.expanded;
      if (!robot.expanded && this.focus) {
        let tweet = this.getTweetById(this.focus);
        if (tweet.cluster === robot.cluster) {
          this.focus = null;
          this.updateReplies();
        }
      }
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

    onToioLink (event) {
      let from = this.getRobotByName(event.from);
      let to = this.getRobotByName(event.to);
      
      if (from.linked.includes(to.name) && to.linked.includes(from.name)) {
        from.linked = from.linked.filter(name => name !== to.name);
        to.linked = to.linked.filter(name => name !== from.name);
        from.expanded = false;
        to.automatic = false;
        to.expanded = false;
        to.automatic = false;

        let tweet = this.getTweetById(this.focus);
        if (tweet.cluster === from.cluster || tweet.cluster === to.cluster ) {
          this.focus = null;
          this.updateReplies();
        }

      } else {
        from.linked.push(to.name);
        to.linked.push(from.name);
        from.expanded = true;
        to.expanded = true;
      }
    },

    onBrowse (event) {
      // console.log('Linked browsing', event.cube, event.tweet);
      this.focus = event.tweet;
      this.caluclateRelatedTweets();
    },

    onBrowseLinked (event) {
      // console.log('Linked browsing', event.cube, event.tweet);
      this.focus = event.tweet;
      let robot = this.getRobotByName(event.cube);
      this.caluclateRelatedTweets();
      this.setLinkedAutomatic(robot.name, true)
      robot.automatic = false;
    },

    rotateRobot (event) {
      let robot = this.getRobotByName(event.cube);
      let tweet = this.getTweetById(event.tweet);
      // console.log('Rotating robot to tweet', event.cube, tweet.content)

      let deltaPos = Vector(tweet.x, tweet.y).subtract(Vector(robot.x, robot.y));
      let angle = deltaPos.angleDeg();
      if (angle < 0) angle += 360;

      this.toio.rotate(event.cube, angle);

    },

    setLinkedAutomatic (current, value, visited) {
      if (!visited) visited = new Set();
      if (visited.has(current)) return;

      let robot = this.getRobotByName(current);
      if (visited.size > 0) {
        robot.automatic = value;
        // console.log(this.$refs['robot' + robot.id].updateRotation);
        // this.$refs['robot' + robot.id].updateRotation();
      }

      visited.add(current);
      for (let robotName of robot.linked) {
        this.setLinkedAutomatic(robotName, value, visited);
      }
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
    },

    updateReplies() {
      let replies = [];
      if (this.focus) {
        let tweet = this.getTweetById(this.focus);

        if (tweet.replyTo) {
          let replyToTweet = this.getTweetById(tweet.replyTo);
          replies.push({ from: replyToTweet, to: tweet });
        }

        tweet.replies.forEach(tweetId => {
          let reply = this.getTweetById(tweetId);
          replies.push({ from: tweet, to: reply });
        })
      }
      this.replies = replies;
    },

    caluclateRelatedTweets () {
      this.updateReplies();
      let related = {};
      if (this.focus) {
        let tweet = this.getTweetById(this.focus);

        if (tweet.replyTo) {
          let replyToTweet = this.getTweetById(tweet.replyTo);
          if (!related[replyToTweet.cluster]) related[replyToTweet.cluster] = new Set();
          related[replyToTweet.cluster].add(tweet.replyTo);
        }

        tweet.replies.forEach(tweetId => {
          let reply = this.getTweetById(tweetId);
          if (!related[reply.cluster]) related[reply.cluster] = new Set();
          related[reply.cluster].add(tweetId);
        })

        this.activeRobots.forEach(robot => {
          if (!related[robot.cluster]) related[robot.cluster] = new Set();
          if (related[robot.cluster].size < 4) {
            let tweets = this.tweets.filter(t => t.cluster);
            let vec = Vector.fromArray(tweet.vector);
            tweets.sort( (t1, t2) => {
              let vec1 = Vector.fromArray(t1.vector);
              let vec2 = Vector.fromArray(t2.vector);
              let cos1 = vec1.dot(vec) / (vec1.length() * vec.length());
              let cos2 = vec2.dot(vec) / (vec2.length() * vec.length());
              return cos1 - cos2
            });
            // console.log(tweets);
            let sliceSize = 4 - related[robot.cluster].size;
            tweets = tweets.slice(0, sliceSize);
            // console.log(tweets);
            tweets.forEach(t => {
              related[robot.cluster].add(t.id);
            });
          }
        })
      }

      Object.keys(related).forEach(id => {
        this.robots[id].related = [...related[id]];
      })
    },
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
        let robotPos = Vector(robot.x, robot.y);
        let robotAngle = Vector(1, 0).rotateDeg(robot.angle).angleDeg();
        
        let angles = tweets.map(tweet => {
          let angle = Vector(tweet.x, tweet.y).subtract(robotPos).angleDeg();
          return Math.abs(angle - robotAngle);
        });
        
        let selectedIndex = angles.indexOf(Math.min(...angles));
        if (tweets[selectedIndex]) {
          selected.push(tweets[selectedIndex].id);
          robot.selected = tweets[selectedIndex].id;
        }
      });
      return selected;
    },

    links() {
      let links = [], mapping = {};
      this.activeRobots.forEach(robot => {
        robot.linked.forEach(robotName => {
          if (!mapping[robot.name]) mapping[robot.name] = [];
          if (!mapping[robotName]) mapping[robotName] = [];

          if (mapping[robot.name].includes(robotName)) return;
          if (mapping[robotName].includes(robot.name)) return;

          mapping[robot.name].push(robotName);
          links.push({
            from: robot,
            to: this.getRobotByName(robotName)
          })
        });
      });
      return links;
    },

    hasLinks () {
      let result = false;
      this.activeRobots.forEach(robot => {
        if (robot.linked.length > 0) result = true;
      });
      return result;
    },
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

.title {
  position: absolute;
  top: 1rem;
  left: calc(1.414 * 100vh / 2);
  width: 300px;
  transform: translate(-50%, 0);
  text-align: center;
}

.title .main {
  font-size: 2rem;
  color: white;
}

.title .sub {
  font-size: 1rem;
  color: #a692ec;
}

</style>
