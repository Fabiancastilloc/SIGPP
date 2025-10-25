import { defineStore } from 'pinia'
import authApi from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => {
      console.log('🔍 Verificando autenticación:', !!state.token)
      return !!state.token
    },
    userRole: (state) => state.user?.rol || null,
    userName: (state) => state.user?.nombre_completo || ''
  },
  
  actions: {
    async login(credentials) {
      try {
        console.log('🔑 Iniciando login...')
        const response = await authApi.login(credentials)
        
        this.token = response.data.access_token
        this.user = response.data.user
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        
        console.log('✅ Login exitoso')
        console.log('Token guardado:', this.token.substring(0, 30) + '...')
        console.log('Usuario:', this.user)
        
        return response.data
      } catch (error) {
        console.error('❌ Error en login:', error)
        throw error
      }
    },
    
    logout() {
      console.log('🚪 Cerrando sesión')
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    
    initializeAuth() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      
      if (token && user) {
        this.token = token
        try {
          this.user = JSON.parse(user)
          console.log('✅ Sesión recuperada:', this.user.nombre_completo)
        } catch (e) {
          console.error('❌ Error parseando usuario:', e)
          this.logout()
        }
      } else {
        console.log('ℹ️ No hay sesión guardada')
      }
    }
  }
})
