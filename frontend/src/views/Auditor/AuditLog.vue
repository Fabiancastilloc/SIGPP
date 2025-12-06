<template>
  <div class="audit-log-page">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Back Button -->
      <div class="page-header">
        <router-link :to="`/auditor/project/${projectId}`" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Proyecto
        </router-link>
      </div>

      <!-- Hero Header -->
      <div class="hero-header">
        <div class="hero-icon">📋</div>
        <div class="hero-content">
          <h1>Registro de Auditoría</h1>
          <p v-if="project" class="project-name">{{ project.nombre }}</p>
          <span v-if="project" class="project-code">{{ project.codigo_proyecto }}</span>
        </div>
      </div>

      <!-- Stats Summary -->
      <div class="stats-summary">
        <div class="stat-item">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <div class="stat-value">{{ auditLogs.length }}</div>
            <div class="stat-label">Registros Totales</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">👥</div>
          <div class="stat-content">
            <div class="stat-value">{{ uniqueUsers }}</div>
            <div class="stat-label">Usuarios Involucrados</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">🕒</div>
          <div class="stat-content">
            <div class="stat-value">{{ daysSinceCreation }}</div>
            <div class="stat-label">Días de Actividad</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">📝</div>
          <div class="stat-content">
            <div class="stat-value">{{ actionTypes }}</div>
            <div class="stat-label">Tipos de Acción</div>
          </div>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <div class="filter-section">
          <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <span class="filter-label">Filtros activos</span>
        </div>
        
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input" 
            placeholder="Buscar en registros..."
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Analizando registros de auditoría...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredLogs.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>Sin Registros de Auditoría</h3>
        <p>No hay actividad registrada para este proyecto</p>
      </div>

      <!-- Timeline -->
      <div v-else class="audit-timeline">
        <div 
          v-for="(log, index) in filteredLogs" 
          :key="log.id" 
          class="timeline-item"
          :class="{ 'animate-in': true }"
          :style="{ animationDelay: `${index * 0.05}s` }"
        >
          <div class="timeline-marker" :class="getActionClass(log.action)">
            <svg class="marker-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path v-html="getActionIcon(log.action)" />
            </svg>
          </div>

          <div class="timeline-content">
            <!-- Log Header -->
            <div class="log-header">
              <div class="log-title">
                <span :class="['log-badge', getActionClass(log.action)]">
                  {{ getActionLabel(log.action) }}
                </span>
                <span class="log-table">{{ formatTableName(log.table_name) }}</span>
              </div>
              <div class="log-meta">
                <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="log-date">{{ formatDate(log.created_at) }}</span>
              </div>
            </div>

            <!-- Log Body -->
            <div class="log-body">
              <div class="log-info-row">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Usuario</span>
                  <span class="info-value">{{ log.user.nombre }}</span>
                </div>
              </div>

              <div v-if="log.comentario" class="log-info-row">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                </svg>
                <div class="info-content">
                  <span class="info-label">Comentario</span>
                  <span class="info-value">{{ log.comentario }}</span>
                </div>
              </div>

              <!-- Changes Detail (if available) -->
              <div v-if="log.changes" class="changes-section">
                <div class="changes-header">
                  <svg class="changes-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Cambios Registrados</span>
                </div>
                <div class="changes-content">
                  <pre>{{ formatChanges(log.changes) }}</pre>
                </div>
              </div>

              <!-- Record ID -->
              <div class="log-footer">
                <span class="record-id">ID: {{ log.id }}</span>
                <span class="record-table">Tabla: {{ log.table_name }}</span>
              </div>
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
// import auditApi from '../../api/audit' // Cuando esté disponible el endpoint

export default {
  name: 'AuditLog',
  setup() {
    const route = useRoute()
    const project = ref(null)
    const auditLogs = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    
    const projectId = computed(() => parseInt(route.params.id))

    const uniqueUsers = computed(() => {
      const users = new Set(auditLogs.value.map(log => log.user.nombre))
      return users.size
    })

    const daysSinceCreation = computed(() => {
      if (!auditLogs.value.length) return 0
      const oldest = new Date(auditLogs.value[auditLogs.value.length - 1].created_at)
      const now = new Date()
      return Math.floor((now - oldest) / (1000 * 60 * 60 * 24))
    })

    const actionTypes = computed(() => {
      const types = new Set(auditLogs.value.map(log => log.action))
      return types.size
    })

    const filteredLogs = computed(() => {
      if (!searchQuery.value) return auditLogs.value
      const query = searchQuery.value.toLowerCase()
      return auditLogs.value.filter(log => 
        log.action.toLowerCase().includes(query) ||
        log.user.nombre.toLowerCase().includes(query) ||
        log.comentario?.toLowerCase().includes(query) ||
        log.table_name.toLowerCase().includes(query)
      )
    })
    
    const loadData = async () => {
      loading.value = true
      try {
        const projectRes = await projectsApi.getProjectById(projectId.value)
        project.value = projectRes.data
        
        // 🔄 TEMPORAL: Mock audit logs (reemplazar cuando el endpoint esté listo)
        // const auditRes = await auditApi.getProjectAudit(projectId.value)
        // auditLogs.value = auditRes.data
        
        auditLogs.value = [
          { 
            id: 1, 
            action: 'CREATE', 
            table_name: 'projects', 
            user: { nombre: 'Juan Estudiante' }, 
            created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000), 
            comentario: 'Proyecto creado inicialmente',
            changes: { nombre: project.value.nombre, descripcion: project.value.descripcion }
          },
          { 
            id: 2, 
            action: 'UPDATE', 
            table_name: 'projects', 
            user: { nombre: 'Juan Estudiante' }, 
            created_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000), 
            comentario: 'Actualización de descripción del proyecto',
            changes: { descripcion: { old: 'Desc anterior', new: 'Nueva descripción' } }
          },
          { 
            id: 3, 
            action: 'SUBMIT', 
            table_name: 'projects', 
            user: { nombre: 'Juan Estudiante' }, 
            created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), 
            comentario: 'Proyecto enviado para revisión'
          },
          { 
            id: 4, 
            action: 'APPROVE', 
            table_name: 'projects', 
            user: { nombre: 'Prof. María García' }, 
            created_at: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000), 
            comentario: 'Proyecto aprobado por el profesor'
          },
          { 
            id: 5, 
            action: 'VALIDATE', 
            table_name: 'projects', 
            user: { nombre: 'Comité Validación' }, 
            created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), 
            comentario: 'Proyecto validado por el comité académico'
          },
          { 
            id: 6, 
            action: 'BUDGET_ASSIGN', 
            table_name: 'projects', 
            user: { nombre: 'Área Financiera' }, 
            created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), 
            comentario: 'Presupuesto asignado al proyecto',
            changes: { presupuesto_asignado: project.value.presupuesto_asignado }
          },
          { 
            id: 7, 
            action: 'ACTIVATE', 
            table_name: 'projects', 
            user: { nombre: 'Área Financiera' }, 
            created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), 
            comentario: 'Proyecto activado para ejecución'
          },
          { 
            id: 8, 
            action: 'EXPENSE_CREATE', 
            table_name: 'expenses', 
            user: { nombre: 'Juan Estudiante' }, 
            created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), 
            comentario: 'Registro de primer gasto del proyecto'
          }
        ].reverse() // Más recientes primero
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar los datos de auditoría')
      } finally {
        loading.value = false
      }
    }

    const getActionClass = (action) => {
      const classes = {
        'CREATE': 'action-create',
        'UPDATE': 'action-update',
        'DELETE': 'action-delete',
        'SUBMIT': 'action-submit',
        'APPROVE': 'action-approve',
        'REJECT': 'action-reject',
        'VALIDATE': 'action-validate',
        'BUDGET_ASSIGN': 'action-budget',
        'ACTIVATE': 'action-activate',
        'EXPENSE_CREATE': 'action-expense'
      }
      return classes[action] || 'action-default'
    }

    const getActionLabel = (action) => {
      const labels = {
        'CREATE': 'Creación',
        'UPDATE': 'Actualización',
        'DELETE': 'Eliminación',
        'SUBMIT': 'Envío',
        'APPROVE': 'Aprobación',
        'REJECT': 'Rechazo',
        'VALIDATE': 'Validación',
        'BUDGET_ASSIGN': 'Asignación de Presupuesto',
        'ACTIVATE': 'Activación',
        'EXPENSE_CREATE': 'Registro de Gasto'
      }
      return labels[action] || action
    }

    const getActionIcon = (action) => {
      const icons = {
        'CREATE': 'M12 4v16m8-8H4',
        'UPDATE': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
        'DELETE': 'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16',
        'SUBMIT': 'M12 19l9 2-9-18-9 18 9-2zm0 0v-8',
        'APPROVE': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        'REJECT': 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
        'VALIDATE': 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z',
        'BUDGET_ASSIGN': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        'ACTIVATE': 'M13 10V3L4 14h7v7l9-11h-7z',
        'EXPENSE_CREATE': 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z'
      }
      return icons[action] || 'M12 4v16m8-8H4'
    }

    const formatTableName = (tableName) => {
      const names = {
        'projects': 'Proyectos',
        'expenses': 'Gastos',
        'users': 'Usuarios',
        'comments': 'Comentarios'
      }
      return names[tableName] || tableName
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatChanges = (changes) => {
      return JSON.stringify(changes, null, 2)
    }
    
    onMounted(() => loadData())
    
    return { 
      project, auditLogs, loading, projectId, searchQuery,
      uniqueUsers, daysSinceCreation, actionTypes, filteredLogs,
      getActionClass, getActionLabel, getActionIcon, formatTableName,
      formatDate, formatChanges
    }
  }
}
</script>

<style scoped>
/* BASE */
.audit-log-page {
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
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  top: -200px;
  right: -200px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -150px;
  left: -150px;
  animation-delay: -7s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 50%;
  left: 50%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-50px, 50px) scale(0.9); }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER */
.page-header {
  margin-bottom: 24px;
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
}

.btn-back:hover {
  background: #334155;
  border-color: #f59e0b;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* HERO HEADER */
.hero-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  border: 3px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3);
}

.hero-icon {
  font-size: 64px;
  filter: drop-shadow(0 4px 12px rgba(245, 158, 11, 0.6));
}

.hero-content h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.project-name {
  font-size: 18px;
  color: #f59e0b;
  font-weight: 700;
  margin-bottom: 6px;
  display: block;
}

.project-code {
  display: inline-block;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #64748b;
  font-weight: 700;
  background: rgba(100, 116, 139, 0.2);
  padding: 4px 12px;
  border-radius: 6px;
}

/* STATS SUMMARY */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  transition: all 0.3s;
}

.stat-item:hover {
  transform: translateY(-2px);
  border-color: #f59e0b;
}

.stat-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(245, 158, 11, 0.4));
}

.stat-value {
  font-size: 28px;
  font-weight: 900;
  color: #f59e0b;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* FILTER BAR */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  margin-bottom: 32px;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-icon {
  width: 20px;
  height: 20px;
  color: #f59e0b;
}

.filter-label {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 700;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #64748b;
}

.search-input {
  width: 100%;
  padding: 10px 16px 10px 44px;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid #334155;
  border-radius: 10px;
  color: #ffffff;
  font-weight: 600;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #f59e0b;
}

/* TIMELINE */
.audit-timeline {
  position: relative;
  padding-left: 60px;
}

.audit-timeline::before {
  content: '';
  position: absolute;
  left: 23px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #334155, rgba(51, 65, 85, 0.2));
}

.timeline-item {
  position: relative;
  margin-bottom: 32px;
  opacity: 0;
}

.timeline-item.animate-in {
  animation: slideIn 0.4s ease forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.timeline-marker {
  position: absolute;
  left: -50px;
  top: 8px;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  background: #1e293b;
  border: 3px solid;
  z-index: 2;
}

.marker-icon {
  width: 22px;
  height: 22px;
}

/* ACTION STYLES */
.action-create { border-color: #10b981; background: rgba(16, 185, 129, 0.15); }
.action-create .marker-icon { color: #10b981; }

.action-update { border-color: #3b82f6; background: rgba(59, 130, 246, 0.15); }
.action-update .marker-icon { color: #3b82f6; }

.action-delete { border-color: #ef4444; background: rgba(239, 68, 68, 0.15); }
.action-delete .marker-icon { color: #ef4444; }

.action-submit { border-color: #8b5cf6; background: rgba(139, 92, 246, 0.15); }
.action-submit .marker-icon { color: #8b5cf6; }

.action-approve { border-color: #10b981; background: rgba(16, 185, 129, 0.15); }
.action-approve .marker-icon { color: #10b981; }

.action-reject { border-color: #ef4444; background: rgba(239, 68, 68, 0.15); }
.action-reject .marker-icon { color: #ef4444; }

.action-validate { border-color: #f59e0b; background: rgba(245, 158, 11, 0.15); }
.action-validate .marker-icon { color: #f59e0b; }

.action-budget { border-color: #10b981; background: rgba(16, 185, 129, 0.15); }
.action-budget .marker-icon { color: #10b981; }

.action-activate { border-color: #f59e0b; background: rgba(245, 158, 11, 0.15); }
.action-activate .marker-icon { color: #f59e0b; }

.action-expense { border-color: #3b82f6; background: rgba(59, 130, 246, 0.15); }
.action-expense .marker-icon { color: #3b82f6; }

/* TIMELINE CONTENT */
.timeline-content {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
}

.timeline-content:hover {
  border-color: #f59e0b;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.log-header {
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.log-title {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.log-badge {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.log-badge.action-create { background: #10b981; color: #ffffff; }
.log-badge.action-update { background: #3b82f6; color: #ffffff; }
.log-badge.action-delete { background: #ef4444; color: #ffffff; }
.log-badge.action-submit { background: #8b5cf6; color: #ffffff; }
.log-badge.action-approve { background: #10b981; color: #ffffff; }
.log-badge.action-reject { background: #ef4444; color: #ffffff; }
.log-badge.action-validate { background: #f59e0b; color: #ffffff; }
.log-badge.action-budget { background: #10b981; color: #ffffff; }
.log-badge.action-activate { background: #f59e0b; color: #ffffff; }
.log-badge.action-expense { background: #3b82f6; color: #ffffff; }

.log-table {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.log-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  font-weight: 600;
}

.meta-icon {
  width: 16px;
  height: 16px;
}

.log-body {
  padding: 24px;
}

.log-info-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.info-icon {
  width: 20px;
  height: 20px;
  color: #f59e0b;
  flex-shrink: 0;
  margin-top: 2px;
}

.info-content {
  flex: 1;
}

.info-label {
  display: block;
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.info-value {
  display: block;
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 600;
  line-height: 1.4;
}

/* CHANGES SECTION */
.changes-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 2px solid #334155;
}

.changes-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 13px;
  font-weight: 700;
  color: #cbd5e1;
}

.changes-icon {
  width: 18px;
  height: 18px;
  color: #f59e0b;
}

.changes-content {
  padding: 12px;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #334155;
  border-radius: 8px;
}

.changes-content pre {
  margin: 0;
  font-size: 12px;
  color: #10b981;
  font-family: 'Courier New', monospace;
  white-space: pre-wrap;
  word-break: break-word;
}

.log-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
  margin-top: 16px;
  border-top: 1px solid #334155;
  font-size: 11px;
  color: #64748b;
  font-weight: 600;
}

.record-id {
  font-family: 'Courier New', monospace;
}

.record-table {
  font-family: 'Courier New', monospace;
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
  border-top-color: #f59e0b;
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
  padding: 100px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
}

.empty-icon {
  font-size: 96px;
  margin-bottom: 24px;
  opacity: 0.5;
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
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .audit-log-page {
    padding: 20px 12px;
  }

  .hero-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    width: 100%;
    max-width: none;
  }

  .audit-timeline {
    padding-left: 40px;
  }

  .timeline-marker {
    left: -32px;
    width: 36px;
    height: 36px;
  }

  .marker-icon {
    width: 18px;
    height: 18px;
  }

  .audit-timeline::before {
    left: 15px;
  }

  .log-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
