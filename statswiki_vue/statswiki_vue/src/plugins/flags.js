export default {
  install(app) {
    app.config.globalProperties.$getFlagUrl = (langCode) => {
      // Utilisation de import.meta.env.BASE_URL pour obtenir l'URL de base
      const flagUrl = `${import.meta.env.BASE_URL}assets/${langCode}.svg`;
      return flagUrl;
    };
  }
};