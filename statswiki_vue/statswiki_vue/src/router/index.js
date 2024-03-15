import { createRouter, createWebHistory } from 'vue-router'; // Importer les modules de Vue Router depuis le package installé
import ArticleComponent from '../views/ArticleComponent.vue'; // Importer le composant ArticleComponent

const routes = [
  {
    path: '/:lang/:qid', 
    name: 'Article',
    component: ArticleComponent,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;