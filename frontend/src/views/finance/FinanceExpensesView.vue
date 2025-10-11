<template>
  <div class="finance-expenses">
    <div class="page-header">
      <div>
        <h1 class="page-title">💳 Gestión de Gastos y Egresos</h1>
        <p class="page-subtitle">Supervisión de ejecución presupuestal</p>
      </div>
      <div class="header-actions">
        <button @click="exportarGastos" class="btn btn-outline">
          📥 Exportar Gastos
        </button>
        <notification-center />
      </div>
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="expenses-content">
      <!-- Estadísticas de Gastos -->
      <div class="stats-grid">
        <div class="stat-card card-info">
          <div class="stat-icon">📝</div>
          <div class="stat-info">
            <p class="stat-label">Total Gastos Registrados</p>
            <h3 class="stat-value">{{ stats.totalGastos }}</h3>
            <p class="stat-change">{{ formatMoney(stats.montoTotal) }} COP</p>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">Gastos Pendientes</p>
            <h3 class="stat-value">{{ stats.gastosPendientes }}</h3>
            <p class="stat-change">{{ formatMoney(stats.montoPendiente) }} COP</p>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Gastos Aprobados</p>
            <h3 class="stat-value">{{ stats.gastosAprobados }}</h3>
            <p class="stat-change">{{ formatMoney(stats.montoAprobado) }} COP</p>
          </div>
        </div>

        <div class="stat-card card-danger">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <p class="stat-label">Gastos Rechazados</p>
            <h3 class="stat-value">{{ stats.gastosRechazados }}</h3>
            <p class="stat-change">{{ formatMoney(stats.montoRechazado) }} COP</p>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-card">
        <h3 class="filters-title">🔍 Filtrar Gastos</h3>
        <div class="filters-grid">
          <div class="filter-group">
            <label>Proyecto</label>
            <select v-model="filtros.proyectoId" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los proyectos</option>
              <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">
                {{ proyecto.codigoproyecto }} - {{ proyecto.nombre }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Estado</label>
            <select v-model="filtros.estado" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendiente</option>
              <option value="aprobado">Aprobado</option>
              <option value="rechazado">Rechazado</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Búsqueda</label>
            <input v-model="filtros.busqueda" @input="aplicarFiltros" type="text" placeholder="Buscar por concepto..."
              class="form-input" />
          </div>

          <div class="filter-actions">
            <button @click="limpiarFiltros" class="btn btn-sm btn-outline">
              🔄 Limpiar
            </button>
          </div>
        </div>
      </div>

      <!-- Tabla de Gastos -->
      <div class="expenses-section">
        <div class="section-header">
          <h2 class="section-title">📋 Listado de Gastos</h2>
          <p class="section-subtitle">
            Mostrando {{ gastosFiltrados.length }} de {{ gastos.length }} gastos
          </p>
        </div>

        <div v-if="gastosFiltrados.length === 0" class="empty-state">
          <span class="empty-icon">📭</span>
          <h3>No hay gastos registrados</h3>
          <p>Los gastos aparecerán aquí cuando los estudiantes los registren</p>
        </div>

        <div v-else class="expenses-table-container">
          <table class="expenses-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Proyecto</th>
                <th>Estudiante</th>
                <th>Concepto</th>
                <th>Monto</th>
                <th>Estado</th>
                <th>Fecha Registro</th>
                <th>Soporte</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="gasto in gastosFiltrados" :key="gasto.id" class="table-row">
                <td class="cell-id">{{ gasto.id }}</td>
                <td class="cell-proyecto">
                  {{ getProyectoNombre(gasto.proyectoid) }}
                </td>
                <td>{{ gasto.estudiantenombre || 'N/A' }}</td>
                <td class="cell-concepto">{{ gasto.concepto }}</td>
                <td class="cell-money">{{ formatMoney(gasto.monto) }}</td>
                <td>
                  <span class="status-badge" :class="`status-${gasto.estado}`">
                    {{ formatEstado(gasto.estado) }}
                  </span>
                </td>
                <td class="cell-date">{{ formatDate(gasto.creadoen) }}</td>
                <td class="cell-soporte">
                  <a v-if="gasto.soporteurl" :href="gasto.soporteurl" target="_blank" class="btn-link">
                    📎 Ver
                  </a>
                  <span v-else>—</span>
                </td>
                <td class="cell-actions">
                  <div class="action-buttons">
                    <button @click="verDetalleGasto(gasto)" class="btn-action btn-view" title="Ver detalles">
                      👁️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Detalle de Gasto -->
    <div v-if="mostrarModalDetalle" class="modal-overlay" @click.self="cerrarModalDetalle">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">📄 Detalle del Gasto</h2>
          <button @click="cerrarModalDetalle" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <div class="detail-grid">
            <div class="detail-item">
              <label>ID del Gasto</label>
              <p>{{ gastoSeleccionado?.id }}</p>
            </div>

            <div class="detail-item">
              <label>Proyecto</label>
              <p>{{ getProyectoNombre(gastoSeleccionado?.proyectoid) }}</p>
            </div>

            <div class="detail-item">
              <label>Estudiante</label>
              <p>{{ gastoSeleccionado?.estudiantenombre }}</p>
            </div>

            <div class="detail-item">
              <label>Concepto</label>
              <p>{{ gastoSeleccionado?.concepto }}</p>
            </div>

            <div class="detail-item">
              <label>Monto</label>
              <p class="monto-destacado">{{ formatMoney(gastoSeleccionado?.monto) }} COP</p>
            </div>

            <div class="detail-item">
              <label>Estado</label>
              <span class="status-badge" :class="`status-${gastoSeleccionado?.estado}`">
                {{ formatEstado(gastoSeleccionado?.estado) }}
              </span>
            </div>

            <div class="detail-item">
              <label>Fecha de Registro</label>
              <p>{{ formatDateFull(gastoSeleccionado?.creadoen) }}</p>
            </div>

            <div class="detail-item" v-if="gastoSeleccionado?.aprobadoen">
              <label>Fecha de Aprobación</label>
              <p>{{ formatDateFull(gastoSeleccionado?.aprobadoen) }}</p>
            </div>

            <div class="detail-item full-width" v-if="gastoSeleccionado?.comentarios">
              <label>Comentarios</label>
              <p>{{ gastoSeleccionado?.comentarios }}</p>
            </div>

            <div class="detail-item full-width" v-if="gastoSeleccionado?.soporteurl">
              <label>Soporte</label>
              <a :href="gastoSeleccionado?.soporteurl" target="_blank" class="btn btn-outline">
                📎 Ver Documento de Soporte
              </a>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="cerrarModalDetalle" class="btn btn-outline">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { expenseService } from '@/services/expenseService';
import { projectService } from '@/services/projectService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';
import NotificationCenter from '@/components/shared/NotificationCenter.vue';

const router = useRouter();
const notifStore = useNotificationStore();

const loading = ref(false);
const gastos = ref([]);
const proyectos = ref([]);

const filtros = ref({
  proyectoId: '',
  estado: '',
  busqueda: ''
});

const mostrarModalDetalle = ref(false);
const gastoSeleccionado = ref(null);

const stats = computed(() => ({
  totalGastos: gastos.value.length,
  gastosPendientes: gastos.value.filter(g => g.estado === 'pendiente').length,
  gastosAprobados: gastos.value.filter(g => g.estado === 'aprobado').length,
  gastosRechazados: gastos.value.filter(g => g.estado === 'rechazado').length,
  montoTotal: gastos.value.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0),
  montoPendiente: gastos.value.filter(g => g.estado === 'pendiente').reduce((sum, g) => sum + parseFloat(g.monto || 0), 0),
  montoAprobado: gastos.value.filter(g => g.estado === 'aprobado').reduce((sum, g) => sum + parseFloat(g.monto || 0), 0),
  montoRechazado: gastos.value.filter(g => g.estado === 'rechazado').reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
}));

const gastosFiltrados = computed(() => {
  let resultado = [...gastos.value];

  if (filtros.value.proyectoId) {
    resultado = resultado.filter(g => g.proyectoid === parseInt(filtros.value.proyectoId));
  }

  if (filtros.value.estado) {
    resultado = resultado.filter(g => g.estado === filtros.value.estado);
  }

  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase();
    resultado = resultado.filter(g => g.concepto.toLowerCase().includes(busqueda));
  }

  return resultado;
});

onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  try {
    loading.value = true;

    const [gastosData, proyectosData] = await Promise.all([
      expenseService.getAll(),
      projectService.getAll()
    ]);

    gastos.value = gastosData;
    proyectos.value = proyectosData;
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar los gastos'
    });
  } finally {
    loading.value = false;
  }
};

const aplicarFiltros = () => {
  // Los filtros se aplican automáticamente con computed
};

const limpiarFiltros = () => {
  filtros.value = {
    proyectoId: '',
    estado: '',
    busqueda: ''
  };
};

const verDetalleGasto = (gasto) => {
  gastoSeleccionado.value = gasto;
  mostrarModalDetalle.value = true;
};

const cerrarModalDetalle = () => {
  mostrarModalDetalle.value = false;
  gastoSeleccionado.value = null;
};

const exportarGastos = async () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: 'Exportación en progreso',
    mensaje: 'Generando reporte de gastos...'
  });

  router.push('/finance/reports');
};

const getProyectoNombre = (proyectoId) => {
  const proyecto = proyectos.value.find(p => p.id === proyectoId);
  return proyecto ? `${proyecto.codigoproyecto} - ${proyecto.nombre}` : 'N/A';
};

const formatEstado = (estado) => {
  const estados = {
    'pendiente': 'Pendiente',
    'aprobado': 'Aprobado',
    'rechazado': 'Rechazado'
  };
  return estados[estado] || estado;
};

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 0 }).format(value || 0);
};

const formatDate = (date) => {
  if (!date) return '—';
  return new Date(date).toLocaleDateString('es-CO');
};

const formatDateFull = (date) => {
  if (!date) return '—';
  return new Date(date).toLocaleString('es-CO');
};
</script>

<style scoped>
.finance-expenses {
  padding: var(--space-8);
  max-width: 1800px;
  margin: 0 auto;
}

.page-header {
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

.header-actions {
  display: flex;
  gap: var(--space-4);
  align-items: center;
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
  border-left: 5px solid;
  transition: var(--transition-base);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.stat-card.card-info {
  border-left-color: var(--info);
}

.stat-card.card-warning {
  border-left-color: var(--warning);
}

.stat-card.card-success {
  border-left-color: var(--success);
}

.stat-card.card-danger {
  border-left-color: var(--error);
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

.filters-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-6);
}

.filters-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: var(--space-5);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  align-items: end;
}

.filter-group label {
  display: block;
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.form-select,
.form-input {
  width: 100%;
  padding: var(--space-3);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  transition: var(--transition-base);
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: var(--primary);
}

.expenses-section {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
}

.section-header {
  margin-bottom: var(--space-6);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: var(--space-2);
}

.section-subtitle {
  color: var(--gray-600);
}

.expenses-table-container {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px;
}

.expenses-table thead {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.expenses-table th {
  padding: var(--space-4);
  text-align: left;
  font-weight: 800;
  font-size: 0.875rem;
  text-transform: uppercase;
}

.expenses-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
}

.table-row:hover {
  background: var(--gray-50);
}

.cell-id {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--primary);
}

.cell-concepto {
  max-width: 300px;
}

.cell-money {
  font-weight: 700;
  color: var(--success);
  text-align: right;
}

.status-badge {
  display: inline-block;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.status-pendiente {
  background: #fef3c7;
  color: #92400e;
}

.status-aprobado {
  background: #d1fae5;
  color: #065f46;
}

.status-rechazado {
  background: #fee2e2;
  color: #991b1b;
}

.btn-link {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
}

.btn-link:hover {
  text-decoration: underline;
}

.btn-action {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-200);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-base);
}

.btn-action:hover {
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
  margin-bottom: var(--space-2);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-4);
}

.modal-content {
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-6);
  border-bottom: 2px solid var(--gray-200);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 800;
}

.btn-close {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  border: none;
  border-radius: var(--radius-full);
  font-size: 1.5rem;
  cursor: pointer;
  transition: var(--transition-base);
}

.btn-close:hover {
  background: var(--error);
  color: white;
}

.modal-body {
  padding: var(--space-6);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-5);
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-weight: 700;
  color: var(--gray-600);
  font-size: 0.875rem;
  margin-bottom: var(--space-2);
}

.detail-item p {
  color: var(--gray-900);
  font-weight: 600;
}

.monto-destacado {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--success);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: var(--space-6);
  border-top: 2px solid var(--gray-200);
}

@media (max-width: 768px) {
  .finance-expenses {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
