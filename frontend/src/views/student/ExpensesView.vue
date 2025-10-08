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
      <router-link to="/projects" class="menu-item">
        <span>📁</span> Proyectos
      </router-link>
      <router-link to="/expenses" class="menu-item active">
        <span>💰</span> Gastos
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <div class="header-actions">
          <h1>Gestión de Gastos</h1>
          <button v-if="authStore.isEstudiante" @click="showCreateModal = true" class="btn btn-primary">
            + Registrar Gasto
          </button>
        </div>

        <div class="filters">
          <select v-model="projectFilter" @change="loadExpenses" class="form-control">
            <option value="">Todos los proyectos</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.nombre }}
            </option>
          </select>

          <select v-model="estadoFilter" @change="loadExpenses" class="form-control">
            <option value="">Todos los estados</option>
            <option value="pendiente">Pendiente</option>
            <option value="aprobado">Aprobado</option>
            <option value="rechazado">Rechazado</option>
          </select>
        </div>

        <div v-if="loading" class="loading">Cargando gastos...</div>

        <div v-else-if="expenses.length === 0" class="empty-state">
          <p>💰 No hay gastos registrados</p>
          <button v-if="authStore.isEstudiante" @click="showCreateModal = true" class="btn btn-primary">
            Registrar primer gasto
          </button>
        </div>

        <div v-else class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Proyecto</th>
                <th>Concepto</th>
                <th>Monto</th>
                <th>Estado</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="expense in expenses" :key="expense.id">
                <td>{{ expense.id }}</td>
                <td>{{ getProjectName(expense.proyecto_id) }}</td>
                <td>{{ expense.concepto }}</td>
                <td>${{ formatNumber(expense.monto) }}</td>
                <td>
                  <span :class="getEstadoBadgeClass(expense.estado)">
                    {{ formatEstado(expense.estado) }}
                  </span>
                </td>
                <td>{{ formatDate(expense.creado_en) }}</td>
                <td>
                  <button @click="viewExpense(expense.id)" class="btn-icon" title="Ver detalles">
                    👁️
                  </button>
                  <button v-if="expense.estado === 'pendiente' && authStore.isEstudiante"
                    @click="deleteExpense(expense.id)" class="btn-icon btn-danger" title="Eliminar">
                    🗑️
                  </button>
                  <button v-if="expense.estado === 'pendiente' && (authStore.isProfesor || authStore.isFinanciera)"
                    @click="approveExpense(expense.id)" class="btn-icon btn-success" title="Aprobar">
                    ✅
                  </button>
                  <button v-if="expense.estado === 'pendiente' && (authStore.isProfesor || authStore.isFinanciera)"
                    @click="rejectExpense(expense.id)" class="btn-icon btn-danger" title="Rechazar">
                    ❌
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal para crear gasto -->
    <div v-if="showCreateModal" class="modal" @click="closeCreateModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Registrar Nuevo Gasto</h2>
          <button @click="closeCreateModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleCreateExpense">
            <div v-if="error" class="alert alert-error">{{ error }}</div>

            <div class="form-group">
              <label>Proyecto *</label>
              <select v-model="expenseData.proyecto_id" class="form-control" required>
                <option value="">Seleccione un proyecto</option>
                <option v-for="project in activeProjects" :key="project.id" :value="project.id">
                  {{ project.nombre }} (Disponible: ${{ formatNumber(project.presupuesto_asignado -
                    project.presupuesto_ejecutado) }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Concepto *</label>
              <input type="text" v-model="expenseData.concepto" class="form-control" placeholder="Describe el gasto"
                required minlength="5" />
            </div>

            <div class="form-group">
              <label>Monto (COP) *</label>
              <input type="number" v-model="expenseData.monto" class="form-control" placeholder="0" required min="1" />
            </div>

            <div class="form-group">
              <label>URL del Soporte (Factura/Comprobante) *</label>
              <input type="url" v-model="expenseData.soporte_url" class="form-control"
                placeholder="https://ejemplo.com/factura.pdf" required />
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loadingCreate">
                {{ loadingCreate ? 'Registrando...' : 'Registrar Gasto' }}
              </button>
              <button type="button" @click="closeCreateModal" class="btn btn-secondary">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal para ver detalles del gasto -->
    <div v-if="selectedExpense" class="modal" @click="closeDetailModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Detalles del Gasto #{{ selectedExpense.id }}</h2>
          <button @click="closeDetailModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <strong>Proyecto:</strong>
            <span>{{ getProjectName(selectedExpense.proyecto_id) }}</span>
          </div>
          <div class="detail-row">
            <strong>Concepto:</strong>
            <span>{{ selectedExpense.concepto }}</span>
          </div>
          <div class="detail-row">
            <strong>Monto:</strong>
            <span>${{ formatNumber(selectedExpense.monto) }}</span>
          </div>
          <div class="detail-row">
            <strong>Estado:</strong>
            <span :class="getEstadoBadgeClass(selectedExpense.estado)">
              {{ formatEstado(selectedExpense.estado) }}
            </span>
          </div>
          <div class="detail-row">
            <strong>Fecha de Registro:</strong>
            <span>{{ formatDate(selectedExpense.creado_en) }}</span>
          </div>
          <div class="detail-row">
            <strong>Soporte:</strong>
            <a :href="selectedExpense.soporte_url" target="_blank" class="link">Ver documento</a>
          </div>
          <div v-if="selectedExpense.comentarios" class="detail-row">
            <strong>Comentarios:</strong>
            <p>{{ selectedExpense.comentarios }}</p>
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
import { expenseService } from '@/services/expenseService'
import { projectService } from '@/services/projectService'

const router = useRouter()
const authStore = useAuthStore()

const expenses = ref([])
const projects = ref([])
const activeProjects = ref([])
const selectedExpense = ref(null)
const loading = ref(true)
const loadingCreate = ref(false)
const showCreateModal = ref(false)
const projectFilter = ref('')
const estadoFilter = ref('')
const error = ref('')

const expenseData = ref({
  proyecto_id: '',
  concepto: '',
  monto: '',
  soporte_url: ''
})

const loadExpenses = async () => {
  loading.value = true
  try {
    const params = {}
    if (projectFilter.value) params.proyecto_id = projectFilter.value
    if (estadoFilter.value) params.estado = estadoFilter.value

    expenses.value = await expenseService.getAll(params)
  } catch (error) {
    console.error('Error al cargar gastos:', error)
  } finally {
    loading.value = false
  }
}

const loadProjects = async () => {
  try {
    projects.value = await projectService.getAll()
    activeProjects.value = projects.value.filter(p => p.estado === 'activo')
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
  }
}

const viewExpense = async (id) => {
  try {
    selectedExpense.value = await expenseService.getById(id)
  } catch (error) {
    console.error('Error al cargar gasto:', error)
  }
}

const handleCreateExpense = async () => {
  loadingCreate.value = true
  error.value = ''

  try {
    await expenseService.create(expenseData.value)
    closeCreateModal()
    loadExpenses()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar gasto'
  } finally {
    loadingCreate.value = false
  }
}

const approveExpense = async (id) => {
  if (confirm('¿Aprobar este gasto?')) {
    try {
      await expenseService.approve(id, { estado: 'aprobado' })
      loadExpenses()
    } catch (error) {
      alert('Error al aprobar gasto')
    }
  }
}

const rejectExpense = async (id) => {
  const comentarios = prompt('Comentarios (opcional):')
  try {
    await expenseService.approve(id, { estado: 'rechazado', comentarios })
    loadExpenses()
  } catch (error) {
    alert('Error al rechazar gasto')
  }
}

const deleteExpense = async (id) => {
  if (confirm('¿Eliminar este gasto?')) {
    try {
      await expenseService.delete(id)
      loadExpenses()
    } catch (error) {
      alert('Error al eliminar gasto')
    }
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  expenseData.value = {
    proyecto_id: '',
    concepto: '',
    monto: '',
    soporte_url: ''
  }
  error.value = ''
}

const closeDetailModal = () => {
  selectedExpense.value = null
}

const getProjectName = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  return project ? project.nombre : `Proyecto #${projectId}`
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO')
}

const formatEstado = (estado) => {
  const estados = {
    'pendiente': 'Pendiente',
    'aprobado': 'Aprobado',
    'rechazado': 'Rechazado'
  }
  return estados[estado] || estado
}

const getEstadoBadgeClass = (estado) => {
  const classes = {
    'pendiente': 'badge badge-warning',
    'aprobado': 'badge badge-success',
    'rechazado': 'badge badge-danger'
  }
  return classes[estado] || 'badge'
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadProjects()
  loadExpenses()
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
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.form-control {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
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

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  max-width: 600px;
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 20px;
}

.detail-row {
  margin-bottom: 15px;
}

.detail-row strong {
  display: block;
  margin-bottom: 5px;
  color: #667eea;
}

.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.alert {
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
