<template>
  <header class="header-container">
    <div class="logo-container">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg/582px-Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg" alt="StatsWiki Logo" class="logo"/>
      &nbsp;<a :href="`/`" class="title-link">StatsWiki</a>&nbsp;<span class="introduction">Daily viewing statistics of 17+ Wikipedia since July 1, 2015</span>
    </div>
    <table class="navigation-table">
      <tbody>
        <tr v-for="(navigation, index) in navigations" :key="navigation.label">
          <td class="language-item-title">
           {{ navigation.label }}
          </td>
          <td class="language-item-data">
            <span v-for="lang in navigation.languages" :key="lang">
              &nbsp;&nbsp;
              <img :src="$getFlagUrl(lang)" style="max-height: 6px; vertical-align: middle;" />
              <a :href="navigation.getUrl(lang)" class="search-link">{{ navigation.displayPath(lang) }}</a>
              </span>
          </td>
        </tr>
      </tbody>
    </table>
  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  data() {
    const currentDate = new Date();
    const yesterday = new Date(currentDate.getTime() - (24 * 60 * 60 * 1000));
    const thisYear = currentDate.getFullYear();
    const thisMonth = this.pad(currentDate.getMonth() + 1);
    const languages = ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'];
    return {
      navigations: [
        {
          label: 'By lang',
          languages: languages,
          getUrl: (lang) => `/${lang}`,
          displayPath: (lang) => `/${lang}`
        },
        {
          label: 'By lang by day',
          languages: languages.slice(0, 6),
          getUrl: (lang) => `/${lang}/${yesterday.getFullYear()}/${this.pad(yesterday.getMonth() + 1)}/${this.pad(yesterday.getDate())}`,
          displayPath: (lang) => `/${lang}/${yesterday.getFullYear()}/${this.pad(yesterday.getMonth() + 1)}/${this.pad(yesterday.getDate())}`
        },
        {
          label: 'By lang by month',
          languages: languages.slice(6, 11),
          getUrl: (lang) => `/${lang}/${thisYear}/${thisMonth}`,
          displayPath: (lang) => `/${lang}/${thisYear}/${thisMonth}`
        },
        {
          label: 'By lang by year',
          languages: languages.slice(11, 16),
          getUrl: (lang) => `/${lang}/${thisYear}`,
          displayPath: (lang) => `/${lang}/${thisYear}`
        }
      ]
    };
  },
  methods: {
    pad(number) {
      return number.toString().padStart(2, '0');
    }
  }
};
</script>

<style>
.header-container {
  background-color: rgb(54, 54, 54);
  color: white;
  border-radius: 20px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: left;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.title-link {
  font-size: 36px;
  color: white;
  text-decoration: none;
  font-family: 'Arial Narrow', Arial, sans-serif;
}

.title-link:hover {
  text-decoration: underline;
}

.introduction {
  margin-top: 5px;
  text-align: left;
  font-style: italic;
  font-size: 14px;
  color: whitesmoke;
}

.navigation-row {
  display: flex;
  flex-direction: row;
}

.search-languages {
  display: flex;
  flex-wrap: wrap;
}

.language-item-title{
  font-size: 14px;
  color: whitesmoke;
  text-align: left;
  font-weight: bold;
}

.language-item-data a {
  font-size: 14px;
  color: greenyellow;
  text-decoration:none;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.navigation-row span {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
}
</style>