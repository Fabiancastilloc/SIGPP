<template>
  <div class="admin-users">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="container">
      <!-- Header Premium -->
      <div class="page-header">
        <router-link to="/admin" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Panel
        </router-link>
        
        <div class="header-content">
          <div class="header-icon-box">
            <div class="icon-glow"></div>
            <span class="header-icon">👥</span>
          </div>
          <div class="header-text">
            <h1>Gestión de Usuarios</h1>
            <p>Administra todos los usuarios del sistema SIGPP</p>
          </div>
        </div>

        <button @click="openCreateModal" class="btn-gold">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Usuario
        </button>
      </div>

      <!-- Estadísticas Premium -->
      <div class="stats-grid">
        <div class="stat-card card-blue">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">👥</div>
            <div class="stat-glow glow-blue"></div>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">Total Usuarios</div>
          </div>
        </div>

        <div class="stat-card card-green">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">✅</div>
            <div class="stat-glow glow-green"></div>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.activos }}</div>
            <div class="stat-label">Activos</div>
          </div>
        </div>

        <div class="stat-card card-red">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">🚫</div>
            <div class="stat-glow glow-red"></div>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.inactivos }}</div>
            <div class="stat-label">Inactivos</div>
          </div>
        </div>

        <div class="stat-card card-purple">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">🎓</div>
            <div class="stat-glow glow-purple"></div>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.por_rol?.estudiante || 0 }}</div>
            <div class="stat-label">Estudiantes</div>
          </div>
        </div>
      </div>

      <!-- Filtros Premium -->
      <div class="filters-section">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="filters.search" 
            @input="debouncedSearch"
            type="text" 
            placeholder="Buscar por nombre, email o código..."
            class="search-input"
          />
        </div>

        <select v-model="filters.rol" @change="loadUsers" class="filter-select">
          <option value="">📋 Todos los roles</option>
          <option value="estudiante">👨‍🎓 Estudiante</option>
          <option value="profesor">👨‍🏫 Profesor</option>
          <option value="financiera">💼 Financiera</option>
          <option value="auditor">🔍 Auditor</option>
          <option value="superusuario">👑 Administrador</option>
        </select>

        <select v-model="filters.is_active" @change="loadUsers" class="filter-select">
          <option value="">🔘 Todos los estados</option>
          <option value="true">✅ Activos</option>
          <option value="false">🚫 Inactivos</option>
        </select>

        <button @click="resetFilters" class="btn-reset">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Limpiar
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-premium"></div>
        <p>Cargando usuarios...</p>
      </div>

      <!-- Tabla Premium -->
      <div v-else class="table-container">
        <div class="table-header">
          <h3>👥 Lista de Usuarios ({{ pagination.total }})</h3>
        </div>

        <div v-if="users.length === 0" class="empty-state">
          <div class="empty-icon">👥</div>
          <h3>No se encontraron usuarios</h3>
          <p>Intenta ajustar los filtros de búsqueda</p>
        </div>

        <div v-else class="table-wrapper">
          <table class="users-table">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Código</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Registro</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="user in users" 
                :key="user.id" 
                :class="{ 'row-inactive': !user.is_active }"
                class="table-row"
              >
                <td>
                  <div class="user-cell">
                    <div class="avatar" :class="`avatar-${user.rol}`">
                      {{ user.nombre_completo.charAt(0).toUpperCase() }}
                    </div>
                    <div class="user-info">
                      <div class="user-name">{{ user.nombre_completo }}</div>
                      <div class="user-email">{{ user.email }}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="code-badge">{{ user.codigo_institucional }}</span>
                </td>
                <td>
                  <span class="role-badge" :class="`role-${user.rol}`">
                    {{ getRolIcon(user.rol) }} {{ getRolText(user.rol) }}
                  </span>
                </td>
                <td>
                  <span class="status-badge" :class="user.is_active ? 'status-active' : 'status-inactive'">
                    {{ user.is_active ? '✅ Activo' : '🚫 Inactivo' }}
                  </span>
                </td>
                <td>
                  <span class="date-text">{{ formatDate(user.created_at) }}</span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button @click="openEditModal(user)" class="btn-action btn-edit" title="Editar">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="openPasswordModal(user)" class="btn-action btn-key" title="Cambiar contraseña">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                      </svg>
                    </button>
                    <button 
                      @click="toggleUserActive(user)" 
                      class="btn-action btn-toggle" 
                      :title="user.is_active ? 'Desactivar' : 'Activar'"
                    >
                      <svg v-if="user.is_active" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </button>
                    <button @click="confirmDelete(user)" class="btn-action btn-delete" title="Eliminar">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div v-if="pagination.total > pagination.per_page" class="pagination">
          <button 
            @click="changePage(pagination.page - 1)" 
            :disabled="pagination.page === 1" 
            class="btn-page"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Anterior
          </button>
          <span class="page-info">
            Página <strong>{{ pagination.page }}</strong> de <strong>{{ totalPages }}</strong>
            <span class="page-total">({{ pagination.total }} usuarios)</span>
          </span>
          <button 
            @click="changePage(pagination.page + 1)" 
            :disabled="pagination.page >= totalPages" 
            class="btn-page"
          >
            Siguiente
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Crear/Editar Usuario -->
    <div v-if="showUserModal" class="modal-overlay" @click="closeUserModal">
      <div class="modal-box modal-lg" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <span class="modal-icon">{{ editingUser ? '✏️' : '➕' }}</span>
            <h2>{{ editingUser ? 'Editar Usuario' : 'Nuevo Usuario' }}</h2>
          </div>
          <button @click="closeUserModal" class="close-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <form @submit.prevent="saveUser" class="user-form">
            <div class="form-section">
              <h4 class="section-title">📋 Información Básica</h4>
              <div class="form-row">
                <div class="form-field">
                  <label>Código Institucional *</label>
                  <input 
                    v-model="userForm.codigo_institucional" 
                    type="text" 
                    required 
                    placeholder="EST20251001"
                    class="input-premium"
                  />
                </div>
                <div class="form-field">
                  <label>Email Institucional *</label>
                  <input 
                    v-model="userForm.email" 
                    type="email" 
                    required 
                    placeholder="usuario@unicartagena.edu.co"
                    class="input-premium"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-field full-width">
                  <label>Nombre Completo *</label>
                  <input 
                    v-model="userForm.nombre_completo" 
                    type="text" 
                    required 
                    placeholder="Juan Pérez García"
                    class="input-premium"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-field">
                  <label>Rol *</label>
                  <select v-model="userForm.rol" required class="input-premium">
                    <option value="estudiante">👨‍🎓 Estudiante</option>
                    <option value="profesor">👨‍🏫 Profesor</option>
                    <option value="financiera">💼 Financiera</option>
                    <option value="auditor">🔍 Auditor</option>
                    <option value="superusuario">👑 Administrador</option>
                  </select>
                </div>
                <div v-if="editingUser" class="form-field">
                  <label>Estado</label>
                  <select v-model="userForm.is_active" class="input-premium">
                    <option :value="true">✅ Activo</option>
                    <option :value="false">🚫 Inactivo</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="form-section">
              <h4 class="section-title">🎓 Información Académica</h4>
              <div class="form-row">
                <div class="form-field">
                  <label>Sede</label>
                  <select v-model="userForm.sede_id" @change="loadFacultades" class="input-premium">
                    <option :value="null">-- Seleccionar --</option>
                    <option v-for="s in sedes" :key="s.id" :value="s.id">{{ s.nombre }}</option>
                  </select>
                </div>
                <div class="form-field">
                  <label>Facultad</label>
                  <select v-model="userForm.facultad_id" @change="loadCarreras" class="input-premium">
                    <option :value="null">-- Seleccionar --</option>
                    <option v-for="f in facultades" :key="f.id" :value="f.id">{{ f.nombre }}</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-field">
                  <label>Carrera</label>
                  <select v-model="userForm.carrera_id" class="input-premium">
                    <option :value="null">-- Seleccionar --</option>
                    <option v-for="c in carreras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                  </select>
                </div>
                <div class="form-field">
                  <label>Semestre</label>
                  <select v-model="userForm.semestre" class="input-premium">
                    <option :value="null">-- Seleccionar --</option>
                    <option v-for="s in 12" :key="s" :value="s">{{ s }}° Semestre</option>
                  </select>
                </div>
              </div>
            </div>

            <div v-if="!editingUser" class="form-section">
              <h4 class="section-title">🔐 Seguridad</h4>
              <div class="form-row">
                <div class="form-field full-width">
                  <label>Contraseña *</label>
                  <input 
                    v-model="userForm.password" 
                    type="password" 
                    :required="!editingUser" 
                    placeholder="Mínimo 6 caracteres" 
                    minlength="6"
                    class="input-premium"
                  />
                  <small class="form-hint">La contraseña debe tener al menos 6 caracteres</small>
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button @click="closeUserModal" class="btn-modal btn-cancel">
            Cancelar
          </button>
          <button @click="saveUser" class="btn-modal btn-save" :disabled="saving">
            <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            <div v-else class="btn-spinner"></div>
            {{ saving ? 'Guardando...' : (editingUser ? 'Actualizar Usuario' : 'Crear Usuario') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Cambiar Contraseña -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-box" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <span class="modal-icon">🔑</span>
            <h2>Cambiar Contraseña</h2>
          </div>
          <button @click="closePasswordModal" class="close-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <div class="user-info-card">
            <div class="avatar" :class="`avatar-${selectedUser?.rol}`">
              {{ selectedUser?.nombre_completo?.charAt(0).toUpperCase() }}
            </div>
            <div>
              <strong>{{ selectedUser?.nombre_completo }}</strong>
              <p>{{ selectedUser?.email }}</p>
            </div>
          </div>

          <div class="form-field">
            <label>Nueva Contraseña *</label>
            <input 
              v-model="newPassword" 
              type="password" 
              placeholder="Mínimo 6 caracteres" 
              minlength="6"
              class="input-premium"
            />
          </div>

          <div class="form-field">
            <label>Confirmar Contraseña *</label>
            <input 
              v-model="confirmPassword" 
              type="password" 
              placeholder="Repite la contraseña"
              class="input-premium"
            />
          </div>

          <div v-if="newPassword && confirmPassword && newPassword !== confirmPassword" class="alert-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Las contraseñas no coinciden
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closePasswordModal" class="btn-modal btn-cancel">
            Cancelar
          </button>
          <button 
            @click="resetUserPassword" 
            class="btn-modal btn-save" 
            :disabled="saving || !newPassword || newPassword !== confirmPassword"
          >
            <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            <div v-else class="btn-spinner"></div>
            {{ saving ? 'Cambiando...' : 'Cambiar Contraseña' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-box modal-danger" @click.stop>
        <div class="modal-header modal-header-danger">
          <div class="modal-title">
            <span class="modal-icon">⚠️</span>
            <h2>Eliminar Usuario</h2>
          </div>
          <button @click="closeDeleteModal" class="close-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <div class="delete-warning">
            <div class="warning-icon">🗑️</div>
            <h3>¿Estás seguro de eliminar este usuario?</h3>
            
            <div class="user-to-delete">
              <div class="avatar avatar-large" :class="`avatar-${selectedUser?.rol}`">
                {{ selectedUser?.nombre_completo?.charAt(0).toUpperCase() }}
              </div>
              <div>
                <strong>{{ selectedUser?.nombre_completo }}</strong>
                <p>{{ selectedUser?.email }}</p>
                <span class="code-badge">{{ selectedUser?.codigo_institucional }}</span>
              </div>
            </div>

            <div class="alert-danger">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <strong>Esta acción no se puede deshacer.</strong> Todos los datos relacionados con este usuario serán eliminados permanentemente.
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeDeleteModal" class="btn-modal btn-cancel">
            Cancelar
          </button>
          <button @click="deleteUser" class="btn-modal btn-danger" :disabled="deleting">
            <svg v-if="!deleting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <div v-else class="btn-spinner"></div>
            {{ deleting ? 'Eliminando...' : 'Sí, Eliminar Usuario' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import adminUsersApi from '../../api/adminUsers'
import catalogsApi from '../../api/catalogs'

export default {
  name: 'AdminUsers',
  setup() {
    const users = ref([])
    const loading = ref(true)
    const saving = ref(false)
    const deleting = ref(false)
    
    const stats = ref({ total: 0, activos: 0, inactivos: 0, por_rol: {} })
    const filters = ref({ search: '', rol: '', is_active: '' })
    const pagination = ref({ page: 1, per_page: 10, total: 0 })
    
    const sedes = ref([])
    const facultades = ref([])
    const carreras = ref([])
    
    const showUserModal = ref(false)
    const showPasswordModal = ref(false)
    const showDeleteModal = ref(false)
    const editingUser = ref(null)
    const selectedUser = ref(null)
    
    const userForm = ref({
      codigo_institucional: '',
      email: '',
      nombre_completo: '',
      password: '',
      rol: 'estudiante',
      sede_id: null,
      facultad_id: null,
      carrera_id: null,
      semestre: null,
      is_active: true
    })
    
    const newPassword = ref('')
    const confirmPassword = ref('')
    
    const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.per_page))
    
    const loadUsers = async () => {
      loading.value = true
      try {
        const params = { page: pagination.value.page, per_page: pagination.value.per_page, ...filters.value }
        Object.keys(params).forEach(key => { if (params[key] === '') delete params[key] })
        const { data } = await adminUsersApi.getUsers(params)
        users.value = data.users
        pagination.value.total = data.total
      } catch (err) {
        console.error('Error:', err)
        alert('Error al cargar usuarios')
      } finally {
        loading.value = false
      }
    }
    
    const loadStats = async () => {
      try {
        const { data } = await adminUsersApi.getStats()
        stats.value = data
      } catch (err) { console.error('Error:', err) }
    }
    
    const loadSedes = async () => {
      try {
        const { data } = await catalogsApi.getSedes()
        sedes.value = data
      } catch (err) { console.error('Error:', err) }
    }
    
    const loadFacultades = async () => {
      if (!userForm.value.sede_id) { facultades.value = []; return }
      try {
        const { data } = await catalogsApi.getFacultades(userForm.value.sede_id)
        facultades.value = data
      } catch (err) { console.error('Error:', err) }
    }
    
    const loadCarreras = async () => {
      if (!userForm.value.facultad_id) { carreras.value = []; return }
      try {
        const { data } = await catalogsApi.getCarreras(userForm.value.facultad_id)
        carreras.value = data
      } catch (err) { console.error('Error:', err) }
    }
    
    let searchTimeout = null
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => { pagination.value.page = 1; loadUsers() }, 400)
    }
    
    const resetFilters = () => {
      filters.value = { search: '', rol: '', is_active: '' }
      pagination.value.page = 1
      loadUsers()
    }
    
    const changePage = (page) => { pagination.value.page = page; loadUsers() }
    
    const openCreateModal = () => {
      editingUser.value = null
      userForm.value = {
        codigo_institucional: '', email: '', nombre_completo: '', password: '',
        rol: 'estudiante', sede_id: null, facultad_id: null, carrera_id: null, semestre: null, is_active: true
      }
      facultades.value = []
      carreras.value = []
      showUserModal.value = true
    }
    
    const openEditModal = async (user) => {
      editingUser.value = user
      userForm.value = {
        codigo_institucional: user.codigo_institucional,
        email: user.email,
        nombre_completo: user.nombre_completo,
        rol: user.rol,
        sede_id: user.sede_id,
        facultad_id: user.facultad_id,
        carrera_id: user.carrera_id,
        semestre: user.semestre,
        is_active: user.is_active
      }
      if (user.sede_id) await loadFacultades()
      if (user.facultad_id) await loadCarreras()
      showUserModal.value = true
    }
    
    const closeUserModal = () => { showUserModal.value = false; editingUser.value = null }
    
    const saveUser = async () => {
      if (!userForm.value.codigo_institucional || !userForm.value.email || !userForm.value.nombre_completo) {
        alert('Código, email y nombre son requeridos'); return
      }
      if (!editingUser.value && (!userForm.value.password || userForm.value.password.length < 6)) {
        alert('La contraseña debe tener al menos 6 caracteres'); return
      }
      
      saving.value = true
      try {
        if (editingUser.value) {
          const { password, ...updateData } = userForm.value
          await adminUsersApi.updateUser(editingUser.value.id, updateData)
          alert('✅ Usuario actualizado exitosamente')
        } else {
          await adminUsersApi.createUser(userForm.value)
          alert('✅ Usuario creado exitosamente')
        }
        closeUserModal()
        loadUsers()
        loadStats()
      } catch (err) {
        const msg = err.response?.data?.detail || 'Error al guardar el usuario'
        alert(`❌ ${msg}`)
      } finally { saving.value = false }
    }
    
    const openPasswordModal = (user) => {
      selectedUser.value = user
      newPassword.value = ''
      confirmPassword.value = ''
      showPasswordModal.value = true
    }
    
    const closePasswordModal = () => { showPasswordModal.value = false; selectedUser.value = null }
    
    const resetUserPassword = async () => {
      if (newPassword.value !== confirmPassword.value) { alert('Las contraseñas no coinciden'); return }
      if (newPassword.value.length < 6) { alert('La contraseña debe tener al menos 6 caracteres'); return }
      
      saving.value = true
      try {
        await adminUsersApi.resetPassword(selectedUser.value.id, newPassword.value)
        alert('✅ Contraseña actualizada exitosamente')
        closePasswordModal()
      } catch (err) { 
        alert('❌ Error al cambiar la contraseña') 
      } finally { 
        saving.value = false 
      }
    }
    
    const toggleUserActive = async (user) => {
      const action = user.is_active ? 'desactivar' : 'activar'
      if (!confirm(`¿${action.charAt(0).toUpperCase() + action.slice(1)} a ${user.nombre_completo}?`)) return
      try {
        await adminUsersApi.toggleActive(user.id)
        alert(`✅ Usuario ${action === 'activar' ? 'activado' : 'desactivado'} exitosamente`)
        loadUsers()
        loadStats()
      } catch (err) {
        const msg = err.response?.data?.detail || 'Error al cambiar el estado'
        alert(`❌ ${msg}`)
      }
    }
    
    const confirmDelete = (user) => { selectedUser.value = user; showDeleteModal.value = true }
    const closeDeleteModal = () => { showDeleteModal.value = false; selectedUser.value = null }
    
    const deleteUser = async () => {
      deleting.value = true
      try {
        await adminUsersApi.deleteUser(selectedUser.value.id)
        alert('✅ Usuario eliminado exitosamente')
        closeDeleteModal()
        loadUsers()
        loadStats()
      } catch (err) {
        const msg = err.response?.data?.detail || 'Error al eliminar el usuario'
        alert(`❌ ${msg}`)
      } finally { deleting.value = false }
    }
    
    const getRolIcon = (rol) => ({ estudiante: '👨‍🎓', profesor: '👨‍🏫', financiera: '💼', auditor: '🔍', superusuario: '👑' }[rol] || '👤')
    const getRolText = (rol) => ({ estudiante: 'Estudiante', profesor: 'Profesor', financiera: 'Financiera', auditor: 'Auditor', superusuario: 'Admin' }[rol] || rol)
    const formatDate = (date) => new Date(date).toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric' })
    
    onMounted(() => { loadUsers(); loadStats(); loadSedes() })
    
    return {
      users, loading, saving, deleting, stats, filters, pagination, totalPages,
      sedes, facultades, carreras,
      showUserModal, showPasswordModal, showDeleteModal, editingUser, selectedUser,
      userForm, newPassword, confirmPassword,
      loadUsers, loadFacultades, loadCarreras, debouncedSearch, resetFilters, changePage,
      openCreateModal, openEditModal, closeUserModal, saveUser,
      openPasswordModal, closePasswordModal, resetUserPassword,
      toggleUserActive, confirmDelete, closeDeleteModal, deleteUser,
      getRolIcon, getRolText, formatDate
    }
  }
}
</script>

<style scoped>
/* BASE */
.admin-users {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  padding: 32px 16px;
  position: relative;
}

/* ANIMATED BACKGROUND */
.dashboard-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
  animation: float 25s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  top: -300px;
  right: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -250px;
  left: -250px;
  animation-delay: -12s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -6s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-50px, 50px) scale(0.9); }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER PREMIUM */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 32px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.3s;
}

.btn-back:hover {
  background: #334155;
  border-color: #3b82f6;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 1;
  justify-content: center;
}

.header-icon-box {
  position: relative;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-glow {
  position: absolute;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border-radius: 50%;
  filter: blur(20px);
  opacity: 0.5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.3; }
}

.header-icon {
  position: relative;
  z-index: 2;
  font-size: 48px;
  filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.6));
}

.header-text h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 6px;
}

.header-text p {
  color: #cbd5e1;
  font-size: 16px;
  font-weight: 600;
}

.btn-gold {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  border: none;
  border-radius: 12px;
  font-weight: 800;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}

.btn-gold:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(245, 158, 11, 0.6);
}

.btn-gold svg {
  width: 20px;
  height: 20px;
}

/* STATS PREMIUM */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: #1e293b;
  padding: 28px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 2px solid #334155;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: currentColor;
  transition: width 0.3s;
}

.stat-card:hover::before {
  width: 8px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.card-blue { color: #3b82f6; }
.card-green { color: #10b981; }
.card-red { color: #ef4444; }
.card-purple { color: #8b5cf6; }

.stat-icon-wrapper {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-glow {
  position: absolute;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  filter: blur(15px);
  opacity: 0.3;
}

.glow-blue { background: #3b82f6; }
.glow-green { background: #10b981; }
.glow-red { background: #ef4444; }
.glow-purple { background: #8b5cf6; }

.stat-icon {
  position: relative;
  z-index: 2;
  font-size: 38px;
  filter: drop-shadow(0 2px 8px currentColor);
}

.stat-value {
  font-size: 36px;
  font-weight: 900;
  color: white;
  line-height: 1;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* FILTERS PREMIUM */
.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 32px;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 300px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #ffffff;
  font-weight: 600;
  font-size: 15px;
}

.search-input::placeholder {
  color: #64748b;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.filter-select {
  min-width: 200px;
  padding: 14px 20px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.btn-reset {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reset:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: #f59e0b;
  color: #f59e0b;
}

.btn-reset svg {
  width: 18px;
  height: 18px;
}

/* TABLE CONTAINER */
.table-container {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.table-header {
  padding: 24px 28px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid #334155;
}

.table-header h3 {
  font-size: 20px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-wrapper {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: rgba(15, 23, 42, 0.8);
}

.users-table th {
  padding: 16px 20px;
  text-align: left;
  font-weight: 800;
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}

.users-table tbody tr {
  border-bottom: 1px solid #334155;
  transition: all 0.3s;
}

.users-table tbody tr:hover {
  background: rgba(59, 130, 246, 0.05);
}

.users-table tbody tr.row-inactive {
  opacity: 0.5;
  background: rgba(239, 68, 68, 0.03);
}

.users-table td {
  padding: 20px;
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

/* USER CELL */
.user-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 900;
  font-size: 18px;
  flex-shrink: 0;
}

.avatar-estudiante { background: linear-gradient(135deg, #3b82f6, #1e40af); }
.avatar-profesor { background: linear-gradient(135deg, #10b981, #059669); }
.avatar-financiera { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
.avatar-auditor { background: linear-gradient(135deg, #f59e0b, #d97706); }
.avatar-superusuario { background: linear-gradient(135deg, #ef4444, #dc2626); }

.avatar-large {
  width: 60px;
  height: 60px;
  font-size: 24px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 700;
  color: #f1f5f9;
  font-size: 15px;
  margin-bottom: 4px;
}

.user-email {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

/* BADGES */
.code-badge {
  font-family: 'Courier New', monospace;
  color: #3b82f6;
  font-weight: 800;
  font-size: 13px;
  background: rgba(59, 130, 246, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-block;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.role-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.role-estudiante {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.role-profesor {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.role-financiera {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.role-auditor {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.role-superusuario {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.status-active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-inactive {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.date-text {
  color: #94a3b8;
  font-size: 13px;
  font-weight: 600;
}

/* ACTION BUTTONS */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-action {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
}

.btn-action svg {
  width: 18px;
  height: 18px;
}

.btn-edit {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.btn-edit:hover {
  background: rgba(59, 130, 246, 0.25);
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.btn-key {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.btn-key:hover {
  background: rgba(245, 158, 11, 0.25);
  border-color: #f59e0b;
  transform: translateY(-2px);
}

.btn-toggle {
  background: rgba(139, 92, 246, 0.15);
  color: #8b5cf6;
}

.btn-toggle:hover {
  background: rgba(139, 92, 246, 0.25);
  border-color: #8b5cf6;
  transform: translateY(-2px);
}

.btn-delete {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.25);
  border-color: #ef4444;
  transform: translateY(-2px);
}

/* PAGINATION */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-top: 2px solid #334155;
  background: rgba(15, 23, 42, 0.5);
}

.btn-page {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-page:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-page:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn-page svg {
  width: 16px;
  height: 16px;
}

.page-info {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

.page-info strong {
  color: #3b82f6;
  font-weight: 900;
}

.page-total {
  color: #94a3b8;
  margin-left: 8px;
}

/* MODALS */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(8px);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-box {
  background: #1e293b;
  border-radius: 24px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5);
  border: 2px solid #334155;
  animation: slideUp 0.3s ease;
}

.modal-lg {
  max-width: 800px;
}

.modal-danger {
  border-color: rgba(239, 68, 68, 0.5);
}

@keyframes slideUp {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  padding: 28px 32px;
  border-bottom: 2px solid #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 23, 42, 0.5);
}

.modal-header-danger {
  background: rgba(239, 68, 68, 0.1);
  border-bottom-color: rgba(239, 68, 68, 0.3);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  font-size: 32px;
  filter: drop-shadow(0 2px 8px currentColor);
}

.modal-title h2 {
  font-size: 22px;
  font-weight: 900;
  color: #f1f5f9;
  margin: 0;
}

.close-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #334155;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  color: #ef4444;
  transform: rotate(90deg);
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

.modal-content {
  padding: 32px;
}

/* FORM */
.user-form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 800;
  color: #3b82f6;
  margin: 0 0 12px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-field.full-width {
  grid-column: span 2;
}

.form-field label {
  font-weight: 700;
  font-size: 13px;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-premium {
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.input-premium::placeholder {
  color: #64748b;
}

.input-premium:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
  background: rgba(15, 23, 42, 0.8);
}

.form-hint {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

/* USER INFO CARD */
.user-info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid #334155;
  border-radius: 12px;
  margin-bottom: 24px;
}

.user-info-card strong {
  display: block;
  font-size: 17px;
  color: #f1f5f9;
  font-weight: 800;
  margin-bottom: 4px;
}

.user-info-card p {
  margin: 0;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
}

/* ALERTS */
.alert-error {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: rgba(239, 68, 68, 0.15);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: #ef4444;
  font-size: 14px;
  font-weight: 700;
}

.alert-error svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.alert-danger {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(239, 68, 68, 0.15);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.6;
  margin-top: 20px;
}

.alert-danger svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  margin-top: 2px;
}

.alert-danger strong {
  font-weight: 900;
}

/* DELETE WARNING */
.delete-warning {
  text-align: center;
  padding: 20px;
}

.warning-icon {
  font-size: 80px;
  margin-bottom: 20px;
  filter: drop-shadow(0 4px 12px rgba(239, 68, 68, 0.5));
}

.delete-warning h3 {
  font-size: 22px;
  color: #f1f5f9;
  font-weight: 900;
  margin-bottom: 24px;
}

.user-to-delete {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid #334155;
  border-radius: 16px;
  margin-bottom: 20px;
  text-align: left;
}

.user-to-delete strong {
  display: block;
  font-size: 18px;
  color: #f1f5f9;
  font-weight: 800;
  margin-bottom: 6px;
}

.user-to-delete p {
  margin: 0 0 8px 0;
  color: #94a3b8;
  font-size: 14px;
}

/* MODAL FOOTER */
.modal-footer {
  padding: 24px 32px;
  border-top: 2px solid #334155;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  background: rgba(15, 23, 42, 0.5);
}

.btn-modal {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid transparent;
  border-radius: 10px;
  font-weight: 800;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-modal svg {
  width: 18px;
  height: 18px;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.05);
  border-color: #334155;
  color: #cbd5e1;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: #64748b;
}

.btn-save {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: white;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
}

.btn-modal:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* LOADING & EMPTY */
.loading-state,
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.spinner-premium {
  width: 70px;
  height: 70px;
  border: 5px solid #334155;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p,
.empty-state p {
  color: #94a3b8;
  font-size: 16px;
  font-weight: 600;
}

.empty-icon {
  font-size: 100px;
  margin-bottom: 24px;
  opacity: 0.3;
}

.empty-state h3 {
  font-size: 24px;
  color: #f1f5f9;
  font-weight: 900;
  margin-bottom: 12px;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-content {
    justify-content: flex-start;
  }

  .filters-section {
    flex-direction: column;
  }

  .search-box,
  .filter-select {
    width: 100%;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .users-table {
    min-width: 900px;
  }

  .pagination {
    flex-direction: column;
    gap: 16px;
  }
}

/* SCROLLBAR */
.modal-box::-webkit-scrollbar {
  width: 8px;
}

.modal-box::-webkit-scrollbar-track {
  background: #0f172a;
}

.modal-box::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 4px;
}

.modal-box::-webkit-scrollbar-thumb:hover {
  background: #475569;
}
</style>
