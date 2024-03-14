<template>
    <div class="article">
      <h2>{{ title }} ({{ qid }})</h2>
    </div>
</template>
  
  <script>
  export default {
    name: 'ArticleComponent',
    props: {
      lang: String,
      qid: String,
      title: String,
      wikidata_image: String,
      wikidata_image_url: String,
      flag: String,
      sentence: String,
      translation: String,
      statistics: Array,
      redirect: Array,
    },
  };
  </script>
  
  <style scoped>
  .article img {
    width: 100%;
    max-width: 400px;
    height: auto;
  }
  </style>
  