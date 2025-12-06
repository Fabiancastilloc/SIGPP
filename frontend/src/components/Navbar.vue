<!-- frontend/src/components/Navbar.vue -->
<template>
  <nav class="premium-navbar" :class="{ 'scrolled': isScrolled, 'mobile-active': mobileOpen }">
    <!-- Animated Background Effects -->
    <div class="navbar-glow"></div>
    
    <div class="nav-container">
      <!-- Premium Logo Section -->
      <router-link :to="homeRoute" class="logo-section" @click="closeMobile">
        <div class="logo-circle">
          <img src="../assets/logo.png" alt="SIGPP" class="logo-img" />
          <div class="logo-ring"></div>
        </div>
        <div class="logo-content">
          <span class="logo-title">SIGPP</span>
          <span class="logo-subtitle">Universidad de Cartagena</span>
        </div>
      </router-link>

      <!-- Mobile Toggle -->
      <button @click="toggleMobile" class="mobile-toggle" :class="{ active: mobileOpen }" aria-label="Menu">
        <span class="toggle-line"></span>
        <span class="toggle-line"></span>
        <span class="toggle-line"></span>
      </button>

      <!-- Navigation Menu -->
      <div class="nav-menu" :class="{ 'mobile-open': mobileOpen }">
        <!-- Navigation Links -->
        <div class="nav-links">
          <!-- Estudiante -->
          <router-link 
            v-if="userRole === 'estudiante'" 
            to="/student/" 
            class="nav-link" 
            @click="closeMobile"
          >
            <div class="link-icon-wrapper">
              <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <span class="link-text">Mis Proyectos</span>
          </router-link>

          <!-- Profesor -->
          <router-link 
            v-if="userRole === 'profesor'" 
            to="/professor/" 
            class="nav-link" 
            @click="closeMobile"
          >
            <div class="link-icon-wrapper">
              <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <span class="link-text">Gestión Académica</span>
          </router-link>

          <!-- Financiera -->
          <router-link 
            v-if="userRole === 'financiera'" 
            to="/finance/" 
            class="nav-link" 
            @click="closeMobile"
          >
            <div class="link-icon-wrapper">
              <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="link-text">Finanzas</span>
          </router-link>

          <!-- Auditor -->
          <router-link 
            v-if="userRole === 'auditor'" 
            to="/auditor/" 
            class="nav-link" 
            @click="closeMobile"
          >
            <div class="link-icon-wrapper">
              <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="link-text">Auditoría</span>
          </router-link>

          <!-- Admin -->
          <router-link 
            v-if="userRole === 'superusuario'" 
            to="/admin" 
            class="nav-link" 
            @click="closeMobile"
          >
            <div class="link-icon-wrapper">
              <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <span class="link-text">Panel General</span>
          </router-link>
        </div>

        <!-- User Section / Auth Buttons -->
        <div v-if="isAuthenticated" class="user-section">
          <div class="user-badge-wrapper" @click="toggleDropdown" :class="{ active: dropdownOpen }">
            <div class="user-badge">
              <div class="user-avatar">
                <span class="avatar-initial">{{ userInitial }}</span>
                <div class="avatar-ring"></div>
              </div>
              <div class="user-info">
                <span class="user-name">{{ userFirstName }}</span>
                <span class="user-role">{{ getRoleDisplay(userRole) }}</span>
              </div>
              <svg class="chevron-icon" :class="{ rotate: dropdownOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <!-- Dropdown Menu -->
          <transition name="dropdown-fade">
            <div v-if="dropdownOpen" class="dropdown-menu">
              <div class="dropdown-header">
                <div class="dropdown-avatar">
                  <span>{{ userInitial }}</span>
                </div>
                <div class="dropdown-info">
                  <h4>{{ userName }}</h4>
                  <p>{{ userEmail }}</p>
                  <span class="role-tag">{{ getRoleDisplay(userRole) }}</span>
                </div>
              </div>
              
              <div class="dropdown-divider"></div>
              
              <div class="dropdown-body">
                <router-link to="/profile" class="dropdown-item" @click="closeDropdown">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>Mi Perfil</span>
                </router-link>
                
                <button @click="handleLogout" class="dropdown-item logout-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>Cerrar Sesión</span>
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Auth Buttons (Not Logged In) -->
        <div v-else class="auth-section">
          <router-link to="/login" class="auth-btn login-btn" @click="closeMobile">
            Iniciar Sesión
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const dropdownOpen = ref(false)
    const mobileOpen = ref(false)
    const isScrolled = ref(false)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const userName = computed(() => authStore.user?.nombre_completo || 'Invitado')
    const userEmail = computed(() => authStore.user?.email || '')
    const userRole = computed(() => authStore.user?.rol || '')
    
    const userInitial = computed(() => userName.value.charAt(0).toUpperCase())
    const userFirstName = computed(() => userName.value.split(' ')[0])

    const homeRoute = computed(() => {
      if (!isAuthenticated.value) return '/'
      
      const routes = {
        'estudiante': '/student/',
        'profesor': '/professor/',
        'financiera': '/finance/',
        'auditor': '/auditor/',
        'superusuario': '/admin'
      }
      return routes[userRole.value] || '/'
    })
    
    const toggleDropdown = () => {
      dropdownOpen.value = !dropdownOpen.value
    }
    
    const closeDropdown = () => {
      dropdownOpen.value = false
      mobileOpen.value = false
    }
    
    const toggleMobile = () => {
      mobileOpen.value = !mobileOpen.value
    }
    
    const closeMobile = () => {
      mobileOpen.value = false
      dropdownOpen.value = false
    }
    
    const handleLogout = () => {
      authStore.logout()
      closeDropdown()
      router.push('/login')
    }
    
    const getRoleDisplay = (role) => {
      const roles = {
        'estudiante': 'Estudiante',
        'profesor': 'Docente',
        'financiera': 'Financiera',
        'auditor': 'Auditor',
        'superusuario': 'Administrador'
      }
      return roles[role] || role
    }
    
    const handleScroll = () => {
      isScrolled.value = window.scrollY > 20
    }
    
    const handleClickOutside = (e) => {
      if (!e.target.closest('.user-section')) {
        dropdownOpen.value = false
      }
    }
    
    onMounted(() => {
      window.addEventListener('scroll', handleScroll)
      document.addEventListener('click', handleClickOutside)
    })
    
    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      dropdownOpen,
      mobileOpen,
      isScrolled,
      isAuthenticated,
      userName,
      userEmail,
      userRole,
      userInitial,
      userFirstName,
      homeRoute,
      toggleDropdown,
      closeDropdown,
      toggleMobile,
      closeMobile,
      handleLogout,
      getRoleDisplay
    }
  }
}
</script>

<style scoped>
/* BASE */
.premium-navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #0f172a;
  border-bottom: 1px solid rgba(51, 65, 85, 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  height: 80px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.premium-navbar.scrolled {
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(20px);
  height: 70px;
  border-bottom: 1px solid rgba(245, 158, 11, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* ANIMATED BACKGROUND */
.navbar-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(245, 158, 11, 0.5) 20%, 
    rgba(245, 158, 11, 0.8) 50%, 
    rgba(245, 158, 11, 0.5) 80%, 
    transparent
  );
  opacity: 0;
  transition: opacity 0.4s;
}

.premium-navbar.scrolled .navbar-glow {
  opacity: 1;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* PREMIUM LOGO */
.logo-section {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  z-index: 1002;
  transition: transform 0.3s;
  position: relative;
}

.logo-section:hover {
  transform: scale(1.03);
}

.logo-circle {
  position: relative;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  width: 46px;
  height: 46px;
  object-fit: contain;
  filter: drop-shadow(0 4px 12px rgba(245, 158, 11, 0.4));
  position: relative;
  z-index: 2;
  transition: transform 0.3s;
}

.logo-section:hover .logo-img {
  transform: rotate(360deg);
}

.logo-ring {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(245, 158, 11, 0.3);
  border-radius: 50%;
  animation: pulse-ring 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-ring {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.2;
  }
}

.logo-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-size: 24px;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: 0.5px;
  line-height: 1;
}

.logo-subtitle {
  font-size: 10px;
  text-transform: uppercase;
  color: #f59e0b;
  letter-spacing: 1.5px;
  font-weight: 700;
}

/* MOBILE TOGGLE */
.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  z-index: 1002;
  position: relative;
}

.toggle-line {
  width: 28px;
  height: 3px;
  background: #f59e0b;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-toggle.active .toggle-line:nth-child(1) {
  transform: rotate(45deg) translateY(8px);
}

.mobile-toggle.active .toggle-line:nth-child(2) {
  opacity: 0;
  transform: translateX(-20px);
}

.mobile-toggle.active .toggle-line:nth-child(3) {
  transform: rotate(-45deg) translateY(-8px);
}

/* NAVIGATION MENU */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 48px;
  flex: 1;
  justify-content: flex-end;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 10px;
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link:hover {
  color: #ffffff;
  border-color: rgba(245, 158, 11, 0.3);
  transform: translateY(-2px);
}

.link-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.link-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s;
}

.nav-link:hover .link-icon {
  transform: scale(1.1);
  color: #f59e0b;
}

.link-text {
  position: relative;
  z-index: 1;
}

.nav-link.router-link-active {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.5);
  font-weight: 700;
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.15);
}

.nav-link.router-link-active .link-icon {
  color: #f59e0b;
}

/* USER SECTION */
.user-section {
  margin-left: 24px;
  position: relative;
}

.user-badge-wrapper {
  cursor: pointer;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 18px 6px 6px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 50px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.user-badge-wrapper:hover .user-badge,
.user-badge-wrapper.active .user-badge {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.5);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
}

.user-avatar {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-initial {
  position: relative;
  z-index: 2;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0f172a;
  font-weight: 900;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.avatar-ring {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(245, 158, 11, 0.3);
  border-radius: 50%;
  animation: pulse-avatar 2s ease-in-out infinite;
}

@keyframes pulse-avatar {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.2;
  }
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  line-height: 1.2;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
}

.user-role {
  font-size: 11px;
  color: #f59e0b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chevron-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  transition: transform 0.3s;
}

.chevron-icon.rotate {
  transform: rotate(180deg);
  color: #f59e0b;
}

/* DROPDOWN MENU */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 16px);
  right: 0;
  width: 300px;
  background: #1e293b;
  border: 2px solid rgba(51, 65, 85, 0.8);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  z-index: 1001;
}

.dropdown-header {
  padding: 24px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  border-bottom: 2px solid rgba(245, 158, 11, 0.3);
  display: flex;
  align-items: center;
  gap: 16px;
}

.dropdown-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0f172a;
  font-weight: 900;
  font-size: 20px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.dropdown-info {
  flex: 1;
  min-width: 0;
}

.dropdown-info h4 {
  color: #ffffff;
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 800;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-info p {
  color: #94a3b8;
  margin: 0 0 8px 0;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-tag {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(245, 158, 11, 0.2);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 6px;
  font-size: 10px;
  font-weight: 800;
  color: #f59e0b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dropdown-divider {
  height: 1px;
  background: rgba(51, 65, 85, 0.5);
}

.dropdown-body {
  padding: 12px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 14px 16px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #cbd5e1;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s;
  text-align: left;
}

.dropdown-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.dropdown-item:hover {
  background: rgba(51, 65, 85, 0.5);
  color: #ffffff;
  transform: translateX(4px);
}

.dropdown-item.logout-item {
  color: #ef4444;
  margin-top: 4px;
}

.dropdown-item.logout-item:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* AUTH SECTION */
.auth-section {
  margin-left: 24px;
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #0f172a;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
  border-radius: 50px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
  border: 2px solid transparent;
}

.auth-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.5);
  border-color: rgba(255, 255, 255, 0.2);
}

/* TRANSITIONS */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .premium-navbar {
    height: 70px;
  }

  .mobile-toggle {
    display: flex;
  }

  .logo-content {
    display: none;
  }

  .nav-menu {
    position: fixed;
    top: 0;
    right: -100%;
    width: 85%;
    max-width: 400px;
    height: 100vh;
    background: #0f172a;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    padding: 100px 24px 40px;
    transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1001;
    border-left: 2px solid rgba(245, 158, 11, 0.3);
    box-shadow: -10px 0 40px rgba(0, 0, 0, 0.5);
    overflow-y: auto;
  }

  .nav-menu.mobile-open {
    right: 0;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 12px;
    margin-bottom: 32px;
  }

  .nav-link {
    width: 100%;
    justify-content: flex-start;
    font-size: 16px;
    padding: 16px 20px;
  }

  .user-section {
    margin: 0;
    width: 100%;
  }

  .user-badge {
    width: 100%;
    justify-content: space-between;
  }

  .dropdown-menu {
    position: relative;
    top: auto;
    right: auto;
    width: 100%;
    margin-top: 16px;
  }

  .auth-section {
    margin: 0;
    width: 100%;
  }

  .auth-btn {
    width: 100%;
    justify-content: center;
    padding: 16px 24px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .nav-menu {
    width: 100%;
  }
}
</style>
