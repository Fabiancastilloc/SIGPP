<template>
  <div class="finance-dashboard">
    <div class="container">
      <!-- Header -->
      <div class="dashboard-header">
        <div>
          <h1>💼 Panel Financiero</h1>
          <p>Gestiona la asignación de presupuestos para proyectos aprobados</p>
        </div>
        <div class="header-stats">
          <div class="mini-stat">
            <span class="stat-num">{{ pendingCount }}</span>
            <span class="stat-txt">Por Aprobar</span>
          </div>
          <div class="mini-stat">
            <span class="stat-num">${{ formatMillions(totalBudget) }}M</span>
            <span class="stat-txt">Presupuesto Total</span>
          </div>
        </div>
      </div>

      <!-- Estadísticas -->
      <div class="stats-grid">
        <div class="stat-card card-blue">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Total Proyectos</div>
          </div>
        </div>
        
        <div class="stat-card card-orange">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">Pendientes</div>
          </div>
        </div>
        
        <div class="stat-card card-green">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-value">{{ approvedCount }}</div>
            <div class="stat-label">Aprobados</div>
          </div>
        </div>
        
        <div class="stat-card card-purple">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-value">${{ formatMillions(totalBudget) }}M</div>
            <div class="stat-label">Presupuesto Total</div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="controls-bar">
        <div class="filter-buttons">
          <button 
            @click="currentFilter = 'all'" 
            :class="['filter-btn', { active: currentFilter === 'all' }]"
          >
            Todos
          </button>
          <button 
            @click="currentFilter = 'pendiente_financiera'" 
            :class="['filter-btn', { active: currentFilter === 'pendiente_financiera' }]"
          >
            Pendientes ({{ pendingCount }})
          </button>
          <button 
            @click="currentFilter = 'activo'" 
            :class="['filter-btn', { active: currentFilter === 'activo' }]"
          >
            Activos ({{ approvedCount }})
          </button>
        </div>
        
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="🔍 Buscar proyectos..."
          class="search-input"
        />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredProjects.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <h3>{{ searchQuery ? 'No hay resultados' : 'No hay proyectos' }}</h3>
        <p>{{ searchQuery ? 'Intenta otra búsqueda' : 'Los proyectos validados aparecerán aquí' }}</p>
      </div>

      <!-- Grid de Proyectos -->
      <div v-else class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <div class="card-status" :class="getStatusClass(project.estado)">
            {{ getStatusText(project.estado) }}
          </div>
          
          <div class="card-body">
            <h3 class="project-title">{{ project.nombre }}</h3>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
            
            <p class="project-desc">{{ truncate(project.descripcion, 120) }}</p>
            
            <div class="project-info">
              <div class="info-row">
                <span class="info-icon">👨‍🎓</span>
                <span>{{ project.estudiante.nombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">👨‍🏫</span>
                <span>{{ project.profesor.nombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">💰</span>
                <span>Estimado: ${{ formatMoney(project.presupuesto_estimado) }}</span>
              </div>
              <div v-if="project.presupuesto_asignado" class="info-row">
                <span class="info-icon">✅</span>
                <span>Asignado: ${{ formatMoney(project.presupuesto_asignado) }}</span>
              </div>
            </div>
            
            <div v-if="project.comentarios_financiera" class="has-comments">
              💬 Ya comentaste este proyecto
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="btn-action btn-view">
              👁️ Ver
            </button>
            <button 
              v-if="project.estado === 'pendiente_financiera'"
              @click="openActivationModal(project, false)" 
              class="btn-action btn-return"
            >
              ↩️ Devolver
            </button>
            <button 
              v-if="project.estado === 'pendiente_financiera'"
              @click="openActivationModal(project, true)" 
              class="btn-action btn-activate"
            >
              ✅ Activar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Activación/Devolución -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-box" @click.stop>
        <div class="modal-header">
          <h2>{{ activationMode ? '✅ Activar Proyecto' : '↩️ Devolver Proyecto' }}</h2>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        
        <div class="modal-content">
          <div class="modal-project-info">
            <strong>{{ selectedProject.nombre }}</strong>
            <p>Estudiante: {{ selectedProject.estudiante.nombre }}</p>
            <p>Profesor: {{ selectedProject.profesor.nombre }}</p>
            <p>Presupuesto Estimado: ${{ formatMoney(selectedProject.presupuesto_estimado) }}</p>
          </div>
          
          <div v-if="activationMode" class="form-field">
            <label>Presupuesto a Asignar * (COP)</label>
            <input 
              v-model.number="presupuestoAsignado"
              type="number"
              :min="0"
              :max="selectedProject.presupuesto_estimado"
              step="100000"
              placeholder="5000000"
            />
            <small>Máximo: ${{ formatMoney(selectedProject.presupuesto_estimado) }}</small>
          </div>
          
          <div class="form-field">
            <label>Comentarios {{ activationMode ? '(Opcional)' : '* Requerido' }}</label>
            <textarea 
              v-model="comentarios" 
              rows="5"
              :placeholder="activationMode 
                ? 'Recomendaciones sobre el presupuesto...' 
                : 'Explica por qué se devuelve...'"
            ></textarea>
            <small>{{ comentarios.length }}/500</small>
          </div>

          <div v-if="!activationMode" class="modal-alert warning">
            ⚠️ El proyecto volverá al estudiante
          </div>
          
          <div v-if="activationMode" class="modal-alert success">
            ✅ El proyecto será activado con el presupuesto asignado
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeModal" class="btn-modal btn-cancel">Cancelar</button>
          <button 
            @click="confirmActivation" 
            :class="['btn-modal', activationMode ? 'btn-confirm' : 'btn-danger']"
            :disabled="processing || (!activationMode && !comentarios.trim()) || (activationMode && !presupuestoAsignado)"
          >
            {{ processing ? '⏳ Procesando...' : (activationMode ? '✅ Activar' : '↩️ Devolver') }}
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
  name: 'FinanceDashboard',
  setup() {
    const router = useRouter()
    
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    const showModal = ref(false)
    const selectedProject = ref(null)
    const activationMode = ref(true)
    const presupuestoAsignado = ref(null)
    const comentarios = ref('')
    const processing = ref(false)
    
    const totalProjects = computed(() => projects.value.length)
    const pendingCount = computed(() => projects.value.filter(p => p.estado === 'pendiente_financiera').length)
    const approvedCount = computed(() => projects.value.filter(p => p.estado === 'activo').length)
    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + p.presupuesto_asignado, 0)
    })
    
    const filteredProjects = computed(() => {
      let filtered = projects.value
      
      if (currentFilter.value !== 'all') {
        filtered = filtered.filter(p => p.estado === currentFilter.value)
      }
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query) ||
          p.estudiante.nombre.toLowerCase().includes(query)
        )
      }
      
      return filtered
    })
    
    const loadProjects = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjects()
        projects.value = response.data
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar proyectos')
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (projectId) => {
      router.push(`/finance/project/${projectId}`)
    }
    
    const openActivationModal = (project, approve) => {
      selectedProject.value = project
      activationMode.value = approve
      presupuestoAsignado.value = approve ? project.presupuesto_estimado : null
      comentarios.value = ''
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
      selectedProject.value = null
      presupuestoAsignado.value = null
      comentarios.value = ''
    }
    
    const confirmActivation = async () => {
      if (!activationMode.value && !comentarios.value.trim()) {
        alert('Debes agregar comentarios')
        return
      }
      
      if (activationMode.value && !presupuestoAsignado.value) {
        alert('Debes asignar un presupuesto')
        return
      }
      
      processing.value = true
      try {
        await projectsApi.activateProject(selectedProject.value.id, {
          aprobado: activationMode.value,
          presupuesto_asignado: presupuestoAsignado.value,
          comentarios: comentarios.value
        })
        
        alert(activationMode.value ? '✅ Proyecto activado' : '↩️ Proyecto devuelto')
        closeModal()
        loadProjects()
      } catch (err) {
        alert('Error al procesar')
      } finally {
        processing.value = false
      }
    }
    
    const getStatusClass = (estado) => {
      const classes = {
        'pendiente_financiera': 'status-pending',
        'activo': 'status-active'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'pendiente_financiera': '⏳ Pendiente',
        'activo': '✅ Activo'
      }
      return texts[estado] || estado
    }
    
    const truncate = (text, len) => text.length > len ? text.substring(0, len) + '...' : text
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatMillions = (val) => (val / 1000000).toFixed(1)
    
    onMounted(() => loadProjects())
    
    return {
      projects, loading, currentFilter, searchQuery,
      totalProjects, pendingCount, approvedCount, totalBudget, filteredProjects,
      showModal, selectedProject, activationMode, presupuestoAsignado, comentarios, processing,
      viewProject, openActivationModal, closeModal, confirmActivation,
      getStatusClass, getStatusText, truncate, formatMoney, formatMillions
    }
  }
}
</script>

<style scoped>
.finance-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding: 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  border-radius: 20px;
  color: white;
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
}

.dashboard-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.dashboard-header p {
  opacity: 0.95;
  font-size: 16px;
}

.header-stats {
  display: flex;
  gap: 20px;
}

.mini-stat {
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  text-align: center;
  backdrop-filter: blur(10px);
}

.stat-num {
  display: block;
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-txt {
  font-size: 12px;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 28px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.card-blue { border-color: #3b82f6; }
.card-orange { border-color: #f59e0b; }
.card-green { border-color: #10b981; }
.card-purple { border-color: #8b5cf6; }

.stat-icon {
  font-size: 48px;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  color: var(--gray-900);
}

.stat-label {
  font-size: 14px;
  color: var(--gray-600);
  font-weight: 600;
  margin-top: 4px;
}

.controls-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 32px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.filter-btn:hover {
  border-color: #8b5cf6;
}

.filter-btn.active {
  background: #8b5cf6;
  border-color: #8b5cf6;
  color: white;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 10px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #8b5cf6;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.project-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: #8b5cf6;
}

.card-status {
  padding: 10px;
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
}

.status-pending { background: #fef3c7; color: #92400e; }
.status-active { background: #d1fae5; color: #065f46; }

.card-body {
  padding: 24px;
}

.project-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
  color: var(--gray-900);
}

.project-code {
  font-size: 12px;
  color: var(--gray-500);
  font-family: monospace;
  font-weight: 600;
}

.project-desc {
  margin: 16px 0;
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 16px 0;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gray-700);
  font-weight: 500;
}

.info-icon {
  font-size: 16px;
}

.has-comments {
  padding: 10px;
  background: #dbeafe;
  border-radius: 8px;
  font-size: 13px;
  color: #1e40af;
  font-weight: 600;
  margin-top: 12px;
}

.card-actions {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: var(--gray-50);
  border-top: 2px solid var(--gray-100);
}

.btn-action {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-view {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-view:hover {
  background: var(--gray-300);
}

.btn-return {
  background: #fef3c7;
  color: #92400e;
}

.btn-return:hover {
  background: #fde68a;
}

.btn-activate {
  background: #8b5cf6;
  color: white;
}

.btn-activate:hover {
  background: #7c3aed;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
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
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 24px;
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 20px;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: var(--gray-500);
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
}

.modal-content {
  padding: 24px;
}

.modal-project-info {
  padding: 16px;
  background: var(--gray-50);
  border-radius: 12px;
  margin-bottom: 20px;
}

.modal-project-info strong {
  display: block;
  margin-bottom: 8px;
  font-size: 16px;
}

.modal-project-info p {
  margin: 4px 0;
  font-size: 14px;
  color: var(--gray-600);
}

.form-field {
  margin-bottom: 20px;
}

.form-field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 14px;
}

.form-field input,
.form-field textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-family: inherit;
  font-size: 14px;
}

.form-field textarea {
  resize: vertical;
}

.form-field input:focus,
.form-field textarea:focus {
  outline: none;
  border-color: #8b5cf6;
}

.form-field small {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--gray-600);
}

.modal-alert {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  margin-top: 16px;
}

.modal-alert.warning {
  background: #fef3c7;
  color: #92400e;
}

.modal-alert.success {
  background: #d1fae5;
  color: #065f46;
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

.btn-cancel:hover {
  background: var(--gray-300);
}

.btn-confirm {
  background: #8b5cf6;
  color: white;
}

.btn-confirm:hover {
  background: #7c3aed;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

.btn-modal:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>
