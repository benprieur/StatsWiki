<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import ArticleComponent from './views/ArticleComponent.vue';

export default {
  name: 'App',
  components: {
    ArticleComponent
  },
};
</script>
