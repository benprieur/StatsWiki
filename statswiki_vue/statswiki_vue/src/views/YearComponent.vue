<template>
  <article class="container">
    <div v-if="isLoading" class="loader">Loading...</div>

    <div v-if="!isLoading">
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
      
      <div class="table-container">
        <ListComponent :columns="columnsData" :rows="rowsData" v-if="lines.length > 0" />
      </div> 
      <FooterComponent />
    </div>
  </article>
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
    props: [
      'lang',
      'year',
    ],
    data() {
      return {
        fetchError: false,
        isLoading: false,
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

        const isCurrentYear = this.currentYear == this.year;
        const url = isCurrentYear ? `/api/specific/${this.lang}/${this.year}/` : `/api/${this.lang}/${this.year}/`;

        this.isLoading = true;
        const timeoutPromise = new Promise(resolve => setTimeout(resolve, 8000));
        const fetchPromise = axios.get(url, {
          headers: isCurrentYear ? { 'CurrentYear': 'true' } : {}
        });
        await Promise.race([fetchPromise, timeoutPromise]);
        this.isLoading = false;
  
        try {
  
          const response = await fetchPromise;
  
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

.month-navigation {
  background-color: #48466e; /* Fond noir clair */
  color: white;
  text-align: center;
  font-size: 25px;
  padding: 5px 0;
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
  font-size: 25px;
}

.month-navigation a:hover {
  text-decoration: underline;
}

.table-container {
  width: 80%;
  margin: 20px auto; /* Ajoute un espace au-dessus et centre le tableau */
  }
</style>