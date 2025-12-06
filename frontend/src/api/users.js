// frontend/src/api/users.js
import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_URL = `${BASE_URL}/api`

const getToken = () => localStorage.getItem('token')

const usersApi = {
  // Obtener perfil actual
  getCurrentUser: async () => {
    const response = await axios.get(`${API_URL}/users/me`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    return response.data
  },

  // Actualizar perfil (asegura snake_case para backend)
  updateProfile: async (userId, userData) => {
    const payload = {
      nombre_completo: userData.nombre_completo || userData.nombrecompleto,
      email: userData.email
    }

    // Solo agregar campos académicos si existen
    if (userData.sede_id || userData.sedeid) {
      payload.sede_id = userData.sede_id || userData.sedeid
    }
    if (userData.facultad_id || userData.facultadid) {
      payload.facultad_id = userData.facultad_id || userData.facultadid
    }
    if (userData.carrera_id || userData.carreraid) {
      payload.carrera_id = userData.carrera_id || userData.carreraid
    }
    if (userData.semestre) {
      payload.semestre = parseInt(userData.semestre)
    }

    const response = await axios.put(`${API_URL}/users/${userId}`, payload, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    return response.data
  },

  // Cambiar contraseña (snake_case para backend)
  changePassword: async (passwordData) => {
    const payload = {
      current_password: passwordData.current_password || passwordData.currentpassword,
      new_password: passwordData.new_password || passwordData.newpassword
    }

    const response = await axios.post(`${API_URL}/users/change-password`, payload, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    return response.data
  },

  // Estadísticas
  getUserStats: async (userId) => {
    const response = await axios.get(`${API_URL}/users/${userId}/stats`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    return response.data
  }
}

export default usersApi
