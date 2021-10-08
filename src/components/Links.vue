<template>
  <svg>
    <defs>
      <linearGradient v-for="reply in replies" :key="reply.from.id + reply.to.id"
        :id="reply.from.id + reply.to.id" gradientUnits="userSpaceOnUse"
        :x1="reply.from.x" :y1="reply.from.y" :x2="reply.to.x" :y2="reply.to.y">
        <stop offset="0%" style="stop-color:#888"/>
        <stop offset="100%" style="stop-color:#111"/>
      </linearGradient>

      <linearGradient v-for="link in links" :key="link.from.id + link.to.id"
        :id="link.from.id + link.to.id" gradientUnits="userSpaceOnUse"
        :x1="link.from.x" :y1="link.from.y" :x2="link.to.x" :y2="link.to.y">
        <stop offset="0%" style="stop-color:#888"/>
        <stop offset="10%" style="stop-color:#444"/>
        <stop offset="30%" style="stop-color:#222"/>
        <stop offset="50%" style="stop-color:#111"/>
        <stop offset="70%" style="stop-color:#222"/>
        <stop offset="90%" style="stop-color:#444"/>
        <stop offset="100%" style="stop-color:#888"/>
      </linearGradient>
    </defs>
    <line class="reply" v-for="reply in replies" :key="reply.from.id + reply.to.id"
      :x1="reply.from.x" :y1="reply.from.y" :x2="reply.to.x" :y2="reply.to.y"
      :style="{stroke: `url(#${reply.from.id + reply.to.id})`}"></line>

    <line class="link" v-for="link in links" :key="link.from.id + link.to.id"
      :x1="link.from.x" :y1="link.from.y" :x2="link.to.x" :y2="link.to.y"
      :style="{stroke: `url(#${link.from.id + link.to.id})`}"
    ></line>
  </svg>
</template>
<script>
export default {
  name: "Links",
  components: {},

  props: {
    links: Array,
    replies: Array
  },

  data: () => ({
    
  }),

  mounted() {
    
  },

  methods: {
    
  }
};
</script>


<style>
svg {
  width: 100vw;
  height: 100vh;
}

.reply {
  stroke-width: 1;
}

.link {
  stroke-width: 30;
  stroke-linecap: round;
  stroke: rgba(255, 255, 255, 0.2);
}
</style>
