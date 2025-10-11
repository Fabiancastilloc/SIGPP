<template>
  <div class="home-view">
    <!-- Fondo Animado -->
    <div class="animated-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- Contenido Principal -->
    <div class="home-container">
      <!-- Sección Izquierda - Información -->
      <div class="info-section">
        <div class="logo-container">
          <img src="/logo.png" alt="Logo" class="logo-small" />
          <span class="logo-text">SIGPP</span>
        </div>

        <h1 class="main-title">
          Sistema de Gestión de<br />
          <span class="gradient-text">Proyectos de Grado</span>
        </h1>

        <p class="subtitle">
          Plataforma moderna y eficiente para la gestión integral de proyectos
          académicos en la Universidad de Cartagena
        </p>

        <div class="features-list">
          <div class="feature-item">
            <div class="feature-icon">✨</div>
            <div>
              <h4>Gestión Inteligente</h4>
              <p>Administra proyectos y presupuestos fácilmente</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">📊</div>
            <div>
              <h4>Reportes en Tiempo Real</h4>
              <p>Exporta y visualiza estadísticas al instante</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div>
              <h4>Seguro y Confiable</h4>
              <p>Protección de datos con autenticación JWT</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección Derecha - Formulario -->
      <div class="form-section">
        <div class="form-card">
          <!-- Tabs -->
          <div class="tabs">
            <button class="tab" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
              Iniciar Sesión
            </button>
            <button class="tab" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">
              Registrarse
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
            <h3>Bienvenido de nuevo</h3>
            <p class="form-subtitle">Ingresa tus credenciales para continuar</p>

            <div class="form-group">
              <label>Código Institucional</label>
              <input v-model="loginForm.codigo_institucional" type="text" class="input" placeholder="Ej: 0110111222"
                required />
            </div>

            <div class="form-group">
              <label>Contraseña</label>
              <input v-model="loginForm.password" type="password" class="input" placeholder="••••••••" required />
            </div>

            <div v-if="error" class="error-message">
              {{ error }}
            </div>

            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
            </button>
          </form>

          <!-- Register Form -->
          <form v-else @submit.prevent="handleRegister" class="auth-form">
            <h3>Crear cuenta</h3>
            <p class="form-subtitle">Completa el formulario para comenzar</p>

            <div class="form-grid">
              <div class="form-group">
                <label>Código Institucional *</label>
                <input v-model="registerForm.codigo_institucional" type="text" class="input" placeholder="0110111222"
                  required />
              </div>

              <div class="form-group">
                <label>Nombre Completo *</label>
                <input v-model="registerForm.nombre_completo" type="text" class="input" placeholder="Juan Pérez"
                  required />
              </div>
            </div>

            <div class="form-group">
              <label>Email Institucional *</label>
              <input v-model="registerForm.email_institucional" type="email" class="input"
                placeholder="usuario@unicartagena.edu.co" required />
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label>Contraseña *</label>
                <input v-model="registerForm.password" type="password" class="input" placeholder="Min. 8 caracteres"
                  required minlength="8" />
              </div>

              <div class="form-group">
                <label>Rol *</label>
                <select v-model="registerForm.rol" class="input" required>
                  <option value="">Seleccionar</option>
                  <option value="estudiante">Estudiante</option>
                  <option value="profesor">Profesor</option>
                  <option value="financiera">Financiera</option>
                </select>
              </div>
            </div>

            <!-- Campos de Facultad, Sede y Carrera -->
            <div class="academic-section">
              <h4 class="section-subtitle">Información Académica</h4>

              <div class="form-group">
                <label>Facultad</label>
                <select v-model="selectedFacultad" @change="onFacultadChange" class="input">
                  <option value="">Seleccione una facultad</option>
                  <option v-for="f in facultades" :key="f.id" :value="f.id">
                    {{ f.nombre }}
                  </option>
                  <option value="custom">✏️ Escribir manualmente</option>
                </select>
              </div>

              <div v-if="selectedFacultad === 'custom'" class="form-group">
                <label>Nombre de la Facultad</label>
                <input v-model="registerForm.facultad_custom" type="text" class="input"
                  placeholder="Ingrese el nombre de la facultad" />
              </div>

              <div class="form-group">
                <label>Sede</label>
                <select v-model="selectedSede" class="input">
                  <option value="">Seleccione una sede</option>
                  <option v-for="s in sedes" :key="s.id" :value="s.id">
                    {{ s.nombre }}
                  </option>
                  <option value="custom">✏️ Escribir manualmente</option>
                </select>
              </div>

              <div v-if="selectedSede === 'custom'" class="form-group">
                <label>Nombre de la Sede</label>
                <input v-model="registerForm.sede_custom" type="text" class="input"
                  placeholder="Ingrese el nombre de la sede" />
              </div>

              <div class="form-group">
                <label>Carrera/Programa</label>
                <select v-model="selectedCarrera" :disabled="!selectedFacultad || selectedFacultad === 'custom'"
                  class="input">
                  <option value="">Seleccione una carrera</option>
                  <option v-for="c in carrerasFiltradas" :key="c.id" :value="c.id">
                    {{ c.nombre }}
                  </option>
                  <option value="custom">✏️ Escribir manualmente</option>
                </select>
              </div>

              <div v-if="selectedCarrera === 'custom'" class="form-group">
                <label>Nombre de la Carrera</label>
                <input v-model="registerForm.carrera_custom" type="text" class="input"
                  placeholder="Ingrese el nombre de la carrera" />
              </div>
            </div>

            <div v-if="error" class="error-message">
              {{ error }}
            </div>

            <div v-if="success" class="success-message">
              {{ success }}
            </div>

            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? 'Registrando...' : 'Crear Cuenta' }}
            </button>
          </form>
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

const activeTab = ref('login')
const loading = ref(false)
const error = ref('')
const success = ref('')

const loginForm = ref({
  codigo_institucional: '',
  password: ''
})

const registerForm = ref({
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
  if (!selectedFacultad.value || selectedFacultad.value === 'custom') {
    return []
  }
  return carreras.value.filter(c => c.facultad_id === parseInt(selectedFacultad.value))
})

onMounted(async () => {
  await catalogStore.loadFacultades()
  await catalogStore.loadSedes()
  await catalogStore.loadCarreras()
})

const onFacultadChange = () => {
  selectedCarrera.value = ''
  registerForm.value.carrera_id = null
}

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    await authStore.login(loginForm.value)

    success.value = '✅ Inicio de sesión exitoso. Redirigiendo...'

    setTimeout(() => {
      const role = authStore.user?.rol
      if (role === 'estudiante') router.push('/dashboard')
      else if (role === 'profesor') router.push('/profesor/dashboard')
      else if (role === 'financiera') router.push('/financiera/dashboard')
      else router.push('/dashboard')
    }, 1000)
  } catch (err) {
    error.value = '❌ ' + (err.response?.data?.detail || 'Credenciales incorrectas. Verifica tu código y contraseña.')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    // Preparar datos según selección
    if (selectedFacultad.value !== 'custom' && selectedFacultad.value) {
      registerForm.value.facultad_id = parseInt(selectedFacultad.value)
      registerForm.value.facultad_custom = ''
    } else {
      registerForm.value.facultad_id = null
    }

    if (selectedSede.value !== 'custom' && selectedSede.value) {
      registerForm.value.sede_id = parseInt(selectedSede.value)
      registerForm.value.sede_custom = ''
    } else {
      registerForm.value.sede_id = null
    }

    if (selectedCarrera.value !== 'custom' && selectedCarrera.value) {
      registerForm.value.carrera_id = parseInt(selectedCarrera.value)
      registerForm.value.carrera_custom = ''
    } else {
      registerForm.value.carrera_id = null
    }

    await authStore.register(registerForm.value)

    success.value = '✅ Registro exitoso. Bienvenido a SIGPP. Redirigiendo...'

    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (err) {
    error.value = '❌ ' + (err.response?.data?.detail || 'Error al registrar. Verifica que el código y email no estén en uso.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ... (mantén todos los estilos anteriores) ... */

/* Nuevos estilos para la sección académica */
.academic-section {
  margin-top: var(--space-6);
  padding-top: var(--space-6);
  border-top: 2px solid var(--gray-100);
}

.section-subtitle {
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: var(--space-5);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.section-subtitle::before {
  content: '🎓';
  font-size: 1.25rem;
}

.success-message {
  background: #d1fae5;
  color: var(--success);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
  font-size: 0.875rem;
  border-left: 3px solid var(--success);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Ajustes para formulario más largo */
.form-card {
  max-height: 90vh;
  overflow-y: auto;
}

/* Scrollbar personalizada para el formulario */
.form-card::-webkit-scrollbar {
  width: 6px;
}

.form-card::-webkit-scrollbar-track {
  background: transparent;
}

.form-card::-webkit-scrollbar-thumb {
  background: var(--gray-300);
  border-radius: var(--radius-full);
}

.form-card::-webkit-scrollbar-thumb:hover {
  background: var(--gray-400);
}

/* Estilos anteriores continúan igual... */
.home-view {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
}

.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: rgba(102, 126, 234, 0.8);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: rgba(118, 75, 162, 0.8);
  bottom: 10%;
  right: 10%;
  animation-delay: 2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: rgba(79, 172, 254, 0.8);
  top: 50%;
  left: 50%;
  animation-delay: 4s;
}

.home-container {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-16);
  max-width: 1400px;
  width: 100%;
  align-items: center;
}

.info-section {
  color: white;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}

.logo-small {
  height: 40px;
  width: 40px;
  object-fit: contain;
  filter: brightness(0) invert(1);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.main-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: var(--space-6);
  color: white;
}

.gradient-text {
  background: linear-gradient(to right, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: var(--space-12);
  line-height: 1.7;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.feature-item {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
}

.feature-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.feature-item h4 {
  color: white;
  font-size: 1.125rem;
  margin-bottom: var(--space-1);
}

.feature-item p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9375rem;
}

.form-section {
  display: flex;
  justify-content: center;
}

.form-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  box-shadow: var(--shadow-2xl);
  width: 100%;
  max-width: 520px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-8);
  background: var(--gray-100);
  padding: var(--space-1);
  border-radius: var(--radius-lg);
}

.tab {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  border: none;
  background: transparent;
  border-radius: var(--radius-md);
  font-weight: 600;
  color: var(--gray-600);
  cursor: pointer;
  transition: all var(--transition-base);
}

.tab.active {
  background: white;
  color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.auth-form h3 {
  font-size: 1.5rem;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.form-subtitle {
  color: var(--gray-600);
  margin-bottom: var(--space-6);
  font-size: 0.9375rem;
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.btn-block {
  width: 100%;
  margin-top: var(--space-4);
}

.error-message {
  background: #fee2e2;
  color: var(--error);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
  font-size: 0.875rem;
  border-left: 3px solid var(--error);
  animation: slideIn 0.3s ease;
}

@media (max-width: 1024px) {
  .home-container {
    grid-template-columns: 1fr;
    gap: var(--space-8);
  }

  .info-section {
    text-align: center;
  }

  .features-list {
    max-width: 600px;
    margin: 0 auto;
  }

  .main-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: var(--space-6);
    max-width: 100%;
  }
}
</style>
