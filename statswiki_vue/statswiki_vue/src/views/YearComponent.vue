<template>
    Tutu
    {{ articles }}
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'YearComponent',
  components: {

  },
  props: [
    'lang',            
    'articles', 
    'flag',
    'year',
    'year_before_link',
    'year_after_link',
    'year_before',
    'year_after',
    'months',
    'title',
    'title_views',
    'title_article',
    'bymonthyear'
  ],
  data() {
    return {
      fetchError: false,
      yearData: {
          lang : this.lang,            
          articles : this.articles,    
          flag : this.flag,    
          year : this.year,    
          year_before_link : this.year_before_link,    
          year_after_link : this.year_after_link,    
          year_before : this.year_before,    
          year_after : this.year_after,    
          months : this.months,    
          title : this.title,    
          title_views : this.title_views,    
          title_article : this.title_article,    
          bymonthyear : this.bymonthyear
      }
    };
  },
  mounted() {
    console.log("mounted YearComponent");
    this.fetchYearData();
  },
  methods: {
    async fetchYearData() {
      const url = `/api/${this.lang}/${this.year}/`;
      try {
        const response = await axios.get(url);
        console.log(response.data);
        this.yearData = { ...this.yearData, ...response.data };
      } catch (error) {
        console.error("An error occurred while fetching the year data", error);
        this.fetchError = true;
      }
    },
    replaceUnderscoreWithSpace(value) {
      return value ? value.replace(/_/g, " ") : "";
    }
  }
};
</script>

<style scoped>

</style>
