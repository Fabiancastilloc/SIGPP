<template>
  <div class="admin-settings-page">
    <div class="container">
      <div class="page-header">
        <h1>⚙️ Configuración del Sistema</h1>
        <router-link to="/admin" class="btn-back">← Volver</router-link>
      </div>

      <div class="settings-section">
        <h2>🔧 Configuración General</h2>
        <div class="settings-form">
          <div class="setting-item">
            <label>Nombre del Sistema</label>
            <input v-model="settings.systemName" class="form-control" />
          </div>
          <div class="setting-item">
            <label>Email de Contacto</label>
            <input v-model="settings.contactEmail" type="email" class="form-control" />
          </div>
          <button @click="saveSettings" class="btn-save">💾 Guardar Cambios</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AdminSettings',
  setup() {
    const settings = ref({
      systemName: 'SIGPP',
      contactEmail: 'admin@unicartagena.edu.co'
    })
    
    const saveSettings = () => {
      alert('Configuración guardada')
    }
    
    return { settings, saveSettings }
  }
}
</script>

<style scoped>
.admin-settings-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.btn-back {
  padding: 10px 20px;
  background: white;
  border-radius: 8px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  border: 2px solid var(--gray-200);
}

.settings-section {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.settings-section h2 {
  margin-bottom: 24px;
}

.settings-form {
  max-width: 600px;
}

.setting-item {
  margin-bottom: 20px;
}

.setting-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 2px solid var(--gray-300);
  border-radius: 8px;
}

.btn-save {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
</style>
