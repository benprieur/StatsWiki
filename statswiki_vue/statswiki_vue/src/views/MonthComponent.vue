<template>
  <div v-if="isLoading" class="loader"></div>

  <div v-if="!isLoading">

    <article class="container">
      <div class="header">
        <span class="bold-and-large">{{ localized_month }} <a :href="`/${lang}/${year}`">{{ year }}</a></span>&nbsp;&nbsp;
        <img :src="$getFlagUrl(lang)" style="width:25px;" /> <a :href="`https://${lang}.wikipedia.org`">{{ title }}</a>
      </div>

      <div class="day-navigation">
        <ul>
          <li>{{ bymonthday }}</li>&nbsp;&nbsp;
          <li v-for="(day, index) in days" :key="index">
            <a :href="`${day}`">{{ padDay(index + 1) }}</a>
          </li>
        </ul>
      </div>

      <div class="table-container">
        <ListComponent :columns="columnsData" :rows="rowsData" v-if="lines.length > 0" />
      </div> 
    </article>
    <FooterComponent />
    </div>
</template>

<script>
import ListComponent from './ListComponent.vue';
import FooterComponent from './FooterComponent.vue';
import axios from 'axios';

export default {
  name: 'YearComponent',
  components: {
    ListComponent,
    FooterComponent
  },
  props: ['lang', 'year', 'month'],
  data() {
    return {
      fetchError: false,
      isLoading: false,
      lines: [],
      title: '',
      title_article: '',
      title_views: '0',
      bymonthday: '',
      days: [],
      localized_month: '',
      currentDay: new Date().getDay() + 1,
      currentMonth: new Date().getMonth() + 1,
      currentYear: new Date().getFullYear(),
    };
  },
  computed: {
    columnsData() {
      return [
        { label: this.title_article, field: 'title', tdClass: 'article', html: true },
        { label: 'English translation', field: 'en_translation', tdClass: 'normal-behavior' },
        { label: '', field: 'image', sortable: false, html: true, tdClass: 'align-center' },
        { label: this.title_views, field: 'views', tdClass: 'align-right' },
      ];
    },
    rowsData() {
      return this.lines.map((line) => ({
        title: `<a style="text-decoration:none; color: black;" href="/${this.lang}/${line.qid}">${line.title.replace(/_/g, ' ')}</a>`,
        en_translation: line.en_translation || '',
        views: line.views,
        qid_link: `<a style="color: lightgray; text-decoration : none;" href="https://www.wikidata.org/wiki/${line.qid}">${line.qid}</a>`,
        image: `<a style="align: center; color: lightgray; text-decoration : none;" href="${line.wikidata_image_url}"><img style="max-width: 25px;" src="${line.wikidata_image}" />`,
      }));
    },
  },
  mounted() {
    this.fetchMonthData();
  },
  methods: {
    async fetchMonthData() {
      const isCurrentMonthYear = this.currentMonth == this.month  && this.currentYear == this.year;
      const url = isCurrentMonthYear ? `/api/specific/${this.lang}/${this.year}/${this.month}/` : `/api/${this.lang}/${this.year}/${this.month}/`;

      this.isLoading = true;
      const timeoutPromise = new Promise((resolve) => setTimeout(resolve, 8000));
      const fetchPromise = axios.get(url, {
        headers: isCurrentMonthYear  ? { 'CurrentMonth': 'true' } : {}
      });
      await Promise.race([fetchPromise, timeoutPromise]);
      this.isLoading = false;

      try {
        const response = await fetchPromise;

        this.lines = response.data.lines;
        this.title_article = response.data.title_article;
        this.title_views = response.data.title_views;
        this.title = response.data.title;
        this.bymonthday = response.data.bymonthday;
        this.days = response.data.days;
        this.localized_month = response.data.localized_month;
      } catch (error) {
        console.error("An error occurred while fetching the month data", error);
        this.fetchError = true;
      }
    },

    padDay(day) {
      return day.toString().padStart(2, '0');
    },
  },
}
</script>

<style scoped>
  .header {
    display: flex;
    justify-content: center; 
    border-radius: 20px; 
    padding: 10px; 
    margin: 5px 0; 
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  }
  .bold-and-large {
  font-size: 35px; 
  color: black;
  font-weight: bold;
  }
  a {
  font-size: 35px; 
  color: black;
  font-weight: bold;
  }
  a:hover {
  font-size: 35px; 
  color: black;
  font-weight: bold;
  }
    
  .day-navigation {
      background-color: #48466e; /* Fond noir clair */
      color: white;
      text-align: center;
      padding: 10px;
      font-size: 25px;
  }

  .day-navigation ul {
      display: flex; /* Utilise Flexbox pour la disposition */
      flex-wrap: wrap; /* Permet aux éléments de passer à la ligne si nécessaire */
      padding: 0;
      margin: 0;
      list-style-type: none; /* Enlève les puces de la liste */
  }

  .day-navigation li {
      margin-right: 25px; /* Ajoute un peu d'espace entre les éléments */
  }

  .day-navigation a {
      text-decoration: none;
      color: white; /* Définit la couleur du texte des liens */
      font-size: 25px;
  }

  @media (max-width: 600px) { /* Pour les écrans de moins de 600px de large */
      .day-navigation ul {
      justify-content: center; /* Centre les éléments dans le conteneur */
  }}

  .day-navigation li {
      margin-bottom: 5px; /* Ajoute un peu d'espace entre les éléments lorsqu'ils passent à la ligne */
  }

  .table-container {
      width: 80%;
      margin: 20px auto; /* Ajoute un espace au-dessus et centre le tableau */
  }

</style>