import api from "./api";

export const projectService = {
  async getAll(params = {}) {
    const response = await api.get("/projects/", { params });
    return response.data;
  },

  async getById(id) {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },

  async create(projectData) {
    const response = await api.post("/projects/", projectData);
    return response.data;
  },

  async updateStatus(id, estado) {
    const response = await api.patch(`/projects/${id}/estado`, null, {
      params: { nuevo_estado: estado },
    });
    return response.data;
  },

  async delete(id) {
    const response = await api.delete(`/projects/${id}`);
    return response.data;
  },
};
