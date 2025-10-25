<template>
  <div class="activate-page">
    <div class="container">
      <div class="page-header">
        <router-link to="/finance" class="btn-back">
          ← Volver al Dashboard
        </router-link>
        <h1>💼 Activar Proyectos</h1>
        <p>Aprueba presupuestos y activa proyectos validados académicamente</p>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <div v-else-if="pendingProjects.length === 0" class="empty-state">
        <div class="empty-icon">✅</div>
        <h3>No hay proyectos pendientes de aprobación</h3>
        <p>Los proyectos aparecerán aquí después de la validación académica</p>
      </div>

      <div v-else class="projects-table-container">
        <table class="projects-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Proyecto</th>
              <th>Estudiante</th>
              <th>Profesor</th>
              <th>Presupuesto Solicitado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in pendingProjects" :key="project.id">
              <td class="code-column">
                <span class="project-code-badge">{{ project.codigo_proyecto }}</span>
              </td>
              <td class="name-column">
                <strong>{{ project.nombre }}</strong>
              </td>
              <td>{{ project.estudiante.nombre }}</td>
              <td>{{ project.profesor.nombre }}</td>
              <td class="budget-column">
                <span class="budget-amount">${{ formatMoney(project.presupuesto_estimado) }}</span>
              </td>
              <td class="actions-column">
                <button 
                  @click="openApprovalModal(project)" 
                  class="btn btn-sm btn-primary"
                >
                  💼 Revisar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de Aprobación -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content modal-xlarge" @click.stop>
        <div class="modal-header">
          <h2>💼 Revisión Financiera de Proyecto</h2>
          <button @click="closeModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="approval-container">
            <!-- Panel Izquierdo: Información del Proyecto -->
            <div class="info-panel">
              <div class="project-header-modal">
                <h3>{{ selectedProject.nombre }}</h3>
                <span class="project-code-modal">{{ selectedProject.codigo_proyecto }}</span>
              </div>

              <div class="info-grid">
                <div class="info-box">
                  <span class="info-icon">👨‍🎓</span>
                  <div>
                    <span class="info-label">Estudiante</span>
                    <span class="info-value">{{ selectedProject.estudiante.nombre }}</span>
                    <span class="info-extra">{{ selectedProject.estudiante.email }}</span>
                  </div>
                </div>

                <div class="info-box">
                  <span class="info-icon">👨‍🏫</span>
                  <div>
                    <span class="info-label">Profesor Asesor</span>
                    <span class="info-value">{{ selectedProject.profesor.nombre }}</span>
                    <span class="info-extra">{{ selectedProject.profesor.email }}</span>
                  </div>
                </div>
              </div>

              <div class="content-section">
                <h4>📝 Descripción</h4>
                <p>{{ selectedProject.descripcion }}</p>
              </div>

              <div class="content-section">
                <h4>🎯 Objetivos</h4>
                <p>{{ selectedProject.objetivos }}</p>
              </div>

              <div v-if="selectedProject.comentarios_profesor" class="comment-section">
                <h4>💬 Comentarios del Profesor</h4>
                <p>{{ selectedProject.comentarios_profesor }}</p>
              </div>
            </div>

            <!-- Panel Derecho: Formulario de Aprobación -->
            <div class="approval-panel">
              <div class="budget-summary">
                <h4>💰 Resumen Presupuestal</h4>
                <div class="budget-item">
                  <span>Presupuesto Solicitado:</span>
                  <span class="budget-value">${{ formatMoney(selectedProject.presupuesto_estimado) }}</span>
                </div>
              </div>

              <div class="approval-form">
                <div class="form-group">
                  <label class="form-label">Presupuesto a Asignar *</label>
                  <div class="input-group">
                    <span class="input-prefix">$</span>
                    <input 
                      v-model.number="presupuestoAsignado" 
                      type="number" 
                      class="form-control form-control-large" 
                      :placeholder="selectedProject.presupuesto_estimado"
                      min="0"
                      step="100000"
                      required 
                    />
                  </div>
                  <div class="budget-validation">
                    <span v-if="presupuestoAsignado > selectedProject.presupuesto_estimado" class="validation-warning">
                      ⚠️ Mayor al solicitado
                    </span>
                    <span v-else-if="presupuestoAsignado < selectedProject.presupuesto_estimado" class="validation-info">
                      ℹ️ Menor al solicitado
                    </span>
                    <span v-else-if="presupuestoAsignado === selectedProject.presupuesto_estimado" class="validation-success">
                      ✅ Igual al solicitado
                    </span>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">Observaciones</label>
                  <textarea 
                    v-model="comentarios" 
                    class="form-control" 
                    rows="4"
                    placeholder="Añade observaciones sobre el presupuesto asignado (opcional)..."
                  ></textarea>
                </div>
              </div>

              <div class="action-buttons">
                <button 
                  @click="rejectProject" 
                  class="btn btn-danger btn-lg btn-block"
                  :disabled="processing"
                >
                  ❌ Rechazar Proyecto
                </button>
                <button 
                  @click="approveProject" 
                  class="btn btn-success btn-lg btn-block"
                  :disabled="processing || !presupuestoAsignado || presupuestoAsignado <= 0"
                >
                  <span v-if="!processing">✅ Aprobar y Activar</span>
                  <span v-else>⏳ Procesando...</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import projectsApi from '../../api/projects'

export default {
  name: 'ActivateProjects',
  setup() {
    const projects = ref([])
    const loading = ref(true)
    const showModal = ref(false)
    const selectedProject = ref(null)
    const presupuestoAsignado = ref(null)
    const comentarios = ref('')
    const processing = ref(false)
    
    const pendingProjects = computed(() => 
      projects.value.filter(p => p.estado === 'pendiente_financiera')
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
    
    const openApprovalModal = (project) => {
      selectedProject.value = project
      presupuestoAsignado.value = project.presupuesto_estimado
      comentarios.value = ''
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
      selectedProject.value = null
      presupuestoAsignado.value = null
      comentarios.value = ''
    }
    
    const approveProject = async () => {
      if (!presupuestoAsignado.value || presupuestoAsignado.value <= 0) {
        alert('Debes asignar un presupuesto válido')
        return
      }
      
      if (!confirm(`¿Aprobar proyecto con presupuesto de $${formatMoney(presupuestoAsignado.value)}?`)) {
        return
      }
      
      processing.value = true
      try {
        await projectsApi.activateProject(selectedProject.value.id, {
          aprobado: true,
          presupuesto_asignado: presupuestoAsignado.value,
          comentarios: comentarios.value
        })
        alert('✅ Proyecto aprobado y activado exitosamente')
        closeModal()
        loadProjects()
      } catch (err) {
        alert('Error al aprobar proyecto')
      } finally {
        processing.value = false
      }
    }
    
    const rejectProject = async () => {
      if (!confirm('¿Estás seguro de rechazar este proyecto? Esta acción es definitiva.')) {
        return
      }
      
      processing.value = true
      try {
        await projectsApi.activateProject(selectedProject.value.id, {
          aprobado: false,
          comentarios: comentarios.value || 'Proyecto rechazado por financiera'
        })
        alert('❌ Proyecto rechazado')
        closeModal()
        loadProjects()
      } catch (err) {
        alert('Error al rechazar proyecto')
      } finally {
        processing.value = false
      }
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
      showModal,
      selectedProject,
      presupuestoAsignado,
      comentarios,
      processing,
      openApprovalModal,
      closeModal,
      approveProject,
      rejectProject,
      formatMoney
    }
  }
}
</script>

<style scoped>
.activate-page {
  padding: 30px 0;
  min-height: calc(100vh - 70px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.projects-table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.projects-table {
  width: 100%;
  border-collapse: collapse;
}

.projects-table thead {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.projects-table th {
  padding: 18px 16px;
  text-align: left;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.projects-table td {
  padding: 18px 16px;
  border-bottom: 1px solid var(--gray-200);
}

.projects-table tbody tr {
  transition: background 0.3s;
}

.projects-table tbody tr:hover {
  background: var(--gray-50);
}

.project-code-badge {
  padding: 6px 12px;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  border-radius: 6px;
  font-family: monospace;
  font-weight: 700;
  font-size: 12px;
  color: #1e40af;
}

.name-column strong {
  color: var(--gray-900);
  font-weight: 600;
}

.budget-column {
  font-weight: 700;
}

.budget-amount {
  color: var(--success-color);
  font-size: 16px;
}

.actions-column {
  text-align: center;
}

.modal-xlarge {
  max-width: 1200px;
  width: 95%;
}

.approval-container {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
}

.info-panel {
  padding: 24px;
  background: var(--gray-50);
  border-radius: 12px;
}

.project-header-modal h3 {
  font-size: 22px;
  margin-bottom: 8px;
  color: var(--gray-900);
}

.project-code-modal {
  font-size: 13px;
  color: var(--gray-500);
  font-family: monospace;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin: 24px 0;
}

.info-box {
  display: flex;
  align-items: start;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 10px;
  border: 1px solid var(--gray-200);
}

.info-box .info-icon {
  font-size: 28px;
}

.info-box div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.info-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--gray-600);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 15px;
  font-weight: 700;
  color: var(--gray-900);
}

.info-extra {
  font-size: 13px;
  color: var(--gray-600);
}

.content-section {
  margin-top: 20px;
}

.content-section h4 {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--gray-700);
}

.content-section p {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
}

.comment-section {
  margin-top: 20px;
  padding: 16px;
  background: white;
  border-left: 4px solid #3b82f6;
  border-radius: 8px;
}

.comment-section h4 {
  font-size: 14px;
  margin-bottom: 8px;
  color: #1e40af;
}

.comment-section p {
  font-size: 14px;
  color: #1e3a8a;
  line-height: 1.6;
  margin: 0;
}

.approval-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.budget-summary {
  padding: 20px;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border-radius: 12px;
  border: 2px solid #10b981;
}

.budget-summary h4 {
  font-size: 16px;
  margin-bottom: 16px;
  color: #065f46;
  font-weight: 700;
}

.budget-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #047857;
  font-weight: 600;
}

.budget-value {
  font-size: 24px;
  font-weight: 800;
  color: #059669;
}

.approval-form {
  padding: 24px;
  background: white;
  border-radius: 12px;
  border: 2px solid var(--primary-color);
}

.form-control-large {
  font-size: 18px;
  font-weight: 700;
  padding: 16px 16px 16px 40px;
}

.budget-validation {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 600;
}

.validation-warning {
  color: #f59e0b;
}

.validation-info {
  color: #3b82f6;
}

.validation-success {
  color: #10b981;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 1024px) {
  .approval-container {
    grid-template-columns: 1fr;
  }
  
  .projects-table-container {
    overflow-x: auto;
  }
}
</style>
