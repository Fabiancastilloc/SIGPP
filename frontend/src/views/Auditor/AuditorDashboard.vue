<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header auditor-header">
        <div>
          <h1>🔍 Panel de Auditoría</h1>
          <p>Monitoreo y auditoría de proyectos</p>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card card-blue">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Total Proyectos</div>
          </div>
        </div>
        
        <div class="stat-card card-green">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Activos</div>
          </div>
        </div>
        
        <div class="stat-card card-orange">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <div class="stat-value">{{ auditLogs }}</div>
            <div class="stat-label">Registros de Auditoría</div>
          </div>
        </div>
        
        <div class="stat-card card-purple">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-value">${{ formatMoney(totalBudget) }}</div>
            <div class="stat-label">Presupuesto Total</div>
          </div>
        </div>
      </div>

      <div class="controls-bar">
        <div class="filter-buttons">
          <button 
            @click="currentFilter = 'all'" 
            :class="['filter-btn', { active: currentFilter === 'all' }]"
          >
            Todos
          </button>
          <button 
            @click="currentFilter = 'activo'" 
            :class="['filter-btn', { active: currentFilter === 'activo' }]"
          >
            Activos
          </button>
          <button 
            @click="currentFilter = 'finalizado'" 
            :class="['filter-btn', { active: currentFilter === 'finalizado' }]"
          >
            Finalizados
          </button>
        </div>
        
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="🔍 Buscar proyectos..."
          class="search-input"
        />
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <div v-else class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <div class="card-status" :class="getStatusClass(project.estado)">
            {{ getStatusText(project.estado) }}
          </div>
          
          <div class="card-body">
            <h3>{{ project.nombre }}</h3>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
            
            <p class="project-desc">{{ truncate(project.descripcion, 120) }}</p>
            
            <div class="project-info">
              <div class="info-row">
                <span class="info-icon">👨‍🎓</span>
                <span>{{ project.estudiante.nombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">💰</span>
                <span>${{ formatMoney(project.presupuesto_estimado) }}</span>
              </div>
            </div>
            
            <div v-if="project.presupuesto_asignado" class="budget-bar">
              <div class="budget-label">
                <span>Ejecución</span>
                <span>{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"
                ></div>
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="btn-action btn-view">
              👁️ Ver Detalles
            </button>
            <button @click="viewAudit(project.id)" class="btn-action btn-audit">
              📋 Ver Auditoría
            </button>
          </div>
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
  name: 'AuditorDashboard',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    
    const totalProjects = computed(() => projects.value.length)
    const activeProjects = computed(() => projects.value.filter(p => p.estado === 'activo').length)
    const auditLogs = computed(() => totalProjects.value * 5)
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
          p.codigo_proyecto.toLowerCase().includes(query)
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
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (id) => router.push(`/auditor/project/${id}`)
    const viewAudit = (id) => router.push(`/auditor/project/${id}/audit`)
    
    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'finalizado': 'status-finished'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'activo': '✅ Activo',
        'finalizado': '🏁 Finalizado'
      }
      return texts[estado] || estado
    }
    
    const truncate = (text, len) => text.length > len ? text.substring(0, len) + '...' : text
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const calculatePercentage = (executed, total) => {
      if (!total) return 0
      return Math.round((executed / total) * 100)
    }
    
    onMounted(() => loadProjects())
    
    return {
      projects, loading, currentFilter, searchQuery,
      totalProjects, activeProjects, auditLogs, totalBudget, filteredProjects,
      viewProject, viewAudit, getStatusClass, getStatusText,
      truncate, formatMoney, calculatePercentage
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  padding: 40px;
  border-radius: 20px;
  margin-bottom: 40px;
  color: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.auditor-header {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.dashboard-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.dashboard-header p {
  opacity: 0.95;
  font-size: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.card-blue { border-color: #3b82f6; }
.card-green { border-color: #10b981; }
.card-orange { border-color: #f59e0b; }
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
  border-color: #f59e0b;
}

.filter-btn.active {
  background: #f59e0b;
  border-color: #f59e0b;
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
  border-color: #f59e0b;
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
  border: 2px solid var(--gray-200);
  transition: all 0.3s;
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: #f59e0b;
}

.card-status {
  padding: 10px;
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
}

.status-active { background: #d1fae5; color: #065f46; }
.status-finished { background: #dbeafe; color: #1e40af; }

.card-body {
  padding: 24px;
}

.card-body h3 {
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
  font-size: 14px;
  color: var(--gray-700);
  font-weight: 500;
}

.info-icon {
  font-size: 18px;
}

.budget-bar {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 2px solid var(--gray-200);
}

.budget-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  transition: width 0.5s;
}

.card-actions {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: var(--gray-50);
  border-top: 2px solid var(--gray-200);
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

.btn-audit {
  background: #fef3c7;
  color: #92400e;
  border: 2px solid #f59e0b;
}

.btn-audit:hover {
  background: #fde68a;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #f59e0b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
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
