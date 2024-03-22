<template>
    <div>
      <ListComponent :columns="columnsData" :rows="rowsData" v-if="lines.length > 0" />
    </div>
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
      'months',
      'title',
      'title_views',
      'title_article',
      'bymonthyear'
    ],
    data() {
      return {
        fetchError: false,
        lines: [],
        title_article : '',
        title_views : '0'      };
    },
    computed: {
      columnsData() {
        return [
          { label: this.title_article, field: 'title' },
          { label: 'English translation', field: 'en_translation' },
          { label: 'Wikidata', field: 'qid' },
          { label: this.title_views, field: 'views' },

        ];
      },
      rowsData() {
        return this.lines.map(line => ({
          title: line.title.replace(/_/g, " "),
          en_translation: line.en_translation || '',
          qid: line.qid,
          views: line.views,
        }));
      }
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
        } catch (error) {
          console.error("An error occurred while fetching the year data", error);
          this.fetchError = true;
        }
      },
    }
  }
  </script>
  
  <style scoped>
  </style>
  