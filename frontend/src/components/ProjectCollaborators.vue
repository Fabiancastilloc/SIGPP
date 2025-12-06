<!-- frontend/src/components/ProjectCollaborators.vue -->
<template>
  <div class="collaborators-section">
    <div class="section-header">
      <h3>👥 Equipo de Trabajo</h3>
      <button v-if="canManage" @click="showAddModal = true" class="btn-add">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        Agregar Colaborador
      </button>
    </div>

    <!-- Lista de colaboradores -->
    <div v-if="members.length > 0" class="members-list">
      <div v-for="member in members" :key="member.id" class="member-card">
        <div class="member-avatar">
          {{ getInitials(member.student.nombre_completo) }}
        </div>
        <div class="member-info">
          <strong>{{ member.student.nombre_completo }}</strong>
          <span class="member-email">{{ member.student.email }}</span>
          <span class="member-role">{{ member.role === 'owner' ? '👑 Creador' : '🤝 Colaborador' }}</span>
        </div>
        <button 
          v-if="canManage && member.role !== 'owner'" 
          @click="removeMember(member.id)" 
          class="btn-remove"
          title="Eliminar colaborador"
        >
          ❌
        </button>
      </div>
    </div>
    <div v-else class="empty-members">
      <p>No hay colaboradores agregados</p>
    </div>

    <!-- Solicitudes pendientes -->
    <div v-if="canManage && pendingRequests.length > 0" class="requests-section">
      <h4>📬 Solicitudes Pendientes ({{ pendingRequests.length }})</h4>
      <div class="requests-list">
        <div v-for="request in pendingRequests" :key="request.id" class="request-card">
          <div class="request-info">
            <strong>{{ request.student.nombre_completo }}</strong>
            <p v-if="request.message">{{ request.message }}</p>
            <span class="request-date">{{ formatDate(request.created_at) }}</span>
          </div>
          <div class="request-actions">
            <button @click="respondRequest(request.id, true)" class="btn-approve">✅ Aceptar</button>
            <button @click="respondRequest(request.id, false)" class="btn-reject">❌ Rechazar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Agregar Colaborador -->
    <transition name="modal">
      <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Agregar Colaborador</h3>
            <button @click="showAddModal = false" class="modal-close">✕</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>Buscar estudiante por código institucional:</label>
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Ej: EST20251001"
                class="form-control"
                @input="searchStudents"
              />
            </div>
            
            <div v-if="searchResults.length > 0" class="search-results">
              <div 
                v-for="student in searchResults" 
                :key="student.id" 
                class="student-result"
                @click="selectStudent(student)"
              >
                <div class="student-avatar">{{ getInitials(student.nombre_completo) }}</div>
                <div class="student-info">
                  <strong>{{ student.nombre_completo }}</strong>
                  <span>{{ student.codigo_institucional }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="showAddModal = false" class="btn-cancel">Cancelar</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import membersApi from '../api/members'
import catalogsApi from '../api/catalogs'

export default {
  name: 'ProjectCollaborators',
  props: {
    projectId: {
      type: Number,
      required: true
    },
    canManage: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const members = ref([])
    const pendingRequests = ref([])
    const showAddModal = ref(false)
    const searchQuery = ref('')
    const searchResults = ref([])
    
    const loadMembers = async () => {
      try {
        const response = await membersApi.getMembers(props.projectId)
        members.value = response.data
      } catch (err) {
        console.error('Error cargando colaboradores:', err)
      }
    }
    
    const loadPendingRequests = async () => {
      if (!props.canManage) return
      try {
        const response = await membersApi.getPendingRequests(props.projectId)
        pendingRequests.value = response.data
      } catch (err) {
        console.error('Error cargando solicitudes:', err)
      }
    }
    
    const searchStudents = async () => {
      if (searchQuery.value.length < 3) {
        searchResults.value = []
        return
      }
      try {
        const response = await catalogsApi.searchStudents(searchQuery.value)
        searchResults.value = response.data
      } catch (err) {
        console.error('Error buscando estudiantes:', err)
      }
    }
    
    const selectStudent = async (student) => {
      try {
        await membersApi.addMember(props.projectId, student.id)
        alert(`${student.nombre_completo} agregado como colaborador`)
        showAddModal.value = false
        searchQuery.value = ''
        searchResults.value = []
        loadMembers()
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al agregar colaborador')
      }
    }
    
    const removeMember = async (memberId) => {
      if (!confirm('¿Eliminar este colaborador?')) return
      try {
        await membersApi.removeMember(props.projectId, memberId)
        loadMembers()
      } catch (err) {
        alert('Error al eliminar colaborador')
      }
    }
    
    const respondRequest = async (requestId, approve) => {
      try {
        await membersApi.respondRequest(props.projectId, requestId, approve)
        loadPendingRequests()
        if (approve) loadMembers()
      } catch (err) {
        alert('Error al procesar solicitud')
      }
    }
    
    const getInitials = (name) => {
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('es-CO')
    }
    
    onMounted(() => {
      loadMembers()
      loadPendingRequests()
    })
    
    return {
      members, pendingRequests, showAddModal, searchQuery, searchResults,
      removeMember, respondRequest, searchStudents, selectStudent,
      getInitials, formatDate
    }
  }
}
</script>

<style scoped>
.collaborators-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 20px;
  color: #1e293b;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #d4af37, #aa8c2c);
  color: #0f172a;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add svg {
  width: 18px;
  height: 18px;
}

.btn-add:hover {
  transform: translateY(-2px);
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.member-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-info strong {
  font-size: 15px;
  color: #1e293b;
}

.member-email {
  font-size: 13px;
  color: #64748b;
}

.member-role {
  font-size: 12px;
  font-weight: 600;
  color: #d4af37;
}

.btn-remove {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.btn-remove:hover {
  opacity: 1;
}

.empty-members {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

/* Solicitudes */
.requests-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid #e2e8f0;
}

.requests-section h4 {
  font-size: 16px;
  margin-bottom: 16px;
  color: #d4af37;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #fef3c7;
  border-radius: 12px;
  border: 1px solid #d4af37;
}

.request-info strong {
  display: block;
  margin-bottom: 4px;
  color: #1e293b;
}

.request-info p {
  font-size: 14px;
  color: #475569;
  margin: 8px 0;
}

.request-date {
  font-size: 12px;
  color: #64748b;
}

.request-actions {
  display: flex;
  gap: 8px;
}

.btn-approve, .btn-reject {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-approve {
  background: #10b981;
  color: white;
}

.btn-reject {
  background: #ef4444;
  color: white;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 20px;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
}

.modal-body {
  padding: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #334155;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 15px;
}

.form-control:focus {
  outline: none;
  border-color: #d4af37;
}

.search-results {
  margin-top: 16px;
  max-height: 300px;
  overflow-y: auto;
}

.student-result {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.student-result:hover {
  background: #f8fafc;
}

.student-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.student-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.student-info strong {
  font-size: 14px;
  color: #1e293b;
}

.student-info span {
  font-size: 12px;
  color: #64748b;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 2px solid #e2e8f0;
  text-align: right;
}

.btn-cancel {
  padding: 10px 20px;
  background: #e2e8f0;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

/* Transitions */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
