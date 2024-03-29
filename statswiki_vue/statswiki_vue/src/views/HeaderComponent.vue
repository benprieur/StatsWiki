<template>
  <header class="header-container">
    <div class="logo-container">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg/582px-Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg" alt="StatsWiki Logo" class="logo"/>
      &nbsp;
      <a :href="`/`" class="title">StatsWiki</a>&nbsp;
      <span class="introduction">Daily viewing statistics of 17+ Wikipedia since July 1, 2015</span>
    </div>
    <br/>
      <span style="text-align: left;" v-for="(navigation, _) in navigations" :key="navigation.label">
        <span style="color:chartreuse; font-size: 20px;">By lang</span>&nbsp;
        <span v-for="lang in navigation.languages" :key="lang">
              <img :src="$getFlagUrl(lang)" style="max-height: 6px; vertical-align: middle;" />
              <a class="languages" :href="navigation.getUrl(lang)">{{ navigation.displayPath(lang) }}</a>
              &nbsp;
        </span>
      </span>
    <br/>
      <span style="color:chartreuse; ; font-size: 20px;">
        
      By lang by year&nbsp;<img src="/assets/ar.svg" style="max-height: 6px; vertical-align: middle;" /><a class="languages" href="/ar/2024">/ar/2024</a>
     
      &nbsp;&nbsp;&nbsp;

      By lang by month&nbsp;<img src="/assets/pl.svg" style="max-height: 6px; vertical-align: middle;" /><a class="languages" href="/pl/2019/12">/pl/2019/12</a>
      
      &nbsp;&nbsp;&nbsp;

      By lang by day&nbsp;<img src="/assets/fr.svg" style="max-height: 6px; vertical-align: middle;" /><a class="languages" href="/fr/2022/07/14">/fr/2022/07/14</a>
      </span>

  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  data() {
    const languages = ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'];
    return {
      navigations: [
        {
          label: 'By lang [since 1st of July 2015]',
          languages: languages,
          getUrl: (lang) => `/${lang}`,
          displayPath: (lang) => `/${lang}`
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
  width: 75px;
  height: 75px;
  border-radius: 50%;
  object-fit: cover;
}

.title {
  font-size: 50px;
  color: white;
  text-decoration: none;
}


.introduction {
  margin-top: 5px;
  text-align: left;
  font-style: italic;
  font-size: 20px;
  color: whitesmoke;
}

.languages {
  text-decoration: none;
  text-align: left;
  font-size: 25px;
  color: whitesmoke;
}

.navigation-table {
  margin: 20px auto 0;
  border: 0px; 
}

.navigation-table td, .navigation-table th {
  border: 0px solid rgb(0, 255, 38); 
  text-align: left;
  padding: 8px; 
}

</style>