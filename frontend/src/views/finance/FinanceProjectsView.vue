<template>
  <div class="finance-projects">
    <div class="page-header">
      <div>
        <h1 class="page-title">📋 Gestión de Proyectos</h1>
        <p class="page-subtitle">Aprobar y supervisar proyectos académicos</p>
      </div>
      <div class="header-actions">
        <button @click="generarReporte" class="btn btn-outline">
          📊 Generar Reporte
        </button>
        <notification-center />
      </div>
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="projects-content">
      <!-- Filtros Avanzados -->
      <div class="filters-card">
        <h3 class="filters-title">🔍 Filtros de Búsqueda</h3>
        <div class="filters-grid">
          <div class="filter-group">
            <label>Estado</label>
            <select v-model="filtros.estado" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los estados</option>
              <option value="validado_asesor">Pendiente Aprobación</option>
              <option value="activo">Activos</option>
              <option value="rechazado">Rechazados</option>
              <option value="finalizado">Finalizados</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Facultad</label>
            <select v-model="filtros.facultadId" @change="aplicarFiltros" class="form-select">
              <option value="">Todas las facultades</option>
              <option v-for="fac in facultades" :key="fac.id" :value="fac.id">
                {{ fac.nombre }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Sede</label>
            <select v-model="filtros.sedeId" @change="aplicarFiltros" class="form-select">
              <option value="">Todas las sedes</option>
              <option v-for="sede in sedes" :key="sede.id" :value="sede.id">
                {{ sede.nombre }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Carrera</label>
            <select v-model="filtros.carreraId" @change="aplicarFiltros" class="form-select">
              <option value="">Todas las carreras</option>
              <option v-for="carr in carreras" :key="carr.id" :value="carr.id">
                {{ carr.nombre }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Búsqueda</label>
            <input v-model="filtros.busqueda" @input="aplicarFiltros" type="text"
              placeholder="Buscar por nombre o código..." class="form-input" />
          </div>

          <div class="filter-actions">
            <button @click="limpiarFiltros" class="btn btn-sm btn-outline">
              🔄 Limpiar Filtros
            </button>
          </div>
        </div>
      </div>

      <!-- Estadísticas Rápidas -->
      <div class="quick-stats">
        <div class="stat-mini primary">
          <span class="stat-mini-icon">⏳</span>
          <div>
            <p class="stat-mini-value">{{ stats.pendientes }}</p>
            <p class="stat-mini-label">Pendientes</p>
          </div>
        </div>
        <div class="stat-mini success">
          <span class="stat-mini-icon">✅</span>
          <div>
            <p class="stat-mini-value">{{ stats.activos }}</p>
            <p class="stat-mini-label">Activos</p>
          </div>
        </div>
        <div class="stat-mini danger">
          <span class="stat-mini-icon">❌</span>
          <div>
            <p class="stat-mini-value">{{ stats.rechazados }}</p>
            <p class="stat-mini-label">Rechazados</p>
          </div>
        </div>
        <div class="stat-mini info">
          <span class="stat-mini-icon">🏁</span>
          <div>
            <p class="stat-mini-value">{{ stats.finalizados }}</p>
            <p class="stat-mini-label">Finalizados</p>
          </div>
        </div>
      </div>

      <!-- Lista de Proyectos -->
      <div class="projects-section">
        <div class="section-header">
          <h2 class="section-title">
            {{ filtros.estado === 'validado_asesor' ? '📝 Proyectos Pendientes de Aprobación' : '📊 Listado deProyectos'
            }}
          </h2>
          <p class="section-subtitle">
            Mostrando {{ proyectosFiltrados.length }} de {{ proyectos.length }} proyectos
          </p>
        </div>

        <div v-if="proyectosFiltrados.length === 0" class="empty-state">
          <span class="empty-icon">📭</span>
          <h3>{{ obtenerMensajeVacio() }}</h3>
          <p>Intenta ajustar los filtros de búsqueda</p>
        </div>

        <div v-else class="projects-table-container">
          <table class="projects-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Proyecto</th>
                <th>Estudiante</th>
                <th>Asesor</th>
                <th>Estado</th>
                <th>Presupuesto Estimado</th>
                <th>Presupuesto Asignado</th>
                <th>Fecha Creación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="proyecto in proyectosFiltrados" :key="proyecto.id" class="table-row">
                <td class="cell-code">{{ proyecto.codigoproyecto }}</td>
                <td class="cell-name">
                  <router-link :to="`/finance/projects/${proyecto.id}`" class="project-link">
                    {{ proyecto.nombre }}
                  </router-link>
                </td>
                <td>{{ proyecto.estudiantenombre || 'N/A' }}</td>
                <td>{{ proyecto.profesornombre || 'Sin asignar' }}</td>
                <td>
                  <span class="status-badge" :class="`status-${proyecto.estado}`">
                    {{ formatEstado(proyecto.estado) }}
                  </span>
                </td>
                <td class="cell-money">{{ formatMoney(proyecto.presupuestoestimado) }}</td>
                <td class="cell-money">
                  {{ proyecto.presupuestoasignado ? formatMoney(proyecto.presupuestoasignado) : '—' }}
                </td>
                <td class="cell-date">{{ formatDate(proyecto.fechacreacion) }}</td>
                <td class="cell-actions">
                  <div class="action-buttons">
                    <router-link :to="`/finance/projects/${proyecto.id}`" class="btn-action btn-view"
                      title="Ver detalles">
                      👁️
                    </router-link>
                    <button v-if="proyecto.estado === 'validado_asesor'" @click="abrirModalAsignacion(proyecto)"
                      class="btn-action btn-approve" title="Asignar presupuesto y aprobar">
                      ✅
                    </button>
                    <button v-if="proyecto.estado === 'validado_asesor'" @click="rechazarProyecto(proyecto)"
                      class="btn-action btn-reject" title="Rechazar proyecto">
                      ❌
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Asignación de Presupuesto -->
    <div v-if="mostrarModalAsignacion" class="modal-overlay" @click.self="cerrarModalAsignacion">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h2 class="modal-title">💰 Asignar Presupuesto Final</h2>
          <button @click="cerrarModalAsignacion" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <div class="proyecto-info-card">
            <h3>{{ proyectoSeleccionado?.nombre }}</h3>
            <p><strong>Código:</strong> {{ proyectoSeleccionado?.codigoproyecto }}</p>
            <p><strong>Estudiante:</strong> {{ proyectoSeleccionado?.estudiantenombre }}</p>
            <p><strong>Presupuesto Estimado:</strong> {{ formatMoney(proyectoSeleccionado?.presupuestoestimado) }}</p>
          </div>

          <div class="form-group">
            <label class="form-label">
              Presupuesto Final Asignado <span class="required">*</span>
            </label>
            <input v-model.number="presupuestoAsignado" type="number" step="0.01" min="0" placeholder="Ejemplo: 5000000"
              class="form-input" required />
            <p class="form-hint">
              Ingresa el monto en pesos colombianos (COP) sin puntos ni comas
            </p>
          </div>

          <div class="form-group">
            <label class="form-label">Comentarios (opcional)</label>
            <textarea v-model="comentarios" rows="4" placeholder="Observaciones sobre la asignación presupuestal..."
              class="form-textarea"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="cerrarModalAsignacion" class="btn btn-outline">
            Cancelar
          </button>
          <button @click="confirmarAsignacion" :disabled="!presupuestoAsignado || presupuestoAsignado <= 0"
            class="btn btn-success">
            ✅ Asignar y Activar Proyecto
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { projectService } from '@/services/projectService';
import { catalogService } from '@/services/catalogService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';
import NotificationCenter from '@/components/shared/NotificationCenter.vue';

const router = useRouter();
const notifStore = useNotificationStore();

const loading = ref(false);
const proyectos = ref([]);
const facultades = ref([]);
const sedes = ref([]);
const carreras = ref([]);

const filtros = ref({
  estado: 'validado_asesor', // Por defecto mostrar pendientes
  facultadId: '',
  sedeId: '',
  carreraId: '',
  busqueda: ''
});

const mostrarModalAsignacion = ref(false);
const proyectoSeleccionado = ref(null);
const presupuestoAsignado = ref(null);
const comentarios = ref('');

const stats = computed(() => ({
  pendientes: proyectos.value.filter(p => p.estado === 'validado_asesor').length,
  activos: proyectos.value.filter(p => p.estado === 'activo').length,
  rechazados: proyectos.value.filter(p => p.estado === 'rechazado').length,
  finalizados: proyectos.value.filter(p => p.estado === 'finalizado').length
}));

const proyectosFiltrados = computed(() => {
  let resultado = [...proyectos.value];

  if (filtros.value.estado) {
    resultado = resultado.filter(p => p.estado === filtros.value.estado);
  }

  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase();
    resultado = resultado.filter(p =>
      p.nombre.toLowerCase().includes(busqueda) ||
      p.codigoproyecto.toLowerCase().includes(busqueda)
    );
  }

  return resultado;
});

onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  try {
    loading.value = true;

    const [proyectosData, facultadesData, sedesData, carrerasData] = await Promise.all([
      projectService.getAll(),
      catalogService.getFacultades(),
      catalogService.getSedes(),
      catalogService.getCarreras()
    ]);

    proyectos.value = proyectosData;
    facultades.value = facultadesData;
    sedes.value = sedesData;
    carreras.value = carrerasData;
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar los proyectos'
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
    estado: '',
    facultadId: '',
    sedeId: '',
    carreraId: '',
    busqueda: ''
  };
};

const abrirModalAsignacion = (proyecto) => {
  proyectoSeleccionado.value = proyecto;
  presupuestoAsignado.value = proyecto.presupuestoestimado || null;
  comentarios.value = '';
  mostrarModalAsignacion.value = true;
};

const cerrarModalAsignacion = () => {
  mostrarModalAsignacion.value = false;
  proyectoSeleccionado.value = null;
  presupuestoAsignado.value = null;
  comentarios.value = '';
};

const confirmarAsignacion = async () => {
  if (!presupuestoAsignado.value || presupuestoAsignado.value <= 0) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Advertencia',
      mensaje: 'Debe ingresar un presupuesto válido mayor a cero'
    });
    return;
  }

  try {
    loading.value = true;

    // 1. Asignar presupuesto
    await projectService.asignarPresupuesto(
      proyectoSeleccionado.value.id,
      presupuestoAsignado.value,
      comentarios.value
    );

    // 2. Cambiar estado a "activo"
    await projectService.updateStatus(proyectoSeleccionado.value.id, 'activo');

    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Aprobado',
      mensaje: `Presupuesto asignado y proyecto activado correctamente`
    });

    cerrarModalAsignacion();
    await cargarDatos();
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: error.response?.data?.detail || 'No se pudo aprobar el proyecto'
    });
  } finally {
    loading.value = false;
  }
};

const rechazarProyecto = async (proyecto) => {
  if (!confirm(`¿Estás seguro de rechazar el proyecto "${proyecto.nombre}"? Esta acción no se puede deshacer.`)) {
    return;
  }

  try {
    loading.value = true;
    await projectService.updateStatus(proyecto.id, 'rechazado');

    notifStore.addNotification({
      tipo: 'info',
      titulo: 'Proyecto Rechazado',
      mensaje: 'El proyecto ha sido rechazado correctamente'
    });

    await cargarDatos();
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo rechazar el proyecto'
    });
  } finally {
    loading.value = false;
  }
};

const generarReporte = () => {
  router.push('/finance/reports');
};

const obtenerMensajeVacio = () => {
  if (filtros.value.estado) {
    return `No hay proyectos en estado "${formatEstado(filtros.value.estado)}"`;
  }
  return 'No hay proyectos disponibles';
};

const formatEstado = (estado) => {
  const estados = {
    'borrador': 'Borrador',
    'pendiente_validacion': 'Pendiente Validación',
    'validado_asesor': 'Pendiente Aprobación',
    'activo': 'Activo',
    'rechazado': 'Rechazado',
    'finalizado': 'Finalizado'
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
</script>

<style scoped>
.finance-projects {
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

.filters-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-6);
  border: 2px solid var(--gray-200);
}

.filters-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
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
  color: var(--gray-700);
  margin-bottom: var(--space-2);
  font-size: 0.9375rem;
}

.form-select,
.form-input {
  width: 100%;
  padding: var(--space-3);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: 0.9375rem;
  transition: var(--transition-base);
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-actions {
  display: flex;
  align-items: flex-end;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.stat-mini {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-5);
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border-left: 4px solid;
  transition: var(--transition-base);
}

.stat-mini:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-mini.primary {
  border-left-color: var(--warning);
}

.stat-mini.success {
  border-left-color: var(--success);
}

.stat-mini.danger {
  border-left-color: var(--error);
}

.stat-mini.info {
  border-left-color: var(--info);
}

.stat-mini-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  border-radius: var(--radius-lg);
}

.stat-mini-value {
  font-size: 1.75rem;
  font-weight: 900;
  color: var(--gray-900);
  line-height: 1;
}

.stat-mini-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 600;
}

.projects-section {
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
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.section-subtitle {
  color: var(--gray-600);
  font-size: 0.9375rem;
}

.projects-table-container {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.projects-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px;
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
  white-space: nowrap;
}

.projects-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  font-size: 0.9375rem;
}

.table-row:hover {
  background: var(--gray-50);
}

.cell-code {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--primary);
}

.cell-name {
  max-width: 300px;
}

.project-link {
  color: var(--gray-900);
  font-weight: 600;
  text-decoration: none;
  transition: var(--transition-base);
}

.project-link:hover {
  color: var(--primary);
  text-decoration: underline;
}

.status-badge {
  display: inline-block;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-validado_asesor {
  background: #fef3c7;
  color: #92400e;
}

.status-activo {
  background: #d1fae5;
  color: #065f46;
}

.status-rechazado {
  background: #fee2e2;
  color: #991b1b;
}

.status-finalizado {
  background: #dbeafe;
  color: #1e40af;
}

.cell-money {
  font-weight: 700;
  color: var(--success);
  text-align: right;
}

.cell-date {
  color: var(--gray-600);
  font-size: 0.875rem;
}

.cell-actions {
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: var(--space-2);
  justify-content: center;
}

.btn-action {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 1.125rem;
  transition: var(--transition-base);
  text-decoration: none;
}

.btn-view {
  background: var(--gray-200);
}

.btn-view:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.btn-approve {
  background: #d1fae5;
}

.btn-approve:hover {
  background: var(--success);
  transform: scale(1.1);
}

.btn-reject {
  background: #fee2e2;
}

.btn-reject:hover {
  background: var(--error);
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
}

/* Modal Styles */
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
  max-width: 600px;
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
  color: var(--gray-900);
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

.proyecto-info-card {
  background: var(--gray-50);
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-6);
  border: 2px solid var(--gray-200);
}

.proyecto-info-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.proyecto-info-card p {
  margin-bottom: var(--space-2);
  color: var(--gray-700);
}

.form-group {
  margin-bottom: var(--space-5);
}

.form-label {
  display: block;
  font-weight: 700;
  color: var(--gray-700);
  margin-bottom: var(--space-2);
  font-size: 0.9375rem;
}

.required {
  color: var(--error);
}

.form-textarea {
  width: 100%;
  padding: var(--space-3);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: 0.9375rem;
  font-family: inherit;
  resize: vertical;
  transition: var(--transition-base);
}

.form-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-hint {
  margin-top: var(--space-2);
  font-size: 0.875rem;
  color: var(--gray-600);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-6);
  border-top: 2px solid var(--gray-200);
}

@media (max-width: 768px) {
  .finance-projects {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .projects-table-container {
    overflow-x: scroll;
  }
}
</style>
