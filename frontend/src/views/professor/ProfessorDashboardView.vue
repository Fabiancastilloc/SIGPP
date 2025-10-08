<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP - Profesor</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <span class="badge badge-professor">{{ authStore.user?.rol }}</span>
        <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
      </div>
    </nav>

    <div class="sidebar">
      <router-link to="/professor/dashboard" class="menu-item active">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/professor/projects" class="menu-item">
        <span>📁</span> Proyectos Asesorados
      </router-link>
      <router-link to="/professor/expenses" class="menu-item">
        <span>💰</span> Gastos por Aprobar
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <h1>Panel del Profesor</h1>
        <p>Gestión de proyectos y aprobación de gastos</p>

        <div v-if="loading" class="loading">Cargando estadísticas...</div>

        <div v-else-if="stats" class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📁</div>
            <h3>Proyectos Asesorados</h3>
            <div class="stat-value">{{ stats.proyectos.total_proyectos }}</div>
            <div class="stat-details">
              <p>✅ Activos: {{ stats.proyectos.proyectos_activos }}</p>
              <p>⏳ Pendientes Validación: {{ stats.proyectos.proyectos_pendientes }}</p>
              <p>✔️ Finalizados: {{ stats.proyectos.proyectos_finalizados }}</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">💵</div>
            <h3>Presupuesto Total</h3>
            <div class="stat-value">${{ formatNumber(stats.presupuesto.presupuesto_total_asignado) }}</div>
            <div class="stat-details">
              <p>📊 Ejecutado: ${{ formatNumber(stats.presupuesto.presupuesto_total_ejecutado) }}</p>
              <p>💰 Disponible: ${{ formatNumber(stats.presupuesto.presupuesto_disponible) }}</p>
              <p>📈 % Ejecución: {{ stats.presupuesto.porcentaje_ejecucion }}%</p>
            </div>
          </div>

          <div class="stat-card stat-card-warning">
            <div class="stat-icon">⏰</div>
            <h3>Gastos Pendientes</h3>
            <div class="stat-value">{{ stats.gastos.gastos_pendientes }}</div>
            <div class="stat-details">
              <p>✅ Aprobados: {{ stats.gastos.gastos_aprobados }}</p>
              <p>❌ Rechazados: {{ stats.gastos.gastos_rechazados }}</p>
              <p>Total: {{ stats.gastos.total_gastos }}</p>
            </div>
            <router-link to="/professor/expenses" class="btn btn-warning btn-block">
              Ver Gastos Pendientes
            </router-link>
          </div>
        </div>

        <div class="actions-section">
          <h2>Acciones Rápidas</h2>
          <div class="action-cards">
            <router-link to="/professor/projects" class="action-card">
              <span class="action-icon">📋</span>
              <h3>Revisar Proyectos</h3>
              <p>Validar y aprobar proyectos de estudiantes</p>
            </router-link>

            <router-link to="/professor/expenses" class="action-card">
              <span class="action-icon">💸</span>
              <h3>Aprobar Gastos</h3>
              <p>Revisar y aprobar solicitudes de gastos</p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { dashboardService } from '@/services/dashboardService'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref(null)
const loading = ref(true)

const loadStats = async () => {
  try {
    stats.value = await dashboardService.getStats()
  } catch (error) {
    console.error('Error al cargar estadísticas:', error)
  } finally {
    loading.value = false
  }
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.navbar {
  background: white;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
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

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.badge-professor {
  background-color: #6610f2;
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  width: 220px;
  background: white;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  padding-top: 20px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.menu-item:hover {
  background-color: #f0f0f0;
}

.menu-item.active {
  background-color: #667eea;
  color: white;
}

.main-content {
  margin-left: 220px;
  margin-top: 60px;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card-warning {
  border-left: 4px solid #ffc107;
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.stat-card h3 {
  color: #667eea;
  margin-bottom: 15px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.stat-details p {
  margin: 5px 0;
  color: #666;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-warning {
  background-color: #ffc107;
  color: #333;
}

.btn-block {
  width: 100%;
  margin-top: 15px;
}

.actions-section {
  margin-top: 40px;
}

.actions-section h2 {
  color: #333;
  margin-bottom: 20px;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  text-align: center;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 15px;
}

.action-card h3 {
  color: #667eea;
  margin-bottom: 10px;
}

.action-card p {
  color: #666;
  font-size: 14px;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
}
</style>
