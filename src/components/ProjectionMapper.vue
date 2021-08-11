<template>
  <Moveable class="moveable" v-bind="moveable" @warp="warp">
    <slot></slot>
  </Moveable>
</template>
<script>
import Moveable from "vue-moveable";

export default {
  name: "ProjectionMapper",
  components: {
    Moveable,
  },

  props: {
    focused: { type: Boolean, default: false, required: true },
  },

  data: () => ({
    moveable: {
      warpable: true,
    },
  }),

  mounted() {
    document.querySelector(".moveable-control-box").classList.add("hidden");
    document.querySelector(".moveable").addEventListener("click", (e) => {
      this.$emit("click", e);
      e.stopPropagation();
    });
  },

  methods: {
    warp({ target, transform }) {
      target.style.transform = transform;
    },
  },

  watch: {
    focused(value) {
      if (value)
        document
          .querySelector(".moveable-control-box")
          .classList.remove("hidden");
      else
        document.querySelector(".moveable-control-box").classList.add("hidden");
    },
  },
};
</script>


<style>
.moveable {
  width: 100%;
  height: 100%;
}

.hidden {
  visibility: hidden;
}
</style>
