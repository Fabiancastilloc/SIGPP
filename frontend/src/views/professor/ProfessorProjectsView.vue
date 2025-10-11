<template>
  <div class="professor-projects-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">Gestión de Proyectos</h1>
        <p class="page-subtitle">Revisa y valida los proyectos de tus estudiantes</p>
      </div>
      <div class="header-actions">
        <notification-center />
      </div>
    </div>


    <loading-spinner v-if="loading" />


    <div v-else class="projects-content">
      <!-- Estadísticas -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon">📚</div>
          <div class="stat-info">
            <p class="stat-label">Total Proyectos</p>
            <h3 class="stat-value">{{ proyectos.length }}</h3>
          </div>
        </div>


        <div class="stat-card card-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">Pendientes Validación</p>
            <h3 class="stat-value">{{ proyectosPendientes }}</h3>
          </div>
        </div>


        <div class="stat-card card-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Validados</p>
            <h3 class="stat-value">{{ proyectosValidados }}</h3>
          </div>
        </div>


        <div class="stat-card card-info">
          <div class="stat-icon">🚀</div>
          <div class="stat-info">
            <p class="stat-label">Activos</p>
            <h3 class="stat-value">{{ proyectosActivos }}</h3>
          </div>
        </div>
      </div>


      <!-- Filtros -->
      <div class="filters-card">
        <div class="filters-row">
          <div class="filter-group">
            <label>Estado</label>
            <select v-model="filtros.estado" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los estados</option>
              <option value="pendiente_validacion">Pendiente Validación</option>
              <option value="validado">Validado</option>
              <option value="activo">Activo</option>
              <option value="rechazado">Rechazado</option>
            </select>
          </div>


          <div class="filter-group">
            <label>Buscar</label>
            <input v-model="filtros.busqueda" type="text" placeholder="Buscar por nombre..." class="form-input"
              @input="aplicarFiltros" />
          </div>


          <button @click="limpiarFiltros" class="btn btn-secondary">
            Limpiar
          </button>
        </div>
      </div>


      <!-- Lista de Proyectos -->
      <div v-if="proyectosFiltrados.length === 0" class="empty-state">
        <span class="empty-icon">📋</span>
        <h3>No se encontraron proyectos</h3>
        <p v-if="filtros.estado || filtros.busqueda">
          Intenta ajustar los filtros de búsqueda
        </p>
        <p v-else>Aún no tienes proyectos asignados</p>
      </div>


      <div v-else class="projects-grid">
        <div v-for="proyecto in proyectosFiltrados" :key="proyecto.id" class="project-card">
          <div class="project-header">
            <h3 class="project-title">{{ proyecto.nombre }}</h3>
            <project-status-badge :estado="proyecto.estado" />
          </div>


          <p class="project-description">{{ truncate(proyecto.descripcion, 120) }}</p>


          <div class="project-info">
            <div class="info-row">
              <span class="info-label">👤 Estudiante:</span>
              <span class="info-value">{{ proyecto.estudiante?.nombrecompleto || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">💰 Presupuesto:</span>
              <span class="info-value">{{ formatMoney(proyecto.presupuestoasignado || proyecto.presupuestoestimado)
              }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">📅 Creado:</span>
              <span class="info-value">{{ formatDate(proyecto.creadoen) }}</span>
            </div>
          </div>


          <!-- Barra de progreso para proyectos activos -->
          <div v-if="proyecto.estado === 'activo'" class="project-progress">
            <div class="progress-label">
              <span>Ejecución</span>
              <span>{{ calcularPorcentajeEjecucion(proyecto) }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calcularPorcentajeEjecucion(proyecto) + '%' }"
                :class="{ 'progress-warning': calcularPorcentajeEjecucion(proyecto) >= 80 }"></div>
            </div>
          </div>


          <div class="project-actions">
            <button @click="verDetalle(proyecto.id)" class="btn btn-sm btn-outline">
              👁️ Ver Detalle
            </button>
            <button v-if="proyecto.estado === 'pendiente_validacion'" @click="abrirModalValidacion(proyecto)"
              class="btn btn-sm btn-success">
              ✅ Validar
            </button>
            <button v-if="proyecto.estado === 'pendiente_validacion'" @click="abrirModalRechazo(proyecto)"
              class="btn btn-sm btn-danger">
              ❌ Rechazar
            </button>
          </div>
        </div>
      </div>
    </div>


    <!-- Modal de Validación -->
    <modal-dialog v-if="mostrarModalValidacion" @close="cerrarModalValidacion">
      <template #header>
        <h2>Validar Proyecto</h2>
      </template>
      <template #body>
        <div class="modal-content">
          <p>¿Deseas validar el proyecto <strong>{{ proyectoSeleccionado?.nombre }}</strong> y enviarlo al Área
            Financiera?</p>


          <div class="form-group">
            <label class="form-label">Comentarios (opcional)</label>
            <textarea v-model="comentarioValidacion" class="form-textarea" rows="4"
              placeholder="Agrega comentarios o recomendaciones..."></textarea>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalValidacion" class="btn btn-secondary">
          Cancelar
        </button>
        <button @click="confirmarValidacion" class="btn btn-success" :disabled="validando">
          <span v-if="!validando">✅ Validar y Enviar</span>
          <span v-else>Validando...</span>
        </button>
      </template>
    </modal-dialog>


    <!-- Modal de Rechazo -->
    <modal-dialog v-if="mostrarModalRechazo" @close="cerrarModalRechazo">
      <template #header>
        <h2>Devolver Proyecto</h2>
      </template>
      <template #body>
        <div class="modal-content">
          <p>Vas a devolver el proyecto <strong>{{ proyectoSeleccionado?.nombre }}</strong> al estudiante con
            comentarios.</p>


          <div class="form-group">
            <label class="form-label">Comentarios (requeridos)</label>
            <textarea v-model="comentarioRechazo" class="form-textarea" rows="5"
              placeholder="Especifica los ajustes necesarios..." required></textarea>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalRechazo" class="btn btn-secondary">
          Cancelar
        </button>
        <button @click="confirmarRechazo" class="btn btn-danger" :disabled="rechazando || !comentarioRechazo.trim()">
          <span v-if="!rechazando">❌ Devolver con Comentarios</span>
          <span v-else>Procesando...</span>
        </button>
      </template>
    </modal-dialog>
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
import ModalDialog from '@/components/shared/ModalDialog.vue';


const router = useRouter();
const authStore = useAuthStore();
const notifStore = useNotificationStore();


const loading = ref(false);
const validando = ref(false);
const rechazando = ref(false);
const proyectos = ref([]);
const gastos = ref([]);
const filtros = ref({
  estado: '',
  busqueda: ''
});


const mostrarModalValidacion = ref(false);
const mostrarModalRechazo = ref(false);
const proyectoSeleccionado = ref(null);
const comentarioValidacion = ref('');
const comentarioRechazo = ref('');


const proyectosPendientes = computed(() =>
  proyectos.value.filter(p => p.estado === 'pendiente_validacion').length
);


const proyectosValidados = computed(() =>
  proyectos.value.filter(p => p.estado === 'validado').length
);


const proyectosActivos = computed(() =>
  proyectos.value.filter(p => p.estado === 'activo').length
);


const proyectosFiltrados = computed(() => {
  let resultado = proyectos.value;


  if (filtros.value.estado) {
    resultado = resultado.filter(p => p.estado === filtros.value.estado);
  }


  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase();
    resultado = resultado.filter(p =>
      p.nombre.toLowerCase().includes(busqueda) ||
      p.estudiante?.nombrecompleto.toLowerCase().includes(busqueda)
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
    const usuario = authStore.user;


    // Cargar proyectos del profesor
    const [proyectosData, gastosData] = await Promise.all([
      projectService.getAll({ profesorid: usuario.id }),
      expenseService.getAll()
    ]);


    proyectos.value = proyectosData;
    gastos.value = gastosData;


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


const calcularPorcentajeEjecucion = (proyecto) => {
  const presupuesto = parseFloat(proyecto.presupuestoasignado || proyecto.presupuestoestimado || 0);
  if (presupuesto === 0) return 0;


  const gastosProyecto = gastos.value.filter(
    g => g.proyectoid === proyecto.id && g.estado === 'aprobado'
  );
  const ejecutado = gastosProyecto.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0);


  return Math.round((ejecutado / presupuesto) * 100);
};


const aplicarFiltros = () => {
  // Los computed se actualizan automáticamente
};


const limpiarFiltros = () => {
  filtros.value = {
    estado: '',
    busqueda: ''
  };
};


const verDetalle = (id) => {
  router.push(`/profesor/proyectos/${id}`);
};


const abrirModalValidacion = (proyecto) => {
  proyectoSeleccionado.value = proyecto;
  comentarioValidacion.value = '';
  mostrarModalValidacion.value = true;
};


const cerrarModalValidacion = () => {
  mostrarModalValidacion.value = false;
  proyectoSeleccionado.value = null;
  comentarioValidacion.value = '';
};


const confirmarValidacion = async () => {
  try {
    validando.value = true
    await projectService.updateStatus(proyectoSeleccionado.value.id, 'validadoasesor') // ✅ ESTADO CORRECTO
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Validado',
      mensaje: 'El proyecto ha sido validado y enviado al área Financiera'
    })
    cerrarModalValidacion()
    await cargarDatos()
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: error.response?.data?.detail || 'No se pudo validar el proyecto'
    })
  } finally {
    validando.value = false
  }
}


const abrirModalRechazo = (proyecto) => {
  proyectoSeleccionado.value = proyecto;
  comentarioRechazo.value = '';
  mostrarModalRechazo.value = true;
};


const cerrarModalRechazo = () => {
  mostrarModalRechazo.value = false;
  proyectoSeleccionado.value = null;
  comentarioRechazo.value = '';
};


const confirmarRechazo = async () => {
  if (!comentarioRechazo.value.trim()) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Comentario Requerido',
      mensaje: 'Debes especificar los ajustes necesarios'
    });
    return;
  }


  try {
    rechazando.value = true;


    await projectService.updateStatus(proyectoSeleccionado.value.id, 'rechazado');


    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Devuelto',
      mensaje: 'El proyecto ha sido devuelto al estudiante con comentarios'
    });


    cerrarModalRechazo();
    await cargarDatos();


  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: error.response?.data?.detail || 'No se pudo devolver el proyecto'
    });
  } finally {
    rechazando.value = false;
  }
};


const truncate = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};


const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value || 0);
};


const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};
</script>


<style scoped>
.professor-projects-view {
  padding: var(--space-8);
  max-width: 1400px;
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
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
  font-weight: 700;
  text-transform: uppercase;
}


.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--gray-900);
}


.filters-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--space-8);
}


.filters-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
}


.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}


.filter-group label {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--gray-700);
}


.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: var(--space-6);
}


.project-card {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
  transition: var(--transition-base);
}


.project-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
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


.project-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}


.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}


.info-label {
  color: var(--gray-600);
  font-weight: 600;
}


.info-value {
  color: var(--gray-900);
  font-weight: 700;
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


.project-actions {
  display: flex;
  gap: var(--space-2);
  padding-top: var(--space-4);
  border-top: 1px solid var(--gray-200);
}


.modal-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}


.modal-content p {
  line-height: 1.6;
  color: var(--gray-700);
}


.empty-state {
  text-align: center;
  padding: var(--space-16);
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}


.empty-icon {
  font-size: 5rem;
  margin-bottom: var(--space-6);
  opacity: 0.4;
}


.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}


.empty-state p {
  color: var(--gray-600);
  font-size: 1.125rem;
}


@media (max-width: 768px) {
  .professor-projects-view {
    padding: var(--space-4);
  }


  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }


  .projects-grid {
    grid-template-columns: 1fr;
  }


  .filters-row {
    grid-template-columns: 1fr;
  }
}
</style>
