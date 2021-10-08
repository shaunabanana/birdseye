<template>
  <div class="tweets" ref="tweets">
    <tweet v-for="node in nodes" :key="node.id"
      :class="{
        robot: node.type === 'robot',
        expanded: node.expanded,
      }"
      :style="{
        transform: `translate(${node.x}px, ${node.y}px)`,
        width: node.expanded ? `${clusterSizes[node.cluster] * 57 / Math.PI + 30}px` : false,
        height: node.expanded ? `${clusterSizes[node.cluster] * 57 / Math.PI + 30}px` : false,
        top: node.expanded ? `-${clusterSizes[node.cluster] * 57 / Math.PI / 2 + 15}px` : false,
        left: node.expanded ? `-${clusterSizes[node.cluster] * 57 / Math.PI / 2 + 15}px` : false
      }"
      :avatar="node.avatar"
      :content="node.content"
      :sentiment="node.sentiment"
      :robot="node.type === 'robot'"
      :selected="node.type === 'tweet' && selected.includes(node.id)"
      :browsing="robots[node.cluster] ? robots[node.cluster].expanded : false"
      :shrinked="browsing && (robots[node.cluster] ? !robots[node.cluster].expanded : false)"
      :related="related.includes(node.id)"
      />
  </div>
</template>

<script>
import * as d3 from "d3";
import { forceAttract } from 'd3-force-attract'
const Vector = require('victor');

import Tweet from "./Tweet"

export default {
  name: 'Tweets',
  components: {Tweet},
  props: {
    robots: Array,
    tweets: Array,
    selected: Array,
  },

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    nodes: [],
    clusterReady: false,
    targetPoints: {}
  }),

  mounted () {
  },

  watch: {
    robots: {
      deep: true,
      handler () {
        this.restartSimulation();
      }
    },

    tweets () {
      this.nodes = this.robots.concat(this.tweets);
      this.startSimulation();
    }
  },

  methods: {

    startSimulation() {
      this.simulation = d3.forceSimulation(this.nodes)
        // Prevent overlapping nodes.
        .force('collision', d3.forceCollide()
          .radius(d => d.type === 'robot' ? 65 : 25))
        
        // A clustering force towards the center of the screen.
        .force('cluster', forceAttract()
          .target(() => {
            return [(window.innerHeight * 1.414) / 2, window.innerHeight / 2]
          })
          .strength(d => d.type === 'robot' ? 0 : 0.02 + (Math.random() * 0.03 - 0.015))
        )

        // A clustering force towards a designated point on a circle.
        .force('browse', forceAttract()
          .target([0, 0])
          .strength(0)
        )

        .on('tick', () => {
          this.nodes = this.nodes.map(v => v);
        });
    },

    updateForces() {
      // Update collision radius
      this.simulation.force('collision')
        .radius(d => {
          if (d.type === 'robot') return 65;
          if (this.browsing && this.robots[d.cluster] && !this.robots[d.cluster].expanded)
            return 13;
          if (this.selected.includes(d.id)) return 45
          return 25;
        });
      
      // Update browsing targets
      this.simulation.force('browse')
        .target(d => {
          if (d.type === 'robot') return [0, 0];
          else if (d.cluster === -1) return [0, 0];

          let robot = this.robots[d.cluster];
          let robotPos = Vector(robot.x, robot.y);
          let radius = this.clusterSizes[d.cluster] * 57 / Math.PI / 2;
          if (radius < 120) radius = 120;

          let deltaPos = Vector(d.x, d.y).subtract(robotPos).norm();

          let target = deltaPos.multiply(Vector(radius, radius)).add(robotPos);
          
          return [target.x, target.y];
        })
        .strength(d => {
          if (d.type === 'robot') return 0;
          if (!this.robots[d.cluster].expanded) return 0;
          return 1;
        });

      // Update cluster locations
      this.simulation.force('cluster')
        .target(d => [this.robots[d.cluster].x, this.robots[d.cluster].y])
        .strength(d => {
          if (d.type === 'robot') return 0;
          else if (this.robots[d.cluster].expanded) return 0;
          return 0.07 + (Math.random() * 0.1 - 0.05);
        });
      this.clusterReady = true;
    },

    restartSimulation() {
      if (this.clusterReady) this.updateForces();
      // Reset alpha and restart simulation
      if (this.simulation) this.simulation.alphaTarget(0.1).restart();
    },

    clusterRadius(node) {
      return this.clusterSizes[node.cluster] * 57 / Math.PI / 2;
    }

  },

  computed: {
    clusterSizes () {
      let sizes = {};
      this.tweets.forEach( tweet => {
        if (!sizes[tweet.cluster]) sizes[tweet.cluster] = 0;
        sizes[tweet.cluster] ++;
      })
      return sizes;
    },

    browsing () {
      let result = false;
      this.robots.forEach( robot => {
        if (robot.expanded) {
          result = true;
        }
      })
      return result;
    },

    related () {
      let related = [];
      this.robots.forEach( robot => {
        if (robot.related) {
          related = related.concat(robot.related);
        }
      })
      // console.log(related);
      return related;
    }
  }
}
</script>


<style>

.tweets {
  width: 100%;
  height: 100%;
}

.tweet.robot.expanded {
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0px 0px 20px 20px rgba(255, 255, 255, 0.15);
}

</style>
