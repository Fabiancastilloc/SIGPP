import { defineStore } from "pinia";
import { authService } from "@/services/authService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.rol || null,
  },

  actions: {
    async login(credentials) {
      try {
        console.log("Intentando login con:", credentials);
        const response = await authService.login(credentials);
        console.log("Respuesta del login:", response);

        this.token = response.access_token;
        this.user = response.usuario;

        localStorage.setItem("token", response.access_token);

        return response;
      } catch (error) {
        console.error("Error completo en login:", error);
        console.error("Respuesta del error:", error.response?.data);
        throw error;
      }
    },

    async register(userData) {
      try {
        console.log("Intentando registro con:", userData);
        const response = await authService.register(userData);
        console.log("Respuesta del registro:", response);

        this.token = response.access_token;
        this.user = response.usuario;

        localStorage.setItem("token", response.access_token);

        return response;
      } catch (error) {
        console.error("Error completo en registro:", error);
        console.error("Respuesta del error:", error.response?.data);
        throw error;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
    },

    async checkAuth() {
      if (this.token) {
        try {
          const user = await authService.getCurrentUser();
          this.user = user;
        } catch (error) {
          console.error("Error al verificar autenticación:", error);
          this.logout();
        }
      }
    },
  },
});
