import { createRouter, createWebHistory } from 'vue-router'; 
import ArticleComponent from '../views/ArticleComponent.vue'; 
import YearComponent from '../views/YearComponent.vue'; 
import MonthComponent from '../views/MonthComponent.vue'; 
import DayComponent from '../views/DayComponent.vue'; 
import LangComponent from '../views/LangComponent.vue'; 

const routes = [
  {
    path: '/:lang(ar|de|en|eo|es|fr|ja|he|hy|it|ko|nl|pl|pt|ru|uk|zh)/:qid(Q\\d+)', 
    name: 'Article',
    component: ArticleComponent,
    props: true,
  },
  {
    path: '/:lang(ar|de|en|eo|es|fr|ja|he|hy|it|ko|nl|pl|pt|ru|uk|zh)/:year(2015|2016|2017|2018|2019|2020|2021|2022|2023|2024)', 
    name: 'Year',
    component: YearComponent,
    props: true,
  },
  {
    path: '/:lang(ar|de|en|eo|es|fr|ja|he|hy|it|ko|nl|pl|pt|ru|uk|zh)/:year(2015|2016|2017|2018|2019|2020|2021|2022|2023|2024)/:month(0?[1-9]|1[0-2])',
    name: 'Month',
    component: MonthComponent,
    props: true,
  },
  {
    path: '/:lang(ar|de|en|eo|es|fr|ja|he|hy|it|ko|nl|pl|pt|ru|uk|zh)/:year(2015|2016|2017|2018|2019|2020|2021|2022|2023|2024)/:month(0?[1-9]|1[0-2])/:day(0?[1-9]|1[0-9]||2[0-9]|3[0-1])',
    name: 'Day',
    component: DayComponent,
    props: true,
  },
  {
    path: '/:lang(ar|de|en|eo|es|fr|ja|he|hy|it|ko|nl|pl|pt|ru|uk|zh)',
    name: 'Lang',
    component: LangComponent,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;