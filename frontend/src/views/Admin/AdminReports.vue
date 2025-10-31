<template>
  <div class="admin-reports-page">
    <div class="container">
      <div class="page-header">
        <h1>📈 Reportes y Estadísticas</h1>
        <router-link to="/admin" class="btn-back">← Volver</router-link>
      </div>

      <div class="reports-grid">
        <div class="report-card">
          <h3>📊 Reporte General</h3>
          <p>Estadísticas generales del sistema</p>
          <button @click="generateReport('general')" class="btn-generate">Generar</button>
        </div>

        <div class="report-card">
          <h3>💰 Reporte Financiero</h3>
          <p>Análisis de presupuestos y gastos</p>
          <button @click="generateReport('financiero')" class="btn-generate">Generar</button>
        </div>

        <div class="report-card">
          <h3>👨‍🎓 Reporte de Estudiantes</h3>
          <p>Proyectos por estudiante</p>
          <button @click="generateReport('estudiantes')" class="btn-generate">Generar</button>
        </div>

        <div class="report-card">
          <h3>📋 Auditoría</h3>
          <p>Registro completo de actividades</p>
          <button @click="generateReport('auditoria')" class="btn-generate">Generar</button>
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
    const generateReport = (type) => {
      alert(`Generando reporte: ${type}`)
    }
    
    return { generateReport }
  }
}
</script>

<style scoped>
.admin-reports-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.btn-back {
  padding: 10px 20px;
  background: white;
  border-radius: 8px;
  text-decoration: none;
  color: var(--gray-700);
  font-weight: 600;
  border: 2px solid var(--gray-200);
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.report-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.report-card h3 {
  margin-bottom: 12px;
  font-size: 20px;
}

.report-card p {
  margin-bottom: 20px;
  color: var(--gray-600);
}

.btn-generate {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
</style>
