<template>
    <footer class="footer-container">
      <a href="https://twitter.com/StatsWiki" target="_blank" class="social-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5a/X_icon_2.svg" alt="Twitter"/>
        Twitter
      </a>
      <a href="https://instagram.com/StatsWiki" target="_blank" class="social-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg" alt="Instagram"/>
        Instagram
      </a>
      @Medialoco
    </footer>
  </template>
  
  <script>
  export default {
    name: "FooterComponent",
  };
  </script>
  
  <style scoped>
  .footer-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: black;
    color: white;
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
  }
  
  .social-link {
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
  }
  
  .social-link img {
    margin-right: 8px;
    width: 24px; /* Adjust size as needed */
  }
  </style>