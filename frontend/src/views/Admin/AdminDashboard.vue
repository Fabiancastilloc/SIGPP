<template>
  <div class="admin-dashboard">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Header Premium -->
      <div class="dashboard-header">
        <div class="header-content">
          <div class="header-icon-box">
            <div class="icon-glow"></div>
            <span class="header-icon">⚡</span>
          </div>
          <div class="header-text">
            <h1>Panel de Administración</h1>
            <p>Gestión integral del sistema SIGPP</p>
          </div>
        </div>
        <button @click="goToUsers" class="btn-gold">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Gestionar Usuarios
        </button>
      </div>

      <!-- Stats Grid Premium -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Total Proyectos</div>
          </div>
        </div>

        <div class="stat-card card-gold">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ totalUsers }}</div>
            <div class="stat-label">Usuarios</div>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Proyectos Activos</div>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">${{ formatMillions(totalBudget) }}M</div>
            <div class="stat-label">Presupuesto Total</div>
          </div>
        </div>
      </div>

      <!-- Quick Access -->
      <div class="quick-section">
        <h2 class="section-title">🚀 Accesos Rápidos</h2>
        <div class="quick-grid">
          <div class="quick-card" @click="filterByStatus('pendiente_financiera')">
            <div class="quick-icon">💰</div>
            <div class="quick-info">
              <div class="quick-number">{{ pendingFinance }}</div>
              <div class="quick-label">Pendientes Financiera</div>
            </div>
          </div>

          <div class="quick-card" @click="filterByStatus('pendiente_profesor')">
            <div class="quick-icon">👨‍🏫</div>
            <div class="quick-info">
              <div class="quick-number">{{ pendingProfessor }}</div>
              <div class="quick-label">Pendientes Profesor</div>
            </div>
          </div>

          <div class="quick-card" @click="filterByStatus('activo')">
            <div class="quick-icon">✅</div>
            <div class="quick-info">
              <div class="quick-number">{{ activeProjects }}</div>
              <div class="quick-label">En Ejecución</div>
            </div>
          </div>

          <div class="quick-card" @click="filterByStatus('rechazado')">
            <div class="quick-icon">❌</div>
            <div class="quick-info">
              <div class="quick-number">{{ rejectedProjects }}</div>
              <div class="quick-label">Rechazados</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Cards -->
      <div class="nav-section">
        <h2 class="section-title">📂 Módulos del Sistema</h2>
        <div class="nav-grid">
          <router-link to="/admin/projects" class="nav-card card-blue">
            <div class="card-icon">📊</div>
            <h3>Proyectos</h3>
            <p>Gestiona todos los proyectos del sistema</p>
            <div class="card-arrow">→</div>
          </router-link>

          <router-link to="/admin/users" class="nav-card card-purple">
            <div class="card-icon">👥</div>
            <h3>Usuarios</h3>
            <p>Administra usuarios y permisos</p>
            <div class="card-arrow">→</div>
          </router-link>

          <router-link to="/admin/reports" class="nav-card card-green">
            <div class="card-icon">📈</div>
            <h3>Reportes</h3>
            <p>Genera informes y estadísticas</p>
            <div class="card-arrow">→</div>
          </router-link>

          <router-link to="/admin/settings" class="nav-card card-orange">
            <div class="card-icon">⚙️</div>
            <h3>Configuración</h3>
            <p>Ajusta parámetros del sistema</p>
            <div class="card-arrow">→</div>
          </router-link>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="controls-section">
        <div class="filter-group">
          <button 
            @click="currentFilter = 'all'" 
            :class="['filter-chip', { active: currentFilter === 'all' }]"
          >
            Todos
          </button>
          <button 
            @click="currentFilter = 'activo'" 
            :class="['filter-chip', { active: currentFilter === 'activo' }]"
          >
            Activos
          </button>
          <button 
            @click="currentFilter = 'pendiente_profesor'" 
            :class="['filter-chip', { active: currentFilter === 'pendiente_profesor' }]"
          >
            Pend. Profesor
          </button>
          <button 
            @click="currentFilter = 'pendiente_financiera'" 
            :class="['filter-chip', { active: currentFilter === 'pendiente_financiera' }]"
          >
            Pend. Financiera
          </button>
          <button 
            @click="currentFilter = 'rechazado'" 
            :class="['filter-chip', { active: currentFilter === 'rechazado' }]"
          >
            Rechazados
          </button>
        </div>

        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por nombre, código, estudiante o profesor..." 
            class="search-input"
          />
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-gold"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Projects Grid -->
      <div v-else-if="filteredProjects.length > 0" class="projects-section">
        <div class="section-header">
          <h2 class="section-title">📁 Proyectos ({{ filteredProjects.length }})</h2>
        </div>

        <div class="projects-grid">
          <div 
            v-for="project in filteredProjects" 
            :key="project.id"
            class="project-card"
          >
            <!-- Header de la tarjeta -->
            <div class="card-header" :class="getStatusClass(project.estado)">
              <span class="status-badge">{{ getStatusText(project.estado) }}</span>
              <span class="project-code">{{ project.codigo_proyecto }}</span>
            </div>

            <!-- Cuerpo de la tarjeta -->
            <div class="card-body">
              <h3 class="project-name">{{ project.nombre }}</h3>
              <p class="project-desc">{{ truncate(project.descripcion, 80) }}</p>

              <!-- Información del proyecto -->
              <div class="project-meta">
                <!-- Estudiante -->
                <div class="meta-row">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <div class="meta-content">
                    <span class="meta-label">Estudiante</span>
                    <span class="meta-value">{{ project.estudiante?.nombre || 'Sin asignar' }}</span>
                  </div>
                </div>

                <!-- Profesor DESTACADO -->
                <div class="meta-row professor-highlight">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <div class="meta-content">
                    <span class="meta-label">Profesor Asesor</span>
                    <span class="meta-value professor-name">{{ project.profesor?.nombre || 'Sin asignar' }}</span>
                  </div>
                </div>

                <!-- Presupuesto -->
                <div class="meta-row">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div class="meta-content">
                    <span class="meta-label">Presupuesto</span>
                    <span class="meta-value" v-if="project.presupuesto_asignado">{{ formatMoney(project.presupuesto_asignado) }}</span>
                    <span class="meta-value estimated" v-else>{{ formatMoney(project.presupuesto_estimado) }} (estimado)</span>
                  </div>
                </div>
              </div>

              <!-- Barra de ejecución para activos -->
              <div v-if="project.estado === 'activo' && project.presupuesto_asignado" class="execution-bar">
                <div class="execution-header">
                  <span>Ejecución Presupuestal</span>
                  <span class="execution-percent">{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
                </div>
                <div class="progress-track">
                  <div 
                    class="progress-bar" 
                    :class="getProgressClass(project.presupuesto_ejecutado, project.presupuesto_asignado)"
                    :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Acciones -->
            <div class="card-actions">
              <button @click="viewProject(project.id)" class="action-btn btn-view">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                Ver
              </button>
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
              <button @click="manageProject(project.id)" class="action-btn btn-manage">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Gestionar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>No se encontraron proyectos</h3>
        <p>Ajusta los filtros de búsqueda o cambia el estado</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import projectsApi from '../../api/projects'

export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    const totalUsers = ref(150)

    const totalProjects = computed(() => projects.value.length)
    const activeProjects = computed(() => projects.value.filter(p => p.estado === 'activo').length)
    const pendingFinance = computed(() => projects.value.filter(p => p.estado === 'pendiente_financiera').length)
    const pendingProfessor = computed(() => projects.value.filter(p => p.estado === 'pendiente_profesor').length)
    const rejectedProjects = computed(() => projects.value.filter(p => p.estado === 'rechazado').length)
    
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
          p.codigo_proyecto.toLowerCase().includes(query) ||
          p.estudiante?.nombre?.toLowerCase().includes(query) ||
          p.profesor?.nombre?.toLowerCase().includes(query)
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
        console.error('Error cargando proyectos:', err)
      } finally {
        loading.value = false
      }
    }

    const goToUsers = () => router.push('/admin/users')
    const viewProject = (id) => router.push(`/admin/project/${id}`)
    const viewExpenses = (id) => router.push(`/admin/project/${id}/expenses`)
    const manageProject = (id) => router.push(`/admin/projects/${id}/manage`)
    const filterByStatus = (status) => currentFilter.value = status

    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'pendiente_profesor': 'status-pending-prof',
        'pendiente_financiera': 'status-pending-fin',
        'borrador': 'status-draft',
        'rechazado': 'status-rejected'
      }
      return classes[estado]
    }

    const getStatusText = (estado) => {
      const texts = {
        'activo': 'Activo',
        'pendiente_profesor': 'Pend. Profesor',
        'pendiente_financiera': 'Pend. Financiera',
        'borrador': 'Borrador',
        'rechazado': 'Rechazado'
      }
      return texts[estado] || estado
    }

    const truncate = (text, len) => {
      if (!text) return ''
      return text.length > len ? text.substring(0, len) + '...' : text
    }

    const formatMoney = (val) => {
      if (!val) return '$0'
      return new Intl.NumberFormat('es-CO').format(val)
    }

    const formatMillions = (val) => {
      if (!val) return '0.0'
      return (parseFloat(val) / 1000000).toFixed(1)
    }

    const calculatePercentage = (executed, assigned) => {
      if (!assigned || assigned === 0) return 0
      return Math.min(100, Math.round((parseFloat(executed || 0) / parseFloat(assigned)) * 100))
    }

    const getProgressClass = (executed, assigned) => {
      const percent = calculatePercentage(executed, assigned)
      if (percent >= 90) return 'progress-danger'
      if (percent >= 70) return 'progress-warning'
      return 'progress-success'
    }

    onMounted(() => loadProjects())

    return {
      projects,
      loading,
      currentFilter,
      searchQuery,
      totalProjects,
      totalUsers,
      activeProjects,
      pendingFinance,
      pendingProfessor,
      rejectedProjects,
      totalBudget,
      filteredProjects,
      goToUsers,
      viewProject,
      viewExpenses,
      manageProject,
      filterByStatus,
      getStatusClass,
      getStatusText,
      truncate,
      formatMoney,
      formatMillions,
      calculatePercentage,
      getProgressClass
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 40px 20px;
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
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
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
  background: linear-gradient(135deg, #f59e0b, #d97706);
  bottom: -250px;
  left: -250px;
  animation-delay: -12s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -6s;
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

/* Header Premium */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 24px;
  margin-bottom: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.header-icon-box {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-glow {
  position: absolute;
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-radius: 50%;
  filter: blur(20px);
  opacity: 0.5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.3; }
}

.header-icon {
  position: relative;
  z-index: 2;
  font-size: 52px;
  filter: drop-shadow(0 4px 12px rgba(239, 68, 68, 0.6));
}

.header-text h1 {
  font-size: 36px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.header-text p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 18px;
  font-weight: 600;
}

.btn-gold {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  border: none;
  border-radius: 14px;
  font-weight: 800;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}

.btn-gold:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(245, 158, 11, 0.6);
}

.btn-icon {
  width: 22px;
  height: 22px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: #1e293b;
  padding: 32px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 24px;
  border: 2px solid #334155;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.card-primary {
  border-left: 6px solid #3b82f6;
}

.card-gold {
  border-left: 6px solid #f59e0b;
}

.card-success {
  border-left: 6px solid #10b981;
}

.card-warning {
  border-left: 6px solid #ef4444;
}

.stat-icon-wrapper {
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon {
  width: 36px;
  height: 36px;
  color: #f59e0b;
}

.stat-value {
  font-size: 40px;
  font-weight: 900;
  color: white;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Quick Section */
.quick-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 800;
  color: #ef4444;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.quick-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 28px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid rgba(255, 255, 255, 0.05);
}

.quick-card:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  transform: translateY(-3px);
}

.quick-icon {
  font-size: 42px;
  filter: drop-shadow(0 2px 8px rgba(239, 68, 68, 0.4));
}

.quick-number {
  font-size: 32px;
  font-weight: 900;
  color: white;
  line-height: 1;
}

.quick-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 700;
  margin-top: 6px;
}

/* Navigation Cards */
.nav-section {
  margin-bottom: 40px;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

.nav-card {
  background: #1e293b;
  padding: 32px;
  border-radius: 20px;
  text-decoration: none;
  border: 2px solid #334155;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.nav-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, transparent, currentColor, transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-card:hover::before {
  opacity: 1;
}

.nav-card:hover {
  transform: translateY(-6px);
  border-color: currentColor;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
}

.card-blue { color: #3b82f6; }
.card-purple { color: #8b5cf6; }
.card-green { color: #10b981; }
.card-orange { color: #f59e0b; }

.card-icon {
  font-size: 52px;
  margin-bottom: 16px;
  filter: drop-shadow(0 4px 12px currentColor);
}

.nav-card h3 {
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 12px;
}

.nav-card p {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 20px;
}

.card-arrow {
  font-size: 28px;
  color: currentColor;
  font-weight: 900;
  transition: transform 0.3s;
}

.nav-card:hover .card-arrow {
  transform: translateX(10px);
}

/* Controls Section */
.controls-section {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-chip {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  border-radius: 50px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-chip:hover {
  border-color: #ef4444;
  color: white;
}

.filter-chip.active {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border-color: #ef4444;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.search-box {
  flex: 1;
  min-width: 320px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  color: rgba(255, 255, 255, 0.4);
}

.search-input {
  width: 100%;
  padding: 14px 18px 14px 52px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  color: white;
  font-size: 15px;
  font-weight: 600;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.search-input:focus {
  outline: none;
  border-color: #ef4444;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 100px 20px;
}

.spinner-gold {
  width: 70px;
  height: 70px;
  border: 5px solid rgba(255, 255, 255, 0.1);
  border-top-color: #f59e0b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 18px;
  font-weight: 600;
}

/* Projects Section */
.projects-section {
  margin-bottom: 40px;
}

.section-header {
  margin-bottom: 28px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 28px;
}

.project-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.project-card:hover {
  transform: translateY(-6px);
  border-color: rgba(239, 68, 68, 0.5);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
}

.card-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.status-badge {
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 50px;
  letter-spacing: 0.5px;
}

.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid #10b981;
}

.status-pending-prof {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.status-pending-fin {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid #8b5cf6;
}

.status-draft {
  background: rgba(100, 116, 139, 0.2);
  color: #64748b;
  border: 1px solid #64748b;
}

.status-rejected {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid #ef4444;
}

.project-code {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #f59e0b;
  font-weight: 800;
  background: rgba(245, 158, 11, 0.1);
  padding: 4px 12px;
  border-radius: 6px;
}

.card-body {
  padding: 28px;
}

.project-name {
  font-size: 20px;
  font-weight: 800;
  color: white;
  margin-bottom: 12px;
  line-height: 1.3;
}

.project-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.7;
  margin-bottom: 24px;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.meta-row {
  display: flex;
  gap: 14px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.meta-icon {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

.meta-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meta-value {
  font-size: 15px;
  font-weight: 700;
  color: white;
}

/* PROFESOR DESTACADO */
.professor-highlight {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
  border: 2px solid rgba(239, 68, 68, 0.3);
}

.professor-highlight .meta-icon {
  color: #ef4444;
}

.professor-name {
  color: #ef4444 !important;
  font-weight: 800 !important;
  font-size: 16px !important;
}

.estimated {
  font-style: italic;
  opacity: 0.7;
}

/* Execution Bar */
.execution-bar {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.execution-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.6);
}

.execution-percent {
  color: #f59e0b;
  font-weight: 900;
  font-size: 14px;
}

.progress-track {
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 999px;
  transition: width 0.8s ease;
}

.progress-success {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-warning {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

/* Card Actions */
.card-actions {
  display: flex;
  gap: 10px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.btn-view:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-expenses:hover {
  background: rgba(16, 185, 129, 0.2);
  border-color: #10b981;
  color: #10b981;
}

.btn-manage:hover {
  background: rgba(245, 158, 11, 0.2);
  border-color: #f59e0b;
  color: #f59e0b;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-icon {
  font-size: 100px;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 28px;
  color: white;
  margin-bottom: 12px;
  font-weight: 900;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }

  .controls-section {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    width: 100%;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
