<!-- frontend/src/views/Admin/AdminProjectHistory.vue -->
<template>
  <div class="history-view">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">← Volver</button>
        <div>
          <h1>📋 Historial del Proyecto</h1>
          <p v-if="project">{{ project.nombre }}</p>
        </div>
      </div>

      <!-- Info del Proyecto -->
      <div v-if="project" class="project-info-card">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Código</span>
            <span class="info-value">{{ project.codigo_proyecto }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Estado Actual</span>
            <span class="status-badge" :class="getStatusClass(project.estado)">
              {{ getStatusText(project.estado) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Estudiante</span>
            <span class="info-value">{{ project.estudiante?.nombre_completo || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Profesor</span>
            <span class="info-value">{{ project.profesor?.nombre_completo || 'N/A' }}</span>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando historial...</p>
      </div>

      <!-- Timeline -->
      <div v-else class="timeline-container">
        <h2>🕐 Línea de Tiempo</h2>
        
        <div v-if="history.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <h3>Sin registros</h3>
          <p>Este proyecto no tiene historial de cambios</p>
        </div>

        <div v-else class="timeline">
          <div v-for="(item, index) in history" :key="item.id" class="timeline-item">
            <div class="timeline-marker" :class="getMarkerClass(item.estado_nuevo)"></div>
            <div class="timeline-content">
              <div class="timeline-header">
                <span class="timeline-status" :class="getStatusClass(item.estado_nuevo)">
                  {{ getStatusText(item.estado_nuevo) }}
                </span>
                <span class="timeline-date">{{ formatDateTime(item.timestamp) }}</span>
              </div>
              
              <div v-if="item.estado_anterior" class="timeline-change">
                <span class="old-status">{{ getStatusText(item.estado_anterior) }}</span>
                <span class="arrow">→</span>
                <span class="new-status">{{ getStatusText(item.estado_nuevo) }}</span>
              </div>
              
              <p v-if="item.comentario" class="timeline-comment">
                💬 {{ item.comentario }}
              </p>
              
              <div class="timeline-user">
                <span class="user-icon">👤</span>
                <span>{{ item.usuario?.nombre_completo || 'Sistema' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'

export default {
  name: 'AdminProjectHistory',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const projectId = route.params.id
    
    const project = ref(null)
    const history = ref([])
    const loading = ref(true)
    
    const loadData = async () => {
      loading.value = true
      try {
        // Cargar proyecto
        const projectRes = await projectsApi.getProject(projectId)
        project.value = projectRes.data
        
        // Cargar historial
        const historyRes = await projectsApi.getProjectHistory(projectId)
        history.value = historyRes.data || []
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar el historial')
      } finally {
        loading.value = false
      }
    }
    
    const goBack = () => router.back()
    
    const getStatusClass = (estado) => {
      const classes = {
        'activo': 'status-active',
        'pendiente_profesor': 'status-pending-prof',
        'pendiente_financiera': 'status-pending-fin',
        'borrador': 'status-draft',
        'rechazado': 'status-rejected'
      }
      return classes[estado] || ''
    }
    
    const getStatusText = (estado) => {
      const texts = {
        'activo': '✅ Activo',
        'pendiente_profesor': '👨‍🏫 Pend. Profesor',
        'pendiente_financiera': '💼 Pend. Financiera',
        'borrador': '📝 Borrador',
        'rechazado': '❌ Rechazado'
      }
      return texts[estado] || estado
    }
    
    const getMarkerClass = (estado) => {
      const classes = {
        'activo': 'marker-green',
        'pendiente_profesor': 'marker-blue',
        'pendiente_financiera': 'marker-purple',
        'borrador': 'marker-gray',
        'rechazado': 'marker-red'
      }
      return classes[estado] || 'marker-gray'
    }
    
    const formatDateTime = (date) => {
      return new Date(date).toLocaleString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => loadData())
    
    return {
      project,
      history,
      loading,
      goBack,
      getStatusClass,
      getStatusText,
      getMarkerClass,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.history-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.btn-back {
  background: white;
  border: 2px solid var(--gray-300);
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.page-header h1 {
  font-size: 28px;
  color: var(--gray-900);
  margin-bottom: 8px;
}

.page-header p {
  color: var(--gray-600);
  font-size: 16px;
}

/* Project Info Card */
.project-info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-500);
  text-transform: uppercase;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-900);
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  width: fit-content;
}

.status-active { background: #d1fae5; color: #065f46; }
.status-pending-prof { background: #dbeafe; color: #1e40af; }
.status-pending-fin { background: #f3e8ff; color: #7c3aed; }
.status-draft { background: #f3f4f6; color: #4b5563; }
.status-rejected { background: #fee2e2; color: #991b1b; }

/* Timeline */
.timeline-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.timeline-container h2 {
  font-size: 20px;
  margin-bottom: 24px;
  color: var(--gray-800);
}

.timeline {
  position: relative;
  padding-left: 32px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 11px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--gray-200);
}

.timeline-item {
  position: relative;
  padding-bottom: 32px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-marker {
  position: absolute;
  left: -32px;
  top: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.marker-green { background: #10b981; }
.marker-blue { background: #3b82f6; }
.marker-purple { background: #8b5cf6; }
.marker-gray { background: #6b7280; }
.marker-red { background: #ef4444; }

.timeline-content {
  background: var(--gray-50);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid var(--gray-200);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.timeline-status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
}

.timeline-date {
  font-size: 12px;
  color: var(--gray-500);
}

.timeline-change {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 13px;
}

.old-status {
  color: var(--gray-500);
  text-decoration: line-through;
}

.arrow {
  color: var(--gray-400);
}

.new-status {
  color: var(--gray-700);
  font-weight: 600;
}

.timeline-comment {
  background: white;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--gray-700);
  margin-bottom: 12px;
  border-left: 3px solid #ef4444;
}

.timeline-user {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gray-600);
}

.user-icon {
  font-size: 16px;
}

/* Loading & Empty */
.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--gray-200);
  border-top-color: #ef4444;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin-bottom: 8px;
  color: var(--gray-700);
}

.empty-state p {
  color: var(--gray-500);
}

@media (max-width: 768px) {
  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
