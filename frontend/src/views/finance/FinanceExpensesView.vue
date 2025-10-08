<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP - Área Financiera</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
      </div>
    </nav>

    <div class="sidebar">
      <router-link to="/finance/dashboard" class="menu-item">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/finance/projects" class="menu-item">
        <span>📁</span> Todos los Proyectos
      </router-link>
      <router-link to="/finance/expenses" class="menu-item active">
        <span>💰</span> Aprobación de Gastos
      </router-link>
      <router-link to="/finance/budgets" class="menu-item">
        <span>💵</span> Asignación Presupuestal
      </router-link>
      <router-link to="/finance/reports" class="menu-item">
        <span>📈</span> Reportes
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <div class="header-actions">
          <h1>Aprobación de Gastos</h1>
          <div class="badge badge-warning-lg">
            {{ pendingCount }} Gastos Pendientes
          </div>
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
            <option value="pendiente">Pendientes</option>
            <option value="aprobado">Aprobados</option>
            <option value="rechazado">Rechazados</option>
          </select>
        </div>

        <div v-if="loading" class="loading">Cargando gastos...</div>

        <div v-else-if="expenses.length === 0" class="empty-state">
          <p>💰 No hay gastos para mostrar</p>
        </div>

        <div v-else class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Proyecto</th>
                <th>Estudiante</th>
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
                <td>{{ getStudentName(expense.estudiante_id) }}</td>
                <td>{{ expense.concepto }}</td>
                <td class="amount">${{ formatNumber(expense.monto) }}</td>
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
                  <button v-if="expense.estado === 'pendiente'" @click="approveExpense(expense.id)"
                    class="btn-icon btn-success" title="Aprobar">
                    ✅
                  </button>
                  <button v-if="expense.estado === 'pendiente'" @click="showRejectModal(expense.id)"
                    class="btn-icon btn-danger" title="Rechazar">
                    ❌
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de rechazo -->
    <div v-if="rejectModalOpen" class="modal" @click="closeRejectModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Rechazar Gasto</h2>
          <button @click="closeRejectModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Comentarios *</label>
            <textarea v-model="rejectComments" class="form-control" rows="4" placeholder="Explica la razón del rechazo"
              required></textarea>
          </div>
          <div class="form-actions">
            <button @click="confirmReject" class="btn btn-danger">Rechazar Gasto</button>
            <button @click="closeRejectModal" class="btn btn-secondary">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de detalles -->
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
            <strong>Estudiante:</strong>
            <span>{{ getStudentName(selectedExpense.estudiante_id) }}</span>
          </div>
          <div class="detail-row">
            <strong>Concepto:</strong>
            <span>{{ selectedExpense.concepto }}</span>
          </div>
          <div class="detail-row">
            <strong>Monto:</strong>
            <span class="amount-lg">${{ formatNumber(selectedExpense.monto) }}</span>
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
            <a :href="selectedExpense.soporte_url" target="_blank" class="link">📄 Ver documento</a>
          </div>
          <div v-if="selectedExpense.comentarios" class="detail-row">
            <strong>Comentarios:</strong>
            <p class="comments">{{ selectedExpense.comentarios }}</p>
          </div>

          <div v-if="selectedExpense.estado === 'pendiente'" class="approval-actions">
            <button @click="approveExpense(selectedExpense.id)" class="btn btn-success">
              ✅ Aprobar Gasto
            </button>
            <button @click="showRejectModal(selectedExpense.id)" class="btn btn-danger">
              ❌ Rechazar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { expenseService } from '@/services/expenseService'
import { projectService } from '@/services/projectService'

const router = useRouter()
const authStore = useAuthStore()

const expenses = ref([])
const projects = ref([])
const selectedExpense = ref(null)
const loading = ref(true)
const projectFilter = ref('')
const estadoFilter = ref('')
const rejectModalOpen = ref(false)
const rejectExpenseId = ref(null)
const rejectComments = ref('')

const pendingCount = computed(() => {
  return expenses.value.filter(e => e.estado === 'pendiente').length
})

const loadExpenses = async () => {
  loading.value = true
  try {
    const params = {}
    if (projectFilter.value) params.proyecto_id = projectFilter.value
    if (estadoFilter.value) params.estado = estadoFilter.value

    expenses.value = await expenseService.getAll(params)
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

const loadProjects = async () => {
  try {
    projects.value = await projectService.getAll()
  } catch (error) {
    console.error('Error:', error)
  }
}

const viewExpense = async (id) => {
  try {
    selectedExpense.value = await expenseService.getById(id)
  } catch (error) {
    console.error('Error:', error)
  }
}

const approveExpense = async (id) => {
  if (confirm('¿Aprobar este gasto?')) {
    try {
      await expenseService.approve(id, { estado: 'aprobado' })
      closeDetailModal()
      loadExpenses()
      alert('Gasto aprobado exitosamente')
    } catch (error) {
      alert('Error al aprobar gasto')
    }
  }
}

const showRejectModal = (id) => {
  rejectExpenseId.value = id
  rejectModalOpen.value = true
  closeDetailModal()
}

const closeRejectModal = () => {
  rejectModalOpen.value = false
  rejectExpenseId.value = null
  rejectComments.value = ''
}

const confirmReject = async () => {
  if (!rejectComments.value) {
    alert('Debes proporcionar comentarios')
    return
  }

  try {
    await expenseService.approve(rejectExpenseId.value, {
      estado: 'rechazado',
      comentarios: rejectComments.value
    })
    closeRejectModal()
    loadExpenses()
    alert('Gasto rechazado')
  } catch (error) {
    alert('Error al rechazar gasto')
  }
}

const closeDetailModal = () => {
  selectedExpense.value = null
}

const getProjectName = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  return project ? project.nombre : `Proyecto #${projectId}`
}

const getStudentName = (studentId) => {
  // Placeholder - deberías obtener esto del proyecto o de un endpoint de usuarios
  return `Estudiante #${studentId}`
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
/* Estilos similares a los anteriores */
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
  width: 250px;
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
  margin-left: 250px;
  margin-top: 60px;
  padding: 40px 20px;
}

.container {
  max-width: 1600px;
  margin: 0 auto;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.badge-warning-lg {
  background-color: #ffc107;
  color: #333;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 16px;
  font-weight: 600;
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
}

.amount {
  font-weight: 600;
  color: #28a745;
}

.amount-lg {
  font-size: 24px;
  font-weight: bold;
  color: #28a745;
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

.badge-success {
  background-color: #28a745;
}

.badge-danger {
  background-color: #dc3545;
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
  max-width: 700px;
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

.comments {
  background: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  color: #666;
}

.approval-actions {
  margin-top: 30px;
  display: flex;
  gap: 15px;
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

.btn-secondary {
  background-color: #6c757d;
}

.link {
  color: #007bff;
  text-decoration: none;
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
</style>
