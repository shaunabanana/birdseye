
<template>
  <div class="tweet" ref="tweet">
    <div class="avatar"
        :class="{
          selected: selected,
          browsing: browsing,
          shrinked: shrinked,
          related: related
        }"
        :style="{
          'background-image': `url(${avatar})`,
          'box-shadow': robot ? 'none' : `0px 0px 20px 10px rgba(${r}, ${g}, ${b}, ${alpha})`
        }"></div>

    <div class="content left" 
        :style="{ opacity:selected ? 1 : 0 }">
      <div v-for="(line, index) in tweetLines" :key="avatar + index"
          :class="{'reply-line': index === 0 & line.startsWith('Replying')}">
        {{line}}
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: 'Tweet',
  components: {},
  props: {
    robot: Boolean,
    x: Number, y: Number,
    avatar: String, content: String, sentiment: Number,
    browsing: Boolean, 
    selected: Boolean, 
    shrinked: Boolean, 
    related: Boolean, 
    detailed: Boolean
  },

  data: () => ({
    drag: null,
    simulation: null,
    selection: new Set(),
    clusterSize: [],
    nodes: [],
  }),

  mounted () {
    
  },

  computed: {
    r () {
      if (this.sentiment && this.sentiment > 0) {
        return Math.ceil(this.sentiment * 255);
      }
      return 0;
    },

    g () {
      if (this.sentiment && this.sentiment < 0) {
        return Math.ceil(-this.sentiment * 100);
      }
      return 0;
    },

    b () {
      if (this.sentiment && this.sentiment < 0) {
        return Math.ceil(-this.sentiment * 255);
      }
      return 0;
    },

    alpha () {
      if (this.sentiment) {
        if (this.sentiment > 0) return Math.abs(this.sentiment) * 0.3;
        if (this.sentiment < 0) return Math.abs(this.sentiment) * 0.5;
      }
      return 0;
    },

    tweetLines () {
      return this.content.split("\n");
    },


  }
}
</script>


<style>

:root {
  --size: 30px;
}

/* 头像+content整体的样式 */
.tweet {
  position: absolute;
  width: var(--size);
  height: var(--size);
  left: calc(var(--size) / -2);
  top: calc(var(--size) / -2);
  border-radius: 50%;
  overflow: visible;
}

/* 默认头像的样式 */
.avatar {
  position: absolute;
  width: var(--size);
  height: var(--size);
  background-size: var(--size) var(--size);
  border-radius: 50%; 
  overflow: hidden;
  transition: all 0.2s ease-in-out;
  z-index: 0;
}

/* 被选中的头像的样式 */
/* 需考虑加border之后 会不会被overflow切掉 */
.avatar.browsing.selected {
  transform: translate(-1px, -1px) scale(2.0);
  border: 1px solid white;
  opacity: 1.0;
}

.avatar.browsing {
  transform: scale(1.2);
  opacity: 0.8;
}

.avatar.browsing.related {
  transform: scale(1.6);
  border: 1px solid gray;
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
  position: absolute;
  top: 0px;
  padding: 0.5rem;
  width: 350px; 
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 8px; 
  overflow: hidden;
  transition: all 0.1s ease-in-out;
  z-index: 99999;
}

.content.left {
  left: calc(var(--size) * 2);
}

.content.right {
  right: calc(var(--size) * 2);
}

.contentText {
  font-family: "Open Sans";
  color: #14171a;
  font-size: 14px;
  line-height: 20px;
}

.reply-line {
  font-size: 13px;
  padding-bottom: 4px;
  color: #a692ec;
}
</style>
