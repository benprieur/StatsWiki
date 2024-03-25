<template>
  <div id="app">
    <HeaderComponent />
    <router-view></router-view>
    <FooterComponent />
  </div>
</template>

<script>
import YearComponent from './views/YearComponent.vue';
import MonthComponent from './views/MonthComponent.vue';
import DayComponent from './views/DayComponent.vue';
import HeaderComponent from './views/HeaderComponent.vue';
import FooterComponent from './views/FooterComponent.vue';

export default {
  name: 'StatsWiki',
  components: {
    YearComponent,
    MonthComponent,
    DayComponent,
    HeaderComponent,
    FooterComponent
  },
};
</script>

<style>
</style>