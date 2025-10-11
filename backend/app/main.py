from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
import os
from dotenv import load_dotenv
from app.api.routes import auth, projects
from app.api.routes import auth, projects, expenses, dashboard, reports
from app.api.routes import auth, projects, expenses, dashboard, reports, catalogs



# Cargar variables de entorno
load_dotenv()

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="SIGPP - Sistema Integral de Gestión Presupuestal",
    description="API REST para gestión de proyectos de grado - Universidad de Cartagena",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuración de CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de base de datos
def get_db():
    """
    Dependencia que proporciona una sesión de base de datos.
    Se cierra automáticamente después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== ENDPOINTS BÁSICOS ====================

@app.get("/")
def root():
    """
    Endpoint raíz - Información básica de la API
    """
    return {
        "message": "SIGPP API - Universidad de Cartagena",
        "proyecto": "Sistema Integral de Gestión Presupuestal para Proyectos de Grado",
        "version": "1.0.0",
        "status": "online",
        "documentacion": "/api/docs"
    }

@app.get("/api/health")
def health_check():
    """
    Endpoint de health check - Verifica que el servicio está funcionando
    """
    return {
        "status": "healthy",
        "service": "SIGPP Backend",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/db-test")
def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint para probar la conexión a la base de datos PostgreSQL
    
    Retorna:
    - db_connection: "ok" si la conexión es exitosa
    - database: nombre de la base de datos
    - message: mensaje descriptivo
    """
    try:
        # Ejecutar una consulta simple para verificar la conexión
        result = db.execute("SELECT 1 as test;")
        test_value = result.scalar()
        
        # Obtener información de la base de datos
        db_name_result = db.execute("SELECT current_database();")
        db_name = db_name_result.scalar()
        
        # Contar tablas en el schema public
        tables_result = db.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables_count = tables_result.scalar()
        
        return {
            "db_connection": "ok" if test_value == 1 else "fail",
            "database": db_name,
            "tables_count": tables_count,
            "message": "Conexión a PostgreSQL exitosa"
        }
    except Exception as e:
        return {
            "db_connection": "error",
            "error": str(e),
            "message": "Error al conectar con la base de datos"
        }

@app.get("/api/db-info")
def get_database_info(db: Session = Depends(get_db)):
    """
    Endpoint que retorna información detallada de la base de datos
    
    Retorna información sobre:
    - Versión de PostgreSQL
    - Nombre de la base de datos
    - Lista de tablas disponibles
    """
    try:
        # Versión de PostgreSQL
        version_result = db.execute("SELECT version();")
        pg_version = version_result.scalar()
        
        # Nombre de la base de datos
        db_name_result = db.execute("SELECT current_database();")
        db_name = db_name_result.scalar()
        
        # Listar todas las tablas
        tables_result = db.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in tables_result.fetchall()]
        
        return {
            "status": "success",
            "postgresql_version": pg_version,
            "database_name": db_name,
            "tables": tables,
            "tables_count": len(tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# ==================== EVENTOS DE CICLO DE VIDA ====================

@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación
    """
    print("=" * 60)
    print("🚀 SIGPP Backend iniciado correctamente")
    print(f"📚 Documentación disponible en: http://localhost:8000/api/docs")
    print(f"🗄️  Base de datos: PostgreSQL")
    print(f"🌍 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación
    """
    print("=" * 60)
    print("⏹️  SIGPP Backend detenido")
    print("=" * 60)

# ==================== IMPORTAR Y REGISTRAR ROUTERS ====================

# Importar routers
from app.api.routes import auth

# Incluir routers en la aplicación
app.include_router(
    auth.router, 
    prefix="/api/v1/auth", 
    tags=["Autenticación"]
)

app.include_router(
    projects.router,
    prefix="/api/v1/projects",
    tags=["Proyectos"]
)

app.include_router(
    expenses.router,
    prefix="/api/v1/expenses",
    tags=["Gastos"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    reports.router,
    prefix="/api/v1/reports",
    tags=["Reportes"]
)

app.include_router(
    catalogs.router,
    prefix="/api/v1/catalogs",
    tags=["Catálogos"]
)
# Descomentar cuando crees estos routers:
# from app.api.routes import projects, expenses, dashboard, reports
# 
# app.include_router(
#     projects.router, 
#     prefix="/api/v1/projects", 
#     tags=["Proyectos"]
# )
# 
# app.include_router(
#     expenses.router, 
#     prefix="/api/v1/expenses", 
#     tags=["Gastos"]
# )
# 
# app.include_router(
#     dashboard.router, 
#     prefix="/api/v1/dashboard", 
#     tags=["Dashboard"]
# )
# 
# app.include_router(
#     reports.router, 
#     prefix="/api/v1/reports", 
#     tags=["Reportes"]
# )
