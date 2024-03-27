<template>
  <div id="app" style="background-color: #e8e8e8;">
    <HeaderComponent />
    <router-view></router-view>
  </div>
</template>

<script>
import YearComponent from './views/YearComponent.vue';
import MonthComponent from './views/MonthComponent.vue';
import DayComponent from './views/DayComponent.vue';
import HeaderComponent from './views/HeaderComponent.vue';

export default {
  name: 'StatsWiki',
  components: {
    YearComponent,
    MonthComponent,
    DayComponent,
    HeaderComponent
  },
};

</script>

<style>
.router-view {
  display: flex;
  flex-direction: column;
}

.loader,
.loader:before,
.loader:after {
  border-radius: 50%;
  color: #717270;
}
.loader {
  font-size: 11px;
  text-indent: -99999em;
  margin: 55px auto;
  position: relative;
  width: 10em;
  height: 10em;
  box-shadow: inset 0 0 0 1em;
  transform: translateZ(0);
}
.loader:before,
.loader:after {
  position: absolute;
  content: '';
}
.loader:before {
  width: 5.2em;
  height: 10.2em;
  background: #abaeab;
  border-radius: 10.2em 0 0 10.2em;
  top: -0.1em;
  left: -0.1em;
  transform-origin: 5.1em 5.1em;
  animation: load2 2s infinite ease 1.5s;
}
.loader:after {
  width: 5.2em;
  height: 10.2em;
  background: #b4b9b4;
  border-radius: 0 10.2em 10.2em 0;
  top: -0.1em;
  left: 4.9em;
  transform-origin: 0.1em 5.1em;
  animation: load2 2s infinite ease;
}

@keyframes load2 {
  0%,
  100% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>