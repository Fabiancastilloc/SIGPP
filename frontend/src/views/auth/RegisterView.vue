<template>
  <div class="register-view">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <div class="logo-circle">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h2>Crear cuenta</h2>
          <p>Únete al sistema de gestión de proyectos</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="codigo">Código Institucional</label>
              <input id="codigo" v-model="formData.codigo_institucional" type="text" required placeholder="0110111222"
                class="form-input" />
            </div>

            <div class="form-group">
              <label for="nombre">Nombre Completo</label>
              <input id="nombre" v-model="formData.nombre_completo" type="text" required placeholder="Juan Pérez López"
                class="form-input" />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email Institucional</label>
            <input id="email" v-model="formData.email_institucional" type="email" required
              placeholder="usuario@unicartagena.edu.co" class="form-input" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="password">Contraseña</label>
              <input id="password" v-model="formData.password" type="password" required minlength="8"
                placeholder="Mínimo 8 caracteres" class="form-input" />
            </div>

            <div class="form-group">
              <label for="rol">Rol</label>
              <select id="rol" v-model="formData.rol" required class="form-input">
                <option value="">Selecciona un rol</option>
                <option value="estudiante">Estudiante</option>
                <option value="profesor">Profesor</option>
                <option value="financiera">Financiera</option>
              </select>
            </div>
          </div>

          <div class="info-section">
            <h3>Información Académica</h3>

            <div class="form-row">
              <div class="form-group">
                <label for="facultad">Facultad</label>
                <select id="facultad" v-model="selectedFacultad" @change="onFacultadChange" class="form-input">
                  <option value="">Selecciona una facultad</option>
                  <option v-for="f in facultades" :key="f.id" :value="f.id">
                    {{ f.nombre }}
                  </option>
                  <option value="custom">✏️ Otra (escribir)</option>
                </select>
              </div>

              <div class="form-group">
                <label for="sede">Sede</label>
                <select id="sede" v-model="selectedSede" class="form-input">
                  <option value="">Selecciona una sede</option>
                  <option v-for="s in sedes" :key="s.id" :value="s.id">
                    {{ s.nombre }}
                  </option>
                  <option value="custom">✏️ Otra (escribir)</option>
                </select>
              </div>
            </div>

            <div v-if="selectedFacultad === 'custom'" class="form-group">
              <input v-model="formData.facultad_custom" type="text" placeholder="Escribe el nombre de la facultad"
                class="form-input" />
            </div>

            <div v-if="selectedSede === 'custom'" class="form-group">
              <input v-model="formData.sede_custom" type="text" placeholder="Escribe el nombre de la sede"
                class="form-input" />
            </div>

            <div class="form-group">
              <label for="carrera">Carrera/Programa</label>
              <select id="carrera" v-model="selectedCarrera"
                :disabled="!selectedFacultad || selectedFacultad === 'custom'" class="form-input">
                <option value="">Selecciona una carrera</option>
                <option v-for="c in carrerasFiltradas" :key="c.id" :value="c.id">
                  {{ c.nombre }}
                </option>
                <option value="custom">✏️ Otra (escribir)</option>
              </select>
            </div>

            <div v-if="selectedCarrera === 'custom'" class="form-group">
              <input v-model="formData.carrera_custom" type="text" placeholder="Escribe el nombre de la carrera"
                class="form-input" />
            </div>
          </div>

          <div v-if="error" class="error-alert">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            <span v-if="!loading">Crear Cuenta</span>
            <span v-else class="loading-spinner"></span>
          </button>
        </form>

        <div class="register-footer">
          <p>¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCatalogStore } from '@/stores/catalog'

const router = useRouter()
const authStore = useAuthStore()
const catalogStore = useCatalogStore()

const loading = ref(false)
const error = ref('')

const formData = ref({
  codigo_institucional: '',
  nombre_completo: '',
  email_institucional: '',
  password: '',
  rol: '',
  facultad_id: null,
  sede_id: null,
  carrera_id: null,
  facultad_custom: '',
  sede_custom: '',
  carrera_custom: ''
})

const selectedFacultad = ref('')
const selectedSede = ref('')
const selectedCarrera = ref('')

const facultades = computed(() => catalogStore.facultades)
const sedes = computed(() => catalogStore.sedes)
const carreras = computed(() => catalogStore.carreras)

const carrerasFiltradas = computed(() => {
  if (!selectedFacultad.value || selectedFacultad.value === 'custom') return []
  return carreras.value.filter(c => c.facultad_id === parseInt(selectedFacultad.value))
})

onMounted(async () => {
  await catalogStore.loadFacultades()
  await catalogStore.loadSedes()
  await catalogStore.loadCarreras()
})

const onFacultadChange = () => {
  selectedCarrera.value = ''
  formData.value.carrera_id = null
}

const handleRegister = async () => {
  try {
    loading.value = true
    error.value = ''

    if (selectedFacultad.value !== 'custom' && selectedFacultad.value) {
      formData.value.facultad_id = parseInt(selectedFacultad.value)
      formData.value.facultad_custom = ''
    } else {
      formData.value.facultad_id = null
    }

    if (selectedSede.value !== 'custom' && selectedSede.value) {
      formData.value.sede_id = parseInt(selectedSede.value)
      formData.value.sede_custom = ''
    } else {
      formData.value.sede_id = null
    }

    if (selectedCarrera.value !== 'custom' && selectedCarrera.value) {
      formData.value.carrera_id = parseInt(selectedCarrera.value)
      formData.value.carrera_custom = ''
    } else {
      formData.value.carrera_id = null
    }

    await authStore.register(formData.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: var(--space-8) var(--space-4);
}

.register-container {
  max-width: 700px;
  width: 100%;
}

.register-card {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--space-12) var(--space-8);
  box-shadow: var(--shadow-xl);
}

.register-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.logo-circle {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto var(--space-6);
}

.logo-circle svg {
  width: 32px;
  height: 32px;
}

.register-header h2 {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: var(--space-2);
}

.register-header p {
  color: var(--gray-600);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.info-section {
  padding: var(--space-6);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
}

.info-section h3 {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: var(--space-4);
  color: var(--gray-900);
}

.error-alert {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: var(--radius-lg);
  color: #991b1b;
  font-size: 0.875rem;
  font-weight: 500;
}

.error-alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.register-footer {
  margin-top: var(--space-6);
  text-align: center;
  padding-top: var(--space-6);
  border-top: 1px solid var(--gray-200);
}

.register-footer p {
  color: var(--gray-600);
}

.register-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
}

.register-footer a:hover {
  color: var(--primary-dark);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .register-card {
    padding: var(--space-8) var(--space-6);
  }
}
</style>
