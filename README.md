# SIGPP - Sistema Integral de Gestión Presupuestal para Proyectos

## Universidad de Cartagena - Facultad de Ingeniería

### Programa de Ingeniería de Software

Sistema web para gestionar presupuestos de proyectos de grado.

## Stack Tecnológico

- **Backend:** FastAPI (Python 3.12)
- **Frontend:** Vue.js 3 + Vite
- **Base de Datos:** PostgreSQL 16
- **Estado Global:** Pinia
- **Estilos:** CSS3

## Estructura del Proyecto

SIGPP/
├── backend/ # API REST con FastAPI
├── frontend/ # Aplicación Vue.js
├── database/ # Scripts SQL
└── docs/ # Documentación

text

## Instalación y Ejecución

### Backend

cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

text

### Frontend

cd frontend
npm install
npm run dev

text

## Equipo de Desarrollo - CIPA Codex

- Stivenson García Romero
- Fabian Castillo Carmona
- Joiner Marimon Blanco
- Neider Barrios Villalba
- Keyner Infante Castaño

**Docente:** Rosmery Canabal Mestre

## Licencia

© 2025 Universidad de Cartagena. Todos los derechos reservados.
