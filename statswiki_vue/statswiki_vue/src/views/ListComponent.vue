<template>
  <vue-good-table :columns="columns" :rows="rows" :pagination-options="{enabled: true}" :line-numbers="true" theme="black-rhino">
    <template v-slot:cell(qid)="props">
        <div :class="{'highlight-cell': !/^Q\d+$/.test(props.row.qid)}">{{ props.row.qid }}</div>
    </template>
  
    <template v-slot:cell(views)="props">
        <div class="align-right">{{ props.row.views }}</div>
    </template>
  </vue-good-table>
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
  
  .article{
    text-align: left;
    font-family: Arial, sans-serif;
    font-size: 25px;
    vertical-align: middle;
    text-decoration: underline; 
  }
  
  .normal-behavior{
    font-family: Arial, sans-serif;
    text-align: left;
    font-size: 22px;
    vertical-align: middle;
  }
  
  .align-right {
    font-family: Arial, sans-serif;
    text-align: right;
    font-size: 25px;
    vertical-align: middle;
  }
  
  .align-center {
    font-family: Arial, sans-serif;
    text-align: center;
    vertical-align: middle;
  }
  
  .highlight-cell {
    background-color: #f8d7da; /* Une teinte de rose clair */
  }
  </style>
  