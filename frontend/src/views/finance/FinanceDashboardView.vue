<template>
  <div class="finance-dashboard">
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">📊 Dashboard Financiero</h1>
        <p class="page-subtitle">Panel de control y supervisión presupuestal</p>
      </div>
      <notification-center />
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="dashboard-content">
      <!-- Estadísticas Principales -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Pendientes</p>
            <h3 class="stat-value">{{ stats.proyectosPendientes }}</h3>
            <p class="stat-change">Esperando aprobación financiera</p>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Activos</p>
            <h3 class="stat-value">{{ stats.proyectosActivos }}</h3>
            <p class="stat-change">Con presupuesto asignado</p>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <p class="stat-label">Presupuesto Total Asignado</p>
            <h3 class="stat-value">{{ formatMoney(stats.presupuestoTotal) }}</h3>
            <p class="stat-change">COP</p>
          </div>
        </div>

        <div class="stat-card card-info">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <p class="stat-label">Presupuesto Ejecutado</p>
            <h3 class="stat-value">{{ formatMoney(stats.presupuestoEjecutado) }}</h3>
            <p class="stat-change">{{ stats.porcentajeEjecucion }}% ejecutado</p>
          </div>
        </div>
      </div>

      <!-- Acciones Rápidas -->
      <div class="quick-actions">
        <h2 class="section-title">⚡ Acciones Rápidas</h2>
        <div class="actions-grid">
          <router-link to="/finance/projects?estado=validado_asesor" class="action-card">
            <div class="action-icon">📝</div>
            <div class="action-content">
              <h3>Revisar Proyectos</h3>
              <p>{{ stats.proyectosPendientes }} proyectos pendientes</p>
            </div>
          </router-link>

          <router-link to="/finance/expenses" class="action-card">
            <div class="action-icon">💳</div>
            <div class="action-content">
              <h3>Gastos y Egresos</h3>
              <p>Supervisar ejecución presupuestal</p>
            </div>
          </router-link>

          <button @click="generarReporte" class="action-card">
            <div class="action-icon">📊</div>
            <div class="action-content">
              <h3>Generar Reportes</h3>
              <p>Exportar datos en PDF/Excel</p>
            </div>
          </button>

          <button @click="verAnalisis" class="action-card">
            <div class="action-icon">🔍</div>
            <div class="action-content">
              <h3>Análisis Financiero</h3>
              <p>Estadísticas y tendencias</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Proyectos Pendientes de Aprobación -->
      <div class="pending-projects">
        <div class="section-header">
          <h2 class="section-title">📋 Proyectos Pendientes de Aprobación</h2>
          <router-link to="/finance/projects" class="link-primary">Ver todos</router-link>
        </div>

        <div v-if="proyectosPendientes.length === 0" class="empty-state">
          <span class="empty-icon">📭</span>
          <h3>No hay proyectos pendientes</h3>
          <p>Todos los proyectos están aprobados o en revisión</p>
        </div>

        <div v-else class="projects-grid">
          <div v-for="proyecto in proyectosPendientes.slice(0, 4)" :key="proyecto.id" class="project-card">
            <div class="project-header">
              <h3 class="project-title">{{ proyecto.nombre }}</h3>
              <span class="project-badge validado">Validado por Asesor</span>
            </div>

            <div class="project-info">
              <div class="info-row">
                <span class="info-label">Código:</span>
                <span class="info-value">{{ proyecto.codigoproyecto }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Estudiante:</span>
                <span class="info-value">{{ proyecto.estudiantenombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Presupuesto Estimado:</span>
                <span class="info-value amount">{{ formatMoney(proyecto.presupuestoestimado) }}</span>
              </div>
            </div>

            <div class="project-footer">
              <router-link :to="`/finance/projects/${proyecto.id}`" class="btn btn-sm btn-primary">
                Revisar Proyecto
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Proyectos Activos -->
      <div class="active-projects">
        <div class="section-header">
          <h2 class="section-title">✅ Proyectos Activos</h2>
          <router-link to="/finance/projects?estado=activo" class="link-primary">Ver todos</router-link>
        </div>

        <div v-if="proyectosActivos.length === 0" class="empty-state-small">
          <p>No hay proyectos activos en este momento</p>
        </div>

        <div v-else class="table-wrapper">
          <table class="projects-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Proyecto</th>
                <th>Estudiante</th>
                <th>Presupuesto Asignado</th>
                <th>Ejecutado</th>
                <th>% Ejecución</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="proyecto in proyectosActivos.slice(0, 5)" :key="proyecto.id">
                <td class="cell-code">{{ proyecto.codigoproyecto }}</td>
                <td class="cell-name">{{ proyecto.nombre }}</td>
                <td>{{ proyecto.estudiantenombre }}</td>
                <td class="cell-money">{{ formatMoney(proyecto.presupuestoasignado) }}</td>
                <td class="cell-money">{{ formatMoney(proyecto.presupuestoejecutado) }}</td>
                <td>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: `${calcularPorcentaje(proyecto)}%` }"
                      :class="getProgressClass(calcularPorcentaje(proyecto))"></div>
                    <span class="progress-text">{{ calcularPorcentaje(proyecto) }}%</span>
                  </div>
                </td>
                <td>
                  <router-link :to="`/finance/projects/${proyecto.id}`" class="btn-icon" title="Ver detalle">
                    👁️
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { projectService } from '@/services/projectService';
import { dashboardService } from '@/services/dashboardService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';
import NotificationCenter from '@/components/shared/NotificationCenter.vue';

const router = useRouter();
const notifStore = useNotificationStore();

const loading = ref(false);
const proyectosPendientes = ref([]);
const proyectosActivos = ref([]);

const stats = computed(() => ({
  proyectosPendientes: proyectosPendientes.value.length,
  proyectosActivos: proyectosActivos.value.length,
  presupuestoTotal: proyectosActivos.value.reduce((sum, p) => sum + parseFloat(p.presupuestoasignado || 0), 0),
  presupuestoEjecutado: proyectosActivos.value.reduce((sum, p) => sum + parseFloat(p.presupuestoejecutado || 0), 0),
  porcentajeEjecucion: (() => {
    const total = proyectosActivos.value.reduce((sum, p) => sum + parseFloat(p.presupuestoasignado || 0), 0);
    const ejecutado = proyectosActivos.value.reduce((sum, p) => sum + parseFloat(p.presupuestoejecutado || 0), 0);
    return total > 0 ? Math.round((ejecutado / total) * 100) : 0;
  })()
}));

onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  try {
    loading.value = true;

    // Cargar proyectos pendientes de finanzas (validado_asesor)
    const pendientes = await projectService.getAll({ estado: 'validado_asesor' });
    proyectosPendientes.value = pendientes;

    // Cargar proyectos activos
    const activos = await projectService.getAll({ estado: 'activo' });
    proyectosActivos.value = activos;
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar la información del dashboard'
    });
  } finally {
    loading.value = false;
  }
};

const calcularPorcentaje = (proyecto) => {
  if (!proyecto.presupuestoasignado || proyecto.presupuestoasignado === 0) return 0;
  return Math.min(Math.round((proyecto.presupuestoejecutado / proyecto.presupuestoasignado) * 100), 100);
};

const getProgressClass = (porcentaje) => {
  if (porcentaje >= 90) return 'fill-danger';
  if (porcentaje >= 70) return 'fill-warning';
  return 'fill-success';
};

const generarReporte = () => {
  router.push('/finance/reports');
};

const verAnalisis = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: 'Próximamente',
    mensaje: 'Función de análisis financiero en desarrollo'
  });
};

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(value || 0);
};
</script>

<style scoped>
.finance-dashboard {
  padding: var(--space-8);
  max-width: 1600px;
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
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
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
  border-left: 5px solid var(--primary);
  transition: var(--transition-base);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
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
  font-size: 3rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
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
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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
  font-size: 2.5rem;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.action-content h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-1);
}

.action-content p {
  font-size: 0.875rem;
  color: var(--gray-600);
}

.pending-projects,
.active-projects {
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
  border: 2px solid var(--gray-200);
  transition: var(--transition-base);
}

.project-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
}

.project-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  flex: 1;
  margin-right: var(--space-3);
}

.project-badge {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
}

.project-badge.validado {
  background: var(--warning-light);
  color: #92400e;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9375rem;
}

.info-label {
  color: var(--gray-600);
  font-weight: 600;
}

.info-value {
  color: var(--gray-900);
  font-weight: 700;
}

.info-value.amount {
  color: var(--primary);
  font-size: 1.125rem;
}

.project-footer {
  padding-top: var(--space-4);
  border-top: 1px solid var(--gray-200);
}

.table-wrapper {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.projects-table {
  width: 100%;
  border-collapse: collapse;
}

.projects-table thead {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.projects-table th {
  padding: var(--space-4);
  text-align: left;
  font-weight: 800;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.projects-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  font-size: 0.9375rem;
}

.projects-table tbody tr:hover {
  background: var(--gray-50);
}

.cell-code {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--primary);
}

.cell-name {
  font-weight: 600;
  max-width: 300px;
}

.cell-money {
  font-weight: 700;
  color: var(--success);
}

.progress-bar {
  position: relative;
  width: 100%;
  height: 24px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: var(--space-2);
  transition: width 0.5s ease;
}

.progress-text {
  color: white;
  font-weight: 700;
  font-size: 0.75rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.fill-success {
  background: linear-gradient(90deg, var(--success), #34d399);
}

.fill-warning {
  background: linear-gradient(90deg, var(--warning), #fbbf24);
}

.fill-danger {
  background: linear-gradient(90deg, var(--error), #f87171);
}

.btn-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-base);
  text-decoration: none;
  font-size: 1.125rem;
}

.btn-icon:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
}

.empty-icon {
  font-size: 5rem;
  display: block;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.empty-state p {
  color: var(--gray-600);
  font-size: 1.125rem;
}

.empty-state-small {
  text-align: center;
  padding: var(--space-8);
  color: var(--gray-500);
}

@media (max-width: 768px) {
  .finance-dashboard {
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

  .table-wrapper {
    overflow-x: scroll;
  }
}
</style>
