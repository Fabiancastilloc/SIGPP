<template>
  <div class="validate-page">
    <div class="container">
      <div class="page-header">
        <router-link to="/professor" class="btn-back">
          ← Volver al Dashboard
        </router-link>
        <h1>✅ Validar Proyectos</h1>
        <p>Revisa los proyectos pendientes de validación académica</p>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <div v-else-if="pendingProjects.length === 0" class="empty-state">
        <div class="empty-icon">✅</div>
        <h3>No hay proyectos pendientes</h3>
        <p>Todos los proyectos han sido validados</p>
      </div>

      <div v-else class="validation-grid">
        <div v-for="project in pendingProjects" :key="project.id" class="validation-card">
          <div class="card-ribbon">Pendiente de Revisión</div>
          
          <div class="card-header">
            <h3>{{ project.nombre }}</h3>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
          </div>

          <div class="card-body">
            <div class="info-section">
              <div class="info-item">
                <span class="info-icon">👨‍🎓</span>
                <div>
                  <span class="info-label">Estudiante</span>
                  <span class="info-value">{{ project.estudiante.nombre }}</span>
                </div>
              </div>
              <div class="info-item">
                <span class="info-icon">💰</span>
                <div>
                  <span class="info-label">Presupuesto</span>
                  <span class="info-value">${{ formatMoney(project.presupuesto_estimado) }}</span>
                </div>
              </div>
            </div>

            <div class="description-box">
              <h4>📝 Descripción</h4>
              <p>{{ truncate(project.descripcion, 200) }}</p>
              <button @click="expandProject(project)" class="btn-expand">
                Ver más →
              </button>
            </div>
          </div>

          <div class="card-actions">
            <button 
              @click="openValidationModal(project, true)" 
              class="btn btn-success btn-block"
            >
              ✅ Validar
            </button>
            <button 
              @click="openValidationModal(project, false)" 
              class="btn btn-outline-danger btn-block"
            >
              ↩️ Devolver
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalle -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header">
          <h2>📋 Detalles del Proyecto</h2>
          <button @click="closeDetailModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-card">
            <h3>{{ selectedProject.nombre }}</h3>
            <p class="project-code">{{ selectedProject.codigo_proyecto }}</p>
            
            <div class="detail-section">
              <h4>👨‍🎓 Información del Estudiante</h4>
              <p><strong>Nombre:</strong> {{ selectedProject.estudiante.nombre }}</p>
              <p><strong>Email:</strong> {{ selectedProject.estudiante.email }}</p>
            </div>

            <div class="detail-section">
              <h4>📝 Descripción Completa</h4>
              <p>{{ selectedProject.descripcion }}</p>
            </div>

            <div class="detail-section">
              <h4>🎯 Objetivos</h4>
              <p>{{ selectedProject.objetivos }}</p>
            </div>

            <div class="detail-section">
              <h4>💰 Presupuesto Estimado</h4>
              <p class="budget-amount">${{ formatMoney(selectedProject.presupuesto_estimado) }} COP</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeDetailModal" class="btn btn-secondary">
            Cerrar
          </button>
          <button 
            @click="openValidationModal(selectedProject, true); closeDetailModal();" 
            class="btn btn-success"
          >
            ✅ Validar Proyecto
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Validación (igual que en ProfessorDashboard) -->
    <div v-if="showValidationModal" class="modal-overlay" @click="closeValidationModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ validationMode ? '✅ Validar Proyecto' : '↩️ Devolver Proyecto' }}</h2>
          <button @click="closeValidationModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="project-summary">
            <h3>{{ projectToValidate.nombre }}</h3>
            <p>Estudiante: {{ projectToValidate.estudiante.nombre }}</p>
          </div>
          
          <div class="form-group">
            <label class="form-label">Comentarios {{ validationMode ? '(Opcional)' : '*' }}</label>
            <textarea 
              v-model="comentarios" 
              class="form-control" 
              rows="4"
              :placeholder="validationMode ? 'Añade comentarios o sugerencias...' : 'Explica por qué devuelves el proyecto...'"
              :required="!validationMode"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeValidationModal" class="btn btn-secondary">
            Cancelar
          </button>
          <button 
            @click="confirmValidation" 
            :class="['btn', validationMode ? 'btn-success' : 'btn-danger']"
            :disabled="processing"
          >
            <span v-if="!processing">{{ validationMode ? '✅ Confirmar' : '↩️ Devolver' }}</span>
            <span v-else>⏳ Procesando...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import projectsApi from '../../api/projects'

export default {
  name: 'ValidateProjects',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    const showDetailModal = ref(false)
    const showValidationModal = ref(false)
    const selectedProject = ref(null)
    const projectToValidate = ref(null)
    const validationMode = ref(true)
    const comentarios = ref('')
    const processing = ref(false)
    
    const pendingProjects = computed(() => 
      projects.value.filter(p => p.estado === 'pendiente_profesor')
    )
    
    const loadProjects = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjects()
        projects.value = response.data
      } catch (err) {
        console.error('Error cargando proyectos', err)
      } finally {
        loading.value = false
      }
    }
    
    const expandProject = (project) => {
      selectedProject.value = project
      showDetailModal.value = true
    }
    
    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedProject.value = null
    }
    
    const openValidationModal = (project, approve) => {
      projectToValidate.value = project
      validationMode.value = approve
      comentarios.value = ''
      showValidationModal.value = true
    }
    
    const closeValidationModal = () => {
      showValidationModal.value = false
      projectToValidate.value = null
      comentarios.value = ''
    }
    
    const confirmValidation = async () => {
      if (!validationMode.value && !comentarios.value.trim()) {
        alert('Debes agregar comentarios al devolver un proyecto')
        return
      }
      
      processing.value = true
      try {
        await projectsApi.validateProject(projectToValidate.value.id, {
          aprobado: validationMode.value,
          comentarios: comentarios.value
        })
        alert(validationMode.value ? '✅ Proyecto validado exitosamente' : '↩️ Proyecto devuelto al estudiante')
        closeValidationModal()
        loadProjects()
      } catch (err) {
        alert('Error al procesar el proyecto')
      } finally {
        processing.value = false
      }
    }
    
    const truncate = (text, length) => {
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const formatMoney = (value) => {
      return new Intl.NumberFormat('es-CO').format(value)
    }
    
    onMounted(() => {
      loadProjects()
    })
    
    return {
      projects,
      loading,
      pendingProjects,
      showDetailModal,
      showValidationModal,
      selectedProject,
      projectToValidate,
      validationMode,
      comentarios,
      processing,
      expandProject,
      closeDetailModal,
      openValidationModal,
      closeValidationModal,
      confirmValidation,
      truncate,
      formatMoney
    }
  }
}
</script>

<style scoped>
.validate-page {
  padding: 30px 0;
  min-height: calc(100vh - 70px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.validation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.validation-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.validation-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
}

.card-ribbon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 8px 20px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-header {
  padding: 24px 24px 16px;
  border-bottom: 2px solid var(--gray-100);
}

.card-header h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: var(--gray-900);
  font-weight: 700;
}

.project-code {
  font-size: 12px;
  color: var(--gray-500);
  font-family: monospace;
  font-weight: 600;
}

.card-body {
  padding: 24px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--gray-50);
  border-radius: 10px;
}

.info-icon {
  font-size: 24px;
}

.info-item div {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: var(--gray-600);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  color: var(--gray-900);
  font-weight: 600;
}

.description-box {
  background: var(--gray-50);
  padding: 16px;
  border-radius: 10px;
  border-left: 4px solid var(--primary-color);
}

.description-box h4 {
  font-size: 14px;
  margin-bottom: 10px;
  color: var(--gray-700);
  font-weight: 700;
}

.description-box p {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
  margin-bottom: 10px;
}

.btn-expand {
  background: none;
  border: none;
  color: var(--primary-color);
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: transform 0.3s;
}

.btn-expand:hover {
  transform: translateX(4px);
}

.card-actions {
  padding: 20px 24px;
  background: var(--gray-50);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-outline-danger {
  background: white;
  border: 2px solid var(--danger-color);
  color: var(--danger-color);
}

.btn-outline-danger:hover {
  background: var(--danger-color);
  color: white;
}

.detail-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
}

.detail-card h3 {
  font-size: 24px;
  margin-bottom: 8px;
}

.detail-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 2px solid var(--gray-100);
}

.detail-section:first-of-type {
  border-top: none;
  padding-top: 0;
}

.detail-section h4 {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--gray-700);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-section p {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
  margin-bottom: 8px;
}

.budget-amount {
  font-size: 28px;
  font-weight: 800;
  color: var(--success-color);
  margin: 0;
}

@media (max-width: 768px) {
  .validation-grid {
    grid-template-columns: 1fr;
  }
}
</style>
