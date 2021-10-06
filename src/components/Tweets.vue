<template>
  <div class="tweets" ref="tweets">
    <div v-for="node in nodes" :key="node.id"
      :class="node.type"
      :style="{
        'background-image': `url(${node.avatar})`,
        'transform': `translate(${node.x}px, ${node.y}px) scale(${selected.includes(node.id) ? 2 : 1}) rotate(${node.angle ? node.angle : 0}deg)`
      }">
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { forceAttract } from 'd3-force-attract'
const Victor = require('victor');

export default {
  name: 'Tweets',
  components: {},
  props: {
    robots: Array,
    tweets: Array,
    selected: Array
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
        .radius(d => d.type === 'robot' ? 65 : (this.selected.includes(d.id) ? 45 : 25));
      
      // Update browsing targets
      this.simulation.force('browse')
        .target(d => {
          if (d.type === 'robot') return [0, 0];
          else if (d.cluster === -1) return [0, 0];

          let robot = this.robots[d.cluster];
          let robotPos = Victor(robot.x, robot.y);
          let radius = this.clusterSizes[d.cluster] * 55 / Math.PI / 2;

          let deltaPos = Victor(d.x, d.y).subtract(robotPos).norm();

          let target = deltaPos.multiply(Victor(radius, radius)).add(robotPos);
          
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

  },

  computed: {
    clusterSizes () {
      let sizes = {};
      this.tweets.forEach( tweet => {
        if (!sizes[tweet.cluster]) sizes[tweet.cluster] = 0;
        sizes[tweet.cluster] ++;
      })
      return sizes;
    }
  }
}
</script>


<style>

:root {
  --scale: 1.0;
}

.tweets {
  width: 100%;
  height: 100%;
}

/* .robot {
  cursor: pointer;
} */

.tweet {
  position: absolute;
  width: calc(var(--scale) * 30px);
  height: calc(var(--scale) * 30px);
  left: calc(var(--scale) * -15px);
  top: calc(var(--scale) * -15px);
  background-size: calc(var(--scale) * 30px) calc(var(--scale) * 30px);
  border-radius: 25px;
  overflow: hidden;
}

</style>
