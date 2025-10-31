<template>
  <div class="expenses-view-page">
    <div class="container">
      <div class="page-header">
        <router-link :to="`/auditor/project/${projectId}`" class="btn-back">← Volver al Proyecto</router-link>
        <h1>💳 Registro de Gastos - Auditoría</h1>
        <p v-if="project">{{ project.nombre }}</p>
      </div>

      <div class="budget-summary">
        <div class="summary-card total">
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
            <div class="card-value">${{ formatMoney(available) }}</div>
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

      <div class="progress-section">
        <div class="progress-header">
          <span>Ejecución Presupuestal</span>
          <span>{{ executionPercentage }}% ejecutado</span>
        </div>
        <div class="progress-bar-large">
          <div class="progress-fill" :style="{ width: executionPercentage + '%' }"></div>
        </div>
      </div>

      <div class="audit-note">
        <span class="note-icon">🔍</span>
        <div>
          <strong>Modo Auditoría</strong>
          <p>Vista de solo lectura para auditoría y verificación de gastos</p>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando gastos...</p>
      </div>

      <div v-else-if="expenses.length === 0" class="empty-state">
        <div class="empty-icon">💳</div>
        <h3>Sin gastos registrados</h3>
        <p>El proyecto aún no tiene gastos</p>
      </div>

      <div v-else class="expenses-grid">
        <div v-for="expense in expenses" :key="expense.id" class="expense-card">
          <div class="expense-header">
            <div class="expense-category">{{ getCategoryIcon(expense.categoria) }} {{ expense.categoria }}</div>
            <div class="expense-date">{{ formatDate(expense.fecha) }}</div>
          </div>
          
          <div class="expense-body">
            <h4>{{ expense.concepto }}</h4>
            <p v-if="expense.descripcion">{{ truncate(expense.descripcion, 100) }}</p>
            <div class="expense-amount">${{ formatMoney(expense.monto) }}</div>
            <div v-if="expense.factura_numero" class="expense-invoice">
              📄 Factura: {{ expense.factura_numero }}
            </div>
            <div class="expense-meta">
              Registrado: {{ formatDate(expense.created_at) }}
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
  name: 'AuditorExpensesView',
  setup() {
    const route = useRoute()
    const project = ref(null)
    const expenses = ref([])
    const loading = ref(true)
    
    const projectId = computed(() => parseInt(route.params.id))
    const totalExecuted = computed(() => expenses.value.reduce((sum, e) => sum + e.monto, 0))
    const available = computed(() => (project.value?.presupuesto_asignado || 0) - totalExecuted.value)
    const executionPercentage = computed(() => {
      if (!project.value?.presupuesto_asignado) return 0
      return Math.round((totalExecuted.value / project.value.presupuesto_asignado) * 100)
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
    
    const getCategoryIcon = (category) => {
      const icons = { 'Material': '🛠️', 'Equipo': '💻', 'Servicio': '⚙️', 'Transporte': '🚗', 'Otro': '📦' }
      return icons[category] || '📦'
    }
    
    const truncate = (text, len) => text && text.length > len ? text.substring(0, len) + '...' : text
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-CO')
    
    onMounted(() => loadData())
    
    return { project, expenses, loading, projectId, totalExecuted, available, executionPercentage, getCategoryIcon, truncate, formatMoney, formatDate }
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
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  margin: 16px 0 8px;
}

.btn-back {
  display: inline-block;
  padding: 12px 24px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  border: 2px solid var(--gray-200);
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #f59e0b;
}

.budget-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
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

.summary-card.total { border-color: #3b82f6; }
.summary-card.executed { border-color: #f59e0b; }
.summary-card.available { border-color: #10b981; }
.summary-card.percentage { border-color: #8b5cf6; }

.card-icon {
  font-size: 40px;
}

.card-value {
  font-size: 28px;
  font-weight: 800;
  color: var(--gray-900);
}

.card-label {
  font-size: 14px;
  color: var(--gray-600);
  font-weight: 600;
}

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
  margin-bottom: 12px;
  font-weight: 600;
}

.progress-bar-large {
  height: 20px;
  background: var(--gray-200);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  transition: width 0.5s;
}

.audit-note {
  background: #fef3c7;
  border: 2px solid #f59e0b;
  padding: 16px 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.note-icon {
  font-size: 32px;
}

.audit-note strong {
  display: block;
  font-size: 16px;
  margin-bottom: 4px;
  color: #92400e;
}

.audit-note p {
  margin: 0;
  font-size: 14px;
  color: #92400e;
}

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
  border-color: #f59e0b;
}

.expense-header {
  padding: 16px 20px;
  background: var(--gray-50);
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
}

.expense-category {
  font-weight: 700;
  font-size: 14px;
}

.expense-date {
  font-size: 12px;
  color: var(--gray-600);
}

.expense-body {
  padding: 20px;
}

.expense-body h4 {
  font-size: 18px;
  margin-bottom: 8px;
}

.expense-body p {
  font-size: 14px;
  color: var(--gray-600);
  margin-bottom: 12px;
}

.expense-amount {
  font-size: 24px;
  font-weight: 800;
  color: #f59e0b;
  margin-bottom: 12px;
}

.expense-invoice {
  padding: 8px 12px;
  background: var(--gray-50);
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

.expense-meta {
  font-size: 12px;
  color: var(--gray-500);
  font-style: italic;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #f59e0b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .expenses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
