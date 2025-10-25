<template>
  <div class="dashboard">
    <div class="container">
      <!-- Header del Dashboard -->
      <div class="dashboard-header">
        <div class="header-content">
          <div class="welcome-section">
            <h1>👋 ¡Hola, {{ userName }}!</h1>
            <p>Bienvenido a tu panel de gestión de proyectos</p>
          </div>
          <router-link to="/student/create-project" class="btn btn-primary btn-lg">
            <span class="btn-icon">➕</span>
            Crear Nuevo Proyecto
          </router-link>
        </div>
      </div>

      <!-- Estadísticas Rápidas -->
      <div class="stats-grid">
        <div class="stat-card stat-primary">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <div class="stat-value">{{ totalProjects }}</div>
            <div class="stat-label">Total de Proyectos</div>
          </div>
        </div>
        
        <div class="stat-card stat-warning">
          <div class="stat-icon">📝</div>
          <div class="stat-content">
            <div class="stat-value">{{ draftProjects }}</div>
            <div class="stat-label">En Borrador</div>
          </div>
        </div>
        
        <div class="stat-card stat-info">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingProjects }}</div>
            <div class="stat-label">En Revisión</div>
          </div>
        </div>
        
        <div class="stat-card stat-success">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Activos</div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-section">
        <div class="filters-bar">
          <button 
            @click="currentFilter = 'all'" 
            :class="['filter-btn', { active: currentFilter === 'all' }]"
          >
            Todos ({{ totalProjects }})
          </button>
          <button 
            @click="currentFilter = 'borrador'" 
            :class="['filter-btn', { active: currentFilter === 'borrador' }]"
          >
            Borradores ({{ draftProjects }})
          </button>
          <button 
            @click="currentFilter = 'revision'" 
            :class="['filter-btn', { active: currentFilter === 'revision' }]"
          >
            En Revisión ({{ pendingProjects }})
          </button>
          <button 
            @click="currentFilter = 'activo'" 
            :class="['filter-btn', { active: currentFilter === 'activo' }]"
          >
            Activos ({{ activeProjects }})
          </button>
        </div>
        
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="🔍 Buscar proyectos..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando tus proyectos...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredProjects.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">{{ searchQuery ? '🔍' : '📂' }}</div>
        <h3>{{ searchQuery ? 'No se encontraron proyectos' : '¡Comienza tu primer proyecto!' }}</h3>
        <p>{{ searchQuery ? 'Intenta con otros términos de búsqueda' : 'Crea una nueva propuesta de investigación' }}</p>
        <router-link v-if="!searchQuery" to="/student/create-project" class="btn btn-primary btn-lg">
          <span class="btn-icon">🚀</span>
          Crear Mi Primer Proyecto
        </router-link>
      </div>

      <!-- Lista de Proyectos -->
      <div v-else class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <div class="card-ribbon" :class="getStatusClass(project.estado)">
            {{ getStatusText(project.estado) }}
          </div>
          
          <div class="card-content">
            <div class="project-header">
              <h3 class="project-title">{{ project.nombre }}</h3>
              <span class="project-code">{{ project.codigo_proyecto }}</span>
            </div>

            <p class="project-description">{{ truncate(project.descripcion, 120) }}</p>

            <div class="project-meta">
              <div class="meta-item">
                <span class="meta-icon">👨‍🏫</span>
                <span class="meta-text">{{ project.profesor.nombre }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">💰</span>
                <span class="meta-text">${{ formatMoney(project.presupuesto_estimado) }}</span>
              </div>
            </div>

            <!-- Barra de progreso presupuestal (solo para activos) -->
            <div v-if="project.estado === 'activo' && project.presupuesto_asignado" class="budget-progress">
              <div class="progress-header">
                <span>Presupuesto Ejecutado</span>
                <span class="progress-value">{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) + '%' }"
                ></div>
              </div>
            </div>

            <!-- Alertas de comentarios -->
            <div v-if="project.comentarios_profesor" class="project-alert alert-info">
              <span class="alert-icon">💬</span>
              <span>Hay comentarios del profesor</span>
            </div>

            <div class="card-actions">
              <button @click="viewProject(project.id)" class="btn btn-secondary btn-sm">
                👁️ Ver Detalles
              </button>
              
              <button 
                v-if="project.estado === 'borrador'"
                @click="editProject(project.id)" 
                class="btn btn-outline btn-sm"
              >
                ✏️ Editar
              </button>
              
              <button 
                v-if="project.estado === 'borrador'"
                @click="submitProject(project.id)" 
                class="btn btn-primary btn-sm"
              >
                📤 Enviar
              </button>
              
              <button 
                v-if="project.estado === 'activo'"
                @click="manageExpenses(project.id)" 
                class="btn btn-success btn-sm"
              >
                💳 Gastos
              </button>
            </div>
          </div>
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
  name: 'StudentDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const projects = ref([])
    const loading = ref(true)
    const currentFilter = ref('all')
    const searchQuery = ref('')
    
    const userName = computed(() => authStore.user?.nombre_completo?.split(' ')[0] || 'Estudiante')
    
    // Estadísticas
    const totalProjects = computed(() => projects.value.length)
    const draftProjects = computed(() => projects.value.filter(p => p.estado === 'borrador').length)
    const pendingProjects = computed(() => projects.value.filter(p => 
      p.estado === 'pendiente_profesor' || p.estado === 'pendiente_financiera'
    ).length)
    const activeProjects = computed(() => projects.value.filter(p => p.estado === 'activo').length)
    
    // Proyectos filtrados
    const filteredProjects = computed(() => {
      let filtered = projects.value
      
      // Filtro por estado
      if (currentFilter.value === 'borrador') {
        filtered = filtered.filter(p => p.estado === 'borrador')
      } else if (currentFilter.value === 'revision') {
        filtered = filtered.filter(p => p.estado === 'pendiente_profesor' || p.estado === 'pendiente_financiera')
      } else if (currentFilter.value === 'activo') {
        filtered = filtered.filter(p => p.estado === 'activo')
      }
      
      // Filtro por búsqueda
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query) ||
          p.profesor.nombre.toLowerCase().includes(query)
        )
      }
      
      return filtered
    })
    
    const loadProjects = async () => {
      loading.value = true
      try {
        console.log('📡 Cargando proyectos del estudiante...')
        const response = await projectsApi.getProjects()
        projects.value = response.data
        console.log('✅ Proyectos cargados:', projects.value.length)
      } catch (err) {
        console.error('❌ Error cargando proyectos:', err)
        alert('Error al cargar proyectos. Por favor recarga la página.')
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (projectId) => {
      router.push(`/student/project/${projectId}`)
    }
    
    const editProject = (projectId) => {
      router.push(`/student/edit-project/${projectId}`)
    }
    
    const submitProject = async (projectId) => {
      if (!confirm('¿Enviar proyecto para revisión del profesor? No podrás editarlo después.')) return
      
      try {
        await projectsApi.submitProject(projectId)
        alert('✅ Proyecto enviado exitosamente para revisión')
        loadProjects()
      } catch (err) {
        console.error('Error enviando proyecto:', err)
        alert('Error al enviar proyecto')
      }
    }
    
    const manageExpenses = (projectId) => {
      router.push(`/student/project/${projectId}/expenses`)
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
    
    const truncate = (text, length) => {
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const formatMoney = (value) => {
      return new Intl.NumberFormat('es-CO').format(value)
    }
    
    const calculatePercentage = (executed, total) => {
      if (!total) return 0
      return Math.round((executed / total) * 100)
    }
    
    onMounted(() => {
      loadProjects()
    })
    
    return {
      projects,
      loading,
      currentFilter,
      searchQuery,
      userName,
      totalProjects,
      draftProjects,
      pendingProjects,
      activeProjects,
      filteredProjects,
      viewProject,
      editProject,
      submitProject,
      manageExpenses,
      getStatusClass,
      getStatusText,
      truncate,
      formatMoney,
      calculatePercentage
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 30px 0;
  min-height: calc(100vh - 70px);
  background: var(--gray-50);
}

.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px;
  border-radius: 20px;
  margin-bottom: 40px;
  color: white;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-section h1 {
  font-size: 32px;
  margin-bottom: 8px;
  color: white;
}

.welcome-section p {
  font-size: 16px;
  opacity: 0.95;
  margin: 0;
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
  border: 2px solid transparent;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-primary { border-color: #667eea; }
.stat-warning { border-color: #f59e0b; }
.stat-info { border-color: #3b82f6; }
.stat-success { border-color: #10b981; }

.stat-icon {
  font-size: 40px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 16px;
  border-radius: 12px;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--gray-600);
  font-weight: 500;
}

.filters-section {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filters-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  flex: 1;
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
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.filter-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.search-box {
  flex: 0 0 300px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
  position: relative;
  border: 2px solid var(--gray-200);
}

.project-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
  border-color: var(--primary-color);
}

.card-ribbon {
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-draft {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #92400e;
}

.status-pending {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
}

.status-review {
  background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
  color: #3730a3;
}

.status-active {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
}

.status-rejected {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
}

.card-content {
  padding: 24px;
}

.project-header {
  margin-bottom: 12px;
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

.project-description {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
  margin-bottom: 16px;
}

.project-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--gray-700);
  font-weight: 500;
}

.meta-icon {
  font-size: 16px;
}

.budget-progress {
  padding: 12px;
  background: var(--gray-50);
  border-radius: 8px;
  margin-bottom: 16px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-700);
}

.progress-value {
  color: var(--primary-color);
}

.progress-bar {
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.5s;
}

.project-alert {
  padding: 8px 12px;
  background: #dbeafe;
  border-left: 3px solid #3b82f6;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #1e40af;
  font-weight: 600;
  margin-bottom: 16px;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.card-actions .btn {
  flex: 1;
  min-width: 100px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: var(--primary-color);
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

.empty-state h3 {
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--gray-900);
}

.empty-state p {
  font-size: 16px;
  color: var(--gray-600);
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .search-box {
    flex: 1 1 100%;
  }
}
</style>
