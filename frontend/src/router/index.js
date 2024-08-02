
import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import NewProduct from '@/components/NewProduct.vue'
import NewPost from '../views/NewPost.vue'
import PostList from '../views/PostList.vue'
import Login from '../views/auth/Login.vue'
import ProductList from '@/views/ProductList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', component: () => import('../views/auth/Layout.vue'),
      children: [
        { path: '', component: () => import('../views/auth/Login.vue') },
        { path: 'registration', component: () => import('../views/auth/Registration.vue') },
        { path: 'forget-password', component: () => import('../views/auth/ForgetPassword.vue') },
        { path: 'reset-password', component: () => import('../views/auth/ResetPassword.vue') }
      ],
      meta: {
        guest: true
      }
    },
    {
      path: '/', component: () => import('../views/auth/Layout.vue'),
      children: [
        {
          path: '/postlist',
          name: 'postlist',
          component: PostList
        },
        {
          path: '/login',
          name: 'login',
          component:Login
        },
        {
          path: '/newpost',
          name: 'newpost',
          component: NewPost
        },
        {
          path: '/marketplace',
          name: 'marketplace',
          component: ProductList
        },
        {
          path: '/newproduct',
          name: 'newproduct',
          component: NewProduct
        },
      ],
      meta: {
        auth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!store.state.token // Check if the token exists in Vuex state
  const requiresAuth = to.matched.some(record => record.meta.auth)
  const isGuest = to.matched.some(record => record.meta.guest)

  if (requiresAuth && !isAuthenticated) {
    // If the route requires authentication and the user is not authenticated
    next({ path: '/' }) // Redirect to the login page or any other route
  } else if (isGuest && isAuthenticated) {
    // If the route is for guests and the user is authenticated
    next({ path: '/postlist' }) // Redirect to a protected route or dashboard
  } else {
    next() // Proceed to the requested route
  }
})

export default router
