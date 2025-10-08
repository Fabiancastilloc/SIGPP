import { defineStore } from "pinia";
import { authService } from "@/services/authService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user")) || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.rol,
    isEstudiante: (state) => state.user?.rol === "estudiante",
    isProfesor: (state) => state.user?.rol === "profesor",
    isFinanciera: (state) => state.user?.rol === "financiera",
    isAuditor: (state) => state.user?.rol === "auditor",
  },

  actions: {
    async login(credentials) {
      try {
        const response = await authService.login(credentials);
        this.token = response.access_token;
        this.user = response.usuario;
        localStorage.setItem("token", response.access_token);
        localStorage.setItem("user", JSON.stringify(response.usuario));
        return response;
      } catch (error) {
        throw error;
      }
    },

    async register(userData) {
      try {
        const response = await authService.register(userData);
        return response;
      } catch (error) {
        throw error;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    async loadCurrentUser() {
      if (this.token) {
        try {
          const user = await authService.getCurrentUser();
          this.user = user;
          localStorage.setItem("user", JSON.stringify(user));
        } catch (error) {
          this.logout();
        }
      }
    },
  },
});
