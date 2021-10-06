
<template>
  <div class="tweet" ref="tweet">
    <div 
      class="avatar"
      :style="{
        'background-image': `url(${node.avatar})`,
      }"
    >
    </div>

    <div v-if="seleted" class="content" :style="contentBackground">
      {{tweetContent}}
    </div>

  </div>
</template>

<script>

export default {
  name: 'Tweet',
  components: {},
  props: ['tweetContent'],

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
  }),

  mounted () {
    this.dataLoader = new DataLoader('./dataset');
    this.dataLoader.loadData(tweets => {
      this.nodes = this.robots.concat(tweets);
      this.startSimulation();
    });
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

/* 头像+content整体的样式 */
.tweet {
  position: absolute;
  width: 50px;
  height: 50px;
  left: -25px;
  top: -25px;
  overflow: visible;
}

/* 默认头像的样式 */
.avatar {
  width: 50px; /* 这边可不可以直接等于一个default头像大小的变量，这样就不用每次每个地方都要改 */
  height: 50px;
  background-size: 50px 50px;
  border-radius: 50%; 
  overflow: hidden;
}

/* 被选中的头像的样式 */
/* 需考虑加border之后 会不会被overflow切掉 */
.avatar.selected {
  transform: scale(2.0);
  border: 2px solid #00FFE0;
}

.avatar.browsing {
  transform: scale(1.2);
  opacity: 0.8;
}

.avatar.browsing.related {
  transform: scale(1.6);
  border: 2px solid #ffffff;
}

.avatar.shrinked {
  transform: scale(0.4);
  opacity: 0.6;
}

.avatar.shrinked.related {
  transform: scale(0.8);
  opacity: 1;
}

.content {
  width: 100px; 
  height: 400px; /* flexible */
  background-size: 50px 50px;  /* 和上面长宽的区别是？ */
  background-color: #333333;
  opacity: 0.2;
  border-radius: 6%; 
  overflow: hidden;
}

.contentText {
  font-family: "Open Sans";
  color: #14171a;
  font-size: 14px;
  line-height: 20px;
}
</style>
