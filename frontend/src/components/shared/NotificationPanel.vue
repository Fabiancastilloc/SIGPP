<template>
  <div class="notification-panel">
    <button @click="togglePanel" class="notification-button" :class="{ 'has-unread': unreadCount > 0 }">
      <span class="notification-icon">🔔</span>
      <span v-if="unreadCount > 0" class="notification-badge">
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <transition name="slide">
      <div v-if="isOpen" class="notification-dropdown">
        <div class="dropdown-header">
          <h3 class="dropdown-title">Notificaciones</h3>
          <div class="header-actions">
            <button v-if="notifications.length > 0" @click="markAllAsRead" class="btn-header"
              title="Marcar todas como leídas">
              ✓
            </button>
            <button v-if="notifications.length > 0" @click="clearAll" class="btn-header" title="Eliminar todas">
              🗑️
            </button>
            <button @click="togglePanel" class="btn-header" title="Cerrar">
              ✕
            </button>
          </div>
        </div>

        <div class="dropdown-content">
          <div v-if="notifications.length === 0" class="empty-notifications">
            <span class="empty-icon">🔕</span>
            <p>No tienes notificaciones</p>
          </div>

          <div v-else class="notifications-list">
            <div v-for="notification in notifications" :key="notification.id"
              :class="['notification-item', `notification-${notification.type}`, { 'unread': !notification.read }]"
              @click="markAsRead(notification.id)">
              <div class="notification-content">
                <div class="notification-header">
                  <span class="notification-title">{{ notification.title }}</span>
                  <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
                </div>
                <p class="notification-message">{{ notification.message }}</p>
              </div>
              <button @click.stop="removeNotification(notification.id)" class="btn-remove" title="Eliminar">
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Notificaciones Toast (flotantes) -->
    <transition-group name="toast" tag="div" class="toast-container">
      <div v-for="notification in recentNotifications" :key="notification.id"
        :class="['toast-notification', `toast-${notification.type}`]">
        <div class="toast-content">
          <span class="toast-title">{{ notification.title }}</span>
          <p class="toast-message">{{ notification.message }}</p>
        </div>
        <button @click="removeNotification(notification.id)" class="toast-close">
          ✕
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useNotificationStore } from '@/stores/notifications'

const notificationStore = useNotificationStore()

const isOpen = ref(false)
const recentNotifications = ref([])

const notifications = computed(() => notificationStore.sortedNotifications)
const unreadCount = computed(() => notificationStore.unreadCount)

// Watch para mostrar toast de nuevas notificaciones
watch(() => notificationStore.userNotifications.length, (newLength, oldLength) => {
  if (newLength > oldLength) {
    const latestNotification = notifications.value[0]
    if (latestNotification && latestNotification.duration > 0) {
      recentNotifications.value.unshift(latestNotification)

      // Limitar a 3 toasts simultáneos
      if (recentNotifications.value.length > 3) {
        recentNotifications.value.pop()
      }

      // Remover el toast después de su duración
      setTimeout(() => {
        const index = recentNotifications.value.findIndex(n => n.id === latestNotification.id)
        if (index !== -1) {
          recentNotifications.value.splice(index, 1)
        }
      }, latestNotification.duration)
    }
  }
})

const togglePanel = () => {
  isOpen.value = !isOpen.value
}

const markAsRead = (id) => {
  notificationStore.markAsRead(id)
}

const markAllAsRead = () => {
  notificationStore.markAllAsRead()
}

const removeNotification = (id) => {
  notificationStore.removeNotification(id)

  // También remover del toast si existe
  const toastIndex = recentNotifications.value.findIndex(n => n.id === id)
  if (toastIndex !== -1) {
    recentNotifications.value.splice(toastIndex, 1)
  }
}

const clearAll = () => {
  if (confirm('¿Eliminar todas las notificaciones?')) {
    notificationStore.clearAllNotifications()
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'Ahora'
  if (minutes < 60) return `Hace ${minutes} min`
  if (hours < 24) return `Hace ${hours} h`
  if (days < 7) return `Hace ${days} d`

  return date.toLocaleDateString('es-CO', {
    day: 'numeric',
    month: 'short'
  })
}
</script>

<style scoped>
.notification-panel {
  position: relative;
}

.notification-button {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: white;
  border: 2px solid var(--gray-200);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-button:hover {
  background: var(--gray-50);
  border-color: var(--primary);
}

.notification-button.has-unread {
  animation: pulse 2s infinite;
}

.notification-icon {
  font-size: 1.5rem;
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--error);
  color: white;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
}

.notification-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 400px;
  max-height: 600px;
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-2xl);
  border: 2px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4) var(--space-5);
  border-bottom: 2px solid var(--gray-200);
}

.dropdown-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: var(--gray-900);
}

.header-actions {
  display: flex;
  gap: var(--space-2);
}

.btn-header {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--gray-100);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-header:hover {
  background: var(--gray-200);
}

.dropdown-content {
  flex: 1;
  overflow-y: auto;
  max-height: 500px;
}

.empty-notifications {
  text-align: center;
  padding: var(--space-12) var(--space-6);
  color: var(--gray-500);
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.notifications-list {
  display: flex;
  flex-direction: column;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--gray-100);
  cursor: pointer;
  transition: all 0.2s;
}

.notification-item:hover {
  background: var(--gray-50);
}

.notification-item.unread {
  background: #f0f9ff;
  border-left: 4px solid var(--primary);
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2);
}

.notification-title {
  font-weight: 800;
  font-size: 0.875rem;
  color: var(--gray-900);
}

.notification-time {
  font-size: 0.75rem;
  color: var(--gray-500);
}

.notification-message {
  font-size: 0.875rem;
  color: var(--gray-700);
  line-height: 1.4;
}

.btn-remove {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-md);
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--gray-400);
  transition: all 0.2s;
}

.btn-remove:hover {
  background: var(--error-light);
  color: var(--error);
}

/* Toast Notifications */
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  pointer-events: none;
}

.toast-notification {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-2xl);
  border-left: 4px solid;
  min-width: 320px;
  max-width: 400px;
  pointer-events: all;
}

.toast-success {
  border-color: var(--success);
  background: #f0fdf4;
}

.toast-error {
  border-color: var(--error);
  background: #fef2f2;
}

.toast-warning {
  border-color: var(--warning);
  background: #fffbeb;
}

.toast-info {
  border-color: var(--info);
  background: #eff6ff;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 800;
  font-size: 0.875rem;
  color: var(--gray-900);
  display: block;
  margin-bottom: var(--space-1);
}

.toast-message {
  font-size: 0.875rem;
  color: var(--gray-700);
  line-height: 1.4;
}

.toast-close {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-md);
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--gray-400);
  transition: all 0.2s;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--gray-700);
}

/* Animations */
@keyframes pulse {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.7;
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.toast-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

@media (max-width: 768px) {
  .notification-dropdown {
    width: 100vw;
    max-width: 100vw;
    right: -24px;
    border-radius: 0;
  }

  .toast-container {
    right: 12px;
    left: 12px;
  }

  .toast-notification {
    min-width: auto;
    max-width: 100%;
  }
}
</style>
