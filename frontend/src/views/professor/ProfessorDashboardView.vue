<template>
  <div class="professor-dashboard">
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">Dashboard del Profesor</h1>
        <p class="page-subtitle">Bienvenido, {{ usuario?.nombrecompleto }}</p>
      </div>
      <notification-center />
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="dashboard-content">
      <!-- Estadísticas Rápidas -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon">🎓</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Asesorados</p>
            <h3 class="stat-value">{{ stats.totalProyectos }}</h3>
            <p class="stat-change">{{ stats.proyectosActivos }} activos</p>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">Pendientes de Validación</p>
            <h3 class="stat-value">{{ stats.pendientesValidacion }}</h3>
            <p class="stat-change">Requieren revisión</p>
          </div>
        </div>

        <div class="stat-card card-info">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <p class="stat-label">Gastos Pendientes</p>
            <h3 class="stat-value">{{ stats.gastosPendientes }}</h3>
            <p class="stat-change">{{ formatMoney(stats.montoGastosPendientes) }}</p>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Presupuesto Total</p>
            <h3 class="stat-value">{{ formatMoney(stats.presupuestoTotal) }}</h3>
            <p class="stat-change">COP</p>
          </div>
        </div>
      </div>

      <!-- Proyectos Recientes -->
      <div class="recent-projects">
        <div class="section-header">
          <h2 class="section-title">Proyectos Asesorados</h2>
          <router-link to="/profesor/proyectos" class="link-primary">Ver todos</router-link>
        </div>

        <div v-if="proyectos.length === 0" class="empty-state">
          <span class="empty-icon">📚</span>
          <h3>No tienes proyectos asignados aún</h3>
          <p>Los estudiantes te enviarán sus propuestas para revisión</p>
        </div>

        <div v-else class="projects-grid">
          <div v-for="proyecto in proyectos.slice(0, 4)" :key="proyecto.id" class="project-card">
            <div class="project-header">
              <h3 class="project-title">{{ proyecto.nombre }}</h3>
              <project-status-badge :estado="proyecto.estado" />
            </div>
            <p class="project-description">{{ truncate(proyecto.descripcion, 100) }}</p>
            <div class="project-meta">
              <div class="meta-item">
                <span class="meta-icon">👤</span>
                <span>{{ proyecto.estudiante?.nombrecompleto || 'Estudiante' }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">💵</span>
                <span>{{ formatMoney(proyecto.presupuestoasignado || proyecto.presupuestoestimado) }}</span>
              </div>
            </div>
            <div class="project-progress" v-if="proyecto.estado === 'activo'">
              <div class="progress-label">
                <span>Ejecución</span>
                <span>{{ calcularPorcentajeEjecucion(proyecto) }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: calcularPorcentajeEjecucion(proyecto) + '%' }"
                  :class="{ 'progress-warning': calcularPorcentajeEjecucion(proyecto) >= 80 }"></div>
              </div>
            </div>
            <div class="project-footer">
              <router-link :to="`/profesor/proyectos/${proyecto.id}`" class="btn btn-sm btn-primary">
                Ver Detalle
              </router-link>
              <button v-if="proyecto.estado === 'pendiente_validacion'" @click="validarProyecto(proyecto)"
                class="btn btn-sm btn-success">
                Validar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Gastos Pendientes de Aprobación -->
      <div class="pending-expenses">
        <div class="section-header">
          <h2 class="section-title">Gastos Pendientes de Aprobación</h2>
          <router-link to="/profesor/proyectos" class="link-primary">Ver todos</router-link>
        </div>

        <div v-if="gastosPendientes.length === 0" class="empty-state-small">
          <p>No hay gastos pendientes de aprobación</p>
        </div>

        <div v-else class="expenses-list">
          <div v-for="gasto in gastosPendientes.slice(0, 5)" :key="gasto.id" class="expense-item">
            <div class="expense-info">
              <h4 class="expense-concept">{{ gasto.concepto }}</h4>
              <p class="expense-project">{{ gasto.proyecto?.nombre || 'Proyecto' }}</p>
            </div>
            <div class="expense-details">
              <span class="expense-amount">{{ formatMoney(gasto.monto) }}</span>
              <div class="expense-actions">
                <button @click="aprobarGasto(gasto.id)" class="btn-icon approve" title="Aprobar">
                  ✓
                </button>
                <button @click="rechazarGasto(gasto.id)" class="btn-icon reject" title="Rechazar">
                  ✗
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alertas de Presupuesto -->
      <div v-if="alertasPresupuesto.length > 0" class="budget-alerts">
        <h2 class="section-title">⚠️ Alertas de Presupuesto</h2>
        <div class="alerts-list">
          <div v-for="alerta in alertasPresupuesto" :key="alerta.id" class="alert-item">
            <span class="alert-icon">⚠️</span>
            <div class="alert-content">
              <h4>{{ alerta.proyecto.nombre }}</h4>
              <p>Ejecución presupuestal: <strong>{{ alerta.porcentaje }}%</strong></p>
            </div>
            <router-link :to="`/profesor/proyectos/${alerta.proyecto.id}`" class="btn btn-sm btn-warning">
              Ver Proyecto
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { projectService } from '@/services/projectService';
import { expenseService } from '@/services/expenseService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';
import NotificationCenter from '@/components/shared/NotificationCenter.vue';
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue';

const router = useRouter();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const loading = ref(false);
const proyectos = ref([]);
const gastos = ref([]);

const usuario = computed(() => authStore.user);

const stats = computed(() => ({
  totalProyectos: proyectos.value.length,
  proyectosActivos: proyectos.value.filter(p => p.estado === 'activo').length,
  pendientesValidacion: proyectos.value.filter(p => p.estado === 'pendiente_validacion').length,
  gastosPendientes: gastos.value.filter(g => g.estado === 'pendiente').length,
  montoGastosPendientes: gastos.value
    .filter(g => g.estado === 'pendiente')
    .reduce((sum, g) => sum + parseFloat(g.monto || 0), 0),
  presupuestoTotal: proyectos.value.reduce(
    (sum, p) => sum + parseFloat(p.presupuestoasignado || p.presupuestoestimado || 0),
    0
  )
}));

const gastosPendientes = computed(() =>
  gastos.value.filter(g => g.estado === 'pendiente')
);

const alertasPresupuesto = computed(() => {
  return proyectos.value
    .filter(p => p.estado === 'activo')
    .map(p => {
      const porcentaje = calcularPorcentajeEjecucion(p);
      return { proyecto: p, porcentaje };
    })
    .filter(a => a.porcentaje >= 80 && a.porcentaje < 100);
});

onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  try {
    loading.value = true;
    // Cargar proyectos donde el profesor es el asesor
    const [proyectosData, gastosData] = await Promise.all([
      projectService.getAll({ profesorid: usuario.value.id }),
      expenseService.getAll()
    ]);

    proyectos.value = proyectosData;

    // Filtrar gastos solo de los proyectos del profesor
    const proyectosIds = proyectosData.map(p => p.id);
    gastos.value = gastosData.filter(g => proyectosIds.includes(g.proyectoid));

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

const calcularPorcentajeEjecucion = (proyecto) => {
  const presupuesto = parseFloat(proyecto.presupuestoasignado || proyecto.presupuestoestimado || 0);
  if (presupuesto === 0) return 0;

  const gastosProyecto = gastos.value.filter(
    g => g.proyectoid === proyecto.id && g.estado === 'aprobado'
  );
  const ejecutado = gastosProyecto.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0);

  return Math.round((ejecutado / presupuesto) * 100);
};

const validarProyecto = (proyecto) => {
  router.push(`/profesor/proyectos/${proyecto.id}`);
};

const aprobarGasto = async (gastoId) => {
  if (!confirm('¿Aprobar este gasto?')) return;

  try {
    await expenseService.approve(gastoId);
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Gasto Aprobado',
      mensaje: 'El gasto ha sido aprobado exitosamente'
    });
    await cargarDatos();
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo aprobar el gasto'
    });
  }
};

const rechazarGasto = async (gastoId) => {
  const comentario = prompt('Comentario (opcional):');
  if (comentario === null) return;

  try {
    await expenseService.reject(gastoId, comentario);
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Gasto Rechazado',
      mensaje: 'El gasto ha sido rechazado'
    });
    await cargarDatos();
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo rechazar el gasto'
    });
  }
};

const truncate = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value || 0);
};
</script>

<style scoped>
.professor-dashboard {
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

.stat-card.card-warning {
  border-left-color: var(--warning);
}

.stat-card.card-success {
  border-left-color: var(--success);
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

.recent-projects,
.pending-expenses,
.budget-alerts {
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

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--gray-900);
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

.project-progress {
  margin-bottom: var(--space-4);
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}

.progress-bar {
  height: 8px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--success);
  transition: width 0.3s ease;
}

.progress-fill.progress-warning {
  background: var(--warning);
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
  gap: var(--space-2);
}

.expense-amount {
  font-size: 1rem;
  font-weight: 700;
  color: var(--success);
}

.expense-actions {
  display: flex;
  gap: var(--space-2);
}

.btn-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-base);
  font-size: 1rem;
  font-weight: bold;
}

.btn-icon.approve:hover {
  background: var(--success);
  color: white;
}

.btn-icon.reject:hover {
  background: var(--error);
  color: white;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.alert-item {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: var(--radius-lg);
}

.alert-icon {
  font-size: 2rem;
}

.alert-content {
  flex: 1;
}

.alert-content h4 {
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-1);
}

.alert-content p {
  color: var(--gray-700);
  font-size: 0.875rem;
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
}

.empty-state-small {
  text-align: center;
  padding: var(--space-8);
  color: var(--gray-500);
}

@media (max-width: 768px) {
  .professor-dashboard {
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
}
</style>
