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
      path: '/',
      component: () => import('../views/auth/Layout.vue'),
      children: [
        { path: '', name: 'login', component: Login },
        { path: 'registration', component: () => import('../views/auth/Registration.vue') },
        { path: 'forget-password', component: () => import('../views/auth/ForgetPassword.vue') },
        { path: 'reset-password', component: () => import('../views/auth/ResetPassword.vue') }
      ],
      meta: {
        guest: true
      }
    },
    {
      path: '/app', // A base path for authenticated routes
      component: () => import('../views/auth/Layout.vue'),
      children: [
        {
          path: 'postlist',
          name: 'postlist',
          component: PostList
        },
        {
          path: 'newpost',
          name: 'newpost',
          component: NewPost
        },
        {
          path: 'marketplace',
          name: 'marketplace',
          component: ProductList
        },
        {
          path: 'newproduct',
          name: 'newproduct',
          component: NewProduct
        }
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

  console.log(`Navigating to: ${to.fullPath}`)
  console.log(`Is authenticated: ${isAuthenticated}`)
  console.log(`Requires auth: ${requiresAuth}`)
  console.log(`Is guest route: ${isGuest}`)

  if (requiresAuth && !isAuthenticated) {
    console.log('Redirecting to login')
    next({ path: '/' }) // Redirect to login if the route requires authentication and the user is not authenticated
  } else if (isGuest && isAuthenticated) {
    console.log('Redirecting to post list')
    next({ path: '/app/postlist' }) // Redirect to a default authenticated route
  } else {
    console.log('Proceeding to route')
    next() // Proceed to the requested route
  }
})

export default router

