<template>
  <svg class="tweets" ref="tweets">
  </svg>
</template>

<script>
import * as d3 from "d3";
// import { forceCluster } from 'd3-force-cluster'
import { drag } from 'd3-drag'
import { forceAttract } from 'd3-force-attract'

export default {
  name: 'Tweets',
  components: {
  },
  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    tweets: [
      {id: 0, type: 'robot', cluster: 0, x: 200, y: 200, fx: 200, fy: 200},
      {id: 1, type: 'robot', cluster: 1, x: 500, y: 200, fx: 500, fy: 200},
      {id: 2, type: 'robot', cluster: 2, x: 200, y: 500, fx: 200, fy: 500},
      {id: 3, type: 'robot', cluster: 3, x: 500, y: 500, fx: 500, fy: 500},
      
      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},

      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 5, type: 'tweet', text: 'Hi!', cluster: 0},
      {id: 6, type: 'tweet', text: 'Yo!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 9, type: 'tweet', text: 'Bon journee!', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},

      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 5, type: 'tweet', text: 'Hi!', cluster: 0},
      {id: 6, type: 'tweet', text: 'Yo!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 9, type: 'tweet', text: 'Bon journee!', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 18, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 19, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 20, type: 'tweet', text: 'Ciao!', cluster: 3},

      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},

      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 5, type: 'tweet', text: 'Hi!', cluster: 0},
      {id: 6, type: 'tweet', text: 'Yo!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 9, type: 'tweet', text: 'Bon journee!', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},

      {id: 4, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 5, type: 'tweet', text: 'Hi!', cluster: 0},
      {id: 6, type: 'tweet', text: 'Yo!', cluster: 0},
      {id: 7, type: 'tweet', text: 'Hello!', cluster: 0},
      {id: 8, type: 'tweet', text: 'Ca va bien', cluster: 1},
      {id: 9, type: 'tweet', text: 'Bon journee!', cluster: 1},
      {id: 10, type: 'tweet', text: 'Comment ca va?', cluster: 1},
      {id: 11, type: 'tweet', text: 'Bonjour!', cluster: 1},
      {id: 12, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 13, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 14, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 15, type: 'tweet', text: 'Hola!', cluster: 2},
      {id: 17, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 18, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 19, type: 'tweet', text: 'Ciao!', cluster: 3},
      {id: 20, type: 'tweet', text: 'Ciao!', cluster: 3},
    ],

    robots: [
      {id: 0, cluster: 0, x: 200, y: 200, fx: 200, fy: 200, angle: 0},
      {id: 1, cluster: 1, x: 500, y: 200, fx: 500, fy: 200, angle: 0},
      {id: 2, cluster: 2, x: 200, y: 500, fx: 200, fy: 500, angle: 0},
      {id: 3, cluster: 3, x: 500, y: 500, fx: 500, fy: 500, angle: 0},
    ]
  }),

  mounted () {

    this.drag = drag();

    for (let tweet of this.tweets) {
      if (tweet.type === 'tweet') {
        if (!this.clusterSize[tweet.cluster]) this.clusterSize[tweet.cluster] = 0;
        this.clusterSize[tweet.cluster] += 1;
      }
    }
    
    this.drawTweets();
    this.drawRobots();
    this.startSimulation();

    window.addEventListener('keypress', this.updateSimulation.bind(this))
  },

  methods: {

    drawTweets() {
      d3.select(this.$refs.tweets)
        .selectAll('circle')
        .data(this.tweets)
        .enter()
        .append('circle')
        .attr('r', 15)
        .attr('fill', d => d.type === 'robot' ? 'white' : 'gray');
    },

    drawRobots() {
      d3.select(this.$refs.tweets)
        .selectAll('rect')
        .data(this.robots)
        .enter()
        .append('rect')
        .attr('id', d => d.id)
        .attr('style', 'cursor: grab;')
        .attr('x', d => d.x - 25)
        .attr('y', d => d.y - 25)
        .attr('width', 50)
        .attr('height', 50)
        .attr('fill', 'white')
        .on('click', this.robotClicked.bind(this))
        .call(d3.drag()
          // .on("start", (event, d) => circle.filter(p => p === d).raise().attr("stroke", "black"))
          .on("drag", (event, d) => (d.x = event.x, d.y = event.y))
          // .on("end", (event, d) => circle.filter(p => p === d).attr("stroke", null))
          .on("start.update drag.update end.update", this.updateSimulation.bind(this)));
    },

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
      this.simulation = d3.forceSimulation(this.tweets)
        // Prevent overlapping nodes.
        .force('collision', d3.forceCollide()
          .radius(d => d.type === 'robot' ? 40 : 20))
        
        // A clustering force towards the robot.
        .force('cluster', forceAttract()
          .target(d => {
            return [this.robots[d.cluster].x, this.robots[d.cluster].y]
          })
          .strength(() => 0.2 + (Math.random() * 0.1 - 0.05))
        )

        .on('tick', () => {
          d3.selectAll('circle')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y)
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

      // Update robot positions
      d3.select(this.$refs.tweets)
        .selectAll('rect')
        .attr('x', d => d.x - 25)
        .attr('y', d => d.y - 25)

    }

  }
}
</script>


<style scoped>

.tweets {
  width: 100%;
  height: 100%;
}

.robot {
  cursor: pointer;
}

</style>
