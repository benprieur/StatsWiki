<template>
    <div class="language-selector">
      <select v-model="selectedLanguage" @change="onLanguageChange">
        <option disabled value="">Lang</option>
        <option v-for="code in SUPPORTED_LANGUAGES" :key="code" :value="code">
          {{ code }}
        </option>
      </select>
      <img v-if="selectedLanguage" :src="`./assets/${selectedLanguage}.svg`" :alt="selectedLanguage" class="flag-img">


      <input type="text" v-model="searchQuery" @input="fetchResults" placeholder="Search...">
        <ul v-if="results.length > 0">
          <li v-for="(result, index) in results" :key="index">
            {{ result }}
          </li>
        </ul>
      </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SearchLangQidComponent',
    data() {
      return {
        searchQuery: '',
        results: [],
        isLoading: false
      }
    },
    methods: {
      async fetchResults() {
        if (this.searchQuery.length < 3) { // Optionnel: Seulement rechercher si la query a 3 caractères ou plus
          this.results = [];
          return;
        }
  
        this.isLoading = true;
        try {
          // Remplacez `YOUR_API_ENDPOINT` par l'URL de votre API et configurez les paramètres selon votre API
          const response = await axios.get(`YOUR_API_ENDPOINT`, { params: { query: this.searchQuery } });
          // Assurez-vous de transformer la réponse de l'API en fonction du format attendu pour `results`
          this.results = response.data; // Supposons que l'API renvoie directement un tableau de suggestions
        } catch (error) {
          console.error("Erreur lors de la récupération des résultats:", error);
          this.results = [];
        } finally {
          this.isLoading = false;
        }
      }
    }
  }
  </script>
  
  <style>
  /* Styles de base pour la liste de suggestions */
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin: 5px 0;
    cursor: pointer;
  }
  </style>