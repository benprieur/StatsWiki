<template>
    <vue-good-table
      :columns="columns"
      :rows="rows"
      :pagination-options="{enabled: true}"
      :search-options="{enabled: true}"
      style-class="vgt-table striped"
    />
  </template>
  
  <script>
  import { VueGoodTable } from 'vue-good-table-next';
  
  export default {
    name: 'ListComponent',
    components: {
      VueGoodTable
    },
    props: {
      columns: {
        type: Array,
        required: true
      },
      rows: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style>
  @import 'vue-good-table-next/dist/vue-good-table-next.css';
  </style>
  