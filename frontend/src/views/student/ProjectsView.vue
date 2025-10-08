<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <span class="badge">{{ authStore.user?.rol }}</span>
        <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
      </div>
    </nav>

    <div class="sidebar">
      <router-link to="/dashboard" class="menu-item">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/projects" class="menu-item active">
        <span>📁</span> Proyectos
      </router-link>
      <router-link to="/expenses" class="menu-item">
        <span>💰</span> Gastos
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <div class="header-actions">
          <h1>Mis Proyectos</h1>
          <router-link v-if="authStore.isEstudiante" to="/projects/create" class="btn btn-primary">
            + Crear Proyecto
          </router-link>
        </div>

        <div class="filters">
          <select v-model="estadoFilter" @change="loadProjects" class="form-control">
            <option value="">Todos los estados</option>
            <option value="borrador">Borrador</option>
            <option value="pendiente_validacion">Pendiente Validación</option>
            <option value="validado_asesor">Validado Asesor</option>
            <option value="activo">Activo</option>
            <option value="rechazado">Rechazado</option>
            <option value="finalizado">Finalizado</option>
          </select>
        </div>

        <div v-if="loading" class="loading">Cargando proyectos...</div>

        <div v-else-if="projects.length === 0" class="empty-state">
          <p>📁 No tienes proyectos registrados</p>
          <router-link v-if="authStore.isEstudiante" to="/projects/create" class="btn btn-primary">
            Crear mi primer proyecto
          </router-link>
        </div>

        <div v-else class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Nombre</th>
                <th>Estado</th>
                <th>Presupuesto Asignado</th>
                <th>Presupuesto Ejecutado</th>
                <th>Fecha Creación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="project in projects" :key="project.id">
                <td>{{ project.codigo_proyecto }}</td>
                <td>{{ project.nombre }}</td>
                <td>
                  <span :class="getEstadoBadgeClass(project.estado)">
                    {{ formatEstado(project.estado) }}
                  </span>
                </td>
                <td>${{ formatNumber(project.presupuesto_asignado || 0) }}</td>
                <td>${{ formatNumber(project.presupuesto_ejecutado) }}</td>
                <td>{{ formatDate(project.fecha_creacion) }}</td>
                <td>
                  <button @click="viewProject(project.id)" class="btn-icon" title="Ver detalles">
                    👁️
                  </button>
                  <button v-if="project.estado === 'borrador' && authStore.isEstudiante"
                    @click="deleteProject(project.id)" class="btn-icon btn-danger" title="Eliminar">
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de detalles del proyecto -->
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
          <div class="detail-row">
            <strong>Presupuesto Estimado:</strong>
            <span>${{ formatNumber(selectedProject.presupuesto_estimado) }}</span>
          </div>
          <div class="detail-row">
            <strong>Presupuesto Asignado:</strong>
            <span>${{ formatNumber(selectedProject.presupuesto_asignado || 0) }}</span>
          </div>
          <div class="detail-row">
            <strong>Presupuesto Ejecutado:</strong>
            <span>${{ formatNumber(selectedProject.presupuesto_ejecutado) }}</span>
          </div>

          <h3>Items de Presupuesto</h3>
          <table class="table-small">
            <thead>
              <tr>
                <th>Concepto</th>
                <th>Justificación</th>
                <th>Costo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedProject.items_presupuesto" :key="item.id">
                <td>{{ item.concepto }}</td>
                <td>{{ item.justificacion }}</td>
                <td>${{ formatNumber(item.costo) }}</td>
              </tr>
            </tbody>
          </table>
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
    console.error('Error al cargar proyectos:', error)
  } finally {
    loading.value = false
  }
}

const viewProject = async (id) => {
  try {
    selectedProject.value = await projectService.getById(id)
  } catch (error) {
    console.error('Error al cargar proyecto:', error)
  }
}

const closeModal = () => {
  selectedProject.value = null
}

const deleteProject = async (id) => {
  if (confirm('¿Estás seguro de eliminar este proyecto?')) {
    try {
      await projectService.delete(id)
      loadProjects()
    } catch (error) {
      alert('Error al eliminar proyecto')
    }
  }
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO')
}

const formatEstado = (estado) => {
  const estados = {
    'borrador': 'Borrador',
    'pendiente_validacion': 'Pendiente Validación',
    'validado_asesor': 'Validado Asesor',
    'activo': 'Activo',
    'rechazado': 'Rechazado',
    'finalizado': 'Finalizado'
  }
  return estados[estado] || estado
}

const getEstadoBadgeClass = (estado) => {
  const classes = {
    'borrador': 'badge badge-secondary',
    'pendiente_validacion': 'badge badge-warning',
    'validado_asesor': 'badge badge-info',
    'activo': 'badge badge-success',
    'rechazado': 'badge badge-danger',
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

.navbar-menu {
  display: flex;
  gap: 15px;
  align-items: center;
}

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.badge-success {
  background-color: #28a745;
}

.badge-warning {
  background-color: #ffc107;
  color: #333;
}

.badge-danger {
  background-color: #dc3545;
}

.badge-info {
  background-color: #17a2b8;
}

.badge-secondary {
  background-color: #6c757d;
}

.badge-primary {
  background-color: #007bff;
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
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
  transition: all 0.3s;
}

.menu-item:hover {
  background-color: #f0f0f0;
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

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  margin-bottom: 20px;
}

.form-control {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  max-width: 300px;
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
  font-weight: 600;
}

.table tr:hover {
  background-color: #f5f5f5;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  margin: 0 5px;
}

.btn-icon:hover {
  transform: scale(1.2);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 8px;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
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
  color: #999;
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

.table-small {
  width: 100%;
  margin-top: 10px;
  border-collapse: collapse;
}

.table-small th,
.table-small td {
  padding: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.table-small th {
  background-color: #f0f0f0;
}
</style>
