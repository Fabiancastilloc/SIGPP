<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header admin-header">
        <div>
          <h1>👑 Panel de Administración</h1>
          <p>Gestión completa del sistema SIGPP</p>
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
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <div class="stat-value">{{ totalUsers }}</div>
            <div class="stat-label">Usuarios</div>
          </div>
        </div>
        
        <div class="stat-card card-purple">
          <div class="stat-icon">🚀</div>
          <div class="stat-info">
            <div class="stat-value">{{ activeProjects }}</div>
            <div class="stat-label">Proyectos Activos</div>
          </div>
        </div>
        
        <div class="stat-card card-orange">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-value">${{ formatMoney(totalBudget) }}</div>
            <div class="stat-label">Presupuesto Total</div>
          </div>
        </div>
      </div>

      <div class="admin-sections">
        <div class="section-card">
          <h3>📊 Proyectos</h3>
          <p>{{ totalProjects }} proyectos en el sistema</p>
          <button @click="viewProjects" class="btn-section">Ver Todos</button>
        </div>
        
        <div class="section-card">
          <h3>👥 Usuarios</h3>
          <p>{{ totalUsers }} usuarios registrados</p>
          <button @click="viewUsers" class="btn-section">Gestionar</button>
        </div>
        
        <div class="section-card">
          <h3>📋 Reportes</h3>
          <p>Generar informes y estadísticas</p>
          <button @click="viewReports" class="btn-section">Generar</button>
        </div>
        
        <div class="section-card">
          <h3>⚙️ Configuración</h3>
          <p>Ajustes del sistema</p>
          <button @click="viewSettings" class="btn-section">Configurar</button>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando datos...</p>
      </div>

      <div v-else class="projects-grid">
        <div v-for="project in recentProjects" :key="project.id" class="project-card">
          <div class="card-status" :class="getStatusClass(project.estado)">
            {{ getStatusText(project.estado) }}
          </div>
          
          <div class="card-body">
            <h3>{{ project.nombre }}</h3>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
            
            <div class="project-info">
              <div class="info-row">
                <span class="info-icon">👨‍🎓</span>
                <span>{{ project.estudiante.nombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">👨‍🏫</span>
                <span>{{ project.profesor.nombre }}</span>
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="viewProject(project.id)" class="btn-action">Ver Detalles</button>
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
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    
    const totalProjects = computed(() => projects.value.length)
    const totalUsers = computed(() => 50)
    const activeProjects = computed(() => projects.value.filter(p => p.estado === 'activo').length)
    const totalBudget = computed(() => {
      return projects.value
        .filter(p => p.presupuesto_asignado)
        .reduce((sum, p) => sum + p.presupuesto_asignado, 0)
    })
    
    const recentProjects = computed(() => projects.value.slice(0, 6))
    
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
    
    const viewProjects = () => router.push('/admin/projects')
    const viewUsers = () => router.push('/admin/users')
    const viewReports = () => router.push('/admin/reports')
    const viewSettings = () => router.push('/admin/settings')
    const viewProject = (id) => router.push(`/admin/project/${id}`)
    
    const getStatusClass = (estado) => {
      const classes = {
        'borrador': 'status-draft',
        'pendiente_profesor': 'status-pending',
        'pendiente_financiera': 'status-review',
        'activo': 'status-active'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'borrador': '📝 Borrador',
        'pendiente_profesor': '⏳ En Revisión',
        'pendiente_financiera': '💼 En Financiera',
        'activo': '✅ Activo'
      }
      return texts[estado] || estado
    }
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    
    onMounted(() => loadProjects())
    
    return {
      projects, loading, totalProjects, totalUsers, activeProjects, totalBudget, recentProjects,
      viewProjects, viewUsers, viewReports, viewSettings, viewProject,
      getStatusClass, getStatusText, formatMoney
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

.admin-header {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
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
  margin-bottom: 40px;
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
.card-purple { border-color: #8b5cf6; }
.card-orange { border-color: #f59e0b; }

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

.admin-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.section-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 2px solid var(--gray-200);
  transition: all 0.3s;
}

.section-card:hover {
  transform: translateY(-4px);
  border-color: #ef4444;
}

.section-card h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.section-card p {
  color: var(--gray-600);
  margin-bottom: 20px;
}

.btn-section {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-section:hover {
  transform: scale(1.05);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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
  border-color: #ef4444;
}

.card-status {
  padding: 10px;
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
}

.status-draft { background: #fef3c7; color: #92400e; }
.status-pending { background: #dbeafe; color: #1e40af; }
.status-review { background: #e0e7ff; color: #3730a3; }
.status-active { background: #d1fae5; color: #065f46; }

.card-body {
  padding: 20px;
}

.card-body h3 {
  font-size: 18px;
  margin-bottom: 4px;
}

.project-code {
  font-size: 12px;
  color: var(--gray-500);
  font-family: monospace;
}

.project-info {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.info-icon {
  font-size: 18px;
}

.card-actions {
  padding: 16px 20px;
  background: var(--gray-50);
  border-top: 2px solid var(--gray-200);
}

.btn-action {
  width: 100%;
  padding: 10px;
  background: var(--gray-200);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #ef4444;
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
}
</style>
