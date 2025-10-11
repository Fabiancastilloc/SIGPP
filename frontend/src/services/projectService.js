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

  async update(id, projectData) {
    const response = await api.put(`/projects/${id}`, projectData);
    return response.data;
  },

  // CORREGIDO: Enviar estado como query parameter
  async updateStatus(id, estado) {
    const response = await api.patch(`/projects/${id}/estado`, null, {
      params: { nuevo_estado: estado },
    });
    return response.data;
  },

  // NUEVO: Asignar presupuesto (Finanzas)
  async asignarPresupuesto(id, presupuestoAsignado, comentarios = null) {
    const response = await api.patch(
      `/projects/${id}/asignar-presupuesto`,
      null,
      {
        params: {
          presupuesto_asignado: presupuestoAsignado,
          comentarios: comentarios,
        },
      }
    );
    return response.data;
  },

  async delete(id) {
    const response = await api.delete(`/projects/${id}`);
    return response.data;
  },
};
