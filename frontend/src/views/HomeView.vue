<!-- frontend/src/views/Home.vue -->
<template>
  <div class="home-page">
    
    <!-- Hero Section Ultra Premium -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
        <div class="gradient-orb orb-3"></div>
        <div class="particles">
          <div 
            v-for="i in 30" 
            :key="i" 
            class="particle"
            :style="{
              left: Math.random() * 100 + '%',
              animationDelay: Math.random() * 5 + 's',
              animationDuration: (3 + Math.random() * 4) + 's'
            }"
          ></div>
        </div>
      </div>

      <div class="hero-content container">
        <div class="hero-badge fade-in">
          <span class="badge-icon">🎓</span>
          <span>Universidad de Cartagena</span>
        </div>

        <h1 class="hero-title fade-in" style="animation-delay: 0.1s">
          Sistema Integral de Gestión<br>
          <span class="gradient-text">de Propuestas y Proyectos</span>
        </h1>

        <p class="hero-subtitle fade-in" style="animation-delay: 0.2s">
          La plataforma digital definitiva para gestionar el ciclo completo de proyectos académicos 
          con transparencia, eficiencia y control total del presupuesto.
        </p>

        <div class="hero-cta fade-in" style="animation-delay: 0.3s">
          <router-link to="/login" class="cta-btn cta-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            <span>Iniciar Sesión</span>
            <span class="btn-arrow">→</span>
          </router-link>

          <router-link to="/register" class="cta-btn cta-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            <span>Crear Cuenta Gratis</span>
          </router-link>
        </div>

        <div class="hero-stats fade-in" style="animation-delay: 0.4s">
          <div class="stat-box">
            <div class="stat-number">500+</div>
            <div class="stat-label">Proyectos Gestionados</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">1,000+</div>
            <div class="stat-label">Estudiantes Activos</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">50+</div>
            <div class="stat-label">Profesores Asesores</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">$5B+</div>
            <div class="stat-label">Presupuesto Gestionado</div>
          </div>
        </div>
      </div>

      <div class="scroll-indicator">
        <span>Descubre más</span>
        <div class="scroll-arrow">↓</div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <span class="section-badge">Características</span>
          <h2 class="section-title">Todo lo que necesitas en un solo lugar</h2>
          <p class="section-subtitle">
            Herramientas poderosas diseñadas para simplificar la gestión de proyectos académicos
          </p>
        </div>

        <div class="features-grid">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="feature-card"
          >
            <div class="feature-icon-wrapper">
              <div class="feature-icon">{{ feature.icon }}</div>
              <div class="feature-icon-bg"></div>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <div class="feature-link">
              <span>Saber más</span>
              <span>→</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Workflow Section -->
    <section class="workflow-section">
      <div class="container">
        <div class="section-header">
          <span class="section-badge">Proceso</span>
          <h2 class="section-title">Flujo de trabajo simplificado</h2>
          <p class="section-subtitle">
            De la idea a la ejecución en cuatro pasos simples
          </p>
        </div>

        <div class="workflow-timeline">
          <div 
            v-for="(step, index) in workflowSteps" 
            :key="index"
            class="timeline-item"
          >
            <div class="timeline-marker">
              <div class="marker-number">{{ index + 1 }}</div>
              <div class="marker-pulse"></div>
            </div>
            <div class="timeline-content">
              <div class="timeline-icon">{{ step.icon }}</div>
              <h4>{{ step.title }}</h4>
              <p>{{ step.description }}</p>
            </div>
            <div v-if="index < workflowSteps.length - 1" class="timeline-connector"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section">
      <div class="container">
        <div class="benefits-grid">
          <div class="benefit-content">
            <span class="section-badge">Beneficios</span>
            <h2 class="section-title">¿Por qué elegir SIGPP?</h2>
            
            <div class="benefits-list">
              <div 
                v-for="(benefit, index) in benefits" 
                :key="index"
                class="benefit-item"
              >
                <div class="benefit-icon">{{ benefit.icon }}</div>
                <div>
                  <h4>{{ benefit.title }}</h4>
                  <p>{{ benefit.description }}</p>
                </div>
              </div>
            </div>

            <router-link to="/register" class="cta-btn cta-primary">
              Comenzar Ahora
              <span class="btn-arrow">→</span>
            </router-link>
          </div>

          <div class="benefit-visual">
            <div class="visual-card card-1">
              <div class="card-header">
                <span class="card-icon">📊</span>
                <span class="card-title">Dashboard</span>
              </div>
              <div class="card-chart">
                <div class="chart-bar" style="height: 60%"></div>
                <div class="chart-bar" style="height: 85%"></div>
                <div class="chart-bar" style="height: 45%"></div>
                <div class="chart-bar" style="height: 95%"></div>
              </div>
            </div>

            <div class="visual-card card-2">
              <div class="card-header">
                <span class="card-icon">💰</span>
                <span class="card-title">Presupuesto</span>
              </div>
              <div class="progress-ring">
                <svg viewBox="0 0 100 100">
                  ircle cx="50" cy="50" r="40" class="ring-bg" />
                  ircle cx="50" cy="50" r="40" class="ring-progress" />
                </svg>
                <div class="ring-text">75%</div>
              </div>
            </div>

            <div class="visual-card card-3">
              <div class="status-item status-success">
                <span class="status-dot"></span>
                <span>Proyecto Activo</span>
              </div>
              <div class="status-item status-pending">
                <span class="status-dot"></span>
                <span>En Revisión</span>
              </div>
              <div class="status-item status-complete">
                <span class="status-dot"></span>
                <span>Completado</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="final-cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>¿Listo para transformar tu gestión de proyectos?</h2>
          <p>Únete a cientos de estudiantes y profesores que ya confían en SIGPP</p>
          
          <div class="cta-buttons">
            <router-link to="/register" class="cta-btn cta-large cta-primary">
              Crear Cuenta Gratis
              <span class="btn-arrow">→</span>
            </router-link>
            <router-link to="/login" class="cta-btn cta-large cta-secondary">
              Iniciar Sesión
            </router-link>
          </div>

          <p class="cta-note">✓ Configuración en 2 minutos • Sin tarjeta de crédito</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      features: [
        {
          icon: '🚀',
          title: 'Gestión Completa',
          description: 'Crea, edita y gestiona propuestas con flujo de aprobación multinivel y seguimiento en tiempo real.'
        },
        {
          icon: '💰',
          title: 'Control Financiero',
          description: 'Seguimiento detallado de gastos, presupuesto disponible y notificaciones automáticas de alertas.'
        },
        {
          icon: '📊',
          title: 'Reportes Avanzados',
          description: 'Genera reportes profesionales en PDF y Excel con análisis completo y trazabilidad total.'
        },
        {
          icon: '🔒',
          title: 'Seguridad Total',
          description: 'Control de acceso basado en roles (RBAC) con autenticación segura y cifrado de datos.'
        },
        {
          icon: '🔔',
          title: 'Notificaciones',
          description: 'Alertas en tiempo real sobre cambios de estado, acciones pendientes y actualizaciones importantes.'
        },
        {
          icon: '📱',
          title: 'Multiplataforma',
          description: 'Acceso desde cualquier dispositivo con conexión a internet de forma segura y responsive.'
        }
      ],
      workflowSteps: [
        {
          icon: '📝',
          title: 'Crear Propuesta',
          description: 'El estudiante documenta su proyecto con objetivos, descripción y presupuesto estimado.'
        },
        {
          icon: '👨‍🏫',
          title: 'Validación Académica',
          description: 'El profesor revisa, valida o devuelve la propuesta con comentarios detallados.'
        },
        {
          icon: '💵',
          title: 'Aprobación Financiera',
          description: 'El equipo financiero asigna presupuesto y activa el proyecto para ejecución.'
        },
        {
          icon: '✅',
          title: 'Ejecución y Seguimiento',
          description: 'Registro de gastos, aprobaciones y monitoreo continuo del progreso del proyecto.'
        }
      ],
      benefits: [
        {
          icon: '⏱️',
          title: 'Ahorra Tiempo',
          description: 'Automatiza procesos repetitivos y reduce trámites administrativos.'
        },
        {
          icon: '📈',
          title: 'Mayor Control',
          description: 'Visibilidad completa del estado de proyectos y presupuesto en tiempo real.'
        },
        {
          icon: '🤝',
          title: 'Colaboración',
          description: 'Comunicación fluida entre estudiantes, profesores y área financiera.'
        },
        {
          icon: '🔍',
          title: 'Trazabilidad',
          description: 'Historial completo de cambios, aprobaciones y movimientos financieros.'
        }
      ]
    }
  }
}
</script>

<style scoped>
/* Base */
.home-page {
  overflow-x: hidden;
}

/* Hero Section Ultra Premium */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 50%, #0a0f1e 100%);
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.3;
  animation: float-orb 20s infinite ease-in-out;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #d4af37, #f3e5ab);
  top: -300px;
  left: -300px;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  bottom: -250px;
  right: -250px;
  animation-delay: -10s;
}

.orb-3 {
  width: 450px;
  height: 450px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 50%;
  right: 10%;
  animation-delay: -5s;
}

@keyframes float-orb {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(50px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-30px, 30px) scale(0.9);
  }
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(212, 175, 55, 0.6);
  border-radius: 50%;
  opacity: 0;
  animation: particle-float infinite ease-in-out;
}

@keyframes particle-float {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) translateX(50px);
    opacity: 0;
  }
}

/* Hero Content */
.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  padding: 80px 20px;
  max-width: 1100px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 28px;
  background: rgba(212, 175, 55, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  font-size: 15px;
  font-weight: 700;
  border: 2px solid rgba(212, 175, 55, 0.3);
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(212, 175, 55, 0.2);
}

.badge-icon {
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(212, 175, 55, 0.5));
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 28px;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.gradient-text {
  background: linear-gradient(90deg, #d4af37, #f3e5ab, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: gradient-flow 3s linear infinite;
}

@keyframes gradient-flow {
  to {
    background-position: 200% center;
  }
}

.hero-subtitle {
  font-size: 1.35rem;
  line-height: 1.8;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto 48px;
  color: #e0e7ff;
}

/* CTA Buttons */
.hero-cta {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 64px;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 18px 36px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 16px;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.cta-btn svg {
  width: 22px;
  height: 22px;
}

.cta-primary {
  background: linear-gradient(135deg, #d4af37 0%, #b8960f 100%);
  color: #0a0f1e;
}

.cta-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(212, 175, 55, 0.5);
}

.cta-secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: #d4af37;
  transform: translateY(-4px);
}

.btn-arrow {
  transition: transform 0.3s;
  font-size: 20px;
}

.cta-btn:hover .btn-arrow {
  transform: translateX(5px);
}

/* Hero Stats */
.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.stat-box {
  padding: 28px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.stat-box:hover {
  transform: translateY(-4px);
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.3);
}

.stat-number {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 8px;
  color: #d4af37;
  text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
}

.stat-label {
  font-size: 0.95rem;
  opacity: 0.85;
  font-weight: 600;
  color: #cbd5e1;
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 600;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-10px);
  }
}

.scroll-arrow {
  font-size: 24px;
  animation: arrow-bounce 2s infinite;
}

@keyframes arrow-bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(10px);
  }
}

/* Fade In Animation */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fade-in 0.8s ease-out forwards;
  opacity: 0;
}

/* Features Section */
.features-section {
  padding: 120px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e0e7ff 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 64px;
}

.section-badge {
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(135deg, #d4af37, #b8960f);
  color: white;
  border-radius: 50px;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.section-title {
  font-size: 2.75rem;
  margin-bottom: 20px;
  color: #1e293b;
  font-weight: 900;
}

.section-subtitle {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.7;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 32px;
}

.feature-card {
  padding: 40px 32px;
  background: white;
  border-radius: 20px;
  border: 2px solid #e2e8f0;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #d4af37, #b8960f);
  transform: scaleX(0);
  transition: transform 0.4s;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: #d4af37;
}

.feature-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.feature-icon {
  position: relative;
  z-index: 2;
  font-size: 48px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.feature-icon-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(212, 175, 55, 0.05));
  opacity: 0.5;
  border-radius: 20px;
  transform: rotate(45deg);
  transition: transform 0.4s;
}

.feature-card:hover .feature-icon-bg {
  transform: rotate(0deg) scale(1.1);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 12px;
  color: #1e293b;
  font-weight: 800;
}

.feature-card p {
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 16px;
}

.feature-link {
  color: #d4af37;
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: gap 0.3s;
}

.feature-card:hover .feature-link {
  gap: 10px;
}

/* Workflow Section */
.workflow-section {
  padding: 120px 20px;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  color: white;
}

.workflow-timeline {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.timeline-item {
  position: relative;
  text-align: center;
}

.timeline-marker {
  position: relative;
  width: 90px;
  height: 90px;
  margin: 0 auto 24px;
}

.marker-number {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #d4af37, #b8960f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 900;
  color: #0a0f1e;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.4);
}

.marker-pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid #d4af37;
  animation: pulse-ring 2s infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.timeline-content {
  background: rgba(255, 255, 255, 0.05);
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.timeline-content:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: rgba(212, 175, 55, 0.3);
  transform: translateY(-4px);
}

.timeline-icon {
  font-size: 48px;
  margin-bottom: 16px;
  filter: drop-shadow(0 2px 8px rgba(212, 175, 55, 0.3));
}

.timeline-content h4 {
  font-size: 1.3rem;
  margin-bottom: 12px;
  color: #d4af37;
  font-weight: 800;
}

.timeline-content p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

.timeline-connector {
  position: absolute;
  top: 45px;
  left: calc(50% + 45px);
  width: calc(100% - 90px);
  height: 3px;
  background: linear-gradient(90deg, #d4af37, transparent);
  z-index: 1;
}

/* Benefits Section */
.benefits-section {
  padding: 120px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e0e7ff 100%);
}

.benefits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin: 32px 0;
}

.benefit-item {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.benefit-item:hover {
  border-color: #d4af37;
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.2);
}

.benefit-icon {
  font-size: 36px;
  flex-shrink: 0;
  filter: drop-shadow(0 2px 4px rgba(212, 175, 55, 0.3));
}

.benefit-item h4 {
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 800;
}

.benefit-item p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* Visual Cards */
.benefit-visual {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  position: relative;
}

.visual-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 2px solid #e2e8f0;
}

.card-1 {
  grid-column: 1 / 2;
  animation: float-card 3s infinite ease-in-out;
}

.card-2 {
  grid-column: 2 / 3;
  animation: float-card 3s infinite ease-in-out;
  animation-delay: -1.5s;
}

.card-3 {
  grid-column: 1 / 3;
  animation: float-card 3s infinite ease-in-out;
  animation-delay: -1s;
}

@keyframes float-card {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-weight: 700;
  color: #1e293b;
}

.card-icon {
  font-size: 24px;
}

.card-chart {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  height: 100px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(135deg, #d4af37, #b8960f);
  border-radius: 8px 8px 0 0;
  animation: bar-grow 1s ease-out;
}

@keyframes bar-grow {
  from {
    transform: scaleY(0);
  }
  to {
    transform: scaleY(1);
  }
}

.progress-ring {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.ring-bg {
  fill: none;
  stroke: #e2e8f0;
  stroke-width: 10;
}

.ring-progress {
  fill: none;
  stroke: #d4af37;
  stroke-width: 10;
  stroke-linecap: round;
  stroke-dasharray: 251;
  stroke-dashoffset: 63;
  animation: ring-fill 2s ease-out;
}

@keyframes ring-fill {
  from {
    stroke-dashoffset: 251;
  }
}

.ring-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  font-weight: 900;
  color: #d4af37;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.status-success {
  background: #d1fae5;
  color: #059669;
}

.status-pending {
  background: #dbeafe;
  color: #2563eb;
}

.status-complete {
  background: #fef3c7;
  color: #d97706;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Final CTA */
.final-cta-section {
  padding: 120px 20px;
  background: linear-gradient(135deg, #0a0f1e 0%, #1a1f35 100%);
  color: white;
  text-align: center;
}

.cta-content h2 {
  font-size: 3.5rem;
  margin-bottom: 24px;
  color: white;
  font-weight: 900;
}

.cta-content > p {
  font-size: 1.25rem;
  margin-bottom: 48px;
  opacity: 0.9;
  color: #cbd5e1;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 28px;
}

.cta-large {
  padding: 22px 44px;
  font-size: 18px;
}

.cta-note {
  font-size: 15px;
  opacity: 0.7;
  margin: 0;
  color: #94a3b8;
}

/* Responsive */
@media (max-width: 968px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .workflow-timeline {
    grid-template-columns: 1fr;
  }
  
  .timeline-connector {
    display: none;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
  
  .benefit-visual {
    order: -1;
  }
  
  .cta-content h2 {
    font-size: 2.25rem;
  }
  
  .hero-stats {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
