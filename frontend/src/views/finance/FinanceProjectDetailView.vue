<template>
  <div class="finance-project-detail">
    <loading-spinner v-if="loading" />

    <div v-else-if="proyecto" class="detail-container">
      <!-- Header con navegación -->
      <div class="detail-header">
        <button @click="volver" class="btn-back">
          ← Volver
        </button>
        <div class="header-actions">
          <button @click="exportarPDF" class="btn btn-outline">
            📄 Exportar PDF
          </button>
        </div>
      </div>

      <!-- Información Principal -->
      <div class="main-card">
        <div class="card-header">
          <div>
            <h1 class="project-title">{{ proyecto.nombre }}</h1>
            <p class="project-code">{{ proyecto.codigoproyecto }}</p>
          </div>
          <span class="status-badge" :class="`status-${proyecto.estado}`">
            {{ formatEstado(proyecto.estado) }}
          </span>
        </div>

        <div class="card-body">
          <div class="info-grid">
            <div class="info-item">
              <label>Estudiante</label>
              <p>{{ proyecto.estudiantenombre || 'N/A' }}</p>
            </div>

            <div class="info-item">
              <label>Asesor</label>
              <p>{{ proyecto.profesornombre || 'Sin asignar' }}</p>
            </div>

            <div class="info-item">
              <label>Fecha de Creación</label>
              <p>{{ formatDate(proyecto.fechacreacion) }}</p>
            </div>

            <div class="info-item">
              <label>Última Modificación</label>
              <p>{{ formatDate(proyecto.fechaultimamodificacion) }}</p>
            </div>
          </div>

          <div class="description-section">
            <h3>Descripción del Proyecto</h3>
            <p>{{ proyecto.descripcion }}</p>
          </div>

          <div class="description-section">
            <h3>Objetivos</h3>
            <p>{{ proyecto.objetivos }}</p>
          </div>
        </div>
      </div>

      <!-- Presupuesto -->
      <div class="budget-card">
        <h2 class="section-title">💰 Información Presupuestal</h2>

        <div class="budget-stats">
          <div class="budget-stat">
            <label>Presupuesto Estimado</label>
            <p class="amount estimated">{{ formatMoney(proyecto.presupuestoestimado) }}</p>
          </div>

          <div class="budget-stat">
            <label>Presupuesto Asignado</label>
            <p class="amount assigned">
              {{ proyecto.presupuestoasignado ? formatMoney(proyecto.presupuestoasignado) : 'No asignado' }}
            </p>
          </div>

          <div class="budget-stat">
            <label>Presupuesto Ejecutado</label>
            <p class="amount executed">{{ formatMoney(proyecto.presupuestoejecutado) }}</p>
          </div>
        </div>

        <!-- Items de Presupuesto -->
        <div v-if="proyecto.itemspresupuesto && proyecto.itemspresupuesto.length > 0" class="budget-items">
          <h3>Detalle del Presupuesto</h3>
          <table class="items-table">
            <thead>
              <tr>
                <th>Concepto</th>
                <th>Justificación</th>
                <th>Costo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in proyecto.itemspresupuesto" :key="item.id">
                <td class="cell-concepto">{{ item.concepto }}</td>
                <td class="cell-justificacion">{{ item.justificacion }}</td>
                <td class="cell-costo">{{ formatMoney(item.costo) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Acciones de Aprobación -->
      <div v-if="proyecto.estado === 'validado_asesor'" class="actions-card">
        <h2 class="section-title">⚡ Acciones Financieras</h2>

        <div class="action-buttons-grid">
          <button @click="abrirModalAsignacion" class="btn btn-success btn-lg">
            ✅ Asignar Presupuesto y Aprobar
          </button>
          <button @click="rechazarProyecto" class="btn btn-danger btn-lg">
            ❌ Rechazar Proyecto
          </button>
        </div>
      </div>

      <!-- Historial de Aprobaciones -->
      <div v-if="historial.length > 0" class="history-card">
        <h2 class="section-title">📜 Historial de Aprobaciones</h2>

        <div class="timeline">
          <div v-for="entry in historial" :key="entry.id" class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-header">
                <strong>{{ entry.usuarionombre }}</strong>
                <span class="timeline-date">{{ formatDateFull(entry.fecha) }}</span>
              </div>
              <p class="timeline-action">
                {{ entry.estadoanterior }} → <strong>{{ entry.estadonuevo }}</strong>
              </p>
              <p v-if="entry.comentarios" class="timeline-comments">
                {{ entry.comentarios }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Asignación -->
    <div v-if="mostrarModalAsignacion" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">💰 Asignar Presupuesto Final</h2>
          <button @click="cerrarModal" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">
              Presupuesto Final Asignado <span class="required">*</span>
            </label>
            <input v-model.number="presupuestoAsignado" type="number" step="0.01" min="0" placeholder="Ejemplo: 5000000"
              class="form-input" required />
            <p class="form-hint">
              Presupuesto estimado: {{ formatMoney(proyecto?.presupuestoestimado) }}
            </p>
          </div>

          <div class="form-group">
            <label class="form-label">Comentarios (opcional)</label>
            <textarea v-model="comentarios" rows="4" placeholder="Observaciones sobre la asignación presupuestal..."
              class="form-textarea"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="cerrarModal" class="btn btn-outline">
            Cancelar
          </button>
          <button @click="confirmarAsignacion" :disabled="!presupuestoAsignado || presupuestoAsignado <= 0"
            class="btn btn-success">
            ✅ Asignar y Activar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { projectService } from '@/services/projectService';
import { useNotificationStore } from '@/stores/notifications';
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue';

const router = useRouter();
const route = useRoute();
const notifStore = useNotificationStore();

const loading = ref(false);
const proyecto = ref(null);
const historial = ref([]);
const mostrarModalAsignacion = ref(false);
const presupuestoAsignado = ref(null);
const comentarios = ref('');

onMounted(async () => {
  await cargarProyecto();
});

const cargarProyecto = async () => {
  try {
    loading.value = true;
    const proyectoId = route.params.id;

    proyecto.value = await projectService.getById(proyectoId);
    presupuestoAsignado.value = proyecto.value.presupuestoestimado;

    // Cargar historial si existe el endpoint
    try {
      historial.value = await projectService.getHistorial(proyectoId);
    } catch (err) {
      console.log('No se pudo cargar el historial');
    }
  } catch (error) {
    console.error('Error:', error);
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar el proyecto'
    });
    router.push('/finance/projects');
  } finally {
    loading.value = false;
  }
};

const abrirModalAsignacion = () => {
  mostrarModalAsignacion.value = true;
};

const cerrarModal = () => {
  mostrarModalAsignacion.value = false;
  presupuestoAsignado.value = proyecto.value.presupuestoestimado;
  comentarios.value = '';
};

const confirmarAsignacion = async () => {
  if (!presupuestoAsignado.value || presupuestoAsignado.value <= 0) {
    notifStore.addNotification({
      tipo: 'warning',
      titulo: 'Advertencia',
      mensaje: 'Debe ingresar un presupuesto válido'
    });
    return;
  }

  try {
    loading.value = true;

    await projectService.asignarPresupuesto(
      proyecto.value.id,
      presupuestoAsignado.value,
      comentarios.value
    );

    await projectService.updateStatus(proyecto.value.id, 'activo');

    notifStore.addNotification({
      tipo: 'success',
      titulo: 'Proyecto Aprobado',
      mensaje: 'Presupuesto asignado y proyecto activado correctamente'
    });

    cerrarModal();
    await cargarProyecto();
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

const rechazarProyecto = async () => {
  if (!confirm(`¿Estás seguro de rechazar el proyecto "${proyecto.value.nombre}"?`)) {
    return;
  }

  try {
    loading.value = true;
    await projectService.updateStatus(proyecto.value.id, 'rechazado');

    notifStore.addNotification({
      tipo: 'info',
      titulo: 'Proyecto Rechazado',
      mensaje: 'El proyecto ha sido rechazado correctamente'
    });

    router.push('/finance/projects');
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

const volver = () => {
  router.push('/finance/projects');
};

const exportarPDF = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: 'Próximamente',
    mensaje: 'Función de exportación en desarrollo'
  });
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

const formatDateFull = (date) => {
  if (!date) return '—';
  return new Date(date).toLocaleString('es-CO');
};
</script>

<style scoped>
.finance-project-detail {
  padding: var(--space-8);
  max-width: 1400px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-8);
}

.btn-back {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-base);
}

.btn-back:hover {
  background: var(--gray-50);
  border-color: var(--primary);
}

.main-card,
.budget-card,
.actions-card,
.history-card {
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  padding: var(--space-8);
  margin-bottom: var(--space-6);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-6);
  border-bottom: 2px solid var(--gray-200);
}

.project-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.project-code {
  font-family: var(--font-mono);
  color: var(--gray-600);
  font-weight: 700;
}

.status-badge {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}

.info-item label {
  display: block;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--gray-600);
  margin-bottom: var(--space-2);
}

.info-item p {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-900);
}

.description-section {
  margin-bottom: var(--space-6);
}

.description-section h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.description-section p {
  color: var(--gray-700);
  line-height: 1.8;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.budget-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.budget-stat {
  text-align: center;
  padding: var(--space-6);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.budget-stat label {
  display: block;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--gray-600);
  margin-bottom: var(--space-3);
}

.amount {
  font-size: 1.75rem;
  font-weight: 900;
}

.amount.estimated {
  color: var(--info);
}

.amount.assigned {
  color: var(--success);
}

.amount.executed {
  color: var(--warning);
}

.budget-items h3 {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: var(--space-4);
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.items-table thead {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.items-table th {
  padding: var(--space-4);
  text-align: left;
  font-weight: 800;
  font-size: 0.875rem;
}

.items-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
}

.cell-costo {
  font-weight: 700;
  color: var(--success);
  text-align: right;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-4);
}

.timeline {
  position: relative;
  padding-left: var(--space-8);
}

.timeline::before {
  content: '';
  position: absolute;
  left: 12px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--gray-300);
}

.timeline-item {
  position: relative;
  padding-bottom: var(--space-6);
}

.timeline-marker {
  position: absolute;
  left: -26px;
  top: 4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary);
  border: 3px solid white;
  box-shadow: 0 0 0 2px var(--primary);
}

.timeline-content {
  background: var(--gray-50);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.timeline-date {
  color: var(--gray-600);
  font-size: 0.875rem;
}

.timeline-action {
  font-weight: 600;
  margin-bottom: var(--space-2);
}

.timeline-comments {
  color: var(--gray-600);
  font-size: 0.9375rem;
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

.form-group {
  margin-bottom: var(--space-5);
}

.form-label {
  display: block;
  font-weight: 700;
  margin-bottom: var(--space-2);
}

.required {
  color: var(--error);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: var(--space-3);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: 0.9375rem;
  font-family: inherit;
  transition: var(--transition-base);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
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
  .finance-project-detail {
    padding: var(--space-4);
  }

  .detail-header {
    flex-direction: column;
    gap: var(--space-4);
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
