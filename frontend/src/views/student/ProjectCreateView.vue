<template>
  <div class="project-create-view">
    <div class="create-header">
      <button @click="volver" class="btn-back">
        ← Volver a Proyectos
      </button>

      <div class="header-content">
        <h1 class="page-title">Crear Nuevo Proyecto</h1>
        <p class="page-subtitle">Completa la información para registrar tu proyecto de grado</p>
      </div>
    </div>

    <loading-spinner v-if="cargandoDatos" message="Cargando formulario..." />

    <div v-else class="create-content">
      <form @submit.prevent="guardarProyecto" class="project-form">

        <!-- Sección: Información Básica -->
        <div class="form-section">
          <div class="section-header">
            <h2 class="section-title">📋 Información Básica</h2>
            <span class="required-note">* Campos obligatorios</span>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label class="form-label">
                Nombre del Proyecto *
                <span class="label-hint">Título descriptivo de tu proyecto</span>
              </label>
              <input v-model="formulario.nombre" type="text" class="form-input"
                placeholder="Ej: Sistema de Gestión de Proyectos de Grado" required maxlength="200" />
              <span class="char-count">{{ formulario.nombre.length }}/200</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label class="form-label">
                Descripción *
                <span class="label-hint">Describe brevemente tu proyecto</span>
              </label>
              <textarea v-model="formulario.descripcion" class="form-textarea" rows="4"
                placeholder="Describe el problema que resuelve tu proyecto, su alcance y principales características..."
                required maxlength="1000"></textarea>
              <span class="char-count">{{ formulario.descripcion.length }}/1000</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label class="form-label">
                Objetivos *
                <span class="label-hint">Define los objetivos que persigue tu proyecto</span>
              </label>
              <textarea v-model="formulario.objetivos" class="form-textarea" rows="4"
                placeholder="Lista los objetivos generales y específicos de tu proyecto..." required
                maxlength="1000"></textarea>
              <span class="char-count">{{ formulario.objetivos.length }}/1000</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                Profesor Asesor *
                <span class="label-hint">Selecciona tu director de proyecto</span>
              </label>
              <select v-model="formulario.profesor_id" class="form-select" required>
                <option value="">-- Selecciona un profesor --</option>
                <option v-for="profesor in profesores" :key="profesor.id" :value="profesor.id">
                  {{ profesor.nombre_completo }}
                </option>
              </select>
              <p v-if="profesores.length === 0" class="form-hint error">
                ⚠️ No hay profesores disponibles. Contacta con administración.
              </p>
            </div>
          </div>
        </div>

        <!-- Sección: Presupuesto -->
        <div class="form-section">
          <div class="section-header">
            <h2 class="section-title">💰 Presupuesto Estimado</h2>
            <button type="button" @click="agregarItem" class="btn btn-sm btn-secondary">
              ➕ Agregar Item
            </button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                Presupuesto Total Estimado *
                <span class="label-hint">Monto total solicitado (COP)</span>
              </label>
              <div class="input-with-prefix">
                <span class="input-prefix">$</span>
                <input v-model.number="formulario.presupuesto_estimado" type="number" class="form-input" placeholder="0"
                  required min="0" step="1000" />
              </div>
              <p class="form-hint">
                💡 Presupuesto calculado automáticamente: <strong>${{ formatMoney(presupuestoCalculado) }}</strong>
              </p>
            </div>
          </div>

          <!-- Items del Presupuesto -->
          <div v-if="formulario.items_presupuesto.length > 0" class="budget-items">
            <h3 class="subsection-title">📝 Desglose del Presupuesto</h3>

            <div v-for="(item, index) in formulario.items_presupuesto" :key="index" class="budget-item-card">
              <div class="item-header">
                <span class="item-number">Item {{ index + 1 }}</span>
                <button type="button" @click="eliminarItem(index)" class="btn-delete" title="Eliminar item">
                  🗑️
                </button>
              </div>

              <div class="item-content">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Concepto *</label>
                    <input v-model="item.concepto" type="text" class="form-input" placeholder="Ej: Equipos de cómputo"
                      required />
                  </div>

                  <div class="form-group">
                    <label class="form-label">Costo *</label>
                    <div class="input-with-prefix">
                      <span class="input-prefix">$</span>
                      <input v-model.number="item.costo" type="number" class="form-input" placeholder="0" required
                        min="0" @input="calcularPresupuestoTotal" />
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">Justificación *</label>
                  <textarea v-model="item.justificacion" class="form-textarea" rows="2"
                    placeholder="Explica por qué necesitas este recurso..." required></textarea>
                </div>
              </div>
            </div>

            <div class="budget-total">
              <span class="total-label">Total Calculado:</span>
              <span class="total-amount">${{ formatMoney(presupuestoCalculado) }}</span>
            </div>
          </div>

          <div v-else class="empty-budget">
            <span class="empty-icon">📋</span>
            <p>No has agregado items al presupuesto</p>
            <button type="button" @click="agregarItem" class="btn btn-primary">
              ➕ Agregar Primer Item
            </button>
          </div>
        </div>

        <!-- Botones de Acción -->
        <div class="form-actions">
          <button type="button" @click="cancelar" class="btn btn-secondary btn-lg">
            ❌ Cancelar
          </button>

          <button type="button" @click="guardarBorrador" class="btn btn-outline btn-lg" :disabled="enviando">
            💾 Guardar Borrador
          </button>

          <button type="submit" class="btn btn-primary btn-lg" :disabled="enviando">
            <span v-if="enviando">⏳ Creando...</span>
            <span v-else>✅ Crear Proyecto</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Barra de Progreso -->
    <div class="progress-indicator">
      <div class="progress-step" :class="{ completed: formulario.nombre }">
        <span class="step-number">1</span>
        <span class="step-label">Información</span>
      </div>
      <div class="progress-step" :class="{ completed: formulario.presupuesto_estimado > 0 }">
        <span class="step-number">2</span>
        <span class="step-label">Presupuesto</span>
      </div>
      <div class="progress-step" :class="{ completed: formulario.items_presupuesto.length > 0 }">
        <span class="step-number">3</span>
        <span class="step-label">Items</span>
      </div>
    </div>

    <notification-center />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { projectService } from '@/services/projectService'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import NotificationCenter from '@/components/shared/NotificationCenter.vue'

const router = useRouter()
const authStore = useAuthStore()
const notifStore = useNotificationStore()

const cargandoDatos = ref(false)
const enviando = ref(false)
const profesores = ref([])

const formulario = ref({
  nombre: '',
  descripcion: '',
  objetivos: '',
  profesor_id: '',
  presupuesto_estimado: 0,
  items_presupuesto: []
})

const presupuestoCalculado = computed(() => {
  return formulario.value.items_presupuesto.reduce((sum, item) => {
    return sum + (parseFloat(item.costo) || 0)
  }, 0)
})

onMounted(async () => {
  await cargarProfesores()
})

const cargarProfesores = async () => {
  try {
    cargandoDatos.value = true

    // Intentar primero el endpoint específico de profesores
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/profesores', {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })

      if (response.ok) {
        profesores.value = await response.json()
        console.log('Profesores cargados:', profesores.value)

        if (profesores.value.length === 0) {
          notifStore.addNotification({
            tipo: 'warning',
            titulo: 'Sin Profesores',
            mensaje: 'No hay profesores registrados en el sistema'
          })
        }
        return
      }
    } catch (error) {
      console.warn('Endpoint /profesores no disponible, intentando /usuarios')
    }

    // Si falla, intentar con el endpoint de usuarios
    const response = await fetch('http://localhost:8000/api/v1/auth/usuarios', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    if (!response.ok) {
      throw new Error('No se pudo cargar la lista de usuarios')
    }

    const usuarios = await response.json()

    // Filtrar solo profesores
    profesores.value = usuarios.filter(u => u.rol === 'profesor')
    console.log('Profesores filtrados:', profesores.value)

    if (profesores.value.length === 0) {
      notifStore.addNotification({
        tipo: 'warning',
        titulo: 'Sin Profesores',
        mensaje: 'No hay profesores registrados en el sistema. Por favor contacta al administrador.'
      })
    }

  } catch (error) {
    console.error('Error al cargar profesores:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar la lista de profesores. Verifica tu conexión.'
    })
    profesores.value = []
  } finally {
    cargandoDatos.value = false
  }
}


const agregarItem = () => {
  formulario.value.items_presupuesto.push({
    concepto: '',
    costo: 0,
    justificacion: ''
  })
}

const eliminarItem = (index) => {
  formulario.value.items_presupuesto.splice(index, 1)
  calcularPresupuestoTotal()
}

const calcularPresupuestoTotal = () => {
  formulario.value.presupuesto_estimado = presupuestoCalculado.value
}

const validarFormulario = () => {
  if (!formulario.value.nombre.trim()) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'El nombre del proyecto es obligatorio'
    })
    return false
  }

  if (!formulario.value.descripcion.trim()) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'La descripción del proyecto es obligatoria'
    })
    return false
  }

  if (!formulario.value.objetivos.trim()) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'Los objetivos del proyecto son obligatorios'
    })
    return false
  }

  if (!formulario.value.profesor_id) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'Debes seleccionar un profesor asesor'
    })
    return false
  }

  if (formulario.value.presupuesto_estimado <= 0) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Presupuesto Inválido',
      mensaje: 'El presupuesto debe ser mayor a cero'
    })
    return false
  }

  if (formulario.value.items_presupuesto.length === 0) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Sin Items',
      mensaje: 'Se recomienda agregar items al presupuesto'
    })
  }

  // Validar que todos los items tengan datos completos
  for (let i = 0; i < formulario.value.items_presupuesto.length; i++) {
    const item = formulario.value.items_presupuesto[i]
    if (!item.concepto || !item.costo || !item.justificacion) {
      notifStore.addNotification({
        tipo: 'error',
        titulo: 'Item Incompleto',
        mensaje: `El item ${i + 1} tiene campos vacíos`
      })
      return false
    }
  }

  return true
}

const guardarProyecto = async () => {
  if (!validarFormulario()) return

  try {
    enviando.value = true

    const proyecto = {
      nombre: formulario.value.nombre.trim(),
      descripcion: formulario.value.descripcion.trim(),
      objetivos: formulario.value.objetivos.trim(),
      profesor_id: parseInt(formulario.value.profesor_id),
      presupuesto_estimado: formulario.value.presupuesto_estimado,
      items_presupuesto: formulario.value.items_presupuesto,
      estado: 'borrador'
    }

    await projectService.create(proyecto)

    notifStore.addNotification({
      tipo: 'success',
      titulo: '✅ Proyecto Creado',
      mensaje: 'El proyecto ha sido creado exitosamente como borrador'
    })

    router.push('/proyectos')
  } catch (error) {
    console.error('Error:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: error.response?.data?.detail || 'No se pudo crear el proyecto'
    })
  } finally {
    enviando.value = false
  }
}

const guardarBorrador = async () => {
  if (!formulario.value.nombre.trim()) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Nombre Requerido',
      mensaje: 'Debes ingresar al menos el nombre del proyecto'
    })
    return
  }

  await guardarProyecto()
}

const cancelar = () => {
  const confirmacion = confirm('¿Estás seguro de cancelar? Se perderán los datos ingresados.')
  if (confirmacion) {
    router.push('/proyectos')
  }
}

const volver = () => {
  cancelar()
}

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value || 0)
}
</script>

<style scoped>
.project-create-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: var(--space-8);
  position: relative;
}

.create-header {
  max-width: 1200px;
  margin: 0 auto var(--space-8);
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-weight: 700;
  color: var(--gray-700);
  cursor: pointer;
  transition: var(--transition-base);
  margin-bottom: var(--space-6);
}

.btn-back:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  transform: translateX(-5px);
}

.header-content {
  text-align: center;
  margin-bottom: var(--space-4);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.page-subtitle {
  font-size: 1.125rem;
  color: var(--gray-600);
}

.create-content {
  max-width: 1200px;
  margin: 0 auto;
}

.project-form {
  background: white;
  border-radius: var(--radius-2xl);
  padding: var(--space-10);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: var(--space-10);
  padding-bottom: var(--space-8);
  border-bottom: 3px solid var(--gray-100);
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-8);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--gray-900);
}

.required-note {
  font-size: 0.875rem;
  color: var(--gray-500);
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--gray-900);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.label-hint {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--gray-500);
}

.form-input,
.form-select,
.form-textarea {
  padding: var(--space-4);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-size: 1rem;
  font-family: var(--font-sans);
  transition: var(--transition-base);
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.char-count {
  font-size: 0.75rem;
  color: var(--gray-500);
  text-align: right;
  margin-top: var(--space-1);
}

.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: var(--space-4);
  font-weight: 700;
  color: var(--gray-600);
  font-size: 1.125rem;
}

.input-with-prefix .form-input {
  padding-left: var(--space-10);
}

.form-hint {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-top: var(--space-2);
}

.form-hint.error {
  color: var(--error);
  font-weight: 600;
}

.subsection-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.budget-items {
  margin-top: var(--space-6);
}

.budget-item-card {
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
  transition: var(--transition-base);
}

.budget-item-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-3);
  border-bottom: 2px solid var(--gray-100);
}

.item-number {
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--primary);
  background: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  border: 2px solid var(--primary);
}

.btn-delete {
  background: var(--error-light);
  color: var(--error);
  border: none;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 1.125rem;
  transition: var(--transition-base);
}

.btn-delete:hover {
  background: var(--error);
  color: white;
  transform: scale(1.1);
}

.item-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.budget-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-6);
  background: var(--gradient-blue);
  color: white;
  border-radius: var(--radius-xl);
  margin-top: var(--space-6);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.total-label {
  font-size: 1.25rem;
  font-weight: 700;
}

.total-amount {
  font-size: 2rem;
  font-weight: 900;
}

.empty-budget {
  text-align: center;
  padding: var(--space-12);
  background: var(--gray-50);
  border-radius: var(--radius-xl);
  border: 2px dashed var(--gray-300);
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: var(--space-4);
  padding-top: var(--space-8);
}

.btn-outline {
  background: white;
  border: 2px solid var(--primary);
  color: var(--primary);
}

.btn-outline:hover:not(:disabled) {
  background: var(--primary);
  color: white;
}

.progress-indicator {
  position: fixed;
  bottom: var(--space-8);
  right: var(--space-8);
  background: white;
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  gap: var(--space-3);
  z-index: 100;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
}

.step-number {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-200);
  color: var(--gray-600);
  border-radius: 50%;
  font-weight: 700;
  transition: var(--transition-base);
}

.progress-step.completed .step-number {
  background: var(--success);
  color: white;
}

.step-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--gray-600);
}

.progress-step.completed .step-label {
  color: var(--success);
}

@media (max-width: 768px) {
  .project-create-view {
    padding: var(--space-4);
  }

  .page-title {
    font-size: 1.75rem;
  }

  .project-form {
    padding: var(--space-6);
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }

  .progress-indicator {
    bottom: var(--space-4);
    right: var(--space-4);
    left: var(--space-4);
  }
}
</style>
