<template>
  <div class="project-detail-view">
    <loading-spinner v-if="loading" overlay message="Cargando proyecto..." />

    <div v-else-if="proyecto" class="detail-wrapper">
      <!-- Header con Navegación y Acciones -->
      <div class="detail-header">
        <button @click="volver" class="btn-back">
          ← Volver a Proyectos
        </button>

        <div class="header-main">
          <div class="header-info">
            <h1 class="project-title">{{ proyecto.nombre }}</h1>
            <div class="title-meta">
              <span class="project-code">🔖 {{ proyecto.codigo_proyecto }}</span>
              <project-status-badge :estado="proyecto.estado" />
            </div>
          </div>

          <div class="header-actions">
            <button v-if="puedeEditar" @click="editar" class="btn btn-secondary" title="Editar proyecto">
              ✏️ Editar
            </button>

            <button v-if="puedeEnviar" @click="enviarValidacion" class="btn btn-success" title="Enviar para validación">
              📤 Enviar para Validación
            </button>

            <button @click="exportarPDF" class="btn btn-primary" title="Exportar a PDF">
              📄 Exportar PDF
            </button>

            <button @click="compartir" class="btn btn-secondary" title="Compartir proyecto">
              🔗 Compartir
            </button>

            <button @click="imprimir" class="btn btn-secondary" title="Imprimir">
              🖨️ Imprimir
            </button>

            <button v-if="puedeEliminar" @click="eliminar" class="btn btn-danger" title="Eliminar proyecto">
              🗑️ Eliminar
            </button>

            <notification-center />
          </div>
        </div>
      </div>

      <!-- Contenido Principal en Pestañas -->
      <div class="detail-tabs">
        <button v-for="tab in tabs" :key="tab.id" @click="tabActiva = tab.id" class="tab-button"
          :class="{ active: tabActiva === tab.id }">
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
        </button>
      </div>

      <!-- Contenido de las Pestañas -->
      <div class="detail-content">

        <!-- TAB: Información General -->
        <div v-show="tabActiva === 'info'" class="tab-content">
          <div class="info-section">
            <div class="section-card">
              <h2 class="section-title">📋 Información del Proyecto</h2>

              <div class="info-grid">
                <div class="info-item full-width">
                  <label class="info-label">Descripción</label>
                  <div class="info-value-box">
                    <p>{{ proyecto.descripcion }}</p>
                  </div>
                </div>

                <div class="info-item full-width">
                  <label class="info-label">Objetivos</label>
                  <div class="info-value-box">
                    <p>{{ proyecto.objetivos }}</p>
                  </div>
                </div>

                <div class="info-item">
                  <label class="info-label">Profesor Asesor</label>
                  <div class="info-badge">
                    <span class="badge-icon">👨‍🏫</span>
                    <span>{{ proyecto.profesor_nombre || 'Sin asignar' }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <label class="info-label">Fecha de Creación</label>
                  <div class="info-badge">
                    <span class="badge-icon">📅</span>
                    <span>{{ formatDateLong(proyecto.fecha_creacion) }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <label class="info-label">Última Modificación</label>
                  <div class="info-badge">
                    <span class="badge-icon">🕒</span>
                    <span>{{ formatDateLong(proyecto.fecha_ultima_modificacion) }}</span>
                  </div>
                </div>

                <div class="info-item">
                  <label class="info-label">Estado Actual</label>
                  <div class="info-badge">
                    <project-status-badge :estado="proyecto.estado" />
                  </div>
                </div>
              </div>

              <div v-if="proyecto.comentarios" class="comments-section">
                <h3 class="subsection-title">💬 Comentarios del Asesor</h3>
                <div class="comment-box">
                  <p>{{ proyecto.comentarios }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB: Presupuesto -->
        <div v-show="tabActiva === 'presupuesto'" class="tab-content">
          <div class="budget-section">
            <!-- Resumen Presupuestal -->
            <div class="budget-summary">
              <div class="budget-card estimado">
                <div class="budget-icon">💵</div>
                <div class="budget-info">
                  <span class="budget-label">Presupuesto Estimado</span>
                  <span class="budget-amount">${{ formatMoney(proyecto.presupuesto_estimado) }}</span>
                  <span class="budget-currency">COP</span>
                </div>
              </div>

              <div class="budget-card asignado">
                <div class="budget-icon">✅</div>
                <div class="budget-info">
                  <span class="budget-label">Presupuesto Asignado</span>
                  <span class="budget-amount">${{ formatMoney(proyecto.presupuesto_asignado || 0) }}</span>
                  <span class="budget-currency">COP</span>
                </div>
              </div>

              <div class="budget-card ejecutado">
                <div class="budget-icon">📊</div>
                <div class="budget-info">
                  <span class="budget-label">Presupuesto Ejecutado</span>
                  <span class="budget-amount">${{ formatMoney(proyecto.presupuesto_ejecutado) }}</span>
                  <span class="budget-currency">COP</span>
                </div>
              </div>

              <div class="budget-card disponible">
                <div class="budget-icon">💳</div>
                <div class="budget-info">
                  <span class="budget-label">Saldo Disponible</span>
                  <span class="budget-amount">${{ formatMoney(saldoDisponible) }}</span>
                  <span class="budget-currency">COP</span>
                </div>
              </div>
            </div>

            <!-- Barra de Ejecución -->
            <div v-if="proyecto.presupuesto_asignado > 0" class="execution-card">
              <h3 class="subsection-title">📈 Ejecución Presupuestal</h3>
              <div class="execution-visual">
                <div class="execution-bar">
                  <div class="execution-fill" :class="getProgressClass(porcentajeEjecucion)"
                    :style="{ width: porcentajeEjecucion + '%' }">
                    <span class="execution-text">{{ porcentajeEjecucion }}%</span>
                  </div>
                </div>
                <div class="execution-legend">
                  <span>0%</span>
                  <span>25%</span>
                  <span>50%</span>
                  <span>75%</span>
                  <span>100%</span>
                </div>
              </div>
              <div class="execution-details">
                <div class="detail-item">
                  <span class="detail-label">Ejecutado:</span>
                  <span class="detail-value ejecutado">${{ formatMoney(proyecto.presupuesto_ejecutado) }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Disponible:</span>
                  <span class="detail-value disponible">${{ formatMoney(saldoDisponible) }}</span>
                </div>
              </div>
            </div>

            <!-- Items del Presupuesto -->
            <div v-if="proyecto.items_presupuesto && proyecto.items_presupuesto.length > 0" class="items-section">
              <div class="section-header-with-action">
                <h3 class="subsection-title">📝 Desglose del Presupuesto</h3>
                <button @click="exportarPresupuesto" class="btn btn-sm btn-secondary">
                  📊 Exportar Items
                </button>
              </div>

              <div class="items-list">
                <div v-for="(item, index) in proyecto.items_presupuesto" :key="index" class="item-card">
                  <div class="item-header">
                    <span class="item-number">Item #{{ index + 1 }}</span>
                    <span class="item-cost">${{ formatMoney(item.costo) }}</span>
                  </div>
                  <h4 class="item-concept">{{ item.concepto }}</h4>
                  <p class="item-justification">{{ item.justificacion }}</p>
                </div>
              </div>

              <div class="items-total">
                <span class="total-label">Total Presupuesto Estimado:</span>
                <span class="total-amount">${{ formatMoney(totalPresupuesto) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB: Gastos -->
        <div v-show="tabActiva === 'gastos'" class="tab-content">
          <div class="expenses-section">
            <div class="section-header-with-action">
              <h3 class="subsection-title">💸 Gastos del Proyecto</h3>
              <div class="expense-actions">
                <button @click="exportarGastos" class="btn btn-sm btn-secondary">
                  📊 Exportar Gastos
                </button>
                <button v-if="proyecto.estado === 'activo'" @click="registrarGasto" class="btn btn-sm btn-primary">
                  ➕ Registrar Gasto
                </button>
              </div>
            </div>

            <loading-spinner v-if="cargandoGastos" message="Cargando gastos..." />

            <div v-else-if="gastos.length === 0" class="empty-state-inline">
              <span class="empty-icon">📭</span>
              <div class="empty-content">
                <h4>No hay gastos registrados</h4>
                <p>Los gastos del proyecto aparecerán aquí</p>
                <button v-if="proyecto.estado === 'activo'" @click="registrarGasto" class="btn btn-primary">
                  ➕ Registrar Primer Gasto
                </button>
              </div>
            </div>

            <div v-else class="expenses-content">
              <!-- Resumen de Gastos -->
              <div class="expenses-summary">
                <div class="summary-card">
                  <span class="summary-icon">💰</span>
                  <div class="summary-info">
                    <span class="summary-label">Total Gastos</span>
                    <span class="summary-value">${{ formatMoney(totalGastos) }}</span>
                  </div>
                </div>
                <div class="summary-card">
                  <span class="summary-icon">📊</span>
                  <div class="summary-info">
                    <span class="summary-label">Cantidad</span>
                    <span class="summary-value">{{ gastos.length }}</span>
                  </div>
                </div>
                <div class="summary-card">
                  <span class="summary-icon">✅</span>
                  <div class="summary-info">
                    <span class="summary-label">Aprobados</span>
                    <span class="summary-value">{{ gastosAprobados }}</span>
                  </div>
                </div>
                <div class="summary-card">
                  <span class="summary-icon">⏳</span>
                  <div class="summary-info">
                    <span class="summary-label">Pendientes</span>
                    <span class="summary-value">{{ gastosPendientes }}</span>
                  </div>
                </div>
              </div>

              <!-- Tabla de Gastos -->
              <div class="expenses-table-wrapper">
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
                      <td class="cell-id">#{{ gasto.id }}</td>
                      <td class="cell-concept">
                        <span class="concept-text">{{ gasto.concepto }}</span>
                      </td>
                      <td class="cell-amount">${{ formatMoney(gasto.monto) }}</td>
                      <td class="cell-status">
                        <span class="status-badge" :class="`status-${gasto.estado}`">
                          {{ formatEstado(gasto.estado) }}
                        </span>
                      </td>
                      <td class="cell-date">{{ formatDate(gasto.creado_en) }}</td>
                      <td class="cell-soporte">
                        <a v-if="gasto.soporte_url" :href="gasto.soporte_url" target="_blank" class="btn-link">
                          📎 Ver Soporte
                        </a>
                        <span v-else class="text-muted">Sin soporte</span>
                      </td>
                      <td class="cell-actions">
                        <button @click="verDetalleGasto(gasto)" class="btn-icon" title="Ver detalle">
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

        <!-- TAB: Actividad -->
        <div v-show="tabActiva === 'actividad'" class="tab-content">
          <div class="activity-section">
            <h3 class="subsection-title">🕒 Historial de Actividad</h3>
            <div class="timeline">
              <div class="timeline-item">
                <div class="timeline-marker created"></div>
                <div class="timeline-content">
                  <h4>Proyecto Creado</h4>
                  <p>{{ formatDateLong(proyecto.fecha_creacion) }}</p>
                </div>
              </div>

              <div v-if="proyecto.fecha_ultima_modificacion !== proyecto.fecha_creacion" class="timeline-item">
                <div class="timeline-marker updated"></div>
                <div class="timeline-content">
                  <h4>Última Actualización</h4>
                  <p>{{ formatDateLong(proyecto.fecha_ultima_modificacion) }}</p>
                </div>
              </div>

              <div v-if="proyecto.estado !== 'borrador'" class="timeline-item">
                <div class="timeline-marker" :class="proyecto.estado"></div>
                <div class="timeline-content">
                  <h4>Estado: {{ formatEstadoProyecto(proyecto.estado) }}</h4>
                  <p v-if="proyecto.comentarios">{{ proyecto.comentarios }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-state">
      <span class="error-icon">⚠️</span>
      <h2>Proyecto no encontrado</h2>
      <p>El proyecto que buscas no existe o no tienes permiso para verlo</p>
      <button @click="volver" class="btn btn-primary">
        ← Volver a Proyectos
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { projectService } from '@/services/projectService'
import { expenseService } from '@/services/expenseService'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import NotificationCenter from '@/components/shared/NotificationCenter.vue'
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue'

const route = useRoute()
const router = useRouter()
const notifStore = useNotificationStore()

const proyecto = ref(null)
const gastos = ref([])
const loading = ref(false)
const cargandoGastos = ref(false)
const tabActiva = ref('info')

const tabs = [
  { id: 'info', label: 'Información', icon: '📋' },
  { id: 'presupuesto', label: 'Presupuesto', icon: '💰' },
  { id: 'gastos', label: 'Gastos', icon: '💸' },
  { id: 'actividad', label: 'Actividad', icon: '🕒' }
]

const puedeEditar = computed(() => {
  return proyecto.value?.estado === 'borrador' || proyecto.value?.estado === 'rechazado'
})

const puedeEnviar = computed(() => {
  return proyecto.value?.estado === 'borrador'
})

const puedeEliminar = computed(() => {
  return proyecto.value?.estado === 'borrador'
})

const saldoDisponible = computed(() => {
  if (!proyecto.value) return 0
  return (proyecto.value.presupuesto_asignado || 0) - proyecto.value.presupuesto_ejecutado
})

const porcentajeEjecucion = computed(() => {
  if (!proyecto.value || !proyecto.value.presupuesto_asignado) return 0
  return Math.min(
    Math.round((proyecto.value.presupuesto_ejecutado / proyecto.value.presupuesto_asignado) * 100),
    100
  )
})

const totalPresupuesto = computed(() => {
  if (!proyecto.value?.items_presupuesto) return 0
  return proyecto.value.items_presupuesto.reduce((sum, item) => sum + (item.costo || 0), 0)
})

const totalGastos = computed(() => {
  return gastos.value.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
})

const gastosAprobados = computed(() => {
  return gastos.value.filter(g => g.estado === 'aprobado').length
})

const gastosPendientes = computed(() => {
  return gastos.value.filter(g => g.estado === 'pendiente').length
})

onMounted(async () => {
  const id = route.params.id
  await cargarProyecto(id)
  await cargarGastos(id)
})

const cargarProyecto = async (id) => {
  try {
    loading.value = true
    proyecto.value = await projectService.getById(id)
  } catch (error) {
    console.error('Error:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar el proyecto'
    })
  } finally {
    loading.value = false
  }
}

const cargarGastos = async (proyectoId) => {
  try {
    cargandoGastos.value = true
    const todosGastos = await expenseService.getAll()
    gastos.value = todosGastos.filter(g => g.proyecto_id === parseInt(proyectoId))
  } catch (error) {
    console.error('Error:', error)
  } finally {
    cargandoGastos.value = false
  }
}

const volver = () => {
  router.push('/proyectos')
}

const editar = () => {
  router.push(`/proyectos/${route.params.id}/editar`)
}

const enviarValidacion = async () => {
  const confirmacion = confirm('¿Estás seguro de enviar este proyecto para validación del asesor?')
  if (!confirmacion) return

  try {
    await projectService.updateStatus(route.params.id, { estado: 'pendiente_validacion' })
    notifStore.addNotification({
      tipo: 'success',
      titulo: '✅ Proyecto Enviado',
      mensaje: 'El proyecto ha sido enviado para validación'
    })
    await cargarProyecto(route.params.id)
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo enviar el proyecto'
    })
  }
}

const eliminar = async () => {
  const confirmacion = confirm('¿Estás seguro de eliminar este proyecto? Esta acción no se puede deshacer.')
  if (!confirmacion) return

  try {
    await projectService.delete(route.params.id)
    notifStore.addNotification({
      tipo: 'success',
      titulo: '🗑️ Proyecto Eliminado',
      mensaje: 'El proyecto ha sido eliminado'
    })
    router.push('/proyectos')
  } catch (error) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo eliminar el proyecto'
    })
  }
}

const registrarGasto = () => {
  router.push(`/gastos/crear?proyecto_id=${route.params.id}`)
}

const exportarPDF = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: '📄 Generando PDF',
    mensaje: 'El PDF se está generando. Se descargará automáticamente.'
  })
  // Aquí implementarías la generación del PDF
  console.log('Exportando a PDF...')
}

const exportarPresupuesto = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: '📊 Exportando Items',
    mensaje: 'Descargando items del presupuesto...'
  })
  console.log('Exportando presupuesto...')
}

const exportarGastos = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: '📊 Exportando Gastos',
    mensaje: 'Descargando reporte de gastos...'
  })
  console.log('Exportando gastos...')
}

const compartir = () => {
  if (navigator.share) {
    navigator.share({
      title: proyecto.value.nombre,
      text: proyecto.value.descripcion,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    notifStore.addNotification({
      tipo: 'success',
      titulo: '🔗 Enlace Copiado',
      mensaje: 'El enlace ha sido copiado al portapapeles'
    })
  }
}

const imprimir = () => {
  window.print()
}

const verDetalleGasto = (gasto) => {
  alert(`Detalle del gasto: ${gasto.concepto}\nMonto: $${formatMoney(gasto.monto)}\nEstado: ${formatEstado(gasto.estado)}`)
}

const getProgressClass = (porcentaje) => {
  if (porcentaje >= 90) return 'fill-danger'
  if (porcentaje >= 70) return 'fill-warning'
  return 'fill-success'
}

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value || 0)
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDateLong = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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

const formatEstadoProyecto = (estado) => {
  const estados = {
    borrador: 'Borrador',
    pendiente_validacion: 'Pendiente de Validación',
    validado_asesor: 'Validado por Asesor',
    activo: 'Activo',
    rechazado: 'Rechazado',
    finalizado: 'Finalizado'
  }
  return estados[estado] || estado
}
</script>

<style scoped>
.project-detail-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: var(--space-8);
}

.detail-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.detail-header {
  margin-bottom: var(--space-6);
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
  margin-bottom: var(--space-6);
  font-size: 0.9375rem;
}

.btn-back:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  transform: translateX(-5px);
}

.header-main {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  margin-bottom: var(--space-6);
}

.header-info {
  margin-bottom: var(--space-6);
}

.project-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
  line-height: 1.2;
}

.title-meta {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.project-code {
  font-family: var(--font-mono);
  font-size: 1rem;
  color: var(--primary);
  font-weight: 700;
  background: var(--gray-50);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
}

.header-actions {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  align-items: center;
}

.detail-tabs {
  display: flex;
  gap: var(--space-2);
  background: white;
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--space-6);
  overflow-x: auto;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: transparent;
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 700;
  color: var(--gray-600);
  cursor: pointer;
  transition: var(--transition-base);
  white-space: nowrap;
  font-size: 0.9375rem;
}

.tab-button:hover {
  background: var(--gray-50);
  color: var(--gray-900);
}

.tab-button.active {
  background: var(--gradient-blue);
  color: white;
  box-shadow: var(--shadow-md);
}

.tab-icon {
  font-size: 1.25rem;
}

.detail-content {
  animation: fadeIn 0.5s ease;
}

.tab-content {
  animation: slideIn 0.3s ease;
}

.section-card {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  margin-bottom: var(--space-6);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-4);
  border-bottom: 3px solid var(--primary);
}

.subsection-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-6);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-6);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--gray-700);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.info-value-box {
  padding: var(--space-5);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--primary);
}

.info-value-box p {
  color: var(--gray-800);
  line-height: 1.8;
  font-size: 1rem;
}

.info-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-5);
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: var(--radius-lg);
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--gray-900);
  border: 2px solid var(--gray-200);
}

.badge-icon {
  font-size: 1.5rem;
}

.comments-section {
  margin-top: var(--space-8);
  padding-top: var(--space-8);
  border-top: 2px solid var(--gray-100);
}

.comment-box {
  padding: var(--space-6);
  background: linear-gradient(135deg, #dbeafe, #e0e7ff);
  border-left: 6px solid var(--info);
  border-radius: var(--radius-xl);
  color: var(--gray-800);
  line-height: 1.8;
  font-size: 1rem;
}

/* Presupuesto */
.budget-summary {
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
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 2px solid var(--gray-100);
  transition: var(--transition-base);
}

.budget-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
  border-color: var(--primary);
}

.budget-icon {
  font-size: 3rem;
  flex-shrink: 0;
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
  letter-spacing: 0.1em;
}

.budget-amount {
  font-size: 1.875rem;
  font-weight: 900;
  color: var(--primary);
}

.budget-card.estimado .budget-amount {
  color: var(--info);
}

.budget-card.asignado .budget-amount {
  color: var(--primary);
}

.budget-card.ejecutado .budget-amount {
  color: var(--warning);
}

.budget-card.disponible .budget-amount {
  color: var(--success);
}

.budget-currency {
  font-size: 0.75rem;
  color: var(--gray-500);
  font-weight: 700;
}

.execution-card {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  margin-bottom: var(--space-8);
}

.execution-visual {
  margin-bottom: var(--space-6);
}

.execution-bar {
  width: 100%;
  height: 32px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.execution-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: var(--space-4);
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.execution-text {
  color: white;
  font-weight: 900;
  font-size: 1rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
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

.execution-legend {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--gray-500);
  font-weight: 700;
  margin-top: var(--space-2);
}

.execution-details {
  display: flex;
  justify-content: space-around;
  gap: var(--space-6);
  padding: var(--space-6);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.detail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.detail-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 700;
}

.detail-value {
  font-size: 1.5rem;
  font-weight: 900;
}

.detail-value.ejecutado {
  color: var(--warning);
}

.detail-value.disponible {
  color: var(--success);
}

.items-section {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.section-header-with-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-4);
}

.expense-actions {
  display: flex;
  gap: var(--space-3);
}

.items-list {
  display: grid;
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.item-card {
  padding: var(--space-6);
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border-radius: var(--radius-xl);
  border: 2px solid var(--gray-200);
  transition: var(--transition-base);
}

.item-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.item-number {
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--primary);
  background: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  border: 2px solid var(--primary);
}

.item-cost {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--success);
}

.item-concept {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.item-justification {
  color: var(--gray-700);
  line-height: 1.7;
  font-size: 0.9375rem;
}

.items-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-6);
  background: var(--gradient-blue);
  color: white;
  border-radius: var(--radius-xl);
  font-size: 1.25rem;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.total-label {
  font-weight: 700;
}

.total-amount {
  font-size: 2rem;
  font-weight: 900;
}

/* Gastos */
.expenses-section {
  background: white;
  padding: var(--space-8);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.expenses-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.summary-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-5);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border: 2px solid var(--gray-200);
}

.summary-icon {
  font-size: 2rem;
}

.summary-info {
  display: flex;
  flex-direction: column;
}

.summary-label {
  font-size: 0.75rem;
  color: var(--gray-600);
  font-weight: 700;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--gray-900);
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
  letter-spacing: 0.05em;
}

.expenses-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  font-size: 0.9375rem;
}

.expenses-table tbody tr {
  transition: var(--transition-base);
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
  align-items: center;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 800;
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

.btn-link {
  color: var(--primary);
  font-weight: 700;
  text-decoration: none;
  transition: var(--transition-base);
}

.btn-link:hover {
  text-decoration: underline;
  color: var(--primary-dark);
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
  font-size: 1.125rem;
}

.btn-icon:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.empty-state-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-6);
  padding: var(--space-12);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border: 2px dashed var(--gray-300);
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.empty-content {
  text-align: center;
}

.empty-content h4 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.empty-content p {
  color: var(--gray-600);
  margin-bottom: var(--space-4);
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: var(--space-8);
}

.timeline::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--gray-200);
}

.timeline-item {
  position: relative;
  padding-bottom: var(--space-8);
}

.timeline-marker {
  position: absolute;
  left: -46px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  border: 4px solid white;
  box-shadow: 0 0 0 4px var(--gray-200);
}

.timeline-marker.created {
  background: var(--info);
}

.timeline-marker.updated {
  background: var(--warning);
}

.timeline-marker.activo {
  background: var(--success);
}

.timeline-marker.rechazado {
  background: var(--error);
}

.timeline-content h4 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.timeline-content p {
  color: var(--gray-600);
  line-height: 1.6;
}

.error-state {
  text-align: center;
  padding: var(--space-16);
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 6rem;
  margin-bottom: var(--space-6);
  opacity: 0.5;
}

.error-state h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.error-state p {
  color: var(--gray-600);
  font-size: 1.125rem;
  margin-bottom: var(--space-8);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media print {

  .detail-header,
  .detail-tabs,
  .header-actions {
    display: none;
  }
}

@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .budget-summary {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .project-detail-view {
    padding: var(--space-4);
  }

  .project-title {
    font-size: 1.75rem;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .header-actions .btn {
    width: 100%;
  }

  .budget-summary {
    grid-template-columns: 1fr;
  }

  .detail-tabs {
    overflow-x: scroll;
  }

  .expenses-table-wrapper {
    overflow-x: scroll;
  }
}
</style>
