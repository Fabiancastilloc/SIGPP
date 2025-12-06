<!-- frontend/src/views/Auth/RegisterView.vue -->
<template>
  <div class="register-page">
    <div class="register-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="particles">
        <div 
          v-for="i in 15" 
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

    <div class="register-container">
      <div class="register-card">
        
        <!-- Header -->
        <div class="register-header">
          <router-link to="/login" class="back-button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Volver</span>
          </router-link>

          <div class="header-content">
            <div class="header-icon">✨</div>
            <h1>Crear Cuenta</h1>
            <p>Completa el formulario para registrarte en SIGPP</p>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegister" class="register-form">
          
          <!-- Selector de Rol -->
          <div class="form-section">
            <h3 class="section-title">
              <span class="section-icon">👥</span>
              <span>Tipo de Usuario</span>
            </h3>
            
            <div class="role-selector">
              <label 
                v-for="rol in roles" 
                :key="rol.value" 
                class="role-card"
                :class="{ active: formData.rol === rol.value }"
              >
                <input 
                  type="radio" 
                  v-model="formData.rol" 
                  :value="rol.value"
                  @change="onRoleChange"
                  :disabled="loading"
                />
                <div class="role-icon-wrapper">
                  <div class="role-icon">{{ rol.icon }}</div>
                  <div class="role-glow"></div>
                </div>
                <div class="role-info">
                  <span class="role-name">{{ rol.label }}</span>
                  <span class="role-desc">{{ rol.description }}</span>
                </div>
                <div class="check-mark">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </label>
            </div>
          </div>

          <!-- Información Personal -->
          <div v-if="formData.rol" class="form-section animate-in">
            <h3 class="section-title">
              <span class="section-icon">📋</span>
              <span>Información Personal</span>
            </h3>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                  </svg>
                  <span>Código Institucional</span>
                  <span class="label-required">*</span>
                </label>
                <input 
                  v-model="formData.codigo_institucional" 
                  type="text"
                  class="form-input"
                  placeholder="Ej: 20251001"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>Correo Institucional</span>
                  <span class="label-required">*</span>
                </label>
                <input 
                  v-model="formData.email" 
                  type="email"
                  class="form-input"
                  placeholder="usuario@unicartagena.edu.co"
                  required
                  :disabled="loading"
                />
                <span class="input-hint">Debe ser @unicartagena.edu.co</span>
              </div>

              <div class="form-group form-group-full">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>Nombre Completo</span>
                  <span class="label-required">*</span>
                </label>
                <input 
                  v-model="formData.nombre_completo" 
                  type="text"
                  class="form-input"
                  placeholder="Nombre y apellidos completos"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  <span>Contraseña</span>
                  <span class="label-required">*</span>
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="formData.password" 
                    :type="showPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="Mínimo 8 caracteres"
                    required
                    :disabled="loading"
                  />
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="password-toggle"
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
                <span class="input-hint">Incluye mayúsculas, minúsculas y números</span>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span>Confirmar Contraseña</span>
                  <span class="label-required">*</span>
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="confirmPassword" 
                    :type="showConfirmPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="Repite la contraseña"
                    required
                    :disabled="loading"
                  />
                  <button 
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="password-toggle"
                    tabindex="-1"
                  >
                    <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Información Académica (solo para roles que la necesiten) -->
          <div v-if="showCatalogs" class="form-section animate-in">
            <h3 class="section-title">
              <span class="section-icon">🏛️</span>
              <span>Información Académica</span>
            </h3>
            
            <div class="form-grid">
              <div v-if="showSedeField" class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span>Sede</span>
                  <span class="label-required">*</span>
                </label>
                <select 
                  v-model="formData.sede_id" 
                  class="form-select"
                  required
                  @change="loadFacultades"
                  :disabled="loading"
                >
                  <option value="">Seleccione una sede</option>
                  <option v-for="sede in sedes" :key="sede.id" :value="sede.id">
                    {{ sede.nombre }}
                  </option>
                </select>
              </div>

              <div v-if="showFacultadField" class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
                  </svg>
                  <span>Facultad</span>
                  <span class="label-required">*</span>
                </label>
                <select 
                  v-model="formData.facultad_id" 
                  class="form-select"
                  required
                  @change="loadCarreras"
                  :disabled="loading || !formData.sede_id"
                >
                  <option value="">Seleccione una facultad</option>
                  <option v-for="facultad in facultades" :key="facultad.id" :value="facultad.id">
                    {{ facultad.nombre }}
                  </option>
                </select>
              </div>

              <div v-if="showCarreraField" class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <span>Carrera</span>
                  <span class="label-required">*</span>
                </label>
                <select 
                  v-model="formData.carrera_id" 
                  class="form-select"
                  required
                  :disabled="loading || !formData.facultad_id"
                >
                  <option value="">Seleccione una carrera</option>
                  <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                    {{ carrera.nombre }}
                  </option>
                </select>
              </div>

              <div v-if="showSemestreField" class="form-group">
                <label class="form-label">
                  <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                  <span>Semestre</span>
                  <span class="label-required">*</span>
                </label>
                <input 
                  v-model.number="formData.semestre" 
                  type="number"
                  class="form-input"
                  min="1"
                  max="12"
                  placeholder="1-12"
                  required
                  :disabled="loading"
                />
              </div>
            </div>
          </div>

          <!-- Alerts -->
          <transition name="alert-fade">
            <div v-if="error" class="alert alert-error">
              <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ error }}</span>
            </div>
          </transition>

          <transition name="alert-fade">
            <div v-if="success" class="alert alert-success">
              <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ success }}</span>
            </div>
          </transition>

          <!-- Submit Button -->
          <button 
            type="submit" 
            class="btn-submit"
            :disabled="loading || !canSubmit"
          >
            <svg v-if="loading" class="btn-spinner" viewBox="0 0 24 24">
              ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            <span>{{ loading ? 'Registrando...' : 'Crear Cuenta' }}</span>
          </button>
        </form>

        <!-- Footer -->
        <div class="register-footer">
          <p>¿Ya tienes una cuenta?</p>
          <router-link to="/login" class="login-link">
            <span>Iniciar sesión</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authApi from '../../api/auth'
import catalogsApi from '../../api/catalogs'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    
    const formData = ref({
      codigo_institucional: '',
      email: '',
      nombre_completo: '',
      password: '',
      rol: '',
      sede_id: null,
      facultad_id: null,
      carrera_id: null,
      semestre: null
    })
    
    const confirmPassword = ref('')
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const sedes = ref([])
    const facultades = ref([])
    const carreras = ref([])
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    
    const roles = [
      { 
        value: 'estudiante', 
        label: 'Estudiante', 
        icon: '🎓',
        description: 'Crea y gestiona proyectos académicos'
      },
      { 
        value: 'profesor', 
        label: 'Profesor', 
        icon: '👨‍🏫',
        description: 'Asesora y aprueba propuestas'
      },
      { 
        value: 'financiera', 
        label: 'Financiera', 
        icon: '💼',
        description: 'Gestiona presupuestos y gastos'
      },
      { 
        value: 'auditor', 
        label: 'Auditor', 
        icon: '🔍',
        description: 'Supervisa y audita proyectos'
      }
    ]
    
    const showCatalogs = computed(() => formData.value.rol !== '')
    const showSedeField = computed(() => ['estudiante', 'profesor', 'financiera', 'auditor'].includes(formData.value.rol))
    const showFacultadField = computed(() => ['estudiante', 'profesor'].includes(formData.value.rol))
    const showCarreraField = computed(() => formData.value.rol === 'estudiante')
    const showSemestreField = computed(() => formData.value.rol === 'estudiante')
    
    const canSubmit = computed(() => {
      if (!formData.value.rol || !formData.value.codigo_institucional || 
          !formData.value.email || !formData.value.nombre_completo || 
          !formData.value.password || !confirmPassword.value) {
        return false
      }
      
      if (showSedeField.value && !formData.value.sede_id) return false
      if (showFacultadField.value && !formData.value.facultad_id) return false
      if (showCarreraField.value && !formData.value.carrera_id) return false
      if (showSemestreField.value && !formData.value.semestre) return false
      
      return true
    })
    
    const onRoleChange = () => {
      formData.value.sede_id = null
      formData.value.facultad_id = null
      formData.value.carrera_id = null
      formData.value.semestre = null
      facultades.value = []
      carreras.value = []
    }
    
    const loadFacultades = async () => {
      if (!formData.value.sede_id) return
      try {
        const response = await catalogsApi.getFacultades(formData.value.sede_id)
        facultades.value = response.data
        formData.value.facultad_id = null
        formData.value.carrera_id = null
        carreras.value = []
      } catch (err) {
        console.error('Error cargando facultades:', err)
      }
    }
    
    const loadCarreras = async () => {
      if (!formData.value.facultad_id) return
      try {
        const response = await catalogsApi.getCarreras(formData.value.facultad_id)
        carreras.value = response.data
        formData.value.carrera_id = null
      } catch (err) {
        console.error('Error cargando carreras:', err)
      }
    }
    
    const handleRegister = async () => {
      error.value = ''
      success.value = ''
      
      // Validaciones
      if (formData.value.password !== confirmPassword.value) {
        error.value = '❌ Las contraseñas no coinciden'
        return
      }
      
      if (formData.value.password.length < 8) {
        error.value = '❌ La contraseña debe tener al menos 8 caracteres'
        return
      }
      
      if (!formData.value.email.endsWith('@unicartagena.edu.co')) {
        error.value = '❌ El correo debe ser del dominio @unicartagena.edu.co'
        return
      }
      
      loading.value = true
      
      try {
        await authApi.register(formData.value)
        success.value = '✅ Registro exitoso. Redirigiendo al login...'
        
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } catch (err) {
        console.error('Error en registro:', err)
        if (err.response?.data?.detail) {
          error.value = `❌ ${err.response.data.detail}`
        } else {
          error.value = '❌ Error al registrar usuario. Intenta nuevamente.'
        }
      } finally {
        loading.value = false
      }
    }
    
    onMounted(async () => {
      try {
        const response = await catalogsApi.getSedes()
        sedes.value = response.data
      } catch (err) {
        console.error('Error cargando sedes:', err)
      }
    })
    
    return {
      formData,
      confirmPassword,
      showPassword,
      showConfirmPassword,
      roles,
      sedes,
      facultades,
      carreras,
      loading,
      error,
      success,
      showCatalogs,
      showSedeField,
      showFacultadField,
      showCarreraField,
      showSemestreField,
      canSubmit,
      onRoleChange,
      loadFacultades,
      loadCarreras,
      handleRegister
    }
  }
}
</script>

<style scoped>
/* Base */
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
}

/* Animated Background */
.register-background {
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
  opacity: 0.2;
  animation: float-orb 20s infinite ease-in-out;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -200px;
  left: -200px;
}

.orb-2 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -175px;
  right: -175px;
  animation-delay: -10s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 50%;
  right: 20%;
  animation-delay: -5s;
}

@keyframes float-orb {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
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
  background: rgba(212, 175, 55, 0.4);
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
    transform: translateY(-100vh) translateX(20px);
    opacity: 0;
  }
}

/* Container */
.register-container {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  width: 100%;
}

.register-card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(212, 175, 55, 0.2);
}

/* Header */
.register-header {
  padding: 40px 50px 30px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(212, 175, 55, 0.05));
  border-bottom: 2px solid rgba(212, 175, 55, 0.2);
  position: relative;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.3s;
  margin-bottom: 24px;
}

.back-button:hover {
  background: rgba(212, 175, 55, 0.15);
  border-color: rgba(212, 175, 55, 0.3);
  color: #d4af37;
  transform: translateX(-4px);
}

.back-button svg {
  width: 18px;
  height: 18px;
}

.header-content {
  text-align: center;
}

.header-icon {
  font-size: 64px;
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.4));
  animation: float-icon 3s ease-in-out infinite;
}

@keyframes float-icon {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.register-header h1 {
  font-size: 2.5rem;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 12px;
}

.register-header p {
  font-size: 15px;
  color: #94a3b8;
  font-weight: 600;
}

/* Form */
.register-form {
  padding: 50px;
}

.form-section {
  margin-bottom: 40px;
  padding: 32px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 16px;
  border: 1px solid rgba(212, 175, 55, 0.1);
  transition: all 0.3s;
}

.form-section:hover {
  border-color: rgba(212, 175, 55, 0.3);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.1);
}

@keyframes animate-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: animate-in 0.5s ease-out;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.4rem;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(212, 175, 55, 0.2);
}

.section-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 6px rgba(212, 175, 55, 0.3));
}

/* Role Selector */
.role-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.role-card {
  position: relative;
  padding: 28px 20px;
  background: rgba(30, 41, 59, 0.8);
  border: 2px solid #334155;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.role-card:hover {
  border-color: #d4af37;
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(212, 175, 55, 0.2);
  background: rgba(212, 175, 55, 0.08);
}

.role-card.active {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.15);
  box-shadow: 0 16px 40px rgba(212, 175, 55, 0.3);
  transform: scale(1.02);
}

.role-card input[type="radio"] {
  display: none;
}

.role-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-icon {
  font-size: 48px;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: all 0.3s;
}

.role-card:hover .role-icon {
  transform: scale(1.1) rotate(5deg);
}

.role-card.active .role-icon {
  transform: scale(1.15) rotate(360deg);
}

.role-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3), transparent);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s;
}

.role-card.active .role-glow {
  opacity: 1;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.8;
  }
}

.role-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.role-name {
  font-size: 18px;
  font-weight: 800;
  color: #f1f5f9;
  transition: color 0.3s;
}

.role-card.active .role-name {
  color: #d4af37;
}

.role-desc {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  line-height: 1.4;
}

.check-mark {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #d4af37, #b8960f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

.role-card.active .check-mark {
  opacity: 1;
  transform: scale(1);
}

.check-mark svg {
  width: 18px;
  height: 18px;
  color: #0a0f1e;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.form-group-full {
  grid-column: 1 / -1;
}

/* Form Group */
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

.label-required {
  color: #ef4444;
  font-weight: 900;
}

.form-input,
.form-select {
  width: 100%;
  padding: 14px 18px;
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

.form-input:focus,
.form-select:focus {
  outline: none;
  background: #1e293b;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.15);
}

.form-input:disabled,
.form-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.password-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #d4af37;
}

.password-toggle svg {
  width: 100%;
  height: 100%;
}

.input-hint {
  font-size: 12px;
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

.alert-fade-enter-active,
.alert-fade-leave-active {
  transition: all 0.3s ease;
}

.alert-fade-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.alert-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Submit Button */
.btn-submit {
  width: 100%;
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
  margin-top: 32px;
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

/* Footer */
.register-footer {
  padding: 32px 50px;
  background: rgba(15, 23, 42, 0.5);
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  text-align: center;
}

.register-footer p {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.login-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  text-decoration: none;
  font-weight: 800;
  font-size: 15px;
  transition: all 0.2s;
}

.login-link:hover {
  gap: 12px;
  color: #f3e5ab;
}

.login-link svg {
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 968px) {
  .register-page {
    padding: 20px 12px;
  }
  
  .register-form {
    padding: 32px 24px;
  }
  
  .register-header {
    padding: 32px 24px 24px;
  }
  
  .form-section {
    padding: 24px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .role-selector {
    grid-template-columns: 1fr;
  }
  
  .register-header h1 {
    font-size: 2rem;
  }
  
  .register-footer {
    padding: 24px;
  }
}
</style>
