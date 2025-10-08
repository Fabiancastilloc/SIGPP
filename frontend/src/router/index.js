import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/auth/LoginView.vue"),
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/auth/RegisterView.vue"),
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("@/views/student/DashboardView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects",
    name: "Projects",
    component: () => import("@/views/student/ProjectsView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects/create",
    name: "ProjectCreate",
    component: () => import("@/views/student/ProjectCreateView.vue"),
    meta: { requiresAuth: true, role: "estudiante" },
  },
  {
    path: "/expenses",
    name: "Expenses",
    component: () => import("@/views/student/ExpensesView.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else if (to.meta.role && authStore.userRole !== to.meta.role) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
