<template>
  <div class="professor-project-detail">
    <div class="detail-header">
      <button @click="volver" class="btn-back">
        ← Volver a Proyectos
      </button>
    </div>

    <loading-spinner v-if="loading" message="Cargando proyecto..." />

    <div v-else-if="proyecto" class="detail-content">
      <!-- Encabezado del Proyecto -->
      <div class="project-header-card">
        <div class="header-main">
          <div class="header-info">
            <h1 class="project-title">{{ proyecto.nombre }}</h1>
            <p class="project-code">Código: {{ proyecto.codigoproyecto || 'N/A' }}</p>
          </div>
          <project-status-badge :estado="proyecto.estado" />
        </div>

        <div class="project-meta">
          <div class="meta-item">
            <span class="meta-icon">👤</span>
            <div class="meta-content">
              <span class="meta-label">Estudiante</span>
              <span class="meta-value">{{ proyecto.estudiante?.nombrecompleto || 'N/A' }}</span>
            </div>
          </div>
          <div class="meta-item">
            <span class="meta-icon">📧</span>
            <div class="meta-content">
              <span class="meta-label">Email</span>
              <span class="meta-value">{{ proyecto.estudiante?.emailinstitucional || 'N/A' }}</span>
            </div>
          </div>
          <div class="meta-item">
            <span class="meta-icon">🏛️</span>
            <div class="meta-content">
              <span class="meta-label">Facultad</span>
              <span class="meta-value">{{ proyecto.estudiante?.facultad?.nombre || 'N/A' }}</span>
            </div>
          </div>
          <div class="meta-item">
            <span class="meta-icon">📅</span>
            <div class="meta-content">
              <span class="meta-label">Fecha de Creación</span>
              <span class="meta-value">{{ formatDate(proyecto.creadoen) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="detail-tabs">
        <button v-for="tab in tabs" :key="tab.id" @click="tabActiva = tab.id" class="tab-button"
          :class="{ active: tabActiva === tab.id }">
          <span class="tab-icon">{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- Contenido de Tabs -->
      <div class="tab-content">
        <!-- TAB: Información -->
        <div v-show="tabActiva === 'info'" class="tab-panel">
          <div class="info-card">
            <h2 class="section-title">Información del Proyecto</h2>

            <div class="info-section">
              <h3 class="subsection-title">Descripción</h3>
              <p class="info-text">{{ proyecto.descripcion }}</p>
            </div>

            <div class="info-section">
              <h3 class="subsection-title">Objetivos</h3>
              <p class="info-text">{{ proyecto.objetivos }}</p>
            </div>

            <div v-if="proyecto.comentarios" class="info-section alert">
              <h3 class="subsection-title">📝 Comentarios</h3>
              <div class="comment-box">
                <p>{{ proyecto.comentarios }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB: Presupuesto -->
        <div v-show="tabActiva === 'presupuesto'" class="tab-panel">
          <div class="budget-overview">
            <div class="budget-card">
              <div class="budget-icon">💰</div>
              <div class="budget-info">
                <span class="budget-label">Presupuesto Estimado</span>
                <span class="budget-amount">{{ formatMoney(proyecto.presupuestoestimado) }}</span>
              </div>
            </div>

            <div class="budget-card" v-if="proyecto.presupuestoasignado">
              <div class="budget-icon">✅</div>
              <div class="budget-info">
                <span class="budget-label">Presupuesto Asignado</span>
                <span class="budget-amount">{{ formatMoney(proyecto.presupuestoasignado) }}</span>
              </div>
            </div>

            <div class="budget-card" v-if="proyecto.estado === 'activo'">
              <div class="budget-icon">📊</div>
              <div class="budget-info">
                <span class="budget-label">Ejecutado</span>
                <span class="budget-amount">{{ formatMoney(proyecto.presupuestoejecutado || 0) }}</span>
              </div>
            </div>

            <div class="budget-card" v-if="proyecto.estado === 'activo'">
              <div class="budget-icon">💵</div>
              <div class="budget-info">
                <span class="budget-label">Disponible</span>
                <span class="budget-amount">{{ formatMoney(saldoDisponible) }}</span>
              </div>
            </div>
          </div>

          <!-- Barra de Ejecución -->
          <div v-if="proyecto.estado === 'activo'" class="execution-section">
            <h3 class="subsection-title">Ejecución Presupuestal</h3>
            <div class="execution-bar-container">
              <div class="execution-info">
                <span>Progreso</span>
                <span class="execution-percentage">{{ porcentajeEjecucion }}%</span>
              </div>
              <div class="execution-bar">
                <div class="execution-fill" :style="{ width: porcentajeEjecucion + '%' }" :class="{
                  'fill-warning': porcentajeEjecucion >= 80 && porcentajeEjecucion < 95,
                  'fill-danger': porcentajeEjecucion >= 95
                }"></div>
              </div>
            </div>

            <div v-if="porcentajeEjecucion >= 80" class="alert-warning">
              ⚠️ El presupuesto está por agotarse ({{ porcentajeEjecucion }}% ejecutado)
            </div>
          </div>

          <!-- Items del Presupuesto -->
          <div v-if="proyecto.itemspresupuesto && proyecto.itemspresupuesto.length > 0" class="items-section">
            <h3 class="subsection-title">Desglose del Presupuesto</h3>
            <div class="items-list">
              <div v-for="(item, index) in proyecto.itemspresupuesto" :key="index" class="item-card">
                <div class="item-header">
                  <span class="item-number">Item {{ index + 1 }}</span>
                  <span class="item-cost">{{ formatMoney(item.costo) }}</span>
                </div>
                <h4 class="item-concept">{{ item.concepto }}</h4>
                <p class="item-justification">{{ item.justificacion }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB: Gastos -->
        <div v-show="tabActiva === 'gastos'" class="tab-panel">
          <div class="expenses-section">
            <div class="section-header">
              <h2 class="section-title">Gastos del Proyecto</h2>
              <div class="expenses-stats">
                <span class="stat-badge pending">{{ gastosPendientes }} Pendientes</span>
                <span class="stat-badge approved">{{ gastosAprobados }} Aprobados</span>
                <span class="stat-badge rejected">{{ gastosRechazados }} Rechazados</span>
              </div>
            </div>

            <loading-spinner v-if="loadingGastos" message="Cargando gastos..." />

            <div v-else-if="gastos.length === 0" class="empty-state">
              <span class="empty-icon">💸</span>
              <h3>No hay gastos registrados</h3>
              <p>El estudiante aún no ha registrado gastos para este proyecto</p>
            </div>

            <div v-else class="expenses-table-wrapper">
              <table class="expenses-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Concepto</th>
                    <th>Monto</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Soporte</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="gasto in gastos" :key="gasto.id">
                    <td class="cell-id">{{ gasto.id }}</td>
                    <td class="cell-concept">{{ gasto.concepto }}</td>
                    <td class="cell-amount">{{ formatMoney(gasto.monto) }}</td>
                    <td class="cell-status">
                      <span class="status-badge" :class="'status-' + gasto.estado">
                        {{ formatEstado(gasto.estado) }}
                      </span>
                    </td>
                    <td class="cell-date">{{ formatDate(gasto.creadoen) }}</td>
                    <td class="cell-soporte">
                      <a v-if="gasto.soporteurl" :href="gasto.soporteurl" target="_blank" class="btn-link">
                        Ver Soporte
                      </a>
                      <span v-else class="text-muted">Sin soporte</span>
                    </td>
                    <td class="cell-actions">
                      <button v-if="gasto.estado === 'pendiente'" @click="aprobarGasto(gasto)" class="btn-icon approve"
                        title="Aprobar gasto">
                        ✓
                      </button>
                      <button v-if="gasto.estado === 'pendiente'" @click="rechazarGasto(gasto)" class="btn-icon reject"
                        title="Rechazar gasto">
                        ✗
                      </button>
                      <button @click="verDetalleGasto(gasto)" class="btn-icon view" title="Ver detalle">
                        👁️
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones del Proyecto -->
      <div v-if="proyecto.estado === 'pendiente_validacion'" class="project-actions-card">
        <h3>Acciones del Proyecto</h3>
        <div class="actions-buttons">
          <button @click="validarProyecto" class="btn btn-lg btn-success">
            ✅ Validar y Enviar a Financiera
          </button>
          <button @click="devolverProyecto" class="btn btn-lg btn-danger">
            ❌ Devolver con Comentarios
          </button>
        </div>
      </div>
    </div>

    <!-- Modal: Detalle del Gasto -->
    <modal-dialog v-if="mostrarModalDetalle" @close="cerrarModalDetalle">
      <template #header>
        <h2>Detalle del Gasto #{{ gastoSeleccionado?.id }}</h2>
      </template>
      <template #body>
        <div v-if="gastoSeleccionado" class="expense-detail">
          <div class="detail-row">
            <span class="detail-label">Concepto:</span>
            <span class="detail-value">{{ gastoSeleccionado.concepto }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Monto:</span>
            <span class="detail-value amount">{{ formatMoney(gastoSeleccionado.monto) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Estado:</span>
            <span class="status-badge" :class="'status-' + gastoSeleccionado.estado">
              {{ formatEstado(gastoSeleccionado.estado) }}
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Fecha de Registro:</span>
            <span class="detail-value">{{ formatDateLong(gastoSeleccionado.creadoen) }}</span>
          </div>
          <div v-if="gastoSeleccionado.soporteurl" class="detail-row">
            <span class="detail-label">Soporte:</span>
            <a :href="gastoSeleccionado.soporteurl" target="_blank" class="btn-link">
              Ver Documento
            </a>
          </div>
          <div v-if="gastoSeleccionado.comentarios" class="detail-row full">
            <span class="detail-label">Comentarios:</span>
            <div class="comment-box">
              <p>{{ gastoSeleccionado.comentarios }}</p>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalDetalle" class="btn btn-primary">Cerrar</button>
      </template>
    </modal-dialog>

    <!-- Modal: Validar Proyecto -->
    <modal-dialog v-if="mostrarModalValidacion" @close="cerrarModalValidacion">
      <template #header>
        <h2>Validar Proyecto</h2>
      </template>
      <template #body>
        <div class="modal-content">
          <p>¿Deseas validar el proyecto <strong>{{ proyecto?.nombre }}</strong> y enviarlo al Área Financiera?</p>
          <div class="form-group">
            <label class="form-label">Comentarios (opcional)</label>
            <textarea v-model="comentarioValidacion" class="form-textarea" rows="4"
              placeholder="Agrega comentarios o recomendaciones..."></textarea>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalValidacion" class="btn btn-secondary">Cancelar</button>
        <button @click="confirmarValidacion" class="btn btn-success" :disabled="validando">
          {{ validando ? 'Validando...' : '✅ Validar y Enviar' }}
        </button>
      </template>
    </modal-dialog>

    <!-- Modal: Devolver Proyecto -->
    <modal-dialog v-if="mostrarModalDevolucion" @close="cerrarModalDevolucion">
      <template #header>
        <h2>Devolver Proyecto</h2>
      </template>
      <template #body>
        <div class="modal-content">
          <p>Vas a devolver el proyecto <strong>{{ proyecto?.nombre }}</strong> al estudiante.</p>
          <div class="form-group">
            <label class="form-label">Comentarios (requeridos)</label>
            <textarea v-model="comentarioDevolucion" class="form-textarea" rows="5"
              placeholder="Especifica los ajustes necesarios..." required></textarea>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalDevolucion" class="btn btn-secondary">Cancelar</button>
        <button @click="confirmarDevolucion" class="btn btn-danger"
          :disabled="devolviendo || !comentarioDevolucion.trim()">
          {{ devolviendo ? 'Procesando...' : '❌ Devolver con Comentarios' }}
        </button>
      </template>
    </modal-dialog>

    <!-- Modal: Rechazar Gasto -->
    <modal-dialog v-if="mostrarModalRechazoGasto" @close="cerrarModalRechazoGasto">
      <template #header>
        <h2>Rechazar Gasto</h2>
      </template>
      <template #body>
        <div class="modal-content">
          <p>¿Estás seguro de rechazar el gasto "<strong>{{ gastoSeleccionado?.concepto }}</strong>"?</p>
          <div class="form-group">
            <label class="form-label">Motivo del rechazo (opcional)</label>
            <textarea v-model="comentarioRechazoGasto" class="form-textarea" rows="4"
              placeholder="Explica por qué se rechaza este gasto..."></textarea>
          </div>
        </div>
      </template>
      <template #footer>
        <button @click="cerrarModalRechazoGasto" class="btn btn-secondary">Cancelar</button>
        <button @click="confirmarRechazoGasto" class="btn btn-danger" :disabled="rechazandoGasto">
          {{ rechazandoGasto ? 'Rechazando...' : 'Rechazar Gasto' }}
        </button>
      </template>
    </modal-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { projectService } from '@/services/projectService';
import { expenseService } from '@/services/expenseService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue';
import ModalDialog from '@/components/shared/ModalDialog.vue';

const router = useRouter();
const route = useRoute();
const notifStore = useNotificationStore();

const loading = ref(false);
const loadingGastos = ref(false);
const validando = ref(false);
const devolviendo = ref(false);
const rechazandoGasto = ref(false);

const proyecto = ref(null);
const gastos = ref([]);
const tabActiva = ref('info');

const mostrarModalDetalle = ref(false);
const mostrarModalValidacion = ref(false);
const mostrarModalDevolucion = ref(false);
const mostrarModalRechazoGasto = ref(false);

const gastoSeleccionado = ref(null);
const comentarioValidacion = ref('');
const comentarioDevolucion = ref('');
const comentarioRechazoGasto = ref('');

const tabs = [
  { id: 'info', label: 'Información', icon: '📋' },
  { id: 'presupuesto', label: 'Presupuesto', icon: '💰' },
  { id: 'gastos', label: 'Gastos', icon: '💸' }
];

const saldoDisponible = computed(() => {
  if (!proyecto.value) return 0;
  const presupuesto = parseFloat(proyecto.value.presupuestoasignado || proyecto.value.presupuestoestimado || 0);
  const ejecutado = parseFloat(proyecto.value.presupuestoejecutado || 0);
  return presupuesto - ejecutado;
});

const porcentajeEjecucion = computed(() => {
  if (!proyecto.value) return 0;
  const presupuesto = parseFloat(proyecto.value.presupuestoasignado || proyecto.value.presupuestoestimado || 0);
  if (presupuesto === 0) return 0;
  const ejecutado = parseFloat(proyecto.value.presupuestoejecutado || 0);
  return Math.min(Math.round((ejecutado / presupuesto) * 100), 100);
});

const gastosPendientes = computed(() => gastos.value.filter(g => g.estado === 'pendiente').length);
const gastosAprobados = computed(() => gastos.value.filter(g => g.estado === 'aprobado').length);
const gastosRechazados = computed(() => gastos.value.filter(g => g.estado === 'rechazado').length);

onMounted(async () => {
  await cargarDatos();
});

const cargarDatos = async () => {
  try {
    loading.value = true;
    const id = route.params.id;
    proyecto.value = await projectService.getById(id);
    await cargarGastos(id);
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar el proyecto'
    });
    router.push('/profesor/proyectos');
  } finally {
    loading.value = false;
  }
};

const cargarGastos = async (proyectoId) => {
  try {
    loadingGastos.value = true;
    const todosGastos = await expenseService.getAll();
    gastos.value = todosGastos.filter(g => g.proyectoid === parseInt(proyectoId));
  } catch (error) {
    console.error('Error:', error);
  } finally {
    loadingGastos.value = false;
  }
};

const volver = () => {
  router.push('/profesor/proyectos');
};

const validarProyecto = () => {
  comentarioValidacion.value = '';
  mostrarModalValidacion.value = true;
};

const cerrarModalValidacion = () => {
  mostrarModalValidacion.value = false;
  comentarioValidacion.value = '';
};

const confirmarValidacion = async () => {
  try {
    validando.value = true;
    await projectService.updateStatus(proyecto.value.id, 'validadoasesor')
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Validado',
      mensaje: 'El proyecto ha sido validado y enviado al Área Financiera'
    });
    cerrarModalValidacion();
    await cargarDatos();
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo validar el proyecto'
    });
  } finally {
    validando.value = false;
  }
};

const devolverProyecto = () => {
  comentarioDevolucion.value = '';
  mostrarModalDevolucion.value = true;
};

const cerrarModalDevolucion = () => {
  mostrarModalDevolucion.value = false;
  comentarioDevolucion.value = '';
};

const confirmarDevolucion = async () => {
  if (!comentarioDevolucion.value.trim()) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Comentario Requerido',
      mensaje: 'Debes especificar los ajustes necesarios'
    });
    return;
  }

  try {
    devolviendo.value = true;
    await projectService.updateStatus(proyecto.value.id, 'rechazado');
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Devuelto',
      mensaje: 'El proyecto ha sido devuelto al estudiante con comentarios'
    });
    cerrarModalDevolucion();
    await cargarDatos();
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo devolver el proyecto'
    });
  } finally {
    devolviendo.value = false;
  }
};

const aprobarGasto = async (gasto) => {
  if (!confirm('¿Aprobar este gasto?')) return;

  try {
    await expenseService.approve(gasto.id);
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Gasto Aprobado',
      mensaje: 'El gasto ha sido aprobado exitosamente'
    });
    await cargarGastos(proyecto.value.id);
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo aprobar el gasto'
    });
  }
};

const rechazarGasto = (gasto) => {
  gastoSeleccionado.value = gasto;
  comentarioRechazoGasto.value = '';
  mostrarModalRechazoGasto.value = true;
};

const cerrarModalRechazoGasto = () => {
  mostrarModalRechazoGasto.value = false;
  gastoSeleccionado.value = null;
  comentarioRechazoGasto.value = '';
};

const confirmarRechazoGasto = async () => {
  try {
    rechazandoGasto.value = true;
    await expenseService.reject(gastoSeleccionado.value.id, comentarioRechazoGasto.value);
    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Gasto Rechazado',
      mensaje: 'El gasto ha sido rechazado'
    });
    cerrarModalRechazoGasto();
    await cargarGastos(proyecto.value.id);
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo rechazar el gasto'
    });
  } finally {
    rechazandoGasto.value = false;
  }
};

const verDetalleGasto = (gasto) => {
  gastoSeleccionado.value = gasto;
  mostrarModalDetalle.value = true;
};

const cerrarModalDetalle = () => {
  mostrarModalDetalle.value = false;
  gastoSeleccionado.value = null;
};

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value || 0);
};

const formatDate = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatDateLong = (date) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatEstado = (estado) => {
  const estados = {
    pendiente: 'Pendiente',
    aprobado: 'Aprobado',
    rechazado: 'Rechazado'
  };
  return estados[estado] || estado;
};
</script>

<style scoped>
.professor-project-detail {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: var(--space-8);
}

.detail-header {
  max-width: 1400px;
  margin: 0 auto var(--space-6);
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-weight: 700;
  color: var(--gray-700);
  cursor: pointer;
  transition: var(--transition-base);
}

.btn-back:hover {
  background: var(--gray-50);
  border-color: var(--primary);
  color: var(--primary);
}

.detail-content {
  max-width: 1400px;
  margin: 0 auto;
}

.project-header-card {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  margin-bottom: var(--space-8);
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
}

.project-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.project-code {
  font-size: 0.875rem;
  color: var(--gray-500);
  font-family: var(--font-mono);
}

.project-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.meta-icon {
  font-size: 1.5rem;
}

.meta-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.meta-label {
  font-size: 0.75rem;
  color: var(--gray-600);
  font-weight: 600;
  text-transform: uppercase;
}

.meta-value {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--gray-900);
}

.detail-tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  background: white;
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-6);
  background: transparent;
  border: 2px solid transparent;
  border-radius: var(--radius-lg);
  font-weight: 700;
  color: var(--gray-600);
  cursor: pointer;
  transition: var(--transition-base);
}

.tab-button:hover {
  background: var(--gray-50);
  color: var(--gray-900);
}

.tab-button.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.tab-icon {
  font-size: 1.25rem;
}

.tab-content {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  min-height: 400px;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.subsection-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.info-section {
  margin-bottom: var(--space-6);
}

.info-text {
  color: var(--gray-700);
  line-height: 1.7;
  font-size: 1rem;
}

.comment-box {
  padding: var(--space-5);
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  border-radius: var(--radius-lg);
  color: var(--gray-800);
}

.budget-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.budget-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6);
  background: linear-gradient(135deg, var(--gray-50), white);
  border-radius: var(--radius-xl);
  border: 2px solid var(--gray-200);
  transition: var(--transition-base);
}

.budget-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.budget-icon {
  font-size: 2.5rem;
}

.budget-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.budget-label {
  font-size: 0.75rem;
  color: var(--gray-600);
  font-weight: 700;
  text-transform: uppercase;
}

.budget-amount {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--primary);
}

.execution-section {
  margin-bottom: var(--space-8);
  padding: var(--space-6);
  background: var(--gray-50);
  border-radius: var(--radius-xl);
}

.execution-bar-container {
  margin-top: var(--space-4);
}

.execution-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
  font-weight: 700;
  color: var(--gray-700);
}

.execution-percentage {
  color: var(--primary);
  font-size: 1.125rem;
}

.execution-bar {
  height: 24px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.execution-fill {
  height: 100%;
  background: var(--success);
  transition: width 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: var(--space-3);
  color: white;
  font-weight: 700;
}

.execution-fill.fill-warning {
  background: var(--warning);
}

.execution-fill.fill-danger {
  background: var(--error);
}

.alert-warning {
  margin-top: var(--space-4);
  padding: var(--space-4);
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: var(--radius-lg);
  color: #856404;
  font-weight: 600;
}

.items-list {
  display: grid;
  gap: var(--space-5);
}

.item-card {
  padding: var(--space-6);
  background: var(--gray-50);
  border-radius: var(--radius-xl);
  border: 2px solid var(--gray-200);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.item-number {
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--primary);
  background: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
}

.item-cost {
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--success);
}

.item-concept {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.item-justification {
  color: var(--gray-600);
  line-height: 1.6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-4);
}

.expenses-stats {
  display: flex;
  gap: var(--space-3);
}

.stat-badge {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 700;
}

.stat-badge.pending {
  background: var(--warning-light);
  color: #856404;
}

.stat-badge.approved {
  background: var(--success-light);
  color: #065f46;
}

.stat-badge.rejected {
  background: var(--error-light);
  color: #991b1b;
}

.expenses-table-wrapper {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
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
  font-size: 0.9375rem;
}

.expenses-table tbody tr:hover {
  background: var(--gray-50);
}

.cell-id {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--primary);
}

.cell-concept {
  font-weight: 600;
}

.cell-amount {
  font-weight: 900;
  color: var(--success);
  font-size: 1.125rem;
}

.status-badge {
  display: inline-flex;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 800;
}

.status-pendiente {
  background: var(--warning-light);
  color: #856404;
}

.status-aprobado {
  background: var(--success-light);
  color: #065f46;
}

.status-rechazado {
  background: var(--error-light);
  color: #991b1b;
}

.btn-link {
  color: var(--primary);
  font-weight: 700;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}

.text-muted {
  color: var(--gray-500);
  font-size: 0.875rem;
}

.cell-actions {
  display: flex;
  gap: var(--space-2);
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
  font-size: 1rem;
}

.btn-icon.approve:hover {
  background: var(--success);
  color: white;
  transform: scale(1.1);
}

.btn-icon.reject:hover {
  background: var(--error);
  color: white;
  transform: scale(1.1);
}

.btn-icon.view:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.empty-state {
  text-align: center;
  padding: var(--space-16);
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

.project-actions-card {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  margin-top: var(--space-8);
}

.project-actions-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.actions-buttons {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
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

.expense-detail {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.detail-row.full {
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-3);
}

.detail-label {
  font-weight: 700;
  color: var(--gray-700);
}

.detail-value {
  font-weight: 600;
  color: var(--gray-900);
}

.detail-value.amount {
  font-size: 1.5rem;
  color: var(--success);
  font-weight: 900;
}

@media (max-width: 768px) {
  .professor-project-detail {
    padding: var(--space-4);
  }

  .project-meta {
    grid-template-columns: 1fr;
  }

  .budget-overview {
    grid-template-columns: 1fr;
  }

  .detail-tabs {
    flex-direction: column;
  }

  .actions-buttons {
    flex-direction: column;
  }

  .expenses-table-wrapper {
    overflow-x: scroll;
  }
}
</style>
