<template>
  <span class="status-badge" :class="`status-${estado}`">
    <span class="status-icon">{{ getIcon(estado) }}</span>
    <span class="status-text">{{ getLabel(estado) }}</span>
  </span>
</template>

<script setup>
defineProps({
  estado: {
    type: String,
    required: true
  }
})

const getLabel = (estado) => {
  const labels = {
    borrador: 'Borrador',
    pendiente_validacion: 'Pendiente',
    validado_asesor: 'Validado',
    activo: 'Activo',
    rechazado: 'Rechazado',
    finalizado: 'Finalizado'
  }
  return labels[estado] || estado
}

const getIcon = (estado) => {
  const icons = {
    borrador: '📝',
    pendiente_validacion: '⏳',
    validado_asesor: '✅',
    activo: '🚀',
    rechazado: '❌',
    finalizado: '🏁'
  }
  return icons[estado] || '•'
}
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-icon {
  font-size: 1rem;
}

.status-borrador {
  background: #dbeafe;
  color: #1e40af;
}

.status-pendiente_validacion {
  background: #fef3c7;
  color: #92400e;
}

.status-validado_asesor {
  background: #d1fae5;
  color: #065f46;
}

.status-activo {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  font-weight: 700;
}

.status-rechazado {
  background: #fee2e2;
  color: #991b1b;
}

.status-finalizado {
  background: var(--gray-200);
  color: var(--gray-700);
}
</style>
