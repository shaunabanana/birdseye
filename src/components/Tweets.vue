<template>
  <div class="tweets" ref="tweets">
    <div v-for="node in nodes" :key="node.id"
      :class="node.type"
      :style="{
        'background-image': `url(${node.avatar})`,
        'transform': `translate(${node.x}px, ${node.y}px) scale(1.0) rotate(${node.angle ? node.angle : 0}deg)`
      }">
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
// import { drag } from 'd3-drag'
import { forceAttract } from 'd3-force-attract'

export default {
  name: 'Tweets',
  components: {},
  props: {
    robots: Array,
    tweets: Array
  },

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
    clusterReady: false

    // robots: [
    //   { id: '0', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '1', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '2', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '3', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    // ]
  }),

  mounted () {
    // this.dataLoader = new DataLoader('./dataset');
    // this.dataLoader.loadData(tweets => {
    //   this.nodes = this.robots.concat(tweets);
    //   this.tweets = tweets;
    //   this.startSimulation();
    //   this.clusterer.cluster(this.tweets, 4);
    // });

    // this.clusterer = new Clusterer();
  },

  watch: {
    robots: {
      deep: true,
      handler () {
        // this.simulation.data(this.robots);
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
          .radius(d => d.type === 'robot' ? (d.active ? 65 : 65) : 25))
        
        // A clustering force towards the center of the screen.
        .force('cluster', forceAttract()
          .target(() => {
            return [(window.innerHeight * 1.414) / 2, window.innerHeight / 2]
          })
          .strength(d => d.type === 'robot' ? 0 : 0.02 + (Math.random() * 0.03 - 0.015))
        )

        .on('tick', () => {
          this.nodes = this.nodes.map(v => v);
        });
    },

    updateClusterForces() {
      // Update cluster locations
      this.simulation.force('cluster')
        .target(d => [this.robots[d.cluster].x, this.robots[d.cluster].y])
        .strength(d => d.type === 'robot' ? 0 : 0.07 + (Math.random() * 0.1 - 0.05))
      this.clusterReady = true;
    },

    restartSimulation() {
      if (this.clusterReady) this.updateClusterForces();
      // Reset alpha and restart simulation
      if (this.simulation) this.simulation.alphaTarget(0.1).restart();
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

/* .robot {
  position: absolute;
  width: calc(var(--scale) * 60px);
  height: calc(var(--scale) * 60px);
  left: calc(var(--scale) * -30px);
  top: calc(var(--scale) * -30px);
  background: white;
  overflow: visible;
} */

</style>
