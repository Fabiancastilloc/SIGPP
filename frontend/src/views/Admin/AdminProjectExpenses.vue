<!-- frontend/src/views/Admin/AdminProjectExpenses.vue -->
<template>
  <div class="expenses-view-page">
    <div class="container">
      <router-link :to="`/admin`" class="btn-back">
        ← Volver al Panel
      </router-link>

      <div class="page-header">
        <h1>💳 Gastos del Proyecto</h1>
        <p v-if="project">{{ project.nombre }}</p>
        <span v-if="project" class="project-code">{{ project.codigo_proyecto }}</span>
      </div>

      <!-- Resumen Presupuestal -->
      <div class="budget-summary">
        <div class="summary-card assigned">
          <div class="card-icon">💰</div>
          <div class="card-content">
            <div class="card-value">${{ formatMoney(project?.presupuesto_asignado || 0) }}</div>
            <div class="card-label">Presupuesto Asignado</div>
          </div>
        </div>
        <div class="summary-card executed">
          <div class="card-icon">📊</div>
          <div class="card-content">
            <div class="card-value">${{ formatMoney(totalExecuted) }}</div>
            <div class="card-label">Ejecutado</div>
          </div>
        </div>
        <div class="summary-card available">
          <div class="card-icon">✅</div>
          <div class="card-content">
            <div class="card-value">${{ formatMoney(availableBudget) }}</div>
            <div class="card-label">Disponible</div>
          </div>
        </div>
        <div class="summary-card percentage">
          <div class="card-icon">📈</div>
          <div class="card-content">
            <div class="card-value">{{ executionPercentage }}%</div>
            <div class="card-label">Ejecución</div>
          </div>
        </div>
      </div>

      <!-- Barra de progreso -->
      <div class="progress-section">
        <div class="progress-header">
          <span>Ejecución Presupuestal</span>
          <span>{{ executionPercentage }}% ejecutado</span>
        </div>
        <div class="progress-bar-large">
          <div 
            class="progress-fill" 
            :class="getProgressClass(executionPercentage)"
            :style="{ width: executionPercentage + '%' }"
          ></div>
        </div>
      </div>

      <!-- Info banner -->
      <div class="info-banner">
        <span class="banner-icon">👑</span>
        <div>
          <strong>Vista de Administrador</strong>
          <p>Supervisión completa de gastos del proyecto</p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando gastos...</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="expenses.length === 0" class="empty-state">
        <div class="empty-icon">💳</div>
        <h3>Sin gastos registrados</h3>
        <p>El proyecto no tiene gastos registrados aún</p>
      </div>

      <!-- Lista de gastos -->
      <div v-else>
        <div class="filter-bar">
          <select v-model="filterCategory" class="filter-select">
            <option value="">Todas las categorías</option>
            <option value="Material">📦 Material</option>
            <option value="Equipo">🖥️ Equipo</option>
            <option value="Servicio">🔧 Servicio</option>
            <option value="Transporte">🚗 Transporte</option>
            <option value="Otro">📋 Otro</option>
          </select>
          <span class="results-count">{{ filteredExpenses.length }} gastos encontrados</span>
        </div>

        <div class="expenses-grid">
          <div v-for="expense in filteredExpenses" :key="expense.id" class="expense-card">
            <div class="expense-header">
              <div class="expense-category">
                {{ getCategoryIcon(expense.categoria) }} {{ expense.categoria }}
              </div>
              <div class="expense-date">{{ formatDate(expense.fecha) }}</div>
            </div>
            
            <div class="expense-body">
              <h4>{{ expense.concepto }}</h4>
              <p v-if="expense.descripcion">{{ truncate(expense.descripcion, 100) }}</p>
              <div class="expense-amount">${{ formatMoney(expense.monto) }}</div>
            </div>
            
            <div class="expense-footer">
              <div v-if="expense.factura_numero" class="expense-invoice">
                📄 {{ expense.factura_numero }}
              </div>
              <div class="expense-time">🕐 {{ formatDateTime(expense.created_at) }}</div>
              <a 
                v-if="expense.soporte_url" 
                :href="`http://localhost:8000/uploads/${expense.soporte_url}`" 
                target="_blank" 
                class="btn-download"
              >
                📎 Ver Soporte
              </a>
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
import expensesApi from '../../api/expenses'

export default {
  name: 'AdminProjectExpenses',
  setup() {
    const route = useRoute()
    const project = ref(null)
    const expenses = ref([])
    const loading = ref(true)
    const filterCategory = ref('')

    const projectId = computed(() => parseInt(route.params.id))

    const totalExecuted = computed(() => {
      return expenses.value.reduce((sum, e) => sum + e.monto, 0)
    })

    const availableBudget = computed(() => {
      if (!project.value) return 0
      return (project.value.presupuesto_asignado || 0) - totalExecuted.value
    })

    const executionPercentage = computed(() => {
      if (!project.value?.presupuesto_asignado) return 0
      return Math.round((totalExecuted.value / project.value.presupuesto_asignado) * 100)
    })

    const filteredExpenses = computed(() => {
      if (!filterCategory.value) return expenses.value
      return expenses.value.filter(e => e.categoria === filterCategory.value)
    })

    const loadData = async () => {
      loading.value = true
      try {
        const [projectRes, expensesRes] = await Promise.all([
          projectsApi.getProjectById(projectId.value),
          expensesApi.getExpenses(projectId.value)
        ])
        project.value = projectRes.data
        expenses.value = expensesRes.data
      } catch (err) {
        console.error('Error:', err)
      } finally {
        loading.value = false
      }
    }

    const getProgressClass = (percent) => {
      if (percent >= 90) return 'progress-danger'
      if (percent >= 70) return 'progress-warning'
      return 'progress-success'
    }

    const getCategoryIcon = (category) => {
      const icons = {
        'Material': '📦',
        'Equipo': '🖥️',
        'Servicio': '🔧',
        'Transporte': '🚗',
        'Otro': '📋'
      }
      return icons[category] || '📋'
    }

    const truncate = (text, len) => {
      if (!text) return ''
      return text.length > len ? text.substring(0, len) + '...' : text
    }

    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-CO')
    const formatDateTime = (dateStr) => new Date(dateStr).toLocaleString('es-CO')

    onMounted(loadData)

    return {
      project, expenses, loading, filterCategory, projectId,
      totalExecuted, availableBudget, executionPercentage, filteredExpenses,
      getProgressClass, getCategoryIcon, truncate,
      formatMoney, formatDate, formatDateTime
    }
  }
}
</script>

<style scoped>
.expenses-view-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
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
  border-color: #ef4444;
  color: #ef4444;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 18px;
  color: var(--gray-700);
  margin-bottom: 4px;
}

.project-code {
  font-family: monospace;
  background: var(--gray-200);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 14px;
}

/* Budget Summary */
.budget-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.summary-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
}

.summary-card.assigned { border-color: #3b82f6; }
.summary-card.executed { border-color: #f59e0b; }
.summary-card.available { border-color: #10b981; }
.summary-card.percentage { border-color: #8b5cf6; }

.card-icon { font-size: 36px; }
.card-value { font-size: 24px; font-weight: 800; color: var(--gray-900); }
.card-label { font-size: 13px; color: var(--gray-600); font-weight: 600; }

/* Progress Section */
.progress-section {
  background: white;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  margin-bottom: 12px;
  font-size: 14px;
}

.progress-bar-large {
  height: 16px;
  background: var(--gray-200);
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

/* Info Banner */
.info-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fef2f2;
  border: 2px solid #ef4444;
  border-radius: 12px;
  margin-bottom: 24px;
}

.banner-icon { font-size: 32px; }
.info-banner strong { display: block; font-size: 16px; color: #991b1b; }
.info-banner p { margin: 0; font-size: 14px; color: #b91c1c; }

/* Filter Bar */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filter-select {
  padding: 10px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.results-count {
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-600);
}

/* Expenses Grid */
.expenses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.expense-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 2px solid var(--gray-200);
  transition: all 0.3s;
}

.expense-card:hover {
  transform: translateY(-4px);
  border-color: #ef4444;
}

.expense-header {
  padding: 16px 20px;
  background: var(--gray-50);
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.expense-category {
  font-weight: 700;
  font-size: 14px;
}

.expense-date {
  font-size: 12px;
  color: var(--gray-600);
  font-weight: 600;
}

.expense-body {
  padding: 20px;
}

.expense-body h4 {
  font-size: 18px;
  margin-bottom: 8px;
  color: var(--gray-900);
}

.expense-body p {
  font-size: 14px;
  color: var(--gray-600);
  margin-bottom: 16px;
  line-height: 1.5;
}

.expense-amount {
  font-size: 28px;
  font-weight: 800;
  color: #10b981;
}

.expense-footer {
  padding: 16px 20px;
  background: var(--gray-50);
  border-top: 2px solid var(--gray-200);
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.expense-invoice, .expense-time {
  font-size: 12px;
  color: var(--gray-600);
  font-weight: 600;
}

.btn-download {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
  margin-left: auto;
  transition: all 0.3s;
}

.btn-download:hover {
  background: #2563eb;
}

/* Loading & Empty */
.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #ef4444;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-icon { font-size: 80px; margin-bottom: 20px; }
.empty-state h3 { font-size: 24px; margin-bottom: 8px; }
.empty-state p { color: var(--gray-600); }

@media (max-width: 768px) {
  .budget-summary { grid-template-columns: repeat(2, 1fr); }
  .expenses-grid { grid-template-columns: 1fr; }
}
</style>
