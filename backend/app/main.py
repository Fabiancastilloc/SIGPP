from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routers import auth, projects, expenses, catalogs
import os
from .routers import admin_users
from .routers import auth, projects, expenses, catalogs, members  # ← AGREGAR members

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear uploads directory
os.makedirs("/app/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routers import auth, projects, expenses, catalogs
import os

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS - MÁS PERMISIVO PARA DESARROLLO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear uploads directory
os.makedirs("/app/uploads", exist_ok=True)
try:
    app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")
except:
    pass  # Si falla, continuar sin montaje

# Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(catalogs.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(expenses.router, prefix=settings.API_V1_STR)
app.include_router(admin_users.router, prefix=settings.API_V1_STR)
app.include_router(members.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {
        "message": "SIGPP API v1.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}
