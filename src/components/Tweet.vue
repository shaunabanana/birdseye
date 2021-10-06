
<template>
  <div class="tweet" ref="tweet">
    <div 
      class="avatar"
      :class="{
        selected: selected,
        browsing: browsing,
        shrinked: shrinked,
        related: related
      }"
      :style="{
        'background-image': `url(${avatar})`,
      }"
    >
    </div>

    <div class="content" 
        :style="{ opacity:selected ? 1:0 }">
      {{detailed ? content : content.slice(0, 80)}}
    </div>

  </div>
</template>

<script>

export default {
  name: 'Tweet',
  components: {},
  props: ['avatar', 'selected', 'browsing', 'shrinked', 'related', 'content', 'detailed'],

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
  }),

  mounted () {
    
  },

  methods: {

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
