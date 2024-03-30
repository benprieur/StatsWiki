<template>
  <div class="selectors-container">
    <div class="language-selector">
      <select v-model="selectedLanguage" @change="onLanguageChange">
        <option disabled value="">Lang</option>
        <option v-for="code in SUPPORTED_LANGUAGES" :key="code" :value="code">
          {{ code }}
        </option>
      </select>
      <img v-if="selectedLanguage" :src="`./assets/${selectedLanguage}.svg`" :alt="selectedLanguage" class="flag-img">
    </div>

    <div class="date-selector">
      <select v-model="selectedYear" @change="onYearChange">
        <option disabled value="">Year</option>
        <option v-for="year in years.slice(-10)" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
  
      <select v-model="selectedMonth" @change="onMonthChange">
        <option value="">Month</option>
        <option v-for="month in 12" :key="month" :value="month">
          {{ month }}
        </option>
      </select>
  
      <select v-model="selectedDay">
        <option value="">Day</option>
        <option v-for="day in daysInMonth" :key="day" :value="day">
          {{ day }}
        </option>
      </select>
    </div>
    
    <button class="button" @click="onSubmit">Go</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedYear: '',
      selectedMonth: '',
      selectedDay: '',
      selectedLanguage: '',
      SUPPORTED_LANGUAGES: ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh'],
      startDate: new Date(2015, 6, 1), // Les mois sont indexés à partir de 0
      endDate: new Date(new Date().setDate(new Date().getDate() - 1)),
    };
  },
  computed: {
    years() {
      const endYear = this.endDate.getFullYear();
      const startYear = this.startDate.getFullYear();
      let years = [];
      for (let year = startYear; year <= endYear; year++) {
        years.push(year);
      }
      return years;
    },
    daysInMonth() {
      if (this.selectedYear && this.selectedMonth) {
        return new Date(this.selectedYear, this.selectedMonth, 0).getDate();
      }
      return 31; // Par défaut, pour simplifier
    },
  },
  methods: {
    onYearChange() {
      this.selectedDay = ''; // Réinitialiser le jour lors du changement d'année
      this.selectedMonth = ''; // Assure que l'utilisateur doit rechoisir un mois, réinitialisation nécessaire pour cohérence
    },
    onMonthChange() {
      this.selectedDay = ''; // Réinitialiser le jour lors du changement de mois
    },
    onLanguageChange() {
      // Vous pouvez ajouter une logique ici si nécessaire quand la langue change
    },
    redirectToDate(lang, year, month, day) {
      // Vérifications initiales...
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();

      if (!lang || !year || year < 2015 || year > currentYear) {
        alert('Please ensure you select a valid language and year.');
        return;
      }

      // Pour l'année 2015...
      if (year === 2015 && month && month < 7) {
        alert('For 2015, the month must be at least July.');
        return;
      }

      // Construction de l'URL de redirection
      let redirectUrl = `/${lang}/${year}`;
      if (month) redirectUrl += `/${month}`;
      if (day) redirectUrl += `/${day}`;

      window.location.href = redirectUrl;
    },
    onSubmit() {
      const year = this.selectedYear ? Number(this.selectedYear) : undefined;
      const month = this.selectedMonth ? Number(this.selectedMonth) : undefined;
      const day = this.selectedDay ? Number(this.selectedDay) : undefined;

      this.redirectToDate(this.selectedLanguage, year, month, day);
    },
  }
};
</script>

<style>
.selectors-container {
  display: flex;
  align-items: center;
}

.language-selector, .date-selector {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.language-selector select, .date-selector select {
  margin: 2px;
  padding: 5px;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  background-color: rgb(54, 54, 54);
  color: white;
  font-size: 20px;
}

.flag-img {
  width: 30px;
  margin-left: 10px;
}

.button{
  background-color: rgb(54, 54, 54);
  color: rgb(0, 255, 38);
  font-size: 21px;
  display: inline-block;
}
</style>