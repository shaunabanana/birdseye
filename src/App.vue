<template>
  <div class="app" @click="focused = false">
    <Moveable class="moveable" v-bind="moveable" @warp="warp">
      <Tweets />
    </Moveable>
  </div>
</template>
<script>
import Moveable from "vue-moveable";

import Tweets from "./components/Tweets";

export default {
  name: "App",
  components: {
    Moveable,
    Tweets,
  },


  data: () => ({
    moveable: {
      warpable: true,
    },
    focused: false
  }),

  mounted () {
    document.querySelector('.moveable-control-box').classList.add('hidden');
    document.querySelector('.moveable').addEventListener('click', (e) => {
      this.focused = !this.focused;
      e.stopPropagation();
    })
  },

  methods: {
    warp({ target, transform }) {
      target.style.transform = transform;
    },
  },

  watch: {
    focused (value) {
      console.log(value);
      if (value) document.querySelector('.moveable-control-box').classList.remove('hidden');
      else document.querySelector('.moveable-control-box').classList.add('hidden');
    }
  }
};
</script>


<style>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;

  background: black;
  color: white;
}

.app, .moveable {
  width: 100%;
  height: 100%;
}

.hidden { visibility: hidden; }
</style>
