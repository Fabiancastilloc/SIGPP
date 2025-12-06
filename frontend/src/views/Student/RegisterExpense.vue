<!-- frontend/src/views/Student/RegisterExpense.vue -->
<template>
  <div class="register-expense-page">
    <div class="container">
      
      <!-- Header -->
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Cancelar
        </button>
      </div>

      <!-- Hero Header -->
      <div class="hero-header">
        <div class="hero-icon">💰</div>
        <div class="hero-content">
          <h1>Registrar Nuevo Gasto</h1>
          <p>Proyecto: <strong>{{ project?.nombre }}</strong></p>
          <p class="budget-info">
            Disponible: <span class="budget-value">{{ formatCurrency(availableBudget) }}</span>
          </p>
        </div>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="expense-form">
        
        <!-- Información del Gasto -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">📋</div>
            <div>
              <h2>Información del Gasto</h2>
              <p>Completa los datos de la erogación</p>
            </div>
          </div>

          <div class="form-grid">
            <!-- Fecha -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Fecha del Gasto</span>
                <span class="label-required">*</span>
              </label>
              <input 
                v-model="formData.fecha" 
                type="date" 
                class="field-input"
                required
                :max="today"
              />
              <div class="field-footer">
                <span class="field-hint">📅 Fecha en que se realizó el gasto</span>
              </div>
            </div>

            <!-- Categoría -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Categoría</span>
                <span class="label-required">*</span>
              </label>
              <div class="custom-select" :class="{ open: selectOpen }" @click="toggleSelect">
                <div class="select-trigger">
                  <div class="select-value">
                    <span v-if="!formData.categoria" class="select-placeholder">
                      🔍 Selecciona una categoría
                    </span>
                    <span v-else class="select-selected">
                      {{ getCategoryIcon(formData.categoria) }} {{ getCategoryName(formData.categoria) }}
                    </span>
                  </div>
                  <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
                
                <div v-show="selectOpen" class="select-dropdown">
                  <div 
                    v-for="cat in categories" 
                    :key="cat.value"
                    class="select-option"
                    :class="{ selected: formData.categoria === cat.value }"
                    @click.stop="selectCategory(cat.value)"
                  >
                    <span class="option-icon">{{ cat.icon }}</span>
                    <span class="option-text">{{ cat.name }}</span>
                    <svg v-if="formData.categoria === cat.value" class="option-check" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Descripción -->
            <div class="form-field full-width">
              <label class="field-label">
                <span class="label-text">Descripción</span>
                <span class="label-required">*</span>
              </label>
              <textarea 
                v-model="formData.descripcion" 
                class="field-textarea"
                placeholder="Describe detalladamente el gasto realizado..."
                required
                rows="4"
                maxlength="500"
              ></textarea>
              <div class="field-footer">
                <span class="field-hint">💡 Sé específico sobre el concepto del gasto</span>
                <span class="field-counter">{{ formData.descripcion.length }}/500</span>
              </div>
            </div>

            <!-- Monto -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Monto</span>
                <span class="label-required">*</span>
              </label>
              <div class="currency-input">
                <span class="currency-symbol">$</span>
                <input 
                  v-model.number="formData.monto" 
                  type="number" 
                  class="currency-field"
                  placeholder="0"
                  required
                  min="0"
                  step="100"
                  :max="availableBudget"
                />
                <span class="currency-code">COP</span>
              </div>
              <div class="field-footer">
                <span 
                  :class="['currency-formatted', { error: formData.monto > availableBudget }]"
                >
                  {{ formatCurrency(formData.monto) }}
                </span>
                <span v-if="formData.monto > availableBudget" class="field-error">
                  ⚠️ Excede presupuesto disponible
                </span>
              </div>
            </div>

            <!-- Referencia -->
            <div class="form-field">
              <label class="field-label">
                <span class="label-text">Referencia / Factura</span>
                <span class="label-optional">(Opcional)</span>
              </label>
              <input 
                v-model="formData.referencia" 
                type="text" 
                class="field-input"
                placeholder="Ej: FAC-2025-001, REC-123"
                maxlength="100"
              />
              <div class="field-footer">
                <span class="field-hint">📄 Número de factura o recibo</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Resumen -->
        <div class="summary-section">
          <div class="summary-header">
            <h3>📊 Resumen del Registro</h3>
          </div>
          <div class="summary-body">
            <div class="summary-row">
              <span class="summary-label">Categoría</span>
              <span class="summary-value">
                {{ formData.categoria ? getCategoryName(formData.categoria) : 'No seleccionada' }}
              </span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Monto a Registrar</span>
              <span class="summary-value highlight">{{ formatCurrency(formData.monto) }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">Presupuesto Disponible</span>
              <span class="summary-value">{{ formatCurrency(availableBudget) }}</span>
            </div>
            <div class="summary-row total">
              <span class="summary-label">Disponible Después</span>
              <span class="summary-value" :class="{ negative: formData.monto > availableBudget }">
                {{ formatCurrency(availableBudget - (formData.monto || 0)) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <button type="button" @click="goBack" class="action-btn btn-cancel">
            Cancelar
          </button>
          <button 
            type="submit" 
            class="action-btn btn-submit"
            :disabled="submitting || !canSubmit()"
          >
            <svg v-if="submitting" class="btn-spinner" viewBox="0 0 24 24">
              ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="50" stroke-dashoffset="25" />
            </svg>
            <span v-else>💾 Registrar Gasto</span>
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
    
    const projectId = parseInt(route.params.id)
    const project = ref(null)
    const submitting = ref(false)
    const selectOpen = ref(false)
    
    const today = new Date().toISOString().split('T')[0]
    
    const formData = ref({
      fecha: today,
      categoria: '',
      descripcion: '',
      monto: 0,
      referencia: ''
    })
    
    const categories = [
      { value: 'personal', name: 'Personal', icon: '👥' },
      { value: 'equipamiento', name: 'Equipamiento', icon: '🖥️' },
      { value: 'materiales', name: 'Materiales', icon: '📦' },
      { value: 'servicios', name: 'Servicios', icon: '🔧' },
      { value: 'software', name: 'Software', icon: '💻' },
      { value: 'transporte', name: 'Transporte', icon: '🚗' },
      { value: 'otros', name: 'Otros', icon: '📌' }
    ]
    
    const availableBudget = computed(() => {
      if (!project.value) return 0
      const asignado = parseFloat(project.value.presupuesto_asignado || 0)
      const ejecutado = parseFloat(project.value.presupuesto_ejecutado || 0)
      return asignado - ejecutado
    })
    
    const loadProject = async () => {
      try {
        const response = await projectsApi.getProjectById(projectId)
        project.value = response.data
        
        // Verificar que el proyecto esté activo
        if (project.value.estado !== 'activo') {
          alert('⚠️ Solo puedes registrar gastos en proyectos activos')
          router.push(`/student/project/${projectId}`)
        }
      } catch (err) {
        console.error('Error cargando proyecto:', err)
        alert('Error al cargar el proyecto')
        router.push('/student')
      }
    }
    
    const toggleSelect = () => {
      selectOpen.value = !selectOpen.value
    }
    
    const selectCategory = (value) => {
      formData.value.categoria = value
      selectOpen.value = false
    }
    
    const getCategoryIcon = (category) => {
      const cat = categories.find(c => c.value === category)
      return cat ? cat.icon : '📌'
    }
    
    const getCategoryName = (category) => {
      const cat = categories.find(c => c.value === category)
      return cat ? cat.name : category
    }
    
    const canSubmit = () => {
      return formData.value.fecha &&
             formData.value.categoria &&
             formData.value.descripcion.length > 0 &&
             formData.value.monto > 0 &&
             formData.value.monto <= availableBudget.value
    }
    
    const handleSubmit = async () => {
      if (!canSubmit()) {
        alert('Por favor completa todos los campos requeridos correctamente')
        return
      }
      
      if (formData.value.monto > availableBudget.value) {
        alert('⚠️ El monto excede el presupuesto disponible')
        return
      }
      
      if (!confirm(`¿Confirmar registro de gasto por ${formatCurrency(formData.value.monto)}?`)) {
        return
      }
      
      submitting.value = true
      
      try {
        await expensesApi.createExpense(projectId, formData.value)
        alert('✅ Gasto registrado exitosamente')
        router.push(`/student/project/${projectId}/expenses`)
      } catch (err) {
        console.error('Error registrando gasto:', err)
        alert('❌ Error al registrar el gasto')
      } finally {
        submitting.value = false
      }
    }
    
    const goBack = () => router.push(`/student/project/${projectId}/expenses`)
    
    const formatCurrency = (value) => {
      if (!value) return '$0 COP'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }
    
    onMounted(() => {
      loadProject()
    })
    
    return {
      project,
      formData,
      categories,
      submitting,
      selectOpen,
      today,
      availableBudget,
      toggleSelect,
      selectCategory,
      getCategoryIcon,
      getCategoryName,
      canSubmit,
      handleSubmit,
      goBack,
      formatCurrency
    }
  }
}
</script>

<style scoped>
/* Base */
.register-expense-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  padding: 32px 16px;
}

.container {
  max-width: 900px;
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

/* Hero */
.hero-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border: 3px solid #3b82f6;
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.hero-icon {
  font-size: 64px;
  filter: drop-shadow(0 4px 12px rgba(212, 175, 55, 0.6));
}

.hero-content h1 {
  font-size: 28px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.hero-content p {
  font-size: 15px;
  color: #e0e7ff;
  font-weight: 600;
  margin-bottom: 4px;
}

.hero-content strong {
  color: #d4af37;
  font-weight: 800;
}

.budget-info {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 2px solid rgba(212, 175, 55, 0.3);
}

.budget-value {
  color: #10b981;
  font-weight: 900;
  font-size: 20px;
}

/* Form */
.expense-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid #d4af37;
}

.section-icon {
  font-size: 40px;
  filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.4));
}

.section-header h2 {
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 4px;
}

.section-header p {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.full-width {
  grid-column: 1 / -1;
}

/* Form Fields */
.form-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.label-text {
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-required {
  color: #ef4444;
  font-weight: 900;
  font-size: 16px;
}

.label-optional {
  font-size: 11px;
  color: #64748b;
  font-weight: 600;
  text-transform: lowercase;
}

.field-input,
.field-textarea {
  width: 100%;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.3s ease;
}

.field-input::placeholder,
.field-textarea::placeholder {
  color: #64748b;
}

.field-input:focus,
.field-textarea:focus {
  outline: none;
  background: #1e293b;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.field-textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
}

.field-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.field-hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.field-counter {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.field-error {
  font-size: 12px;
  color: #ef4444;
  font-weight: 700;
}

/* Currency Input */
.currency-input {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.currency-input:focus-within {
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.currency-symbol {
  font-size: 20px;
  font-weight: 900;
  color: #d4af37;
}

.currency-field {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 18px;
  font-weight: 800;
  outline: none;
}

.currency-code {
  font-size: 13px;
  font-weight: 700;
  color: #94a3b8;
  padding: 4px 10px;
  background: #1e293b;
  border-radius: 6px;
}

.currency-formatted {
  font-size: 16px;
  font-weight: 900;
  color: #10b981;
}

.currency-formatted.error {
  color: #ef4444;
}

/* Custom Select */
.custom-select {
  position: relative;
}

.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #0f172a;
  border: 2px solid #334155;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-trigger:hover {
  border-color: #d4af37;
}

.custom-select.open .select-trigger {
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
}

.select-placeholder {
  color: #64748b;
  font-weight: 600;
  font-size: 14px;
}

.select-selected {
  color: #f1f5f9;
  font-weight: 700;
  font-size: 14px;
}

.select-arrow {
  width: 20px;
  height: 20px;
  color: #d4af37;
  transition: transform 0.3s ease;
}

.custom-select.open .select-arrow {
  transform: rotate(180deg);
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: #0f172a;
  border: 2px solid #d4af37;
  border-radius: 10px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.select-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid #1e293b;
}

.select-option:hover {
  background: #1e293b;
}

.select-option.selected {
  background: rgba(212, 175, 55, 0.15);
}

.option-icon {
  font-size: 24px;
}

.option-text {
  flex: 1;
  font-size: 14px;
  color: #f1f5f9;
  font-weight: 700;
}

.option-check {
  width: 22px;
  height: 22px;
  color: #10b981;
}

/* Summary Section */
.summary-section {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(212, 175, 55, 0.05));
  border: 2px solid rgba(212, 175, 55, 0.3);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.summary-header {
  padding: 20px 24px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 2px solid rgba(212, 175, 55, 0.3);
}

.summary-header h3 {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-body {
  padding: 24px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row.total {
  margin-top: 12px;
  padding-top: 20px;
  border-top: 2px solid rgba(212, 175, 55, 0.4);
  border-bottom: none;
}

.summary-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 16px;
  color: #f1f5f9;
  font-weight: 900;
}

.summary-value.highlight {
  font-size: 20px;
  color: #d4af37;
}

.summary-value.negative {
  color: #ef4444;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 16px;
  padding: 32px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.action-btn {
  flex: 1;
  padding: 16px 28px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-cancel {
  background: #475569;
  color: #ffffff;
}

.btn-cancel:hover {
  background: #334155;
  transform: translateY(-2px);
}

.btn-submit {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  color: #0a0f1e;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(212, 175, 55, 0.6);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .register-expense-page {
    padding: 20px 12px;
  }

  .hero-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }

  .form-section {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
