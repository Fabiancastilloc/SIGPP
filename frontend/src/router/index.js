import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// Layouts
import HomeView from "@/views/HomeView.vue";

// Auth
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";

// Student
import DashboardView from "@/views/student/DashboardView.vue";
import ProjectsView from "@/views/student/ProjectsView.vue";
import ProjectDetailView from "@/views/student/ProjectDetailView.vue";
import ProjectCreateView from "@/views/student/ProjectCreateView.vue";
import ProjectEditView from "@/views/student/ProjectEditView.vue";
import ExpensesView from "@/views/student/ExpensesView.vue";

// Professor
import ProfessorDashboardView from "@/views/professor/ProfessorDashboardView.vue";
import ProfessorProjectsView from "@/views/professor/ProfessorProjectsView.vue";
import ProfessorProjectDetailView from "@/views/professor/ProfessorProjectDetailView.vue";

// Finance
import FinanceDashboardView from "@/views/finance/FinanceDashboardView.vue";
import FinanceExpensesView from "@/views/finance/FinanceExpensesView.vue";
import FinanceProjectsView from "@/views/finance/FinanceProjectsView.vue";
import FinanceProjectDetailView from "@/views/finance/FinanceProjectDetailView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresGuest: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { requiresGuest: true },
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: { requiresGuest: true },
  },

  // Rutas de Estudiante
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },
  {
    path: "/proyectos",
    name: "proyectos",
    component: ProjectsView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },
  {
    path: "/proyectos/crear",
    name: "proyecto-crear",
    component: ProjectCreateView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },
  {
    path: "/proyectos/:id",
    name: "proyecto-detalle",
    component: ProjectDetailView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },
  {
    path: "/proyectos/:id/editar",
    name: "proyecto-editar",
    component: ProjectEditView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },
  {
    path: "/gastos",
    name: "gastos",
    component: ExpensesView,
    meta: { requiresAuth: true, roles: ["estudiante"] },
  },

  // Rutas de Profesor
  {
    path: "/profesor/dashboard",
    name: "profesor-dashboard",
    component: ProfessorDashboardView,
    meta: { requiresAuth: true, roles: ["profesor"] },
  },
  {
    path: "/profesor/proyectos",
    name: "profesor-proyectos",
    component: ProfessorProjectsView,
    meta: { requiresAuth: true, roles: ["profesor"] },
  },
  {
    path: "/profesor/proyectos/:id",
    name: "profesor-proyecto-detalle",
    component: ProfessorProjectDetailView,
    meta: { requiresAuth: true, roles: ["profesor"] },
  },

  // Rutas de Financiera
  {
    path: "/financiera/dashboard",
    name: "financiera-dashboard",
    component: FinanceDashboardView,
    meta: { requiresAuth: true, roles: ["financiera"] },
  },
  {
    path: "/financiera/proyectos",
    name: "financiera-proyectos",
    component: FinanceProjectsView,
    meta: { requiresAuth: true, roles: ["financiera"] },
  },
  {
    path: "/financiera/proyectos/:id",
    name: "financiera-proyecto-detalle",
    component: FinanceProjectDetailView,
    meta: { requiresAuth: true, roles: ["financiera"] },
  },
  {
    path: "/financiera/gastos",
    name: "financiera-gastos",
    component: FinanceExpensesView,
    meta: { requiresAuth: true, roles: ["financiera"] },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Verificar autenticación si hay token
  if (authStore.token && !authStore.user) {
    await authStore.checkAuth();
  }

  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.user?.rol;

  // Redirigir usuarios autenticados fuera de login/register
  if (to.meta.requiresGuest && isAuthenticated) {
    if (userRole === "estudiante") {
      return next({ name: "dashboard" });
    } else if (userRole === "profesor") {
      return next({ name: "profesor-dashboard" });
    } else if (userRole === "financiera") {
      return next({ name: "financiera-dashboard" });
    }
    return next({ name: "dashboard" });
  }

  // Proteger rutas que requieren autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "login" });
  }

  // Verificar roles
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    if (userRole === "estudiante") {
      return next({ name: "dashboard" });
    } else if (userRole === "profesor") {
      return next({ name: "profesor-dashboard" });
    } else if (userRole === "financiera") {
      return next({ name: "financiera-dashboard" });
    }
    return next({ name: "login" });
  }

  next();
});

export default router;
