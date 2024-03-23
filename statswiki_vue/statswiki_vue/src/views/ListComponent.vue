<template>
<vue-good-table :columns="columns" :rows="rows" :pagination-options="{enabled: true}" :line-numbers="true" theme="black-rhino">
 
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
  
  .normal-behavior{
    text-align: left;
    font-size: 17px !important;
    vertical-align: middle;
  }

  .align-right {
    text-align: right;
    font-size: 18px !important;
    vertical-align: middle;
  }

  .align-center {
    text-align: center;
    vertical-align: middle;
  }

</style>
  