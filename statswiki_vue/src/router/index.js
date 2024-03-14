import { createRouter, createWebHistory } from 'vue-router';
import ArticleComponent from '../views/ArticleComponent.vue';

const routes = [
  {
    path: '/api',
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