import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', requiresAuth: true },
      },
      {
        path: 'strategies',
        name: 'Strategies',
        component: () => import('@/views/Strategies/index.vue'),
        meta: { title: '策略管理', requiresAuth: true },
      },
      {
        path: 'strategies/:id',
        name: 'StrategyDetail',
        component: () => import('@/views/Strategies/Detail.vue'),
        meta: { title: '策略详情', requiresAuth: true },
      },
      {
        path: 'backtests',
        name: 'Backtests',
        component: () => import('@/views/Backtests/index.vue'),
        meta: { title: '回测管理', requiresAuth: true },
      },
      {
        path: 'backtests/:id',
        name: 'BacktestDetail',
        component: () => import('@/views/Backtests/Detail.vue'),
        meta: { title: '回测详情', requiresAuth: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && userStore.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router

