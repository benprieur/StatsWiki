<template>
  <article class="article-container">
    <div class="content">
      <div class="text-side">
        <p>{{ articleData.lang }} {{ replaceUnderscoreWithSpace(articleData.title) }}
          <span v-if="articleData.en_translation" style="font-style: italic;"> ({{ articleData.en_translation }})</span>
        </p>
        <p>
          <a :href="`https://www.wikidata.org/wiki/${articleData.qid}`">{{ articleData.qid }}</a>
        </p>
        <p style="font-style: italic;">{{ articleData.sentence }}
          <a :href="`https://${articleData.lang}.wikipedia.org/wiki/${replaceUnderscoreWithSpace(articleData.title)}`">...</a>
        </p>
      </div>
      <div class="image-side">
        <a :href="articleData.wikidata_image_url">
          <img :src="articleData.wikidata_image" />
        </a>
      </div>
    </div>
    <div v-if="articleData && articleData.statistics_global">
    <ChartComponent :data="articleData.statistics_global"></ChartComponent>
  </div>
  </article>
</template>

<script>
import ChartComponent from './ChartComponent.vue';
import axios from 'axios';

export default {
  name: 'ArticleComponent',
  components: {
    ChartComponent
  },
  props: {
    lang: String,
    qid: String,
    title: String,
    en_translation: String,
    sentence: String,
    wikidata_image: String,
    wikidata_image_url: String,
    statistics_global: Object
  },
  data() {
    return {
      fetchError: false,
      articleData: {
        // Initialisez les données de l'article ici, si nécessaire
        lang: this.lang,
        qid: this.qid,
        title: this.title,
        en_translation: this.en_translation,
        sentence: this.sentence,
        wikidata_image: this.wikidata_image,
        wikidata_image_url: this.wikidata_image_url,
        statistics_global: this.statistics_global
      }
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
        this.articleData = { ...this.articleData, ...response.data };
      } catch (error) {
        console.error("An error occurred while fetching the article data", error);
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
.article-container {
  display: flex;
  flex-direction: column;
}
.content {
  display: flex;
  justify-content: space-between;
}
.text-side, .image-side {
  flex: 1;
}
.text-side {
  padding-right: 20px; 
}
.image-side img {
  width: 100%; 
  height: auto; 
}
canvas {
  max-width: 100%;
}
</style>