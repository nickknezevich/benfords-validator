import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import FileExamplesView from '../views/FileExamplesView.vue'
import { useAuthStore } from '../stores/auth.store';
import AdminLayout from '/src/layouts/AdminLayout.vue';
import PublicLayout from '/src/layouts/PublicLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: AdminLayout,
      redirect: '/',
      children: [
        {
          path: '/',
          name: 'Home',
          component: HomeView
        }
      ]
    },
    {
      path: '/examples',
      name: 'Examples',
      component: AdminLayout,
      redirect: '/',
      children: [
        {
          path: '/examples',
          name: 'Examples',
          component: FileExamplesView
        }
      ]
    },
    // {
    //   path: '/examples',
    //   name: 'examples',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: FileExamplesView
    // },
    {
      path: '/login',
      name: 'SignIn',
      component: PublicLayout,
      redirect: '/login',
      children: [
        {
          path: '/login',
          name: 'Login',
          component: LoginView
        }
      ]
    }
    // {
    //   path: '/login',
    //   name: 'login',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/LoginView.vue')
    // }
  ]
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/examples'];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.user) {
      auth.returnUrl = to.fullPath;
      return '/login';
  }
});

export default router
