<!-- frontend/src/views/Student/ProjectDetail.vue -->
<template>
  <div class="project-detail-page">
    <div class="container">
      
      <!-- Header -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyecto...</p>
      </div>

      <!-- Project Content -->
      <div v-else-if="project" class="project-content">
        
        <!-- Hero Section -->
        <div class="project-hero">
          <div class="hero-status" :class="getStatusClass(project.estado)">
            <span class="status-badge">{{ getStatusText(project.estado) }}</span>
            <span class="project-code">{{ project.codigo_proyecto }}</span>
          </div>
          <h1 class="project-title">{{ project.nombre }}</h1>
          <div class="project-meta">
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Creado: {{ formatDate(project.created_at) }}
            </div>
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Actualizado: {{ formatDate(project.updated_at) }}
            </div>
          </div>
        </div>

        <!-- Main Grid -->
        <div class="content-grid">
          
          <!-- Left Column -->
          <div class="main-column">
            
            <!-- Descripción -->
            <div class="section-card">
              <div class="section-header">
                <h2>📋 Descripción</h2>
              </div>
              <div class="section-content">
                <p class="description-text">{{ project.descripcion }}</p>
              </div>
            </div>

            <!-- Objetivos -->
            <div class="section-card">
              <div class="section-header">
                <h2>🎯 Objetivos</h2>
              </div>
              <div class="section-content">
                <pre class="objectives-text">{{ project.objetivos }}</pre>
              </div>
            </div>

            <!-- Comentarios -->
            <div v-if="project.comentarios_profesor || project.comentarios_financiera" class="section-card comments-card">
              <div class="section-header">
                <h2>💬 Comentarios</h2>
              </div>
              <div class="section-content">
                <div v-if="project.comentarios_profesor" class="comment-block">
                  <div class="comment-header">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    <strong>Profesor Asesor</strong>
                  </div>
                  <p class="comment-text">{{ project.comentarios_profesor }}</p>
                </div>

                <div v-if="project.comentarios_financiera" class="comment-block">
                  <div class="comment-header">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                      <path d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
                    </svg>
                    <strong>Área Financiera</strong>
                  </div>
                  <p class="comment-text">{{ project.comentarios_financiera }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Sidebar -->
          <div class="sidebar-column">
            
            <!-- Equipo -->
            <div class="info-card">
              <div class="info-header">
                <h3>👥 Equipo de Trabajo</h3>
              </div>
              <div class="info-body">
                <!-- Estudiante Principal -->
                <div class="team-member member-owner">
                  <div class="member-avatar">
                    {{ getInitials(project.estudiante.nombre) }}
                  </div>
                  <div class="member-info">
                    <strong>{{ project.estudiante.nombre }}</strong>
                    <span class="member-role">👑 Creador</span>
                    <span class="member-email">{{ project.estudiante.email }}</span>
                  </div>
                </div>

                <!-- Colaboradores -->
                <div v-if="members.length > 0" class="collaborators-section">
                  <div class="collab-divider">
                    <span>Colaboradores ({{ members.length }})</span>
                  </div>
                  <div 
                    v-for="member in members" 
                    :key="member.id"
                    class="team-member member-collab"
                  >
                    <div class="member-avatar collab-avatar">
                      {{ getInitials(member.student.nombre_completo) }}
                    </div>
                    <div class="member-info">
                      <strong>{{ member.student.nombre_completo }}</strong>
                      <span class="member-role">🤝 Colaborador</span>
                      <span class="member-email">{{ member.student.email }}</span>
                    </div>
                  </div>
                </div>

                <!-- Profesor -->
                <div class="collab-divider">
                  <span>Asesor</span>
                </div>
                <div class="team-member member-professor">
                  <div class="member-avatar professor-avatar">
                    {{ getInitials(project.profesor.nombre) }}
                  </div>
                  <div class="member-info">
                    <strong>{{ project.profesor.nombre }}</strong>
                    <span class="member-role">👨‍🏫 Profesor Asesor</span>
                    <span class="member-email">{{ project.profesor.email }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Presupuesto -->
            <div class="info-card budget-card">
              <div class="info-header">
                <h3>💰 Presupuesto</h3>
              </div>
              <div class="info-body">
                <div class="budget-item">
                  <span class="budget-label">Estimado</span>
                  <span class="budget-value">{{ formatCurrency(project.presupuesto_estimado) }}</span>
                </div>
                <div v-if="project.presupuesto_asignado" class="budget-item highlight">
                  <span class="budget-label">Asignado</span>
                  <span class="budget-value">{{ formatCurrency(project.presupuesto_asignado) }}</span>
                </div>
                <div v-if="project.presupuesto_ejecutado" class="budget-item">
                  <span class="budget-label">Ejecutado</span>
                  <span class="budget-value executed">{{ formatCurrency(project.presupuesto_ejecutado) }}</span>
                </div>
                <div v-if="project.presupuesto_asignado" class="budget-item">
                  <span class="budget-label">Disponible</span>
                  <span class="budget-value available">{{ formatCurrency(project.presupuesto_asignado - project.presupuesto_ejecutado) }}</span>
                </div>

                <!-- Barra de progreso -->
                <div v-if="project.presupuesto_asignado" class="budget-progress">
                  <div class="progress-header">
                    <span>Ejecución</span>
                    <span>{{ calculatePercentage(project.presupuesto_ejecutado, project.presupuesto_asignado) }}%</span>
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
            </div>

            <!-- Acciones -->
            <div class="actions-card">
              <button 
                v-if="project.estado === 'borrador'" 
                @click="editProject" 
                class="action-button btn-edit"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar Proyecto
              </button>

              <button 
                v-if="project.estado === 'activo' && project.presupuesto_asignado" 
                @click="viewExpenses" 
                class="action-button btn-expenses"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
                Ver Gastos
              </button>

              <button 
                v-if="project.estado === 'borrador'" 
                @click="submitProject" 
                class="action-button btn-submit"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Enviar para Revisión
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-state">
        <div class="error-icon">⚠️</div>
        <h2>Proyecto no encontrado</h2>
        <p>No se pudo cargar la información del proyecto</p>
        <button @click="goBack" class="btn-back-error">Volver al Dashboard</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'
import membersApi from '../../api/members'

export default {
  name: 'ProjectDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const project = ref(null)
    const members = ref([])
    const loading = ref(true)
    
    const projectId = parseInt(route.params.id)
    
    const loadProject = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjectById(projectId)
        project.value = response.data
        console.log('✅ Proyecto cargado:', project.value)
        
        // Cargar colaboradores
        await loadMembers()
      } catch (err) {
        console.error('❌ Error cargando proyecto:', err)
      } finally {
        loading.value = false
      }
    }
    
    const loadMembers = async () => {
      try {
        const response = await membersApi.getMembers(projectId)
        members.value = response.data
        console.log('✅ Colaboradores:', members.value.length)
      } catch (err) {
        console.error('Error cargando colaboradores:', err)
        members.value = []
      }
    }
    
    const goBack = () => router.push('/student')
    const editProject = () => router.push(`/student/edit-project/${projectId}`)
    const viewExpenses = () => router.push(`/student/project/${projectId}/expenses`)
    
    const submitProject = async () => {
      if (!confirm('¿Enviar proyecto para revisión del profesor?')) return
      
      try {
        await projectsApi.submitProject(projectId)
        alert('✅ Proyecto enviado para revisión')
        loadProject()
      } catch (err) {
        alert('❌ Error al enviar el proyecto')
      }
    }
    
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
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
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
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    onMounted(() => {
      loadProject()
    })
    
    return {
      project,
      members,
      loading,
      goBack,
      editProject,
      viewExpenses,
      submitProject,
      getStatusClass,
      getStatusText,
      formatDate,
      formatCurrency,
      calculatePercentage,
      getProgressClass,
      getInitials
    }
  }
}
</script>

<style scoped>
/* Base */
.project-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
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
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: #334155;
  border-color: #d4af37;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 100px 20px;
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

/* Hero Section */
.project-hero {
  padding: 40px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border: 3px solid #3b82f6;
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.hero-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.status-badge {
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 8px 16px;
  border-radius: 12px;
  letter-spacing: 0.5px;
}

.status-active { background: #10b981; color: #ffffff; }
.status-pending { background: #f59e0b; color: #ffffff; }
.status-draft { background: #64748b; color: #ffffff; }
.status-rejected { background: #ef4444; color: #ffffff; }

.project-code {
  font-size: 14px;
  font-family: 'Courier New', monospace;
  color: #d4af37;
  font-weight: 700;
  background: rgba(212, 175, 55, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
}

.project-title {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 16px;
  line-height: 1.2;
}

.project-meta {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #e0e7ff;
  font-weight: 600;
}

.meta-item svg {
  width: 18px;
  height: 18px;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
}

/* Section Cards */
.section-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.section-header h2 {
  font-size: 20px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 20px;
}

.description-text,
.objectives-text {
  color: #cbd5e1;
  font-size: 15px;
  line-height: 1.8;
  font-weight: 500;
}

.objectives-text {
  font-family: inherit;
  white-space: pre-wrap;
}

/* Comments */
.comments-card {
  background: rgba(212, 175, 55, 0.05);
  border-color: rgba(212, 175, 55, 0.3);
}

.comment-block {
  padding: 20px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 12px;
  margin-bottom: 16px;
}

.comment-block:last-child {
  margin-bottom: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.comment-header svg {
  width: 20px;
  height: 20px;
  color: #d4af37;
}

.comment-header strong {
  font-size: 14px;
  color: #d4af37;
  font-weight: 800;
  text-transform: uppercase;
}

.comment-text {
  color: #e0e7ff;
  font-size: 14px;
  line-height: 1.6;
  font-weight: 500;
}

/* Info Cards */
.info-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.info-header {
  padding: 20px 24px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 2px solid #334155;
}

.info-header h3 {
  font-size: 16px;
  font-weight: 800;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-body {
  padding: 24px;
}

/* Team Members */
.team-member {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  margin-bottom: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.team-member:hover {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.05);
}

.member-owner {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.member-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 16px;
  flex-shrink: 0;
}

.collab-avatar {
  background: linear-gradient(135deg, #10b981, #059669);
}

.professor-avatar {
  background: linear-gradient(135deg, #d4af37, #b8960f);
  color: #0a0f1e;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-info strong {
  font-size: 14px;
  color: #ffffff;
  font-weight: 700;
}

.member-role {
  font-size: 12px;
  color: #d4af37;
  font-weight: 700;
}

.member-email {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.collab-divider {
  padding: 12px 0;
  margin: 16px 0;
  border-top: 2px solid #334155;
}

.collab-divider span {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Budget */
.budget-card {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(212, 175, 55, 0.05));
  border-color: rgba(212, 175, 55, 0.3);
}

.budget-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  margin-bottom: 10px;
}

.budget-item.highlight {
  background: rgba(212, 175, 55, 0.15);
  border: 2px solid rgba(212, 175, 55, 0.3);
}

.budget-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
}

.budget-value {
  font-size: 16px;
  color: #ffffff;
  font-weight: 900;
}

.budget-value.executed {
  color: #ef4444;
}

.budget-value.available {
  color: #10b981;
}

.budget-progress {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px solid #334155;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 12px;
  color: #cbd5e1;
  font-weight: 700;
}

.progress-bar {
  height: 10px;
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

/* Actions */
.actions-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-button svg {
  width: 20px;
  height: 20px;
}

.btn-edit {
  background: #f59e0b;
  color: #ffffff;
}

.btn-edit:hover {
  background: #d97706;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.btn-expenses {
  background: #10b981;
  color: #ffffff;
}

.btn-expenses:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-submit {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  color: #0a0f1e;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
}

/* Error State */
.error-state {
  text-align: center;
  padding: 100px 20px;
}

.error-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.error-state h2 {
  font-size: 28px;
  color: #ffffff;
  font-weight: 900;
  margin-bottom: 12px;
}

.error-state p {
  font-size: 16px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.btn-back-error {
  padding: 14px 28px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back-error:hover {
  background: #334155;
  border-color: #d4af37;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .sidebar-column {
    order: -1;
  }
}

@media (max-width: 768px) {
  .project-detail-page {
    padding: 20px 12px;
  }

  .project-hero {
    padding: 24px;
  }

  .project-title {
    font-size: 24px;
  }

  .section-card {
    padding: 20px;
  }
}
</style>
