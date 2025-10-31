<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Logo y Título -->
      <router-link to="/" class="navbar-brand">
        <img src="../assets/logo.png" alt="UdC Logo" class="logo" />
        <div class="brand-text">
          <span class="brand-title">SIGPP</span>
          <span class="brand-subtitle">Universidad de Cartagena</span>
        </div>
      </router-link>

      <!-- Menu Toggle (Mobile) -->
      <button @click="toggleMenu" class="menu-toggle">
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- Navigation Links -->
      <div :class="['navbar-menu', { active: isMenuOpen }]">
        <!-- Links públicos (sin login) -->
        <template v-if="!isAuthenticated">
          <router-link to="/" class="nav-link">
            <span class="icon">🏠</span>
            Inicio
          </router-link>
          <router-link to="/login" class="nav-link">
            <span class="icon">🔐</span>
            Iniciar Sesión
          </router-link>
          <router-link to="/register" class="nav-link-primary">
            <span class="icon">📝</span>
            Registrarse
          </router-link>
        </template>

        <!-- Links con autenticación -->
        <template v-else>
          <router-link :to="getDashboardRoute()" class="nav-link">
            <span class="icon">📊</span>
            Dashboard
          </router-link>
          
          <router-link to="/profile" class="nav-link">
            <span class="icon">👤</span>
            Mi Perfil
          </router-link>

          <!-- Dropdown de Usuario -->
          <div class="user-dropdown" @click="toggleDropdown">
            <div class="user-avatar">
              {{ getInitials(user.nombre_completo) }}
            </div>
            <div class="user-info">
              <span class="user-name">{{ getFirstName(user.nombre_completo) }}</span>
              <span class="user-role">{{ getRoleText(user.rol) }}</span>
            </div>
            <span class="dropdown-arrow">▼</span>

            <!-- Dropdown Menu -->
            <div :class="['dropdown-menu', { active: isDropdownOpen }]">
              <div class="dropdown-header">
                <div class="dropdown-avatar">{{ getInitials(user.nombre_completo) }}</div>
                <div class="dropdown-user-info">
                  <strong>{{ user.nombre_completo }}</strong>
                  <span>{{ user.email }}</span>
                </div>
              </div>
              
              <div class="dropdown-divider"></div>
              
              <router-link :to="getDashboardRoute()" class="dropdown-item" @click="closeDropdown">
                <span class="icon">📊</span>
                Dashboard
              </router-link>
              
              <router-link to="/profile" class="dropdown-item" @click="closeDropdown">
                <span class="icon">👤</span>
                Mi Perfil
              </router-link>
              
              <div class="dropdown-divider"></div>
              
              <button @click="handleLogout" class="dropdown-item logout">
                <span class="icon">🚪</span>
                Cerrar Sesión
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const isMenuOpen = ref(false)
    const isDropdownOpen = ref(false)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)
    
    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value
    }
    
    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }
    
    const closeDropdown = () => {
      isDropdownOpen.value = false
      isMenuOpen.value = false
    }
    
    const getDashboardRoute = () => {
      const routes = {
        'estudiante': '/student',
        'profesor': '/professor',
        'financiera': '/finance',
        'auditor': '/auditor',
        'superusuario': '/admin'
      }
      return routes[user.value?.rol] || '/'
    }
    
    const handleLogout = () => {
      if (confirm('¿Cerrar sesión?')) {
        authStore.logout()
        closeDropdown()
        router.push('/login')
      }
    }
    
    const getInitials = (name) => {
      return name?.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || '??'
    }
    
    const getFirstName = (name) => {
      return name?.split(' ')[0] || ''
    }
    
    const getRoleText = (rol) => {
      const texts = {
        'estudiante': 'Estudiante',
        'profesor': 'Profesor',
        'financiera': 'Financiera',
        'auditor': 'Auditor',
        'superusuario': 'Admin'
      }
      return texts[rol] || rol
    }
    
    return {
      isMenuOpen,
      isDropdownOpen,
      isAuthenticated,
      user,
      toggleMenu,
      toggleDropdown,
      closeDropdown,
      getDashboardRoute,
      handleLogout,
      getInitials,
      getFirstName,
      getRoleText
    }
  }
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: linear-gradient(135deg, #7541ee 0%, #1e40af 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  transition: transform 0.3s;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.logo {
  height: 50px;
  width: auto;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-title {
  font-size: 24px;
  font-weight: 800;
  color: white;
  letter-spacing: -0.5px;
}

.brand-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.menu-toggle span {
  display: block;
  width: 25px;
  height: 3px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  transition: all 0.3s;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.nav-link-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: white;
  color: #1e40af;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
  border-radius: 8px;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.nav-link-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.icon {
  font-size: 16px;
}

.user-dropdown {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
  margin-left: 12px;
}

.user-dropdown:hover {
  background: rgba(255, 255, 255, 0.25);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  color: white;
  font-weight: 700;
  font-size: 14px;
}

.user-role {
  color: rgba(255, 255, 255, 0.8);
  font-size: 11px;
  font-weight: 600;
}

.dropdown-arrow {
  color: white;
  font-size: 10px;
  transition: transform 0.3s;
}

.user-dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  min-width: 280px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s;
  overflow: hidden;
}

.dropdown-menu.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-header {
  padding: 20px;
  background: linear-gradient(135deg, #1e3a8a, #1e40af);
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
}

.dropdown-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
}

.dropdown-user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dropdown-user-info strong {
  font-size: 15px;
}

.dropdown-user-info span {
  font-size: 12px;
  opacity: 0.9;
}

.dropdown-divider {
  height: 1px;
  background: var(--gray-200);
  margin: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: var(--gray-700);
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dropdown-item:hover {
  background: var(--gray-50);
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout:hover {
  background: #fee2e2;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
  }

  .navbar-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #1e3a8a, #1e40af);
    flex-direction: column;
    padding: 20px;
    gap: 12px;
    transform: translateX(-100%);
    transition: transform 0.3s;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .navbar-menu.active {
    transform: translateX(0);
  }

  .user-dropdown {
    width: 100%;
    justify-content: space-between;
    margin-left: 0;
  }

  .brand-subtitle {
    display: none;
  }
}
</style>
