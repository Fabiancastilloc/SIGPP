import api from "./api";

export const expenseService = {
  async getAll(params = {}) {
    const response = await api.get("/expenses/", { params });
    return response.data;
  },

  async getById(id) {
    const response = await api.get(`/expenses/${id}`);
    return response.data;
  },

  async create(expenseData) {
    const response = await api.post("/expenses/", expenseData);
    return response.data;
  },

  async approve(id) {
    const response = await api.patch(`/expenses/${id}/aprobar`);
    return response.data;
  },

  async reject(id) {
    const response = await api.patch(`/expenses/${id}/rechazar`);
    return response.data;
  },

  async delete(id) {
    const response = await api.delete(`/expenses/${id}`);
    return response.data;
  },
};
