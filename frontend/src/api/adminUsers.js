// frontend/src/api/adminUsers.js
import apiClient from './axios-config'

const adminUsersApi = {
  // Listar usuarios con filtros
  getUsers: (params = {}) => {
    const query = new URLSearchParams()
    if (params.page) query.append('page', params.page)
    if (params.per_page) query.append('per_page', params.per_page)
    if (params.search) query.append('search', params.search)
    if (params.rol) query.append('rol', params.rol)
    if (params.is_active !== undefined && params.is_active !== '') {
      query.append('is_active', params.is_active)
    }
    return apiClient.get(`/admin/users?${query.toString()}`)
  },
  
  // Obtener usuario
  getUser: (id) => apiClient.get(`/admin/users/${id}`),
  
  // Crear usuario (usa tu schema UserRegister)
  createUser: (data) => apiClient.post('/admin/users', data),
  
  // Actualizar usuario
  updateUser: (id, data) => apiClient.put(`/admin/users/${id}`, data),
  
  // Eliminar usuario
  deleteUser: (id) => apiClient.delete(`/admin/users/${id}`),
  
  // Resetear contraseña
  resetPassword: (id, newPassword) => apiClient.post(`/admin/users/${id}/reset-password`, { new_password: newPassword }),
  
  // Toggle activo/inactivo
  toggleActive: (id) => apiClient.post(`/admin/users/${id}/toggle-active`),
  
  // Estadísticas
  getStats: () => apiClient.get('/admin/users/stats/summary')
}

export default adminUsersApi
