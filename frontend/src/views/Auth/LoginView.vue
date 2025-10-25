<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <div class="logo-circle">🎓</div>
          <h2>Bienvenido al SIGPP</h2>
          <p>Ingresa tus credenciales para continuar</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label class="form-label">
              <span class="label-icon">👤</span>
              Código Institucional
            </label>
            <input 
              v-model="credentials.codigo_institucional" 
              class="form-control" 
              placeholder="Ej: EST20251001"
              required 
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label class="form-label">
              <span class="label-icon">🔒</span>
              Contraseña
            </label>
            <div class="password-input-wrapper">
              <input 
                v-model="credentials.password" 
                :type="showPassword ? 'text' : 'password'" 
                class="form-control"
                placeholder="Ingresa tu contraseña" 
                required 
                autocomplete="current-password"
              />
              <button 
                type="button" 
                class="password-toggle" 
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary btn-block btn-lg" 
            :disabled="loading"
          >
            <span v-if="!loading">🚀 Iniciar Sesión</span>
            <span v-else class="loading-spinner">⏳ Ingresando...</span>
          </button>

          <div v-if="error" class="alert alert-error">
            <span class="alert-icon">⚠️</span>
            {{ error }}
          </div>
        </form>

        <div class="auth-footer">
          <p>¿No tienes cuenta? 
            <router-link to="/register" class="link-primary">Regístrate aquí</router-link>
          </p>
          <router-link to="/" class="link-secondary">← Volver al inicio</router-link>
        </div>
      </div>

      <div class="auth-info">
        <div class="info-card">
          <div class="info-icon">📊</div>
          <h3>Gestión Integral</h3>
          <p>Control completo de tus proyectos académicos y presupuesto</p>
        </div>
        <div class="info-card">
          <div class="info-icon">🔐</div>
          <h3>Seguro y Confiable</h3>
          <p>Tus datos protegidos con tecnología de última generación</p>
        </div>
        <div class="info-card">
          <div class="info-icon">⚡</div>
          <h3>Rápido y Eficiente</h3>
          <p>Acceso instantáneo desde cualquier dispositivo</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const credentials = ref({ codigo_institucional: '', password: '' })
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      try {
        await authStore.login(credentials.value)
        const role = authStore.userRole
        const routes = {
          'estudiante': '/student',
          'profesor': '/professor',
          'financiera': '/finance',
          'auditor': '/auditor',
          'superusuario': '/admin'
        }
        router.push(routes[role] || '/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al iniciar sesión'
      } finally {
        loading.value = false
      }
    }
    
    return { credentials, showPassword, loading, error, handleLogin }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.auth-page::before {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  top: -250px;
  right: -250px;
  animation: float 20s infinite ease-in-out;
}

.auth-page::after {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  bottom: -150px;
  left: -150px;
  animation: float 15s infinite ease-in-out reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(180deg); }
}

.auth-container {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.auth-card {
  background: white;
  border-radius: 20px;
  padding: 50px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideInLeft 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin: 0 auto 20px;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.auth-header h2 {
  font-size: 28px;
  margin-bottom: 8px;
  color: var(--gray-900);
}

.auth-header p {
  color: var(--gray-600);
  font-size: 14px;
}

.auth-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-weight: 600;
  color: var(--gray-700);
  font-size: 14px;
}

.label-icon {
  font-size: 18px;
}

.password-input-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.password-toggle:hover {
  opacity: 1;
}

.loading-spinner {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.alert {
  padding: 14px 16px;
  border-radius: 10px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.alert-error {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fca5a5;
}

.alert-icon {
  font-size: 20px;
}

.auth-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--gray-200);
}

.auth-footer p {
  margin-bottom: 12px;
  color: var(--gray-600);
  font-size: 14px;
}

.link-primary {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
}

.link-primary:hover {
  color: var(--primary-dark);
}

.link-secondary {
  color: var(--gray-500);
  font-size: 13px;
  text-decoration: none;
  transition: color 0.3s;
}

.link-secondary:hover {
  color: var(--gray-700);
}

.auth-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.info-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  color: white;
  transition: transform 0.3s, box-shadow 0.3s;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

.info-icon {
  font-size: 48px;
  margin-bottom: 16px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.info-card h3 {
  font-size: 18px;
  margin-bottom: 8px;
  font-weight: 700;
}

.info-card p {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.6;
}

@media (max-width: 968px) {
  .auth-container {
    grid-template-columns: 1fr;
  }
  
  .auth-info {
    display: none;
  }
  
  .auth-card {
    max-width: 480px;
    margin: 0 auto;
  }
}
</style>
