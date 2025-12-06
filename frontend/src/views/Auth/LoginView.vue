<!-- frontend/src/views/Login.vue -->
<template>
  <div class="login-page">
    <div class="login-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="particles">
        <div 
          v-for="i in 20" 
          :key="i" 
          class="particle"
          :style="{
            left: Math.random() * 100 + '%',
            animationDelay: Math.random() * 5 + 's',
            animationDuration: (3 + Math.random() * 4) + 's'
          }"
        ></div>
      </div>
    </div>

    <div class="login-container">
      <!-- Left Side - Branding -->
      <div class="login-branding">
        <div class="branding-content">
          <div class="brand-logo">
            <div class="logo-icon">🎓</div>
          </div>
          
          <h1 class="brand-title">
            <span class="gradient-text">SIGPP</span>
          </h1>
          
          <p class="brand-subtitle">
            Sistema Integral de Gestión de Propuestas y Proyectos
          </p>

          <div class="brand-features">
            <div class="feature-item">
              <div class="feature-icon">✓</div>
              <span>Gestión Completa de Proyectos</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">✓</div>
              <span>Control Financiero en Tiempo Real</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">✓</div>
              <span>Flujo de Aprobación Automatizado</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">✓</div>
              <span>Seguridad y Trazabilidad Total</span>
            </div>
          </div>

          <div class="brand-footer">
            <p>Universidad de Cartagena</p>
            <p class="footer-year">© 2025 - Todos los derechos reservados</p>
          </div>
        </div>
      </div>

      <!-- Right Side - Login Form -->
      <div class="login-form-section">
        <div class="form-wrapper">
          
          <!-- Header -->
          <div class="form-header">
            <div class="header-icon">🔐</div>
            <h2>Iniciar Sesión</h2>
            <p>Ingresa tus credenciales para acceder al sistema</p>
          </div>

          <!-- Alert Messages -->
          <div v-if="error" class="alert alert-error">
            <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <div v-if="success" class="alert alert-success">
            <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ success }}</span>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="handleLogin" class="login-form">
            
            <!-- Usuario Field (Código o Email) -->
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>Código Institucional o Email</span>
              </label>
              <div class="input-wrapper">
                <input 
                  v-model="formData.identifier"
                  type="text"
                  class="form-input"
                  placeholder="Ej: 20211234567 o usuario@unicartagena.edu.co"
                  required
                  autocomplete="username"
                  :disabled="loading"
                />
                <div class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              <div class="input-hint">
                💡 Puedes usar tu código institucional o correo electrónico
              </div>
            </div>

            <!-- Password Field -->
            <div class="form-group">
              <label class="form-label">
                <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span>Contraseña</span>
              </label>
              <div class="input-wrapper">
                <input 
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Ingresa tu contraseña"
                  required
                  autocomplete="current-password"
                  :disabled="loading"
                />
                <button 
                  type="button"
                  @click="showPassword = !showPassword"
                  class="input-icon icon-button"
                  tabindex="-1"
                >
                  <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="form-options">
              <label class="checkbox-label">
                <input 
                  v-model="formData.remember"
                  type="checkbox"
                  class="checkbox-input"
                  :disabled="loading"
                />
                <span class="checkbox-custom"></span>
                <span class="checkbox-text">Recordar sesión</span>
              </label>

              <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            <!-- Submit Button -->
            <button 
              type="submit" 
              class="btn-submit"
              :disabled="loading || !formData.identifier || !formData.password"
            >
              <svg v-if="loading" class="btn-spinner" viewBox="0 0 24 24">
                ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              <span>{{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
            </button>

            <!-- Divider -->
            <div class="divider">
              <span>o</span>
            </div>

            <!-- Register Link -->
            <div class="form-footer">
              <p>¿No tienes una cuenta?</p>
              <router-link to="/register" class="register-link">
                <span>Crear cuenta gratis</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </router-link>
            </div>
          </form>

          <!-- Back to Home -->
          <router-link to="/" class="back-home">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Volver al inicio</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'  // ⬅️ CORRECCIÓN: dos niveles arriba

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const formData = ref({
      identifier: '', // Puede ser código o email
      password: '',
      remember: false
    })
    
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    const showPassword = ref(false)
    
    const handleLogin = async () => {
      error.value = ''
      success.value = ''
      
      // Validaciones básicas
      if (!formData.value.identifier.trim()) {
        error.value = '⚠️ Debes ingresar tu código o email'
        return
      }
      
      if (!formData.value.password) {
        error.value = '⚠️ Debes ingresar tu contraseña'
        return
      }
      
      loading.value = true
      
      try {
        // Determinar si es email o código
        const isEmail = formData.value.identifier.includes('@')
        
        const loginData = {
          password: formData.value.password
        }
        
        // Agregar el campo correcto según el tipo de identificador
        if (isEmail) {
          loginData.email = formData.value.identifier.trim().toLowerCase()
        } else {
          loginData.codigo_institucional = formData.value.identifier.trim()
        }
        
        console.log('🔐 Intentando login con:', isEmail ? 'email' : 'código institucional')
        
        await authStore.login(loginData)
        
        success.value = '✅ Inicio de sesión exitoso. Redirigiendo...'
        
        // Pequeña pausa para mostrar mensaje
        setTimeout(() => {
          // Redireccionar según el rol
          const roleRoutes = {
            estudiante: '/student',
            profesor: '/professor',
            financiera: '/finance',
            auditor: '/auditor',
            super_usuario: '/admin'
          }
          
          const route = roleRoutes[authStore.user.rol] || '/student'
          router.push(route)
        }, 800)
        
      } catch (err) {
        console.error('❌ Error en login:', err)
        
        if (err.response?.status === 401) {
          error.value = '❌ Credenciales incorrectas. Verifica tu código/email y contraseña.'
        } else if (err.response?.status === 404) {
          error.value = '❌ Usuario no encontrado. Verifica tus credenciales.'
        } else if (err.response?.data?.detail) {
          error.value = `❌ ${err.response.data.detail}`
        } else {
          error.value = '❌ Error al iniciar sesión. Intenta nuevamente.'
        }
      } finally {
        loading.value = false
      }
    }
    
    const handleForgotPassword = () => {
      alert('Funcionalidad de recuperación de contraseña en desarrollo.\n\nPor favor contacta al administrador del sistema.')
    }
    
    return {
      formData,
      loading,
      error,
      success,
      showPassword,
      handleLogin,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
/* Base */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* Animated Background */
.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.25;
  animation: float-orb 20s infinite ease-in-out;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -250px;
  left: -250px;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -200px;
  right: -200px;
  animation-delay: -10s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 50%;
  right: 15%;
  animation-delay: -5s;
}

@keyframes float-orb {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(40px, -40px) scale(1.1);
  }
  66% {
    transform: translate(-30px, 30px) scale(0.9);
  }
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(212, 175, 55, 0.5);
  border-radius: 50%;
  opacity: 0;
  animation: particle-float infinite ease-in-out;
}

@keyframes particle-float {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) translateX(30px);
    opacity: 0;
  }
}

/* Login Container */
.login-container {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1200px;
  width: 100%;
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(212, 175, 55, 0.2);
}

/* Left Side - Branding */
.login-branding {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(212, 175, 55, 0.05));
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-right: 2px solid rgba(212, 175, 55, 0.2);
  position: relative;
  overflow: hidden;
}

.login-branding::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.branding-content {
  position: relative;
  z-index: 1;
}

.brand-logo {
  margin-bottom: 32px;
}

.logo-icon {
  font-size: 72px;
  filter: drop-shadow(0 4px 16px rgba(212, 175, 55, 0.4));
  animation: float-logo 3s infinite ease-in-out;
}

@keyframes float-logo {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.brand-title {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 16px;
  line-height: 1;
}

.gradient-text {
  background: linear-gradient(90deg, #d4af37, #f3e5ab, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: gradient-flow 3s linear infinite;
}

@keyframes gradient-flow {
  to {
    background-position: 200% center;
  }
}

.brand-subtitle {
  font-size: 1.1rem;
  color: #cbd5e1;
  line-height: 1.6;
  margin-bottom: 48px;
  font-weight: 600;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 48px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(212, 175, 55, 0.1);
  transition: all 0.3s;
}

.feature-item:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.3);
  transform: translateX(5px);
}

.feature-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #d4af37, #b8960f);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0a0f1e;
  font-weight: 900;
  font-size: 18px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.feature-item span {
  color: #f1f5f9;
  font-weight: 600;
  font-size: 15px;
}

.brand-footer {
  margin-top: auto;
  padding-top: 32px;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
}

.brand-footer p {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.footer-year {
  font-size: 12px;
  opacity: 0.7;
}

/* Right Side - Form */
.login-form-section {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: rgba(15, 23, 42, 0.8);
}

.form-wrapper {
  max-width: 450px;
  width: 100%;
  margin: 0 auto;
}

/* Form Header */
.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.header-icon {
  font-size: 56px;
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.4));
}

.form-header h2 {
  font-size: 2.25rem;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 12px;
}

.form-header p {
  font-size: 15px;
  color: #94a3b8;
  font-weight: 600;
}

/* Alerts */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 14px;
  font-weight: 700;
  animation: slide-in 0.3s ease-out;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-error {
  background: rgba(239, 68, 68, 0.15);
  border: 2px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.alert-success {
  background: rgba(16, 185, 129, 0.15);
  border: 2px solid rgba(16, 185, 129, 0.3);
  color: #6ee7b7;
}

.alert-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-icon {
  width: 18px;
  height: 18px;
  color: #d4af37;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 16px 50px 16px 20px;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus {
  outline: none;
  background: #1e293b;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.15);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  color: #64748b;
  pointer-events: none;
}

.icon-button {
  pointer-events: all;
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  transition: color 0.2s;
}

.icon-button:hover {
  color: #d4af37;
}

.input-hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #334155;
  border-radius: 6px;
  background: rgba(15, 23, 42, 0.8);
  transition: all 0.3s;
  position: relative;
}

.checkbox-input:checked + .checkbox-custom {
  background: linear-gradient(135deg, #d4af37, #b8960f);
  border-color: #d4af37;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #0a0f1e;
  font-weight: 900;
  font-size: 14px;
}

.checkbox-text {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

.forgot-password {
  font-size: 14px;
  color: #d4af37;
  text-decoration: none;
  font-weight: 700;
  transition: all 0.2s;
}

.forgot-password:hover {
  color: #f3e5ab;
  text-decoration: underline;
}

/* Submit Button */
.btn-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 18px 32px;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border: none;
  border-radius: 12px;
  color: #0a0f1e;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.4);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(212, 175, 55, 0.6);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-submit svg {
  width: 22px;
  height: 22px;
}

.btn-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Divider */
.divider {
  position: relative;
  text-align: center;
  margin: 32px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(212, 175, 55, 0.2);
}

.divider span {
  position: relative;
  display: inline-block;
  padding: 0 16px;
  background: rgba(15, 23, 42, 0.8);
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

/* Form Footer */
.form-footer {
  text-align: center;
}

.form-footer p {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.register-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  text-decoration: none;
  font-weight: 800;
  font-size: 15px;
  transition: all 0.2s;
}

.register-link:hover {
  gap: 12px;
  color: #f3e5ab;
}

.register-link svg {
  width: 18px;
  height: 18px;
}

/* Back to Home */
.back-home {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 32px;
  color: #64748b;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.2s;
}

.back-home:hover {
  color: #d4af37;
  gap: 12px;
}

.back-home svg {
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 968px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  
  .login-branding {
    display: none;
  }
  
  .login-form-section {
    padding: 40px 24px;
  }
  
  .form-header h2 {
    font-size: 1.75rem;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 12px;
  }
  
  .form-wrapper {
    max-width: 100%;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
