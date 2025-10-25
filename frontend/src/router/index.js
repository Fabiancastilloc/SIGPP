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
  // 👨‍🎓 RUTAS DE ESTUDIANTE
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
  
  // ============================================
  // 👨‍🏫 RUTAS DE PROFESOR
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
  
  // ============================================
  // 💼 RUTAS DE FINANCIERA
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
  
  // ============================================
  // 🔍 RUTAS DE AUDITOR
  // ============================================
  {
    path: '/auditor',
    name: 'AuditorDashboard',
    component: () => import('../views/Auditor/AuditorDashboard.vue'),
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

  
  // ============================================
  // ❌ RUTA 404
  // ============================================
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ============================================
// 🔒 GUARD DE AUTENTICACIÓN
// ============================================
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  console.log('🛣️ Navegando a:', to.path)
  console.log('👤 Usuario:', authStore.user?.nombre_completo)
  console.log('🔐 Autenticado:', authStore.isAuthenticated)
  
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    console.warn('⚠️ Ruta protegida, redirigiendo a login')
    next('/login')
    return
  }
  
  // Verificar rol si la ruta lo requiere
  if (to.meta.role && authStore.user?.rol !== to.meta.role) {
    console.warn('⚠️ Rol incorrecto:', authStore.user?.rol, 'requerido:', to.meta.role)
    
    // Redirigir al dashboard correspondiente según su rol
    const dashboards = {
      'estudiante': '/student',
      'profesor': '/professor',
      'financiera': '/finance',
      'auditor': '/auditor',
      'superusuario': '/admin'
    }
    
    const userDashboard = dashboards[authStore.user?.rol]
    if (userDashboard && to.path !== userDashboard) {
      next(userDashboard)
    } else {
      next('/')
    }
    return
  }
  
  // Si está en login/register y ya está autenticado, redirigir a dashboard
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
  
  console.log('✅ Navegación permitida')
  next()
})

export default router
