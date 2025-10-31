<template>
  <div class="audit-log-page">
    <div class="container">
      <router-link :to="`/auditor/project/${projectId}`" class="btn-back">← Volver al Proyecto</router-link>

      <div class="page-header">
        <h1>📋 Registro de Auditoría</h1>
        <p v-if="project">{{ project.nombre }}</p>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando registros...</p>
      </div>

      <div v-else class="audit-timeline">
        <div v-for="log in auditLogs" :key="log.id" class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="log-header">
              <span class="log-action">{{ log.action }}</span>
              <span class="log-date">{{ formatDate(log.created_at) }}</span>
            </div>
            <div class="log-body">
              <p><strong>Usuario:</strong> {{ log.user.nombre }}</p>
              <p><strong>Tabla:</strong> {{ log.table_name }}</p>
              <p v-if="log.comentario"><strong>Comentario:</strong> {{ log.comentario }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import projectsApi from '../../api/projects'

export default {
  name: 'AuditLog',
  setup() {
    const route = useRoute()
    const project = ref(null)
    const auditLogs = ref([])
    const loading = ref(true)
    
    const projectId = computed(() => parseInt(route.params.id))
    
    const loadData = async () => {
      loading.value = true
      try {
        const projectRes = await projectsApi.getProjectById(projectId.value)
        project.value = projectRes.data
        
        // Mock audit logs (debes crear el endpoint en backend)
        auditLogs.value = [
          { id: 1, action: 'CREAR_PROYECTO', table_name: 'projects', user: { nombre: 'Estudiante' }, created_at: new Date(), comentario: 'Proyecto creado' },
          { id: 2, action: 'ENVIAR_PROYECTO', table_name: 'projects', user: { nombre: 'Estudiante' }, created_at: new Date(), comentario: 'Enviado para revisión' },
        ]
      } catch (err) {
        console.error('Error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (date) => new Date(date).toLocaleString('es-CO')
    
    onMounted(() => loadData())
    
    return { project, auditLogs, loading, projectId, formatDate }
  }
}
</script>

<style scoped>
.audit-log-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.btn-back {
  display: inline-block;
  padding: 12px 24px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  margin-bottom: 24px;
  border: 2px solid var(--gray-200);
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.audit-timeline {
  position: relative;
  padding-left: 40px;
}

.audit-timeline::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--gray-300);
}

.timeline-item {
  position: relative;
  margin-bottom: 30px;
}

.timeline-marker {
  position: absolute;
  left: -35px;
  top: 5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f59e0b;
  border: 4px solid white;
  box-shadow: 0 0 0 2px #f59e0b;
}

.timeline-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.log-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--gray-200);
}

.log-action {
  font-weight: 700;
  color: #f59e0b;
}

.log-date {
  font-size: 14px;
  color: var(--gray-600);
}

.log-body p {
  margin: 8px 0;
  font-size: 14px;
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
</style>
