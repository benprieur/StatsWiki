<template>
      <div class="homepage-container">
        <div class="row">
          <DayComponent lang="en" :year="yesterday.year" :month="yesterday.month" :day="yesterday.day" class="component" />
          <DayComponent lang="ja" :year="yesterday.year" :month="yesterday.month" :day="yesterday.day" class="component" />
        </div>
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
      };
    },
  };
  </script>
  
  <style>
  .homepage-container {
    background-color: #e8e8e8;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .row {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  
  .component {
    width: calc(50% - 10px); /* Adjust based on your gap */
    margin-bottom: 20px; /* Space between rows */
  }
  </style>