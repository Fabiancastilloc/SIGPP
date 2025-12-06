<template>
  <div class="auditor-expenses-page">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Back Button -->
      <div class="page-header">
        <router-link :to="`/auditor/project/${projectId}`" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Proyecto
        </router-link>
      </div>

      <!-- Hero Header -->
      <div class="hero-header">
        <div class="hero-icon">💳</div>
        <div class="hero-content">
          <h1>Auditoría de Gastos</h1>
          <p v-if="project" class="project-name">{{ project.nombre }}</p>
          <span v-if="project" class="project-code">{{ project.codigo_proyecto }}</span>
        </div>
        <div class="audit-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Modo Auditoría</span>
        </div>
      </div>

      <!-- Budget Summary Cards -->
      <div class="budget-summary">
        <div class="summary-card card-total">
          <div class="card-header">
            <span class="card-icon">💰</span>
            <span class="card-badge">Asignado</span>
          </div>
          <div class="card-body">
            <div class="card-value">{{ formatMoney(project?.presupuesto_asignado || 0) }}</div>
            <div class="card-label">Presupuesto Total</div>
          </div>
        </div>

        <div class="summary-card card-executed">
          <div class="card-header">
            <span class="card-icon">💸</span>
            <span class="card-badge executed">Gastado</span>
          </div>
          <div class="card-body">
            <div class="card-value executed">{{ formatMoney(totalExecuted) }}</div>
            <div class="card-label">{{ expenses.length }} transacciones</div>
          </div>
        </div>

        <div class="summary-card card-available">
          <div class="card-header">
            <span class="card-icon">✅</span>
            <span class="card-badge available">Disponible</span>
          </div>
          <div class="card-body">
            <div class="card-value available">{{ formatMoney(available) }}</div>
            <div class="card-label">{{ executionPercentage }}% utilizado</div>
          </div>
        </div>

        <div class="summary-card card-percentage">
          <div class="card-header">
            <span class="card-icon">📊</span>
            <span class="card-badge percentage">Ejecución</span>
          </div>
          <div class="card-body">
            <div class="card-value percentage">{{ executionPercentage }}%</div>
            <div class="card-label">Nivel de ejecución</div>
          </div>
        </div>
      </div>

      <!-- Progress Section -->
      <div class="progress-section">
        <div class="progress-header">
          <div class="progress-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Ejecución Presupuestal
          </div>
          <div class="progress-percentage" :class="getProgressClass(executionPercentage)">
            {{ executionPercentage }}%
          </div>
        </div>

        <div class="progress-bar-container">
          <div 
            class="progress-bar-fill" 
            :class="getProgressClass(executionPercentage)" 
            :style="{ width: executionPercentage + '%' }"
          >
            <span class="progress-bar-label">{{ executionPercentage }}%</span>
          </div>
        </div>

        <div class="progress-footer">
          <div class="progress-stat">
            <span class="stat-icon">📤</span>
            <div>
              <div class="stat-label">Ejecutado</div>
              <div class="stat-value executed">{{ formatMoney(totalExecuted) }}</div>
            </div>
          </div>
          <div class="progress-stat">
            <span class="stat-icon">📥</span>
            <div>
              <div class="stat-label">Disponible</div>
              <div class="stat-value available">{{ formatMoney(available) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alert Banner -->
      <div v-if="executionPercentage >= 90" class="alert alert-danger">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <strong>⚠️ Alerta de Auditoría</strong>
          <p>El proyecto ha utilizado más del 90% del presupuesto asignado</p>
        </div>
      </div>

      <div v-else-if="executionPercentage >= 70" class="alert alert-warning">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <strong>🔔 Observación Presupuestal</strong>
          <p>El proyecto ha utilizado más del 70% del presupuesto asignado</p>
        </div>
      </div>

      <!-- Info Banner -->
      <div class="info-banner">
        <svg class="banner-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <div>
          <strong>Modo Verificación y Control</strong>
          <p>Vista de auditoría financiera - Los datos son de solo lectura</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando registros financieros...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="expenses.length === 0" class="empty-state">
        <div class="empty-icon">💳</div>
        <h3>Sin Gastos Registrados</h3>
        <p>Este proyecto no tiene transacciones registradas</p>
      </div>

      <!-- Expenses Section -->
      <div v-else>
        <!-- Filter Bar -->
        <div class="filter-section">
          <div class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filtrar Transacciones
          </div>

          <div class="filter-bar">
            <select v-model="filterCategory" class="filter-select">
              <option value="">📊 Todas las categorías</option>
              <option value="personal">👨‍💼 Personal</option>
              <option value="equipamiento">🖥️ Equipamiento</option>
              <option value="materiales">📦 Materiales</option>
              <option value="servicios">🔧 Servicios</option>
              <option value="software">💻 Software</option>
              <option value="transporte">🚗 Transporte</option>
              <option value="otros">📌 Otros</option>
            </select>

            <div class="filter-results">
              <span class="results-badge">{{ filteredExpenses.length }}</span>
              <span class="results-text">registros auditados</span>
              <span class="results-divider">|</span>
              <span class="results-total">Total: {{ formatMoney(filteredTotal) }}</span>
            </div>
          </div>
        </div>

        <!-- Category Summary (if filtered) -->
        <div v-if="filterCategory" class="category-summary">
          <div class="summary-info">
            <span class="category-icon">{{ getCategoryIcon(filterCategory) }}</span>
            <div>
              <div class="category-name">{{ getCategoryName(filterCategory) }}</div>
              <div class="category-stats">
                {{ filteredExpenses.length }} transacciones · {{ formatMoney(filteredTotal) }}
              </div>
            </div>
          </div>
          <button @click="filterCategory = ''" class="btn-clear-filter">
            Limpiar filtro ✕
          </button>
        </div>

        <!-- Expenses Grid -->
        <div class="expenses-grid">
          <div 
            v-for="(expense, index) in filteredExpenses" 
            :key="expense.id" 
            class="expense-card audited"
            :class="{ 'animate-in': true }"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <!-- Audit Stamp -->
            <div class="audit-stamp">
              <svg class="stamp-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>AUDITADO</span>
            </div>

            <!-- Card Header -->
            <div class="expense-header">
              <div class="expense-category">
                <span class="category-icon-badge">{{ getCategoryIcon(expense.categoria) }}</span>
                <span class="category-name">{{ getCategoryName(expense.categoria) }}</span>
              </div>
              <div class="expense-date">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ formatDate(expense.fecha) }}
              </div>
            </div>

            <!-- Card Body -->
            <div class="expense-body">
              <h4 class="expense-description">{{ expense.descripcion }}</h4>

              <!-- Reference Number -->
              <div v-if="expense.referencia" class="expense-reference">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="ref-label">Ref:</span>
                <span class="ref-value">{{ expense.referencia }}</span>
              </div>

              <!-- Amount -->
              <div class="expense-amount">
                <span class="amount-symbol">$</span>
                <span class="amount-value">{{ formatMoneyShort(expense.monto) }}</span>
              </div>

              <!-- Footer with verification -->
              <div class="expense-footer">
                <div class="footer-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{{ formatDateTime(expense.created_at) }}</span>
                </div>
                <div class="verification-badge">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span>Verificado</span>
                </div>
              </div>
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
    const filterCategory = ref('')

    const projectId = computed(() => parseInt(route.params.id))

    const totalExecuted = computed(() => {
      return expenses.value.reduce((sum, e) => sum + parseFloat(e.monto || 0), 0)
    })

    const available = computed(() => {
      const assigned = parseFloat(project.value?.presupuesto_asignado || 0)
      return Math.max(0, assigned - totalExecuted.value)
    })

    const executionPercentage = computed(() => {
      const assigned = parseFloat(project.value?.presupuesto_asignado || 0)
      if (!assigned || assigned === 0) return 0
      return Math.min(100, Math.round((totalExecuted.value / assigned) * 100))
    })

    const filteredExpenses = computed(() => {
      if (!filterCategory.value) return expenses.value
      return expenses.value.filter(e => e.categoria === filterCategory.value)
    })

    const filteredTotal = computed(() => {
      return filteredExpenses.value.reduce((sum, e) => sum + parseFloat(e.monto || 0), 0)
    })

    const loadData = async () => {
      loading.value = true
      try {
        const [projectRes, expensesRes] = await Promise.all([
          projectsApi.getProjectById(projectId.value),
          expensesApi.getExpenses(projectId.value)
        ])
        
        project.value = projectRes.data
        expenses.value = expensesRes.data.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
        
        console.log('✅ Auditoría cargada:', {
          proyecto: project.value.nombre,
          transacciones: expenses.value.length,
          total_ejecutado: totalExecuted.value
        })
      } catch (err) {
        console.error('❌ Error cargando datos:', err)
        alert('Error al cargar la información financiera')
      } finally {
        loading.value = false
      }
    }

    const getCategoryIcon = (category) => {
      const icons = {
        'personal': '👨‍💼',
        'equipamiento': '🖥️',
        'materiales': '📦',
        'servicios': '🔧',
        'software': '💻',
        'transporte': '🚗',
        'otros': '📌'
      }
      return icons[category] || '📌'
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

    const getProgressClass = (percentage) => {
      if (percentage >= 90) return 'progress-danger'
      if (percentage >= 70) return 'progress-warning'
      return 'progress-success'
    }

    const formatMoney = (val) => {
      if (!val) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(val)
    }

    const formatMoneyShort = (val) => {
      if (!val) return '0'
      return new Intl.NumberFormat('es-CO', {
        minimumFractionDigits: 0
      }).format(val)
    }

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const formatDateTime = (dateStr) => {
      return new Date(dateStr).toLocaleString('es-CO', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => loadData())

    return {
      project,
      expenses,
      loading,
      filterCategory,
      projectId,
      totalExecuted,
      available,
      executionPercentage,
      filteredExpenses,
      filteredTotal,
      getCategoryIcon,
      getCategoryName,
      getProgressClass,
      formatMoney,
      formatMoneyShort,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style scoped>
/* BASE */
.auditor-expenses-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
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
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  top: -300px;
  right: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -250px;
  left: -250px;
  animation-delay: -12s;
}

.orb-3 {
  width: 450px;
  height: 450px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  top: 50%;
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
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.3s;
}

.btn-back:hover {
  background: #334155;
  border-color: #f59e0b;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* HERO HEADER */
.hero-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  border: 3px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3);
  position: relative;
}

.hero-icon {
  font-size: 64px;
  filter: drop-shadow(0 4px 12px rgba(245, 158, 11, 0.6));
}

.hero-content {
  flex: 1;
}

.hero-content h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.project-name {
  font-size: 18px;
  color: #f59e0b;
  font-weight: 700;
  margin-bottom: 6px;
  display: block;
}

.project-code {
  display: inline-block;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: #64748b;
  font-weight: 700;
  background: rgba(100, 116, 139, 0.2);
  padding: 4px 12px;
  border-radius: 6px;
}

.audit-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(245, 158, 11, 0.2);
  border: 2px solid rgba(245, 158, 11, 0.4);
  border-radius: 12px;
  font-weight: 800;
  font-size: 14px;
  color: #fbbf24;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-icon {
  width: 24px;
  height: 24px;
}

/* BUDGET SUMMARY */
.budget-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.summary-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s;
  border-left: 4px solid;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.card-total {
  border-color: #3b82f6;
}

.card-executed {
  border-color: #f59e0b;
}

.card-available {
  border-color: #10b981;
}

.card-percentage {
  border-color: #8b5cf6;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(245, 158, 11, 0.3));
}

.card-badge {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 12px;
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  letter-spacing: 0.5px;
}

.card-badge.executed {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.card-badge.available {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.card-badge.percentage {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.card-value {
  font-size: 32px;
  font-weight: 900;
  color: #3b82f6;
  line-height: 1;
  margin-bottom: 8px;
}

.card-value.executed {
  color: #f59e0b;
}

.card-value.available {
  color: #10b981;
}

.card-value.percentage {
  color: #8b5cf6;
}

.card-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* PROGRESS SECTION */
.progress-section {
  background: #1e293b;
  padding: 32px;
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid #334155;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.progress-title svg {
  width: 24px;
  height: 24px;
  color: #f59e0b;
}

.progress-percentage {
  font-size: 28px;
  font-weight: 900;
  padding: 8px 20px;
  border-radius: 12px;
}

.progress-percentage.progress-success {
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
}

.progress-percentage.progress-warning {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.15);
}

.progress-percentage.progress-danger {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.15);
}

.progress-bar-container {
  height: 32px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 20px;
  position: relative;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
}

.progress-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.8s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 16px;
  position: relative;
  overflow: hidden;
}

.progress-bar-fill::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.progress-bar-fill.progress-success {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-bar-fill.progress-warning {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-bar-fill.progress-danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.progress-bar-label {
  font-size: 14px;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 1;
}

.progress-footer {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.progress-stat {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  border: 1px solid #334155;
}

.stat-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 6px rgba(245, 158, 11, 0.3));
}

.stat-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 900;
  line-height: 1;
}

.stat-value.executed {
  color: #f59e0b;
}

.stat-value.available {
  color: #10b981;
}

/* ALERTS */
.alert {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 24px;
  border-radius: 16px;
  margin-bottom: 32px;
  border: 2px solid;
}

.alert svg {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}

.alert strong {
  display: block;
  font-size: 16px;
  font-weight: 900;
  margin-bottom: 6px;
}

.alert p {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.alert-danger {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.alert-danger svg {
  color: #ef4444;
}

.alert-danger strong {
  color: #ef4444;
}

.alert-warning {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
  color: #fcd34d;
}

.alert-warning svg {
  color: #f59e0b;
}

.alert-warning strong {
  color: #f59e0b;
}

/* INFO BANNER */
.info-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(245, 158, 11, 0.1);
  border: 2px solid rgba(245, 158, 11, 0.3);
  border-radius: 16px;
  margin-bottom: 32px;
}

.banner-icon {
  width: 32px;
  height: 32px;
  color: #f59e0b;
  flex-shrink: 0;
}

.info-banner strong {
  display: block;
  font-size: 16px;
  margin-bottom: 6px;
  color: #fbbf24;
  font-weight: 900;
}

.info-banner p {
  margin: 0;
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

/* FILTER SECTION */
.filter-section {
  background: #1e293b;
  padding: 28px;
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid #334155;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 20px;
}

.section-title svg {
  width: 22px;
  height: 22px;
  color: #f59e0b;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-select {
  flex: 1;
  min-width: 250px;
  padding: 14px 20px;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.2);
}

.filter-results {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 700;
}

.results-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  padding: 0 12px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 999px;
  color: #ffffff;
  font-weight: 900;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
}

.results-text {
  color: #cbd5e1;
}

.results-divider {
  color: #334155;
}

.results-total {
  color: #f59e0b;
  font-weight: 900;
}

/* CATEGORY SUMMARY */
.category-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: rgba(245, 158, 11, 0.1);
  border: 2px solid rgba(245, 158, 11, 0.3);
  border-radius: 16px;
  margin-bottom: 24px;
}

.summary-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.category-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 6px rgba(245, 158, 11, 0.4));
}

.category-name {
  font-size: 18px;
  font-weight: 900;
  color: #fbbf24;
  margin-bottom: 4px;
}

.category-stats {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 700;
}

.btn-clear-filter {
  padding: 10px 20px;
  background: rgba(239, 68, 68, 0.2);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  color: #fca5a5;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear-filter:hover {
  background: #ef4444;
  border-color: #ef4444;
  color: #ffffff;
}

/* EXPENSES GRID */
.expenses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 24px;
}

.expense-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s;
  position: relative;
  opacity: 0;
}

.expense-card.animate-in {
  animation: slideIn 0.4s ease forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.expense-card.audited {
  border-color: rgba(245, 158, 11, 0.5);
}

.expense-card:hover {
  transform: translateY(-4px);
  border-color: #f59e0b;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

/* AUDIT STAMP */
.audit-stamp {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(245, 158, 11, 0.15));
  border: 2px solid rgba(245, 158, 11, 0.5);
  border-radius: 8px;
  font-size: 10px;
  font-weight: 900;
  color: #fbbf24;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.stamp-icon {
  width: 14px;
  height: 14px;
}

.expense-header {
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.expense-category {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-icon-badge {
  font-size: 20px;
  filter: drop-shadow(0 2px 4px rgba(245, 158, 11, 0.3));
}

.category-name {
  font-weight: 800;
  font-size: 13px;
  color: #f59e0b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.expense-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
}

.expense-date svg {
  width: 14px;
  height: 14px;
}

.expense-body {
  padding: 24px;
}

.expense-description {
  font-size: 16px;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 16px;
  line-height: 1.4;
}

.expense-reference {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 10px;
  margin-bottom: 16px;
}

.expense-reference svg {
  width: 16px;
  height: 16px;
  color: #60a5fa;
}

.ref-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
}

.ref-value {
  font-size: 13px;
  color: #60a5fa;
  font-weight: 800;
  font-family: 'Courier New', monospace;
}

.expense-amount {
  display: flex;
  align-items: baseline;
  gap: 6px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  border: 2px solid rgba(245, 158, 11, 0.3);
  border-radius: 12px;
  margin-bottom: 16px;
}

.amount-symbol {
  font-size: 20px;
  font-weight: 900;
  color: #f59e0b;
}

.amount-value {
  font-size: 32px;
  font-weight: 900;
  color: #f59e0b;
  line-height: 1;
}

.expense-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 2px solid #334155;
  gap: 12px;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}

.footer-item svg {
  width: 14px;
  height: 14px;
}

.verification-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 6px;
  font-size: 11px;
  color: #10b981;
  font-weight: 800;
  text-transform: uppercase;
}

.verification-badge svg {
  width: 14px;
  height: 14px;
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
  border-top-color: #f59e0b;
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

/* EMPTY STATE */
.empty-state {
  text-align: center;
  padding: 100px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.empty-icon {
  font-size: 96px;
  margin-bottom: 24px;
  opacity: 0.5;
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
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .expenses-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}

@media (max-width: 768px) {
  .auditor-expenses-page {
    padding: 20px 12px;
  }

  .hero-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .audit-badge {
    width: 100%;
    justify-content: center;
  }

  .budget-summary {
    grid-template-columns: 1fr;
  }

  .progress-footer {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    width: 100%;
  }

  .filter-results {
    justify-content: center;
  }

  .category-summary {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .expenses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
