<!-- frontend/src/views/Professor/ProfessorExpensesView.vue -->
<template>
  <div class="expenses-page">
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Proyecto
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando información...</p>
      </div>

      <div v-else>
        <!-- Project Info Hero -->
        <div class="project-hero">
          <div class="hero-left">
            <div class="hero-icon">📊</div>
            <div class="hero-content">
              <h1>{{ project?.nombre }}</h1>
              <p class="project-code">{{ project?.codigo_proyecto }}</p>
              <p class="student-info">
                👤 <strong>{{ project?.estudiante?.nombre }}</strong>
              </p>
            </div>
          </div>
        </div>

        <!-- Budget Summary -->
        <div class="budget-summary">
          <div class="summary-card card-total">
            <div class="card-icon">💰</div>
            <div class="card-content">
              <span class="card-label">Presupuesto Asignado</span>
              <span class="card-value">{{ formatCurrency(budgetSummary.asignado) }}</span>
            </div>
          </div>

          <div class="summary-card card-executed">
            <div class="card-icon">📉</div>
            <div class="card-content">
              <span class="card-label">Ejecutado</span>
              <span class="card-value">{{ formatCurrency(budgetSummary.ejecutado) }}</span>
            </div>
          </div>

          <div class="summary-card card-available">
            <div class="card-icon">💵</div>
            <div class="card-content">
              <span class="card-label">Disponible</span>
              <span class="card-value">{{ formatCurrency(budgetSummary.disponible) }}</span>
            </div>
          </div>

          <div class="summary-card card-percentage">
            <div class="card-icon">📈</div>
            <div class="card-content">
              <span class="card-label">Ejecución</span>
              <span class="card-value">{{ budgetSummary.porcentaje }}%</span>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="progress-card">
          <div class="progress-header">
            <span class="progress-title">Progreso de Ejecución Presupuestal</span>
            <span class="progress-value">{{ budgetSummary.porcentaje }}%</span>
          </div>
          <div class="progress-bar-container">
            <div 
              class="progress-bar-fill" 
              :class="getProgressClass(budgetSummary.porcentaje)"
              :style="{ width: budgetSummary.porcentaje + '%' }"
            ></div>
          </div>
          <div class="progress-footer">
            <span>{{ formatCurrency(budgetSummary.ejecutado) }} de {{ formatCurrency(budgetSummary.asignado) }}</span>
            <span class="remaining">Restante: {{ formatCurrency(budgetSummary.disponible) }}</span>
          </div>
        </div>

        <!-- Filters -->
        <div class="filters-section">
          <div class="filters-header">
            <h2 class="section-title">📋 Registro de Gastos</h2>
            
            <div class="filter-actions">
              <select v-model="categoryFilter" class="filter-select">
                <option value="">Todas las categorías</option>
                <option value="personal">Personal</option>
                <option value="equipamiento">Equipamiento</option>
                <option value="materiales">Materiales</option>
                <option value="servicios">Servicios</option>
                <option value="software">Software</option>
                <option value="transporte">Transporte</option>
                <option value="otros">Otros</option>
              </select>

              <select v-model="statusFilter" class="filter-select">
                <option value="">Todos los estados</option>
                <option value="pendiente">Pendientes</option>
                <option value="aprobado">Aprobados</option>
                <option value="rechazado">Rechazados</option>
              </select>
            </div>
          </div>

          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="Buscar por descripción o referencia..."
            />
          </div>
        </div>

        <!-- Expenses Table -->
        <div v-if="filteredExpenses.length > 0" class="expenses-table-card">
          <div class="table-container">
            <table class="expenses-table">
              <thead>
                <tr>
                  <th class="th-date">Fecha</th>
                  <th class="th-category">Categoría</th>
                  <th class="th-description">Descripción</th>
                  <th class="th-amount">Monto</th>
                  <th class="th-status">Estado</th>
                  <th class="th-actions">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="expense in filteredExpenses" 
                  :key="expense.id"
                  class="expense-row"
                  :class="getRowClass(expense.estado)"
                >
                  <td class="td-date">
                    <div class="date-cell">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>{{ formatDate(expense.fecha) }}</span>
                    </div>
                  </td>

                  <td class="td-category">
                    <span :class="['category-badge', 'cat-' + expense.categoria]">
                      {{ getCategoryIcon(expense.categoria) }}
                      {{ getCategoryName(expense.categoria) }}
                    </span>
                  </td>

                  <td class="td-description">
                    <div class="description-cell">
                      <strong>{{ expense.descripcion }}</strong>
                      <span v-if="expense.referencia" class="reference">Ref: {{ expense.referencia }}</span>
                    </div>
                  </td>

                  <td class="td-amount">
                    <span class="amount-value">{{ formatCurrency(expense.monto) }}</span>
                  </td>

                  <td class="td-status">
                    <span :class="['status-badge', 'status-' + expense.estado]">
                      {{ getStatusText(expense.estado) }}
                    </span>
                  </td>

                  <td class="td-actions">
                    <div class="action-buttons">
                      <button 
                        @click="viewExpense(expense)" 
                        class="action-btn btn-view"
                        title="Ver detalles"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>

                      <button 
                        v-if="expense.estado === 'pendiente'"
                        @click="openApprovalModal(expense, true)" 
                        class="action-btn btn-approve"
                        title="Aprobar gasto"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </button>

                      <button 
                        v-if="expense.estado === 'pendiente'"
                        @click="openApprovalModal(expense, false)" 
                        class="action-btn btn-reject"
                        title="Rechazar gasto"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="table-footer">
            <span class="footer-info">Mostrando {{ filteredExpenses.length }} de {{ expenses.length }} gastos</span>
            <span class="footer-total">Total: {{ formatCurrency(getTotalFiltered()) }}</span>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">📂</div>
          <h3>No hay gastos registrados</h3>
          <p>{{ getEmptyMessage() }}</p>
        </div>
      </div>
    </div>

    <!-- Expense Detail Modal -->
    <div v-if="selectedExpense" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>💰 Detalle del Gasto</h3>
          <button @click="closeModal" class="btn-close-modal">✕</button>
        </div>

        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">Fecha</span>
            <span class="detail-value">{{ formatDate(selectedExpense.fecha) }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Categoría</span>
            <span class="detail-value">
              {{ getCategoryIcon(selectedExpense.categoria) }}
              {{ getCategoryName(selectedExpense.categoria) }}
            </span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Descripción</span>
            <span class="detail-value">{{ selectedExpense.descripcion }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Monto</span>
            <span class="detail-value amount">{{ formatCurrency(selectedExpense.monto) }}</span>
          </div>

          <div v-if="selectedExpense.referencia" class="detail-row">
            <span class="detail-label">Referencia</span>
            <span class="detail-value">{{ selectedExpense.referencia }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Estado</span>
            <span class="detail-value">
              <span :class="['status-badge', 'status-' + selectedExpense.estado]">
                {{ getStatusText(selectedExpense.estado) }}
              </span>
            </span>
          </div>

          <div v-if="selectedExpense.comentarios_financiera" class="detail-row">
            <span class="detail-label">Comentarios del Área Financiera</span>
            <span class="detail-value">{{ selectedExpense.comentarios_financiera }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Registrado</span>
            <span class="detail-value">{{ formatDateTime(selectedExpense.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Approval Modal -->
    <div v-if="approvalModal.show" class="modal-overlay" @click="closeApprovalModal">
      <div class="modal-content approval-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ approvalModal.approve ? '✅ Aprobar Gasto' : '❌ Rechazar Gasto' }}</h3>
          <button @click="closeApprovalModal" class="btn-close-modal">✕</button>
        </div>

        <div class="modal-body">
          <div class="expense-summary">
            <h4>{{ approvalModal.expense?.descripcion }}</h4>
            <p class="expense-amount">{{ formatCurrency(approvalModal.expense?.monto) }}</p>
            <p class="expense-category">
              {{ getCategoryIcon(approvalModal.expense?.categoria) }}
              {{ getCategoryName(approvalModal.expense?.categoria) }}
            </p>
          </div>

          <div class="form-group">
            <label class="form-label">
              {{ approvalModal.approve ? 'Comentarios (opcional)' : 'Motivo del rechazo *' }}
            </label>
            <textarea 
              v-model="approvalModal.comentarios"
              class="form-textarea"
              :placeholder="approvalModal.approve ? 'Agrega observaciones sobre este gasto...' : 'Explica por qué rechazas este gasto...'"
              rows="4"
            ></textarea>
          </div>

          <div v-if="!approvalModal.approve" class="warning-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p>El estudiante será notificado del rechazo y deberá justificar o corregir este gasto.</p>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeApprovalModal" class="modal-btn btn-cancel" :disabled="approvalModal.processing">
            Cancelar
          </button>
          <button 
            @click="confirmApproval" 
            :class="['modal-btn', approvalModal.approve ? 'btn-approve' : 'btn-reject']"
            :disabled="approvalModal.processing"
          >
            <div v-if="approvalModal.processing" class="spinner-small"></div>
            <span v-else>{{ approvalModal.approve ? '✅ Aprobar Gasto' : '❌ Rechazar Gasto' }}</span>
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
  name: 'ProfessorExpensesView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const projectId = parseInt(route.params.id)

    const loading = ref(true)
    const project = ref(null)
    const expenses = ref([])
    const categoryFilter = ref('')
    const statusFilter = ref('')
    const searchQuery = ref('')
    const selectedExpense = ref(null)
    
    const approvalModal = ref({
      show: false,
      expense: null,
      approve: true,
      comentarios: '',
      processing: false
    })

    const budgetSummary = computed(() => {
      const asignado = parseFloat(project.value?.presupuesto_asignado || 0)
      const ejecutado = parseFloat(project.value?.presupuesto_ejecutado || 0)
      const disponible = asignado - ejecutado
      const porcentaje = asignado > 0 ? Math.min(100, Math.round((ejecutado / asignado) * 100)) : 0

      return { asignado, ejecutado, disponible, porcentaje }
    })

    const filteredExpenses = computed(() => {
      let filtered = expenses.value

      // Filtrar por categoría
      if (categoryFilter.value) {
        filtered = filtered.filter(e => e.categoria === categoryFilter.value)
      }

      // Filtrar por estado
      if (statusFilter.value) {
        filtered = filtered.filter(e => e.estado === statusFilter.value)
      }

      // Filtrar por búsqueda
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(e => 
          e.descripcion.toLowerCase().includes(query) ||
          (e.referencia && e.referencia.toLowerCase().includes(query))
        )
      }

      return filtered.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
    })

    const loadProject = async () => {
      try {
        const response = await projectsApi.getProjectById(projectId)
        project.value = response.data
      } catch (err) {
        console.error('Error cargando proyecto:', err)
      }
    }

    const loadExpenses = async () => {
      try {
        const response = await expensesApi.getExpenses(projectId)
        expenses.value = response.data
        console.log('Gastos cargados:', expenses.value.length)
      } catch (err) {
        console.error('Error cargando gastos:', err)
      }
    }

    const loadAll = async () => {
      loading.value = true
      await Promise.all([loadProject(), loadExpenses()])
      loading.value = false
    }

    const goBack = () => {
      router.push(`/professor/project/${projectId}`)
    }

    const viewExpense = (expense) => {
      selectedExpense.value = expense
    }

    const closeModal = () => {
      selectedExpense.value = null
    }

    const openApprovalModal = (expense, approve) => {
      approvalModal.value = {
        show: true,
        expense: expense,
        approve: approve,
        comentarios: '',
        processing: false
      }
    }

    const closeApprovalModal = () => {
      approvalModal.value = {
        show: false,
        expense: null,
        approve: true,
        comentarios: '',
        processing: false
      }
    }

    const confirmApproval = async () => {
      if (!approvalModal.value.approve && !approvalModal.value.comentarios.trim()) {
        alert('⚠️ Debes agregar un motivo al rechazar un gasto')
        return
      }

      approvalModal.value.processing = true
      try {
        await expensesApi.approveExpense(projectId, approvalModal.value.expense.id, {
          aprobado: approvalModal.value.approve,
          comentarios: approvalModal.value.comentarios
        })

        alert(approvalModal.value.approve ? '✅ Gasto aprobado exitosamente' : '❌ Gasto rechazado')
        closeApprovalModal()
        await loadAll() // Recargar todo
      } catch (err) {
        console.error('Error:', err)
        alert('❌ Error al procesar el gasto')
      } finally {
        approvalModal.value.processing = false
      }
    }

    const formatCurrency = (value) => {
      if (!value) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const formatDateTime = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getCategoryIcon = (category) => {
      const icons = {
        'personal': '👤',
        'equipamiento': '🖥️',
        'materiales': '📦',
        'servicios': '🔧',
        'software': '💿',
        'transporte': '🚗',
        'otros': '📋'
      }
      return icons[category] || '📋'
    }

    const getCategoryName = (category) => {
      const names = {
        'personal': 'Personal',
        'equipamiento': 'Equipamiento',
        'materiales': 'Materiales',
        'servicios': 'Servicios',
        'software': 'Software',
        'transporte': 'Transporte',
        'otros': 'Otros'
      }
      return names[category] || category
    }

    const getStatusText = (status) => {
      const texts = {
        'aprobado': 'Aprobado',
        'pendiente': 'Pendiente',
        'rechazado': 'Rechazado'
      }
      return texts[status] || status
    }

    const getProgressClass = (percentage) => {
      if (percentage >= 90) return 'progress-danger'
      if (percentage >= 70) return 'progress-warning'
      return 'progress-success'
    }

    const getRowClass = (status) => {
      return `row-${status}`
    }

    const getTotalFiltered = () => {
      return filteredExpenses.value.reduce((sum, e) => sum + parseFloat(e.monto), 0)
    }

    const getEmptyMessage = () => {
      if (categoryFilter.value || statusFilter.value || searchQuery.value) {
        return 'No se encontraron gastos con los filtros aplicados'
      }
      return 'Este proyecto aún no tiene gastos registrados'
    }

    onMounted(() => {
      loadAll()
    })

    return {
      loading,
      project,
      expenses,
      budgetSummary,
      categoryFilter,
      statusFilter,
      searchQuery,
      filteredExpenses,
      selectedExpense,
      approvalModal,
      goBack,
      viewExpense,
      closeModal,
      openApprovalModal,
      closeApprovalModal,
      confirmApproval,
      formatCurrency,
      formatDate,
      formatDateTime,
      getCategoryIcon,
      getCategoryName,
      getStatusText,
      getProgressClass,
      getRowClass,
      getTotalFiltered,
      getEmptyMessage
    }
  }
}
</script>

<style scoped>
/* BASE */
.expenses-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
  position: relative;
  overflow-x: hidden;
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
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
  animation: float-smooth 25s ease-in-out infinite;
}

.orb-1 {
  width: 700px;
  height: 700px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -350px;
  right: -350px;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -300px;
  left: -300px;
  animation-delay: -12s;
}

.orb-3 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 40%;
  left: 50%;
  animation-delay: -6s;
}

@keyframes float-smooth {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(60px, -60px) scale(1.15);
  }
  66% {
    transform: translate(-50px, 50px) scale(0.9);
  }
}

.container {
  max-width: 1400px;
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

/* LOADING */
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
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #cbd5e1;
  font-size: 16px;
  font-weight: 600;
}

/* PROJECT HERO */
.project-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(168, 85, 247, 0.05));
  border: 3px solid rgba(168, 85, 247, 0.3);
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(168, 85, 247, 0.3);
}

.hero-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hero-icon {
  font-size: 56px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.6));
}

.hero-content h1 {
  font-size: 28px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.project-code {
  font-size: 14px;
  font-family: 'Courier New', monospace;
  color: #d4af37;
  font-weight: 700;
  margin-bottom: 4px;
}

.student-info {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

.student-info strong {
  color: #a855f7;
  font-weight: 800;
}

/* BUDGET SUMMARY */
.budget-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.card-total {
  border-left: 4px solid #3b82f6;
}

.card-executed {
  border-left: 4px solid #ef4444;
}

.card-available {
  border-left: 4px solid #10b981;
}

.card-percentage {
  border-left: 4px solid #d4af37;
}

.card-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.3));
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-value {
  font-size: 24px;
  color: #ffffff;
  font-weight: 900;
}

/* PROGRESS CARD */
.progress-card {
  padding: 28px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.progress-title {
  font-size: 16px;
  color: #f1f5f9;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.progress-value {
  font-size: 28px;
  color: #d4af37;
  font-weight: 900;
}

.progress-bar-container {
  height: 16px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease;
}

.progress-success {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-warning {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.progress-footer {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 600;
}

.remaining {
  color: #10b981;
  font-weight: 700;
}

/* FILTERS */
.filters-section {
  margin-bottom: 24px;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.section-title {
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
}

.filter-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 16px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

/* SEARCH */
.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 14px 20px 14px 52px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

/* TABLE */
.expenses-table-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.table-container {
  overflow-x: auto;
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
}

.expenses-table thead {
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 2px solid #d4af37;
}

.expenses-table th {
  padding: 16px;
  text-align: left;
  font-size: 12px;
  color: #d4af37;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.expense-row {
  border-bottom: 1px solid #334155;
  transition: all 0.3s ease;
}

.expense-row:hover {
  background: rgba(212, 175, 55, 0.05);
}

.row-aprobado {
  background: rgba(16, 185, 129, 0.05);
}

.row-rechazado {
  background: rgba(239, 68, 68, 0.05);
}

.expenses-table td {
  padding: 16px;
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

.date-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-cell svg {
  width: 16px;
  height: 16px;
  color: #64748b;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.cat-personal {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.cat-equipamiento {
  background: rgba(168, 85, 247, 0.2);
  color: #a855f7;
}

.cat-materiales {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.cat-servicios {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.cat-software {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.cat-transporte {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.cat-otros {
  background: rgba(100, 116, 139, 0.2);
  color: #64748b;
}

.description-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.description-cell strong {
  color: #f1f5f9;
  font-weight: 700;
}

.reference {
  font-size: 11px;
  color: #64748b;
  font-family: 'Courier New', monospace;
}

.amount-value {
  font-size: 16px;
  color: #d4af37;
  font-weight: 900;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.status-aprobado {
  background: #10b981;
  color: #ffffff;
}

.status-pendiente {
  background: #f59e0b;
  color: #ffffff;
}

.status-rechazado {
  background: #ef4444;
  color: #ffffff;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.btn-view {
  background: #3b82f6;
  color: #ffffff;
}

.btn-view:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.btn-approve {
  background: #10b981;
  color: #ffffff;
}

.btn-approve:hover {
  background: #059669;
  transform: scale(1.1);
}

.btn-reject {
  background: #ef4444;
  color: #ffffff;
}

.btn-reject:hover {
  background: #dc2626;
  transform: scale(1.1);
}

/* TABLE FOOTER */
.table-footer {
  display: flex;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.6);
  border-top: 2px solid #334155;
}

.footer-info,
.footer-total {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 700;
}

.footer-total {
  color: #d4af37;
  font-weight: 900;
}

/* EMPTY STATE */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 24px;
  color: #ffffff;
  font-weight: 900;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 600;
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #1e293b;
  border: 2px solid #d4af37;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 2px solid #334155;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
}

.btn-close-modal {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(239, 68, 68, 0.2);
  border-radius: 50%;
  color: #ef4444;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-close-modal:hover {
  background: #ef4444;
  color: #ffffff;
  transform: rotate(90deg);
}

.modal-body {
  padding: 28px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding: 14px;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 10px;
  margin-bottom: 12px;
}

.detail-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
  width: 140px;
}

.detail-value {
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 700;
  text-align: right;
  flex: 1;
}

.detail-value.amount {
  font-size: 18px;
  color: #d4af37;
  font-weight: 900;
}

.expense-summary {
  padding: 20px;
  background: rgba(168, 85, 247, 0.1);
  border: 2px solid rgba(168, 85, 247, 0.3);
  border-radius: 12px;
  margin-bottom: 24px;
  text-align: center;
}

.expense-summary h4 {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
}

.expense-amount {
  font-size: 28px;
  color: #d4af37;
  font-weight: 900;
  margin-bottom: 8px;
}

.expense-category {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 700;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.form-label {
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-textarea {
  width: 100%;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  resize: vertical;
  transition: all 0.3s;
}

.form-textarea::placeholder {
  color: #64748b;
}

.form-textarea:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.warning-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
}

.warning-box svg {
  width: 24px;
  height: 24px;
  color: #ef4444;
  flex-shrink: 0;
}

.warning-box p {
  font-size: 13px;
  color: #fca5a5;
  font-weight: 600;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 20px 28px;
  background: rgba(15, 23, 42, 0.6);
  border-top: 2px solid #334155;
}

.modal-btn {
  flex: 1;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-cancel {
  background: #475569;
  color: #ffffff;
}

.btn-cancel:hover:not(:disabled) {
  background: #334155;
  transform: translateY(-2px);
}

.modal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .budget-summary {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .expenses-page {
    padding: 20px 12px;
  }

  .project-hero {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .hero-left {
    flex-direction: column;
  }

  .budget-summary {
    grid-template-columns: 1fr;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
  }

  .table-container {
    overflow-x: scroll;
  }

  .expenses-table {
    min-width: 800px;
  }

  .modal-content {
    max-width: 95%;
  }
}
</style>
