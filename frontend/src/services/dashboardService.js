import api from "./api";

export const dashboardService = {
  async getStats() {
    const response = await api.get("/dashboard/");
    return response.data;
  },

  async getTopProjects(limit = 5) {
    const response = await api.get("/dashboard/top-proyectos", {
      params: { limit },
    });
    return response.data;
  },
};
