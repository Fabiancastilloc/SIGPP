// frontend/src/api/catalogs.js
/**
 * API de Catálogos - SIGPP
 * Manejo de peticiones para datos maestros del sistema
 */

import apiClient from './axios-config'

const catalogsApi = {
  // ==================== SEDES ====================
  
  /**
   * Obtener todas las sedes disponibles
   * @returns {Promise} Lista de sedes
   */
  getSedes() {
    return apiClient.get('/catalogs/sedes')
  },

  // ==================== FACULTADES ====================
  
  /**
   * Obtener facultades, opcionalmente filtradas por sede
   * @param {number|null} sedeId - ID de la sede para filtrar
   * @returns {Promise} Lista de facultades
   */
  getFacultades(sedeId = null) {
    const params = {}
    if (sedeId) {
      params.sede_id = sedeId
    }
    return apiClient.get('/catalogs/facultades', { params })
  },

  // ==================== CARRERAS ====================
  
  /**
   * Obtener carreras, opcionalmente filtradas por facultad
   * @param {number|null} facultadId - ID de la facultad para filtrar
   * @returns {Promise} Lista de carreras
   */
  getCarreras(facultadId = null) {
    const params = {}
    if (facultadId) {
      params.facultad_id = facultadId
    }
    return apiClient.get('/catalogs/carreras', { params })
  },

  /**
   * Obtener información completa de una carrera
   * @param {number} carreraId - ID de la carrera
   * @returns {Promise} Información detallada de la carrera
   */
  getCarreraInfo(carreraId) {
    return apiClient.get(`/catalogs/carrera/${carreraId}/info`)
  },

  // ==================== PROFESORES ====================
  
  /**
   * Obtener lista de profesores activos
   * @param {number|null} facultadId - Filtrar por facultad (opcional)
   * @returns {Promise} Lista de profesores
   */
  getProfesores(facultadId = null) {
    const params = {}
    if (facultadId) {
      params.facultad_id = facultadId
    }
    return apiClient.get('/catalogs/profesores', { params })
  },

  // ==================== ESTUDIANTES ====================
  
  /**
   * Obtener estudiantes de la misma carrera que el usuario actual
   * @returns {Promise} Lista de estudiantes de la misma carrera
   */
  getStudentsSameCareer() {
    return apiClient.get('/catalogs/students/same-career')
  },

  /**
   * Buscar estudiantes por nombre o código
   * @param {string} query - Término de búsqueda
   * @param {number|null} carreraId - Filtrar por carrera
   * @param {number|null} semestre - Filtrar por semestre
   * @param {number} limit - Límite de resultados
   * @returns {Promise} Lista de estudiantes encontrados
   */
  searchStudents(query = '', carreraId = null, semestre = null, limit = 20) {
    const params = { q: query, limit }
    
    if (carreraId) {
      params.carrera_id = carreraId
    }
    
    if (semestre) {
      params.semestre = semestre
    }
    
    return apiClient.get('/catalogs/students/search', { params })
  },

  /**
   * Obtener estudiantes de una carrera específica
   * @param {number} carreraId - ID de la carrera
   * @param {number|null} semestre - Filtrar por semestre
   * @returns {Promise} Lista de estudiantes de la carrera
   */
  getStudentsByCareer(carreraId, semestre = null) {
    const params = {}
    if (semestre) {
      params.semestre = semestre
    }
    return apiClient.get(`/catalogs/students/by-career/${carreraId}`, { params })
  },

  // ==================== ESTADÍSTICAS ====================
  
  /**
   * Obtener estadísticas generales de catálogos
   * @returns {Promise} Objeto con contadores de sedes, facultades, etc.
   */
  getStats() {
    return apiClient.get('/catalogs/stats')
  },

  // ==================== UTILIDADES ====================
  
  /**
   * Obtener jerarquía completa: Sede > Facultad > Carrera
   * @param {number} sedeId - ID de la sede
   * @returns {Promise} Estructura jerárquica completa
   */
  async getHierarchy(sedeId) {
    try {
      const [sedesRes, facultadesRes] = await Promise.all([
        this.getSedes(),
        this.getFacultades(sedeId)
      ])
      
      const sede = sedesRes.data.find(s => s.id === sedeId)
      const facultades = facultadesRes.data
      
      const hierarchy = {
        sede,
        facultades: []
      }
      
      for (const facultad of facultades) {
        const carrerasRes = await this.getCarreras(facultad.id)
        hierarchy.facultades.push({
          ...facultad,
          carreras: carrerasRes.data
        })
      }
      
      return hierarchy
      
    } catch (error) {
      console.error('Error obteniendo jerarquía:', error)
      throw error
    }
  },

  /**
   * Validar si un profesor existe
   * @param {number} profesorId - ID del profesor
   * @returns {Promise<boolean>} true si existe, false si no
   */
  async validateProfesor(profesorId) {
    try {
      const response = await this.getProfesores()
      return response.data.some(p => p.id === profesorId)
    } catch (error) {
      console.error('Error validando profesor:', error)
      return false
    }
  },

  /**
   * Validar si un estudiante existe
   * @param {number} studentId - ID del estudiante
   * @returns {Promise<boolean>} true si existe, false si no
   */
  async validateStudent(studentId) {
    try {
      const response = await this.getStudentsSameCareer()
      return response.data.some(s => s.id === studentId)
    } catch (error) {
      console.error('Error validando estudiante:', error)
      return false
    }
  }
}

export default catalogsApi
