<template>
  <article class="article-container">
    <div class="content">
      
      <div class="image-side">
        <a :href="articleData.wikidata_image_url">
          <img :src="articleData.wikidata_image" />
        </a>
      </div>

      <div class="text-side">
        <p><img :src="$getFlagUrl(lang)" style="width:25px;" /> <a :href="`https://${articleData.lang}.wikipedia.org`">{{ articleData.lang }}.wikipedia</a></p>
        
        <p>
          <span class="bold-and-large"><a :href="`https://${articleData.lang}.wikipedia.org/wiki/${articleData.title}`">{{ replaceUnderscoreWithSpace(articleData.title) }}</a></span>
          <span v-if="articleData.en_translation" style="font-style: italic;">&nbsp;&nbsp;({{ articleData.en_translation }})</span>
          <span class="small-wikidata">&nbsp;&nbsp;&nbsp;&nbsp;
            <a :href="`https://www.wikidata.org/wiki/${articleData.qid}`">{{ articleData.qid }}</a>
            &nbsp;<img :src="$getFlagUrl('wd')" style="width:13px;" />
          </span>
        </p>
        
        <p class="article-excerpt">{{ articleData.sentence }}...</p>
      
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
  background-color: #e8e8e8;
  border: 3px solid black; /* Liseret noir */
  border-radius: 20px; /* Bords arrondis */
  padding: 20px; /* Espacement intérieur pour ne pas coller au bord */
  margin: 20px 0; /* Ajout d'une marge extérieure pour l'espacement avec d'autres éléments */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optionnel: ajoute une ombre pour un effet de profondeur */
}

.content {
  display: flex;
  align-items: flex-start;
  background-color: #c1c1c1;
  border: 1px solid black;
  border-radius: 20px; 
}

.text-side, .image-side {
  flex: 1;
}

.text-side {
  padding-left: 20px; 
  flex: 3;
}

.image-side img {
  flex: 1;
  padding: 20px;
  width: auto; 
  max-width: 100px;
}

canvas {
  align-self: center;
  max-width: 90%;
}

.bold-and-large {
  font-size: 30px; 
  color: black;
  font-weight: bold;
}

.small-wikidata {
  font-size: 13px; 
}

.article-excerpt {
  font-family: 'Georgia', serif; 
  font-size: 20px; 
  line-height: 1.6; 
  color: #4c4c4c;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

a {
  color: black;
  text-decoration: underline; 
}

a:hover {
  color: darkgray; 
}

</style>