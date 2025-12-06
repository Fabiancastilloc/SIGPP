<!-- frontend/src/views/MyProfile.vue -->
<template>
  <div class="profile-page">
    <!-- Fondo Animado Mejorado -->
    <div class="profile-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="floating-shapes">
        <div v-for="i in 8" :key="i" class="shape" :style="getShapeStyle(i)"></div>
      </div>
    </div>

    <div class="profile-wrapper">
      <!-- Cover Header -->
      <div class="profile-cover">
        <div class="cover-overlay"></div>
        <button @click="goBack" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>Volver</span>
        </button>
      </div>

      <div class="profile-container">
        <!-- Profile Header con Avatar -->
        <div class="profile-header">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <div class="avatar-circle">
                <div class="avatar-content">
                  <span class="avatar-emoji">{{ getAvatarEmoji }}</span>
                </div>
                <div class="avatar-ring"></div>
              </div>
              
              <button v-if="!editMode && !changePasswordMode" @click="changeAvatar" class="btn-avatar-change">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>

            <div class="user-details">
              <h1 class="user-name">{{ user?.nombre_completo || 'Usuario' }}</h1>
              <div class="user-badges">
                <span class="badge badge-role" :class="`badge-${user?.rol}`">
                  <span class="badge-icon">{{ getRoleIcon }}</span>
                  <span>{{ getRoleLabel }}</span>
                </span>
                <span class="badge badge-code">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                  </svg>
                  <span>{{ user?.codigo_institucional }}</span>
                </span>
              </div>
            </div>
          </div>

          <div class="header-actions" v-if="!editMode && !changePasswordMode">
            <button @click="enableEditMode" class="btn-action btn-edit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span>Editar Perfil</span>
            </button>

            <button @click="enablePasswordMode" class="btn-action btn-password">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
              <span>Cambiar Contraseña</span>
            </button>
          </div>
        </div>

        <!-- Stats (Solo para estudiantes) -->
        <div v-if="user?.rol === 'estudiante' && !editMode && !changePasswordMode" class="stats-section">
          <div class="stat-card">
            <div class="stat-icon-wrapper">
              <div class="stat-icon">📊</div>
            </div>
            <div class="stat-details">
              <div class="stat-value">{{ userStats.totalProjects }}</div>
              <div class="stat-label">Total Proyectos</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper">
              <div class="stat-icon">✅</div>
            </div>
            <div class="stat-details">
              <div class="stat-value">{{ userStats.activeProjects }}</div>
              <div class="stat-label">Activos</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper">
              <div class="stat-icon">⏳</div>
            </div>
            <div class="stat-details">
              <div class="stat-value">{{ userStats.pendingProjects }}</div>
              <div class="stat-label">Pendientes</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper">
              <div class="stat-icon">💰</div>
            </div>
            <div class="stat-details">
              <div class="stat-value">{{ formatCurrency(userStats.totalBudget) }}</div>
              <div class="stat-label">Presupuesto Total</div>
            </div>
          </div>
        </div>

        <!-- MODO VISTA -->
        <div v-if="!editMode && !changePasswordMode" class="profile-content">
          
          <!-- Información Personal -->
          <div class="info-card">
            <div class="card-header">
              <div class="header-left">
                <span class="header-icon">👤</span>
                <h2>Información Personal</h2>
              </div>
            </div>

            <div class="card-body">
              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>Email</span>
                </div>
                <div class="info-value">{{ user?.email }}</div>
              </div>

              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>Rol</span>
                </div>
                <div class="info-value">
                  <span class="info-badge" :class="`badge-${user?.rol}`">{{ getRoleLabel }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Información Académica -->
          <div v-if="['estudiante', 'profesor'].includes(user?.rol)" class="info-card">
            <div class="card-header">
              <div class="header-left">
                <span class="header-icon">🎓</span>
                <h2>Información Académica</h2>
              </div>
            </div>

            <div class="card-body">
              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span>Sede</span>
                </div>
                <div class="info-value">{{ user?.sede?.nombre || 'No asignada' }}</div>
              </div>

              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                  </svg>
                  <span>Facultad</span>
                </div>
                <div class="info-value">{{ user?.facultad?.nombre || 'No asignada' }}</div>
              </div>

              <div v-if="user?.rol === 'estudiante'" class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <span>Carrera</span>
                </div>
                <div class="info-value">{{ user?.carrera?.nombre || 'No asignada' }}</div>
              </div>

              <div v-if="user?.rol === 'estudiante' && user?.semestre" class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <span>Semestre</span>
                </div>
                <div class="info-value">
                  <span class="info-badge badge-semester">Semestre {{ user.semestre }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Información de Cuenta -->
          <div class="info-card">
            <div class="card-header">
              <div class="header-left">
                <span class="header-icon">⚙️</span>
                <h2>Información de Cuenta</h2>
              </div>
            </div>

            <div class="card-body">
              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Fecha de Registro</span>
                </div>
                <div class="info-value">{{ formatDate(user?.created_at) }}</div>
              </div>

              <div class="info-row">
                <div class="info-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Estado</span>
                </div>
                <div class="info-value">
                  <span class="info-badge badge-active">
                    <span class="badge-pulse"></span>
                    Activo
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODO EDICIÓN -->
        <div v-if="editMode" class="edit-content">
          <form @submit.prevent="handleUpdateProfile" class="edit-form">
            
            <div class="form-card">
              <div class="card-header">
                <div class="header-left">
                  <span class="header-icon">✏️</span>
                  <h2>Editar Información Personal</h2>
                </div>
              </div>

              <div class="card-body">
                <div class="form-grid">
                  <div class="form-group full-width">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span>Nombre Completo</span>
                      <span class="required">*</span>
                    </label>
                    <input 
                      v-model="editedUser.nombre_completo"
                      type="text"
                      class="form-input"
                      required
                      :disabled="loading"
                    />
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <span>Correo</span>
                      <span class="required">*</span>
                    </label>
                    <input 
                      v-model="editedUser.email"
                      type="email"
                      class="form-input"
                      required
                      :disabled="loading"
                    />
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                      </svg>
                      <span>Código</span>
                    </label>
                    <input 
                      v-model="editedUser.codigo_institucional"
                      type="text"
                      class="form-input"
                      disabled
                    />
                    <span class="form-hint">No se puede modificar</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información Académica Editable -->
            <div v-if="['estudiante', 'profesor'].includes(user?.rol)" class="form-card">
              <div class="card-header">
                <div class="header-left">
                  <span class="header-icon">🎓</span>
                  <h2>Información Académica</h2>
                </div>
              </div>

              <div class="card-body">
                <div class="form-grid">
                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      <span>Sede</span>
                    </label>
                    <select 
                      v-model="editedUser.sede_id"
                      class="form-select"
                      @change="loadFacultadesEdit"
                      :disabled="loading"
                    >
                      <option value="">Seleccione una sede</option>
                      <option v-for="sede in sedes" :key="sede.id" :value="sede.id">
                        {{ sede.nombre }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                      </svg>
                      <span>Facultad</span>
                    </label>
                    <select 
                      v-model="editedUser.facultad_id"
                      class="form-select"
                      @change="loadCarrerasEdit"
                      :disabled="loading || !editedUser.sede_id"
                    >
                      <option value="">Seleccione una facultad</option>
                      <option v-for="facultad in facultades" :key="facultad.id" :value="facultad.id">
                        {{ facultad.nombre }}
                      </option>
                    </select>
                  </div>

                  <div v-if="user?.rol === 'estudiante'" class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                      <span>Carrera</span>
                    </label>
                    <select 
                      v-model="editedUser.carrera_id"
                      class="form-select"
                      :disabled="loading || !editedUser.facultad_id"
                    >
                      <option value="">Seleccione una carrera</option>
                      <option v-for="carrera in carreras" :key="carrera.id" :value="carrera.id">
                        {{ carrera.nombre }}
                      </option>
                    </select>
                  </div>

                  <div v-if="user?.rol === 'estudiante'" class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                      <span>Semestre</span>
                    </label>
                    <input 
                      v-model.number="editedUser.semestre"
                      type="number"
                      class="form-input"
                      min="1"
                      max="12"
                      :disabled="loading"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Alerts -->
            <transition name="alert-fade">
              <div v-if="error" class="alert alert-error">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ error }}</span>
              </div>
            </transition>

            <transition name="alert-fade">
              <div v-if="success" class="alert alert-success">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ success }}</span>
              </div>
            </transition>

            <!-- Form Actions -->
            <div class="form-actions">
              <button type="button" @click="cancelEdit" class="btn-action btn-cancel" :disabled="loading">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>Cancelar</span>
              </button>

              <button type="submit" class="btn-action btn-save" :disabled="loading">
                <svg v-if="loading" class="spinner" viewBox="0 0 24 24">
                  ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <span>{{ loading ? 'Guardando...' : 'Guardar Cambios' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- MODO CAMBIAR CONTRASEÑA -->
        <div v-if="changePasswordMode" class="edit-content">
          <form @submit.prevent="handleChangePassword" class="edit-form">
            
            <div class="form-card">
              <div class="card-header">
                <div class="header-left">
                  <span class="header-icon">🔐</span>
                  <h2>Cambiar Contraseña</h2>
                </div>
              </div>

              <div class="card-body">
                <div class="form-grid">
                  <div class="form-group full-width">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      <span>Contraseña Actual</span>
                      <span class="required">*</span>
                    </label>
                    <div class="password-field">
                      <input 
                        v-model="passwordForm.current_password"
                        :type="showCurrentPassword ? 'text' : 'password'"
                        class="form-input"
                        placeholder="Tu contraseña actual"
                        required
                        :disabled="loading"
                      />
                      <button 
                        type="button"
                        @click="showCurrentPassword = !showCurrentPassword"
                        class="password-toggle"
                      >
                        <svg v-if="!showCurrentPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      <span>Nueva Contraseña</span>
                      <span class="required">*</span>
                    </label>
                    <div class="password-field">
                      <input 
                        v-model="passwordForm.new_password"
                        :type="showNewPassword ? 'text' : 'password'"
                        class="form-input"
                        placeholder="Mínimo 8 caracteres"
                        required
                        :disabled="loading"
                      />
                      <button 
                        type="button"
                        @click="showNewPassword = !showNewPassword"
                        class="password-toggle"
                      >
                        <svg v-if="!showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                    <span class="form-hint">Incluye mayúsculas, minúsculas y números</span>
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                      <span>Confirmar Contraseña</span>
                      <span class="required">*</span>
                    </label>
                    <div class="password-field">
                      <input 
                        v-model="passwordForm.confirm_password"
                        :type="showConfirmPassword ? 'text' : 'password'"
                        class="form-input"
                        placeholder="Repite la nueva contraseña"
                        required
                        :disabled="loading"
                      />
                      <button 
                        type="button"
                        @click="showConfirmPassword = !showConfirmPassword"
                        class="password-toggle"
                      >
                        <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Alerts -->
            <transition name="alert-fade">
              <div v-if="error" class="alert alert-error">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ error }}</span>
              </div>
            </transition>

            <transition name="alert-fade">
              <div v-if="success" class="alert alert-success">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ success }}</span>
              </div>
            </transition>

            <!-- Form Actions -->
            <div class="form-actions">
              <button type="button" @click="cancelPasswordChange" class="btn-action btn-cancel" :disabled="loading">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>Cancelar</span>
              </button>

              <button type="submit" class="btn-action btn-save" :disabled="loading">
                <svg v-if="loading" class="spinner" viewBox="0 0 24 24">
                  ircle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                <span>{{ loading ? 'Cambiando...' : 'Cambiar Contraseña' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'      // ⬅️ SIN /auth al final
import catalogsApi from '../api/catalogs'
import usersApi from '../api/users'


export default {
  name: 'MyProfile',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const user = computed(() => authStore.user)
    const editMode = ref(false)
    const changePasswordMode = ref(false)
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    
    const editedUser = ref({})
    const sedes = ref([])
    const facultades = ref([])
    const carreras = ref([])
    
    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    const showCurrentPassword = ref(false)
    const showNewPassword = ref(false)
    const showConfirmPassword = ref(false)
    
    const userStats = ref({
      totalProjects: 0,
      activeProjects: 0,
      pendingProjects: 0,
      totalBudget: 0
    })
    
    const getAvatarEmoji = computed(() => {
      const emojis = {
        estudiante: '🎓',
        profesor: '👨‍🏫',
        financiera: '💼',
        auditor: '🔍',
        super_usuario: '⚡'
      }
      return emojis[user.value?.rol] || '👤'
    })
    
    const getRoleIcon = computed(() => {
      const icons = {
        estudiante: '🎓',
        profesor: '👨‍🏫',
        financiera: '💼',
        auditor: '🔍',
        super_usuario: '⚡'
      }
      return icons[user.value?.rol] || '👤'
    })
    
    const getRoleLabel = computed(() => {
      const labels = {
        estudiante: 'Estudiante',
        profesor: 'Profesor',
        financiera: 'Financiera',
        auditor: 'Auditor',
        super_usuario: 'Super Usuario'
      }
      return labels[user.value?.rol] || 'Usuario'
    })
    
    const getShapeStyle = (index) => {
      const size = 100 + Math.random() * 200
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${15 + Math.random() * 10}s`
      }
    }
    
    const goBack = () => {
      const routes = {
        estudiante: '/student',
        profesor: '/professor',
        financiera: '/finance',
        auditor: '/auditor',
        super_usuario: '/admin'
      }
      router.push(routes[user.value?.rol] || '/')
    }
    
    const enableEditMode = () => {
      editedUser.value = {
        nombre_completo: user.value.nombre_completo,
        email: user.value.email,
        codigo_institucional: user.value.codigo_institucional,
        sede_id: user.value.sede?.id || null,
        facultad_id: user.value.facultad?.id || null,
        carrera_id: user.value.carrera?.id || null,
        semestre: user.value.semestre || null
      }
      editMode.value = true
      loadCatalogsForEdit()
    }
    
    const cancelEdit = () => {
      editMode.value = false
      error.value = ''
      success.value = ''
    }
    
    const enablePasswordMode = () => {
      changePasswordMode.value = true
      passwordForm.value = {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
    
    const cancelPasswordChange = () => {
      changePasswordMode.value = false
      error.value = ''
      success.value = ''
      passwordForm.value = {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
    
    const changeAvatar = () => {
      alert('Funcionalidad de cambio de avatar en desarrollo')
    }
    
    const loadCatalogsForEdit = async () => {
      try {
        const sedesResponse = await catalogsApi.getSedes()
        sedes.value = sedesResponse.data
        
        if (editedUser.value.sede_id) {
          await loadFacultadesEdit()
        }
        
        if (editedUser.value.facultad_id) {
          await loadCarrerasEdit()
        }
      } catch (err) {
        console.error('Error cargando catálogos:', err)
      }
    }
    
    const loadFacultadesEdit = async () => {
      if (!editedUser.value.sede_id) return
      try {
        const response = await catalogsApi.getFacultades(editedUser.value.sede_id)
        facultades.value = response.data
      } catch (err) {
        console.error('Error cargando facultades:', err)
      }
    }
    
    const loadCarrerasEdit = async () => {
      if (!editedUser.value.facultad_id) return
      try {
        const response = await catalogsApi.getCarreras(editedUser.value.facultad_id)
        carreras.value = response.data
      } catch (err) {
        console.error('Error cargando carreras:', err)
      }
    }
    
    const handleUpdateProfile = async () => {
      error.value = ''
      success.value = ''
      loading.value = true
      
      try {
        await usersApi.updateProfile(user.value.id, editedUser.value)
        success.value = '✅ Perfil actualizado exitosamente'
        
        await authStore.fetchUser()
        
        setTimeout(() => {
          editMode.value = false
          success.value = ''
        }, 2000)
      } catch (err) {
        console.error('Error actualizando perfil:', err)
        error.value = err.response?.data?.detail || '❌ Error al actualizar el perfil'
      } finally {
        loading.value = false
      }
    }
    
    const handleChangePassword = async () => {
      error.value = ''
      success.value = ''
      
      if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
        error.value = '❌ Las contraseñas nuevas no coinciden'
        return
      }
      
      if (passwordForm.value.new_password.length < 8) {
        error.value = '❌ La contraseña debe tener al menos 8 caracteres'
        return
      }
      
      loading.value = true
      
      try {
        await usersApi.changePassword({
          current_password: passwordForm.value.current_password,
          new_password: passwordForm.value.new_password
        })
        
        success.value = '✅ Contraseña cambiada exitosamente'
        
        setTimeout(() => {
          changePasswordMode.value = false
          success.value = ''
          passwordForm.value = {
            current_password: '',
            new_password: '',
            confirm_password: ''
          }
        }, 2000)
      } catch (err) {
        console.error('Error cambiando contraseña:', err)
        error.value = err.response?.data?.detail || '❌ Error al cambiar la contraseña'
      } finally {
        loading.value = false
      }
    }
    
    const formatCurrency = (value) => {
      if (!value) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
      }).format(value)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'No disponible'
      return new Date(dateString).toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    onMounted(async () => {
      if (user.value?.rol === 'estudiante') {
        try {
          const statsResponse = await usersApi.getUserStats(user.value.id)
          userStats.value = statsResponse.data
        } catch (err) {
          console.error('Error cargando estadísticas:', err)
        }
      }
    })
    
    return {
      user,
      editMode,
      changePasswordMode,
      loading,
      error,
      success,
      editedUser,
      sedes,
      facultades,
      carreras,
      passwordForm,
      showCurrentPassword,
      showNewPassword,
      showConfirmPassword,
      userStats,
      getAvatarEmoji,
      getRoleIcon,
      getRoleLabel,
      getShapeStyle,
      goBack,
      enableEditMode,
      cancelEdit,
      enablePasswordMode,
      cancelPasswordChange,
      changeAvatar,
      loadFacultadesEdit,
      loadCarrerasEdit,
      handleUpdateProfile,
      handleChangePassword,
      formatCurrency,
      formatDate
    }
  }
}
</script>

<style scoped>
/* ===== BASE ===== */
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  position: relative;
  overflow-x: hidden;
}

/* ===== BACKGROUND ANIMADO ===== */
.profile-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
  animation: float-smooth 25s ease-in-out infinite;
}

.orb-1 {
  width: 700px;
  height: 700px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -350px;
  right: -350px;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -300px;
  left: -300px;
  animation-delay: -12s;
}

.orb-3 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 40%;
  left: 50%;
  animation-delay: -6s;
}

@keyframes float-smooth {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(60px, -60px) scale(1.15);
  }
  66% {
    transform: translate(-50px, 50px) scale(0.9);
  }
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  background: rgba(212, 175, 55, 0.03);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation: float-shape infinite ease-in-out;
}

@keyframes float-shape {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  50% {
    transform: translate(30px, -30px) rotate(180deg);
  }
}

/* ===== WRAPPER ===== */
.profile-wrapper {
  position: relative;
  z-index: 1;
}

/* ===== COVER ===== */
.profile-cover {
  height: 240px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.4) 0%, rgba(59, 130, 246, 0.4) 100%);
  position: relative;
  overflow: hidden;
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%);
}

.btn-back {
  position: absolute;
  top: 28px;
  left: 28px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 26px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  color: white;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 10;
}

.btn-back:hover {
  background: rgba(212, 175, 55, 0.3);
  border-color: rgba(212, 175, 55, 0.6);
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* ===== CONTAINER ===== */
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px 80px;
}

/* ===== PROFILE HEADER ===== */
.profile-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
  margin-top: -100px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.avatar-section {
  display: flex;
  align-items: flex-end;
  gap: 28px;
}

.avatar-wrapper {
  position: relative;
}

.avatar-circle {
  width: 160px;
  height: 160px;
  position: relative;
}

.avatar-content {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 6px solid rgba(30, 41, 59, 0.9);
  box-shadow: 
    0 16px 48px rgba(212, 175, 55, 0.5),
    0 0 0 4px rgba(212, 175, 55, 0.2);
  position: relative;
  z-index: 2;
}

.avatar-emoji {
  font-size: 72px;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));
}

.avatar-ring {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border: 3px solid rgba(212, 175, 55, 0.4);
  border-radius: 50%;
  animation: pulse-ring 3s ease-in-out infinite;
}

@keyframes pulse-ring {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.btn-avatar-change {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 48px;
  height: 48px;
  background: rgba(212, 175, 55, 0.95);
  border: 4px solid rgba(30, 41, 59, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 3;
}

.btn-avatar-change:hover {
  background: #d4af37;
  transform: scale(1.15) rotate(10deg);
}

.btn-avatar-change svg {
  width: 22px;
  height: 22px;
  color: #0a0f1e;
}

.user-details {
  padding-bottom: 16px;
}

.user-name {
  font-size: 2.75rem;
  font-weight: 900;
  color: white;
  margin-bottom: 16px;
  text-shadow: 0 3px 12px rgba(0, 0, 0, 0.4);
  line-height: 1.1;
}

.user-badges {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  border: 2px solid;
  transition: all 0.3s;
}

.badge svg {
  width: 18px;
  height: 18px;
}

.badge-role {
  background: rgba(212, 175, 55, 0.15);
  border-color: rgba(212, 175, 55, 0.4);
  color: #d4af37;
}

.badge-role:hover {
  background: rgba(212, 175, 55, 0.25);
  transform: translateY(-2px);
}

.badge-icon {
  font-size: 20px;
}

.badge-code {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.4);
  color: #60a5fa;
  font-family: 'Courier New', monospace;
}

.badge-code:hover {
  background: rgba(59, 130, 246, 0.25);
  transform: translateY(-2px);
}

/* ===== HEADER ACTIONS ===== */
.header-actions {
  display: flex;
  gap: 14px;
  padding-bottom: 16px;
  flex-wrap: wrap;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 28px;
  border: 2px solid;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-action svg {
  width: 22px;
  height: 22px;
}

.btn-edit {
  background: rgba(212, 175, 55, 0.1);
  border-color: #d4af37;
  color: #d4af37;
}

.btn-edit:hover:not(:disabled) {
  background: linear-gradient(135deg, #d4af37, #b8960f);
  color: #0a0f1e;
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(212, 175, 55, 0.5);
}

.btn-password {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
  color: #60a5fa;
}

.btn-password:hover:not(:disabled) {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(59, 130, 246, 0.5);
}

.btn-cancel {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #fca5a5;
}

.btn-cancel:hover:not(:disabled) {
  background: #ef4444;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(239, 68, 68, 0.5);
}

.btn-save {
  background: linear-gradient(135deg, #10b981, #059669);
  border-color: #10b981;
  color: white;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(16, 185, 129, 0.6);
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* ===== STATS SECTION ===== */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px;
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(212, 175, 55, 0.25);
  border-radius: 18px;
  transition: all 0.4s;
}

.stat-card:hover {
  border-color: rgba(212, 175, 55, 0.6);
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(212, 175, 55, 0.25);
  background: rgba(212, 175, 55, 0.08);
}

.stat-icon-wrapper {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.1));
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid rgba(212, 175, 55, 0.3);
}

.stat-icon {
  font-size: 44px;
  filter: drop-shadow(0 3px 8px rgba(212, 175, 55, 0.4));
}

.stat-details {
  flex: 1;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 900;
  color: #d4af37;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ===== CONTENT SECTIONS ===== */
.profile-content,
.edit-content {
  display: grid;
  gap: 28px;
}

.info-card,
.form-card {
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(212, 175, 55, 0.25);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
}

.info-card:hover,
.form-card:hover {
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 12px 32px rgba(212, 175, 55, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 32px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 2px solid rgba(212, 175, 55, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  font-size: 36px;
  filter: drop-shadow(0 3px 8px rgba(212, 175, 55, 0.4));
}

.card-header h2 {
  font-size: 1.75rem;
  font-weight: 900;
  color: #f1f5f9;
}

.card-body {
  padding: 32px;
}

.info-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 24px;
  padding: 20px;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 14px;
  border: 1px solid rgba(212, 175, 55, 0.1);
  transition: all 0.3s;
  align-items: center;
}

.info-row:not(:last-child) {
  margin-bottom: 16px;
}

.info-row:hover {
  background: rgba(212, 175, 55, 0.08);
  border-color: rgba(212, 175, 55, 0.3);
}

.info-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-label svg {
  width: 18px;
  height: 18px;
  color: #d4af37;
}

.info-value {
  font-size: 17px;
  font-weight: 700;
  color: #f1f5f9;
}

.info-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 2px solid;
}

.badge-estudiante {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.4);
  color: #60a5fa;
}

.badge-profesor {
  background: rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.4);
  color: #c084fc;
}

.badge-financiera {
  background: rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.4);
  color: #6ee7b7;
}

.badge-auditor {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.4);
  color: #fbbf24;
}

.badge-semester {
  background: rgba(212, 175, 55, 0.2);
  border-color: rgba(212, 175, 55, 0.4);
  color: #d4af37;
}

.badge-active {
  background: rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.4);
  color: #6ee7b7;
  position: relative;
}

.badge-pulse {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.3);
  }
}

/* ===== FORMS ===== */
.edit-form {
  display: grid;
  gap: 28px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 800;
  color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-label svg {
  width: 20px;
  height: 20px;
  color: #d4af37;
}

.required {
  color: #ef4444;
  font-size: 18px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.9);
  border: 2px solid #334155;
  border-radius: 14px;
  color: #f1f5f9;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  background: #1e293b;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.15);
}

.form-input:disabled,
.form-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.password-field {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover {
  color: #d4af37;
}

.password-toggle svg {
  width: 100%;
  height: 100%;
}

.form-hint {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
  font-style: italic;
}

/* ===== ALERTS ===== */
.alert {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 24px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  border: 2px solid;
  animation: slide-down 0.4s ease-out;
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.alert-error {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}

.alert-success {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.4);
  color: #6ee7b7;
}

.alert-fade-enter-active,
.alert-fade-leave-active {
  transition: all 0.3s ease;
}

.alert-fade-enter-from,
.alert-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ===== FORM ACTIONS ===== */
.form-actions {
  display: flex;
  gap: 18px;
  justify-content: flex-end;
  padding-top: 32px;
  border-top: 2px solid rgba(212, 175, 55, 0.2);
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .avatar-section {
    flex-direction: column;
    align-items: center;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
  
  .user-badges {
    justify-content: center;
  }
  
  .info-row {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-action {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .profile-container {
    padding: 0 20px 60px;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
  }
  
  .user-name {
    font-size: 2rem;
  }
  
  .card-header {
    padding: 20px;
  }
  
  .card-body {
    padding: 20px;
  }
}
</style>
