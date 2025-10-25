<template>
  <div class="register-expense-page">
    <div class="container">
      <router-link :to="`/student/project/${projectId}/expenses`" class="btn-back">← Volver a Gastos</router-link>

      <form @submit.prevent="handleSubmit" class="expense-form">
        <h1>💳 Registrar Nuevo Gasto</h1>

        <div class="form-card">
          <h3>📋 Información del Gasto</h3>
          
          <div class="form-group">
            <label>Categoría *</label>
            <select v-model="formData.categoria" class="form-control" required>
              <option value="">-- Seleccionar categoría --</option>
              <option value="Material">🛠️ Material</option>
              <option value="Equipo">💻 Equipo</option>
              <option value="Servicio">⚙️ Servicio</option>
              <option value="Transporte">🚗 Transporte</option>
              <option value="Otro">📦 Otro</option>
            </select>
          </div>

          <div class="form-group">
            <label>Concepto *</label>
            <input v-model="formData.concepto" class="form-control" placeholder="Ej: Compra de materiales de laboratorio" required maxlength="200" />
          </div>

          <div class="form-group">
            <label>Descripción Detallada *</label>
            <textarea v-model="formData.descripcion" class="form-control" rows="4" placeholder="Describe el gasto en detalle..." required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Monto *</label>
              <div class="input-money">
                <span>$</span>
                <input v-model.number="formData.monto" type="number" min="1" step="0.01" required />
                <span>COP</span>
              </div>
              <small v-if="formData.monto">Monto: ${{ formatMoney(formData.monto) }}</small>
            </div>

            <div class="form-group">
              <label>Fecha *</label>
              <input v-model="formData.fecha" type="date" class="form-control" required :max="maxDate" />
            </div>
          </div>

          <div class="form-group">
            <label>Número de Factura (Opcional)</label>
            <input v-model="formData.factura_numero" class="form-control" placeholder="Ej: FAC-2025-001" />
          </div>
        </div>

        <!-- Resumen -->
        <div class="summary-card">
          <h3>📊 Resumen del Gasto</h3>
          <div class="summary-grid">
            <div class="summary-item">
              <span class="label">Categoría:</span>
              <span class="value">{{ formData.categoria || 'No seleccionada' }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Monto:</span>
              <span class="value amount">${{ formData.monto ? formatMoney(formData.monto) : '0' }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Fecha:</span>
              <span class="value">{{ formData.fecha || 'No especificada' }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Disponible:</span>
              <span class="value available">${{ formatMoney(available) }}</span>
            </div>
          </div>

          <div v-if="formData.monto > available" class="alert alert-warning">
            ⚠️ El monto excede el presupuesto disponible
          </div>
        </div>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <div class="form-actions">
          <button type="button" @click="goBack" class="btn btn-secondary">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="saving || formData.monto > available">
            {{ saving ? '⏳ Guardando...' : '💾 Registrar Gasto' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'
import expensesApi from '../../api/expenses'

export default {
  name: 'RegisterExpense',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const formData = ref({
      categoria: '',
      concepto: '',
      descripcion: '',
      monto: null,
      fecha: new Date().toISOString().split('T')[0],
      factura_numero: ''
    })
    
    const project = ref(null)
    const saving = ref(false)
    const error = ref('')
    
    const projectId = computed(() => parseInt(route.params.id))
    const maxDate = computed(() => new Date().toISOString().split('T')[0])
    
    const available = computed(() => {
      if (!project.value) return 0
      return (project.value.presupuesto_asignado || 0) - (project.value.presupuesto_ejecutado || 0)
    })
    
    const loadProject = async () => {
      try {
        const response = await projectsApi.getProjectById(projectId.value)
        project.value = response.data
      } catch (err) {
        error.value = 'Error al cargar proyecto'
      }
    }
    
    const handleSubmit = async () => {
      if (formData.value.monto > available.value) {
        error.value = 'El monto excede el presupuesto disponible'
        return
      }
      
      saving.value = true
      error.value = ''
      
      try {
        await expensesApi.createExpense(projectId.value, formData.value)
        alert('✅ Gasto registrado exitosamente')
        router.push(`/student/project/${projectId.value}/expenses`)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al registrar gasto'
      } finally {
        saving.value = false
      }
    }
    
    const goBack = () => {
      if (confirm('¿Cancelar registro?')) {
        router.push(`/student/project/${projectId.value}/expenses`)
      }
    }
    
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    
    onMounted(() => loadProject())
    
    return {
      formData, project, saving, error, projectId, maxDate, available,
      handleSubmit, goBack, formatMoney
    }
  }
}
</script>

<style scoped>
.register-expense-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 800px;
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

.expense-form h1 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.form-card h3 {
  font-size: 20px;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
}

.input-money {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
}

.input-money input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  font-weight: 600;
}

.form-group small {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: var(--gray-600);
}

.summary-card {
  background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  border: 2px solid #667eea;
}

.summary-card h3 {
  font-size: 18px;
  margin-bottom: 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.summary-item {
  padding: 12px;
  background: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-item .label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-600);
  text-transform: uppercase;
}

.summary-item .value {
  font-size: 16px;
  font-weight: 700;
  color: var(--gray-900);
}

.summary-item .amount {
  color: #f59e0b;
  font-size: 20px;
}

.summary-item .available {
  color: #10b981;
}

.alert {
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.alert-warning {
  background: #fef3c7;
  border: 2px solid #f59e0b;
  color: #92400e;
}

.alert-error {
  background: #fee2e2;
  border: 2px solid #ef4444;
  color: #991b1b;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  padding: 14px 32px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  font-size: 15px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
