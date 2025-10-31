<template>
  <div class="admin-projects-page">
    <div class="container">
      <div class="page-header">
        <h1>📊 Gestión de Proyectos</h1>
        <router-link to="/admin" class="btn-back">← Volver</router-link>
      </div>

      <div class="filters-bar">
        <input v-model="searchQuery" type="text" placeholder="🔍 Buscar..." class="search-input" />
        <select v-model="filterStatus" class="filter-select">
          <option value="">Todos los estados</option>
          <option value="borrador">Borrador</option>
          <option value="pendiente_profesor">Pendiente Profesor</option>
          <option value="pendiente_financiera">Pendiente Financiera</option>
          <option value="activo">Activo</option>
          <option value="rechazado">Rechazado</option>
        </select>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
      </div>

      <div v-else class="projects-table">
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Estudiante</th>
              <th>Profesor</th>
              <th>Estado</th>
              <th>Presupuesto</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in filteredProjects" :key="project.id">
              <td>{{ project.codigo_proyecto }}</td>
              <td>{{ project.nombre }}</td>
              <td>{{ project.estudiante.nombre }}</td>
              <td>{{ project.profesor.nombre }}</td>
              <td><span :class="['badge', getStatusClass(project.estado)]">{{ getStatusText(project.estado) }}</span></td>
              <td>${{ formatMoney(project.presupuesto_estimado) }}</td>
              <td>
                <button @click="viewProject(project.id)" class="btn-sm btn-view">Ver</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import projectsApi from '../../api/projects'

export default {
  name: 'AdminProjects',
  setup() {
    const router = useRouter()
    const projects = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const filterStatus = ref('')
    
    const filteredProjects = computed(() => {
      let filtered = projects.value
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo_proyecto.toLowerCase().includes(query)
        )
      }
      if (filterStatus.value) {
        filtered = filtered.filter(p => p.estado === filterStatus.value)
      }
      return filtered
    })
    
    const loadProjects = async () => {
      loading.value = true
      try {
        const response = await projectsApi.getProjects()
        projects.value = response.data
      } catch (err) {
        console.error('Error:', err)
      } finally {
        loading.value = false
      }
    }
    
    const viewProject = (id) => router.push(`/admin/project/${id}`)
    const getStatusClass = (estado) => `status-${estado}`
    const getStatusText = (estado) => estado
    const formatMoney = (val) => new Intl.NumberFormat('es-CO').format(val)
    
    onMounted(() => loadProjects())
    
    return { projects, loading, searchQuery, filterStatus, filteredProjects, viewProject, getStatusClass, getStatusText, formatMoney }
  }
}
</script>

<style scoped>
.admin-projects-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.btn-back {
  padding: 10px 20px;
  background: white;
  border-radius: 8px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  border: 2px solid var(--gray-200);
}

.filters-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input, .filter-select {
  padding: 10px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 8px;
  font-size: 14px;
}

.search-input { flex: 1; }

.projects-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: var(--gray-100);
  padding: 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

td {
  padding: 16px;
  border-top: 1px solid var(--gray-200);
  font-size: 14px;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.btn-sm {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.btn-view {
  background: var(--gray-200);
  color: var(--gray-700);
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid var(--gray-200);
  border-top-color: #ef4444;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
