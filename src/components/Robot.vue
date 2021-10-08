<template>
  <div class="robot" ref="robot"
  :style="{
    'transform': `translate(${x}px, ${y}px) scale(1.0) rotate(${angle ? angle : 0}deg)`,
    'background': expanded ? `rgb(${255 * 0.15}, ${255 * 0.15}, ${255 * 0.15})` : 'black'
  }">
    <!-- {{ locked ? "locked" : "" }}
    {{ expanded ? "expanded" : "" }}
    {{ automatic ? "automatic" : "" }} -->

    <div class="keyword" v-for="(keyword, index) in keywords" :key="keyword"
    :style="{
      'transform': `translate(-50%, -50%) rotate(${index * 90}deg) translate(0, 50px)`
    }">
      #{{keyword}}
    </div>

  </div>
</template>

<script>

export default {
  name: 'Robot',
  components: {},
  props: {
    name: String,
    x: Number, y: Number, angle: Number,
    keywords: Array,
    locked: Boolean, expanded: Boolean, automatic: Boolean,
    selection: String,
    linked: Array,
    related: Array,
  },

  data: () => ({
    currentRotation: 0,
    rotationTimer: null,
  }),

  mounted () {
  },

  watch: {
    selection () {
      if (this.expanded && this.linked.length > 0 && !this.moving) {
        this.$emit('browse-linked', { cube: this.name, tweet: this.selection });
      } else if (this.expanded && !this.moving) {
        this.$emit('browse', { cube: this.name, tweet: this.selection });
      }
    },

    automatic () {
      this.updateRotation();
    },

    related () {
      this.updateRotation();
    }
  },

  methods: {
    updateRotation () {
      if (this.rotationTimer) {
        // console.log('stopping rotation', this.name);
        clearInterval(this.rotationTimer);
        this.rotationTimer = null;
      }

      if (this.automatic && this.related.length > 0) {
        // console.log('starting rotation', this.name);
        this.currentRotation = 0;
        this.rotationTimer = setInterval(this.rotate.bind(this), 2000);
      }
    },

    rotate() {
      // console.log('in timer callback', this.name);
      if (this.related.length > 0) {
        if (this.currentRotation >= this.related.length) this.currentRotation = 0;
        this.$emit('rotate', { cube: this.name, tweet: this.related[this.currentRotation] });
        // console.log('rotating', this.name, this.related[this.currentRotation]);
        this.currentRotation = (this.currentRotation + 1) % this.related.length;
      } else if (this.rotationTimer) {
        // console.log('stopping rotation (in timer callback)', this.name);
        clearInterval(this.rotationTimer);
        this.rotationTimer = null;
      }
    }
  }
}
</script>


<style scoped>

.robot {
  cursor: pointer;
}

.robot {
  position: absolute;
  width: calc(var(--size) * 2);
  height: calc(var(--size) * 2);
  left: calc(var(--size) * -1);
  top: calc(var(--size) * -1);
  overflow: visible;
  color: white;
  text-align: center;
}

.keyword {
  position: absolute;
  top: var(--size);
  left: var(--size);
  color: white;
}

</style>
