<template>
  <div class="student-dashboard">
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">Dashboard del Estudiante</h1>
        <p class="page-subtitle">Bienvenido, {{ usuario?.nombre_completo }}</p>
      </div>
      <notification-center />
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="dashboard-content">
      <!-- Estadísticas Rápidas -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon">📚</div>
          <div class="stat-info">
            <p class="stat-label">Mis Proyectos</p>
            <h3 class="stat-value">{{ stats.total_proyectos }}</h3>
            <p class="stat-change">
              {{ stats.proyectos_activos }} activos
            </p>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">En Revisión</p>
            <h3 class="stat-value">{{ stats.pendientes_validacion }}</h3>
            <p class="stat-change">Esperando validación</p>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <p class="stat-label">Presupuesto Total</p>
            <h3 class="stat-value">${{ formatMoney(stats.presupuesto_total) }}</h3>
            <p class="stat-change">COP</p>
          </div>
        </div>

        <div class="stat-card card-info">
          <div class="stat-icon">💸</div>
          <div class="stat-info">
            <p class="stat-label">Gastos Totales</p>
            <h3 class="stat-value">{{ stats.total_gastos }}</h3>
            <p class="stat-change">${{ formatMoney(stats.monto_gastos) }}</p>
          </div>
        </div>
      </div>

      <!-- Acciones Rápidas -->
      <div class="quick-actions">
        <h2 class="section-title">⚡ Acciones Rápidas</h2>
        <div class="actions-grid">
          <router-link to="/proyectos/crear" class="action-card">
            <div class="action-icon">➕</div>
            <div class="action-content">
              <h3>Nuevo Proyecto</h3>
              <p>Crea un proyecto de grado</p>
            </div>
          </router-link>

          <router-link to="/proyectos" class="action-card">
            <div class="action-icon">📂</div>
            <div class="action-content">
              <h3>Ver Proyectos</h3>
              <p>Gestiona tus proyectos</p>
            </div>
          </router-link>

          <router-link to="/gastos" class="action-card">
            <div class="action-icon">💸</div>
            <div class="action-content">
              <h3>Mis Gastos</h3>
              <p>Registra y consulta gastos</p>
            </div>
          </router-link>

          <button @click="mostrarAyuda" class="action-card">
            <div class="action-icon">❓</div>
            <div class="action-content">
              <h3>Ayuda</h3>
              <p>Guía de uso del sistema</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Proyectos Recientes -->
      <div class="recent-projects">
        <div class="section-header">
          <h2 class="section-title">📚 Mis Proyectos</h2>
          <router-link to="/proyectos" class="link-primary">
            Ver todos →
          </router-link>
        </div>

        <div v-if="proyectos.length === 0" class="empty-state">
          <span class="empty-icon">📂</span>
          <h3>No tienes proyectos aún</h3>
          <p>Comienza creando tu primer proyecto de grado</p>
          <router-link to="/proyectos/crear" class="btn btn-primary">
            ➕ Crear Proyecto
          </router-link>
        </div>

        <div v-else class="projects-grid">
          <div v-for="proyecto in proyectos.slice(0, 3)" :key="proyecto.id" class="project-card">
            <div class="project-header">
              <h3 class="project-title">{{ proyecto.nombre }}</h3>
              <project-status-badge :estado="proyecto.estado" />
            </div>

            <p class="project-description">{{ truncate(proyecto.descripcion, 100) }}</p>

            <div class="project-meta">
              <div class="meta-item">
                <span class="meta-icon">📅</span>
                <span>{{ formatDate(proyecto.fecha_creacion) }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">💰</span>
                <span>${{ formatMoney(proyecto.presupuesto_estimado) }}</span>
              </div>
            </div>

            <div class="project-footer">
              <router-link :to="`/proyectos/${proyecto.id}`" class="btn btn-sm btn-primary">
                Ver Detalle
              </router-link>
              <button v-if="puedeEditar(proyecto.estado)" @click="editarProyecto(proyecto.id)"
                class="btn btn-sm btn-secondary">
                ✏️ Editar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Gastos Recientes -->
      <div class="recent-expenses">
        <div class="section-header">
          <h2 class="section-title">💸 Gastos Recientes</h2>
          <router-link to="/gastos" class="link-primary">
            Ver todos →
          </router-link>
        </div>

        <div v-if="gastos.length === 0" class="empty-state-small">
          <p>No hay gastos registrados</p>
        </div>

        <div v-else class="expenses-list">
          <div v-for="gasto in gastos.slice(0, 5)" :key="gasto.id" class="expense-item">
            <div class="expense-info">
              <h4 class="expense-concept">{{ gasto.concepto }}</h4>
              <p class="expense-project">{{ getProyectoNombre(gasto.proyecto_id) }}</p>
            </div>
            <div class="expense-details">
              <span class="expense-amount">${{ formatMoney(gasto.monto) }}</span>
              <span class="expense-status" :class="`status-${gasto.estado}`">
                {{ formatEstado(gasto.estado) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { projectService } from '@/services/projectService'
import { expenseService } from '@/services/expenseService'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import NotificationCenter from '@/components/shared/NotificationCenter.vue'
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue'

const router = useRouter()
const authStore = useAuthStore()
const notifStore = useNotificationStore()

const loading = ref(false)
const proyectos = ref([])
const gastos = ref([])

const usuario = computed(() => authStore.user)

const stats = computed(() => ({
  total_proyectos: proyectos.value.length,
  proyectos_activos: proyectos.value.filter(p => p.estado === 'activo').length,
  pendientes_validacion: proyectos.value.filter(p => p.estado === 'pendiente_validacion').length,
  presupuesto_total: proyectos.value.reduce((sum, p) => sum + parseFloat(p.presupuesto_asignado || 0), 0),
  total_gastos: gastos.value.length,
  monto_gastos: gastos.value.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
}))

onMounted(async () => {
  await cargarDatos()
})

const cargarDatos = async () => {
  try {
    loading.value = true
    const [proyectosData, gastosData] = await Promise.all([
      projectService.getAll(),
      expenseService.getAll()
    ])
    proyectos.value = proyectosData
    gastos.value = gastosData
  } catch (error) {
    console.error('Error:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar la información del dashboard'
    })
  } finally {
    loading.value = false
  }
}

const puedeEditar = (estado) => {
  return estado === 'borrador' || estado === 'rechazado'
}

const editarProyecto = (id) => {
  router.push(`/proyectos/${id}/editar`)
}

const mostrarAyuda = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: '📖 Guía Rápida',
    mensaje: 'Puedes crear proyectos, registrar gastos y dar seguimiento a tus solicitudes en tiempo real'
  })
}

const getProyectoNombre = (id) => {
  const p = proyectos.value.find(x => x.id === id)
  return p ? p.nombre : `Proyecto ${id}`
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value || 0)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatEstado = (estado) => {
  const estados = {
    pendiente: 'Pendiente',
    aprobado: 'Aprobado',
    rechazado: 'Rechazado'
  }
  return estados[estado] || estado
}
</script>

<style scoped>
.student-dashboard {
  padding: var(--space-8);
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-8);
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
}

.page-subtitle {
  color: var(--gray-600);
  margin-top: var(--space-2);
  font-size: 1.125rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  display: flex;
  gap: var(--space-4);
  border-left: 4px solid var(--primary);
  transition: var(--transition-base);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-card.card-success {
  border-left-color: var(--success);
}

.stat-card.card-warning {
  border-left-color: var(--warning);
}

.stat-card.card-info {
  border-left-color: var(--info);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-bottom: var(--space-1);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--gray-900);
}

.stat-change {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-top: var(--space-1);
}

.quick-actions {
  margin-bottom: var(--space-8);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
}

.action-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 2px solid var(--gray-100);
  cursor: pointer;
  transition: var(--transition-base);
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.action-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.action-content h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-1);
}

.action-content p {
  font-size: 0.875rem;
  color: var(--gray-600);
}

.recent-projects,
.recent-expenses {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-8);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.link-primary {
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9375rem;
}

.link-primary:hover {
  text-decoration: underline;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
}

.project-card {
  background: var(--gray-50);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  border: 1px solid var(--gray-200);
  transition: var(--transition-base);
}

.project-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
}

.project-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  flex: 1;
  margin-right: var(--space-3);
}

.project-description {
  color: var(--gray-600);
  font-size: 0.9375rem;
  line-height: 1.6;
  margin-bottom: var(--space-4);
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
  word-break: break-word;
}

.project-meta {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.875rem;
  color: var(--gray-700);
}

.meta-icon {
  font-size: 1rem;
}

.project-footer {
  display: flex;
  gap: var(--space-2);
  padding-top: var(--space-4);
  border-top: 1px solid var(--gray-200);
}

.expenses-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  transition: var(--transition-base);
}

.expense-item:hover {
  background: var(--gray-100);
}

.expense-concept {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: var(--space-1);
}

.expense-project {
  font-size: 0.875rem;
  color: var(--gray-600);
}

.expense-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-1);
}

.expense-amount {
  font-size: 1rem;
  font-weight: 700;
  color: var(--success);
}

.expense-status {
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
}

.status-pendiente {
  background: var(--warning-light);
  color: #92400e;
}

.status-aprobado {
  background: var(--success-light);
  color: #065f46;
}

.status-rechazado {
  background: var(--error-light);
  color: #991b1b;
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.empty-state p {
  color: var(--gray-600);
  margin-bottom: var(--space-6);
}

.empty-state-small {
  text-align: center;
  padding: var(--space-8);
  color: var(--gray-500);
}

@media (max-width: 768px) {
  .student-dashboard {
    padding: var(--space-4);
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
