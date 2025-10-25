<template>
  <div class="edit-project-page">
    <div class="container">
      <router-link to="/student" class="btn-back">← Volver</router-link>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando proyecto...</p>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="project-form">
        <h1>✏️ Editar Proyecto</h1>

        <div class="form-card">
          <h3>📝 Información Básica</h3>
          
          <div class="form-group">
            <label>Nombre del Proyecto *</label>
            <input v-model="formData.nombre" class="form-control" required maxlength="200" />
          </div>

          <div class="form-group">
            <label>Descripción *</label>
            <textarea v-model="formData.descripcion" class="form-control" rows="6" required minlength="100"></textarea>
            <small>{{ formData.descripcion.length }}/2000 caracteres (mínimo 100)</small>
          </div>

          <div class="form-group">
            <label>Objetivos *</label>
            <textarea v-model="formData.objetivos" class="form-control" rows="6" required minlength="50"></textarea>
            <small>{{ formData.objetivos.length }}/1500 caracteres</small>
          </div>
        </div>

        <div class="form-card">
          <h3>👨‍🏫 Información Académica</h3>
          
          <div class="form-group">
            <label>Profesor Asesor *</label>
            <select v-model="formData.profesor_id" class="form-control" required>
              <option value="">-- Seleccionar --</option>
              <option v-for="prof in profesores" :key="prof.id" :value="prof.id">
                {{ prof.nombre_completo }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Presupuesto Estimado *</label>
            <div class="input-money">
              <span>$</span>
              <input v-model.number="formData.presupuesto_estimado" type="number" min="100000" required />
              <span>COP</span>
            </div>
          </div>
        </div>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <div class="form-actions">
          <button type="button" @click="goBack" class="btn btn-secondary">Cancelar</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? '⏳ Guardando...' : '💾 Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import projectsApi from '../../api/projects'
import catalogsApi from '../../api/catalogs'

export default {
  name: 'EditProject',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const formData = ref({
      nombre: '',
      descripcion: '',
      objetivos: '',
      profesor_id: '',
      presupuesto_estimado: null
    })
    
    const profesores = ref([])
    const loading = ref(true)
    const saving = ref(false)
    const error = ref('')
    
    const projectId = parseInt(route.params.id)
    
    const loadProject = async () => {
      try {
        const [projectRes, profRes] = await Promise.all([
          projectsApi.getProjectById(projectId),
          catalogsApi.getProfesores()
        ])
        
        const project = projectRes.data
        formData.value = {
          nombre: project.nombre,
          descripcion: project.descripcion,
          objetivos: project.objetivos,
          profesor_id: project.profesor.id,
          presupuesto_estimado: project.presupuesto_estimado
        }
        
        profesores.value = profRes.data
      } catch (err) {
        error.value = 'Error al cargar proyecto'
      } finally {
        loading.value = false
      }
    }
    
    const handleSubmit = async () => {
      saving.value = true
      error.value = ''
      try {
        await projectsApi.updateProject(projectId, formData.value)
        alert('✅ Proyecto actualizado')
        router.push('/student')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al guardar'
      } finally {
        saving.value = false
      }
    }
    
    const goBack = () => {
      if (confirm('¿Descartar cambios?')) router.push('/student')
    }
    
    onMounted(() => loadProject())
    
    return { formData, profesores, loading, saving, error, handleSubmit, goBack }
  }
}
</script>

<style scoped>
.edit-project-page {
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
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateX(-4px);
  border-color: var(--primary-color);
}

.project-form h1 {
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
  border: 2px solid var(--gray-200);
}

.form-card h3 {
  font-size: 20px;
  margin-bottom: 24px;
  color: var(--gray-900);
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--gray-700);
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group small {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: var(--gray-600);
}

.input-money {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 10px;
}

.input-money span {
  font-weight: 700;
  color: var(--gray-600);
}

.input-money input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  font-weight: 600;
}

.alert-error {
  padding: 16px;
  background: #fee2e2;
  border: 2px solid #ef4444;
  color: #991b1b;
  border-radius: 12px;
  margin-bottom: 24px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  padding: 12px 32px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn:hover {
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
