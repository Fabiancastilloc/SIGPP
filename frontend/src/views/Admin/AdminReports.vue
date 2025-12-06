<template>
  <div class="admin-reports-page">
    <!-- Animated Background -->
    <div class="dashboard-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <router-link to="/admin" class="btn-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Volver al Panel
        </router-link>
        
        <div class="header-title">
          <h1>📈 Reportes y Estadísticas</h1>
          <p>Generación de informes y análisis del sistema</p>
        </div>
      </div>

      <!-- Info Banner -->
      <div class="info-banner">
        <svg class="banner-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <strong>Generación de Reportes</strong>
          <p>Selecciona el tipo de reporte que deseas generar para análisis y auditoría</p>
        </div>
      </div>

      <!-- Reports Grid -->
      <div class="reports-grid">
        <!-- General Report -->
        <div class="report-card card-blue">
          <div class="card-icon-wrapper">
            <div class="card-icon">📊</div>
            <div class="icon-glow glow-blue"></div>
          </div>
          <div class="card-content">
            <h3>Reporte General</h3>
            <p>Estadísticas generales del sistema incluyendo proyectos, usuarios y actividad global</p>
            <ul class="feature-list">
              <li>✓ Total de proyectos</li>
              <li>✓ Usuarios registrados</li>
              <li>✓ Actividad mensual</li>
            </ul>
          </div>
          <button @click="generateReport('general')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generar Reporte
          </button>
        </div>

        <!-- Financial Report -->
        <div class="report-card card-green">
          <div class="card-icon-wrapper">
            <div class="card-icon">💰</div>
            <div class="icon-glow glow-green"></div>
          </div>
          <div class="card-content">
            <h3>Reporte Financiero</h3>
            <p>Análisis completo de presupuestos, gastos ejecutados y disponibilidad por proyecto</p>
            <ul class="feature-list">
              <li>✓ Presupuestos asignados</li>
              <li>✓ Gastos ejecutados</li>
              <li>✓ Balance general</li>
            </ul>
          </div>
          <button @click="generateReport('financiero')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generar Reporte
          </button>
        </div>

        <!-- Students Report -->
        <div class="report-card card-purple">
          <div class="card-icon-wrapper">
            <div class="card-icon">👨‍🎓</div>
            <div class="icon-glow glow-purple"></div>
          </div>
          <div class="card-content">
            <h3>Reporte de Estudiantes</h3>
            <p>Listado detallado de proyectos por estudiante con estados y presupuestos</p>
            <ul class="feature-list">
              <li>✓ Proyectos por estudiante</li>
              <li>✓ Estados de avance</li>
              <li>✓ Historial académico</li>
            </ul>
          </div>
          <button @click="generateReport('estudiantes')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generar Reporte
          </button>
        </div>

        <!-- Audit Report -->
        <div class="report-card card-orange">
          <div class="card-icon-wrapper">
            <div class="card-icon">📋</div>
            <div class="icon-glow glow-orange"></div>
          </div>
          <div class="card-content">
            <h3>Auditoría Completa</h3>
            <p>Registro completo de todas las actividades y cambios realizados en el sistema</p>
            <ul class="feature-list">
              <li>✓ Bitácora de cambios</li>
              <li>✓ Acciones de usuarios</li>
              <li>✓ Trazabilidad total</li>
            </ul>
          </div>
          <button @click="generateReport('auditoria')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generar Reporte
          </button>
        </div>

        <!-- Custom Report -->
        <div class="report-card card-red">
          <div class="card-icon-wrapper">
            <div class="card-icon">⚙️</div>
            <div class="icon-glow glow-red"></div>
          </div>
          <div class="card-content">
            <h3>Reporte Personalizado</h3>
            <p>Crea reportes personalizados seleccionando filtros y campos específicos</p>
            <ul class="feature-list">
              <li>✓ Filtros personalizados</li>
              <li>✓ Campos seleccionables</li>
              <li>✓ Exportación múltiple</li>
            </ul>
          </div>
          <button @click="generateReport('personalizado')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generar Reporte
          </button>
        </div>

        <!-- Export Options -->
        <div class="report-card card-cyan">
          <div class="card-icon-wrapper">
            <div class="card-icon">📤</div>
            <div class="icon-glow glow-cyan"></div>
          </div>
          <div class="card-content">
            <h3>Opciones de Exportación</h3>
            <p>Exporta los datos del sistema en diferentes formatos para análisis externo</p>
            <ul class="feature-list">
              <li>✓ Formato PDF</li>
              <li>✓ Formato Excel</li>
              <li>✓ Formato CSV</li>
            </ul>
          </div>
          <button @click="generateReport('exportacion')" class="btn-generate">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Opciones
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AdminReports',
  setup() {
    const generating = ref(false)

    const generateReport = async (type) => {
      if (generating.value) return

      generating.value = true

      // Simulación de generación
      setTimeout(() => {
        alert(`✅ Reporte "${type}" generado exitosamente!\n\nEn producción, aquí se descargaría el archivo.`)
        generating.value = false
      }, 1500)
    }
    
    return { generateReport, generating }
  }
}
</script>

<style scoped>
/* BASE */
.admin-reports-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  padding: 32px 16px;
  position: relative;
}

/* ANIMATED BACKGROUND */
.dashboard-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
  animation: float 25s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  top: -300px;
  left: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -250px;
  right: -250px;
  animation-delay: -12s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-50px, 50px) scale(0.9); }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER */
.page-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 32px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 12px;
  color: #f1f5f9;
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  transition: all 0.3s;
  width: fit-content;
}

.btn-back:hover {
  background: #334155;
  border-color: #3b82f6;
  transform: translateX(-4px);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.header-title h1 {
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 8px;
}

.header-title p {
  font-size: 16px;
  color: #cbd5e1;
  font-weight: 600;
}

/* INFO BANNER */
.info-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(59, 130, 246, 0.1);
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 16px;
  margin-bottom: 40px;
}

.banner-icon {
  width: 32px;
  height: 32px;
  color: #3b82f6;
  flex-shrink: 0;
}

.info-banner strong {
  display: block;
  font-size: 16px;
  margin-bottom: 6px;
  color: #60a5fa;
  font-weight: 900;
}

.info-banner p {
  margin: 0;
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 600;
}

/* REPORTS GRID */
.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.report-card {
  background: #1e293b;
  border: 2px solid #334155;
  border-radius: 20px;
  padding: 32px 28px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.report-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent, currentColor, transparent);
  opacity: 0;
  transition: opacity 0.4s;
}

.report-card:hover::before {
  opacity: 1;
}

.report-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.card-blue { color: #3b82f6; }
.card-blue:hover { border-color: rgba(59, 130, 246, 0.5); }

.card-green { color: #10b981; }
.card-green:hover { border-color: rgba(16, 185, 129, 0.5); }

.card-purple { color: #8b5cf6; }
.card-purple:hover { border-color: rgba(139, 92, 246, 0.5); }

.card-orange { color: #f59e0b; }
.card-orange:hover { border-color: rgba(245, 158, 11, 0.5); }

.card-red { color: #ef4444; }
.card-red:hover { border-color: rgba(239, 68, 68, 0.5); }

.card-cyan { color: #06b6d4; }
.card-cyan:hover { border-color: rgba(6, 182, 212, 0.5); }

.card-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.card-icon {
  position: relative;
  z-index: 2;
  font-size: 48px;
  filter: drop-shadow(0 4px 12px currentColor);
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  border-radius: 50%;
  filter: blur(20px);
  opacity: 0.3;
  transition: all 0.4s;
}

.report-card:hover .icon-glow {
  width: 90px;
  height: 90px;
  opacity: 0.5;
}

.glow-blue { background: #3b82f6; }
.glow-green { background: #10b981; }
.glow-purple { background: #8b5cf6; }
.glow-orange { background: #f59e0b; }
.glow-red { background: #ef4444; }
.glow-cyan { background: #06b6d4; }

.card-content h3 {
  font-size: 22px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 12px;
}

.card-content p {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 20px;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.feature-list li {
  font-size: 13px;
  color: #cbd5e1;
  font-weight: 600;
  padding: 8px 0;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

.feature-list li:last-child {
  border-bottom: none;
}

.btn-generate {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 14px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-generate svg {
  width: 20px;
  height: 20px;
}

.btn-generate:hover {
  background: currentColor;
  border-color: currentColor;
  color: #0f172a;
  transform: translateY(-2px);
}

.card-blue .btn-generate:hover { background: #3b82f6; }
.card-green .btn-generate:hover { background: #10b981; }
.card-purple .btn-generate:hover { background: #8b5cf6; }
.card-orange .btn-generate:hover { background: #f59e0b; }
.card-red .btn-generate:hover { background: #ef4444; }
.card-cyan .btn-generate:hover { background: #06b6d4; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .admin-reports-page {
    padding: 20px 12px;
  }

  .reports-grid {
    grid-template-columns: 1fr;
  }
}
</style>
