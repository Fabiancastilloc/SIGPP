<template>
  <div class="not-found-page">
    <div class="content">
      <h1>404</h1>
      <h2>Página No Encontrada</h2>
      <p>La página que buscas no existe</p>
      <router-link to="/" class="btn-home">🏠 Volver al Inicio</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

h1 {
  font-size: 120px;
  margin: 0;
  font-weight: 800;
}

h2 {
  font-size: 32px;
  margin: 20px 0;
}

p {
  font-size: 18px;
  margin-bottom: 32px;
  opacity: 0.9;
}

.btn-home {
  display: inline-block;
  padding: 14px 32px;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  transition: transform 0.3s;
}

.btn-home:hover {
  transform: translateY(-2px);
}
</style>
