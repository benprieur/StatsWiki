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
        &nbsp;
        <span v-for="lang in navigation.languages" :key="lang">
              <img :src="$getFlagUrl(lang)" style="max-height: 6px; vertical-align: middle;" />
              <a class="languages" :href="navigation.getUrl(lang)">{{ navigation.displayPath(lang) }}</a>
              &nbsp;
        </span>
      </span>
      <br />
      <table style="text-align: left;">
          <tr>
            <td class="chartreuse">
              By lang and year, month or day
              <DateNavigatorComponent/>
            </td>
            <td class="chartreuse">
              By lang and Wikidata concept
              <SearchLangQidComponent />
            </td>
          </tr>
      </table>
  </header>
</template>

<script>
import DateNavigatorComponent from './DateNavigatorComponent.vue';
import SearchLangQidComponent from './SearchLangQidComponent.vue';

export default {
  name: "HeaderComponent",
  components: {
    DateNavigatorComponent,
    SearchLangQidComponent
  },
  data() {
    const languages = ['ar', 'az', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'];
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
    },
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
  width: 100%; /* Assurez que le conteneur de la table utilise toute la largeur disponible */
  overflow-x: auto; /* Permet le défilement horizontal si la table dépasse la largeur de l'écran */
}

table {
  border-collapse: collapse; /* Supprime les espaces entre les cellules */
  width: auto; /* Permet à la table de s'ajuster à la largeur de son contenu */
  max-width: 80%; /* Empêche la table de dépasser la largeur du conteneur */
  border-collapse: separate;
  border-spacing: 10px 0;
}

td, th {
  border: 1px solid #ddd; /* Style de bordure pour les cellules */
  padding: 8px; /* Padding pour les cellules */
  max-width: 300px; /* Astuce pour forcer les cellules à s'ajuster au contenu */
  color: chartreuse;
  font-size: 20px;
  word-wrap: break-word; /* Permet de casser les mots longs */
  white-space: normal; /* Assure que le contenu peut passer à la ligne */
}

.logo-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap; /* Permet aux éléments de passer à la ligne sur les petits écrans */
}

.logo {
  width: 75px;
  height: 75px;
  border-radius: 50%;
  object-fit: cover;
}

.title {
  font-size: 2em; /* Utilisation de em pour une meilleure flexibilité */
  color: white;
  text-decoration: none;
  margin-right: auto; /* Assure que le titre pousse les éléments vers la gauche */
}

.introduction, .languages {
  font-size: 1em; /* Ajustement de la taille de police pour être plus flexible */
  color: whitesmoke;
}

@media (max-width: 768px) {
  .logo {
    width: 50px; /* Réduction de la taille du logo */
    height: 50px;
  }
  
  .title {
    font-size: 1.5em; /* Police plus petite pour le titre */
  }

  .introduction, .languages {
    font-size: 0.8em; /* Texte plus petit pour l'introduction et les langues */
  }

  .header-container {
    padding: 5px; /* Moins de padding */
  }
  
  .logo-container {
    justify-content: center; /* Centrer le contenu sur petits écrans */
  }
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
  font-size: 20px;
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