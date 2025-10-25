<template>
  <div class="create-project-page">
    <div class="container">
      <div class="page-header">
        <router-link to="/student" class="btn-back">
          ← Volver al Dashboard
        </router-link>
        <h1>✨ Crear Nuevo Proyecto</h1>
        <p>Completa la información de tu propuesta de investigación</p>
      </div>

      <form @submit.prevent="handleSubmit" class="project-form">
        <!-- Información Básica -->
        <div class="form-card">
          <div class="card-header">
            <div class="header-icon">📝</div>
            <h3>Información Básica</h3>
          </div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-required">*</span>
                Nombre del Proyecto
              </label>
              <input 
                v-model="formData.nombre" 
                class="form-control" 
                placeholder="Ej: Sistema de Gestión de Inventario para Pymes"
                required
                maxlength="200"
              />
              <small class="form-hint">
                <span class="hint-icon">💡</span>
                Usa un nombre descriptivo y único ({{ formData.nombre.length }}/200 caracteres)
              </small>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-required">*</span>
                Descripción Detallada
              </label>
              <textarea 
                v-model="formData.descripcion" 
                class="form-control" 
                rows="6"
                placeholder="Describe detalladamente en qué consiste tu proyecto, el problema que resuelve y su alcance..."
                required
                minlength="100"
                maxlength="2000"
              ></textarea>
              <small class="form-hint" :class="{ 'hint-error': formData.descripcion.length < 100 && formData.descripcion.length > 0 }">
                <span class="hint-icon">{{ formData.descripcion.length >= 100 ? '✅' : '⚠️' }}</span>
                {{ formData.descripcion.length }}/2000 caracteres (mínimo 100 requerido)
              </small>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-required">*</span>
                Objetivos del Proyecto
              </label>
              <textarea 
                v-model="formData.objetivos" 
                class="form-control" 
                rows="6"
                placeholder="Define los objetivos generales y específicos de tu proyecto..."
                required
                minlength="50"
                maxlength="1500"
              ></textarea>
              <small class="form-hint">
                <span class="hint-icon">🎯</span>
                Especifica qué esperas lograr ({{ formData.objetivos.length }}/1500 caracteres)
              </small>
            </div>
          </div>
        </div>

        <!-- Información Académica -->
        <div class="form-card">
          <div class="card-header">
            <div class="header-icon">👨‍🏫</div>
            <h3>Información Académica</h3>
          </div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">
                <span class="label-required">*</span>
                Profesor Asesor
              </label>
              
              <div v-if="loadingProfesores" class="loading-select">
                <div class="spinner-small"></div>
                <span>Cargando profesores...</span>
              </div>
              
              <select 
                v-else
                v-model="formData.profesor_id" 
                class="form-control" 
                required
                @change="onProfesorChange"
              >
                <option value="">-- Seleccione un profesor asesor --</option>
                <option 
                  v-for="profesor in profesores" 
                  :key="profesor.id" 
                  :value="profesor.id"
                >
                  {{ profesor.nombre_completo }} - {{ profesor.email }}
                </option>
              </select>
              
              <small class="form-hint">
                <span class="hint-icon">👨‍🏫</span>
                Profesor que guiará y asesorará tu proyecto
              </small>

              <!-- Info del profesor seleccionado -->
              <div v-if="selectedProfesor" class="profesor-info">
                <div class="profesor-avatar">
                  {{ getInitials(selectedProfesor.nombre_completo) }}
                </div>
                <div class="profesor-details">
                  <strong>{{ selectedProfesor.nombre_completo }}</strong>
                  <span>{{ selectedProfesor.email }}</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-required">*</span>
                Presupuesto Estimado
              </label>
              <div class="input-group">
                <span class="input-prefix">$</span>
                <input 
                  v-model.number="formData.presupuesto_estimado" 
                  type="number" 
                  class="form-control" 
                  placeholder="5000000"
                  min="100000"
                  max="100000000"
                  step="100000"
                  required
                  @input="formatPresupuesto"
                />
                <span class="input-suffix">COP</span>
              </div>
              <small class="form-hint">
                <span class="hint-icon">💵</span>
                <span v-if="formData.presupuesto_estimado">
                  Presupuesto: {{ formatMoney(formData.presupuesto_estimado) }} COP
                </span>
                <span v-else>
                  Estimación en pesos colombianos (entre $100,000 y $100,000,000)
                </span>
              </small>
            </div>
          </div>
        </div>

        <!-- Resumen -->
        <div class="form-card summary-card">
          <div class="card-header">
            <div class="header-icon">📋</div>
            <h3>Resumen de la Propuesta</h3>
          </div>
          <div class="card-body">
            <div class="summary-grid">
              <div class="summary-item">
                <span class="summary-label">Nombre:</span>
                <span class="summary-value">{{ formData.nombre || 'Sin especificar' }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Profesor:</span>
                <span class="summary-value">{{ selectedProfesor?.nombre_completo || 'No seleccionado' }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Presupuesto:</span>
                <span class="summary-value">{{ formData.presupuesto_estimado ? '$' + formatMoney(formData.presupuesto_estimado) : 'No especificado' }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Estado inicial:</span>
                <span class="summary-value status-draft">📝 Borrador</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Alertas de validación -->
        <div v-if="validationErrors.length > 0" class="alert alert-warning">
          <div class="alert-header">
            <span class="alert-icon">⚠️</span>
            <strong>Completa los siguientes campos:</strong>
          </div>
          <ul class="alert-list">
            <li v-for="(error, index) in validationErrors" :key="index">{{ error }}</li>
          </ul>
        </div>

        <!-- Error del servidor -->
        <div v-if="error" class="alert alert-error">
          <span class="alert-icon">❌</span>
          {{ error }}
        </div>

        <!-- Botones de acción -->
        <div class="form-actions">
          <button type="button" @click="goBack" class="btn btn-secondary btn-lg" :disabled="loading">
            <span class="btn-icon">↩️</span>
            Cancelar
          </button>
          <button 
            type="submit" 
            class="btn btn-primary btn-lg" 
            :disabled="loading || !isFormValid"
          >
            <span v-if="!loading" class="btn-icon">🚀</span>
            <span v-if="!loading">Crear Proyecto</span>
            <span v-else class="loading-spinner">⏳ Creando...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'
import projectsApi from '../../api/projects'
import catalogsApi from '../../api/catalogs'

export default {
  name: 'CreateProject',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const formData = ref({
      nombre: '',
      descripcion: '',
      objetivos: '',
      profesor_id: '',
      presupuesto_estimado: null
    })
    
    const profesores = ref([])
    const loadingProfesores = ref(true)
    const loading = ref(false)
    const error = ref('')
    
    // Profesor seleccionado
    const selectedProfesor = computed(() => {
      if (!formData.value.profesor_id) return null
      return profesores.value.find(p => p.id === formData.value.profesor_id)
    })
    
    // Validaciones
    const validationErrors = computed(() => {
      const errors = []
      
      if (!formData.value.nombre.trim()) {
        errors.push('El nombre del proyecto es obligatorio')
      }
      
      if (formData.value.descripcion.length < 100) {
        errors.push('La descripción debe tener al menos 100 caracteres')
      }
      
      if (formData.value.objetivos.length < 50) {
        errors.push('Los objetivos deben tener al menos 50 caracteres')
      }
      
      if (!formData.value.profesor_id) {
        errors.push('Debes seleccionar un profesor asesor')
      }
      
      if (!formData.value.presupuesto_estimado || formData.value.presupuesto_estimado < 100000) {
        errors.push('El presupuesto debe ser al menos $100,000 COP')
      }
      
      return errors
    })
    
    const isFormValid = computed(() => {
      return validationErrors.value.length === 0
    })
    
    // Cargar profesores desde la BD
    const loadProfesores = async () => {
      loadingProfesores.value = true
      try {
        console.log('📡 Cargando profesores desde la BD...')
        const response = await catalogsApi.getProfesores()
        profesores.value = response.data
        console.log('✅ Profesores cargados:', profesores.value.length)
        
        // Validación: Verificar que solo sean profesores
        if (profesores.value.length === 0) {
          error.value = 'No hay profesores disponibles. Contacta al administrador.'
        }
      } catch (err) {
        console.error('❌ Error cargando profesores:', err)
        error.value = 'Error al cargar la lista de profesores. Por favor recarga la página.'
      } finally {
        loadingProfesores.value = false
      }
    }
    
    const onProfesorChange = () => {
      console.log('👨‍🏫 Profesor seleccionado:', selectedProfesor.value)
    }
    
    const formatPresupuesto = () => {
      // Validar que sea un número positivo
      if (formData.value.presupuesto_estimado < 0) {
        formData.value.presupuesto_estimado = 0
      }
    }
    
    const handleSubmit = async () => {
      error.value = ''
      
      // Validación final
      if (!isFormValid.value) {
        error.value = 'Por favor completa todos los campos correctamente'
        return
      }
      
      loading.value = true
      
      try {
        console.log('📤 Enviando proyecto:', formData.value)
        console.log('👤 Usuario actual:', authStore.user)
        
        const response = await projectsApi.createProject(formData.value)
        
        console.log('✅ Proyecto creado exitosamente:', response.data)
        
        // Mostrar mensaje de éxito
        alert(`✅ Proyecto creado exitosamente!\n\nCódigo: ${response.data.id}\nEstado: Borrador\n\nPuedes encontrarlo en tu dashboard.`)
        
        // Redirigir al dashboard
        router.push('/student')
      } catch (err) {
        console.error('❌ Error creando proyecto:', err)
        
        // Mostrar error específico del backend
        if (err.response?.data?.detail) {
          error.value = err.response.data.detail
        } else if (err.response?.status === 400) {
          error.value = 'Datos inválidos. Verifica todos los campos.'
        } else if (err.response?.status === 401) {
          error.value = 'Tu sesión ha expirado. Por favor inicia sesión nuevamente.'
          setTimeout(() => router.push('/login'), 2000)
        } else {
          error.value = 'Error al crear el proyecto. Intenta nuevamente.'
        }
      } finally {
        loading.value = false
      }
    }
    
    const goBack = () => {
      if (confirm('¿Estás seguro de cancelar? Se perderán los datos ingresados.')) {
        router.push('/student')
      }
    }
    
    const getInitials = (name) => {
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    const formatMoney = (value) => {
      return new Intl.NumberFormat('es-CO').format(value)
    }
    
    onMounted(() => {
      loadProfesores()
    })
    
    return {
      formData,
      profesores,
      loadingProfesores,
      loading,
      error,
      selectedProfesor,
      validationErrors,
      isFormValid,
      onProfesorChange,
      formatPresupuesto,
      handleSubmit,
      goBack,
      getInitials,
      formatMoney
    }
  }
}
</script>

<style scoped>
.create-project-page {
  padding: 30px 0;
  min-height: calc(100vh - 70px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.btn-back {
  position: absolute;
  left: 0;
  top: 0;
  padding: 12px 24px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid var(--gray-200);
}

.btn-back:hover {
  background: var(--gray-100);
  transform: translateX(-4px);
  border-color: var(--primary-color);
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-header p {
  font-size: 16px;
  color: var(--gray-600);
}

.project-form {
  max-width: 900px;
  margin: 0 auto;
}

.form-card {
  background: white;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 2px solid var(--gray-200);
  transition: border-color 0.3s;
}

.form-card:hover {
  border-color: var(--primary-color);
}

.card-header {
  padding: 24px 32px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card-header h3 {
  margin: 0;
  font-size: 20px;
  color: var(--gray-900);
  font-weight: 700;
}

.card-body {
  padding: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--gray-700);
  font-size: 14px;
}

.label-required {
  color: var(--danger-color);
  margin-right: 4px;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control::placeholder {
  color: var(--gray-400);
}

.form-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: var(--gray-600);
  display: flex;
  align-items: center;
  gap: 4px;
}

.hint-error {
  color: var(--danger-color);
}

.hint-icon {
  font-size: 14px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 16px;
  font-weight: 700;
  color: var(--gray-600);
  font-size: 16px;
  z-index: 1;
}

.input-group .form-control {
  padding-left: 40px;
  padding-right: 60px;
}

.input-suffix {
  position: absolute;
  right: 16px;
  font-weight: 600;
  color: var(--gray-500);
  font-size: 12px;
  text-transform: uppercase;
}

.loading-select {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--gray-50);
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  color: var(--gray-600);
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-200);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.profesor-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  border-radius: 12px;
  margin-top: 12px;
  border: 2px solid #93c5fd;
}

.profesor-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 18px;
  flex-shrink: 0;
}

.profesor-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profesor-details strong {
  font-size: 15px;
  color: var(--gray-900);
}

.profesor-details span {
  font-size: 13px;
  color: var(--gray-600);
}

.summary-card {
  border: 2px solid var(--primary-color);
  background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid var(--gray-200);
}

.summary-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.summary-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-900);
}

.status-draft {
  color: #f59e0b;
}

.alert {
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.alert-warning {
  background: #fef3c7;
  border: 2px solid #f59e0b;
  color: #92400e;
}

.alert-error {
  background: #fee2e2;
  border: 2px solid #ef4444;
  color: #991b1b;
  display: flex;
  align-items: center;
  gap: 8px;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
}

.alert-icon {
  font-size: 20px;
}

.alert-list {
  margin: 8px 0 0 28px;
  padding: 0;
}

.alert-list li {
  margin-bottom: 4px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.form-actions .btn {
  min-width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  font-size: 18px;
}

.loading-spinner {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .btn-back {
    position: static;
    display: inline-block;
    margin-bottom: 20px;
  }
  
  .page-header {
    text-align: left;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
