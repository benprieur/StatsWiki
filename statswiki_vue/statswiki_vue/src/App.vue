<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import ArticleComponent from './views/ArticleComponent.vue';
import YearComponent from './views/YearComponent.vue';

export default {
  name: 'App',
  components: {
    ArticleComponent,
    YearComponent
  }
};
</script>
