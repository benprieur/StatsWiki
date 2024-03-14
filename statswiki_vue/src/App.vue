<template>
  <div id="app">
    <!-- Check if articleData is available and no error occurred -->
    <ArticleComponent v-if="articleData && !fetchError" v-bind="articleData" />
    
    <!-- Display an error message if the fetch operation fails -->
    <div v-if="fetchError" class="error-message">
      Unable to load the article data. Please try again later.
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ArticleComponent from './views/ArticleComponent.vue';

export default {
  name: 'App',
  components: {
    ArticleComponent
  },
  data() {
    return {
      articleData: null,
      fetchError: false, // New state to track if an error occurred during fetch
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/fr/Q708078/'); 
        this.articleData = response.data; // Make sure to correct this to match your data property
        this.fetchError = false; // Reset or ensure the error state is false on a successful fetch
      } catch (error) {
        console.error("An error occurred while fetching the data", error);
        this.fetchError = true; // Set the error state to true when fetch fails
      }
    }
  },
};
</script>

<style>
/* Style for the error message */
.error-message {
  color: red;
  font-weight: bold;
}
</style>