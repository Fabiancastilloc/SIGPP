import { defineStore } from "pinia";
import { catalogService } from "@/services/catalogService";

export const useCatalogStore = defineStore("catalog", {
  state: () => ({
    facultades: [],
    sedes: [],
    carreras: [],
    loading: false,
  }),

  actions: {
    async loadFacultades() {
      try {
        this.loading = true;
        this.facultades = await catalogService.getFacultades();
      } catch (error) {
        console.error("Error loading facultades:", error);
      } finally {
        this.loading = false;
      }
    },

    async loadSedes() {
      try {
        this.loading = true;
        this.sedes = await catalogService.getSedes();
      } catch (error) {
        console.error("Error loading sedes:", error);
      } finally {
        this.loading = false;
      }
    },

    async loadCarreras(facultadId = null) {
      try {
        this.loading = true;
        this.carreras = await catalogService.getCarreras(facultadId);
      } catch (error) {
        console.error("Error loading carreras:", error);
      } finally {
        this.loading = false;
      }
    },

    async createFacultad(nombre) {
      const nuevaFacultad = await catalogService.createFacultad(nombre);
      this.facultades.push(nuevaFacultad);
      return nuevaFacultad;
    },

    async createSede(nombre) {
      const nuevaSede = await catalogService.createSede(nombre);
      this.sedes.push(nuevaSede);
      return nuevaSede;
    },

    async createCarrera(nombre, facultadId) {
      const nuevaCarrera = await catalogService.createCarrera(
        nombre,
        facultadId
      );
      this.carreras.push(nuevaCarrera);
      return nuevaCarrera;
    },
  },
});
