<template>
  <div id="app">
    <Navbar v-if="isAuthenticated" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './store'
import { computed } from 'vue'

export default {
  name: 'App',
  components: { Navbar },
  setup() {
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    return { isAuthenticated }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
}

.main-content {
  min-height: calc(100vh - 70px);
}
</style>
