import api from "./api";

export const authService = {
  async login(credentials) {
    // El backend espera JSON, no FormData
    const response = await api.post("/auth/login", {
      codigo_institucional: credentials.codigo_institucional,
      password: credentials.password,
    });
    return response.data;
  },

  async register(userData) {
    const response = await api.post("/auth/register", userData);
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get("/auth/me");
    return response.data;
  },

  async getProfesores() {
    const response = await api.get("/users/profesores");
    return response.data;
  },
};
