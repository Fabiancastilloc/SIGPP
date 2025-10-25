<template>
  <div class="auth-page">
    <div class="auth-container-wide">
      <div class="auth-card auth-card-wide">
        <div class="auth-header">
          <div class="logo-circle">📝</div>
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
                  <span class="role-icon">{{ rol.icon }}</span>
                  <span class="role-name">{{ rol.label }}</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Información Personal -->
          <div class="form-section">
            <h3 class="section-title">
              <span class="section-icon">📋</span>
              Información Personal
            </h3>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Código Institucional *</label>
                <input 
                  v-model="formData.codigo_institucional" 
                  class="form-control"
                  placeholder="Ej: EST20251001" 
                  required 
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">Correo Institucional *</label>
                <input 
                  v-model="formData.email" 
                  type="email" 
                  class="form-control"
                  placeholder="ejemplo@unicartagena.edu.co" 
                  required 
                />
                <small>Debe ser @unicartagena.edu.co</small>
              </div>
              
              <div class="form-group form-group-full">
                <label class="form-label">Nombre Completo *</label>
                <input 
                  v-model="formData.nombre_completo" 
                  class="form-control"
                  placeholder="Nombre y apellidos completos" 
                  required 
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">Contraseña *</label>
                <input 
                  v-model="formData.password" 
                  type="password" 
                  class="form-control"
                  placeholder="Mínimo 8 caracteres" 
                  required 
                />
              </div>

              <div class="form-group">
                <label class="form-label">Confirmar Contraseña *</label>
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

          <!-- Catálogos Dinámicos -->
          <div v-if="showCatalogs" class="form-section">
            <h3 class="section-title">
              <span class="section-icon">🏛️</span>
              Información Académica
            </h3>
            <div class="form-grid">
              <div v-if="showSedeField" class="form-group">
                <label class="form-label">Sede *</label>
                <select v-model="formData.sede_id" class="form-control" required @change="loadFacultades">
                  <option value="">Seleccione una sede</option>
                  <option v-for="sede in sedes" :key="sede.id" :value="sede.id">
                    {{ sede.nombre }}
                  </option>
                </select>
              </div>
              
              <div v-if="showFacultadField" class="form-group">
                <label class="form-label">Facultad *</label>
                <select v-model="formData.facultad_id" class="form-control" required @change="loadCarreras">
                  <option value="">Seleccione una facultad</option>
                  <option v-for="facultad in facultades" :key="facultad.id" :value="facultad.id">
                    {{ facultad.nombre }}
                  </option>
                </select>
              </div>
              
              <div v-if="showCarreraField" class="form-group">
                <label class="form-label">Carrera *</label>
                <select v-model="formData.carrera_id" class="form-control" required>
                  <option value="">Seleccione una carrera</option>
                  <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                    {{ carrera.nombre }}
                  </option>
                </select>
              </div>
              
              <div v-if="showSemestreField" class="form-group">
                <label class="form-label">Semestre *</label>
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

          <button 
            type="submit" 
            class="btn btn-primary btn-block btn-lg" 
            :disabled="loading"
          >
            <span v-if="!loading">✨ Crear Cuenta</span>
            <span v-else>⏳ Registrando...</span>
          </button>

          <div v-if="error" class="alert alert-error">
            <span class="alert-icon">⚠️</span>
            {{ error }}
          </div>

          <div v-if="success" class="alert alert-success">
            <span class="alert-icon">✅</span>
            {{ success }}
          </div>
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
.auth-container-wide {
  max-width: 900px;
  margin: 0 auto;
}

.auth-card-wide {
  max-width: 100%;
}

.register-form {
  margin-bottom: 30px;
}

.form-section {
  margin-bottom: 40px;
  padding: 24px;
  background: var(--gray-50);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  margin-bottom: 20px;
  color: var(--gray-900);
  font-weight: 700;
}

.section-icon {
  font-size: 24px;
}

.role-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
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
  gap: 12px;
  padding: 24px 16px;
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: 12px;
  transition: all 0.3s;
  text-align: center;
}

.role-option:hover .role-card {
  border-color: var(--primary-color);
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
}

.role-option.active .role-card {
  border-color: var(--primary-color);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.role-icon {
  font-size: 48px;
}

.role-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
}

.role-option.active .role-name {
  color: var(--primary-color);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group-full {
  grid-column: 1 / -1;
}

.alert-success {
  background: #d1fae5;
  color: #059669;
  border: 1px solid #34d399;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .role-selector {
    grid-template-columns: 1fr;
  }
}
</style>
