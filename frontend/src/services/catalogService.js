import api from "./api";

export const catalogService = {
  async getFacultades() {
    const response = await api.get("/catalogs/facultades");
    return response.data;
  },

  async getSedes() {
    const response = await api.get("/catalogs/sedes");
    // Filtrar "Manga" en caso de que exista (seguridad extra)
    const sedes = response.data.filter(
      (sede) => sede.nombre !== "Manga" && sede.nombre !== "manga"
    );
    return sedes;
  },

  async getCarreras(facultadId = null) {
    const params = facultadId ? { facultad_id: facultadId } : {};
    const response = await api.get("/catalogs/carreras", { params });
    return response.data;
  },

  async createSede(nombre) {
    // Validar que no sea "Manga"
    const sedesValidas = [
      "Piedra de Bolívar",
      "Zaragocilla",
      "San Pablo",
      "El Carmen de Bolívar",
    ];

    if (!sedesValidas.includes(nombre)) {
      throw new Error(
        `Sede no válida. Sedes permitidas: ${sedesValidas.join(", ")}`
      );
    }

    const response = await api.post("/catalogs/sedes", { nombre });
    return response.data;
  },

  async getFacultades() {
    const response = await api.get("/catalogs/facultades");
    return response.data;
  },

  async getSedes() {
    const response = await api.get("/catalogs/sedes");
    return response.data;
  },

  async getCarreras(facultadId = null) {
    const params = facultadId ? { facultad_id: facultadId } : {};
    const response = await api.get("/catalogs/carreras", { params });
    return response.data;
  },
};
