<template>
    <div v-if="isLoading" class="loader"></div>
    <div v-if="!isLoading">

    <article class="container">
      <div class="header">
        <span class="bold-and-large">
          {{ day }}&nbsp;<a :href="`/${lang}/${year}/${month}/`">{{ localized_month }}</a>&nbsp;<a :href="`/${lang}/${year}/`">{{ year }}</a>
        </span>
        &nbsp;&nbsp;
        <img :src="$getFlagUrl(lang)" style="width:25px;"/> <a :href="`https://${lang}.wikipedia.org`">{{ title }}</a> 
      </div>
      
      <div class="table-container">
        <ListComponent :columns="columnsData" :rows="rowsData" v-if="lines.length > 0" />
      </div>  
    
    </article>
</div>
</template>
    
    <script>
    import ListComponent from './ListComponent.vue';
    import FooterComponent from './FooterComponent.vue';
    import axios from 'axios';
    
    export default {
      name: 'DayComponent',
      components: {
        ListComponent,
        FooterComponent
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
          isLoading: false,
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

          this.isLoading = true;
          const timeoutPromise = new Promise(resolve => setTimeout(resolve, 8000));
          const fetchPromise = axios.get(url);
          await Promise.race([fetchPromise, timeoutPromise]);
          this.isLoading = false;
      
          try {
            const response = await fetchPromise;

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
  .table-container {
  width: 80%;
  margin: 20px auto; /* Ajoute un espace au-dessus et centre le tableau */
  }

</style>