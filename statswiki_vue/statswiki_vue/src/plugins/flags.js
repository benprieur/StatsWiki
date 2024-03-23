export default {
    install(app) {
      app.config.globalProperties.$getFlagUrl = (langCode) => {
        // Chemin direct depuis le dossier public
        const flagUrl = `/assets/${langCode}.svg`;
        return flagUrl;
      };
    },
};