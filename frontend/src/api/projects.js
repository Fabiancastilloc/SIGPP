// frontend/src/api/projects.js
import apiClient from './axios-config'

const projectsApi = {
  /**
   * Obtener lista de proyectos con filtros opcionales
   * @param {Object} filters - Filtros opcionales (estado, etc.)
   */
  getProjects: (filters = {}) => {
    return apiClient.get('/projects', { params: filters })
  },
  
  /**
   * Obtener proyecto por ID
   * @param {Number} id - ID del proyecto
   */
  getProjectById: (id) => {
    return apiClient.get(`/projects/${id}`)
  },
  
  /**
   * Crear nuevo proyecto
   * @param {Object} projectData - Datos del proyecto
   */
  createProject: (projectData) => {
    return apiClient.post('/projects', projectData)
  },
  
  /**
   * Actualizar proyecto existente
   * @param {Number} projectId - ID del proyecto
   * @param {Object} projectData - Datos actualizados
   */
  updateProject: (projectId, projectData) => {
    return apiClient.put(`/projects/${projectId}`, projectData)
  },
  
  /**
   * Enviar proyecto para revisión del profesor
   * @param {Number} projectId - ID del proyecto
   */
  submitProject: (projectId) => {
    return apiClient.post(`/projects/${projectId}/submit`)
  },
  
  /**
   * Validar proyecto (Profesor)
   * @param {Number} projectId - ID del proyecto
   * @param {Object} validationData - { aprobado: boolean, comentarios: string }
   */
  validateProject: (projectId, validationData) => {
    return apiClient.post(`/projects/${projectId}/validate`, validationData)
  },
  
  /**
   * Activar proyecto y asignar presupuesto (Financiera)
   * @param {Number} projectId - ID del proyecto
   * @param {Object} activationData - { aprobado: boolean, presupuesto_asignado: number, comentarios: string }
   */
  activateProject: (projectId, activationData) => {
    return apiClient.post(`/projects/${projectId}/activate`, activationData)
  },
  
  /**
   * Obtener historial de cambios del proyecto
   * @param {Number} projectId - ID del proyecto
   */
  getProjectHistory: (projectId) => {
    return apiClient.get(`/projects/${projectId}/history`)
  },
  
  /**
   * Obtener proyectos donde el estudiante es colaborador
   */
  getProjectsAsCollaborator: () => {
    return apiClient.get('/projects/as-collaborator')
  },
  
  /**
   * Obtener todos los proyectos donde el estudiante está involucrado
   * (Propios + Como colaborador)
   */
  getAllProjectsInvolved: () => {
    return apiClient.get('/projects/all-involved')
  },
  
  /**
   * Eliminar proyecto (solo borradores)
   * @param {Number} projectId - ID del proyecto
   */
  deleteProject: (projectId) => {
    return apiClient.delete(`/projects/${projectId}`)
  },
  
  /**
   * Rechazar proyecto
   * @param {Number} projectId - ID del proyecto
   * @param {Object} rejectionData - { comentarios: string }
   */
  rejectProject: (projectId, rejectionData) => {
    return apiClient.post(`/projects/${projectId}/reject`, rejectionData)
  }
}

export default projectsApi
