<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <h2>SIGPP</h2>
      </div>
      <div class="navbar-menu">
        <span class="user-name">{{ user.nombre_completo }} ({{ user.rol }})</span>
        <button @click="handleLogout" class="btn btn-danger">Cerrar Sesión</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../store'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

export default {
  name: 'Navbar',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const user = computed(() => authStore.user)
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return { user, handleLogout }
  }
}
</script>

<style scoped>
.navbar {
  background-color: var(--primary-color);
  color: white;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h2 {
  margin: 0;
  font-size: 24px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-name {
  font-size: 14px;
}
</style>