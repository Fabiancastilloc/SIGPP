<template>
  <div class="home">
    <!-- Hero Section Mejorado -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="gradient-orb orb-1"></div>
        <div class="gradient-orb orb-2"></div>
        <div class="gradient-orb orb-3"></div>
        <div class="particles">
          <div v-for="i in 50" :key="i" class="particle" 
               :style="{ 
                 left: Math.random() * 100 + '%', 
                 animationDelay: Math.random() * 3 + 's',
                 animationDuration: (3 + Math.random() * 4) + 's'
               }">
          </div>
        </div>
      </div>
      
      <div class="hero-content container">
        <div class="hero-badge fade-slide-up">
          <span class="badge-icon">🎓</span>
          Universidad de Cartagena
        </div>
        
        <h1 class="hero-title fade-slide-up" style="animation-delay: 0.1s">
          Sistema Integral de Gestión<br/>
          <span class="gradient-text">de Propuestas y Proyectos</span>
        </h1>
        
        <p class="hero-subtitle fade-slide-up" style="animation-delay: 0.2s">
          La plataforma digital definitiva para gestionar el ciclo completo de proyectos académicos
          con transparencia, eficiencia y control total del presupuesto
        </p>
        
        <div class="hero-cta fade-slide-up" style="animation-delay: 0.3s">
          <router-link to="/login" class="cta-btn cta-primary">
            <span class="btn-icon">🚀</span>
            Iniciar Sesión
            <span class="btn-arrow">→</span>
          </router-link>
          <router-link to="/register" class="cta-btn cta-secondary">
            <span class="btn-icon">✨</span>
            Crear Cuenta Gratis
          </router-link>
        </div>
        
        <div class="hero-stats fade-slide-up" style="animation-delay: 0.4s">
          <div class="stat-box">
            <div class="stat-number">500+</div>
            <div class="stat-label">Proyectos Gestionados</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">1000+</div>
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

    <!-- Features Section Premium -->
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
          <div class="feature-card" v-for="(feature, index) in features" :key="index">
            <div class="feature-icon-wrapper">
              <div class="feature-icon">{{ feature.icon }}</div>
              <div class="feature-icon-bg"></div>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <div class="feature-link">
              Saber más <span>→</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Workflow Visual -->
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
          <div class="timeline-item" v-for="(step, index) in workflowSteps" :key="index">
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
              <div class="benefit-item" v-for="(benefit, index) in benefits" :key="index">
                <div class="benefit-icon">{{ benefit.icon }}</div>
                <div>
                  <h4>{{ benefit.title }}</h4>
                  <p>{{ benefit.description }}</p>
                </div>
              </div>
            </div>
            <router-link to="/register" class="cta-btn cta-primary">
              Comenzar Ahora <span class="btn-arrow">→</span>
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
                  <circle cx="50" cy="50" r="40" class="ring-bg"/>
                  <circle cx="50" cy="50" r="40" class="ring-progress"/>
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

    <!-- CTA Final -->
    <section class="final-cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>¿Listo para transformar tu gestión de proyectos?</h2>
          <p>Únete a cientos de estudiantes y profesores que ya confían en SIGPP</p>
          <div class="cta-buttons">
            <router-link to="/register" class="cta-btn cta-large cta-primary">
              Crear Cuenta Gratis <span class="btn-arrow">→</span>
            </router-link>
            <router-link to="/login" class="cta-btn cta-large cta-secondary">
              Iniciar Sesión
            </router-link>
          </div>
          <p class="cta-note">✨ No requiere tarjeta de crédito · Configuración en 2 minutos</p>
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
          icon: '📝',
          title: 'Gestión Completa',
          description: 'Crea, edita y gestiona propuestas con flujo de aprobación multinivel y seguimiento en tiempo real'
        },
        {
          icon: '💰',
          title: 'Control Financiero',
          description: 'Seguimiento detallado de gastos, presupuesto disponible y notificaciones automáticas de alertas'
        },
        {
          icon: '📊',
          title: 'Reportes Avanzados',
          description: 'Genera reportes profesionales en PDF y Excel con análisis completo y trazabilidad total'
        },
        {
          icon: '🔐',
          title: 'Seguridad Total',
          description: 'Control de acceso basado en roles (RBAC) con autenticación segura y cifrado de datos'
        },
        {
          icon: '🔔',
          title: 'Notificaciones',
          description: 'Alertas en tiempo real sobre cambios de estado, acciones pendientes y actualizaciones importantes'
        },
        {
          icon: '📱',
          title: 'Multiplataforma',
          description: 'Acceso desde cualquier dispositivo con conexión a internet de forma segura y responsive'
        }
      ],
      workflowSteps: [
        {
          icon: '📝',
          title: 'Crear Propuesta',
          description: 'El estudiante documenta su proyecto con objetivos, descripción y presupuesto estimado'
        },
        {
          icon: '👨‍🏫',
          title: 'Validación Académica',
          description: 'El profesor revisa, valida o devuelve la propuesta con comentarios detallados'
        },
        {
          icon: '💼',
          title: 'Aprobación Financiera',
          description: 'El equipo financiero asigna presupuesto y activa el proyecto para ejecución'
        },
        {
          icon: '🚀',
          title: 'Ejecución y Seguimiento',
          description: 'Registro de gastos, aprobaciones y monitoreo continuo del progreso del proyecto'
        }
      ],
      benefits: [
        {
          icon: '⚡',
          title: 'Ahorra Tiempo',
          description: 'Automatiza procesos repetitivos y reduce trámites administrativos'
        },
        {
          icon: '🎯',
          title: 'Mayor Control',
          description: 'Visibilidad completa del estado de proyectos y presupuesto en tiempo real'
        },
        {
          icon: '🤝',
          title: 'Colaboración',
          description: 'Comunicación fluida entre estudiantes, profesores y área financiera'
        },
        {
          icon: '📈',
          title: 'Trazabilidad',
          description: 'Historial completo de cambios, aprobaciones y movimientos financieros'
        }
      ]
    }
  }
}
</script>

<style scoped>
.home {
  overflow-x: hidden;
}

/* Hero Section Premium */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  filter: blur(80px);
  opacity: 0.4;
  animation: float-orb 20s infinite ease-in-out;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #ff6b6b, #ffd93d);
  top: -300px;
  left: -300px;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #6bcf7f, #4facfe);
  bottom: -200px;
  right: -200px;
  animation-delay: -10s;
}

.orb-3 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  top: 50%;
  right: 10%;
  animation-delay: -15s;
}

@keyframes float-orb {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: white;
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
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100vh) translateX(50px);
    opacity: 0;
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  padding: 80px 20px;
  max-width: 1000px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.3);
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.badge-icon {
  font-size: 20px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 24px;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.gradient-text {
  background: linear-gradient(90deg, #fff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.7;
  opacity: 0.95;
  max-width: 700px;
  margin: 0 auto 40px;
}

.hero-cta {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 16px;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.cta-primary {
  background: white;
  color: #667eea;
}

.cta-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(255, 255, 255, 0.3);
}

.cta-secondary {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-4px);
}

.btn-icon {
  font-size: 20px;
}

.btn-arrow {
  transition: transform 0.3s;
}

.cta-btn:hover .btn-arrow {
  transform: translateX(4px);
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 32px;
  max-width: 900px;
  margin: 0 auto;
}

.stat-box {
  padding: 24px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s;
}

.stat-box:hover {
  transform: translateY(-4px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 8px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 500;
}

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
  opacity: 0.8;
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

/* Animations */
@keyframes fade-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-slide-up {
  animation: fade-slide-up 0.8s ease-out forwards;
  opacity: 0;
}

/* Features Section */
.features-section {
  padding: 120px 20px;
  background: white;
}

.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 60px;
}

.section-badge {
  display: inline-block;
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50px;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 16px;
  color: var(--gray-900);
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--gray-600);
  line-height: 1.7;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
}

.feature-card {
  padding: 40px 32px;
  background: white;
  border-radius: 20px;
  border: 2px solid var(--gray-200);
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
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transition: transform 0.4s;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
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
  background: linear-gradient(135deg, #667eea, #764ba2);
  opacity: 0.1;
  border-radius: 20px;
  transform: rotate(45deg);
  transition: transform 0.4s;
}

.feature-card:hover .feature-icon-bg {
  transform: rotate(0deg) scale(1.1);
}

.feature-card h3 {
  font-size: 1.4rem;
  margin-bottom: 12px;
  color: var(--gray-900);
}

.feature-card p {
  color: var(--gray-600);
  line-height: 1.7;
  margin-bottom: 16px;
}

.feature-link {
  color: #667eea;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.3s;
}

.feature-card:hover .feature-link {
  gap: 8px;
}

/* Workflow Section */
.workflow-section {
  padding: 120px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
}

.marker-number {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 900;
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.marker-pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #667eea;
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
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.timeline-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.timeline-content h4 {
  font-size: 1.2rem;
  margin-bottom: 12px;
  color: var(--gray-900);
}

.timeline-content p {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
}

.timeline-connector {
  position: absolute;
  top: 40px;
  left: calc(50% + 40px);
  width: calc(100% - 40px);
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  z-index: 1;
}

/* Benefits Section */
.benefits-section {
  padding: 120px 20px;
  background: white;
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
  gap: 16px;
  padding: 20px;
  background: var(--gray-50);
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.benefit-item:hover {
  border-color: #667eea;
  transform: translateX(8px);
}

.benefit-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.benefit-item h4 {
  font-size: 1.1rem;
  margin-bottom: 6px;
  color: var(--gray-900);
}

.benefit-item p {
  font-size: 14px;
  color: var(--gray-600);
  line-height: 1.6;
  margin: 0;
}

.benefit-visual {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  position: relative;
}

.visual-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 2px solid var(--gray-200);
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
  gap: 8px;
  margin-bottom: 16px;
  font-weight: 600;
}

.card-icon {
  font-size: 20px;
}

.card-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 80px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 4px;
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
  width: 100px;
  height: 100px;
  margin: 0 auto;
}

.ring-bg {
  fill: none;
  stroke: var(--gray-200);
  stroke-width: 8;
}

.ring-progress {
  fill: none;
  stroke: url(#gradient);
  stroke-width: 8;
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
  font-size: 24px;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-content h2 {
  font-size: 3rem;
  margin-bottom: 20px;
  color: white;
}

.cta-content > p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.95;
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.cta-large {
  padding: 20px 40px;
  font-size: 18px;
}

.cta-note {
  font-size: 14px;
  opacity: 0.8;
  margin: 0;
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
    font-size: 2rem;
  }
}
</style>
