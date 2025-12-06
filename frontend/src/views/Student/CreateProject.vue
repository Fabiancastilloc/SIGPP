<!-- frontend/src/views/Student/CreateProject.vue -->
<template>
  <div class="create-project-page">
    <div class="container">
      <!-- Header con mejor contraste -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver
        </button>
      </div>

      <!-- Hero Header -->
      <div class="hero-header">
        <div class="hero-icon">🚀</div>
        <div class="hero-content">
          <h1>Crear Nueva Propuesta</h1>
          <p>Completa todos los campos para enviar tu proyecto</p>
        </div>
      </div>

      <!-- Progress Steps - Mejorado -->
      <div class="progress-container">
        <div class="progress-steps">
          <div :class="['step-item', { active: currentStep === 1, completed: currentStep > 1 }]">
            <div class="step-circle">
              <span v-if="currentStep > 1" class="check-icon">✓</span>
              <span v-else>1</span>
            </div>
            <span class="step-label">Información Básica</span>
          </div>
          
          <div class="step-connector" :class="{ active: currentStep > 1 }"></div>
          
          <div :class="['step-item', { active: currentStep === 2, completed: currentStep > 2 }]">
            <div class="step-circle">
              <span v-if="currentStep > 2" class="check-icon">✓</span>
              <span v-else>2</span>
            </div>
            <span class="step-label">Equipo de Trabajo</span>
          </div>
          
          <div class="step-connector" :class="{ active: currentStep > 2 }"></div>
          
          <div :class="['step-item', { active: currentStep === 3, completed: currentStep > 3 }]">
            <div class="step-circle">
              <span v-if="currentStep > 3" class="check-icon">✓</span>
              <span v-else>3</span>
            </div>
            <span class="step-label">Presupuesto</span>
          </div>
        </div>
      </div>

      <!-- Formulario con mejor contraste -->
      <form @submit.prevent="handleSubmit" class="project-form">
        
        <!-- ============ PASO 1: Información Básica ============ -->
        <div v-show="currentStep === 1" class="form-step">
          <div class="step-header">
            <div class="step-header-icon">📋</div>
            <div>
              <h2>Información del Proyecto</h2>
              <p>Define el alcance y objetivos de tu propuesta</p>
            </div>
          </div>

          <div class="form-content">
            <!-- Nombre del Proyecto -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Nombre del Proyecto</span>
                <span class="label-required">*</span>
              </label>
              <input 
                v-model="formData.nombre" 
                type="text" 
                class="field-input"
                placeholder="Ej: Sistema de Gestión de Proyectos de Grado"
                required
                maxlength="200"
              />
              <div class="field-footer">
                <span class="field-hint">Un título claro y descriptivo</span>
                <span class="field-counter">{{ formData.nombre.length }}/200</span>
              </div>
            </div>

            <!-- Descripción -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Descripción Detallada</span>
                <span class="label-required">*</span>
              </label>
              <textarea 
                v-model="formData.descripcion" 
                class="field-textarea"
                placeholder="Describe el problema que resuelve tu proyecto, la metodología a usar, tecnologías y el impacto esperado. Sé específico y detallado."
                required
                rows="8"
                minlength="100"
              ></textarea>
              <div class="field-footer">
                <span 
                  :class="['field-hint', { error: formData.descripcion.length < 100 }]"
                >
                  {{ formData.descripcion.length < 100 ? '⚠️ Mínimo 100 caracteres' : '✓ Descripción válida' }}
                </span>
                <span class="field-counter">{{ formData.descripcion.length }}/100</span>
              </div>
            </div>

            <!-- Objetivos -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Objetivos del Proyecto</span>
                <span class="label-required">*</span>
              </label>
              <textarea 
                v-model="formData.objetivos" 
                class="field-textarea"
                placeholder="• Objetivo General: [Describe el propósito principal]&#10;&#10;• Objetivos Específicos:&#10;  1. [Objetivo específico 1]&#10;  2. [Objetivo específico 2]&#10;  3. [Objetivo específico 3]"
                required
                rows="7"
              ></textarea>
              <div class="field-footer">
                <span class="field-hint">💡 Define objetivos SMART (Específicos, Medibles, Alcanzables)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ============ PASO 2: Equipo de Trabajo ============ -->
        <div v-show="currentStep === 2" class="form-step">
          <div class="step-header">
            <div class="step-header-icon">👥</div>
            <div>
              <h2>Equipo de Trabajo</h2>
              <p>Selecciona tu asesor y agrega colaboradores</p>
            </div>
          </div>

          <div class="form-content">
            <!-- Selección de Profesor -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Profesor Asesor</span>
                <span class="label-required">*</span>
              </label>
              
              <div class="custom-select" :class="{ open: selectOpen }" @click="toggleSelect">
                <div class="select-trigger">
                  <div class="select-value">
                    <span v-if="!formData.profesor_id" class="select-placeholder">
                      🔍 Selecciona un profesor asesor
                    </span>
                    <span v-else class="select-selected">
                      👨‍🏫 {{ getProfesorName() }}
                    </span>
                  </div>
                  <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
                
                <div v-show="selectOpen" class="select-dropdown">
                  <div 
                    v-for="prof in profesores" 
                    :key="prof.id"
                    class="select-option"
                    :class="{ selected: formData.profesor_id === prof.id }"
                    @click.stop="selectProfesor(prof.id)"
                  >
                    <div class="option-avatar">
                      {{ getInitials(prof.nombre_completo) }}
                    </div>
                    <div class="option-info">
                      <strong>{{ prof.nombre_completo }}</strong>
                      <span>{{ prof.email }}</span>
                    </div>
                    <svg v-if="formData.profesor_id === prof.id" class="option-check" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <div v-if="formData.profesor_id" class="field-footer">
                <span class="field-hint success">✅ Profesor seleccionado correctamente</span>
              </div>
            </div>

            <!-- Colaboradores -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Colaboradores</span>
                <span class="label-optional">(Opcional)</span>
              </label>
              
              <div class="collaborators-section">
                <div class="section-banner">
                  <div class="banner-icon">🎓</div>
                  <div class="banner-content">
                    <strong>Estudiantes de tu carrera disponibles</strong>
                    <p>Selecciona compañeros para trabajar en equipo</p>
                  </div>
                </div>

                <!-- Buscador -->
                <div class="search-field">
                  <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <input 
                    v-model="collaboratorSearch" 
                    type="text" 
                    class="search-input"
                    placeholder="Buscar por nombre o código institucional..."
                  />
                </div>

                <!-- Lista de estudiantes -->
                <div v-if="filteredStudents.length > 0" class="students-list">
                  <div 
                    v-for="student in filteredStudents" 
                    :key="student.id"
                    class="student-item"
                    :class="{ selected: isSelected(student.id) }"
                    @click="toggleCollaborator(student)"
                  >
                    <div class="student-avatar">
                      {{ getInitials(student.nombre_completo) }}
                    </div>
                    <div class="student-details">
                      <strong class="student-name">{{ student.nombre_completo }}</strong>
                      <span class="student-code">{{ student.codigo_institucional }}</span>
                      <span class="student-badge">Semestre {{ student.semestre }}</span>
                    </div>
                    <div class="student-checkbox">
                      <div v-if="isSelected(student.id)" class="checkbox-checked">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <div v-else class="checkbox-unchecked"></div>
                    </div>
                  </div>
                </div>

                <!-- Colaboradores seleccionados -->
                <div v-if="selectedCollaborators.length > 0" class="selected-collaborators">
                  <div class="selected-header">
                    <strong>✅ Colaboradores Seleccionados</strong>
                    <span class="selected-count">{{ selectedCollaborators.length }}</span>
                  </div>
                  <div class="selected-list">
                    <div 
                      v-for="collab in selectedCollaborators" 
                      :key="collab.id"
                      class="selected-chip"
                    >
                      <span class="chip-avatar">{{ getInitials(collab.nombre_completo) }}</span>
                      <span class="chip-name">{{ collab.nombre_completo }}</span>
                      <button 
                        type="button" 
                        @click="removeCollaborator(collab.id)" 
                        class="chip-remove"
                        title="Eliminar"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Estado vacío -->
                <div v-if="availableStudents.length === 0" class="empty-message">
                  <div class="empty-icon">👥</div>
                  <p class="empty-text">No hay estudiantes de tu carrera disponibles</p>
                  <span class="empty-hint">Serás el único miembro del equipo</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ============ PASO 3: Presupuesto ============ -->
        <div v-show="currentStep === 3" class="form-step">
          <div class="step-header">
            <div class="step-header-icon">💰</div>
            <div>
              <h2>Presupuesto del Proyecto</h2>
              <p>Define el presupuesto estimado para la ejecución</p>
            </div>
          </div>

          <div class="form-content">
            <!-- Presupuesto -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Presupuesto Estimado</span>
                <span class="label-required">*</span>
              </label>
              <div class="currency-input">
                <span class="currency-symbol">$</span>
                <input 
                  v-model.number="formData.presupuesto_estimado" 
                  type="number" 
                  class="currency-field"
                  placeholder="0"
                  required
                  min="0"
                  step="1000"
                />
                <span class="currency-code">COP</span>
              </div>
              <div class="field-footer">
                <span class="field-hint">💡 Incluye materiales, equipos y otros gastos</span>
                <span class="currency-formatted">{{ formatCurrency(formData.presupuesto_estimado) }}</span>
              </div>
            </div>

            <!-- Resumen del proyecto -->
            <div class="project-summary">
              <h3 class="summary-title">📊 Resumen del Proyecto</h3>
              
              <div class="summary-cards">
                <div class="summary-card card-primary">
                  <div class="card-icon">👥</div>
                  <div class="card-content">
                    <span class="card-label">Equipo de Trabajo</span>
                    <strong class="card-value">{{ selectedCollaborators.length + 1 }} miembros</strong>
                  </div>
                </div>

                <div class="summary-card card-success">
                  <div class="card-icon">💰</div>
                  <div class="card-content">
                    <span class="card-label">Presupuesto</span>
                    <strong class="card-value">{{ formatCurrency(formData.presupuesto_estimado) }}</strong>
                  </div>
                </div>

                <div class="summary-card card-info">
                  <div class="card-icon">👨‍🏫</div>
                  <div class="card-content">
                    <span class="card-label">Profesor Asesor</span>
                    <strong class="card-value">{{ getProfesorName() }}</strong>
                  </div>
                </div>
              </div>

              <div class="summary-details">
                <div class="detail-row">
                  <span class="detail-label">📝 Nombre del proyecto:</span>
                  <span class="detail-value">{{ formData.nombre || 'Sin definir' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">📋 Descripción:</span>
                  <span class="detail-value">{{ formData.descripcion.substring(0, 100) }}{{ formData.descripcion.length > 100 ? '...' : '' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Botones de navegación -->
        <div class="form-navigation">
          <button 
            v-if="currentStep > 1" 
            type="button" 
            @click="prevStep" 
            class="nav-btn nav-btn-secondary"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Anterior
          </button>
          
          <div class="nav-spacer"></div>
          
          <button 
            v-if="currentStep < 3" 
            type="button" 
            @click="nextStep" 
            class="nav-btn nav-btn-primary"
            :disabled="!canProceed()"
          >
            Siguiente
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
          
          <button 
            v-if="currentStep === 3" 
            type="submit" 
            class="nav-btn nav-btn-success"
            :disabled="submitting || !canProceed()"
          >
            <svg v-if="submitting" class="btn-spinner" viewBox="0 0 24 24">
              ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="50" stroke-dashoffset="25" />
            </svg>
            <span v-else>🚀 Crear Proyecto</span>
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
import membersApi from '../../api/members'

export default {
  name: 'CreateProject',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const currentStep = ref(1)
    const submitting = ref(false)
    const selectOpen = ref(false)
    
    const formData = ref({
      nombre: '',
      descripcion: '',
      objetivos: '',
      profesor_id: '',
      presupuesto_estimado: 0
    })
    
    const profesores = ref([])
    const availableStudents = ref([])
    const selectedCollaborators = ref([])
    const collaboratorSearch = ref('')
    
    const filteredStudents = computed(() => {
      if (!collaboratorSearch.value) {
        return availableStudents.value
      }
      
      const query = collaboratorSearch.value.toLowerCase()
      return availableStudents.value.filter(s => 
        s.nombre_completo.toLowerCase().includes(query) ||
        s.codigo_institucional.toLowerCase().includes(query)
      )
    })
    
    const loadProfesores = async () => {
      try {
        const response = await catalogsApi.getProfesores()
        profesores.value = response.data
      } catch (err) {
        console.error('Error cargando profesores:', err)
        alert('Error al cargar la lista de profesores')
      }
    }
    
    const loadAvailableStudents = async () => {
      try {
        const response = await catalogsApi.getStudentsSameCareer()
        availableStudents.value = response.data
      } catch (err) {
        console.error('Error cargando estudiantes:', err)
      }
    }
    
    const toggleSelect = () => {
      selectOpen.value = !selectOpen.value
    }
    
    const selectProfesor = (id) => {
      formData.value.profesor_id = id
      selectOpen.value = false
    }
    
    const toggleCollaborator = (student) => {
      const index = selectedCollaborators.value.findIndex(s => s.id === student.id)
      if (index > -1) {
        selectedCollaborators.value.splice(index, 1)
      } else {
        selectedCollaborators.value.push(student)
      }
    }
    
    const removeCollaborator = (studentId) => {
      selectedCollaborators.value = selectedCollaborators.value.filter(s => s.id !== studentId)
    }
    
    const isSelected = (studentId) => {
      return selectedCollaborators.value.some(s => s.id === studentId)
    }
    
    const canProceed = () => {
      if (currentStep.value === 1) {
        return formData.value.nombre.length > 0 && 
               formData.value.descripcion.length >= 100 &&
               formData.value.objetivos.length > 0
      }
      if (currentStep.value === 2) {
        return formData.value.profesor_id !== ''
      }
      if (currentStep.value === 3) {
        return formData.value.presupuesto_estimado > 0
      }
      return true
    }
    
    const nextStep = () => {
      if (canProceed()) {
        currentStep.value++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        alert('Por favor completa todos los campos requeridos')
      }
    }
    
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    const handleSubmit = async () => {
      if (!canProceed()) {
        alert('Por favor completa todos los campos')
        return
      }
      
      submitting.value = true
      
      try {
        const projectData = {
          nombre: formData.value.nombre,
          descripcion: formData.value.descripcion,
          objetivos: formData.value.objetivos,
          profesor_id: formData.value.profesor_id,
          presupuesto_estimado: formData.value.presupuesto_estimado
        }
        
        const response = await projectsApi.createProject(projectData)
        const projectId = response.data.id
        
        if (selectedCollaborators.value.length > 0) {
          for (const collab of selectedCollaborators.value) {
            try {
              await membersApi.addMember(projectId, collab.id)
            } catch (err) {
              console.error('Error agregando colaborador:', err)
            }
          }
        }
        
        alert('🎉 ¡Proyecto creado exitosamente!')
        router.push('/student')
        
      } catch (err) {
        console.error('Error al crear proyecto:', err)
        alert(err.response?.data?.detail || 'Error al crear el proyecto')
      } finally {
        submitting.value = false
      }
    }
    
    const goBack = () => router.push('/student')
    
    const getInitials = (name) => {
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    const formatCurrency = (value) => {
      if (!value) return '$0 COP'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }
    
    const getProfesorName = () => {
      if (!formData.value.profesor_id) return 'No seleccionado'
      const prof = profesores.value.find(p => p.id === formData.value.profesor_id)
      return prof ? prof.nombre_completo : 'No seleccionado'
    }
    
    onMounted(() => {
      loadProfesores()
      loadAvailableStudents()
    })
    
    return {
      currentStep,
      submitting,
      selectOpen,
      formData,
      profesores,
      availableStudents,
      filteredStudents,
      selectedCollaborators,
      collaboratorSearch,
      toggleSelect,
      selectProfesor,
      toggleCollaborator,
      removeCollaborator,
      isSelected,
      nextStep,
      prevStep,
      canProceed,
      handleSubmit,
      goBack,
      getInitials,
      formatCurrency,
      getProfesorName
    }
  }
}
</script>

<style scoped>
/* ==================== VARIABLES ==================== */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.create-project-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* ==================== HEADER ==================== */
.page-header {
  margin-bottom: 24px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: #334155;
  border-color: #d4af37;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* ==================== HERO HEADER ==================== */
.hero-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border: 3px solid #3b82f6;
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.hero-icon {
  font-size: 72px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.6));
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.hero-content h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.hero-content p {
  font-size: 16px;
  color: #e0e7ff;
  font-weight: 600;
}

/* ==================== PROGRESS STEPS ==================== */
.progress-container {
  margin-bottom: 40px;
  padding: 24px;
  background: rgba(30, 41, 59, 0.6);
  border-radius: 16px;
  border: 2px solid #334155;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 600px;
  margin: 0 auto;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  flex: 0 0 auto;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step-item.active,
.step-item.completed {
  opacity: 1;
}

.step-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #1e293b;
  border: 3px solid #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 20px;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.step-item.active .step-circle {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border-color: #d4af37;
  color: #0a0f1e;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
  transform: scale(1.1);
}

.step-item.completed .step-circle {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-color: #10b981;
  color: #ffffff;
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.5);
}

.check-icon {
  font-size: 24px;
}

.step-label {
  font-size: 13px;
  font-weight: 700;
  color: #f1f5f9;
  text-align: center;
  white-space: nowrap;
}

.step-connector {
  flex: 1;
  height: 4px;
  background: #334155;
  margin: 0 12px;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.step-connector.active {
  background: linear-gradient(90deg, #d4af37 0%, #10b981 100%);
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.5);
}

/* ==================== FORM ==================== */
.project-form {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.form-step {
  animation: slideIn 0.4s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.step-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 3px solid #d4af37;
}

.step-header-icon {
  font-size: 48px;
  filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.4));
}

.step-header h2 {
  font-size: 26px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 4px;
}

.step-header p {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

/* ==================== FORM FIELDS ==================== */
.form-content {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.label-text {
  font-size: 15px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-required {
  color: #ef4444;
  font-weight: 900;
  font-size: 18px;
}

.label-optional {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: none;
}

.field-input,
.field-textarea {
  width: 100%;
  padding: 16px 20px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.3s ease;
}

.field-input::placeholder,
.field-textarea::placeholder {
  color: #64748b;
  font-weight: 500;
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  background: #1e293b;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.field-textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
}

.field-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.field-hint {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

.field-hint.error {
  color: #f87171;
  font-weight: 700;
}

.field-hint.success {
  color: #34d399;
  font-weight: 700;
}

.field-counter {
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

/* ==================== CUSTOM SELECT ==================== */
.custom-select {
  position: relative;
}

.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-trigger:hover {
  border-color: #d4af37;
}

.custom-select.open .select-trigger {
  border-color: #d4af37;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.select-value {
  flex: 1;
}

.select-placeholder {
  color: #64748b;
  font-weight: 600;
  font-size: 15px;
}

.select-selected {
  color: #f1f5f9;
  font-weight: 700;
  font-size: 15px;
}

.select-arrow {
  width: 20px;
  height: 20px;
  color: #d4af37;
  transition: transform 0.3s ease;
}

.custom-select.open .select-arrow {
  transform: rotate(180deg);
}

.select-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #0f172a;
  border: 2px solid #d4af37;
  border-top: none;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  max-height: 320px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.select-dropdown::-webkit-scrollbar {
  width: 8px;
}

.select-dropdown::-webkit-scrollbar-track {
  background: #1e293b;
}

.select-dropdown::-webkit-scrollbar-thumb {
  background: #d4af37;
  border-radius: 4px;
}

.select-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid #1e293b;
}

.select-option:last-child {
  border-bottom: none;
}

.select-option:hover {
  background: #1e293b;
}

.select-option.selected {
  background: rgba(212, 175, 55, 0.15);
}

.option-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 14px;
  flex-shrink: 0;
}

.option-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-info strong {
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 700;
}

.option-info span {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.option-check {
  width: 24px;
  height: 24px;
  color: #10b981;
  flex-shrink: 0;
}

/* ==================== COLLABORATORS SECTION ==================== */
.collaborators-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(30, 64, 175, 0.1));
  border: 2px solid #3b82f6;
  border-radius: 12px;
}

.banner-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(59, 130, 246, 0.5));
}

.banner-content strong {
  display: block;
  font-size: 16px;
  color: #ffffff;
  margin-bottom: 4px;
  font-weight: 800;
}

.banner-content p {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 600;
}

/* ==================== SEARCH FIELD ==================== */
.search-field {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  color: #64748b;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 16px 20px 16px 52px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: #64748b;
}

.search-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

/* ==================== STUDENTS LIST ==================== */
.students-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
  padding: 4px;
}

.students-list::-webkit-scrollbar {
  width: 8px;
}

.students-list::-webkit-scrollbar-track {
  background: #0f172a;
  border-radius: 4px;
}

.students-list::-webkit-scrollbar-thumb {
  background: #d4af37;
  border-radius: 4px;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.student-item:hover {
  background: #1e293b;
  border-color: #475569;
  transform: translateX(4px);
}

.student-item.selected {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.1));
  border-color: #d4af37;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.3);
}

.student-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 16px;
  flex-shrink: 0;
}

.student-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.student-name {
  font-size: 15px;
  color: #f1f5f9;
  font-weight: 700;
}

.student-code {
  font-size: 12px;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
  font-weight: 700;
}

.student-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid #d4af37;
  border-radius: 12px;
  font-size: 11px;
  color: #d4af37;
  font-weight: 800;
  width: fit-content;
}

.student-checkbox {
  flex-shrink: 0;
}

.checkbox-checked,
.checkbox-unchecked {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.checkbox-checked {
  background: #10b981;
}

.checkbox-checked svg {
  width: 28px;
  height: 28px;
  color: #ffffff;
}

.checkbox-unchecked {
  border: 3px solid #475569;
  background: transparent;
}

/* ==================== SELECTED COLLABORATORS ==================== */
.selected-collaborators {
  padding: 20px;
  background: rgba(16, 185, 129, 0.15);
  border: 2px solid #10b981;
  border-radius: 12px;
}

.selected-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.selected-header strong {
  font-size: 15px;
  color: #10b981;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.selected-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #10b981;
  color: #ffffff;
  border-radius: 50%;
  font-weight: 900;
  font-size: 14px;
}

.selected-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.selected-chip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 24px;
  transition: all 0.3s ease;
}

.selected-chip:hover {
  border-color: #d4af37;
}

.chip-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 11px;
}

.chip-name {
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 700;
}

.chip-remove {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ef4444;
  border: none;
  color: #ffffff;
  font-weight: 900;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.chip-remove:hover {
  background: #dc2626;
  transform: scale(1.1);
}

/* ==================== CURRENCY INPUT ==================== */
.currency-input {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.currency-input:focus-within {
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.currency-symbol {
  font-size: 24px;
  font-weight: 900;
  color: #d4af37;
}

.currency-field {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 20px;
  font-weight: 800;
  outline: none;
}

.currency-field::placeholder {
  color: #64748b;
}

.currency-code {
  font-size: 14px;
  font-weight: 700;
  color: #94a3b8;
  padding: 6px 12px;
  background: #1e293b;
  border-radius: 6px;
}

.currency-formatted {
  font-size: 18px;
  font-weight: 900;
  color: #d4af37;
}

/* ==================== PROJECT SUMMARY ==================== */
.project-summary {
  padding: 28px;
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.2), rgba(30, 58, 138, 0.1));
  border: 3px solid #3b82f6;
  border-radius: 16px;
}

.summary-title {
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid;
}

.summary-card.card-primary {
  background: rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
}

.summary-card.card-success {
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
}

.summary-card.card-info {
  background: rgba(212, 175, 55, 0.15);
  border-color: #d4af37;
}

.card-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.3));
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-label {
  font-size: 11px;
  color: #cbd5e1;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-value {
  font-size: 18px;
  color: #ffffff;
  font-weight: 900;
}

.summary-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 20px;
  border-top: 2px solid #334155;
}

.detail-row {
  display: flex;
  gap: 12px;
}

.detail-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  min-width: 180px;
}

.detail-value {
  font-size: 13px;
  color: #f1f5f9;
  font-weight: 600;
  flex: 1;
}

/* ==================== NAVIGATION BUTTONS ==================== */
.form-navigation {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
  padding-top: 32px;
  border-top: 3px solid #334155;
}

.nav-spacer {
  flex: 1;
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-btn svg {
  width: 20px;
  height: 20px;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.nav-btn-secondary {
  background: #1e293b;
  border: 2px solid #475569;
  color: #f1f5f9;
}

.nav-btn-secondary:hover:not(:disabled) {
  background: #334155;
  border-color: #d4af37;
  transform: translateX(-4px);
}

.nav-btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: #ffffff;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
}

.nav-btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(59, 130, 246, 0.6);
}

.nav-btn-success {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  color: #0a0f1e;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
  font-size: 16px;
  padding: 18px 40px;
}

.nav-btn-success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

.btn-spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ==================== EMPTY STATE ==================== */
.empty-message {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 72px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  font-size: 16px;
  color: #f1f5f9;
  font-weight: 700;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .create-project-page {
    padding: 20px 12px;
  }

  .hero-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .hero-icon {
    font-size: 56px;
  }

  .hero-content h1 {
    font-size: 24px;
  }

  .progress-steps {
    flex-direction: column;
  }

  .step-connector {
    width: 4px;
    height: 32px;
    margin: 8px 0;
  }

  .project-form {
    padding: 24px;
  }

  .step-header {
    flex-direction: column;
    text-align: center;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .form-navigation {
    flex-direction: column;
  }

  .nav-spacer {
    display: none;
  }

  .nav-btn {
    width: 100%;
    justify-content: center;
  }

  .detail-row {
    flex-direction: column;
    gap: 4px;
  }

  .detail-label {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .select-dropdown {
    max-height: 240px;
  }

  .students-list {
    max-height: 300px;
  }
}
</style>
