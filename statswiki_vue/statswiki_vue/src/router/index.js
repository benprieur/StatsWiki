import { createRouter, createWebHistory } from 'vue-router'; // Importer les modules de Vue Router depuis le package installé
import ArticleComponent from '../views/ArticleComponent.vue'; 
import YearComponent from '../views/YearComponent.vue';

const routes = [
  {
    path: '/:lang/:qid(Q\\d+)', 
    name: 'Article',
    component: ArticleComponent,
    props: true,
  },
  {
    path: '/:lang/:year(\\d+)', 
    name: 'Year',
    component: YearComponent,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;