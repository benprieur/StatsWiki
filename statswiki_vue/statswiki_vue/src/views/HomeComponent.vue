<template>
  <div class="home-container">
    <div class="day-component-tile">
      <ArticleComponent lang="ja" qid="Q3137013" />
    </div>
    <div class="day-component-tile">
      <ArticleComponent lang="pl" qid="Q989" />
    </div>
    <div class="day-component-tile">
      <ArticleComponent lang="fr" qid="Q81068910" />
    </div>
    <div class="day-component-tile">
      <ArticleComponent lang="en" qid="Q22686" />
    </div>
  </div>
  <FooterComponent/>
</template>

<script>
import ArticleComponent from './ArticleComponent.vue';
import FooterComponent from './FooterComponent.vue';

export default {
  name: 'HomeComponent',
  components: {
    ArticleComponent,
    FooterComponent
  },
  data() {
    return {
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