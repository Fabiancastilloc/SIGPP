from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SIGPP - Sistema Integral de Gestión Presupuestal",
    description="API REST para gestión de proyectos de grado - Universidad de Cartagena",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "SIGPP API - Universidad de Cartagena",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
