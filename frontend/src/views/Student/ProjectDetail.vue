<template>
  <div class="project-detail-page">
    <div class="container">
      <router-link :to="getBackRoute()" class="btn-back">← Volver</router-link>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando detalles del proyecto...</p>
      </div>

      <div v-else-if="project" class="detail-wrapper">
        <div class="project-header">
          <div class="header-top">
            <div>
              <span class="project-code">{{ project.codigo_proyecto }}</span>
              <h1>{{ project.nombre }}</h1>
            </div>
            <span :class="['status-badge', getStatusClass(project.estado)]">
              {{ getStatusText(project.estado) }}
            </span>
          </div>
          
          <div class="header-actions">
            <button v-if="canSubmit" @click="submitProject" class="btn btn-primary">
              📤 Enviar a Revisión
            </button>
            
            <button v-if="canEdit" @click="editProject" class="btn btn-secondary">
              ✏️ Editar
            </button>
            
            <button v-if="canDelete" @click="confirmDelete" class="btn btn-danger">
              🗑️ Eliminar
            </button>
            
            <button v-if="isActive" @click="manageExpenses" class="btn btn-success">
              💳 Gestionar Gastos
            </button>
          </div>
        </div>

        <div class="content-grid">
          <div class="main-content">
            <div class="content-card">
              <h3>📝 Descripción del Proyecto</h3>
              <p>{{ project.descripcion }}</p>
            </div>

            <div class="content-card">
              <h3>🎯 Objetivos</h3>
              <p>{{ project.objetivos }}</p>
            </div>

            <div class="content-card">
              <h3>💰 Información Presupuestal</h3>
              <div class="budget-grid">
                <div class="budget-item">
                  <span class="label">Estimado:</span>
                  <span class="value">${{ formatMoney(project.presupuesto_estimado) }}</span>
                </div>
                <div v-if="project.presupuesto_asignado" class="budget-item">
                  <span class="label">Asignado:</span>
                  <span class="value assigned">${{ formatMoney(project.presupuesto_asignado) }}</span>
                </div>
                <div v-if="project.presupuesto_ejecutado" class="budget-item">
                  <span class="label">Ejecutado:</span>
                  <span class="value executed">${{ formatMoney(project.presupuesto_ejecutado) }}</span>
                </div>
                <div v-if="project.presupuesto_asignado" class="budget-item">
                  <span class="label">Disponible:</span>
                  <span class="value available">
                    ${{ formatMoney(project.presupuesto_asignado - project.presupuesto_ejecutado) }}
                  </span>
                </div>
              </div>

              <div v-if="project.presupuesto_asignado" class="budget-progress">
                <div class="progress-info">
                  <span>Ejecución</span>
                  <span>{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"></div>
                </div>
              </div>
            </div>

            <div v-if="project.comentarios_profesor" class="content-card comment-card professor">
              <h3>💬 Comentarios del Profesor</h3>
              <p>{{ project.comentarios_profesor }}</p>
            </div>

            <div v-if="project.comentarios_financiera" class="content-card comment-card finance">
              <h3>💼 Comentarios de Financiera</h3>
              <p>{{ project.comentarios_financiera }}</p>
            </div>
          </div>

          <div class="sidebar">
            <div class="sidebar-card">
              <h3>👨‍🏫 Profesor Asesor</h3>
              <div class="person-card">
                <div class="person-avatar">{{ getInitials(project.profesor.nombre) }}</div>
                <div class="person-info">
                  <strong>{{ project.profesor.nombre }}</strong>
                  <span>{{ project.profesor.email }}</span>
                </div>
              </div>
            </div>

            <div class="sidebar-card">
              <h3>👨‍🎓 Estudiante Líder</h3>
              <div class="person-card">
                <div class="person-avatar student">{{ getInitials(project.estudiante.nombre) }}</div>
                <div class="person-info">
                  <strong>{{ project.estudiante.nombre }}</strong>
                  <span>{{ project.estudiante.email }}</span>
                </div>
              </div>
            </div>

            <div class="sidebar-card">
              <h3>📋 Información</h3>
              <div class="info-list">
                <div class="info-item">
                  <span class="icon">📅</span>
                  <div>
                    <span class="label">Creado</span>
                    <span class="value">{{ formatDate(project.created_at) }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <span class="icon">🔄</span>
                  <div>
                    <span class="label">Actualizado</span>
                    <span class="value">{{ formatDate(project.updated_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
      <div class="modal-box" @click.stop>
        <div class="modal-header danger">
          <h2>⚠️ Confirmar Eliminación</h2>
          <button @click="cancelDelete" class="close-btn">×</button>
        </div>
        
        <div class="modal-content">
          <div class="warning-box">
            <p><strong>¿Estás seguro de eliminar este proyecto?</strong></p>
            <p>Proyecto: <strong>{{ project.nombre }}</strong></p>
            <p>Código: <strong>{{ project.codigo_proyecto }}</strong></p>
          </div>
          
          <div class="alert-danger">
            <span>⚠️</span>
            <p>Esta acción no se puede deshacer. Todos los datos asociados se eliminarán permanentemente.</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="cancelDelete" class="btn-modal btn-cancel">Cancelar</button>
          <button @click="deleteProject" class="btn-modal btn-delete" :disabled="deleting">
            {{ deleting ? '⏳ Eliminando...' : '🗑️ Eliminar Proyecto' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../store'
import projectsApi from '../../api/projects'

export default {
  name: 'ProjectDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const project = ref(null)
    const loading = ref(true)
    const showDeleteModal = ref(false)
    const deleting = ref(false)
    
    const projectId = computed(() => parseInt(route.params.id))
    const userRole = computed(() => authStore.user?.rol)
    const userId = computed(() => authStore.user?.id)
    
    const isOwner = computed(() => project.value?.estudiante.id === userId.value)
    const isActive = computed(() => project.value?.estado === 'activo')
    const isDraft = computed(() => project.value?.estado === 'borrador')
    
    const canSubmit = computed(() => userRole.value === 'estudiante' && isOwner.value && isDraft.value)
    const canEdit = computed(() => userRole.value === 'estudiante' && isOwner.value && isDraft.value)
    const canDelete = computed(() => userRole.value === 'estudiante' && isOwner.value && isDraft.value)
    
    const loadProject = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjectById(projectId.value)
        project.value = response.data
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar proyecto')
        router.push(getBackRoute())
      } finally {
        loading.value = false
      }
    }
    
    const getBackRoute = () => {
      const routes = {
        'estudiante': '/student',
        'profesor': '/professor',
        'financiera': '/finance',
        'auditor': '/auditor',
        'superusuario': '/admin'
      }
      return routes[userRole.value] || '/'
    }
    
    const submitProject = async () => {
      if (!confirm('¿Enviar proyecto para revisión del profesor?')) return
      try {
        await projectsApi.submitProject(projectId.value)
        alert('✅ Proyecto enviado exitosamente')
        loadProject()
      } catch (err) {
        alert('Error al enviar proyecto')
      }
    }
    
    const editProject = () => router.push(`/student/edit-project/${projectId.value}`)
    const manageExpenses = () => router.push(`/student/project/${projectId.value}/expenses`)
    const confirmDelete = () => { showDeleteModal.value = true }
    const cancelDelete = () => { showDeleteModal.value = false }
    
    const deleteProject = async () => {
      deleting.value = true
      try {
        await projectsApi.deleteProject(projectId.value)
        alert('✅ Proyecto eliminado exitosamente')
        router.push(getBackRoute())
      } catch (err) {
        alert('❌ Error al eliminar proyecto')
      } finally {
        deleting.value = false
        showDeleteModal.value = false
      }
    }
    
    const getStatusClass = (estado) => {
      const classes = {
        'borrador': 'status-draft',
        'pendiente_profesor': 'status-pending',
        'pendiente_financiera': 'status-review',
        'activo': 'status-active',
        'rechazado': 'status-rejected'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'borrador': '📝 Borrador',
        'pendiente_profesor': '⏳ En Revisión (Profesor)',
        'pendiente_financiera': '💼 En Revisión (Financiera)',
        'activo': '✅ Activo',
        'rechazado': '❌ Rechazado'
      }
      return texts[estado] || estado
    }
    
    const getInitials = (name) => name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric' })
    const calculatePercentage = (executed, total) => {
      if (!total) return 0
      return Math.round((executed / total) * 100)
    }
    
    onMounted(() => loadProject())
    
    return {
      project, loading, showDeleteModal, deleting,
      canSubmit, canEdit, canDelete, isActive,
      getBackRoute, submitProject, editProject, manageExpenses,
      confirmDelete, cancelDelete, deleteProject,
      getStatusClass, getStatusText, getInitials,
      formatMoney, formatDate, calculatePercentage
    }
  }
}
</script>

<style scoped>
.project-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.btn-back {
  display: inline-block;
  padding: 12px 24px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid var(--gray-200);
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateX(-4px);
  border-color: #667eea;
}

.detail-wrapper {
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.project-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 24px;
}

.project-code {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 12px;
}

.project-header h1 {
  font-size: 32px;
  margin: 0;
  color: white;
}

.status-badge {
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

.status-draft { background: #fef3c7; color: #92400e; }
.status-pending { background: #dbeafe; color: #1e40af; }
.status-review { background: #e0e7ff; color: #3730a3; }
.status-active { background: #d1fae5; color: #065f46; }
.status-rejected { background: #fee2e2; color: #991b1b; }

.header-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-primary { background: white; color: #667eea; }
.btn-secondary { background: rgba(255, 255, 255, 0.2); color: white; }
.btn-danger { background: #ef4444; color: white; }
.btn-success { background: #10b981; color: white; }

.btn:hover { transform: translateY(-2px); }

.content-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
  padding: 40px;
}

.content-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  border: 2px solid var(--gray-200);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.content-card h3 {
  font-size: 18px;
  margin-bottom: 16px;
  color: var(--gray-900);
}

.content-card p {
  line-height: 1.7;
  color: var(--gray-700);
  margin: 0;
}

.comment-card {
  border-left: 4px solid;
}

.comment-card.professor {
  background: #dbeafe;
  border-color: #3b82f6;
}

.comment-card.finance {
  background: #d1fae5;
  border-color: #10b981;
}

.budget-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.budget-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px;
  background: var(--gray-50);
  border-radius: 10px;
}

.budget-item .label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.budget-item .value {
  font-size: 20px;
  font-weight: 800;
  color: var(--gray-900);
}

.budget-item .assigned { color: #667eea; }
.budget-item .executed { color: #f59e0b; }
.budget-item .available { color: #10b981; }

.budget-progress {
  padding-top: 16px;
  border-top: 2px solid var(--gray-200);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
}

.progress-bar {
  height: 12px;
  background: var(--gray-200);
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.5s;
}

.sidebar-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 20px;
  border: 2px solid var(--gray-200);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.sidebar-card h3 {
  font-size: 16px;
  margin-bottom: 16px;
  color: var(--gray-900);
}

.person-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--gray-50);
  border-radius: 12px;
}

.person-avatar {
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

.person-avatar.student {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.person-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.person-info strong {
  font-size: 15px;
  color: var(--gray-900);
}

.person-info span {
  font-size: 13px;
  color: var(--gray-600);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: start;
  gap: 12px;
  padding: 12px;
  background: var(--gray-50);
  border-radius: 10px;
}

.info-item .icon {
  font-size: 20px;
}

.info-item div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 11px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.info-item .value {
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-900);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.modal-box {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 24px;
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header.danger {
  background: #fee2e2;
  border-color: #ef4444;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #991b1b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: var(--gray-500);
  line-height: 1;
  padding: 0;
}

.modal-content {
  padding: 24px;
}

.warning-box {
  padding: 20px;
  background: var(--gray-50);
  border-radius: 12px;
  margin-bottom: 16px;
}

.warning-box p {
  margin-bottom: 8px;
}

.alert-danger {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fee2e2;
  border: 2px solid #ef4444;
  border-radius: 12px;
  color: #991b1b;
}

.alert-danger span {
  font-size: 24px;
}

.alert-danger p {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 2px solid var(--gray-200);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-modal {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-cancel {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .header-top {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
