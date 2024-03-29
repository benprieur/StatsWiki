<template>
  <div class="home-container">
    <div class="day-component-tile" v-for="lang in languages" :key="lang.code">
      <DayComponent :lang="lang.code" :year="yesterday.year" :month="yesterday.month" :day="yesterday.day" />
    </div>
</div>
<FooterComponent/>
</template>

<script>
import DayComponent from './DayComponent.vue';
import FooterComponent from './FooterComponent.vue';

export default {
  name: 'HomeComponent',
  components: {
    DayComponent,
    FooterComponent
  },
  data() {
    return {
      languages: [
      { code: 'fr', name: 'French' },
      { code: 'ja', name: 'Japanese' }
      ],
      yesterday: this.getYesterdayDate(),
    };
  },
  methods: {
    getYesterdayDate() {
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      return {
        year: yesterday.getFullYear(),
        month: String(yesterday.getMonth() + 1).padStart(2, '0'),
        day: String(yesterday.getDate()).padStart(2, '0'),
      };
    },
  },
};
</script>

<style scoped>
.home-container {
  background-color: rgb(230, 230, 230);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.day-component-tile {
  background-color: whitesmoke;
  width: calc(48% - 20px); /* Trois tuiles par ligne moins la marge */
  margin: 5px; /* Marge entre les tuiles */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Ombre optionnelle pour un peu de profondeur */
}

/* Adaptation pour les tablettes */
@media (max-width: 768px) {
  .day-component-tile {
    width: calc(50% - 20px); /* Deux tuiles par ligne */
  }
}

/* Adaptation pour les mobiles */
@media (max-width: 480px) {
  .day-component-tile {
    width: calc(100% - 20px); /* Une tuile par ligne */
  }
}
</style>