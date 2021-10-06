<template>
  <div class="tweets" ref="tweets">
    <!-- <div v-for="node in nodes" :key="node.id"
      :class="node.type"
      :style="{
        'background-image': `url(${node.avatar})`,
        'transform': `translate(${node.x}px, ${node.y}px) scale(1.0) rotate(${node.angle ? node.angle : 0}deg)`
      }"
    >
    </div> -->
    <tweet :avatar="tweets[0].avatar" :content="tweets[0].content" style="transform: translate(100px, 100px)"
      :browsing="true" :selected="true"/>

  </div>
</template>

<script>
import * as d3 from "d3";
// import { drag } from 'd3-drag'
import { forceAttract } from 'd3-force-attract'
import DataLoader from "../dataloader"
import Clusterer from "../clustering"

import Tweet from "./Tweet"

export default {
  name: 'Tweets',
  components: {Tweet},
  props: {
    robots: Array,
  },

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
    tweets: [],

    // robots: [
    //   { id: '0', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '1', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '2', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    //   { id: '3', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    // ]
  }),

  mounted () {
    this.dataLoader = new DataLoader('./dataset');
    this.dataLoader.loadData(tweets => {
      this.nodes = this.robots.concat(tweets);
      this.tweets = tweets;
      this.startSimulation();
      this.clusterer.cluster(this.tweets, 4);
    });

    this.clusterer = new Clusterer();
  },

  watch: {
    robots: {
      deep: true,
      handler () {
        this.restartSimulation();
      }
    }
  },

  methods: {

    startSimulation() {
      this.simulation = d3.forceSimulation(this.nodes)
        // Prevent overlapping nodes.
        .force('collision', d3.forceCollide()
          .radius(d => d.type === 'robot' ? 80 : 40))
        
        // A clustering force towards the center of the screen.
        .force('cluster', forceAttract()
          .target(() => {
            return [500, 500]
          })
          .strength(d => d.type === 'robot' ? 0 : 0.05 + (Math.random() * 0.1 - 0.05))
        )

        .on('tick', () => {
          this.nodes = this.nodes.map(v => v);
        });
    },

    restartSimulation() {
      // Update cluster locations
      // this.simulation.force('cluster')
      //   .target(d => [this.robots[d.cluster].x, this.robots[d.cluster].y])
      // Reset alpha and restart simulation
      if (this.simulation) this.simulation.alphaTarget(0.1).restart();
    }

  }
}
</script>


<style>

.tweets {
  width: 100%;
  height: 100%;
}

.robot {
  cursor: pointer;
}

.tweet {
  position: absolute;
  width: 50px;
  height: 50px;
  left: -25px;
  top: -25px;
  background-size: 50px 50px;
  border-radius: 25px;
  overflow: hidden;
}

.robot {
  position: absolute;
  width: 100px;
  height: 100px;
  left: -50px;
  top: -50px;
  background: white;
  overflow: hidden;
}

</style>
