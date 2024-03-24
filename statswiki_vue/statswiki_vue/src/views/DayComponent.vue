<template>
    <article class="container">
      <div class="header">

        <span class="bold-and-large"> {{current_date}}>&nbsp;&nbsp;<a :href="`/${lang}/${year}/${month}`">{{ localized_month }}</a>&nbsp;<a :href="`/${lang}/${year}`">{{ year }}</a></span
        <img :src="$getFlagUrl(lang)" style="width:25px;"/> <a :href="`https://${lang}.wikipedia.org`">{{ title }}</a> 
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
      name: 'DayComponent',
      components: {
        ListComponent
      },
      props: [
        'lang',
        'year',
        'month',
        'day'
      ],
      data() {
        return {
          fetchError: false,
          lines: [],
          title: '',
          title_article : '',
          title_views : '0',
          localized_month: '',
          current_date: ''
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
      },
      mounted() {
        this.fetchDayData();
      },
      methods: {
        async fetchDayData() {
          const url = `/api/${this.lang}/${this.year}/${this.month}/${this.day}/`;
          try {
            const response = await axios.get(url);
            this.lines = response.data.lines;
            this.title_article = response.data.title_article;
            this.title_views = response.data.title_views;
            this.title = response.data.title;
            this.localized_month = response.data.localized_month;
            this.current_date = response.data.current_date;
          } catch (error) {
            console.error("An error occurred while fetching the day data", error);
            this.fetchError = true;
          }
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

    a {
        color: black;
        text-decoration: underline; 
    }

    a:hover {
        color: darkgray; 
    }

</style>