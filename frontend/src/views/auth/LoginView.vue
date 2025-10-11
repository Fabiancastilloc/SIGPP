<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-container">
            <div class="logo-circle">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
          </div>
          <h2>Bienvenido de nuevo</h2>
          <p>Ingresa tus credenciales para continuar</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="codigo">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Código Institucional
            </label>
            <input id="codigo" v-model="credentials.codigo_institucional" type="text" required
              placeholder="Ej: 0110111222" class="form-input" />
          </div>

          <div class="form-group">
            <label for="password">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Contraseña
            </label>
            <div class="password-input">
              <input id="password" v-model="credentials.password" :type="showPassword ? 'text' : 'password'" required
                placeholder="Ingresa tu contraseña" class="form-input" />
              <button type="button" @click="showPassword = !showPassword" class="toggle-password">
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="error-alert">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            <span v-if="!loading">Iniciar Sesión</span>
            <span v-else class="loading-spinner"></span>
          </button>
        </form>

        <div class="login-footer">
          <p>¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link></p>
          <router-link to="/" class="back-link">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Volver al inicio
          </router-link>
        </div>
      </div>

      <div class="info-panel">
        <h3>Sistema de Gestión de Proyectos</h3>
        <ul>
          <li>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Gestión integral de proyectos de grado
          </li>
          <li>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Control de presupuestos en tiempo real
          </li>
          <li>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Exportación de reportes PDF/Excel
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const credentials = ref({
  codigo_institucional: '',
  password: ''
})

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''

    await authStore.login(credentials.value)

    const userRole = authStore.user?.rol
    if (userRole === 'estudiante') {
      router.push('/dashboard')
    } else if (userRole === 'profesor') {
      router.push('/profesor/dashboard')
    } else if (userRole === 'financiera') {
      router.push('/financiera/dashboard')
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Credenciales incorrectas'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: var(--space-6);
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.login-card {
  padding: var(--space-12) var(--space-8);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-6);
}

.logo-circle {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo-circle svg {
  width: 32px;
  height: 32px;
}

.login-header h2 {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: var(--space-2);
  color: var(--gray-900);
}

.login-header p {
  color: var(--gray-600);
  font-size: 1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-group label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.form-group label svg {
  width: 18px;
  height: 18px;
  color: var(--gray-500);
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--gray-500);
  padding: var(--space-2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

.error-alert {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: var(--radius-lg);
  color: #991b1b;
  font-size: 0.875rem;
  font-weight: 500;
}

.error-alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.login-footer {
  margin-top: var(--space-8);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.login-footer p {
  color: var(--gray-600);
  font-size: 0.95rem;
}

.login-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-base);
}

.login-footer a:hover {
  color: var(--primary-dark);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--gray-600) !important;
  font-weight: 500 !important;
}

.back-link svg {
  width: 16px;
  height: 16px;
}

.info-panel {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: var(--space-12) var(--space-8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
}

.info-panel h3 {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: var(--space-8);
  color: white;
}

.info-panel ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.info-panel li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: 1.125rem;
}

.info-panel li svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

@media (max-width: 968px) {
  .login-container {
    grid-template-columns: 1fr;
  }

  .info-panel {
    display: none;
  }

  .login-card {
    padding: var(--space-8) var(--space-6);
  }
}
</style>
