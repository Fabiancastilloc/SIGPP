
<template>
  <div class="professor-dashboard">
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
              Bienvenido, <span class="highlight">Profesor {{ userName }}</span>
            </h1>
            <p>Panel de validación y seguimiento académico de proyectos</p>
          </div>
        </div>

        <div class="quick-actions">
          <router-link to="/professor/validate" class="action-card">
            <div class="action-icon">📝</div>
            <div class="action-content">
              <span class="action-count">{{ pendingCount }}</span>
              <span class="action-label">Por Validar</span>
            </div>
          </router-link>

          <div class="action-card info">
            <div class="action-icon">✅</div>
            <div class="action-content">
              <span class="action-count">{{ validatedCount }}</span>
              <span class="action-label">Validados</span>
            </div>
          </div>

          <div class="action-card success">
            <div class="action-icon">🚀</div>
            <div class="action-content">
              <span class="action-count">{{ activeCount }}</span>
              <span class="action-label">Activos</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Proyectos Asignados</div>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">Pendientes de Validar</div>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ validatedCount }}</div>
            <div class="stat-label">Proyectos Validados</div>
          </div>
        </div>

        <div class="stat-card card-gold">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ activeCount }}</div>
            <div class="stat-label">Proyectos Activos</div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filters-header">
          <div class="filter-chips">
            <button 
              @click="currentFilter = 'all'"
              :class="['filter-chip', { active: currentFilter === 'all' }]"
            >
              Todos ({{ totalProjects }})
            </button>
            <button 
              @click="currentFilter = 'pendiente_profesor'"
              :class="['filter-chip', { active: currentFilter === 'pendiente_profesor' }]"
            >
              Pendientes ({{ pendingCount }})
            </button>
            <button 
              @click="currentFilter = 'pendiente_financiera'"
              :class="['filter-chip', { active: currentFilter === 'pendiente_financiera' }]"
            >
              Validados ({{ validatedCount }})
            </button>
            <button 
              @click="currentFilter = 'activo'"
              :class="['filter-chip', { active: currentFilter === 'activo' }]"
            >
              Activos ({{ activeCount }})
            </button>
          </div>

          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="Buscar por proyecto, estudiante o código..."
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyectos...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredProjects.length === 0" class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>{{ searchQuery ? 'No hay resultados' : 'No hay proyectos' }}</h3>
        <p>{{ searchQuery ? 'Intenta con otra búsqueda' : 'Los proyectos asignados aparecerán aquí' }}</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="projects-grid">
        <div 
          v-for="project in filteredProjects" 
          :key="project.id"
          class="project-card"
        >
          <!-- Card Header -->
          <div class="card-header">
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
            <p class="project-description">{{ truncate(project.descripcion, 120) }}</p>

            <!-- Project Info -->
            <div class="project-info">
              <div class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Estudiante</span>
                  <span class="info-value">{{ project.estudiante.nombre }}</span>
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

              <div v-if="project.presupuesto_asignado" class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Asignado</span>
                  <span class="info-value">{{ formatCurrency(project.presupuesto_asignado) }}</span>
                </div>
              </div>
            </div>

            <!-- 🆕 COLABORADORES SECTION -->
            <div v-if="project.members && project.members.length > 0" class="collaborators-section">
              <div class="collaborators-header">
                <svg class="collab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="collab-title">Colaboradores ({{ project.members.length }})</span>
              </div>

              <div class="collaborators-list">
                <div 
                  v-for="member in project.members.slice(0, 3)" 
                  :key="member.id" 
                  class="collaborator-chip"
                  :title="member.student.nombre_completo"
                >
                  <div class="collab-avatar">
                    {{ getInitials(member.student.nombre_completo) }}
                  </div>
                  <span class="collab-name">{{ truncate(member.student.nombre_completo, 20) }}</span>
                </div>

                <div v-if="project.members.length > 3" class="more-collabs">
                  +{{ project.members.length - 3 }} más
                </div>
              </div>
            </div>

            <!-- Comments Badge -->
            <div v-if="project.comentarios_profesor" class="comments-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
              <span>Ya has comentado este proyecto</span>
            </div>
          </div>

          <!-- Card Actions -->
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="action-btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Ver Detalle
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

            <button 
              v-if="project.estado === 'pendiente_profesor'"
              @click="openValidationModal(project, false)" 
              class="action-btn btn-warning"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              Devolver
            </button>

            <button 
              v-if="project.estado === 'pendiente_profesor'"
              @click="openValidationModal(project, true)" 
              class="action-btn btn-approve"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Aprobar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Validation Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ validationMode ? '✅ Aprobar Proyecto' : '⚠️ Devolver Proyecto' }}</h3>
          <button @click="closeModal" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <div class="project-summary">
            <h4>{{ selectedProject.nombre }}</h4>
            <p>{{ selectedProject.codigo_proyecto }}</p>
            <p class="student-name">👤 {{ selectedProject.estudiante.nombre }}</p>
          </div>

          <div class="form-group">
            <label class="form-label">
              {{ validationMode ? 'Comentarios (opcional)' : 'Motivo de devolución *' }}
            </label>
            <textarea 
              v-model="comentarios"
              class="form-textarea"
              :placeholder="validationMode ? 'Agrega comentarios sobre el proyecto...' : 'Explica por qué devuelves el proyecto...'"
              rows="5"
            ></textarea>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="modal-btn btn-cancel" :disabled="processing">
            Cancelar
          </button>
          <button 
            @click="confirmValidation" 
            :class="['modal-btn', validationMode ? 'btn-approve' : 'btn-reject']"
            :disabled="processing"
          >
            <div v-if="processing" class="spinner-small"></div>
            <span v-else>{{ validationMode ? 'Aprobar Proyecto' : 'Devolver al Estudiante' }}</span>
          </button>
        </div>
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
  name: 'ProfessorDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    const showModal = ref(false)
    const selectedProject = ref(null)
    const validationMode = ref(true)
    const comentarios = ref('')
    const processing = ref(false)
    
    const userName = computed(() => {
      return authStore.user?.nombre_completo?.split(' ')[0] || 'Profesor'
    })
    
    const totalProjects = computed(() => projects.value.length)
    
    const pendingCount = computed(() => {
      return projects.value.filter(p => p.estado === 'pendiente_profesor').length
    })
    
    const validatedCount = computed(() => {
      return projects.value.filter(p => p.estado === 'pendiente_financiera').length
    })
    
    const activeCount = computed(() => {
      return projects.value.filter(p => p.estado === 'activo').length
    })
    
    const filteredProjects = computed(() => {
      let filtered = projects.value
      
      // Filter by status
      if (currentFilter.value !== 'all') {
        filtered = filtered.filter(p => p.estado === currentFilter.value)
      }
      
      // Filter by search
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query) ||
          p.estudiante.nombre.toLowerCase().includes(query)
        )
      }
      
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
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
    
    const viewProject = (projectId) => {
      router.push(`/professor/project/${projectId}`)
    }
    
    const viewExpenses = (projectId) => {
      router.push(`/professor/project/${projectId}/expenses`)
    }
    
    const openValidationModal = (project, approve) => {
      selectedProject.value = project
      validationMode.value = approve
      comentarios.value = ''
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
      selectedProject.value = null
      comentarios.value = ''
    }
    
    const confirmValidation = async () => {
      if (!validationMode.value && !comentarios.value.trim()) {
        alert('⚠️ Debes agregar comentarios al devolver un proyecto')
        return
      }
      
      processing.value = true
      try {
        await projectsApi.validateProject(selectedProject.value.id, {
          aprobado: validationMode.value,
          comentarios: comentarios.value
        })
        
        alert(validationMode.value ? '✅ Proyecto validado exitosamente' : '✅ Proyecto devuelto al estudiante')
        closeModal()
        loadProjects()
      } catch (err) {
        console.error('Error:', err)
        alert('❌ Error al procesar el proyecto')
      } finally {
        processing.value = false
      }
    }
    
    const getStatusClass = (estado) => {
      const classes = {
        'pendiente_profesor': 'status-pending',
        'pendiente_financiera': 'status-validated',
        'activo': 'status-active',
        'borrador': 'status-draft'
      }
      return classes[estado] || 'status-draft'
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'pendiente_profesor': 'Pendiente',
        'pendiente_financiera': 'Validado',
        'activo': 'Activo',
        'borrador': 'Borrador'
      }
      return texts[estado] || estado
    }
    
    const truncate = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const formatCurrency = (value) => {
      if (!value) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }

    const getInitials = (name) => {
      if (!name) return '??'
      return name.split(' ')
        .map(n => n[0])
        .join('')
        .substring(0, 2)
        .toUpperCase()
    }
    
    onMounted(() => {
      loadProjects()
    })
    
    return {
      projects,
      loading,
      currentFilter,
      searchQuery,
      showModal,
      selectedProject,
      validationMode,
      comentarios,
      processing,
      userName,
      totalProjects,
      pendingCount,
      validatedCount,
      activeCount,
      filteredProjects,
      viewProject,
      viewExpenses,
      openValidationModal,
      closeModal,
      confirmValidation,
      getStatusClass,
      getStatusText,
      truncate,
      formatCurrency,
      getInitials
    }
  }
}
</script>

<style scoped>
/* BASE */
.professor-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  padding: 32px 16px;
  position: relative;
  overflow-x: hidden;
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
  animation: float-smooth 25s ease-in-out infinite;
}

.orb-1 {
  width: 700px;
  height: 700px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -350px;
  right: -350px;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -300px;
  left: -300px;
  animation-delay: -12s;
}

.orb-3 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 40%;
  left: 50%;
  animation-delay: -6s;
}

@keyframes float-smooth {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(60px, -60px) scale(1.15);
  }
  66% {
    transform: translate(-50px, 50px) scale(0.9);
  }
}

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
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(168, 85, 247, 0.05));
  border: 3px solid rgba(168, 85, 247, 0.3);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(168, 85, 247, 0.3);
}

.hero-content {
  margin-bottom: 32px;
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

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(30, 41, 59, 0.8);
  border: 2px solid #334155;
  border-radius: 16px;
  text-decoration: none;
  transition: all 0.3s;
}

.action-card:hover {
  border-color: #d4af37;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
}

.action-card.info {
  border-left: 4px solid #3b82f6;
}

.action-card.success {
  border-left: 4px solid #10b981;
}

.action-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(212, 175, 55, 0.3));
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.action-count {
  font-size: 28px;
  font-weight: 900;
  color: #d4af37;
  line-height: 1;
}

.action-label {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 700;
  text-transform: uppercase;
}

/* STATS GRID */
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

.card-primary {
  border-left: 4px solid #3b82f6;
}

.card-warning {
  border-left: 4px solid #f59e0b;
}

.card-success {
  border-left: 4px solid #10b981;
}

.card-gold {
  border-left: 4px solid #d4af37;
}

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

.card-primary .stat-icon {
  color: #3b82f6;
}

.card-warning .stat-icon {
  color: #f59e0b;
}

.card-success .stat-icon {
  color: #10b981;
}

.card-gold .stat-icon {
  color: #d4af37;
}

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

/* FILTERS */
.filters-section {
  margin-bottom: 32px;
}

.filters-header {
  display: flex;
  justify-content: space-between;
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
  transition: all 0.3s;
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

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
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
  transition: all 0.3s;
}

.search-input::placeholder {
  color: #64748b;
}

.search-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

/* LOADING */
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
  to {
    transform: rotate(360deg);
  }
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

/* PROJECTS GRID */
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
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: #d4af37;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

/* CARD HEADER */
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

.status-active {
  background: #10b981;
  color: #ffffff;
}

.status-pending {
  background: #f59e0b;
  color: #ffffff;
}

.status-validated {
  background: #3b82f6;
  color: #ffffff;
}

.status-draft {
  background: #64748b;
  color: #ffffff;
}

.project-code {
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: #d4af37;
  font-weight: 700;
  background: rgba(212, 175, 55, 0.15);
  padding: 4px 10px;
  border-radius: 6px;
}

/* CARD BODY */
.card-body {
  padding: 24px;
}

.project-title {
  font-size: 20px;
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

.project-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
  flex-shrink: 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
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

/* 🆕 COLABORADORES SECTION */
.collaborators-section {
  margin-top: 20px;
  padding: 16px;
  background: rgba(16, 185, 129, 0.05);
  border: 2px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
}

.collaborators-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.collab-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
}

.collab-title {
  font-size: 13px;
  color: #10b981;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.collaborators-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.collaborator-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid #334155;
  border-radius: 20px;
  transition: all 0.3s;
  cursor: pointer;
}

.collaborator-chip:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
  transform: translateY(-2px);
}

.collab-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 10px;
  flex-shrink: 0;
}

.collab-name {
  font-size: 12px;
  color: #f1f5f9;
  font-weight: 600;
}

.more-collabs {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background: rgba(100, 116, 139, 0.2);
  border: 1px solid rgba(100, 116, 139, 0.4);
  border-radius: 20px;
  font-size: 11px;
  color: #94a3b8;
  font-weight: 700;
}

.comments-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 10px;
  margin-top: 12px;
}

.comments-badge svg {
  width: 18px;
  height: 18px;
  color: #3b82f6;
}

.comments-badge span {
  font-size: 12px;
  color: #60a5fa;
  font-weight: 700;
}

/* CARD ACTIONS */
.card-actions {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-top: 2px solid #334155;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: #3b82f6;
  color: #ffffff;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-success {
  background: #10b981;
  color: #ffffff;
}

.btn-success:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-warning {
  background: #f59e0b;
  color: #ffffff;
}

.btn-warning:hover {
  background: #d97706;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.btn-approve {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #ffffff;
}

.btn-approve:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #1e293b;
  border: 2px solid #d4af37;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 2px solid #334155;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
}

.btn-close {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(239, 68, 68, 0.2);
  border-radius: 50%;
  color: #ef4444;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #ef4444;
  color: #ffffff;
  transform: rotate(90deg);
}

.modal-body {
  padding: 28px;
}

.project-summary {
  padding: 20px;
  background: rgba(59, 130, 246, 0.1);
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  margin-bottom: 24px;
}

.project-summary h4 {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 8px;
}

.project-summary p {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
  margin-bottom: 4px;
}

.student-name {
  color: #60a5fa !important;
  font-weight: 700 !important;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-textarea {
  width: 100%;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  resize: vertical;
  transition: all 0.3s;
}

.form-textarea::placeholder {
  color: #64748b;
}

.form-textarea:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 20px 28px;
  background: rgba(15, 23, 42, 0.6);
  border-top: 2px solid #334155;
}

.modal-btn {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-cancel {
  background: #475569;
  color: #ffffff;
}

.btn-cancel:hover:not(:disabled) {
  background: #334155;
  transform: translateY(-2px);
}

.btn-reject {
  background: #ef4444;
  color: #ffffff;
}

.btn-reject:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.5);
}

.modal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .professor-dashboard {
    padding: 20px 12px;
  }

  .hero-section {
    padding: 24px;
  }

  .hero-greeting h1 {
    font-size: 28px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filters-header {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }

  .collaborators-list {
    flex-direction: column;
  }

  .collaborator-chip {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
