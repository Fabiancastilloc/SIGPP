import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Auth/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Auth/RegisterView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/MyProfile.vue'),
    meta: { requiresAuth: true }
  },
  
  // ============================================
  // 👨‍🎓 RUTAS DE ESTUDIANTE (CON EXPENSES)
  // ============================================
  {
    path: '/student',
    name: 'StudentDashboard',
    component: () => import('../views/Student/StudentDashboard.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/create-project',
    name: 'CreateProject',
    component: () => import('../views/Student/CreateProject.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/edit-project/:id',
    name: 'EditProject',
    component: () => import('../views/Student/EditProject.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/project/:id',
    name: 'StudentProjectDetail',
    component: () => import('../views/Student/ProjectDetail.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/project/:id/expenses',
    name: 'ExpensesView',
    component: () => import('../views/Student/ExpensesView.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/project/:id/expenses/register',
    name: 'RegisterExpense',
    component: () => import('../views/Student/RegisterExpense.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  {
    path: '/student/project/:projectId/expense/:expenseId',
    name: 'ExpenseDetail',
    component: () => import('../views/Student/ExpenseDetail.vue'),
    meta: { requiresAuth: true, role: 'estudiante' }
  },
  
  // ============================================
  // 👨‍🏫 RUTAS DE PROFESOR (CON EXPENSES)
  // ============================================
  {
    path: '/professor',
    name: 'ProfessorDashboard',
    component: () => import('../views/Professor/ProfessorDashboard.vue'),
    meta: { requiresAuth: true, role: 'profesor' }
  },
  {
    path: '/professor/project/:id',
    name: 'ProfessorProjectDetail',
    component: () => import('../views/Student/ProjectDetail.vue'),
    meta: { requiresAuth: true, role: 'profesor' }
  },
  {
    path: '/professor/project/:id/expenses',
    name: 'ProfessorExpenses',
    component: () => import('../views/Professor/ExpensesView.vue'),
    meta: { requiresAuth: true, role: 'profesor' }
  },
  
  // ============================================
  // 💼 RUTAS DE FINANCIERA (CON EXPENSES)
  // ============================================
  {
    path: '/finance',
    name: 'FinanceDashboard',
    component: () => import('../views/Finance/FinanceDashboard.vue'),
    meta: { requiresAuth: true, role: 'financiera' }
  },
  {
    path: '/finance/project/:id',
    name: 'FinanceProjectDetail',
    component: () => import('../views/Student/ProjectDetail.vue'),
    meta: { requiresAuth: true, role: 'financiera' }
  },
  {
    path: '/finance/project/:id/expenses',
    name: 'FinanceExpenses',
    component: () => import('../views/Finance/ExpensesView.vue'),
    meta: { requiresAuth: true, role: 'financiera' }
  },
  
  // ============================================
  // 🔍 RUTAS DE AUDITOR (CON EXPENSES)
  // ============================================
  {
    path: '/auditor',
    name: 'AuditorDashboard',
    component: () => import('../views/Auditor/AuditorDashboard.vue'),
    meta: { requiresAuth: true, role: 'auditor' }
  },
  {
    path: '/auditor/project/:id',
    name: 'AuditorProjectDetail',
    component: () => import('../views/Student/ProjectDetail.vue'),
    meta: { requiresAuth: true, role: 'auditor' }
  },
  {
    path: '/auditor/project/:id/expenses',
    name: 'AuditorExpenses',
    component: () => import('../views/Auditor/ExpensesView.vue'),
    meta: { requiresAuth: true, role: 'auditor' }
  },
  {
    path: '/auditor/project/:id/audit',
    name: 'AuditLog',
    component: () => import('../views/Auditor/AuditLog.vue'),
    meta: { requiresAuth: true, role: 'auditor' }
  },
  
  // ============================================
  // 👑 RUTAS DE ADMINISTRADOR
  // ============================================
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/Admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },
  {
    path: '/admin/projects',
    name: 'AdminProjects',
    component: () => import('../views/Admin/AdminProjects.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/Admin/AdminUsers.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },
  {
    path: '/admin/reports',
    name: 'AdminReports',
    component: () => import('../views/Admin/AdminReports.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: () => import('../views/Admin/AdminSettings.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },
  {
    path: '/admin/project/:id',
    name: 'AdminProjectDetail',
    component: () => import('../views/Student/ProjectDetail.vue'),
    meta: { requiresAuth: true, role: 'superusuario' }
  },

  {
  path: '/admin/project/:id',
  name: 'AdminProjectDetail',
  component: () => import('../views/Student/ProjectDetail.vue'),
  meta: { requiresAuth: true, role: 'superusuario' }
},
{
  path: '/admin/project/:id/expenses',
  name: 'AdminProjectExpenses',
  component: () => import('../views/Admin/AdminProjectExpenses.vue'),
  meta: { requiresAuth: true, role: 'superusuario' }
},
{
  path: '/admin/project/:id/history',
  name: 'AdminProjectHistory',
  component: () => import('../views/Admin/AdminProjectHistory.vue'),
  meta: { requiresAuth: true, role: 'superusuario' }
},
  
  // ============================================
  // ❌ RUTA 404
  // ============================================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  if (to.meta.role && authStore.user?.rol !== to.meta.role) {
    const dashboards = {
      'estudiante': '/student',
      'profesor': '/professor',
      'financiera': '/finance',
      'auditor': '/auditor',
      'superusuario': '/admin'
    }
    next(dashboards[authStore.user?.rol] || '/')
    return
  }
  
  if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    const dashboards = {
      'estudiante': '/student',
      'profesor': '/professor',
      'financiera': '/finance',
      'auditor': '/auditor',
      'superusuario': '/admin'
    }
    next(dashboards[authStore.user?.rol] || '/')
    return
  }
  
  next()
})

export default router
