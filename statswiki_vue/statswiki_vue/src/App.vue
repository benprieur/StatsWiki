<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import ArticleComponent from './views/ArticleComponent.vue';
import YearComponent from './views/YearComponent.vue';
import MonthComponent from './views/MonthComponent.vue';
import DayComponent from './views/DayComponent.vue';
import LangComponent from './views/LangComponent.vue';

export default {
  name: 'App',
  components: {
    ArticleComponent,
    YearComponent,
    MonthComponent,
    DayComponent,
    LangComponent,
  }
};
</script>

<style>
</style>