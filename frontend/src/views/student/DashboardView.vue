<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">
        <h2>SIGPP</h2>
      </div>
      <div class="navbar-menu">
        <span>{{ authStore.user?.nombre_completo }}</span>
        <span class="badge">{{ authStore.user?.rol }}</span>
        <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
      </div>
    </nav>

    <div class="sidebar">
      <router-link to="/dashboard" class="menu-item active">
        <span>📊</span> Dashboard
      </router-link>
      <router-link to="/projects" class="menu-item">
        <span>📁</span> Proyectos
      </router-link>
      <router-link to="/expenses" class="menu-item">
        <span>💰</span> Gastos
      </router-link>
    </div>

    <div class="main-content">
      <div class="container">
        <h1>Dashboard</h1>
        <p>Bienvenido al Sistema Integral de Gestión Presupuestal</p>

        <div v-if="loading" class="loading">Cargando estadísticas...</div>

        <div v-else-if="stats" class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📁</div>
            <h3>Proyectos</h3>
            <div class="stat-value">{{ stats.proyectos.total_proyectos }}</div>
            <div class="stat-details">
              <p>✅ Activos: {{ stats.proyectos.proyectos_activos }}</p>
              <p>⏳ Pendientes: {{ stats.proyectos.proyectos_pendientes }}</p>
              <p>✔️ Finalizados: {{ stats.proyectos.proyectos_finalizados }}</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">💵</div>
            <h3>Presupuesto</h3>
            <div class="stat-value">${{ formatNumber(stats.presupuesto.presupuesto_total_asignado) }}</div>
            <div class="stat-details">
              <p>📊 Ejecutado: ${{ formatNumber(stats.presupuesto.presupuesto_total_ejecutado) }}</p>
              <p>💰 Disponible: ${{ formatNumber(stats.presupuesto.presupuesto_disponible) }}</p>
              <p>📈 Ejecución: {{ stats.presupuesto.porcentaje_ejecucion }}%</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">🧾</div>
            <h3>Gastos</h3>
            <div class="stat-value">{{ stats.gastos.total_gastos }}</div>
            <div class="stat-details">
              <p>✅ Aprobados: {{ stats.gastos.gastos_aprobados }}</p>
              <p>⏳ Pendientes: {{ stats.gastos.gastos_pendientes }}</p>
              <p>❌ Rechazados: {{ stats.gastos.gastos_rechazados }}</p>
            </div>
          </div>
        </div>

        <div class="actions">
          <router-link to="/projects" class="btn btn-primary">Ver Proyectos</router-link>
          <router-link to="/expenses" class="btn btn-success">Ver Gastos</router-link>
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
  background-color: #17a2b8;
  color: white;
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
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

.container h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
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

.actions {
  display: flex;
  gap: 15px;
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
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #1e7e34;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
}
</style>
