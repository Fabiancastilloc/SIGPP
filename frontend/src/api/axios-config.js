import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  maxRedirects: 5,
  validateStatus: (status) => status >= 200 && status < 400
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('🔑 Token agregado:', token.substring(0, 30) + '...')
    } else {
      console.warn('⚠️ No hay token')
    }
    return config
  },
  (error) => {
    console.error('❌ Error en request:', error)
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ Response:', response.config.url, response.status)
    return response
  },
  (error) => {
    console.error('❌ Error response:', error.config?.url, error.response?.status)
    
    if (error.response?.status === 401) {
      console.warn('🚪 401 - Limpiando sesión')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
