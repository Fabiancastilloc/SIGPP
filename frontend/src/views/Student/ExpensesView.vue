<!-- frontend/src/views/Student/ExpensesView.vue -->
<template>
  <div class="expenses-page">
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
            <div class="hero-icon">💰</div>
            <div class="hero-content">
              <h1>{{ project?.nombre }}</h1>
              <p class="project-code">{{ project?.codigo_proyecto }}</p>
            </div>
          </div>
          <button @click="registerExpense" class="btn-register-expense">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            Registrar Gasto
          </button>
        </div>

        <!-- Budget Summary -->
        <div class="budget-summary">
          <div class="summary-card card-total">
            <div class="card-icon">💵</div>
            <div class="card-content">
              <span class="card-label">Presupuesto Asignado</span>
              <span class="card-value">{{ formatCurrency(budgetSummary.asignado) }}</span>
            </div>
          </div>

          <div class="summary-card card-executed">
            <div class="card-icon">📊</div>
            <div class="card-content">
              <span class="card-label">Ejecutado</span>
              <span class="card-value">{{ formatCurrency(budgetSummary.ejecutado) }}</span>
            </div>
          </div>

          <div class="summary-card card-available">
            <div class="card-icon">✅</div>
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
                <option value="personal">👥 Personal</option>
                <option value="equipamiento">🖥️ Equipamiento</option>
                <option value="materiales">📦 Materiales</option>
                <option value="servicios">🔧 Servicios</option>
                <option value="software">💻 Software</option>
                <option value="transporte">🚗 Transporte</option>
                <option value="otros">📌 Otros</option>
              </select>

              <select v-model="statusFilter" class="filter-select">
                <option value="">Todos los estados</option>
                <option value="aprobado">✅ Aprobados</option>
                <option value="pendiente">⏳ Pendientes</option>
                <option value="rechazado">❌ Rechazados</option>
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
                    <span class="category-badge" :class="'cat-' + expense.categoria">
                      {{ getCategoryIcon(expense.categoria) }} {{ getCategoryName(expense.categoria) }}
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
                    <span class="status-badge" :class="'status-' + expense.estado">
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
                        @click="deleteExpense(expense.id)" 
                        class="action-btn btn-delete"
                        title="Eliminar"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
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
            <span class="footer-info">
              Mostrando {{ filteredExpenses.length }} de {{ expenses.length }} gastos
            </span>
            <span class="footer-total">
              Total: {{ formatCurrency(getTotalFiltered()) }}
            </span>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">📊</div>
          <h3>No hay gastos registrados</h3>
          <p>{{ getEmptyMessage() }}</p>
          <button @click="registerExpense" class="btn-empty-action">
            💰 Registrar Primer Gasto
          </button>
        </div>
      </div>

      <!-- Expense Detail Modal -->
      <div v-if="selectedExpense" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Detalle del Gasto</h3>
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
                {{ getCategoryIcon(selectedExpense.categoria) }} {{ getCategoryName(selectedExpense.categoria) }}
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
                <span class="status-badge" :class="'status-' + selectedExpense.estado">
                  {{ getStatusText(selectedExpense.estado) }}
                </span>
              </span>
            </div>
            <div v-if="selectedExpense.comentarios_financiera" class="detail-row">
              <span class="detail-label">Comentarios</span>
              <span class="detail-value">{{ selectedExpense.comentarios_financiera }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Registrado</span>
              <span class="detail-value">{{ formatDateTime(selectedExpense.created_at) }}</span>
            </div>
          </div>
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
  name: 'ExpensesView',
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
    
    const budgetSummary = computed(() => {
      const asignado = parseFloat(project.value?.presupuesto_asignado || 0)
      const ejecutado = parseFloat(project.value?.presupuesto_ejecutado || 0)
      const disponible = asignado - ejecutado
      const porcentaje = asignado > 0 ? Math.min(100, Math.round((ejecutado / asignado) * 100)) : 0
      
      return {
        asignado,
        ejecutado,
        disponible,
        porcentaje
      }
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
        console.log('✅ Gastos cargados:', expenses.value.length)
      } catch (err) {
        console.error('Error cargando gastos:', err)
      }
    }
    
    const loadAll = async () => {
      loading.value = true
      await Promise.all([loadProject(), loadExpenses()])
      loading.value = false
    }
    
    const goBack = () => router.push(`/student/project/${projectId}`)
    const registerExpense = () => router.push(`/student/project/${projectId}/expenses/register`)
    
    const viewExpense = (expense) => {
      selectedExpense.value = expense
    }
    
    const closeModal = () => {
      selectedExpense.value = null
    }
    
    const deleteExpense = async (expenseId) => {
      if (!confirm('¿Eliminar este gasto? Esta acción no se puede deshacer.')) return
      
      try {
        await expensesApi.deleteExpense(projectId, expenseId)
        expenses.value = expenses.value.filter(e => e.id !== expenseId)
        await loadProject() // Recargar para actualizar presupuesto ejecutado
        alert('✅ Gasto eliminado exitosamente')
      } catch (err) {
        alert('❌ Error al eliminar el gasto')
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
        personal: '👥',
        equipamiento: '🖥️',
        materiales: '📦',
        servicios: '🔧',
        software: '💻',
        transporte: '🚗',
        otros: '📌'
      }
      return icons[category] || '📌'
    }
    
    const getCategoryName = (category) => {
      const names = {
        personal: 'Personal',
        equipamiento: 'Equipamiento',
        materiales: 'Materiales',
        servicios: 'Servicios',
        software: 'Software',
        transporte: 'Transporte',
        otros: 'Otros'
      }
      return names[category] || category
    }
    
    const getStatusText = (status) => {
      const texts = {
        aprobado: '✅ Aprobado',
        pendiente: '⏳ Pendiente',
        rechazado: '❌ Rechazado'
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
      return 'Comienza registrando los gastos de tu proyecto'
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
      goBack,
      registerExpense,
      viewExpense,
      closeModal,
      deleteExpense,
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
/* Base */
.expenses-page {
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

/* Project Hero */
.project-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border: 3px solid #3b82f6;
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
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
}

.btn-register-expense {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border: none;
  border-radius: 12px;
  color: #0a0f1e;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
  white-space: nowrap;
}

.btn-register-expense:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

.btn-register-expense svg {
  width: 20px;
  height: 20px;
}

/* Budget Summary */
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

.card-total { border-left: 4px solid #3b82f6; }
.card-executed { border-left: 4px solid #ef4444; }
.card-available { border-left: 4px solid #10b981; }
.card-percentage { border-left: 4px solid #d4af37; }

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

/* Progress Card */
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

.progress-success { background: linear-gradient(90deg, #10b981, #059669); }
.progress-warning { background: linear-gradient(90deg, #f59e0b, #d97706); }
.progress-danger { background: linear-gradient(90deg, #ef4444, #dc2626); }

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

/* Filters */
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

/* Search */
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

/* Table */
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

.cat-personal { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.cat-equipamiento { background: rgba(168, 85, 247, 0.2); color: #a855f7; }
.cat-materiales { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.cat-servicios { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.cat-software { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.cat-transporte { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.cat-otros { background: rgba(100, 116, 139, 0.2); color: #64748b; }

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

.status-aprobado { background: #10b981; color: #ffffff; }
.status-pendiente { background: #f59e0b; color: #ffffff; }
.status-rechazado { background: #ef4444; color: #ffffff; }

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

.btn-delete {
  background: #ef4444;
  color: #ffffff;
}

.btn-delete:hover {
  background: #dc2626;
  transform: scale(1.1);
}

/* Table Footer */
.table-footer {
  display: flex;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.6);
  border-top: 2px solid #334155;
}

.footer-info,
.footer-total {
  font-size: 13px;
  font-weight: 700;
  color: #cbd5e1;
}

.footer-total {
  color: #d4af37;
  font-size: 16px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-icon {
  font-size: 96px;
  margin-bottom: 24px;
  opacity: 0.6;
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
  margin-bottom: 32px;
}

.btn-empty-action {
  padding: 14px 28px;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border: none;
  border-radius: 12px;
  color: #0a0f1e;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.btn-empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #1e293b;
  border: 2px solid #d4af37;
  border-radius: 16px;
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
  padding: 24px;
  border-bottom: 2px solid #334155;
}

.modal-header h3 {
  font-size: 20px;
  color: #ffffff;
  font-weight: 900;
}

.btn-close-modal {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #ef4444;
  border: none;
  color: #ffffff;
  font-size: 20px;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-close-modal:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.modal-body {
  padding: 24px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #334155;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 15px;
  color: #f1f5f9;
  font-weight: 700;
  text-align: right;
}

.detail-value.amount {
  font-size: 20px;
  color: #d4af37;
  font-weight: 900;
}

/* Responsive */
@media (max-width: 768px) {
  .expenses-page {
    padding: 20px 12px;
  }

  .project-hero {
    flex-direction: column;
    padding: 24px;
  }

  .hero-left {
    flex-direction: column;
    text-align: center;
  }

  .budget-summary {
    grid-template-columns: 1fr;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-actions {
    flex-direction: column;
  }

  .expenses-table {
    font-size: 12px;
  }

  .expenses-table th,
  .expenses-table td {
    padding: 12px 8px;
  }
}
</style>
