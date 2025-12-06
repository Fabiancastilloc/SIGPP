<template>
  <div class="finance-dashboard">
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
              Bienvenido, <span class="highlight">Área Financiera</span>
            </h1>
            <p>Panel de gestión presupuestal y aprobación de proyectos</p>
          </div>
        </div>

        <div class="quick-actions">
          <router-link to="/finance/approve" class="action-card">
            <div class="action-icon">💰</div>
            <div class="action-content">
              <span class="action-count">{{ pendingCount }}</span>
              <span class="action-label">Por Aprobar</span>
            </div>
          </router-link>

          <div class="action-card info">
            <div class="action-icon">✅</div>
            <div class="action-content">
              <span class="action-count">{{ activeCount }}</span>
              <span class="action-label">Activos</span>
            </div>
          </div>

          <div class="action-card success">
            <div class="action-icon">💵</div>
            <div class="action-content">
              <span class="action-count">{{ formatCurrency(totalBudget) }}</span>
              <span class="action-label">Presupuesto Total</span>
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
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">Pendientes de Aprobación</div>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ activeCount }}</div>
            <div class="stat-label">Proyectos Activos</div>
          </div>
        </div>

        <div class="stat-card card-gold">
          <div class="stat-icon-wrapper">
            <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatCurrency(executedBudget) }}</div>
            <div class="stat-label">Presupuesto Ejecutado</div>
          </div>
        </div>
      </div>

      <!-- Budget Overview Card -->
      <div class="budget-overview">
        <div class="overview-header">
          <h2 class="section-title">📊 Resumen Presupuestal Global</h2>
        </div>
        
        <div class="budget-bars">
          <div class="budget-bar-item">
            <div class="bar-header">
              <span class="bar-label">Presupuesto Asignado</span>
              <span class="bar-value">{{ formatCurrency(totalBudget) }}</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill bar-total" style="width: 100%"></div>
            </div>
          </div>

          <div class="budget-bar-item">
            <div class="bar-header">
              <span class="bar-label">Presupuesto Ejecutado</span>
              <span class="bar-value">{{ formatCurrency(executedBudget) }}</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill bar-executed" :style="{ width: executionPercentage + '%' }"></div>
            </div>
            <span class="bar-percentage">{{ executionPercentage }}%</span>
          </div>

          <div class="budget-bar-item">
            <div class="bar-header">
              <span class="bar-label">Presupuesto Disponible</span>
              <span class="bar-value available">{{ formatCurrency(totalBudget - executedBudget) }}</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill bar-available" :style="{ width: (100 - executionPercentage) + '%' }"></div>
            </div>
            <span class="bar-percentage">{{ 100 - executionPercentage }}%</span>
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
              @click="currentFilter = 'pendiente_financiera'"
              :class="['filter-chip', { active: currentFilter === 'pendiente_financiera' }]"
            >
              Pendientes ({{ pendingCount }})
            </button>
            <button 
              @click="currentFilter = 'activo'"
              :class="['filter-chip', { active: currentFilter === 'activo' }]"
            >
              Activos ({{ activeCount }})
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
        <p>{{ searchQuery ? 'Intenta con otra búsqueda' : 'Los proyectos aparecerán aquí' }}</p>
      </div>

      <!-- Projects Grid -->
      <div v-else class="projects-grid">
        <div 
          v-for="project in filteredProjects" 
          :key="project.id"
          class="project-card"
        >
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
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Profesor</span>
                  <span class="info-value">{{ project.profesor?.nombre || 'Sin asignar' }}</span>
                </div>
              </div>

              <div class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Presupuesto Solicitado</span>
                  <span class="info-value">{{ formatCurrency(project.presupuesto_estimado) }}</span>
                </div>
              </div>

              <div v-if="project.presupuesto_asignado" class="info-item">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Presupuesto Asignado</span>
                  <span class="info-value approved">{{ formatCurrency(project.presupuesto_asignado) }}</span>
                </div>
              </div>
            </div>

            <!-- 🆕 COLABORADORES SECTION -->
            <div v-if="project.members && project.members.length > 0" class="collaborators-section">
              <div class="collaborators-header">
                <svg class="collab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="collab-title">Equipo de Trabajo ({{ project.members.length }})</span>
              </div>

              <div class="collaborators-list">
                <div 
                  v-for="member in project.members.slice(0, 4)" 
                  :key="member.id" 
                  class="collaborator-chip"
                  :title="member.student.nombre_completo"
                >
                  <div class="collab-avatar">
                    {{ getInitials(member.student.nombre_completo) }}
                  </div>
                  <span class="collab-name">{{ truncate(member.student.nombre_completo, 18) }}</span>
                </div>

                <div v-if="project.members.length > 4" class="more-collabs">
                  +{{ project.members.length - 4 }} más
                </div>
              </div>
            </div>

            <!-- Progress Bar for Active Projects -->
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
              <div class="progress-footer">
                <span>Ejecutado: {{ formatCurrency(project.presupuesto_ejecutado) }}</span>
                <span class="remaining">Disponible: {{ formatCurrency(project.presupuesto_asignado - project.presupuesto_ejecutado) }}</span>
              </div>
            </div>

            <!-- Comments Badge -->
            <div v-if="project.comentarios_financiera" class="comments-badge">
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
              v-if="project.estado === 'activo'"
              @click="viewExpenses(project.id)" 
              class="action-btn btn-success"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              Gastos
            </button>

            <button 
              v-if="project.estado === 'pendiente_financiera'"
              @click="openApprovalModal(project, false)" 
              class="action-btn btn-warning"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Rechazar
            </button>

            <button 
              v-if="project.estado === 'pendiente_financiera'"
              @click="openApprovalModal(project, true)" 
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

    <!-- Approval Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ approvalMode ? '💰 Aprobar Proyecto' : '❌ Rechazar Proyecto' }}</h3>
          <button @click="closeModal" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <div class="project-summary">
            <h4>{{ selectedProject.nombre }}</h4>
            <p>{{ selectedProject.codigo_proyecto }}</p>
            <p class="student-name">👤 {{ selectedProject.estudiante.nombre }}</p>
            <p class="budget-request">💰 Solicita: {{ formatCurrency(selectedProject.presupuesto_estimado) }}</p>
          </div>

          <div v-if="approvalMode" class="form-group">
            <label class="form-label">
              Presupuesto a Asignar *
              <span class="label-hint">(Puede ser menor o igual al solicitado)</span>
            </label>
            <div class="input-with-icon">
              <span class="currency-icon">$</span>
              <input 
                v-model.number="presupuestoAsignado"
                type="number"
                class="form-input"
                :placeholder="'Máximo: ' + formatCurrency(selectedProject.presupuesto_estimado)"
                :max="selectedProject.presupuesto_estimado"
                min="0"
              />
            </div>
            <span class="form-hint">Formato: {{ formatCurrency(presupuestoAsignado || 0) }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">
              {{ approvalMode ? 'Comentarios (opcional)' : 'Motivo del rechazo *' }}
            </label>
            <textarea 
              v-model="comentarios"
              class="form-textarea"
              :placeholder="approvalMode ? 'Observaciones sobre el presupuesto asignado...' : 'Explica por qué rechazas el proyecto...'"
              rows="5"
            ></textarea>
          </div>

          <div v-if="!approvalMode" class="warning-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p>El proyecto será devuelto al estudiante y profesor para revisión.</p>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="modal-btn btn-cancel" :disabled="processing">
            Cancelar
          </button>
          <button 
            @click="confirmApproval" 
            :class="['modal-btn', approvalMode ? 'btn-approve' : 'btn-reject']"
            :disabled="processing"
          >
            <div v-if="processing" class="spinner-small"></div>
            <span v-else>{{ approvalMode ? '✅ Aprobar y Asignar Presupuesto' : '❌ Rechazar Proyecto' }}</span>
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
    const approvalMode = ref(true)
    const presupuestoAsignado = ref(0)
    const comentarios = ref('')
    const processing = ref(false)
    
    const totalProjects = computed(() => projects.value.length)
    
    const pendingCount = computed(() => {
      return projects.value.filter(p => p.estado === 'pendiente_financiera').length
    })
    
    const activeCount = computed(() => {
      return projects.value.filter(p => p.estado === 'activo').length
    })
    
    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + parseFloat(p.presupuesto_asignado || 0), 0)
    })
    
    const executedBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_ejecutado)
        .reduce((sum, p) => sum + parseFloat(p.presupuesto_ejecutado || 0), 0)
    })
    
    const executionPercentage = computed(() => {
      if (totalBudget.value === 0) return 0
      return Math.min(100, Math.round((executedBudget.value / totalBudget.value) * 100))
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
      
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    })
    
    const loadProjects = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjects()
        projects.value = response.data
        console.log('✅ Proyectos cargados:', projects.value.length)
      } catch (err) {
        console.error('❌ Error cargando proyectos:', err)
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (projectId) => {
      router.push(`/finance/project/${projectId}`)
    }
    
    const viewExpenses = (projectId) => {
      router.push(`/finance/project/${projectId}/expenses`)
    }
    
    const openApprovalModal = (project, approve) => {
      selectedProject.value = project
      approvalMode.value = approve
      presupuestoAsignado.value = approve ? parseFloat(project.presupuesto_estimado) : 0
      comentarios.value = ''
      showModal.value = true
      console.log('🔵 Modal abierto:', {
        proyecto: project.nombre,
        modo: approve ? 'APROBAR' : 'RECHAZAR'
      })
    }
    
    const closeModal = () => {
      showModal.value = false
      selectedProject.value = null
      presupuestoAsignado.value = 0
      comentarios.value = ''
    }
    
    const confirmApproval = async () => {
      // ✅ VALIDACIONES
      if (approvalMode.value && (!presupuestoAsignado.value || presupuestoAsignado.value <= 0)) {
        alert('⚠️ Debes asignar un presupuesto válido')
        return
      }
      
      if (approvalMode.value && presupuestoAsignado.value > parseFloat(selectedProject.value.presupuesto_estimado)) {
        alert('⚠️ El presupuesto asignado no puede ser mayor al solicitado')
        return
      }
      
      if (!approvalMode.value && !comentarios.value.trim()) {
        alert('⚠️ Debes agregar comentarios al rechazar un proyecto')
        return
      }
      
      processing.value = true
      try {
        console.log('📤 Enviando solicitud:', {
          projectId: selectedProject.value.id,
          aprobado: approvalMode.value,
          presupuesto_asignado: approvalMode.value ? presupuestoAsignado.value : null,
          comentarios: comentarios.value
        })

        // 🔥 AQUÍ ESTABA EL ERROR - USA activateProject NO approveFinance
        await projectsApi.activateProject(selectedProject.value.id, {
          aprobado: approvalMode.value,
          presupuesto_asignado: approvalMode.value ? presupuestoAsignado.value : null,
          comentarios: comentarios.value
        })
        
        console.log('✅ Proyecto procesado exitosamente')
        alert(approvalMode.value ? '✅ Proyecto aprobado y presupuesto asignado' : '❌ Proyecto rechazado')
        closeModal()
        await loadProjects() // Recargar proyectos
      } catch (err) {
        console.error('❌ Error al procesar el proyecto:', err)
        alert('❌ Error al procesar el proyecto: ' + (err.response?.data?.detail || err.message))
      } finally {
        processing.value = false
      }
    }
    
    const getStatusClass = (estado) => {
      const classes = {
        'pendiente_financiera': 'status-pending',
        'activo': 'status-active',
        'rechazado': 'status-rejected',
        'borrador': 'status-draft'
      }
      return classes[estado] || 'status-draft'
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'pendiente_financiera': 'Pendiente de Aprobación',
        'activo': 'Activo',
        'rechazado': 'Rechazado',
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
      approvalMode,
      presupuestoAsignado,
      comentarios,
      processing,
      totalProjects,
      pendingCount,
      activeCount,
      totalBudget,
      executedBudget,
      executionPercentage,
      filteredProjects,
      viewProject,
      viewExpenses,
      openApprovalModal,
      closeModal,
      confirmApproval,
      getStatusClass,
      getStatusText,
      truncate,
      formatCurrency,
      calculatePercentage,
      getProgressClass,
      getInitials
    }
  }
}
</script>

<style scoped>
/* BASE */
.finance-dashboard {
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
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -300px;
  left: -300px;
  animation-delay: -12s;
}

.orb-3 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
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
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
  border: 3px solid rgba(16, 185, 129, 0.3);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
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
  color: #10b981;
  text-shadow: 0 2px 8px rgba(16, 185, 129, 0.5);
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
  border-color: #10b981;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.action-card.info {
  border-left: 4px solid #3b82f6;
}

.action-card.success {
  border-left: 4px solid #d4af37;
}

.action-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(16, 185, 129, 0.3));
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.action-count {
  font-size: 24px;
  font-weight: 900;
  color: #10b981;
  line-height: 1;
}

.action-label {
  font-size: 12px;
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
  font-size: 32px;
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

/* BUDGET OVERVIEW */
.budget-overview {
  padding: 32px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.overview-header {
  margin-bottom: 28px;
}

.section-title {
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
}

.budget-bars {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.budget-bar-item {
  position: relative;
}

.bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bar-label {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.bar-value {
  font-size: 18px;
  color: #ffffff;
  font-weight: 900;
}

.bar-value.available {
  color: #10b981;
}

.bar-container {
  height: 20px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.bar-total {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.bar-executed {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.bar-available {
  background: linear-gradient(90deg, #10b981, #059669);
}

.bar-percentage {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
  text-align: right;
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
  border-color: #10b981;
  color: #ffffff;
}

.filter-chip.active {
  background: linear-gradient(135deg, #10b981, #059669);
  border-color: #10b981;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
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
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
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
  border-top-color: #10b981;
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
  border-color: #10b981;
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

.status-rejected {
  background: #ef4444;
  color: #ffffff;
}

.status-draft {
  background: #64748b;
  color: #ffffff;
}

.project-code {
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: #10b981;
  font-weight: 700;
  background: rgba(16, 185, 129, 0.15);
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

.info-value.approved {
  color: #10b981;
  font-weight: 900;
}

/* 🆕 COLABORADORES SECTION */
.collaborators-section {
  margin-top: 20px;
  padding: 16px;
  background: rgba(59, 130, 246, 0.05);
  border: 2px solid rgba(59, 130, 246, 0.2);
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
  color: #3b82f6;
  flex-shrink: 0;
}

.collab-title {
  font-size: 13px;
  color: #3b82f6;
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
  background: rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.collab-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
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

/* PROGRESS */
.progress-section {
  margin-top: 20px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 12px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.progress-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.progress-value {
  font-size: 16px;
  color: #d4af37;
  font-weight: 900;
}

.progress-bar {
  height: 12px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease;
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

.progress-footer {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #cbd5e1;
  font-weight: 600;
}

.remaining {
  color: #10b981;
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
  background: #ef4444;
  color: #ffffff;
}

.btn-warning:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
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
  border: 2px solid #10b981;
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
  background: rgba(16, 185, 129, 0.1);
  border: 2px solid rgba(16, 185, 129, 0.3);
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

.budget-request {
  color: #10b981 !important;
  font-weight: 800 !important;
  font-size: 16px !important;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.form-label {
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-hint {
  font-size: 11px;
  color: #64748b;
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0;
}

.input-with-icon {
  position: relative;
}

.currency-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: #10b981;
  font-weight: 900;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 14px 18px 14px 42px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 16px;
  font-weight: 700;
  transition: all 0.3s;
}

.form-input::placeholder {
  color: #64748b;
  font-weight: 600;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
}

.form-hint {
  font-size: 12px;
  color: #10b981;
  font-weight: 700;
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
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
}

.warning-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
}

.warning-box svg {
  width: 24px;
  height: 24px;
  color: #ef4444;
  flex-shrink: 0;
}

.warning-box p {
  font-size: 13px;
  color: #fca5a5;
  font-weight: 600;
  line-height: 1.5;
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
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

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
  .finance-dashboard {
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
