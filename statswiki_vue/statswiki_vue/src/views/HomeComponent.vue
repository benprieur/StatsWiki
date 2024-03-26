<template>
  <div class="homepage-container">
      <DayComponent :lang="randomLang" :year="yesterday.year" :month="yesterday.month" :day="yesterday.day" />
  </div>
</template>

<script>
import YearComponent from './YearComponent.vue';
import MonthComponent from './MonthComponent.vue';
import DayComponent from './DayComponent.vue';

export default {
name: 'HomeComponent',
components: {
  YearComponent,
  MonthComponent,
  DayComponent,
},
data() {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  return {
    currentYear: today.getFullYear(),
    currentMonth: today.getMonth() + 1, // JS months are 0-indexed
    yesterday: {
      year: yesterday.getFullYear(),
      month: yesterday.getMonth() + 1,
      day: yesterday.getDate(),
    },
    // Pas besoin de mettre randomLang ici puisqu'il est défini comme une computed property
  };
},
computed: {
  randomLang() {
    const langs = ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'];
    const randomIndex = Math.floor(Math.random() * langs.length);
    return langs[randomIndex];
  }
}
};
</script>

<style>
.homepage-container {
background-color: #e8e8e8;
}
</style>