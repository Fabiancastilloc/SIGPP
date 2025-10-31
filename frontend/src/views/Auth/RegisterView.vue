<template>
  <div class="auth-page">
    <div class="auth-container-wide">
      <div class="auth-card auth-card-wide">
        <div class="auth-header">
          <div class="logo-circle">
            <span class="logo-emoji">📝</span>
            <div class="logo-ring"></div>
          </div>
          <h2>Crear Cuenta</h2>
          <p>Completa el formulario para registrarte en el SIGPP</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <!-- Selector de Rol -->
          <div class="form-section">
            <h3 class="section-title">
              <span class="section-icon">👥</span>
              Tipo de Usuario
            </h3>
            <div class="role-selector">
              <label 
                v-for="rol in roles" 
                :key="rol.value" 
                class="role-option"
                :class="{ 'active': formData.rol === rol.value }"
              >
                <input 
                  type="radio" 
                  v-model="formData.rol" 
                  :value="rol.value"
                  @change="onRoleChange"
                  required
                />
                <div class="role-card">
                  <div class="role-icon-wrapper">
                    <span class="role-icon">{{ rol.icon }}</span>
                  </div>
                  <span class="role-name">{{ rol.label }}</span>
                  <div class="check-mark">✓</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Información Personal -->
          <div class="form-section" v-show="formData.rol">
            <h3 class="section-title">
              <span class="section-icon">📋</span>
              Información Personal
            </h3>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🆔</span>
                  Código Institucional *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="formData.codigo_institucional" 
                    class="form-control"
                    placeholder="Ej: EST20251001" 
                    required 
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">📧</span>
                  Correo Institucional *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="formData.email" 
                    type="email" 
                    class="form-control"
                    placeholder="ejemplo@unicartagena.edu.co" 
                    required 
                  />
                </div>
                <small class="input-hint">Debe ser @unicartagena.edu.co</small>
              </div>
              
              <div class="form-group form-group-full">
                <label class="form-label">
                  <span class="label-icon">👤</span>
                  Nombre Completo *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="formData.nombre_completo" 
                    class="form-control"
                    placeholder="Nombre y apellidos completos" 
                    required 
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔒</span>
                  Contraseña *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="formData.password" 
                    type="password" 
                    class="form-control"
                    placeholder="Mínimo 8 caracteres" 
                    required 
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔐</span>
                  Confirmar Contraseña *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="confirmPassword" 
                    type="password" 
                    class="form-control"
                    placeholder="Repite la contraseña" 
                    required 
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Catálogos Dinámicos -->
          <div v-if="showCatalogs" class="form-section animate-in">
            <h3 class="section-title">
              <span class="section-icon">🏛️</span>
              Información Académica
            </h3>
            <div class="form-grid">
              <div v-if="showSedeField" class="form-group">
                <label class="form-label">
                  <span class="label-icon">🏢</span>
                  Sede *
                </label>
                <div class="input-wrapper">
                  <select v-model="formData.sede_id" class="form-control" required @change="loadFacultades">
                    <option value="">Seleccione una sede</option>
                    <option v-for="sede in sedes" :key="sede.id" :value="sede.id">
                      {{ sede.nombre }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div v-if="showFacultadField" class="form-group">
                <label class="form-label">
                  <span class="label-icon">🎓</span>
                  Facultad *
                </label>
                <div class="input-wrapper">
                  <select v-model="formData.facultad_id" class="form-control" required @change="loadCarreras">
                    <option value="">Seleccione una facultad</option>
                    <option v-for="facultad in facultades" :key="facultad.id" :value="facultad.id">
                      {{ facultad.nombre }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div v-if="showCarreraField" class="form-group">
                <label class="form-label">
                  <span class="label-icon">📚</span>
                  Carrera *
                </label>
                <div class="input-wrapper">
                  <select v-model="formData.carrera_id" class="form-control" required>
                    <option value="">Seleccione una carrera</option>
                    <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                      {{ carrera.nombre }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div v-if="showSemestreField" class="form-group">
                <label class="form-label">
                  <span class="label-icon">📖</span>
                  Semestre *
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model.number="formData.semestre" 
                    type="number" 
                    class="form-control" 
                    min="1" 
                    max="12"
                    placeholder="1-12" 
                    required 
                  />
                </div>
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            class="btn btn-primary btn-block btn-lg" 
            :disabled="loading"
          >
            <span v-if="!loading" class="btn-content">
              <span class="btn-icon">✨</span>
              <span>Crear Cuenta</span>
            </span>
            <span v-else class="btn-content">
              <span class="spinner"></span>
              <span>Registrando...</span>
            </span>
          </button>

          <transition name="alert-fade">
            <div v-if="error" class="alert alert-error">
              <span class="alert-icon">⚠️</span>
              <span>{{ error }}</span>
            </div>
          </transition>

          <transition name="alert-fade">
            <div v-if="success" class="alert alert-success">
              <span class="alert-icon">✅</span>
              <span>{{ success }}</span>
            </div>
          </transition>
        </form>

        <div class="auth-footer">
          <p>¿Ya tienes cuenta? 
            <router-link to="/login" class="link-primary">Inicia sesión aquí</router-link>
          </p>
          <router-link to="/" class="link-secondary">← Volver al inicio</router-link>
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
    const sedes = ref([])
    const facultades = ref([])
    const carreras = ref([])
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    
    const roles = [
      { value: 'estudiante', label: 'Estudiante', icon: '🎓' },
      { value: 'profesor', label: 'Profesor', icon: '👨‍🏫' },
      { value: 'financiera', label: 'Financiera', icon: '💼' }
    ]
    
    const showCatalogs = computed(() => formData.value.rol !== '')
    const showSedeField = computed(() => ['estudiante', 'profesor', 'financiera'].includes(formData.value.rol))
    const showFacultadField = computed(() => ['estudiante', 'profesor'].includes(formData.value.rol))
    const showCarreraField = computed(() => formData.value.rol === 'estudiante')
    const showSemestreField = computed(() => formData.value.rol === 'estudiante')
    
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
      } catch (err) {
        console.error('Error cargando facultades', err)
      }
    }
    
    const loadCarreras = async () => {
      if (!formData.value.facultad_id) return
      try {
        const response = await catalogsApi.getCarreras(formData.value.facultad_id)
        carreras.value = response.data
      } catch (err) {
        console.error('Error cargando carreras', err)
      }
    }
    
    const handleRegister = async () => {
      error.value = ''
      success.value = ''
      
      if (formData.value.password !== confirmPassword.value) {
        error.value = 'Las contraseñas no coinciden'
        return
      }
      
      if (formData.value.password.length < 8) {
        error.value = 'La contraseña debe tener al menos 8 caracteres'
        return
      }
      
      loading.value = true
      try {
        await authApi.register(formData.value)
        success.value = 'Registro exitoso. Redirigiendo al login...'
        setTimeout(() => router.push('/login'), 2000)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al registrar usuario'
      } finally {
        loading.value = false
      }
    }
    
    onMounted(async () => {
      try {
        const response = await catalogsApi.getSedes()
        sedes.value = response.data
      } catch (err) {
        console.error('Error cargando sedes', err)
      }
    })
    
    return {
      formData,
      confirmPassword,
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
      onRoleChange,
      loadFacultades,
      loadCarreras,
      handleRegister
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-container-wide {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}

.auth-card-wide {
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  padding: 40px 40px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.auth-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.logo-circle {
  width: 90px;
  height: 90px;
  margin: 0 auto 20px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.logo-emoji {
  position: relative;
  z-index: 2;
}

.logo-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  75%, 100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.auth-header h2 {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
}

.auth-header p {
  font-size: 16px;
  opacity: 0.95;
  position: relative;
  z-index: 1;
}

.register-form {
  padding: 40px;
}

.form-section {
  margin-bottom: 35px;
  padding: 28px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
  border-radius: 16px;
  border: 2px solid #e5e7ff;
  transition: all 0.3s ease;
}

.form-section:hover {
  border-color: #c7cbff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.12);
}

.animate-in {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  margin-bottom: 24px;
  color: #1e293b;
  font-weight: 700;
}

.section-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.role-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 20px;
}

.role-option {
  cursor: pointer;
}

.role-option input[type="radio"] {
  display: none;
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 28px 20px;
  background: white;
  border: 3px solid #e2e8f0;
  border-radius: 16px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.role-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transition: left 0.5s;
}

.role-option:hover .role-card::before {
  left: 100%;
}

.role-option:hover .role-card {
  border-color: #667eea;
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.25);
}

.role-option.active .role-card {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.35);
  transform: scale(1.05);
}

.role-icon-wrapper {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.role-option:hover .role-icon-wrapper {
  transform: rotate(10deg) scale(1.1);
}

.role-option.active .role-icon-wrapper {
  transform: rotate(360deg) scale(1.15);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.role-icon {
  font-size: 42px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.role-name {
  font-size: 16px;
  font-weight: 700;
  color: #475569;
  transition: color 0.3s;
}

.role-option.active .role-name {
  color: #667eea;
  transform: scale(1.05);
}

.check-mark {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.role-option.active .check-mark {
  opacity: 1;
  transform: scale(1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.form-group-full {
  grid-column: 1 / -1;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 10px;
}

.label-icon {
  font-size: 18px;
}

.input-wrapper {
  position: relative;
}

.form-control {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s;
  background: white;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.form-control::placeholder {
  color: #94a3b8;
}

.input-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #64748b;
  font-style: italic;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 32px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-block {
  width: 100%;
}

.btn-lg {
  padding: 18px 40px;
  font-size: 18px;
  margin-top: 20px;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-icon {
  font-size: 22px;
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.2) rotate(-10deg); }
  75% { transform: scale(1.2) rotate(10deg); }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  margin-top: 20px;
  font-size: 15px;
  font-weight: 600;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
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
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
  border: 2px solid #fca5a5;
}

.alert-success {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  border: 2px solid #6ee7b7;
}

.alert-icon {
  font-size: 24px;
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

.auth-footer {
  text-align: center;
  padding: 30px 40px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.auth-footer p {
  margin-bottom: 12px;
  color: #64748b;
  font-size: 15px;
}

.link-primary {
  color: #667eea;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
}

.link-primary::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #667eea;
  transition: width 0.3s;
}

.link-primary:hover::after {
  width: 100%;
}

.link-secondary {
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.link-secondary:hover {
  color: #667eea;
}

@media (max-width: 768px) {
  .auth-page {
    padding: 20px 10px;
  }

  .register-form {
    padding: 24px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .role-selector {
    grid-template-columns: 1fr;
  }

  .form-section {
    padding: 20px;
  }

  .auth-header {
    padding: 30px 20px 20px;
  }

  .auth-header h2 {
    font-size: 26px;
  }

  .logo-circle {
    width: 70px;
    height: 70px;
    font-size: 32px;
  }
}
</style>
