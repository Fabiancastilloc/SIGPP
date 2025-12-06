// frontend/src/api/members.js
import apiClient from './axios-config'

const membersApi = {
  // Obtener colaboradores
  getMembers(projectId) {
    return apiClient.get(`/projects/${projectId}/members`)
  },
  
  // Agregar colaborador
  addMember(projectId, studentId) {
    return apiClient.post(`/projects/${projectId}/members`, { student_id: studentId })
  },
  
  // Eliminar colaborador
  removeMember(projectId, memberId) {
    return apiClient.delete(`/projects/${projectId}/members/${memberId}`)
  },
  
  // Solicitar unirse
  requestMembership(projectId, message) {
    return apiClient.post(`/projects/${projectId}/members/request`, { message })
  },
  
  // Obtener solicitudes pendientes
  getPendingRequests(projectId) {
    return apiClient.get(`/projects/${projectId}/members/requests`)
  },
  
  // Responder solicitud
  respondRequest(projectId, requestId, approve, message = '') {
    return apiClient.post(`/projects/${projectId}/members/requests/${requestId}/respond`, {
      approve,
      message
    })
  },
  
  // Buscar estudiantes
  searchStudents(query) {
    return apiClient.get(`/api/v1/catalogs/students`, { params: { q: query } })
  }
}

export default membersApi
