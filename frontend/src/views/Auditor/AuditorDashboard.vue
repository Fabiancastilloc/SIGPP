<template>
  <div class="auditor-dashboard">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Hero Header -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-greeting">
            <h1>
              Panel de Auditoría <span class="highlight">Integral</span>
            </h1>
            <p>Monitoreo, control y trazabilidad de proyectos en tiempo real</p>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card card-blue">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Total Proyectos</div>
          </div>
        </div>

        <div class="stat-card card-green">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Proyectos Activos</div>
          </div>
        </div>

        <div class="stat-card card-orange">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ auditLogs }}</div>
            <div class="stat-label">Registros de Auditoría</div>
          </div>
        </div>

        <div class="stat-card card-purple">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatMoneyShort(totalBudget) }}</div>
            <div class="stat-label">Presupuesto Auditado</div>
          </div>
        </div>
      </div>

      <!-- Filters & Search -->
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
        
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por nombre o código..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <!-- Card Header -->
          <div class="card-header" :class="getStatusClass(project.estado)">
            <div class="header-left">
              <span :class="['status-badge', getStatusClass(project.estado)]">
                {{ getStatusText(project.estado) }}
              </span>
              <span class="project-code">{{ project.codigo_proyecto }}</span>
            </div>
          </div>
          
          <!-- Card Body -->
          <div class="card-body">
            <h3 class="project-title">{{ project.nombre }}</h3>
            <p class="project-desc">{{ truncate(project.descripcion, 120) }}</p>
            
            <div class="project-info">
              <div class="info-row">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>{{ project.estudiante.nombre }}</span>
              </div>
              <div class="info-row">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ formatMoney(project.presupuesto_estimado) }}</span>
              </div>
            </div>
            
            <!-- Budget Progress Bar -->
            <div v-if="project.presupuesto_asignado" class="budget-section">
              <div class="budget-header">
                <span class="budget-label">Ejecución Presupuestal</span>
                <span class="budget-percent">{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :class="getProgressClass(project.presupuesto_ejecutado, project.presupuesto_asignado)"
                  :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"
                ></div>
              </div>
              <div class="budget-footer">
                <span>Gastado: {{ formatMoney(project.presupuesto_ejecutado) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Card Actions -->
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="action-btn btn-view">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Detalles
            </button>
            
            <!-- ✨ NUEVO: BOTÓN DE GASTOS -->
            <button 
              v-if="project.estado === 'activo' && project.presupuesto_asignado" 
              @click="viewExpenses(project.id)" 
              class="action-btn btn-expenses"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              Gastos
            </button>
            
            <button @click="viewAudit(project.id)" class="action-btn btn-audit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Auditoría
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
    const auditLogs = computed(() => totalProjects.value * 8 + 12) // Simulación de logs
    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + parseFloat(p.presupuesto_asignado || 0), 0)
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
    const viewExpenses = (id) => router.push(`/auditor/project/${id}/expenses`)
    
    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'finalizado': 'status-finished',
        'pendiente_financiera': 'status-pending'
      }
      return classes[estado] || 'status-pending'
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'activo': 'En Ejecución',
        'finalizado': 'Finalizado',
        'pendiente_financiera': 'En Revisión'
      }
      return texts[estado] || estado
    }

    const getProgressClass = (executed, total) => {
      const percent = calculatePercentage(executed, total)
      if (percent >= 90) return 'progress-danger'
      if (percent >= 70) return 'progress-warning'
      return 'progress-success'
    }
    
    const truncate = (text, len) => text.length > len ? text.substring(0, len) + '...' : text
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO', { 
      style: 'currency', 
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(val)

    const formatMoneyShort = (val) => new Intl.NumberFormat('es-CO', { 
      notation: "compact",
      compactDisplay: "short",
      style: 'currency', 
      currency: 'COP'
    }).format(val)
    
    const calculatePercentage = (executed, total) => {
      if (!total || total === 0) return 0
      return Math.round((parseFloat(executed || 0) / parseFloat(total)) * 100)
    }
    
    onMounted(() => loadProjects())
    
    return {
      projects, loading, currentFilter, searchQuery,
      totalProjects, activeProjects, auditLogs, totalBudget, filteredProjects,
      viewProject, viewAudit, viewExpenses,
      getStatusClass, getStatusText, getProgressClass,
      truncate, formatMoney, formatMoneyShort, calculatePercentage
    }
  }
}
</script>

<style scoped>
/* BASE */
.auditor-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  padding: 32px 16px;
  position: relative;
}

/* ANIMATED BACKGROUND */
.dashboard-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
}

.orb-1 { width: 600px; height: 600px; background: #3b82f6; top: -200px; left: -200px; }
.orb-2 { width: 500px; height: 500px; background: #10b981; bottom: -100px; right: -100px; }
.orb-3 { width: 400px; height: 400px; background: #f59e0b; top: 40%; left: 50%; }

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HERO SECTION */
.hero-section {
  margin-bottom: 40px;
  padding: 40px;
  background: rgba(30, 41, 59, 0.5);
  border: 2px solid #334155;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.hero-greeting h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.highlight { color: #f59e0b; }

.hero-greeting p {
  font-size: 16px;
  color: #cbd5e1;
  font-weight: 600;
}

/* STATS GRID */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #1e293b;
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 2px solid #334155;
  transition: transform 0.3s;
}

.stat-card:hover { transform: translateY(-4px); border-color: #f59e0b; }

.card-blue { border-left: 4px solid #3b82f6; }
.card-green { border-left: 4px solid #10b981; }
.card-orange { border-left: 4px solid #f59e0b; }
.card-purple { border-left: 4px solid #8b5cf6; }

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon { width: 32px; height: 32px; color: #cbd5e1; }
.card-blue .stat-icon { color: #3b82f6; }
.card-green .stat-icon { color: #10b981; }
.card-orange .stat-icon { color: #f59e0b; }
.card-purple .stat-icon { color: #8b5cf6; }

.stat-value { font-size: 28px; font-weight: 900; color: #ffffff; margin-bottom: 4px; }
.stat-label { font-size: 13px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }

/* CONTROLS */
.controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-buttons { display: flex; gap: 10px; }

.filter-btn {
  padding: 10px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #cbd5e1;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover, .filter-btn.active {
  background: #f59e0b;
  border-color: #f59e0b;
  color: #ffffff;
}

.search-box {
  position: relative;
  min-width: 300px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #ffffff;
  font-weight: 600;
}

.search-input:focus {
  outline: none;
  border-color: #f59e0b;
}

/* PROJECTS GRID */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.project-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: #f59e0b;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.card-header {
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 8px;
  margin-right: 10px;
}

.status-active { background: #10b981; color: #ffffff; }
.status-finished { background: #3b82f6; color: #ffffff; }
.status-pending { background: #f59e0b; color: #ffffff; }

.project-code {
  font-family: 'Courier New', monospace;
  color: #94a3b8;
  font-weight: 700;
  font-size: 13px;
}

.card-body { padding: 24px; }

.project-title {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
}

.project-desc {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 20px;
  line-height: 1.5;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #cbd5e1;
  font-size: 14px;
  font-weight: 600;
}

.info-icon { width: 18px; height: 18px; color: #f59e0b; }

/* BUDGET BAR */
.budget-section {
  padding-top: 16px;
  border-top: 2px solid #334155;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #cbd5e1;
}

.progress-bar {
  height: 8px;
  background: #334155;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.progress-success { background: #10b981; }
.progress-warning { background: #f59e0b; }
.progress-danger { background: #ef4444; }

.budget-footer {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
  text-align: right;
}

/* ACTIONS */
.card-actions {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-top: 2px solid #334155;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn svg { width: 16px; height: 16px; }

.btn-view { background: #334155; color: #ffffff; }
.btn-view:hover { background: #475569; }

.btn-expenses { background: #10b981; color: #ffffff; }
.btn-expenses:hover { background: #059669; }

.btn-audit { background: #f59e0b; color: #ffffff; }
.btn-audit:hover { background: #d97706; }

/* LOADING */
.loading-state { text-align: center; padding: 80px; }
.spinner {
  width: 50px; height: 50px; border: 4px solid #334155; border-top-color: #f59e0b;
  border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.loading-state p { color: #cbd5e1; }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .controls-bar { flex-direction: column; align-items: stretch; }
  .projects-grid { grid-template-columns: 1fr; }
}
</style>
