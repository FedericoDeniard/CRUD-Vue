import { createRouter, createWebHistory } from 'vue-router'
import UsersView from '../views/User/UsersView.vue'
import Create from '../views/User/Create.vue'
import Edit from '../views/User/Edit.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: UsersView,
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView,
    },
    {
      path: '/users/create',
      name: 'users-create',
      component: Create,
    },
    {
      path: '/users/:id/edit',
      name: 'users-edit',
      component: Edit,
    },
  ],
})

export default router
