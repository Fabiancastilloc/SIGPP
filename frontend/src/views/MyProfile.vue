<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <div class="profile-avatar-large">
          {{ getInitials(user.nombre_completo) }}
        </div>
        <div class="profile-title">
          <h1>{{ user.nombre_completo }}</h1>
          <p class="role-badge" :class="getRoleClass(user.rol)">
            {{ getRoleText(user.rol) }}
          </p>
        </div>
      </div>

      <div class="profile-grid">
        <!-- Información Personal -->
        <div class="profile-card">
          <h3>👤 Información Personal</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="label">Código Institucional:</span>
              <span class="value">{{ user.codigo_institucional }}</span>
            </div>
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="label">Rol:</span>
              <span class="value">{{ getRoleText(user.rol) }}</span>
            </div>
          </div>
        </div>

        <!-- Información Académica -->
        <div v-if="user.rol === 'estudiante'" class="profile-card">
          <h3>🎓 Información Académica</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="label">Sede:</span>
              <span class="value">{{ sede?.nombre || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Facultad:</span>
              <span class="value">{{ facultad?.nombre || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Carrera:</span>
              <span class="value">{{ carrera?.nombre || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Semestre:</span>
              <span class="value">{{ user.semestre || 'N/A' }}</span>
            </div>
          </div>
        </div>

        <!-- Acciones -->
        <div class="profile-card">
          <h3>⚙️ Acciones</h3>
          <div class="actions-list">
            <button @click="goToDashboard" class="btn-action primary">
              <span class="icon">🏠</span>
              <span>Ir al Dashboard</span>
            </button>
            <button @click="logout" class="btn-action danger">
              <span class="icon">🚪</span>
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'
import catalogsApi from '../api/catalogs'

export default {
  name: 'MyProfile',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const sede = ref(null)
    const facultad = ref(null)
    const carrera = ref(null)
    
    const user = computed(() => authStore.user)
    
    const loadAcademicInfo = async () => {
      if (user.value.rol !== 'estudiante') return
      
      try {
        const [sedesRes, facultadesRes, carrerasRes] = await Promise.all([
          catalogsApi.getSedes(),
          catalogsApi.getFacultades(),
          catalogsApi.getCarreras()
        ])
        
        sede.value = sedesRes.data.find(s => s.id === user.value.sede_id)
        facultad.value = facultadesRes.data.find(f => f.id === user.value.facultad_id)
        carrera.value = carrerasRes.data.find(c => c.id === user.value.carrera_id)
      } catch (err) {
        console.error('Error:', err)
      }
    }
    
    const goToDashboard = () => {
      const routes = {
        'estudiante': '/student',
        'profesor': '/professor',
        'financiera': '/finance',
        'auditor': '/auditor',
        'superusuario': '/admin'
      }
      router.push(routes[user.value.rol] || '/')
    }
    
    const logout = () => {
      if (confirm('¿Cerrar sesión?')) {
        authStore.logout()
        router.push('/login')
      }
    }
    
    const getInitials = (name) => {
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    const getRoleClass = (rol) => {
      const classes = {
        'estudiante': 'role-student',
        'profesor': 'role-professor',
        'financiera': 'role-finance',
        'auditor': 'role-auditor',
        'superusuario': 'role-admin'
      }
      return classes[rol] || ''
    }
    
    const getRoleText = (rol) => {
      const texts = {
        'estudiante': '👨‍🎓 Estudiante',
        'profesor': '👨‍🏫 Profesor',
        'financiera': '💼 Financiera',
        'auditor': '🔍 Auditor',
        'superusuario': '👑 Administrador'
      }
      return texts[rol] || rol
    }
    
    onMounted(() => loadAcademicInfo())
    
    return {
      user, sede, facultad, carrera,
      goToDashboard, logout, getInitials, getRoleClass, getRoleText
    }
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.profile-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48px;
  font-weight: 700;
  margin: 0 auto 20px;
}

.profile-title h1 {
  font-size: 32px;
  margin-bottom: 12px;
}

.role-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 14px;
}

.role-student { background: #dbeafe; color: #1e40af; }
.role-professor { background: #d1fae5; color: #065f46; }
.role-finance { background: #e0e7ff; color: #3730a3; }
.role-auditor { background: #fef3c7; color: #92400e; }
.role-admin { background: #fee2e2; color: #991b1b; }

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.profile-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 2px solid var(--gray-200);
}

.profile-card h3 {
  font-size: 20px;
  margin-bottom: 24px;
  color: var(--gray-900);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: var(--gray-50);
  border-radius: 10px;
}

.info-row .label {
  font-weight: 600;
  color: var(--gray-600);
  font-size: 14px;
}

.info-row .value {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 14px;
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 15px;
}

.btn-action .icon {
  font-size: 20px;
}

.btn-action.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-action.danger {
  background: #fee2e2;
  color: #991b1b;
  border: 2px solid #ef4444;
}

.btn-action:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}
</style>
