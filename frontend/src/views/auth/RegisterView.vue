<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>Registro de Usuario</h1>
        <p>SIGPP - Universidad de Cartagena</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <div v-if="success" class="alert alert-success">{{ success }}</div>

        <div class="form-group">
          <label>Código Institucional *</label>
          <input type="text" v-model="userData.codigo_institucional" class="form-control" placeholder="Ej: EST2025001"
            required />
        </div>

        <div class="form-group">
          <label>Email Institucional *</label>
          <input type="email" v-model="userData.email_institucional" class="form-control"
            placeholder="usuario@unicartagena.edu.co" required />
        </div>

        <div class="form-group">
          <label>Nombre Completo *</label>
          <input type="text" v-model="userData.nombre_completo" class="form-control" placeholder="Nombre completo"
            required />
        </div>

        <div class="form-group">
          <label>Rol *</label>
          <select v-model="userData.rol" class="form-control" required>
            <option value="">Seleccione un rol</option>
            <option value="estudiante">Estudiante</option>
            <option value="profesor">Profesor</option>
            <option value="financiera">Área Financiera</option>
            <option value="auditor">Auditor</option>
          </select>
        </div>

        <div class="form-group">
          <label>Contraseña *</label>
          <input type="password" v-model="userData.password" class="form-control" placeholder="Mínimo 8 caracteres"
            required minlength="8" />
        </div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>

        <div class="register-footer">
          <p>¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userData = ref({
  codigo_institucional: '',
  email_institucional: '',
  nombre_completo: '',
  rol: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await authStore.register(userData.value)
    success.value = 'Registro exitoso. Redirigiendo...'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  font-size: 28px;
  color: #667eea;
  margin-bottom: 10px;
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

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-block {
  width: 100%;
  padding: 12px;
  font-size: 16px;
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

.register-footer {
  text-align: center;
  margin-top: 20px;
}

.register-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}
</style>
