<template>
<article class="container">
  <div class="header">
    <span class="bold-and-large">{{ year }}</span>&nbsp;&nbsp;
    <img :src="$getFlagUrl(lang)" style="width:25px;"/> <a :href="`https://${lang}.wikipedia.org`">{{ title }}</a> 
  </div>
  
  <div class="month-navigation">
    <ul>
      <li>{{ bymonthyear }}</li>&nbsp;&nbsp;
      <li v-for="(month, index) in monthsToShow" :key="index">
        <a :href="`/${lang}/${year}/${padMonth(index + 1)}`">{{ month }}</a>
      </li>
    </ul>
  </div>
  
  <div>
    <ListComponent :columns="columnsData" :rows="rowsData" v-if="lines.length > 0" />
  </div>

</article>
</template>

<script>
import ListComponent from './ListComponent.vue';
import axios from 'axios';

export default {
  name: 'YearComponent',
  components: {
    ListComponent
  },
  props: [
    'lang',
    'year',
  ],
  data() {
    return {
      fetchError: false,
      lines: [],
      title: '',
      title_article : '',
      title_views : '0',
      bymonthyear : '',
      months: [],
      currentMonth: new Date().getMonth() +1,
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
      return this.lines.map(line => ({
        title: `<a style="text-decoration:none; color: black;" href="/${this.lang}/${line.qid}">${line.title.replace(/_/g, " ")}</a>`,
        en_translation: line.en_translation || '',
        views: line.views,
        qid_link: `<a style="color: lightgray; text-decoration : none;" href="https://www.wikidata.org/wiki/${line.qid}">${line.qid}</a>`,
        image: `<a style="align: center; color: lightgray; text-decoration : none;" href="${line.wikidata_image_url}"><img style="max-width: 25px;" src="${line.wikidata_image}" />`,
      }));
    },
    monthsToShow() {
      if (parseInt(this.year) < this.currentYear) {
        return this.months;
      } else {
        return this.months.filter((_, index) => index + 1 <= this.currentMonth);
      }
    },
  },
  mounted() {
    this.fetchYearData();
  },
  methods: {
    async fetchYearData() {
      const url = `/api/${this.lang}/${this.year}/`;
      try {
        const response = await axios.get(url);
        this.lines = response.data.lines;
        this.title_article = response.data.title_article;
        this.title_views = response.data.title_views;
        this.title = response.data.title;
        this.bymonthyear = response.data.bymonthyear;
        this.months = response.data.months;
      } catch (error) {
        console.error("An error occurred while fetching the year data", error);
        this.fetchError = true;
      }
    },
    padMonth(month) {
      return month.toString().padStart(2, '0');
    },
  }
}
</script>

<style scoped>

.container {
  background-color: #e8e8e8;
}
.header {
  background-color: #c1c1c1;
  border: 1px solid black; 
  border-radius: 20px; 
  padding: 20px; 
  margin: 20px 0; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
}

.bold-and-large {
  font-size: 50px; 
  color: black;
  font-weight: bold;
}

.month-navigation {
  background-color: #48466e; /* Fond noir clair */
  color: white;
  text-align: center;
  padding: 10px 0;
}

.month-navigation ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.month-navigation li {
  display: inline;
  margin-right: 20px;
}

.month-navigation a {
  color: white;
  text-decoration: none;
}

.month-navigation a:hover {
  text-decoration: underline;
}

a {
  color: black;
  text-decoration: underline; 
}

a:hover {
  color: darkgray; 
}
</style>