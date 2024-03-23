<template>
  <div>
    <img :src="$getFlagUrl(lang)" style="width:25px;"/> {{ title }} {{ year }}
  </div>
  <div>
    {{ bymonthyear }} {{ months }}
  </div>

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
    ],
    data() {
      return {
        fetchError: false,
        lines: [],
        title: '',
        title_article : '',
        title_views : '0',
        bymonthyear : '',
        months: []    
      };
    },
    computed: {

      
      columnsData() {
        return [
          { label: this.title_article, field: 'title', tdClass: 'normal-behavior', html: true },
          
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
          this.title = response.data.title;
          this.bymonthyear = response.data.bymonthyear;
          this.months = response.data.months;
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
  