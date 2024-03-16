<template>
  <article>
    <p>{{ articleData.lang || lang }}</p>
    <p>{{ articleData.qid || qid }}</p>
    <p>{{ articleData.title || title }}</p>
    <p>{{ articleData.en_translation || en_translation }}</p>
    <p>{{ articleData.sentence || sentence }}</p>
    <a :href="articleData.wikidata_image || wikidata_image" target="_blank">
      Link to Image
    </a>
    <img :src="articleData.wikidata_image_url || wikidata_image_url" alt="Wikidata Image">
  </article>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ArticleComponent',
  props: ["lang", "qid", "title", "en_translation", "sentence", "wikidata_image", "wikidata_image_url"],
  data() {
    return {
      fetchError: false,
      articleData: {}, // Initialisation d'un objet vide pour les données de l'article
    };
  },
  mounted() {
    console.log("mounted ArticleComponent");
    this.fetchArticleData();
  },
  methods: {
    async fetchArticleData() {
      const url = `/api/${this.lang}/${this.qid}/`;
      try {
        const response = await axios.get(url);
        console.log(response.data);
        // Mise à jour de articleData avec les données reçues
        this.articleData = response.data;
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