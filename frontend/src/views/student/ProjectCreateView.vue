<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <router-link to="/dashboard" class="btn btn-secondary">Volver</router-link>
      </div>
    </nav>

    <div class="main-content">
      <div class="container">
        <h1>Crear Nuevo Proyecto</h1>

        <form @submit.prevent="handleSubmit" class="project-form">
          <div v-if="error" class="alert alert-error">{{ error }}</div>
          <div v-if="success" class="alert alert-success">{{ success }}</div>

          <div class="form-section">
            <h3>Información General</h3>

            <div class="form-group">
              <label>Nombre del Proyecto *</label>
              <input type="text" v-model="projectData.nombre" class="form-control"
                placeholder="Nombre descriptivo del proyecto" required minlength="10" />
            </div>

            <div class="form-group">
              <label>Descripción *</label>
              <textarea v-model="projectData.descripcion" class="form-control" rows="4"
                placeholder="Describe tu proyecto de grado" required minlength="20"></textarea>
            </div>

            <div class="form-group">
              <label>Objetivos *</label>
              <textarea v-model="projectData.objetivos" class="form-control" rows="4"
                placeholder="Objetivos del proyecto" required minlength="20"></textarea>
            </div>

            <div class="form-group">
              <label>Profesor Asesor *</label>
              <select v-model="projectData.profesor_id" class="form-control" required>
                <option value="">Seleccione un profesor</option>
                <option v-for="profesor in profesores" :key="profesor.id" :value="profesor.id">
                  {{ profesor.nombre_completo }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-section">
            <h3>Presupuesto</h3>

            <div v-for="(item, index) in projectData.items_presupuesto" :key="index" class="budget-item">
              <div class="budget-item-header">
                <h4>Item {{ index + 1 }}</h4>
                <button type="button" @click="removeItem(index)" class="btn-remove"
                  v-if="projectData.items_presupuesto.length > 1">
                  Eliminar
                </button>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Concepto *</label>
                  <input type="text" v-model="item.concepto" class="form-control"
                    placeholder="Ej: Materiales de laboratorio" required minlength="5" />
                </div>

                <div class="form-group">
                  <label>Costo (COP) *</label>
                  <input type="number" v-model="item.costo" class="form-control" placeholder="0" required min="1" />
                </div>
              </div>

              <div class="form-group">
                <label>Justificación *</label>
                <textarea v-model="item.justificacion" class="form-control" rows="2"
                  placeholder="Justifica por qué necesitas este gasto" required minlength="10"></textarea>
              </div>
            </div>

            <button type="button" @click="addItem" class="btn btn-secondary">
              + Agregar Item
            </button>

            <div class="total-presupuesto">
              <strong>Total Presupuesto:</strong>
              <span>${{ formatNumber(calcularTotal()) }}</span>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Creando...' : 'Crear Proyecto' }}
            </button>
            <router-link to="/projects" class="btn btn-secondary">Cancelar</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { projectService } from '@/services/projectService'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const projectData = ref({
  nombre: '',
  descripcion: '',
  objetivos: '',
  profesor_id: '',
  items_presupuesto: [
    {
      concepto: '',
      justificacion: '',
      costo: ''
    }
  ]
})

const profesores = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

const loadProfesores = async () => {
  try {
    // Esto es un placeholder - deberías tener un endpoint para listar profesores
    profesores.value = [
      { id: 1, nombre_completo: 'Dr. Juan Pérez' },
      { id: 2, nombre_completo: 'Dra. María García' }
    ]
  } catch (err) {
    console.error('Error al cargar profesores:', err)
  }
}

const addItem = () => {
  projectData.value.items_presupuesto.push({
    concepto: '',
    justificacion: '',
    costo: ''
  })
}

const removeItem = (index) => {
  projectData.value.items_presupuesto.splice(index, 1)
}

const calcularTotal = () => {
  return projectData.value.items_presupuesto.reduce((total, item) => {
    return total + (parseFloat(item.costo) || 0)
  }, 0)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await projectService.create(projectData.value)
    success.value = 'Proyecto creado exitosamente'
    setTimeout(() => {
      router.push('/projects')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al crear proyecto'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfesores()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background: white;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h2 {
  color: #667eea;
  margin: 0;
}

.navbar-menu {
  display: flex;
  gap: 15px;
  align-items: center;
}

.main-content {
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.project-form {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid #ddd;
}

.form-section h3 {
  color: #667eea;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
}

.budget-item {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.budget-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.budget-item-header h4 {
  margin: 0;
  color: #333;
}

.btn-remove {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 12px;
}

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 15px;
}

.total-presupuesto {
  margin-top: 20px;
  padding: 15px;
  background: #e8f4f8;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  font-size: 18px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
}
</style>
