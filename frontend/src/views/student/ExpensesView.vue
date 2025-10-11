<template>
  <div class="expenses-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">Mis Gastos</h1>
        <p class="page-subtitle">Gestiona los gastos de tus proyectos</p>
      </div>
      <div class="header-actions">
        <notification-center />
        <button @click="mostrarModalRegistro = true" class="btn btn-primary">
          ➕ Registrar Gasto
        </button>
      </div>
    </div>

    <loading-spinner v-if="loading" />

    <div v-else class="expenses-content">
      <!-- Estadísticas -->
      <div class="stats-grid">
        <div class="stat-card card-primary">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <p class="stat-label">Total Gastos</p>
            <h3 class="stat-value">${{ formatMoney(totalGastos) }}</h3>
            <p class="stat-change">{{ gastos.length }} registros</p>
          </div>
        </div>

        <div class="stat-card card-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">Pendientes</p>
            <h3 class="stat-value">{{ gastosPendientes }}</h3>
            <p class="stat-change">${{ formatMoney(montoPendientes) }}</p>
          </div>
        </div>

        <div class="stat-card card-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Aprobados</p>
            <h3 class="stat-value">{{ gastosAprobados }}</h3>
            <p class="stat-change">${{ formatMoney(montoAprobados) }}</p>
          </div>
        </div>

        <div class="stat-card card-danger">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <p class="stat-label">Rechazados</p>
            <h3 class="stat-value">{{ gastosRechazados }}</h3>
            <p class="stat-change">${{ formatMoney(montoRechazados) }}</p>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-card">
        <div class="filters-row">
          <div class="filter-group">
            <label>Proyecto</label>
            <select v-model="filtros.proyecto_id" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los proyectos</option>
              <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">
                {{ proyecto.nombre }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Estado</label>
            <select v-model="filtros.estado" @change="aplicarFiltros" class="form-select">
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendientes</option>
              <option value="aprobado">Aprobados</option>
              <option value="rechazado">Rechazados</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Buscar</label>
            <input v-model="filtros.busqueda" type="text" placeholder="Buscar por concepto..." class="form-input"
              @input="aplicarFiltros" />
          </div>

          <button @click="limpiarFiltros" class="btn btn-secondary">
            🔄 Limpiar
          </button>
        </div>
      </div>

      <!-- Lista de Gastos -->
      <div v-if="gastosFiltrados.length === 0" class="empty-state">
        <span class="empty-icon">📭</span>
        <h3>No se encontraron gastos</h3>
        <p v-if="filtros.proyecto_id || filtros.estado || filtros.busqueda">
          Intenta ajustar los filtros de búsqueda
        </p>
        <p v-else>
          Aún no has registrado gastos. ¡Registra tu primer gasto!
        </p>
        <button @click="mostrarModalRegistro = true" class="btn btn-primary">
          ➕ Registrar Gasto
        </button>
      </div>

      <div v-else class="expenses-table-card">
        <div class="table-header">
          <h3>📋 Listado de Gastos</h3>
          <button @click="exportarGastos" class="btn btn-sm btn-secondary">
            📊 Exportar
          </button>
        </div>

        <div class="table-wrapper">
          <table class="expenses-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Proyecto</th>
                <th>Concepto</th>
                <th>Monto</th>
                <th>Estado</th>
                <th>Fecha</th>
                <th>Soporte</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="gasto in gastosFiltrados" :key="gasto.id">
                <td class="cell-id">#{{ gasto.id }}</td>
                <td class="cell-proyecto">
                  <span class="proyecto-badge">{{ getProyectoNombre(gasto.proyecto_id) }}</span>
                </td>
                <td class="cell-concepto">{{ gasto.concepto }}</td>
                <td class="cell-monto">${{ formatMoney(gasto.monto) }}</td>
                <td class="cell-estado">
                  <span class="status-badge" :class="`status-${gasto.estado}`">
                    {{ formatEstado(gasto.estado) }}
                  </span>
                </td>
                <td class="cell-fecha">{{ formatDate(gasto.creado_en) }}</td>
                <td class="cell-soporte">
                  <a v-if="gasto.soporte_url" :href="gasto.soporte_url" target="_blank" class="btn-link">
                    📎 Ver
                  </a>
                  <span v-else class="text-muted">Sin soporte</span>
                </td>
                <td class="cell-actions">
                  <button @click="verDetalle(gasto)" class="btn-icon" title="Ver detalle">
                    👁️
                  </button>
                  <button v-if="gasto.estado === 'pendiente'" @click="editarGasto(gasto)" class="btn-icon edit"
                    title="Editar">
                    ✏️
                  </button>
                  <button v-if="gasto.estado === 'pendiente'" @click="eliminarGasto(gasto.id)" class="btn-icon delete"
                    title="Eliminar">
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal: Registrar/Editar Gasto -->
    <modal-dialog v-if="mostrarModalRegistro" @close="cerrarModalRegistro">
      <template #header>
        <h2>{{ gastoEditando ? '✏️ Editar Gasto' : '➕ Registrar Nuevo Gasto' }}</h2>
      </template>

      <template #body>
        <form @submit.prevent="guardarGasto" class="expense-form">
          <div class="form-group">
            <label class="form-label">
              Proyecto *
              <span class="label-hint">Selecciona el proyecto al que pertenece este gasto</span>
            </label>
            <select v-model="formularioGasto.proyecto_id" class="form-select" required :disabled="gastoEditando">
              <option value="">-- Selecciona un proyecto --</option>
              <option v-for="proyecto in proyectosActivos" :key="proyecto.id" :value="proyecto.id">
                {{ proyecto.nombre }} - Disponible: ${{ formatMoney(calcularDisponible(proyecto)) }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">
              Concepto *
              <span class="label-hint">Describe brevemente el gasto</span>
            </label>
            <input v-model="formularioGasto.concepto" type="text" class="form-input"
              placeholder="Ej: Compra de materiales de laboratorio" required maxlength="200" />
          </div>

          <div class="form-group">
            <label class="form-label">
              Monto (COP) *
              <span class="label-hint">Valor del gasto</span>
            </label>
            <div class="input-with-prefix">
              <span class="input-prefix">$</span>
              <input v-model.number="formularioGasto.monto" type="number" class="form-input" placeholder="0" required
                min="1" step="100" />
            </div>
            <p v-if="presupuestoSeleccionado" class="form-hint">
              💡 Disponible en proyecto: <strong>${{ formatMoney(presupuestoSeleccionado) }}</strong>
            </p>
          </div>

          <div class="form-group">
            <label class="form-label">
              URL del Soporte *
              <span class="label-hint">Enlace al documento de soporte (Google Drive, Dropbox, etc.)</span>
            </label>
            <input v-model="formularioGasto.soporte_url" type="url" class="form-input"
              placeholder="https://drive.google.com/..." required />
          </div>
        </form>
      </template>

      <template #footer>
        <button @click="cerrarModalRegistro" class="btn btn-secondary">
          Cancelar
        </button>
        <button @click="guardarGasto" class="btn btn-primary" :disabled="enviandoGasto">
          <span v-if="enviandoGasto">⏳ Guardando...</span>
          <span v-else>{{ gastoEditando ? '💾 Actualizar' : '✅ Registrar' }}</span>
        </button>
      </template>
    </modal-dialog>

    <!-- Modal: Detalle del Gasto -->
    <modal-dialog v-if="mostrarModalDetalle" @close="cerrarModalDetalle">
      <template #header>
        <h2>👁️ Detalle del Gasto #{{ gastoSeleccionado?.id }}</h2>
      </template>

      <template #body>
        <div v-if="gastoSeleccionado" class="expense-detail">
          <div class="detail-row">
            <span class="detail-label">Proyecto:</span>
            <span class="detail-value">{{ getProyectoNombre(gastoSeleccionado.proyecto_id) }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Concepto:</span>
            <span class="detail-value">{{ gastoSeleccionado.concepto }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Monto:</span>
            <span class="detail-value amount">${{ formatMoney(gastoSeleccionado.monto) }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Estado:</span>
            <span class="status-badge" :class="`status-${gastoSeleccionado.estado}`">
              {{ formatEstado(gastoSeleccionado.estado) }}
            </span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Fecha de Registro:</span>
            <span class="detail-value">{{ formatDateLong(gastoSeleccionado.creado_en) }}</span>
          </div>

          <div v-if="gastoSeleccionado.aprobado_en" class="detail-row">
            <span class="detail-label">Fecha de Aprobación:</span>
            <span class="detail-value">{{ formatDateLong(gastoSeleccionado.aprobado_en) }}</span>
          </div>

          <div v-if="gastoSeleccionado.comentarios" class="detail-row full">
            <span class="detail-label">Comentarios:</span>
            <div class="comment-box">
              <p>{{ gastoSeleccionado.comentarios }}</p>
            </div>
          </div>

          <div class="detail-row">
            <span class="detail-label">Soporte:</span>
            <a :href="gastoSeleccionado.soporte_url" target="_blank" class="btn-link">
              📎 Ver Documento de Soporte
            </a>
          </div>
        </div>
      </template>

      <template #footer>
        <button @click="cerrarModalDetalle" class="btn btn-primary">
          Cerrar
        </button>
      </template>
    </modal-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { projectService } from '@/services/projectService'
import { expenseService } from '@/services/expenseService'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import NotificationCenter from '@/components/shared/NotificationCenter.vue'
import ModalDialog from '@/components/shared/ModalDialog.vue'

const authStore = useAuthStore()
const notifStore = useNotificationStore()

const loading = ref(false)
const enviandoGasto = ref(false)
const proyectos = ref([])
const gastos = ref([])
const mostrarModalRegistro = ref(false)
const mostrarModalDetalle = ref(false)
const gastoEditando = ref(null)
const gastoSeleccionado = ref(null)

const filtros = ref({
  proyecto_id: '',
  estado: '',
  busqueda: ''
})

const formularioGasto = ref({
  proyecto_id: '',
  concepto: '',
  monto: 0,
  soporte_url: ''
})

// CORRECCIÓN: Filtrar solo proyectos activos del usuario actual
const proyectosActivos = computed(() => {
  const userId = authStore.user?.id
  console.log('Usuario ID:', userId)
  console.log('Todos los proyectos:', proyectos.value)

  const activos = proyectos.value.filter(p => {
    const esActivo = p.estado === 'activo'
    const esDelUsuario = p.estudiante_id === userId
    console.log(`Proyecto ${p.id}: activo=${esActivo}, delUsuario=${esDelUsuario}`)
    return esActivo && esDelUsuario
  })

  console.log('Proyectos activos filtrados:', activos)
  return activos
})

const presupuestoSeleccionado = computed(() => {
  if (!formularioGasto.value.proyecto_id) return 0
  const proyecto = proyectos.value.find(p => p.id === parseInt(formularioGasto.value.proyecto_id))
  if (!proyecto) return 0
  return calcularDisponible(proyecto)
})

const gastosFiltrados = computed(() => {
  let resultado = gastos.value

  if (filtros.value.proyecto_id) {
    resultado = resultado.filter(g => g.proyecto_id === parseInt(filtros.value.proyecto_id))
  }

  if (filtros.value.estado) {
    resultado = resultado.filter(g => g.estado === filtros.value.estado)
  }

  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(g =>
      g.concepto.toLowerCase().includes(busqueda)
    )
  }

  return resultado.sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en))
})

const totalGastos = computed(() => {
  return gastos.value.reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
})

const gastosPendientes = computed(() => {
  return gastos.value.filter(g => g.estado === 'pendiente').length
})

const gastosAprobados = computed(() => {
  return gastos.value.filter(g => g.estado === 'aprobado').length
})

const gastosRechazados = computed(() => {
  return gastos.value.filter(g => g.estado === 'rechazado').length
})

const montoPendientes = computed(() => {
  return gastos.value
    .filter(g => g.estado === 'pendiente')
    .reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
})

const montoAprobados = computed(() => {
  return gastos.value
    .filter(g => g.estado === 'aprobado')
    .reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
})

const montoRechazados = computed(() => {
  return gastos.value
    .filter(g => g.estado === 'rechazado')
    .reduce((sum, g) => sum + parseFloat(g.monto || 0), 0)
})

onMounted(async () => {
  await cargarDatos()
})

const cargarDatos = async () => {
  try {
    loading.value = true

    console.log('Cargando datos...')
    console.log('Usuario actual:', authStore.user)

    const [proyectosData, gastosData] = await Promise.all([
      projectService.getAll(),
      expenseService.getAll()
    ])

    proyectos.value = proyectosData
    gastos.value = gastosData

    console.log('Proyectos cargados:', proyectosData)
    console.log('Gastos cargados:', gastosData)

    if (proyectosActivos.value.length === 0) {
      notifStore.addNotification({
        tipo: 'warning',
        titulo: 'Sin Proyectos Activos',
        mensaje: 'No tienes proyectos activos. Debes tener un proyecto activo para registrar gastos.'
      })
    }

  } catch (error) {
    console.error('Error al cargar datos:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo cargar la información'
    })
  } finally {
    loading.value = false
  }
}

const aplicarFiltros = () => {
  // Computed se encarga automáticamente
}

const limpiarFiltros = () => {
  filtros.value = {
    proyecto_id: '',
    estado: '',
    busqueda: ''
  }
}

const cerrarModalRegistro = () => {
  mostrarModalRegistro.value = false
  gastoEditando.value = null
  formularioGasto.value = {
    proyecto_id: '',
    concepto: '',
    monto: 0,
    soporte_url: ''
  }
}

const guardarGasto = async () => {
  // Validaciones
  if (!formularioGasto.value.proyecto_id) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'Debes seleccionar un proyecto'
    })
    return
  }

  if (!formularioGasto.value.concepto.trim()) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'Debes especificar el concepto del gasto'
    })
    return
  }

  if (formularioGasto.value.monto <= 0) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Monto Inválido',
      mensaje: 'El monto debe ser mayor a cero'
    })
    return
  }

  if (!formularioGasto.value.soporte_url.trim()) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Campo Requerido',
      mensaje: 'Debes proporcionar la URL del soporte'
    })
    return
  }

  // Validar presupuesto disponible
  if (formularioGasto.value.monto > presupuestoSeleccionado.value) {
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Presupuesto Insuficiente',
      mensaje: `El monto excede el presupuesto disponible ($${formatMoney(presupuestoSeleccionado.value)})`
    })
    return
  }

  try {
    enviandoGasto.value = true

    if (gastoEditando.value) {
      // Actualizar gasto existente
      await expenseService.update(gastoEditando.value.id, formularioGasto.value)
      notifStore.addNotification({
        tipo: 'success',
        titulo: '✅ Gasto Actualizado',
        mensaje: 'El gasto ha sido actualizado exitosamente'
      })
    } else {
      // Crear nuevo gasto
      const nuevoGasto = {
        proyecto_id: parseInt(formularioGasto.value.proyecto_id),
        concepto: formularioGasto.value.concepto.trim(),
        monto: parseFloat(formularioGasto.value.monto),
        soporte_url: formularioGasto.value.soporte_url.trim()
      }

      console.log('Enviando gasto:', nuevoGasto)

      await expenseService.create(nuevoGasto)
      notifStore.addNotification({
        tipo: 'success',
        titulo: '✅ Gasto Registrado',
        mensaje: 'El gasto ha sido registrado y está pendiente de aprobación'
      })
    }

    await cargarDatos()
    cerrarModalRegistro()
  } catch (error) {
    console.error('Error al guardar gasto:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: error.response?.data?.detail || 'No se pudo guardar el gasto'
    })
  } finally {
    enviandoGasto.value = false
  }
}

const editarGasto = (gasto) => {
  gastoEditando.value = gasto
  formularioGasto.value = {
    proyecto_id: gasto.proyecto_id,
    concepto: gasto.concepto,
    monto: gasto.monto,
    soporte_url: gasto.soporte_url
  }
  mostrarModalRegistro.value = true
}

const eliminarGasto = async (id) => {
  const confirmacion = confirm('¿Estás seguro de eliminar este gasto? Esta acción no se puede deshacer.')
  if (!confirmacion) return

  try {
    await expenseService.delete(id)
    notifStore.addNotification({
      tipo: 'success',
      titulo: '🗑️ Gasto Eliminado',
      mensaje: 'El gasto ha sido eliminado exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error al eliminar gasto:', error)
    notifStore.addNotification({
      tipo: 'error',
      titulo: 'Error',
      mensaje: 'No se pudo eliminar el gasto'
    })
  }
}

const verDetalle = (gasto) => {
  gastoSeleccionado.value = gasto
  mostrarModalDetalle.value = true
}

const cerrarModalDetalle = () => {
  mostrarModalDetalle.value = false
  gastoSeleccionado.value = null
}

const exportarGastos = () => {
  notifStore.addNotification({
    tipo: 'info',
    titulo: '📊 Exportando',
    mensaje: 'Generando reporte de gastos...'
  })
  console.log('Exportando gastos...')
}

const getProyectoNombre = (id) => {
  const p = proyectos.value.find(x => x.id === id)
  return p ? p.nombre : `Proyecto ${id}`
}

const calcularDisponible = (proyecto) => {
  return (proyecto.presupuesto_asignado || 0) - proyecto.presupuesto_ejecutado
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
</script>


<style scoped>
.expenses-view {
  padding: var(--space-8);
  max-width: 1600px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-8);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
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
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  gap: var(--space-4);
  border-left: 5px solid var(--primary);
  transition: var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
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
  text-transform: uppercase;
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--gray-900);
}

.stat-change {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 600;
}

.filters-card {
  background: white;
  padding: var(--space-6);
  border-radius: var(--radius-2xl);
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

.expenses-table-card {
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-6);
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.table-header h3 {
  font-size: 1.5rem;
  font-weight: 800;
}

.table-wrapper {
  overflow-x: auto;
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
}

.expenses-table thead {
  background: var(--gray-50);
}

.expenses-table th {
  padding: var(--space-4);
  text-align: left;
  font-weight: 800;
  color: var(--gray-700);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 3px solid var(--gray-200);
}

.expenses-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-100);
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

.cell-proyecto {
  max-width: 200px;
}

.proyecto-badge {
  display: inline-block;
  padding: var(--space-2) var(--space-3);
  background: var(--info-light);
  color: var(--info);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 600;
}

.cell-concepto {
  max-width: 300px;
  font-weight: 600;
}

.cell-monto {
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
}

.btn-link:hover {
  text-decoration: underline;
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
  font-size: 1.125rem;
}

.btn-icon:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.btn-icon.edit:hover {
  background: var(--warning);
}

.btn-icon.delete:hover {
  background: var(--error);
}

.empty-state {
  text-align: center;
  padding: var(--space-16);
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-md);
}

.empty-icon {
  font-size: 6rem;
  margin-bottom: var(--space-6);
  opacity: 0.4;
}

.empty-state h3 {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.empty-state p {
  color: var(--gray-600);
  font-size: 1.125rem;
  margin-bottom: var(--space-8);
}

/* Formulario */
.expense-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-label {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--gray-900);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.label-hint {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--gray-500);
}

.form-input,
.form-select {
  padding: var(--space-4);
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-size: 1rem;
  transition: var(--transition-base);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: var(--space-4);
  font-weight: 700;
  color: var(--gray-600);
  font-size: 1.125rem;
}

.input-with-prefix .form-input {
  padding-left: var(--space-10);
}

.form-hint {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-top: var(--space-2);
}

/* Detalle */
.expense-detail {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
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
  font-size: 0.9375rem;
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

.comment-box {
  width: 100%;
  padding: var(--space-4);
  background: var(--info-light);
  border-left: 4px solid var(--info);
  border-radius: var(--radius-lg);
  color: var(--gray-800);
  line-height: 1.7;
}

@media (max-width: 768px) {
  .expenses-view {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .header-actions {
    width: 100%;
  }

  .filters-row {
    grid-template-columns: 1fr;
  }

  .table-wrapper {
    overflow-x: scroll;
  }
}
</style>
