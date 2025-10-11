import api from "./api";

export const reportService = {
  async exportProyectosPDF(estado = null) {
    const params = { formato: "pdf" };
    if (estado) params.estado = estado;

    const response = await api.get("/reports/proyectos/export", {
      params,
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `proyectos_${new Date().toISOString()}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  async exportProyectosExcel(estado = null) {
    const params = { formato: "excel" };
    if (estado) params.estado = estado;

    const response = await api.get("/reports/proyectos/export", {
      params,
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `proyectos_${new Date().toISOString()}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  async exportGastosPDF(proyectoId = null, estado = null) {
    const params = { formato: "pdf" };
    if (proyectoId) params.proyecto_id = proyectoId;
    if (estado) params.estado = estado;

    const response = await api.get("/reports/gastos/export", {
      params,
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `gastos_${new Date().toISOString()}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  async exportGastosExcel(proyectoId = null, estado = null) {
    const params = { formato: "excel" };
    if (proyectoId) params.proyecto_id = proyectoId;
    if (estado) params.estado = estado;

    const response = await api.get("/reports/gastos/export", {
      params,
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `gastos_${new Date().toISOString()}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};
