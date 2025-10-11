<template>
  <footer class="footer-bar">
    <div class="footer-container">
      <!-- Sección Superior -->
      <div class="footer-top">
        <div class="footer-section">
          <div class="footer-brand">
            <span class="brand-icon">🎓</span>
            <h3 class="brand-name">SIGPP</h3>
          </div>
          <p class="brand-description">
            Sistema de Gestión de Proyectos de Grado para la Universidad de Cartagena
          </p>
          <div class="social-links">
            <a href="https://www.unicartagena.edu.co" target="_blank" class="social-link" title="Sitio Web">
              🌐
            </a>
            <a href="https://facebook.com/unicartagena" target="_blank" class="social-link" title="Facebook">
              📘
            </a>
            <a href="https://twitter.com/unicartagena" target="_blank" class="social-link" title="Twitter">
              🐦
            </a>
            <a href="https://instagram.com/unicartagena" target="_blank" class="social-link" title="Instagram">
              📸
            </a>
          </div>
        </div>

        <div class="footer-section">
          <h4 class="section-title">Enlaces Rápidos</h4>
          <ul class="footer-links">
            <li><router-link to="/dashboard" class="footer-link">Dashboard</router-link></li>
            <li><router-link to="/proyectos" class="footer-link">Proyectos</router-link></li>
            <li><router-link to="/gastos" class="footer-link">Gastos</router-link></li>
            <li><a href="#" @click.prevent="abrirAyuda" class="footer-link">Ayuda</a></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="section-title">Recursos</h4>
          <ul class="footer-links">
            <li><a href="#" @click.prevent="abrirDocumentacion" class="footer-link">Documentación</a></li>
            <li><a href="#" @click.prevent="abrirTutoriales" class="footer-link">Tutoriales</a></li>
            <li><a href="#" @click.prevent="abrirFAQ" class="footer-link">Preguntas Frecuentes</a></li>
            <li><a href="#" @click.prevent="reportarProblema" class="footer-link">Reportar Problema</a></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="section-title">Contacto</h4>
          <ul class="footer-contact">
            <li class="contact-item">
              <span class="contact-icon">📧</span>
              <a href="mailto:sigpp@unicartagena.edu.co" class="contact-link">
                sigpp@unicartagena.edu.co
              </a>
            </li>
            <li class="contact-item">
              <span class="contact-icon">📞</span>
              <span class="contact-text">(+57) 5 6698179</span>
            </li>
            <li class="contact-item">
              <span class="contact-icon">📍</span>
              <span class="contact-text">Cartagena de Indias, Colombia</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Separador -->
      <div class="footer-divider"></div>

      <!-- Sección Inferior -->
      <div class="footer-bottom">
        <div class="footer-info">
          <p class="copyright">
            © {{ currentYear }} Universidad de Cartagena. Todos los derechos reservados.
          </p>
          <p class="version">
            SIGPP v1.0.0 | Desarrollado con ❤️ por el Equipo de Desarrollo
          </p>
        </div>
        <div class="footer-legal">
          <a href="#" @click.prevent="abrirTerminos" class="legal-link">Términos de Uso</a>
          <span class="separator">•</span>
          <a href="#" @click.prevent="abrirPrivacidad" class="legal-link">Política de Privacidad</a>
          <span class="separator">•</span>
          <a href="#" @click.prevent="abrirCookies" class="legal-link">Cookies</a>
        </div>
      </div>

      <!-- Sello de Calidad -->
      <div class="footer-seal">
        <div class="seal-item">
          <span class="seal-icon">🏆</span>
          <span class="seal-text">Acreditación de Alta Calidad</span>
        </div>
        <div class="seal-item">
          <span class="seal-icon">🔒</span>
          <span class="seal-text">Datos Seguros</span>
        </div>
        <div class="seal-item">
          <span class="seal-icon">✅</span>
          <span class="seal-text">100% Confiable</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentYear = computed(() => new Date().getFullYear())

const abrirAyuda = () => {
  alert('📖 Guía de Ayuda\n\nAccede a los tutoriales y guías de uso del sistema.')
}

const abrirDocumentacion = () => {
  window.open('https://docs.sigpp.unicartagena.edu.co', '_blank')
}

const abrirTutoriales = () => {
  alert('🎥 Tutoriales\n\nAccede a videos y guías paso a paso.')
}

const abrirFAQ = () => {
  alert('❓ Preguntas Frecuentes\n\n¿Tienes dudas? Consulta nuestras FAQ.')
}

const reportarProblema = () => {
  alert('🐛 Reportar Problema\n\nEnvía un correo a: soporte@unicartagena.edu.co')
}

const abrirTerminos = () => {
  alert('📄 Términos de Uso del SIGPP')
}

const abrirPrivacidad = () => {
  alert('🔒 Política de Privacidad')
}

const abrirCookies = () => {
  alert('🍪 Política de Cookies')
}
</script>

<style scoped>
.footer-bar {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: white;
  margin-top: auto;
  border-top: 4px solid var(--primary);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-10) var(--space-8);
}

.footer-top {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-8);
  margin-bottom: var(--space-8);
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-2);
}

.brand-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 900;
  color: white;
  margin: 0;
  letter-spacing: 0.5px;
}

.brand-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  font-size: 0.9375rem;
}

.social-links {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.social-link {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  font-size: 1.25rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  margin: 0 0 var(--space-3) 0;
  letter-spacing: 0.3px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  display: inline-block;
  position: relative;
  padding-left: var(--space-2);
}

.footer-link::before {
  content: '→';
  position: absolute;
  left: 0;
  opacity: 0;
  transition: all 0.2s ease;
}

.footer-link:hover {
  color: white;
  padding-left: var(--space-4);
  transform: translateX(4px);
}

.footer-link:hover::before {
  opacity: 1;
}

.footer-contact {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9375rem;
}

.contact-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.contact-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.2s ease;
  word-break: break-word;
}

.contact-link:hover {
  color: white;
  text-decoration: underline;
}

.contact-text {
  color: rgba(255, 255, 255, 0.8);
}

.footer-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.2), transparent);
  margin: var(--space-8) 0;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.copyright,
.version {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.footer-legal {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.legal-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.legal-link:hover {
  color: white;
  text-decoration: underline;
}

.separator {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.875rem;
}

.footer-seal {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-8);
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
}

.seal-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.seal-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.seal-icon {
  font-size: 1.5rem;
}

.seal-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer-container {
    padding: var(--space-8) var(--space-4);
  }

  .footer-top {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }

  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }

  .footer-legal {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-2);
  }

  .separator {
    display: none;
  }

  .footer-seal {
    flex-direction: column;
    gap: var(--space-3);
  }

  .seal-item {
    width: 100%;
    justify-content: center;
  }

  .social-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .brand-name {
    font-size: 1.5rem;
  }

  .brand-icon {
    font-size: 2rem;
  }

  .footer-seal {
    gap: var(--space-2);
  }
}
</style>