<template>
  <div class="expenses-view-page">
    <div class="container">
      <div class="page-header">
        <router-link :to="`/professor/project/${projectId}`" class="btn-back">← Volver al Proyecto</router-link>
        <h1>💳 Gastos del Proyecto</h1>
        <p v-if="project">{{ project.nombre }}</p>
      </div>

      <div class="budget-summary">
        <div class="summary-card">
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
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
      </div>

      <div v-else-if="expenses.length === 0" class="empty-state">
        <div class="empty-icon">💳</div>
        <h3>Sin gastos registrados</h3>
      </div>

      <div v-else class="expenses-grid">
        <div v-for="expense in expenses" :key="expense.id" class="expense-card">
          <div class="expense-header">
            <div class="expense-category">{{ getCategoryIcon(expense.categoria) }} {{ expense.categoria }}</div>
            <div class="expense-date">{{ formatDate(expense.fecha) }}</div>
          </div>
          
          <div class="expense-body">
            <h4>{{ expense.concepto }}</h4>
            <p>{{ expense.descripcion }}</p>
            <div class="expense-amount">${{ formatMoney(expense.monto) }}</div>
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
  name: 'ProfessorExpensesView',
  setup() {
    const route = useRoute()
    const project = ref(null)
    const expenses = ref([])
    const loading = ref(true)
    
    const projectId = computed(() => parseInt(route.params.id))
    const totalExecuted = computed(() => expenses.value.reduce((sum, e) => sum + e.monto, 0))
    const available = computed(() => (project.value?.presupuesto_asignado || 0) - totalExecuted.value)
    
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
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-CO')
    
    onMounted(() => loadData())
    
    return { project, expenses, loading, projectId, totalExecuted, available, getCategoryIcon, formatMoney, formatDate }
  }
}
</script>

<style scoped>
/* Usa los mismos estilos de ExpensesView.vue del estudiante */
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

.btn-back {
  display: inline-block;
  padding: 12px 24px;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  margin-bottom: 16px;
  border: 2px solid var(--gray-200);
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
}

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
}

.expense-header {
  padding: 16px 20px;
  background: var(--gray-50);
  border-bottom: 2px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
}

.expense-body {
  padding: 20px;
}

.expense-body h4 {
  font-size: 18px;
  margin-bottom: 8px;
}

.expense-amount {
  font-size: 24px;
  font-weight: 800;
  color: #f59e0b;
  margin-top: 12px;
}

.loading-state, .empty-state {
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
</style>
