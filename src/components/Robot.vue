<template>
  <div class="robot" ref="robot"
  :style="{
    'transform': `translate(${x}px, ${y}px) scale(1.0) rotate(${angle ? angle : 0}deg)`
  }">
    {{ locked ? "locked" : "" }}

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
    x: Number, y: Number, angle: Number,
    keywords: Array,
    locked: Boolean,
  },

  data: () => ({
  }),

  mounted () {
  },

  watch: {
  },

  methods: {}
}
</script>


<style scoped>

.robot {
  cursor: pointer;
}

.robot {
  position: absolute;
  width: calc(var(--scale) * 60px);
  height: calc(var(--scale) * 60px);
  left: calc(var(--scale) * -30px);
  top: calc(var(--scale) * -30px);
  overflow: visible;
  color: white;
  text-align: center;
  background: gray;
}

.keyword {
  position: absolute;
  top: 30px;
  left: 30px;
  color: white;
}

</style>
