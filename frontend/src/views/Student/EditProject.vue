<!-- frontend/src/views/Student/EditProject.vue -->
<template>
  <div class="edit-project-page">
    <div class="container">
      
      <!-- Header -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Cancelar
        </button>
      </div>

      <!-- Hero Header -->
      <div class="hero-header">
        <div class="hero-icon">✏️</div>
        <div class="hero-content">
          <h1>Editar Proyecto</h1>
          <p>Actualiza la información de tu propuesta</p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyecto...</p>
      </div>

      <!-- Edit Form -->
      <form v-else-if="formData" @submit.prevent="handleUpdate" class="edit-form">
        
        <!-- Información Básica -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">📋</div>
            <div>
              <h2>Información del Proyecto</h2>
              <p>Actualiza los datos principales</p>
            </div>
          </div>

          <div class="form-grid">
            <!-- Nombre -->
            <div class="form-field full-width">
              <label class="field-label">
                <span class="label-text">Nombre del Proyecto</span>
                <span class="label-required">*</span>
              </label>
              <input 
                v-model="formData.nombre" 
                type="text" 
                class="field-input"
                placeholder="Nombre del proyecto"
                required
                maxlength="200"
              />
              <div class="field-footer">
                <span class="field-hint">Título claro y descriptivo</span>
                <span class="field-counter">{{ formData.nombre.length }}/200</span>
              </div>
            </div>

            <!-- Descripción -->
            <div class="form-field full-width">
              <label class="field-label">
                <span class="label-text">Descripción</span>
                <span class="label-required">*</span>
              </label>
              <textarea 
                v-model="formData.descripcion" 
                class="field-textarea"
                placeholder="Describe el proyecto en detalle..."
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
            <div class="form-field full-width">
              <label class="field-label">
                <span class="label-text">Objetivos</span>
                <span class="label-required">*</span>
              </label>
              <textarea 
                v-model="formData.objetivos" 
                class="field-textarea"
                placeholder="• Objetivo General:&#10;&#10;• Objetivos Específicos:"
                required
                rows="6"
              ></textarea>
              <div class="field-footer">
                <span class="field-hint">💡 Define objetivos SMART</span>
              </div>
            </div>

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
                <span class="currency-formatted">{{ formatCurrency(formData.presupuesto_estimado) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Profesor Asesor -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">👨‍🏫</div>
            <div>
              <h2>Profesor Asesor</h2>
              <p>Actualiza el asesor del proyecto</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <span class="label-text">Seleccionar Profesor</span>
                <span class="label-required">*</span>
              </label>
              
              <div class="custom-select" :class="{ open: selectOpen }" @click="toggleSelect">
                <div class="select-trigger">
                  <div class="select-value">
                    <span v-if="!formData.profesor_id" class="select-placeholder">
                      🔍 Selecciona un profesor
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
            </div>
          </div>
        </div>

        <!-- Colaboradores -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">👥</div>
            <div>
              <h2>Colaboradores</h2>
              <p>Gestiona el equipo de trabajo</p>
            </div>
          </div>

          <div class="collaborators-manager">
            <!-- Lista Actual -->
            <div v-if="currentMembers.length > 0" class="current-members">
              <h3>✅ Colaboradores Actuales ({{ currentMembers.length }})</h3>
              <div class="members-list">
                <div 
                  v-for="member in currentMembers" 
                  :key="member.id"
                  class="member-chip"
                >
                  <div class="chip-avatar">{{ getInitials(member.student.nombre_completo) }}</div>
                  <div class="chip-info">
                    <strong>{{ member.student.nombre_completo }}</strong>
                    <span>{{ member.student.codigo_institucional }}</span>
                  </div>
                  <button 
                    type="button" 
                    @click="removeMember(member.id)" 
                    class="chip-remove"
                    :disabled="submitting"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>

            <!-- Agregar Nuevos -->
            <div class="add-members-section">
              <h3>➕ Agregar Colaboradores</h3>
              
              <div class="search-field">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input 
                  v-model="collaboratorSearch" 
                  type="text" 
                  class="search-input"
                  placeholder="Buscar estudiantes por nombre o código..."
                />
              </div>

              <div v-if="filteredStudents.length > 0" class="available-students">
                <div 
                  v-for="student in filteredStudents" 
                  :key="student.id"
                  class="student-item"
                  :class="{ selected: isSelected(student.id) }"
                  @click="toggleStudent(student)"
                >
                  <div class="student-avatar">{{ getInitials(student.nombre_completo) }}</div>
                  <div class="student-info">
                    <strong>{{ student.nombre_completo }}</strong>
                    <span>{{ student.codigo_institucional }}</span>
                  </div>
                  <div class="student-checkbox">
                    <div v-if="isSelected(student.id)" class="checkbox-checked">✓</div>
                    <div v-else class="checkbox-unchecked"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Nuevos Seleccionados -->
            <div v-if="newMembers.length > 0" class="new-members-section">
              <h3>🆕 Nuevos a Agregar ({{ newMembers.length }})</h3>
              <div class="new-members-list">
                <div 
                  v-for="student in newMembers" 
                  :key="student.id"
                  class="member-chip new-chip"
                >
                  <div class="chip-avatar">{{ getInitials(student.nombre_completo) }}</div>
                  <span>{{ student.nombre_completo }}</span>
                  <button 
                    type="button" 
                    @click="removeNewMember(student.id)" 
                    class="chip-remove"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <button type="button" @click="goBack" class="action-btn btn-cancel">
            Cancelar
          </button>
          <button 
            type="submit" 
            class="action-btn btn-save"
            :disabled="submitting || !canSave()"
          >
            <svg v-if="submitting" class="btn-spinner" viewBox="0 0 24 24">
              ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="50" stroke-dashoffset="25" />
            </svg>
            <span v-else>💾 Guardar Cambios</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'
import catalogsApi from '../../api/catalogs'
import membersApi from '../../api/members'

export default {
  name: 'EditProject',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const projectId = parseInt(route.params.id)
    const loading = ref(true)
    const submitting = ref(false)
    const selectOpen = ref(false)
    
    const formData = ref(null)
    const profesores = ref([])
    const availableStudents = ref([])
    const currentMembers = ref([])
    const newMembers = ref([])
    const collaboratorSearch = ref('')
    
    const filteredStudents = computed(() => {
      if (!collaboratorSearch.value) return availableStudents.value
      
      const query = collaboratorSearch.value.toLowerCase()
      return availableStudents.value.filter(s => 
        s.nombre_completo.toLowerCase().includes(query) ||
        s.codigo_institucional.toLowerCase().includes(query)
      ).filter(s => !isCurrentMember(s.id))
    })
    
    const isCurrentMember = (studentId) => {
      return currentMembers.value.some(m => m.student.id === studentId)
    }
    
    const isSelected = (studentId) => {
      return newMembers.value.some(s => s.id === studentId)
    }
    
    const loadProject = async () => {
      try {
        const response = await projectsApi.getProjectById(projectId)
        formData.value = {
          nombre: response.data.nombre,
          descripcion: response.data.descripcion,
          objetivos: response.data.objetivos,
          presupuesto_estimado: response.data.presupuesto_estimado,
          profesor_id: response.data.profesor.id
        }
      } catch (err) {
        console.error('Error cargando proyecto:', err)
        alert('Error al cargar el proyecto')
        router.push('/student')
      }
    }
    
    const loadProfesores = async () => {
      try {
        const response = await catalogsApi.getProfesores()
        profesores.value = response.data
      } catch (err) {
        console.error('Error cargando profesores:', err)
      }
    }
    
    const loadStudents = async () => {
      try {
        const response = await catalogsApi.getStudentsSameCareer()
        availableStudents.value = response.data
      } catch (err) {
        console.error('Error cargando estudiantes:', err)
      }
    }
    
    const loadMembers = async () => {
      try {
        const response = await membersApi.getMembers(projectId)
        currentMembers.value = response.data
      } catch (err) {
        console.error('Error cargando colaboradores:', err)
      }
    }
    
    const loadAll = async () => {
      loading.value = true
      await Promise.all([
        loadProject(),
        loadProfesores(),
        loadStudents(),
        loadMembers()
      ])
      loading.value = false
    }
    
    const toggleSelect = () => {
      selectOpen.value = !selectOpen.value
    }
    
    const selectProfesor = (id) => {
      formData.value.profesor_id = id
      selectOpen.value = false
    }
    
    const toggleStudent = (student) => {
      const index = newMembers.value.findIndex(s => s.id === student.id)
      if (index > -1) {
        newMembers.value.splice(index, 1)
      } else {
        newMembers.value.push(student)
      }
    }
    
    const removeNewMember = (studentId) => {
      newMembers.value = newMembers.value.filter(s => s.id !== studentId)
    }
    
    const removeMember = async (memberId) => {
      if (!confirm('¿Eliminar este colaborador del proyecto?')) return
      
      try {
        await membersApi.removeMember(projectId, memberId)
        currentMembers.value = currentMembers.value.filter(m => m.id !== memberId)
        alert('✅ Colaborador eliminado')
      } catch (err) {
        alert('❌ Error al eliminar colaborador')
      }
    }
    
    const canSave = () => {
      return formData.value.nombre.length > 0 &&
             formData.value.descripcion.length >= 100 &&
             formData.value.objetivos.length > 0 &&
             formData.value.presupuesto_estimado > 0 &&
             formData.value.profesor_id
    }
    
    const handleUpdate = async () => {
      if (!canSave()) {
        alert('Por favor completa todos los campos requeridos')
        return
      }
      
      submitting.value = true
      
      try {
        // Actualizar proyecto
        await projectsApi.updateProject(projectId, formData.value)
        
        // Agregar nuevos colaboradores
        for (const student of newMembers.value) {
          try {
            await membersApi.addMember(projectId, student.id)
          } catch (err) {
            console.error('Error agregando colaborador:', err)
          }
        }
        
        alert('✅ Proyecto actualizado exitosamente')
        router.push(`/student/project/${projectId}`)
        
      } catch (err) {
        console.error('Error actualizando proyecto:', err)
        alert('❌ Error al actualizar el proyecto')
      } finally {
        submitting.value = false
      }
    }
    
    const goBack = () => router.push(`/student/project/${projectId}`)
    
    const getInitials = (name) => {
      if (!name) return '??'
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
      loadAll()
    })
    
    return {
      loading,
      submitting,
      selectOpen,
      formData,
      profesores,
      availableStudents,
      filteredStudents,
      currentMembers,
      newMembers,
      collaboratorSearch,
      toggleSelect,
      selectProfesor,
      toggleStudent,
      removeNewMember,
      removeMember,
      isSelected,
      canSave,
      handleUpdate,
      goBack,
      getInitials,
      formatCurrency,
      getProfesorName
    }
  }
}
</script>

<style scoped>
/* Base */
.edit-project-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Header */
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

/* Hero */
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
  font-size: 64px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.6));
}

.hero-content h1 {
  font-size: 28px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.hero-content p {
  font-size: 15px;
  color: #e0e7ff;
  font-weight: 600;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 64px;
  height: 64px;
  border: 4px solid #334155;
  border-top-color: #d4af37;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #cbd5e1;
  font-size: 16px;
  font-weight: 600;
}

/* Form */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid #d4af37;
}

.section-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.4));
}

.section-header h2 {
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 4px;
}

.section-header p {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.full-width {
  grid-column: 1 / -1;
}

/* Form Fields */
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
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-required {
  color: #ef4444;
  font-weight: 900;
  font-size: 16px;
}

.field-input,
.field-textarea {
  width: 100%;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.3s ease;
}

.field-input::placeholder,
.field-textarea::placeholder {
  color: #64748b;
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
}

.field-hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.field-hint.error {
  color: #f87171;
  font-weight: 700;
}

.field-counter {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

/* Currency Input */
.currency-input {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.currency-input:focus-within {
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.currency-symbol {
  font-size: 20px;
  font-weight: 900;
  color: #d4af37;
}

.currency-field {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 18px;
  font-weight: 800;
  outline: none;
}

.currency-code {
  font-size: 13px;
  font-weight: 700;
  color: #94a3b8;
  padding: 4px 10px;
  background: #1e293b;
  border-radius: 6px;
}

.currency-formatted {
  font-size: 16px;
  font-weight: 900;
  color: #d4af37;
}

/* Custom Select */
.custom-select {
  position: relative;
}

.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-trigger:hover {
  border-color: #d4af37;
}

.custom-select.open .select-trigger {
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.select-placeholder {
  color: #64748b;
  font-weight: 600;
  font-size: 14px;
}

.select-selected {
  color: #f1f5f9;
  font-weight: 700;
  font-size: 14px;
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
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: #0f172a;
  border: 2px solid #d4af37;
  border-radius: 10px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.select-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid #1e293b;
}

.select-option:hover {
  background: #1e293b;
}

.select-option.selected {
  background: rgba(212, 175, 55, 0.15);
}

.option-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 13px;
  flex-shrink: 0;
}

.option-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-info strong {
  font-size: 13px;
  color: #f1f5f9;
  font-weight: 700;
}

.option-info span {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
}

.option-check {
  width: 22px;
  height: 22px;
  color: #10b981;
}

/* Collaborators Manager */
.collaborators-manager {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.current-members h3,
.add-members-section h3,
.new-members-section h3 {
  font-size: 15px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.member-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid #334155;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.member-chip:hover {
  border-color: #d4af37;
}

.chip-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 14px;
  flex-shrink: 0;
}

.chip-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chip-info strong {
  font-size: 14px;
  color: #ffffff;
  font-weight: 700;
}

.chip-info span {
  font-size: 12px;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
  font-weight: 600;
}

.chip-remove {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ef4444;
  border: none;
  color: #ffffff;
  font-weight: 900;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.chip-remove:hover:not(:disabled) {
  background: #dc2626;
  transform: scale(1.1);
}

.chip-remove:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Search */
.search-field {
  position: relative;
  margin-bottom: 16px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 14px 18px 14px 48px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

/* Available Students */
.available-students {
  max-height: 350px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 4px;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid #334155;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.student-item:hover {
  background: #1e293b;
  border-color: #475569;
}

.student-item.selected {
  background: rgba(212, 175, 55, 0.15);
  border-color: #d4af37;
}

.student-avatar {
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

.student-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.student-info strong {
  font-size: 13px;
  color: #f1f5f9;
  font-weight: 700;
}

.student-info span {
  font-size: 11px;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
  font-weight: 600;
}

.checkbox-checked,
.checkbox-unchecked {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 16px;
  flex-shrink: 0;
}

.checkbox-checked {
  background: #10b981;
  color: #ffffff;
}

.checkbox-unchecked {
  border: 2px solid #475569;
  background: transparent;
}

/* New Members */
.new-members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.new-chip {
  display: inline-flex;
  padding: 10px 14px;
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
}

.new-chip .chip-avatar {
  width: 28px;
  height: 28px;
  font-size: 12px;
}

.new-chip span {
  font-size: 13px;
  color: #ffffff;
  font-weight: 700;
}

.new-chip .chip-remove {
  width: 24px;
  height: 24px;
  font-size: 14px;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 16px;
  padding: 32px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.action-btn {
  flex: 1;
  padding: 16px 28px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-cancel {
  background: #475569;
  color: #ffffff;
}

.btn-cancel:hover {
  background: #334155;
  transform: translateY(-2px);
}

.btn-save {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  color: #0a0f1e;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

/* Responsive */
@media (max-width: 768px) {
  .edit-project-page {
    padding: 20px 12px;
  }

  .hero-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .form-section {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
