<template>
  <div class="project-edit-view">
    <div class="edit-header">
      <button @click="volver" class="btn-back">
        <span>←</span> Volver
      </button>
      <h1 class="page-title">✏️ Editar Proyecto</h1>
    </div>

    <loading-spinner v-if="loading" overlay />

    <div v-else-if="proyecto" class="edit-container">
      <div class="alert-info">
        <strong>Estado actual:</strong>
        <ProjectStatusBadge :estado="proyecto.estado" />
        <p v-if="proyecto.estado === 'rechazado'" class="warning-text">
          ⚠️ Al guardar cambios, el proyecto volverá a estado "Borrador"
        </p>
      </div>

      <form @submit.prevent="guardarCambios" class="edit-form">
        <div class="form-section">
          <h3>📋 Información General</h3>

          <div class="form-group">
            <label>Nombre del Proyecto *</label>
            <input v-model="formData.nombre" type="text" class="input" required placeholder="Nombre del proyecto" />
          </div>

          <div class="form-group">
            <label>Descripción *</label>
            <textarea v-model="formData.descripcion" class="input" rows="5" required
              placeholder="Describe el proyecto..."></textarea>
          </div>

          <div class="form-group">
            <label>Objetivos *</label>
            <textarea v-model="formData.objetivos" class="input" rows="5" required
              placeholder="Objetivos del proyecto..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <div class="section-header">
            <h3>💰 Presupuesto</h3>
            <button type="button" @click="agregarItem" class="btn btn-secondary btn-sm">
              ➕ Agregar Item
            </button>
          </div>

          <div v-if="formData.items_presupuesto.length === 0" class="empty-items">
            <p>No hay items de presupuesto. Agrega al menos uno.</p>
          </div>

          <div v-else class="items-list">
            <div v-for="(item, index) in formData.items_presupuesto" :key="index" class="budget-item">
              <div class="item-header">
                <span class="item-number">Item {{ index + 1 }}</span>
                <button type="button" @click="eliminarItem(index)" class="btn-delete">
                  🗑️
                </button>
              </div>

              <div class="form-group">
                <label>Concepto *</label>
                <input v-model="item.concepto" type="text" class="input" required placeholder="Ej: Materiales" />
              </div>

              <div class="form-group">
                <label>Justificación *</label>
                <textarea v-model="item.justificacion" class="input" rows="3" required
                  placeholder="Justifica este gasto..."></textarea>
              </div>

              <div class="form-group">
                <label>Costo (COP) *</label>
                <input v-model.number="item.costo" type="number" class="input" required min="0" step="0.01"
                  placeholder="0" />
              </div>
            </div>
          </div>

          <div class="total-presupuesto">
            <strong>Total:</strong>
            <span>${{ formatMoney(totalPresupuesto) }}</span>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-actions">
          <button type="button" @click="volver" class="btn btn-secondary">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : '💾 Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { projectService } from '@/services/projectService'
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const router = useRouter()
const route = useRoute()

const proyecto = ref(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const formData = ref({
  nombre: '',
  descripcion: '',
  objetivos: '',
  items_presupuesto: []
})

const totalPresupuesto = computed(() => {
  return formData.value.items_presupuesto.reduce((sum, item) => {
    return sum + (Number(item.costo) || 0)
  }, 0)
})

onMounted(async () => {
  await cargarProyecto()
})

const cargarProyecto = async () => {
  try {
    loading.value = true
    const proyectoId = route.params.id
    proyecto.value = await projectService.getById(proyectoId)

    if (proyecto.value.estado !== 'borrador' && proyecto.value.estado !== 'rechazado') {
      alert('Este proyecto no puede ser editado en su estado actual')
      router.push('/proyectos')
      return
    }

    formData.value = {
      nombre: proyecto.value.nombre,
      descripcion: proyecto.value.descripcion,
      objetivos: proyecto.value.objetivos,
      items_presupuesto: proyecto.value.items_presupuesto?.map(item => ({
        concepto: item.concepto,
        justificacion: item.justificacion,
        costo: item.costo
      })) || []
    }
  } catch (err) {
    console.error('Error:', err)
    error.value = 'Error al cargar el proyecto'
  } finally {
    loading.value = false
  }
}

const agregarItem = () => {
  formData.value.items_presupuesto.push({
    concepto: '',
    justificacion: '',
    costo: 0
  })
}

const eliminarItem = (index) => {
  if (formData.value.items_presupuesto.length === 1) {
    alert('Debe haber al menos un item de presupuesto')
    return
  }
  formData.value.items_presupuesto.splice(index, 1)
}

const guardarCambios = async () => {
  try {
    saving.value = true
    error.value = ''

    if (formData.value.items_presupuesto.length === 0) {
      error.value = 'Debes agregar al menos un item de presupuesto'
      return
    }

    await projectService.update(route.params.id, formData.value)
    alert('✅ Proyecto actualizado exitosamente')
    router.push('/proyectos')
  } catch (err) {
    console.error('Error:', err)
    error.value = err.response?.data?.detail || 'Error al guardar cambios'
  } finally {
    saving.value = false
  }
}

const volver = () => {
  router.push('/proyectos')
}

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value)
}
</script>

<style scoped>
.project-edit-view {
  padding: var(--space-8);
  max-width: 1000px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease;
}

.edit-header {
  margin-bottom: var(--space-8);
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: white;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-weight: 600;
  color: var(--gray-700);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-bottom: var(--space-6);
}

.btn-back:hover {
  background: var(--gray-100);
  transform: translateX(-3px);
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
}

.alert-info {
  background: #e3f2fd;
  border-left: 4px solid var(--info);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-8);
}

.warning-text {
  margin-top: var(--space-2);
  color: var(--warning);
  font-weight: 600;
}

.edit-form {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-100);
}

.form-section {
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-8);
  border-bottom: 2px solid var(--gray-200);
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h3 {
  color: var(--gray-900);
  margin-bottom: var(--space-6);
  font-size: 1.25rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.form-group {
  margin-bottom: var(--space-5);
}

.form-group label {
  display: block;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: var(--space-2);
  font-size: 0.875rem;
}

.empty-items {
  text-align: center;
  padding: var(--space-12);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  color: var(--gray-600);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.budget-item {
  background: var(--gray-50);
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.item-number {
  font-weight: 700;
  color: var(--primary);
  font-size: 0.875rem;
  background: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
}

.btn-delete {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.btn-delete:hover {
  background: var(--error);
  transform: scale(1.1);
}

.total-presupuesto {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  background: var(--primary);
  color: white;
  border-radius: var(--radius-lg);
  margin-top: var(--space-6);
  font-size: 1.25rem;
}

.total-presupuesto span {
  font-size: 1.5rem;
  font-weight: 700;
}

.error-message {
  background: #ffebee;
  color: var(--error);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--error);
  margin-bottom: var(--space-4);
}

.form-actions {
  display: flex;
  gap: var(--space-4);
  justify-content: flex-end;
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 2px solid var(--gray-200);
}

@media (max-width: 768px) {
  .project-edit-view {
    padding: var(--space-4);
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }
}
</style>
