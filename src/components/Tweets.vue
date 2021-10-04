<template>
  <div class="tweets" ref="tweets">
    <div v-for="node in nodes" :key="node.id"
      :class="node.type"
      :style="{
        'background-image': `url(${node.avatar})`,
        'transform': `translate(${node.x}px, ${node.y}px) scale(1.0)`
      }"
    >
    </div>

  </div>
</template>

<script>
import * as d3 from "d3";
// import { drag } from 'd3-drag'
import { forceAttract } from 'd3-force-attract'
import DataLoader from "../dataloader"
import Clusterer from "../clustering"

export default {
  name: 'Tweets',
  components: {},

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
    tweets: [],

    robots: [
      { id: '0', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
      { id: '1', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
      { id: '2', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
      { id: '3', type: 'robot', x: 0, y: 0, fx: 100, fy: 100 },
    ]
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

  methods: {

    robotClicked(event) {
      let robotId = Number.parseInt(d3.select(event.target).attr('id'));
      // let robot = this.robots[robotId];
      
      if (this.selection.has(robotId)) {
        d3.select(event.target).attr('fill', 'white');
        this.selection.delete(robotId);

      } else {
        d3.select(event.target).attr('fill', 'cyan');
        this.selection.add(robotId);
      }

      // Set robot repel radius based on whether the robot is grabbed
      this.simulation.force('collision')
        .radius(d => {
          if (d.type === 'robot') {
            if (this.selection.has(d.id)) {
              // Make the selection a circle
              let circumference = this.clusterSize[d.id] * 20 * 0.9 * 2;
              return circumference / Math.PI / 2;
            } else {
              return 40;
            }
          } else {
            return 20;
          }
        })
      this.simulation.alphaTarget(0.1).restart();
      
      event.stopPropagation();
    },

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
          .strength(() => 0.05 + (Math.random() * 0.1 - 0.05))
        )

        .on('tick', () => {
          this.nodes = this.nodes.map(v => v);
        });
    },

    updateSimulation() {
      // Update data. This is just code for testing.
      // The robot positions should come from TOIO.
      for (let i in this.robots) {
        this.tweets[i].fx = this.robots[i].x;
        this.tweets[i].fy = this.robots[i].y;
      }

      // Update cluster locations
      this.simulation.force('cluster')
        .target(d => [this.robots[d.cluster].x, this.robots[d.cluster].y])

      // Reset alpha and restart simulation
      this.simulation.alphaTarget(0.1).restart();

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
