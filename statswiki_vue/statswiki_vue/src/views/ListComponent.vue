<template>
    <div class="liste-container">
      <!-- En-têtes de la table pour le tri -->
      <div class="liste-header">
        <div v-for="header in headers" :key="header.key" @click="sortData(header.key)">
          {{ header.name }}
          <span v-if="sortKey === header.key">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
        </div>
      </div>
      <!-- Affichage des données -->
      <div class="liste-items">
        <div v-for="(item, index) in paginatedData" :key="index">
          <!-- Générer dynamiquement les données de l'item ici -->
          <div v-for="(header, index) in headers" :key="index">{{ item[header.key] }}</div>
        </div>
      </div>
      <!-- Pagination -->
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage <= 1">Précédent</button>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">Suivant</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "List",
    props: {
      data: Array,
      headers: Array, // { name: String, key: String }
      itemsPerPage: {
        type: Number,
        default: 10,
      },
    },
    data() {
      return {
        currentPage: 1,
        sortKey: '',
        sortDirection: 'asc',
      };
    },
    computed: {
      sortedData() {
        return [...this.data].sort((a, b) => {
          if (a[this.sortKey] < b[this.sortKey]) return this.sortDirection === 'asc' ? -1 : 1;
          if (a[this.sortKey] > b[this.sortKey]) return this.sortDirection === 'asc' ? 1 : -1;
          return 0;
        });
      },
      paginatedData() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.sortedData.slice(start, start + this.itemsPerPage);
      },
      totalPages() {
        return Math.ceil(this.data.length / this.itemsPerPage);
      },
    },
    methods: {
      sortData(key) {
        if (this.sortKey === key) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortDirection = 'asc';
        }
        this.sortKey = key;
      },
      changePage(page) {
        this.currentPage = page;
      },
    },
  };
  </script>
  
  <style scoped>
  .liste-container {
    /* Styles du conteneur */
  }
  .liste-header div {
    /* Styles des en-têtes, avec un curseur pointeur */
    cursor: pointer;
  }
  .liste-items div {
    /* Styles des éléments de liste */
  }
  .pagination button {
    /* Styles des boutons de pagination */
  }
  </style>
  