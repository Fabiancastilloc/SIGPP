<template>
  <div class="notification-center">
    <button @click="togglePanel" class="notification-button">
      <span class="icon">🔔</span>
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>

    <transition name="slide">
      <div v-if="showPanel" class="notification-panel">
        <div class="panel-header">
          <h3>Notificaciones</h3>
          <button @click="markAllRead" class="btn-text">Marcar todas</button>
        </div>

        <div v-if="notifications.length === 0" class="empty-notifications">
          <span class="empty-icon">📭</span>
          <p>No hay notificaciones</p>
        </div>

        <div v-else class="notifications-list">
          <div v-for="notif in notifications" :key="notif.id" class="notification-item"
            :class="[notif.tipo, { unread: !notif.leida }]" @click="markRead(notif.id)">
            <span class="notif-icon">{{ getIcon(notif.tipo) }}</span>
            <div class="notif-content">
              <p class="notif-title">{{ notif.titulo }}</p>
              <p class="notif-message">{{ notif.mensaje }}</p>
              <span class="notif-time">{{ formatTime(notif.fecha) }}</span>
            </div>
            <button @click.stop="remove(notif.id)" class="btn-close">×</button>
          </div>
        </div>

        <div v-if="notifications.length > 0" class="panel-footer">
          <button @click="clearAll" class="btn-clear">Limpiar todo</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useNotificationStore } from '@/stores/notifications'

const notifStore = useNotificationStore()
const showPanel = ref(false)

const notifications = computed(() => notifStore.notifications)
const unreadCount = computed(() => notifStore.unreadCount)

const togglePanel = () => {
  showPanel.value = !showPanel.value
}

const markRead = (id) => {
  notifStore.markAsRead(id)
}

const markAllRead = () => {
  notifStore.markAllAsRead()
}

const remove = (id) => {
  notifStore.removeNotification(id)
}

const clearAll = () => {
  notifStore.clearAll()
  showPanel.value = false
}

const getIcon = (tipo) => {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: '📌'
  }
  return icons[tipo] || '📬'
}

const formatTime = (fecha) => {
  const now = new Date()
  const diff = Math.floor((now - new Date(fecha)) / 1000)

  if (diff < 60) return 'Ahora'
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)}m`
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)}h`
  return `Hace ${Math.floor(diff / 86400)}d`
}
</script>

<style scoped>
.notification-center {
  position: relative;
}

.notification-button {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: white;
  border: 1px solid var(--gray-300);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-base);
}

.notification-button:hover {
  background: var(--gray-50);
  border-color: var(--primary);
}

.notification-button .icon {
  font-size: 1.25rem;
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--error);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
}

.notification-panel {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 380px;
  max-height: 500px;
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--gray-200);
  z-index: var(--z-dropdown);
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--gray-200);
}

.panel-header h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--gray-900);
}

.btn-text {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
}

.empty-notifications {
  padding: var(--space-12);
  text-align: center;
  color: var(--gray-500);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: var(--space-4);
}

.notifications-list {
  overflow-y: auto;
  max-height: 400px;
}

.notification-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  border-bottom: 1px solid var(--gray-100);
  cursor: pointer;
  transition: var(--transition-base);
}

.notification-item:hover {
  background: var(--gray-50);
}

.notification-item.unread {
  background: #dbeafe;
}

.notif-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
}

.notif-title {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 0.9375rem;
  margin-bottom: var(--space-1);
}

.notif-message {
  color: var(--gray-600);
  font-size: 0.875rem;
  line-height: 1.4;
  margin-bottom: var(--space-1);
}

.notif-time {
  font-size: 0.75rem;
  color: var(--gray-500);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--gray-400);
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.btn-close:hover {
  color: var(--error);
}

.panel-footer {
  padding: var(--space-3);
  border-top: 1px solid var(--gray-200);
  text-align: center;
}

.btn-clear {
  background: none;
  border: none;
  color: var(--error);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
}

.btn-clear:hover {
  background: var(--error-light);
}

/* Transiciones */
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

@media (max-width: 480px) {
  .notification-panel {
    width: 320px;
  }
}
</style>
