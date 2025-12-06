<template>
  <div class="admin-projects-page">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <router-link to="/admin" class="btn-back">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Volver al Panel
          </router-link>
          
          <div class="header-title">
            <h1>📊 Gestión de Proyectos</h1>
            <p>Control y supervisión de todos los proyectos del sistema</p>
          </div>
        </div>
      </div>

      <!-- Stats Summary -->
      <div class="stats-mini">
        <div class="stat-mini">
          <div class="stat-icon">📁</div>
          <div>
            <div class="stat-value">{{ projects.length }}</div>
            <div class="stat-label">Total</div>
          </div>
        </div>
        <div class="stat-mini">
          <div class="stat-icon">✅</div>
          <div>
            <div class="stat-value">{{ activeCount }}</div>
            <div class="stat-label">Activos</div>
          </div>
        </div>
        <div class="stat-mini">
          <div class="stat-icon">⏳</div>
          <div>
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">Pendientes</div>
          </div>
        </div>
        <div class="stat-mini">
          <div class="stat-icon">💰</div>
          <div>
            <div class="stat-value">{{ formatMoneyShort(totalBudget) }}</div>
            <div class="stat-label">Presupuesto</div>
          </div>
        </div>
      </div>

      <!-- Filters Bar -->
      <div class="filters-section">
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

        <select v-model="filterStatus" class="filter-select">
          <option value="">📋 Todos los estados</option>
          <option value="borrador">📝 Borrador</option>
          <option value="pendiente_profesor">👨‍🏫 Pendiente Profesor</option>
          <option value="pendiente_financiera">💰 Pendiente Financiera</option>
          <option value="activo">✅ Activo</option>
          <option value="rechazado">❌ Rechazado</option>
          <option value="finalizado">🏁 Finalizado</option>
        </select>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Projects Table -->
      <div v-else class="table-container">
        <div class="table-header">
          <h3>📊 Lista de Proyectos ({{ filteredProjects.length }})</h3>
        </div>

        <div v-if="filteredProjects.length === 0" class="empty-state">
          <div class="empty-icon">📂</div>
          <h3>No se encontraron proyectos</h3>
          <p>Intenta ajustar los filtros de búsqueda</p>
        </div>

        <div v-else class="table-wrapper">
          <table class="projects-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Nombre del Proyecto</th>
                <th>Estudiante</th>
                <th>Profesor</th>
                <th>Estado</th>
                <th>Presupuesto</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="project in filteredProjects" 
                :key="project.id"
                class="table-row"
              >
                <td>
                  <span class="project-code">{{ project.codigo_proyecto }}</span>
                </td>
                <td>
                  <div class="project-name-cell">
                    <span class="project-name">{{ project.nombre }}</span>
                  </div>
                </td>
                <td>
                  <div class="user-cell">
                    <div class="user-avatar">{{ getInitials(project.estudiante.nombre) }}</div>
                    <span>{{ project.estudiante.nombre }}</span>
                  </div>
                </td>
                <td>
                  <div class="user-cell">
                    <div class="user-avatar professor">{{ getInitials(project.profesor?.nombre || 'SA') }}</div>
                    <span>{{ project.profesor?.nombre || 'Sin asignar' }}</span>
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', getStatusClass(project.estado)]">
                    {{ getStatusText(project.estado) }}
                  </span>
                </td>
                <td>
                  <span class="budget-value">{{ formatMoney(project.presupuesto_estimado) }}</span>
                </td>
                <td>
                  <button @click="viewProject(project.id)" class="action-btn">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    Ver
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
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
  name: 'AdminProjects',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const filterStatus = ref('')

    const activeCount = computed(() => {
      return projects.value.filter(p => p.estado === 'activo').length
    })

    const pendingCount = computed(() => {
      return projects.value.filter(p => 
        p.estado === 'pendiente_profesor' || p.estado === 'pendiente_financiera'
      ).length
    })

    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + parseFloat(p.presupuesto_asignado || 0), 0)
    })
    
    const filteredProjects = computed(() => {
      let filtered = projects.value
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query) ||
          p.estudiante.nombre.toLowerCase().includes(query)
        )
      }
      
      if (filterStatus.value) {
        filtered = filtered.filter(p => p.estado === filterStatus.value)
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
        alert('Error al cargar los proyectos')
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (id) => {
      router.push(`/admin/project/${id}`)
    }

    const getInitials = (name) => {
      if (!name) return '??'
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'borrador': 'status-draft',
        'pendiente_profesor': 'status-pending-prof',
        'pendiente_financiera': 'status-pending-fin',
        'rechazado': 'status-rejected',
        'finalizado': 'status-finished'
      }
      return classes[estado] || 'status-draft'
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'activo': 'Activo',
        'borrador': 'Borrador',
        'pendiente_profesor': 'Pendiente Prof.',
        'pendiente_financiera': 'Pendiente Fin.',
        'rechazado': 'Rechazado',
        'finalizado': 'Finalizado'
      }
      return texts[estado] || estado
    }
    
    const formatMoney = (val) => {
      if (!val) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(val)
    }

    const formatMoneyShort = (val) => {
      if (!val) return '$0'
      return new Intl.NumberFormat('es-CO', {
        notation: "compact",
        compactDisplay: "short",
        style: 'currency',
        currency: 'COP'
      }).format(val)
    }
    
    onMounted(() => loadProjects())
    
    return { 
      projects, 
      loading, 
      searchQuery, 
      filterStatus, 
      activeCount,
      pendingCount,
      totalBudget,
      filteredProjects, 
      viewProject, 
      getInitials,
      getStatusClass, 
      getStatusText, 
      formatMoney,
      formatMoneyShort
    }
  }
}
</script>

<style scoped>
/* BASE */
.admin-projects-page {
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
  filter: blur(120px);
  opacity: 0.12;
  animation: float 25s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  top: -300px;
  right: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -250px;
  left: -250px;
  animation-delay: -12s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-50px, 50px) scale(0.9); }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER */
.page-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.3s;
  width: fit-content;
}

.btn-back:hover {
  background: #334155;
  border-color: #ef4444;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.header-title h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.header-title p {
  font-size: 16px;
  color: #cbd5e1;
  font-weight: 600;
}

/* STATS MINI */
.stats-mini {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-mini {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  transition: all 0.3s;
}

.stat-mini:hover {
  transform: translateY(-2px);
  border-color: #ef4444;
}

.stat-mini .stat-icon {
  font-size: 36px;
  filter: drop-shadow(0 2px 6px rgba(239, 68, 68, 0.3));
}

.stat-mini .stat-value {
  font-size: 24px;
  font-weight: 900;
  color: #ef4444;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-mini .stat-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* FILTERS */
.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
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
  padding: 14px 16px 14px 48px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #ffffff;
  font-weight: 600;
  font-size: 15px;
}

.search-input:focus {
  outline: none;
  border-color: #ef4444;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

.filter-select {
  min-width: 250px;
  padding: 14px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #ef4444;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

/* TABLE CONTAINER */
.table-container {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.table-header {
  padding: 24px 28px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
}

.table-header h3 {
  font-size: 20px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-wrapper {
  overflow-x: auto;
}

.projects-table {
  width: 100%;
  border-collapse: collapse;
}

.projects-table thead {
  background: rgba(15, 23, 42, 0.8);
}

.projects-table th {
  padding: 16px 20px;
  text-align: left;
  font-weight: 800;
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}

.projects-table tbody tr {
  border-bottom: 1px solid #334155;
  transition: all 0.3s;
}

.projects-table tbody tr:hover {
  background: rgba(239, 68, 68, 0.05);
}

.projects-table td {
  padding: 20px;
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

.project-code {
  font-family: 'Courier New', monospace;
  color: #ef4444;
  font-weight: 800;
  font-size: 13px;
  background: rgba(239, 68, 68, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-block;
}

.project-name-cell {
  max-width: 300px;
}

.project-name {
  display: block;
  color: #f1f5f9;
  font-weight: 700;
  line-height: 1.4;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 800;
  font-size: 12px;
  flex-shrink: 0;
}

.user-avatar.professor {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.status-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-draft {
  background: rgba(100, 116, 139, 0.2);
  color: #94a3b8;
  border: 1px solid rgba(100, 116, 139, 0.3);
}

.status-pending-prof {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.status-pending-fin {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.status-rejected {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-finished {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.budget-value {
  font-weight: 800;
  color: #10b981;
  font-size: 15px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn:hover {
  background: #ef4444;
  border-color: #ef4444;
  color: #ffffff;
  transform: translateY(-2px);
}

/* LOADING */
.loading-state {
  text-align: center;
  padding: 100px 20px;
}

.spinner {
  width: 64px;
  height: 64px;
  border: 4px solid #334155;
  border-top-color: #ef4444;
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

/* EMPTY STATE */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  color: #ffffff;
  font-weight: 900;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 600;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .admin-projects-page {
    padding: 20px 12px;
  }

  .stats-mini {
    grid-template-columns: 1fr;
  }

  .filters-section {
    flex-direction: column;
  }

  .search-box,
  .filter-select {
    width: 100%;
  }

  .table-wrapper {
    overflow-x: scroll;
  }

  .projects-table {
    min-width: 800px;
  }
}
</style>
