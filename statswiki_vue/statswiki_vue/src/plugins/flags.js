export default {
  install(app) {
    /*
    app.config.globalProperties.$getFlagUrl = (langCode) => {
      try {
        // Utilisation d'une URL relative au dossier public pour accéder aux drapeaux
        const flagUrl = new URL(`/assets/${langCode}.svg`, import.meta.url).href;
        return flagUrl;
      } catch (error) {
        console.error("Could not load the flag image:", error);
        return '';
      }
    };
    */
    app.config.globalProperties.$getFlagUrl = (langCode) => {
      // Utilisation de import.meta.env.BASE_URL pour obtenir l'URL de base
      const flagUrl = `${import.meta.env.BASE_URL}assets/${langCode}.svg`;
      return flagUrl;
    };
  }
};