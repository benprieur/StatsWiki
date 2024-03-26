<template>
    <header class="header-container">
      <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg/582px-Rosace_trac%C3%A9e_sur_la_pierre_sous_le_porche_de_l%27%C3%A9cole_de_Soug%C3%A8res-en-Puisaye.jpg" alt="StatsWiki Logo" class="logo"/>
        &nbsp;<a :href="`/`" class="search-link">StatsWiki</a>
      </div>
      <p class="introduction">Daily viewing statistics of 17+ Wikipedia since July 1, 2015</p>

      <hr class="custom-hr" />

      <div class="search-modes">
        <span style="color:greenyellow; font-size:24px;">By language [/lang]:&nbsp;&nbsp;</span>
        <div class="search-languages">
            <span v-for="lang in languages" :key="lang" class="language-item">
                <img :src="$getFlagUrl(lang)" style="width:20px; vertical-align:middle;" />
                <a :href="`/${lang}`" class="search-link">/{{ lang }}</a>
                &nbsp;&nbsp;&nbsp;&nbsp;
            </span>
        </div>
    </div>
    <br/>
    <div class="search-modes">
        <span style="color:greenyellow; font-size:24px;">By language & year, month or day [/lang/year/month/day]:&nbsp;&nbsp;</span>
        <div class="search-languages">
          <span v-for="lang in languages" :key="lang" class="language-item">
                <img :src="$getFlagUrl(lang)" style="width:20px; vertical-align:middle;" />
                <a :href="`/${lang}/${yesterday_year}/${yesterday_month}/${yesterday_day}`" class="search-link">/{{ lang }}/{{ yesterday_year }}/{{ yesterday_month }}/{{ yesterday_day }}</a>
                &nbsp;&nbsp;&nbsp;&nbsp;
            </span>
        </div>
    </div>
    <br/>
    <div class="search-modes">
        <span style="color:greenyellow; font-size:24px;">By language & Wikidata concept [/lang/qid]:&nbsp;&nbsp;</span>
        <div class="search-languages">
            <span class="language-item">
                <img :src="$getFlagUrl('pt')" style="width:20px; vertical-align:middle;" />&nbsp;
                <a class="search-link" :href="`/pt/Q12897/`">/pt/Q12897</a>&nbsp;<span style="font-size:15px;">(Pelé)</span>&nbsp;&nbsp;&nbsp;&nbsp;
            </span>
            
            <span class="language-item">
                <img :src="$getFlagUrl('fr')" style="width:20px; vertical-align:middle;" />&nbsp;
                <a class="search-link" :href="`/fr/Q708078/`">/fr/Q708078</a>&nbsp;<span style="font-size:15px;">(Missak Manouchian)</span> &nbsp;&nbsp;&nbsp;&nbsp;
            </span>

        </div>
    </div>
</header>
</template>

  
<script>
export default {
  name: "HeaderComponent",
  data() {
    const currentDate = new Date();
    const yesterday = new Date(currentDate.getTime() - (24 * 60 * 60 * 1000));
    return {
      languages: ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'],
      yesterday_year: yesterday.getFullYear(), 
      yesterday_month: this.pad(yesterday.getMonth() + 1), 
      yesterday_day: this.pad(yesterday.getDate()),
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
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: left;
}

.logo-container {
  display: flex;
  align-items: center;
  font-size: 60px;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.introduction {
  text-align: left;
  font-style: italic;
  font-size: 19px;
  color: whitesmoke;
}

.search-modes {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px; /* Ajustez l'espace entre les éléments */
  margin-bottom: 10px; /* Espace en dessous du bloc des modes de recherche */
}

.search-languages {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px; /* Ajustez l'espace entre les drapeaux et les liens */
}

.language-item {
  display: flex;
  align-items: center;
}

.search-link {
  color: white;
  text-decoration: none;
  margin-left: 5px; /* Espace entre l'image du drapeau et le lien */
}

.search-link:hover {
  text-decoration: underline;
}

.search {
  display: flex;
  padding: 0;
  list-style-type: none;
  gap: 25px; 
  color: white;
}

.search a {
  color: white;
  font-size: 22px;
  text-decoration: none;
}

.search a:hover {
  font-size: 22px;
  color: white;
  text-decoration: underline;
}

.custom-hr {
  background-color: greenyellow;
  height: 1px;
  border: none;
  width: 100%; 
}

</style>