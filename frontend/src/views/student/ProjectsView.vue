<template>
  <div class="projects-view">
    <div class="projects-header">
      <div>
        <h1 class="page-title">Mis Proyectos</h1>
        <p class="page-subtitle">Gestiona y monitorea tus proyectos de grado</p>
      </div>

      <div class="header-actions">
        <button @click="exportarPDF" class="btn btn-secondary">
          <span>📄</span> PDF
        </button>
        <button @click="exportarExcel" class="btn btn-secondary">
          <span>📊</span> Excel
        </button>
        <router-link to="/proyectos/crear" class="btn btn-primary">
          <span>➕</span> Nuevo Proyecto
        </router-link>
      </div>
    </div>

    <div class="filters-card">
      <div class="filter-group">
        <label>Estado</label>
        <select v-model="filtroEstado" class="input">
          <option value="">Todos</option>
          <option value="borrador">Borrador</option>
          <option value="pendiente_validacion">Pendiente</option>
          <option value="validado_asesor">Validado</option>
          <option value="activo">Activo</option>
          <option value="rechazado">Rechazado</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Buscar</label>
        <input v-model="busqueda" type="text" class="input" placeholder="Nombre o código..." />
      </div>
    </div>

    <loading-spinner v-if="loading" />

    <div v-else-if="proyectosFiltrados.length === 0" class="empty-state">
      <div class="empty-icon">📂</div>
      <h3>{{ filtroEstado || busqueda ? 'No se encontraron proyectos' : 'No tienes proyectos' }}</h3>
      <p>{{ filtroEstado || busqueda ? 'Intenta cambiar los filtros' : 'Crea tu primer proyecto' }}</p>
      <router-link v-if="!filtroEstado && !busqueda" to="/proyectos/crear" class="btn btn-primary">
        Crear Primer Proyecto
      </router-link>
    </div>

    <div v-else class="projects-grid">
      <div v-for="proyecto in proyectosFiltrados" :key="proyecto.id" class="project-card">
        <div class="project-header">
          <div class="project-icon">📋</div>
          <ProjectStatusBadge :estado="proyecto.estado" />
        </div>

        <div class="project-content">
          <h3 class="project-title">{{ proyecto.nombre }}</h3>
          <p class="project-code">{{ proyecto.codigo_proyecto }}</p>
          <p class="project-description">{{ truncateText(proyecto.descripcion, 100) }}</p>

          <div class="budget-summary">
            <div class="budget-item">
              <span class="budget-label">Estimado</span>
              <span class="budget-value">${{ formatMoney(proyecto.presupuesto_estimado) }}</span>
            </div>
            <div class="budget-divider"></div>
            <div class="budget-item">
              <span class="budget-label">Ejecutado</span>
              <span class="budget-value">${{ formatMoney(proyecto.presupuesto_ejecutado) }}</span>
            </div>
          </div>

          <div class="progress-container">
            <div class="progress-info">
              <span class="progress-label">Progreso</span>
              <span class="progress-percentage">{{ calcularProgreso(proyecto) }}%</span>
            </div>
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" :style="{ width: calcularProgreso(proyecto) + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="project-actions">
          <button @click="verDetalles(proyecto.id)" class="btn-action btn-primary">
            <span>👁️</span> Ver
          </button>

          <button v-if="puedeEditar(proyecto.estado)" @click="editarProyecto(proyecto.id)"
            class="btn-action btn-secondary">
            <span>✏️</span> Editar
          </button>

          <button v-if="proyecto.estado === 'borrador'" @click="enviarValidacion(proyecto.id)"
            class="btn-action btn-success">
            <span>📤</span> Enviar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { projectService } from '@/services/projectService'
import { reportService } from '@/services/reportService'
import ProjectStatusBadge from '@/components/project/ProjectStatusBadge.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const router = useRouter()
const proyectos = ref([])
const loading = ref(false)
const filtroEstado = ref('')
const busqueda = ref('')

const proyectosFiltrados = computed(() => {
  let filtered = proyectos.value

  if (filtroEstado.value) {
    filtered = filtered.filter(p => p.estado === filtroEstado.value)
  }

  if (busqueda.value) {
    const search = busqueda.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.nombre.toLowerCase().includes(search) ||
      p.codigo_proyecto.toLowerCase().includes(search)
    )
  }

  return filtered
})

onMounted(async () => {
  await cargarProyectos()
})

const cargarProyectos = async () => {
  try {
    loading.value = true
    proyectos.value = await projectService.getAll()
  } catch (error) {
    console.error('Error:', error)
    alert('Error al cargar proyectos')
  } finally {
    loading.value = false
  }
}

const puedeEditar = (estado) => {
  return estado === 'borrador' || estado === 'rechazado'
}

const calcularProgreso = (proyecto) => {
  if (!proyecto.presupuesto_estimado) return 0
  const progreso = (proyecto.presupuesto_ejecutado / proyecto.presupuesto_estimado) * 100
  return Math.min(Math.round(progreso), 100)
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatMoney = (value) => {
  return new Intl.NumberFormat('es-CO').format(value)
}

const verDetalles = (id) => {
  router.push(`/proyectos/${id}`)
}

const editarProyecto = (id) => {
  router.push(`/proyectos/${id}/editar`)
}

const enviarValidacion = async (id) => {
  if (!confirm('¿Enviar proyecto a validación?')) return

  try {
    await projectService.updateStatus(id, 'pendiente_validacion')
    alert('✅ Proyecto enviado')
    await cargarProyectos()
  } catch (error) {
    alert('❌ Error al enviar')
  }
}

const exportarPDF = async () => {
  try {
    await reportService.exportProyectosPDF(filtroEstado.value || null)
  } catch (error) {
    alert('Error al exportar')
  }
}

const exportarExcel = async () => {
  try {
    await reportService.exportProyectosExcel(filtroEstado.value || null)
  } catch (error) {
    alert('Error al exportar')
  }
}
</script>

<style scoped>
.projects-view {
  padding: var(--space-8);
  max-width: 1400px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease;
}

.projects-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-8);
  gap: var(--space-6);
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.page-subtitle {
  color: var(--gray-600);
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: var(--space-3);
}

.filters-card {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-100);
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: var(--space-4);
}

.filter-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}

.empty-state {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--space-16) var(--space-8);
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-100);
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: var(--space-6);
  opacity: 0.5;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: var(--space-6);
}

.project-card {
  background: white;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-100);
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  box-shadow: var(--shadow-xl);
  transform: translateY(-6px);
}

.project-header {
  padding: var(--space-5);
  background: linear-gradient(135deg, var(--gray-50) 0%, white 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--gray-100);
}

.project-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.project-content {
  padding: var(--space-6);
  flex: 1;
}

.project-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
  line-height: 1.4;
}

.project-code {
  font-size: 0.8125rem;
  color: var(--gray-500);
  font-weight: 600;
  margin-bottom: var(--space-4);
}

.project-description {
  font-size: 0.9375rem;
  color: var(--gray-600);
  line-height: 1.6;
  margin-bottom: var(--space-6);
}

.budget-summary {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-5);
}

.budget-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.budget-label {
  font-size: 0.75rem;
  color: var(--gray-500);
  font-weight: 600;
  text-transform: uppercase;
}

.budget-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--primary);
}

.budget-divider {
  width: 1px;
  background: var(--gray-200);
}

.progress-container {
  margin-bottom: var(--space-4);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.progress-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 600;
}

.progress-percentage {
  font-size: 0.875rem;
  color: var(--primary);
  font-weight: 700;
}

.progress-bar-bg {
  height: 6px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: var(--gradient-blue);
  border-radius: var(--radius-full);
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.project-actions {
  padding: var(--space-4) var(--space-6);
  background: var(--gray-50);
  border-top: 1px solid var(--gray-100);
  display: flex;
  gap: var(--space-2);
}

.btn-action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-action.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-action.btn-secondary {
  background: white;
  color: var(--gray-700);
  border: 1px solid var(--gray-300);
}

.btn-action.btn-success {
  background: var(--success);
  color: white;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}

@media (max-width: 768px) {
  .projects-view {
    padding: var(--space-4);
  }

  .projects-header {
    flex-direction: column;
  }

  .filters-card {
    grid-template-columns: 1fr;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
