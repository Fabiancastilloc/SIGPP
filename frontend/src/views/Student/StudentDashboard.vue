<!-- frontend/src/views/Student/StudentDashboard.vue -->
<template>
  <div class="student-dashboard">
    <div class="container">
      
      <!-- Hero Header -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-greeting">
            <h1>Hola, <span class="highlight">{{ userName }}</span> 👋</h1>
            <p>Bienvenido a tu panel de gestión de proyectos</p>
          </div>
          <button @click="createProject" class="btn-create-project">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            Crear Proyecto
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Proyectos Totales</div>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingProjects }}</div>
            <div class="stat-label">En Revisión</div>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Activos</div>
          </div>
        </div>

        <div class="stat-card card-gold">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatCurrency(totalBudget) }}</div>
            <div class="stat-label">Presupuesto Total</div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h2 class="section-title">⚡ Acciones Rápidas</h2>
        <div class="actions-grid">
          <div class="action-card" @click="createProject">
            <div class="action-icon">🚀</div>
            <div class="action-content">
              <strong>Crear Proyecto</strong>
              <p>Inicia una nueva propuesta</p>
            </div>
          </div>
          <div class="action-card" @click="viewDrafts">
            <div class="action-icon">📝</div>
            <div class="action-content">
              <strong>Borradores</strong>
              <p>{{ draftProjects }} sin enviar</p>
            </div>
          </div>
          <div class="action-card" @click="viewProfile">
            <div class="action-icon">👤</div>
            <div class="action-content">
              <strong>Mi Perfil</strong>
              <p>Actualizar información</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filters-header">
          <h2 class="section-title">📂 Mis Proyectos</h2>
          <div class="filter-chips">
            <button 
              @click="currentFilter = 'all'" 
              :class="['filter-chip', { active: currentFilter === 'all' }]"
            >
              Todos ({{ projects.length }})
            </button>
            <button 
              @click="currentFilter = 'owner'" 
              :class="['filter-chip', { active: currentFilter === 'owner' }]"
            >
              👑 Propios ({{ ownProjects.length }})
            </button>
            <button 
              @click="currentFilter = 'collaborator'" 
              :class="['filter-chip', { active: currentFilter === 'collaborator' }]"
            >
              🤝 Colaborador ({{ collaboratorProjects.length }})
            </button>
            <button 
              @click="currentFilter = 'borrador'" 
              :class="['filter-chip', { active: currentFilter === 'borrador' }]"
            >
              📝 Borradores
            </button>
            <button 
              @click="currentFilter = 'pendiente_profesor'" 
              :class="['filter-chip', { active: currentFilter === 'pendiente_profesor' }]"
            >
              ⏳ En Revisión
            </button>
            <button 
              @click="currentFilter = 'activo'" 
              :class="['filter-chip', { active: currentFilter === 'activo' }]"
            >
              ✅ Activos
            </button>
          </div>
        </div>

        <!-- Search -->
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input"
            placeholder="Buscar proyectos por nombre o código..."
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Projects Grid -->
      <div v-else-if="filteredProjects.length > 0" class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <!-- Card Header -->
          <div class="card-header" :class="getStatusClass(project.estado)">
            <div class="header-left">
              <span class="status-badge">{{ getStatusText(project.estado) }}</span>
              <!-- Indicador de rol -->
              <span v-if="project.is_owner" class="role-badge owner-badge" title="Eres el creador">👑 Creador</span>
              <span v-else-if="project.is_collaborator" class="role-badge collab-badge" title="Eres colaborador">🤝 Colaborador</span>
            </div>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
          </div>

          <!-- Card Body -->
          <div class="card-body">
            <h3 class="project-title">{{ project.nombre }}</h3>
            <p class="project-description">{{ truncate(project.descripcion, 100) }}</p>

            <!-- Project Info -->
            <div class="project-info">
              <div class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">
                    {{ project.is_owner ? 'Profesor' : 'Creado por' }}
                  </span>
                  <span class="info-value">
                    {{ project.is_owner ? (project.profesor?.nombre || 'Sin asignar') : project.estudiante.nombre }}
                  </span>
                </div>
              </div>

              <div class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Presupuesto</span>
                  <span class="info-value">{{ formatCurrency(project.presupuesto_estimado) }}</span>
                </div>
              </div>
            </div>

            <!-- Team Size -->
            <div v-if="project.team_size > 1" class="team-indicator">
              <svg class="team-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span class="team-text">Equipo de {{ project.team_size }} personas</span>
            </div>

            <!-- Progress Bar (only for active projects) -->
            <div v-if="project.estado === 'activo' && project.presupuesto_asignado" class="progress-section">
              <div class="progress-header">
                <span class="progress-label">Ejecución Presupuestal</span>
                <span class="progress-value">{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress-fill"
                  :class="getProgressClass(project.presupuesto_ejecutado, project.presupuesto_asignado)"
                  :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Card Actions -->
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="action-btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Ver
            </button>
            
            <button 
              v-if="project.estado === 'borrador' && project.is_owner" 
              @click="editProject(project.id)" 
              class="action-btn btn-warning"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Editar
            </button>

            <button 
              v-if="project.estado === 'activo' && project.presupuesto_asignado" 
              @click="viewExpenses(project.id)" 
              class="action-btn btn-success"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              Gastos
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>No tienes proyectos</h3>
        <p>Crea tu primer proyecto para comenzar</p>
        <button @click="createProject" class="btn-create-first">
          🚀 Crear Mi Primer Proyecto
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store'
import projectsApi from '../../api/projects'

export default {
  name: 'StudentDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    
    const userName = computed(() => {
      return authStore.user?.nombre_completo?.split(' ')[0] || 'Estudiante'
    })
    
    // Proyectos propios
    const ownProjects = computed(() => {
      return projects.value.filter(p => p.is_owner === true)
    })
    
    // Proyectos como colaborador
    const collaboratorProjects = computed(() => {
      return projects.value.filter(p => p.is_collaborator === true)
    })
    
    const totalProjects = computed(() => projects.value.length)
    
    const pendingProjects = computed(() => {
      return projects.value.filter(p => 
        p.estado === 'pendiente_profesor' || p.estado === 'pendiente_financiera'
      ).length
    })
    
    const activeProjects = computed(() => {
      return projects.value.filter(p => p.estado === 'activo').length
    })
    
    const draftProjects = computed(() => {
      return projects.value.filter(p => p.estado === 'borrador').length
    })
    
    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + parseFloat(p.presupuesto_asignado || 0), 0)
    })
    
    const filteredProjects = computed(() => {
      let filtered = projects.value
      
      // Filtrar por tipo
      if (currentFilter.value === 'owner') {
        filtered = ownProjects.value
      } else if (currentFilter.value === 'collaborator') {
        filtered = collaboratorProjects.value
      } else if (currentFilter.value !== 'all') {
        // Filtrar por estado
        filtered = filtered.filter(p => p.estado === currentFilter.value)
      }
      
      // Filtrar por búsqueda
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query)
        )
      }
      
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    })
    
    const loadProjects = async () => {
      loading.value = true
      try {
        // ✅ CAMBIO CRÍTICO: Ahora usa getAllProjectsInvolved
        const response = await projectsApi.getAllProjectsInvolved()
        projects.value = response.data
        
        console.log('✅ Proyectos cargados:', projects.value.length)
        console.log('   👑 Propios:', ownProjects.value.length)
        console.log('   🤝 Colaborador:', collaboratorProjects.value.length)
        
      } catch (err) {
        console.error('❌ Error cargando proyectos:', err)
      } finally {
        loading.value = false
      }
    }
    
    const createProject = () => router.push('/student/create-project')
    const viewProject = (id) => router.push(`/student/project/${id}`)
    const editProject = (id) => router.push(`/student/edit-project/${id}`)
    const viewExpenses = (id) => router.push(`/student/project/${id}/expenses`)
    const viewDrafts = () => currentFilter.value = 'borrador'
    const viewProfile = () => router.push('/profile')
    
    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'pendiente_profesor': 'status-pending',
        'pendiente_financiera': 'status-pending',
        'borrador': 'status-draft',
        'rechazado': 'status-rejected'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'activo': '✅ Activo',
        'pendiente_profesor': '⏳ En Revisión',
        'pendiente_financiera': '💼 Revisión Financiera',
        'borrador': '📝 Borrador',
        'rechazado': '❌ Rechazado'
      }
      return texts[estado] || estado
    }
    
    const truncate = (text, len) => {
      if (!text) return ''
      return text.length > len ? text.substring(0, len) + '...' : text
    }
    
    const formatCurrency = (value) => {
      if (!value) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }
    
    const calculatePercentage = (executed, total) => {
      if (!total || total === 0) return 0
      return Math.min(100, Math.round((parseFloat(executed || 0) / parseFloat(total)) * 100))
    }
    
    const getProgressClass = (executed, total) => {
      const percent = calculatePercentage(executed, total)
      if (percent >= 90) return 'progress-danger'
      if (percent >= 70) return 'progress-warning'
      return 'progress-success'
    }
    
    onMounted(() => {
      loadProjects()
    })
    
    return {
      userName,
      projects,
      ownProjects,
      collaboratorProjects,
      loading,
      currentFilter,
      searchQuery,
      totalProjects,
      pendingProjects,
      activeProjects,
      draftProjects,
      totalBudget,
      filteredProjects,
      createProject,
      viewProject,
      editProject,
      viewExpenses,
      viewDrafts,
      viewProfile,
      getStatusClass,
      getStatusText,
      truncate,
      formatCurrency,
      calculatePercentage,
      getProgressClass
    }
  }
}
</script>

<style scoped>
/* ==================== BASE ==================== */
.student-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

/* ==================== HERO SECTION ==================== */
.hero-section {
  margin-bottom: 40px;
  padding: 40px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border: 3px solid #3b82f6;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.hero-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.hero-greeting h1 {
  font-size: 36px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.hero-greeting .highlight {
  color: #d4af37;
  text-shadow: 0 2px 8px rgba(212, 175, 55, 0.5);
}

.hero-greeting p {
  font-size: 16px;
  color: #e0e7ff;
  font-weight: 600;
}

.btn-create-project {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border: none;
  border-radius: 12px;
  color: #0a0f1e;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
  white-space: nowrap;
}

.btn-create-project:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

.btn-create-project svg {
  width: 22px;
  height: 22px;
}

/* ==================== STATS GRID ==================== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 28px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.card-primary { border-left: 4px solid #3b82f6; }
.card-warning { border-left: 4px solid #f59e0b; }
.card-success { border-left: 4px solid #10b981; }
.card-gold { border-left: 4px solid #d4af37; }

.stat-icon-wrapper {
  width: 64px;
  height: 64px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-primary .stat-icon { color: #3b82f6; }
.card-warning .stat-icon { color: #f59e0b; }
.card-success .stat-icon { color: #10b981; }
.card-gold .stat-icon { color: #d4af37; }

.stat-icon {
  width: 36px;
  height: 36px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 36px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ==================== QUICK ACTIONS ==================== */
.quick-actions {
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 20px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card:hover {
  background: #334155;
  border-color: #d4af37;
  transform: translateX(4px);
}

.action-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(212, 175, 55, 0.3));
}

.action-content strong {
  display: block;
  font-size: 16px;
  color: #ffffff;
  font-weight: 800;
  margin-bottom: 4px;
}

.action-content p {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

/* ==================== FILTERS ==================== */
.filters-section {
  margin-bottom: 32px;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-chips {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-chip {
  padding: 10px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  color: #cbd5e1;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.filter-chip:hover {
  border-color: #d4af37;
  color: #ffffff;
}

.filter-chip.active {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border-color: #d4af37;
  color: #0a0f1e;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

/* ==================== SEARCH ==================== */
.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  color: #64748b;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 16px 20px 16px 56px;
  background: #1e293b;
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

/* ==================== LOADING ==================== */
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

/* ==================== PROJECTS GRID ==================== */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.project-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: #d4af37;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

/* ==================== CARD HEADER ==================== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.status-badge {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 12px;
  letter-spacing: 0.5px;
}

.status-active { background: #10b981; color: #ffffff; }
.status-pending { background: #f59e0b; color: #ffffff; }
.status-draft { background: #64748b; color: #ffffff; }
.status-rejected { background: #ef4444; color: #ffffff; }

/* ✅ NUEVO: Role badges */
.role-badge {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 8px;
  letter-spacing: 0.3px;
}

.owner-badge {
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  border: 1px solid #d4af37;
}

.collab-badge {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid #10b981;
}

.project-code {
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: #d4af37;
  font-weight: 700;
}

/* ==================== CARD BODY ==================== */
.card-body {
  padding: 24px;
}

.project-title {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
  line-height: 1.3;
}

.project-description {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* ==================== PROJECT INFO ==================== */
.project-info {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  border: 1px solid #334155;
}

.info-icon {
  width: 22px;
  height: 22px;
  color: #d4af37;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 700;
}

/* ✅ NUEVO: Team indicator */
.team-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(16, 185, 129, 0.1);
  border: 2px solid rgba(16, 185, 129, 0.3);
  border-radius: 10px;
  margin-bottom: 16px;
}

.team-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
}

.team-text {
  font-size: 12px;
  color: #10b981;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ==================== PROGRESS SECTION ==================== */
.progress-section {
  padding-top: 16px;
  border-top: 2px solid #334155;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 12px;
  color: #cbd5e1;
  font-weight: 700;
}

.progress-value {
  font-size: 14px;
  color: #d4af37;
  font-weight: 900;
}

.progress-bar {
  height: 8px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease;
}

.progress-success { background: linear-gradient(90deg, #10b981, #059669); }
.progress-warning { background: linear-gradient(90deg, #f59e0b, #d97706); }
.progress-danger { background: linear-gradient(90deg, #ef4444, #dc2626); }

/* ==================== CARD ACTIONS ==================== */
.card-actions {
  display: flex;
  gap: 10px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border-top: 2px solid #334155;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: #3b82f6;
  color: #ffffff;
}

.btn-primary:hover {
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-warning {
  background: #f59e0b;
  color: #ffffff;
}

.btn-warning:hover {
  background: #d97706;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.btn-success {
  background: #10b981;
  color: #ffffff;
}

.btn-success:hover {
  background: #059669;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

/* ==================== EMPTY STATE ==================== */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-icon {
  font-size: 96px;
  margin-bottom: 24px;
  opacity: 0.6;
}

.empty-state h3 {
  font-size: 28px;
  color: #ffffff;
  font-weight: 900;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 600;
  margin-bottom: 32px;
}

.btn-create-first {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border: none;
  border-radius: 12px;
  color: #0a0f1e;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.btn-create-first:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .student-dashboard {
    padding: 20px 12px;
  }

  .hero-section {
    padding: 24px;
  }

  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .hero-greeting h1 {
    font-size: 28px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-chips {
    justify-content: center;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
