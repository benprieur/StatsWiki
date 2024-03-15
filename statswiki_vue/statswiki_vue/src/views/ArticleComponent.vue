<template>
    <article>
      <p>{{ lang }}</p>
      <p>{{ qid }}</p>
  </article>
  </template>
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ArticleComponent',
    props: ['lang', 'qid'],
    mounted() {
      console.log("Lang:", this.lang, "QID:", this.qid);  // Ceci devrait afficher les valeurs passées à travers l'URL
    },
    data() {
      return {
        fetchError: false,
      };
    },
    mounted() {
      console.log("bite")
      this.fetchArticleData();
    },
    methods: {
      async fetchArticleData() {
        const url = `/api/${this.lang}/${this.qid}/`;
        try {
          const response = await axios.get(url);
          // Supposons que vous souhaitiez stocker des données spécifiques de réponse
          // Mettez à jour votre objet data ici, par exemple:
          // this.articleSpecificData = response.data.someSpecificField;
          console.log(response.data); // Affichez les données pour vérification
        } catch (error) {
          console.error("An error occurred while fetching the article data", error);
          this.fetchError = true;
        }
      }
    },
  };
  </script>
  
  <style scoped>
  </style>
  