<template>
  <div class="admin-users-page">
    <div class="container">
      <div class="page-header">
        <h1>👥 Gestión de Usuarios</h1>
        <router-link to="/admin" class="btn-back">← Volver</router-link>
      </div>

      <div class="filters-bar">
        <input v-model="searchQuery" type="text" placeholder="🔍 Buscar..." class="search-input" />
        <select v-model="filterRole" class="filter-select">
          <option value="">Todos los roles</option>
          <option value="estudiante">Estudiantes</option>
          <option value="profesor">Profesores</option>
          <option value="financiera">Financiera</option>
          <option value="auditor">Auditores</option>
          <option value="superusuario">Administradores</option>
        </select>
      </div>

      <div class="users-grid">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
          <div class="user-avatar">{{ getInitials(user.nombre_completo) }}</div>
          <div class="user-info">
            <h3>{{ user.nombre_completo }}</h3>
            <p>{{ user.email }}</p>
            <span :class="['role-badge', getRoleClass(user.rol)]">{{ getRoleText(user.rol) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'AdminUsers',
  setup() {
    const users = ref([
      { id: 1, nombre_completo: 'Juan Pérez', email: 'juan@test.com', rol: 'estudiante' },
      { id: 2, nombre_completo: 'María García', email: 'maria@test.com', rol: 'profesor' }
    ])
    const searchQuery = ref('')
    const filterRole = ref('')
    
    const filteredUsers = computed(() => {
      let filtered = users.value
      if (searchQuery.value) {
        filtered = filtered.filter(u => u.nombre_completo.toLowerCase().includes(searchQuery.value.toLowerCase()))
      }
      if (filterRole.value) {
        filtered = filtered.filter(u => u.rol === filterRole.value)
      }
      return filtered
    })
    
    const getInitials = (name) => name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    const getRoleClass = (rol) => `role-${rol}`
    const getRoleText = (rol) => rol
    
    return { users, searchQuery, filterRole, filteredUsers, getInitials, getRoleClass, getRoleText }
  }
}
</script>

<style scoped>
.admin-users-page {
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
  margin-bottom: 32px;
}

.search-input, .filter-select {
  padding: 10px 16px;
  border: 2px solid var(--gray-300);
  border-radius: 8px;
}

.search-input { flex: 1; }

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.user-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 20px;
}

.user-info h3 {
  margin: 0 0 4px;
  font-size: 16px;
}

.user-info p {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--gray-600);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}
</style>
