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

      <div v-else-if="expense" class="detail-card">
        <div class="detail-header">
          <h1>{{ getCategoryIcon(expense.categoria) }} {{ expense.concepto }}</h1>
          <span class="category-badge">{{ expense.categoria }}</span>
        </div>

        <div class="detail-content">
          <div class="detail-section">
            <h3>📝 Descripción</h3>
            <p>{{ expense.descripcion }}</p>
          </div>

          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">💰 Monto</span>
              <span class="value amount">${{ formatMoney(expense.monto) }}</span>
            </div>

            <div class="detail-item">
              <span class="label">📅 Fecha</span>
              <span class="value">{{ formatDate(expense.fecha) }}</span>
            </div>

            <div v-if="expense.factura_numero" class="detail-item">
              <span class="label">📄 Factura</span>
              <span class="value">{{ expense.factura_numero }}</span>
            </div>

            <div class="detail-item">
              <span class="label">🕐 Registrado</span>
              <span class="value">{{ formatDate(expense.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-actions">
          <button @click="goBack" class="btn btn-secondary">Volver</button>
          <button @click="confirmDelete" class="btn btn-danger">🗑️ Eliminar Gasto</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import expensesApi from '../../api/expenses'

export default {
  name: 'ExpenseDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const expense = ref(null)
    const loading = ref(true)
    
    const projectId = computed(() => parseInt(route.params.projectId))
    const expenseId = computed(() => parseInt(route.params.expenseId))
    
    const loadExpense = async () => {
      loading.value = true
      try {
        // Aquí necesitas crear un endpoint para obtener un gasto específico
        const response = await expensesApi.getExpenseById(expenseId.value)
        expense.value = response.data
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar gasto')
      } finally {
        loading.value = false
      }
    }
    
    const confirmDelete = async () => {
      if (!confirm('¿Eliminar este gasto?')) return
      
      try {
        await expensesApi.deleteExpense(expenseId.value)
        alert('✅ Gasto eliminado')
        router.push(`/student/project/${projectId.value}/expenses`)
      } catch (err) {
        alert('Error al eliminar gasto')
      }
    }
    
    const goBack = () => router.push(`/student/project/${projectId.value}/expenses`)
    
    const getCategoryIcon = (category) => {
      const icons = { 'Material': '🛠️', 'Equipo': '💻', 'Servicio': '⚙️', 'Transporte': '🚗', 'Otro': '📦' }
      return icons[category] || '📦'
    }
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    const formatDate = (dateStr) => new Date(dateStr).toLocaleString('es-CO')
    
    onMounted(() => loadExpense())
    
    return { expense, loading, projectId, confirmDelete, goBack, getCategoryIcon, formatMoney, formatDate }
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
  max-width: 900px;
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
}

.detail-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-header h1 {
  font-size: 24px;
  margin: 0;
}

.category-badge {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.detail-content {
  padding: 32px;
}

.detail-section {
  margin-bottom: 32px;
}

.detail-section h3 {
  font-size: 18px;
  margin-bottom: 12px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.detail-item {
  padding: 16px;
  background: var(--gray-50);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item .label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.detail-item .value {
  font-size: 16px;
  font-weight: 700;
  color: var(--gray-900);
}

.detail-item .amount {
  font-size: 24px;
  color: #f59e0b;
}

.detail-actions {
  padding: 24px 32px;
  background: var(--gray-50);
  border-top: 2px solid var(--gray-200);
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-danger {
  background: #ef4444;
  color: white;
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

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
