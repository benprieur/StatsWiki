<template>
  <div v-if="isLoading" class="loader">Loading...</div>
  <div v-else>
    <article class="article-container">
      <div class="header-content">
        <div class="image-side">
          <a :href="articleData.wikidata_image_url">
            <img :src="articleData.wikidata_image" alt="Article Image" />
          </a>
        </div>

        <div class="text-side">
          <p>
            <img :src="$getFlagUrl(lang)" alt="Lang Flag" style="width:25px;" />
            <a :href="`https://${articleData.lang}.wikipedia.org`">{{ articleData.lang }}.wikipedia</a>
          </p>
          <p>
            <span class="bold-and-large">
              <a :href="`https://${articleData.lang}.wikipedia.org/wiki/${articleData.title}`">
                {{ replaceUnderscoreWithSpace(articleData.title) }}
              </a>
            </span>
            <span v-if="articleData.en_translation" style="font-style: italic;">
              ({{ articleData.en_translation }})
            </span>
            <span class="small-wikidata">
              <a :href="`https://www.wikidata.org/wiki/${articleData.qid}`">{{ articleData.qid }}</a>
              <img :src="$getFlagUrl('wd')" alt="WD" style="width:13px;" />
            </span>
          </p>
        </div>
      </div>
      
      <div class="article-excerpt">
          {{ articleData.sentence }}...
      </div>

      <div v-if="articleData && articleData.statistics_global" class="chart-container">
        <ChartComponent :data="articleData.statistics_global" />
      </div>
    </article>
  </div>
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
      isLoading: false,
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

      this.isLoading = true;
      const timeoutPromise = new Promise(resolve => setTimeout(resolve, 8000));
      const fetchPromise = axios.get(url);
      await Promise.race([fetchPromise, timeoutPromise]);
      this.isLoading = false;

      try {
        const response = await fetchPromise;
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
  border: 3px solid black;
  border-radius: 20px;
  padding: 20px;
  margin: 20px auto;
  width: 80%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-side, .text-side {
  text-align: center;
}

.image-side img {
  max-width: 100px;
  height: auto;
  border-radius: 50%;
}

.bold-and-large, .small-wikidata, .article-excerpt, .introduction {
  font-size: 16px;
}

.article-excerpt {
  font-family: 'Georgia', serif;
  line-height: 1.6;
  color: #4c4c4c;
  margin-top: 20px; /* Ajoute plus d'espace avant l'extrait */
  word-break: break-word;
}

@media (max-width: 768px) {
  .article-container {
    width: 95%;
    padding: 10px;
  }

  .header-content {
    align-items: center;
  }

  .bold-and-large, .small-wikidata, .article-excerpt, .introduction {
    font-size: 14px;
  }

  .image-side img {
    max-width: 80px;
  }
}
</style>