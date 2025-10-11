<template>
  <header class="modern-header">
    <div class="header-container">
      <!-- Logo y Marca -->
      <div class="brand">
        <img src="/logo.png" alt="Logo" class="brand-logo" />
        <span class="brand-name">SIGPP</span>
      </div>

      <!-- Navegación Desktop -->
      <nav v-if="isAuthenticated" class="nav-desktop">
        <router-link v-for="item in menuItems" :key="item.path" :to="item.path" class="nav-link" active-class="active">
          <span class="nav-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- Acciones del Usuario -->
      <div class="header-actions">
        <div v-if="isAuthenticated" class="user-menu">
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role">{{ userRoleFormatted }}</span>
          </div>
          <button @click="logout" class="btn-logout">
            <span>🚪</span>
          </button>
        </div>
      </div>

      <!-- Botón Mobile Menu -->
      <button v-if="isAuthenticated" class="mobile-toggle" @click="toggleMobile">
        <span class="hamburger"></span>
      </button>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide-down">
      <nav v-if="showMobileMenu && isAuthenticated" class="nav-mobile">
        <router-link v-for="item in menuItems" :key="item.path" :to="item.path" class="mobile-link"
          @click="toggleMobile">
          <span>{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
        <button @click="logout" class="mobile-logout">
          <span>🚪</span>
          <span>Cerrar Sesión</span>
        </button>
      </nav>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showMobileMenu = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const userName = computed(() => {
  const name = user.value?.nombre_completo || 'Usuario'
  return name.split(' ').slice(0, 2).join(' ')
})

const userInitials = computed(() => {
  const name = user.value?.nombre_completo || 'U'
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
})

const userRoleFormatted = computed(() => {
  const roles = {
    estudiante: 'Estudiante',
    profesor: 'Profesor',
    financiera: 'Financiera',
    auditor: 'Auditor'
  }
  return roles[user.value?.rol] || ''
})

const menuItems = computed(() => {
  if (!user.value) return []

  const baseItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' }
  ]

  if (user.value.rol === 'estudiante') {
    return [
      ...baseItems,
      { path: '/proyectos', label: 'Proyectos', icon: '📁' },
      { path: '/gastos', label: 'Gastos', icon: '💰' }
    ]
  } else if (user.value.rol === 'profesor') {
    return [
      ...baseItems,
      { path: '/profesor/proyectos', label: 'Proyectos', icon: '📚' }
    ]
  } else if (user.value.rol === 'financiera') {
    return [
      ...baseItems,
      { path: '/financiera/proyectos', label: 'Proyectos', icon: '📋' },
      { path: '/financiera/gastos', label: 'Gastos', icon: '💵' }
    ]
  }

  return baseItems
})

const toggleMobile = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const logout = () => {
  authStore.logout()
  showMobileMenu.value = false
  router.push('/')
}
</script>

<style scoped>
.modern-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--gray-200);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-8);
}

/* Marca */
.brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
}

.brand-logo {
  height: 32px;
  width: 32px;
  object-fit: contain;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  background: var(--gradient-blue);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

/* Navegación Desktop */
.nav-desktop {
  display: flex;
  gap: var(--space-2);
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: var(--gray-600);
  font-weight: 500;
  font-size: 0.9375rem;
  transition: all var(--transition-base);
}

.nav-link:hover {
  background: var(--gray-100);
  color: var(--primary);
}

.nav-link.active {
  background: var(--primary);
  color: white;
  box-shadow: var(--shadow-md);
}

.nav-icon {
  font-size: 1.125rem;
}

/* Usuario */
.user-menu {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--gray-50);
  border-radius: var(--radius-full);
  border: 1px solid var(--gray-200);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--gradient-blue);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-900);
}

.user-role {
  font-size: 0.75rem;
  color: var(--gray-500);
}

.btn-logout {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.btn-logout:hover {
  background: var(--gray-200);
}

/* Mobile */
.mobile-toggle {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
}

.hamburger {
  width: 24px;
  height: 2px;
  background: var(--gray-700);
  display: block;
  position: relative;
}

.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: var(--gray-700);
  left: 0;
}

.hamburger::before {
  top: -7px;
}

.hamburger::after {
  bottom: -7px;
}

.nav-mobile {
  display: none;
}

/* Transiciones */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all var(--transition-base);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 968px) {
  .nav-desktop {
    display: none;
  }

  .user-info {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .nav-mobile {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
    padding: var(--space-4);
    background: white;
    border-top: 1px solid var(--gray-200);
  }

  .mobile-link,
  .mobile-logout {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-lg);
    text-decoration: none;
    color: var(--gray-700);
    font-weight: 500;
    transition: all var(--transition-base);
    background: transparent;
    border: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-size: 1rem;
  }

  .mobile-link:hover,
  .mobile-logout:hover {
    background: var(--gray-100);
  }

  .mobile-logout {
    color: var(--error);
    margin-top: var(--space-4);
    border-top: 1px solid var(--gray-200);
    padding-top: var(--space-4);
  }
}
</style>
