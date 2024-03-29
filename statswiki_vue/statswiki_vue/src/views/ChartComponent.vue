<template>
    <div>
      <canvas ref="myChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  export default {
    name: 'ChartComponent',
    props: {
      data: {
        type: Object,
        required: true,
      },
      options: {
        responsive: true, // Assure que le graphique est responsive
        maintainAspectRatio: false, // Permet au graphique de s'étirer en hauteur
      },
    },
    data() {
      return {
        chart: null,
        colorIndex: 0,
        colors: [
          'rgb(0, 0, 0)',
          'rgb(135, 206, 235)',
          'rgb(128, 128, 0)',
          'rgb(255, 165, 0)',
          'rgb(255, 255, 0)',
          'rgb(0, 0, 128)',
          'rgb(128, 0, 128)',
          'rgb(255, 192, 203)',
          'rgb(128, 128, 128)',
          'rgb(0, 255, 255)',
        ],
      };
    },
    mounted() {
      this.$nextTick(() => {
        if (this.$refs.myChart) {
          this.createChart();
        }
      });
    },
    methods: {
      createChart() {
        const ctx = this.$refs.myChart.getContext('2d');
        const dataSets = this.prepareDataSets();
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: this.getAllLabels(),
            datasets: dataSets,
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      },
      prepareDataSets() {
          const dataSets = [];
          Object.keys(this.data).forEach((key) => {
              const dataSet = {
                  label: key,
                  data: [],
                  fill: false,
                  borderColor: this.getNextColor(),
                  tension: 0, // Pour des lignes droites
                  spanGaps: true,
              };
              
              // Obtenir seulement les entrées non nulles pour chaque série de données
              const nonNullEntries = Object.entries(this.data[key]).filter(([label, value]) => value !== 0 && value !== null);
              
              // S'assurer qu'il y a des données non nulles
              if (nonNullEntries.length > 0) {
                  // Convertir les entrées filtrées en données pour le dataSet
                  nonNullEntries.forEach(([label, value]) => {
                      dataSet.data.push({ x: label, y: value });
                  });
              }
              
              dataSets.push(dataSet);
          });
          return dataSets;
      },
      getAllLabels() {
        const allLabels = new Set();
        Object.values(this.data).forEach((dict) => {
          Object.keys(dict).forEach((label) => {
            allLabels.add(label);
          });
        });
        return [...allLabels];
      },
      getNextColor() {
        const color = this.colors[this.colorIndex % this.colors.length];
        this.colorIndex++;
        return color;
      },
    },
  };
  </script>
  