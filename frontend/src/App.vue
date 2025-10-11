<template>
  <div id="app" :class="{ 'authenticated': isAuthenticated }">
    <HeaderNav v-if="isAuthenticated" />

    <main class="main-content" :class="{ 'no-header': !isAuthenticated }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <FooterBar v-if="isAuthenticated" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import HeaderNav from '@/components/layout/HeaderNav.vue'
import FooterBar from '@/components/layout/FooterBar.vue'

const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  authStore.checkAuth()
})
</script>

<style>
@import '@/assets/styles/variables.css';
@import '@/assets/styles/global.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
}

.main-content {
  flex: 1;
  width: 100%;
}

.main-content.no-header {
  padding-top: 0;
}

/* Transiciones de Página */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Estilos adicionales */
* {
  -webkit-tap-highlight-color: transparent;
}

::selection {
  background: var(--primary);
  color: white;
}

::-moz-selection {
  background: var(--primary);
  color: white;
}
</style>
