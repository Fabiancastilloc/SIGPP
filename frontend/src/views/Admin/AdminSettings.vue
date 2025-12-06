<template>
  <div class="admin-settings-page">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <router-link to="/admin" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Panel
        </router-link>
        
        <div class="header-title">
          <h1>⚙️ Configuración del Sistema</h1>
          <p>Administra los parámetros generales del sistema SIGPP</p>
        </div>
      </div>

      <!-- Settings Sections -->
      <div class="settings-grid">
        <!-- General Settings -->
        <div class="settings-section">
          <div class="section-header">
            <div class="header-icon">🔧</div>
            <h2>Configuración General</h2>
          </div>

          <div class="settings-form">
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                Nombre del Sistema
              </label>
              <input 
                v-model="settings.systemName" 
                type="text"
                class="form-control" 
                placeholder="SIGPP"
              />
              <span class="form-hint">El nombre que aparecerá en toda la aplicación</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Email de Contacto
              </label>
              <input 
                v-model="settings.contactEmail" 
                type="email"
                class="form-control" 
                placeholder="admin@unicartagena.edu.co"
              />
              <span class="form-hint">Correo para notificaciones y soporte</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                Teléfono de Soporte
              </label>
              <input 
                v-model="settings.supportPhone" 
                type="tel"
                class="form-control" 
                placeholder="+57 300 123 4567"
              />
              <span class="form-hint">Número de contacto para asistencia técnica</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Descripción del Sistema
              </label>
              <textarea 
                v-model="settings.systemDescription" 
                class="form-control textarea"
                rows="4"
                placeholder="Sistema Integral de Gestión de Proyectos de Pregrado..."
              ></textarea>
              <span class="form-hint">Descripción que aparecerá en la página principal</span>
            </div>
          </div>
        </div>

        <!-- Preferences -->
        <div class="settings-section">
          <div class="section-header">
            <div class="header-icon">🎨</div>
            <h2>Preferencias</h2>
          </div>

          <div class="settings-form">
            <div class="toggle-group">
              <div class="toggle-item">
                <div class="toggle-info">
                  <span class="toggle-label">Modo Mantenimiento</span>
                  <span class="toggle-hint">Desactiva temporalmente el sistema para todos los usuarios</span>
                </div>
                <label class="toggle-switch">
                  <input v-model="settings.maintenanceMode" type="checkbox" />
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-info">
                  <span class="toggle-label">Permitir Registro de Usuarios</span>
                  <span class="toggle-hint">Los usuarios pueden registrarse sin autorización previa</span>
                </div>
                <label class="toggle-switch">
                  <input v-model="settings.allowRegistration" type="checkbox" />
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-info">
                  <span class="toggle-label">Notificaciones por Email</span>
                  <span class="toggle-hint">Enviar notificaciones automáticas a los usuarios</span>
                </div>
                <label class="toggle-switch">
                  <input v-model="settings.emailNotifications" type="checkbox" />
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div class="toggle-item">
                <div class="toggle-info">
                  <span class="toggle-label">Auditoría Detallada</span>
                  <span class="toggle-hint">Registrar todas las acciones en el sistema de auditoría</span>
                </div>
                <label class="toggle-switch">
                  <input v-model="settings.detailedAudit" type="checkbox" />
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Limits -->
        <div class="settings-section">
          <div class="section-header">
            <div class="header-icon">📊</div>
            <h2>Límites y Restricciones</h2>
          </div>

          <div class="settings-form">
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Proyectos Máximos por Estudiante
              </label>
              <input 
                v-model.number="settings.maxProjectsPerStudent" 
                type="number"
                class="form-control" 
                min="1"
                max="10"
              />
              <span class="form-hint">Cantidad máxima de proyectos simultáneos</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Presupuesto Máximo por Proyecto (COP)
              </label>
              <input 
                v-model.number="settings.maxBudgetPerProject" 
                type="number"
                class="form-control" 
                step="1000000"
              />
              <span class="form-hint">Límite superior de presupuesto asignable</span>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Días para Aprobación de Profesor
              </label>
              <input 
                v-model.number="settings.professorApprovalDays" 
                type="number"
                class="form-control" 
                min="1"
                max="30"
              />
              <span class="form-hint">Tiempo límite para revisión académica</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="actions-bar">
        <button @click="resetSettings" class="btn-reset">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Restablecer
        </button>

        <button @click="saveSettings" class="btn-save" :disabled="saving">
          <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          <div v-else class="btn-spinner"></div>
          {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AdminSettings',
  setup() {
    const saving = ref(false)

    const settings = ref({
      systemName: 'SIGPP',
      contactEmail: 'admin@unicartagena.edu.co',
      supportPhone: '+57 300 123 4567',
      systemDescription: 'Sistema Integral de Gestión de Proyectos de Pregrado de la Universidad de Cartagena',
      maintenanceMode: false,
      allowRegistration: true,
      emailNotifications: true,
      detailedAudit: true,
      maxProjectsPerStudent: 3,
      maxBudgetPerProject: 50000000,
      professorApprovalDays: 7
    })
    
    const saveSettings = async () => {
      saving.value = true

      // Simulación de guardado
      setTimeout(() => {
        alert('✅ Configuración guardada exitosamente!')
        saving.value = false
      }, 1500)
    }

    const resetSettings = () => {
      if (confirm('¿Estás seguro de restablecer toda la configuración a los valores predeterminados?')) {
        settings.value = {
          systemName: 'SIGPP',
          contactEmail: 'admin@unicartagena.edu.co',
          supportPhone: '+57 300 123 4567',
          systemDescription: 'Sistema Integral de Gestión de Proyectos de Pregrado',
          maintenanceMode: false,
          allowRegistration: true,
          emailNotifications: true,
          detailedAudit: true,
          maxProjectsPerStudent: 3,
          maxBudgetPerProject: 50000000,
          professorApprovalDays: 7
        }
        alert('⚠️ Configuración restablecida')
      }
    }
    
    return { settings, saving, saveSettings, resetSettings }
  }
}
</script>

<style scoped>
/* BASE */
.admin-settings-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  padding: 32px 16px;
  position: relative;
}

/* ANIMATED BACKGROUND */
.dashboard-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
  animation: float 25s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  top: -300px;
  left: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -250px;
  right: -250px;
  animation-delay: -12s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-50px, 50px) scale(0.9); }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER */
.page-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
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
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.3s;
  width: fit-content;
}

.btn-back:hover {
  background: #334155;
  border-color: #8b5cf6;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.header-title h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.header-title p {
  font-size: 16px;
  color: #cbd5e1;
  font-weight: 600;
}

/* SETTINGS GRID */
.settings-grid {
  display: grid;
  gap: 24px;
  margin-bottom: 32px;
}

.settings-section {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 28px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
}

.header-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 6px rgba(139, 92, 246, 0.4));
}

.section-header h2 {
  font-size: 20px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.settings-form {
  padding: 28px;
}

/* FORM GROUPS */
.form-group {
  margin-bottom: 28px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-weight: 700;
  font-size: 14px;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-label svg {
  width: 18px;
  height: 18px;
  color: #8b5cf6;
}

.form-control {
  width: 100%;
  padding: 14px 18px;
  background: rgba(15, 23, 42, 0.8);
  border: 2px solid #334155;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.form-control.textarea {
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

.form-hint {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}

/* TOGGLE SWITCHES */
.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid #334155;
  border-radius: 12px;
  transition: all 0.3s;
}

.toggle-item:hover {
  background: rgba(139, 92, 246, 0.05);
  border-color: rgba(139, 92, 246, 0.3);
}

.toggle-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toggle-label {
  font-size: 15px;
  font-weight: 700;
  color: #f1f5f9;
}

.toggle-hint {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

.toggle-switch {
  position: relative;
  width: 56px;
  height: 30px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #334155;
  border-radius: 30px;
  transition: all 0.3s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  height: 22px;
  width: 22px;
  left: 4px;
  bottom: 4px;
  background: #ffffff;
  border-radius: 50%;
  transition: all 0.3s;
}

.toggle-switch input:checked + .toggle-slider {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(26px);
}

/* ACTIONS BAR */
.actions-bar {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  padding: 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 16px;
}

.btn-reset,
.btn-save {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 32px;
  border: 2px solid;
  border-radius: 12px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reset {
  background: transparent;
  border-color: #334155;
  color: #cbd5e1;
}

.btn-reset:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.btn-save {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  border-color: transparent;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reset svg,
.btn-save svg {
  width: 20px;
  height: 20px;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .admin-settings-page {
    padding: 20px 12px;
  }

  .toggle-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .actions-bar {
    flex-direction: column;
  }

  .btn-reset,
  .btn-save {
    width: 100%;
  }
}
</style>
