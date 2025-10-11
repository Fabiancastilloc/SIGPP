import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useNotificationStore = defineStore("notifications", () => {
  const notifications = ref([]);
  const unreadCount = computed(
    () => notifications.value.filter((n) => !n.leida).length
  );

  function addNotification(notification) {
    const newNotif = {
      id: Date.now(),
      leida: false,
      fecha: new Date(),
      ...notification,
    };
    notifications.value.unshift(newNotif);

    // Auto-eliminar después de 5 segundos si es tipo success o info
    if (notification.tipo === "success" || notification.tipo === "info") {
      setTimeout(() => {
        removeNotification(newNotif.id);
      }, 5000);
    }
  }

  function markAsRead(id) {
    const notif = notifications.value.find((n) => n.id === id);
    if (notif) notif.leida = true;
  }

  function markAllAsRead() {
    notifications.value.forEach((n) => (n.leida = true));
  }

  function removeNotification(id) {
    const index = notifications.value.findIndex((n) => n.id === id);
    if (index > -1) notifications.value.splice(index, 1);
  }

  function clearAll() {
    notifications.value = [];
  }

  return {
    notifications,
    unreadCount,
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
  };
});
