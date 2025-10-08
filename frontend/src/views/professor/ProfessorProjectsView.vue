<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP - Profesor</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
      </div>
    </nav>

    <div class="sidebar">
      <router-link to="/professor/dashboard" class="menu-item">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/professor/projects" class="menu-item active">
        <span>📁</span> Proyectos Asesorados
      </router-link>
      <router-link to="/professor/expenses" class="menu-item">
        <span>💰</span> Gastos por Aprobar
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <h1>Proyectos Asesorados</h1>

        <div class="filters">
          <select v-model="estadoFilter" @change="loadProjects" class="form-control">
            <option value="">Todos los estados</option>
            <option value="pendiente_validacion">Pendiente Validación</option>
            <option value="validado_asesor">Validado</option>
            <option value="activo">Activo</option>
            <option value="finalizado">Finalizado</option>
          </select>
        </div>

        <div v-if="loading" class="loading">Cargando proyectos...</div>

        <div v-else-if="projects.length === 0" class="empty-state">
          <p>📁 No tienes proyectos asignados</p>
        </div>

        <div v-else class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Nombre</th>
                <th>Estudiante</th>
                <th>Estado</th>
                <th>Presupuesto</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="project in projects" :key="project.id">
                <td>{{ project.codigo_proyecto }}</td>
                <td>{{ project.nombre }}</td>
                <td>{{ project.estudiante?.nombre_completo || 'N/A' }}</td>
                <td>
                  <span :class="getEstadoBadgeClass(project.estado)">
                    {{ formatEstado(project.estado) }}
                  </span>
                </td>
                <td>${{ formatNumber(project.presupuesto_asignado || 0) }}</td>
                <td>
                  <button @click="viewProject(project.id)" class="btn-icon" title="Ver detalles">
                    👁️
                  </button>
                  <button v-if="project.estado === 'pendiente_validacion'" @click="validateProject(project.id)"
                    class="btn-icon btn-success" title="Validar">
                    ✅
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de detalles -->
    <div v-if="selectedProject" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedProject.nombre }}</h2>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <strong>Código:</strong>
            <span>{{ selectedProject.codigo_proyecto }}</span>
          </div>
          <div class="detail-row">
            <strong>Estudiante:</strong>
            <span>{{ selectedProject.estudiante?.nombre_completo }}</span>
          </div>
          <div class="detail-row">
            <strong>Estado:</strong>
            <span :class="getEstadoBadgeClass(selectedProject.estado)">
              {{ formatEstado(selectedProject.estado) }}
            </span>
          </div>
          <div class="detail-row">
            <strong>Descripción:</strong>
            <p>{{ selectedProject.descripcion }}</p>
          </div>
          <div class="detail-row">
            <strong>Objetivos:</strong>
            <p>{{ selectedProject.objetivos }}</p>
          </div>

          <div v-if="selectedProject.estado === 'pendiente_validacion'" class="validation-actions">
            <button @click="approveProject" class="btn btn-success">✅ Validar Proyecto</button>
            <button @click="rejectProject" class="btn btn-danger">❌ Rechazar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { projectService } from '@/services/projectService'

const router = useRouter()
const authStore = useAuthStore()

const projects = ref([])
const selectedProject = ref(null)
const loading = ref(true)
const estadoFilter = ref('')

const loadProjects = async () => {
  loading.value = true
  try {
    const params = estadoFilter.value ? { estado: estadoFilter.value } : {}
    projects.value = await projectService.getAll(params)
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const viewProject = async (id) => {
  try {
    selectedProject.value = await projectService.getById(id)
  } catch (error) {
    console.error('Error:', error)
  }
}

const validateProject = async (id) => {
  if (confirm('¿Validar este proyecto como asesor?')) {
    try {
      await projectService.updateStatus(id, 'validado_asesor')
      loadProjects()
    } catch (error) {
      alert('Error al validar proyecto')
    }
  }
}

const approveProject = async () => {
  try {
    await projectService.updateStatus(selectedProject.value.id, 'validado_asesor')
    closeModal()
    loadProjects()
  } catch (error) {
    alert('Error al aprobar')
  }
}

const rejectProject = async () => {
  if (confirm('¿Rechazar este proyecto?')) {
    try {
      await projectService.updateStatus(selectedProject.value.id, 'rechazado')
      closeModal()
      loadProjects()
    } catch (error) {
      alert('Error al rechazar')
    }
  }
}

const closeModal = () => {
  selectedProject.value = null
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const formatEstado = (estado) => {
  const estados = {
    'pendiente_validacion': 'Pendiente Validación',
    'validado_asesor': 'Validado',
    'activo': 'Activo',
    'finalizado': 'Finalizado'
  }
  return estados[estado] || estado
}

const getEstadoBadgeClass = (estado) => {
  const classes = {
    'pendiente_validacion': 'badge badge-warning',
    'validado_asesor': 'badge badge-info',
    'activo': 'badge badge-success',
    'finalizado': 'badge badge-primary'
  }
  return classes[estado] || 'badge'
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
/* Usa los mismos estilos que ProjectsView.vue */
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.navbar {
  background: white;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-brand h2 {
  color: #667eea;
  margin: 0;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  width: 220px;
  background: white;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  padding-top: 20px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  text-decoration: none;
  color: #333;
}

.menu-item.active {
  background-color: #667eea;
  color: white;
}

.main-content {
  margin-left: 220px;
  margin-top: 60px;
  padding: 40px 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.table th {
  background-color: #667eea;
  color: white;
}

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: #333;
}

.badge-info {
  background-color: #17a2b8;
}

.badge-success {
  background-color: #28a745;
}

.badge-primary {
  background-color: #007bff;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  margin: 0 5px;
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.form-control {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.filters {
  margin-bottom: 20px;
}

.loading {
  text-align: center;
  padding: 50px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 8px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.detail-row {
  margin-bottom: 15px;
}

.detail-row strong {
  display: block;
  margin-bottom: 5px;
  color: #667eea;
}

.validation-actions {
  margin-top: 30px;
  display: flex;
  gap: 15px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  color: white;
}

.btn-success {
  background-color: #28a745;
}

.btn-danger {
  background-color: #dc3545;
}
</style>
