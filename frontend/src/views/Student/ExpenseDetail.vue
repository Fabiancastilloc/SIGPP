<template>
  <div class="expense-detail-page">
    <div class="container">
      <router-link :to="`/student/project/${projectId}/expenses`" class="btn-back">
        ← Volver a Gastos
      </router-link>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando detalle del gasto...</p>
      </div>

      <div v-else-if="expense" class="detail-wrapper">
        <div class="detail-header">
          <div class="header-left">
            <span class="category-badge">{{ getCategoryIcon(expense.categoria) }} {{ expense.categoria }}</span>
            <h1>{{ expense.concepto }}</h1>
          </div>
          <div class="amount-display">${{ formatMoney(expense.monto) }}</div>
        </div>

        <div class="detail-grid">
          <div class="detail-main">
            <div class="detail-card">
              <h3>📝 Descripción</h3>
              <p>{{ expense.descripcion || 'Sin descripción' }}</p>
            </div>

            <div class="detail-card">
              <h3>📋 Información del Gasto</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="icon">📅</span>
                  <div>
                    <span class="label">Fecha del Gasto</span>
                    <span class="value">{{ formatDate(expense.fecha) }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <span class="icon">💰</span>
                  <div>
                    <span class="label">Monto</span>
                    <span class="value">${{ formatMoney(expense.monto) }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <span class="icon">🏷️</span>
                  <div>
                    <span class="label">Categoría</span>
                    <span class="value">{{ expense.categoria }}</span>
                  </div>
                </div>

                <div v-if="expense.factura_numero" class="info-item">
                  <span class="icon">📄</span>
                  <div>
                    <span class="label">Factura</span>
                    <span class="value">{{ expense.factura_numero }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <span class="icon">🕐</span>
                  <div>
                    <span class="label">Registrado</span>
                    <span class="value">{{ formatDateTime(expense.created_at) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="expense.soporte_url" class="detail-card">
              <h3>📎 Soporte Adjunto</h3>
              <div class="soporte-preview">
                <div class="soporte-info">
                  <span class="soporte-icon">{{ getSoporteIcon(expense.soporte_url) }}</span>
                  <span class="soporte-name">{{ expense.soporte_url }}</span>
                </div>
                <button @click="downloadSoporte" class="btn btn-download">
                  ⬇️ Descargar
                </button>
              </div>
            </div>
          </div>

          <div class="detail-sidebar">
            <div class="sidebar-card">
              <h3>⚙️ Acciones</h3>
              <div class="actions-list">
                <button @click="goBack" class="btn-action primary">
                  <span class="icon">↩️</span>
                  Volver a Gastos
                </button>
                <button @click="confirmDelete" class="btn-action danger">
                  <span class="icon">🗑️</span>
                  Eliminar Gasto
                </button>
              </div>
            </div>

            <div class="sidebar-card stats">
              <h3>📊 Estadísticas</h3>
              <div class="stat-item">
                <span class="stat-label">Presupuesto del Proyecto</span>
                <span class="stat-value">${{ formatMoney(project?.presupuesto_asignado || 0) }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Total Ejecutado</span>
                <span class="stat-value executed">${{ formatMoney(project?.presupuesto_ejecutado || 0) }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Disponible</span>
                <span class="stat-value available">${{ formatMoney(available) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
      <div class="modal-box" @click.stop>
        <div class="modal-header danger">
          <h2>⚠️ Confirmar Eliminación</h2>
          <button @click="cancelDelete" class="close-btn">×</button>
        </div>
        
        <div class="modal-content">
          <div class="warning-box">
            <p><strong>¿Estás seguro de eliminar este gasto?</strong></p>
            <p>Concepto: <strong>{{ expense.concepto }}</strong></p>
            <p>Monto: <strong>${{ formatMoney(expense.monto) }}</strong></p>
          </div>
          
          <div class="alert-danger">
            <span>⚠️</span>
            <p>Esta acción no se puede deshacer. El monto se devolverá al presupuesto disponible.</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="cancelDelete" class="btn-modal btn-cancel">Cancelar</button>
          <button @click="deleteExpense" class="btn-modal btn-delete" :disabled="deleting">
            {{ deleting ? '⏳ Eliminando...' : '🗑️ Eliminar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'
import expensesApi from '../../api/expenses'

export default {
  name: 'ExpenseDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const expense = ref(null)
    const project = ref(null)
    const loading = ref(true)
    const showDeleteModal = ref(false)
    const deleting = ref(false)
    
    const projectId = computed(() => parseInt(route.params.projectId))
    const expenseId = computed(() => parseInt(route.params.expenseId))
    
    const available = computed(() => {
      if (!project.value) return 0
      return (project.value.presupuesto_asignado || 0) - (project.value.presupuesto_ejecutado || 0)
    })
    
    const loadData = async () => {
      loading.value = true
      try {
        const [expenseRes, projectRes] = await Promise.all([
          expensesApi.getExpenseById(projectId.value, expenseId.value),
          projectsApi.getProjectById(projectId.value)
        ])
        expense.value = expenseRes.data
        project.value = projectRes.data
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar detalle del gasto')
        goBack()
      } finally {
        loading.value = false
      }
    }
    
    const downloadSoporte = async () => {
      try {
        const response = await expensesApi.downloadSoporte(expense.value.soporte_url)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', expense.value.soporte_url)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        console.error('Error:', err)
        alert('Error al descargar soporte')
      }
    }
    
    const confirmDelete = () => {
      showDeleteModal.value = true
    }
    
    const cancelDelete = () => {
      showDeleteModal.value = false
    }
    
    const deleteExpense = async () => {
      deleting.value = true
      try {
        await expensesApi.deleteExpense(projectId.value, expenseId.value)
        alert('✅ Gasto eliminado exitosamente')
        router.push(`/student/project/${projectId.value}/expenses`)
      } catch (err) {
        console.error('Error:', err)
        alert('❌ Error al eliminar gasto')
      } finally {
        deleting.value = false
        showDeleteModal.value = false
      }
    }
    
    const goBack = () => {
      router.push(`/student/project/${projectId.value}/expenses`)
    }
    
    const getCategoryIcon = (category) => {
      const icons = {
        'Material': '🛠️',
        'Equipo': '💻',
        'Servicio': '⚙️',
        'Transporte': '🚗',
        'Otro': '📦'
      }
      return icons[category] || '📦'
    }
    
    const getSoporteIcon = (filename) => {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'pdf') return '📄'
      if (['jpg', 'jpeg', 'png'].includes(ext)) return '🖼️'
      return '📎'
    }
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: 'numeric' })
    const formatDateTime = (dateStr) => new Date(dateStr).toLocaleString('es-CO')
    
    onMounted(() => loadData())
    
    return {
      expense, project, loading, showDeleteModal, deleting,
      projectId, expenseId, available,
      downloadSoporte, confirmDelete, cancelDelete, deleteExpense, goBack,
      getCategoryIcon, getSoporteIcon, formatMoney, formatDate, formatDateTime
    }
  }
}
</script>

<style scoped>
.expense-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1400px;
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
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #667eea;
}

.detail-wrapper {
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  font-size: 28px;
  margin: 12px 0 0;
  color: white;
}

.category-badge {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.amount-display {
  font-size: 48px;
  font-weight: 800;
  text-align: right;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 32px;
  padding: 40px;
}

.detail-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  border: 2px solid var(--gray-200);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.detail-card h3 {
  font-size: 18px;
  margin-bottom: 16px;
  color: var(--gray-900);
}

.detail-card p {
  line-height: 1.7;
  color: var(--gray-700);
  margin: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: start;
  gap: 12px;
  padding: 16px;
  background: var(--gray-50);
  border-radius: 10px;
}

.info-item .icon {
  font-size: 24px;
}

.info-item div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 11px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.info-item .value {
  font-size: 15px;
  font-weight: 700;
  color: var(--gray-900);
}

.soporte-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--gray-50);
  border-radius: 10px;
}

.soporte-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.soporte-icon {
  font-size: 32px;
}

.soporte-name {
  font-weight: 600;
  color: var(--gray-900);
}

.btn-download {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-download:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.sidebar-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 20px;
  border: 2px solid var(--gray-200);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.sidebar-card h3 {
  font-size: 16px;
  margin-bottom: 16px;
  color: var(--gray-900);
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-action .icon {
  font-size: 18px;
}

.btn-action.primary {
  background: var(--gray-100);
  color: var(--gray-900);
}

.btn-action.danger {
  background: #fee2e2;
  color: #991b1b;
  border: 2px solid #ef4444;
}

.btn-action:hover {
  transform: translateX(4px);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 2px solid var(--gray-200);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-600);
}

.stat-value {
  font-size: 16px;
  font-weight: 800;
  color: var(--gray-900);
}

.stat-value.executed {
  color: #f59e0b;
}

.stat-value.available {
  color: #10b981;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.modal-box {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 24px;
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header.danger {
  background: #fee2e2;
  border-color: #ef4444;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #991b1b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: var(--gray-500);
  line-height: 1;
  padding: 0;
}

.modal-content {
  padding: 24px;
}

.warning-box {
  padding: 20px;
  background: var(--gray-50);
  border-radius: 12px;
  margin-bottom: 16px;
}

.warning-box p {
  margin-bottom: 8px;
}

.alert-danger {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fee2e2;
  border: 2px solid #ef4444;
  border-radius: 12px;
  color: #991b1b;
}

.alert-danger span {
  font-size: 24px;
}

.alert-danger p {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 2px solid var(--gray-200);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-modal {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-cancel {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
