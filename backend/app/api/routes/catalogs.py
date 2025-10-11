from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from pydantic import BaseModel, Field
from app.api.dependencies import get_db

router = APIRouter()

# ==================== SCHEMAS ====================
class CatalogResponse(BaseModel):
    id: int
    nombre: str

class CarreraResponse(BaseModel):
    id: int
    nombre: str
    facultad_id: int

class CatalogCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120)

class CarreraCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120)
    facultad_id: int

# ==================== FACULTADES ====================
@router.get("/facultades", response_model=List[CatalogResponse])
def listar_facultades(db: Session = Depends(get_db)):
    """Obtener todas las facultades disponibles"""
    result = db.execute(text("SELECT id, nombre FROM facultades ORDER BY nombre"))
    return [{"id": row[0], "nombre": row[1]} for row in result.fetchall()]

@router.post("/facultades", response_model=CatalogResponse, status_code=status.HTTP_201_CREATED)
def crear_facultad(data: CatalogCreate, db: Session = Depends(get_db)):
    """Crear una nueva facultad"""
    try:
        result = db.execute(
            text("INSERT INTO facultades (nombre) VALUES (:nombre) RETURNING id, nombre"),
            {"nombre": data.nombre}
        )
        db.commit()
        row = result.fetchone()
        return {"id": row[0], "nombre": row[1]}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La facultad ya existe o hubo un error al crearla"
        )

# ==================== SEDES ====================
@router.get("/sedes", response_model=List[CatalogResponse])
def listar_sedes(db: Session = Depends(get_db)):
    """
    Obtener todas las sedes válidas de la Universidad de Cartagena:
    - Piedra de Bolívar
    - Zaragocilla
    - San Pablo
    - El Carmen de Bolívar
    """
    result = db.execute(text("SELECT id, nombre FROM sedes ORDER BY nombre"))
    return [{"id": row[0], "nombre": row[1]} for row in result.fetchall()]

@router.post("/sedes", response_model=CatalogResponse, status_code=status.HTTP_201_CREATED)
def crear_sede(data: CatalogCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva sede (solo sedes válidas de la Universidad de Cartagena)
    """
    # Validar que sea una sede válida
    sedes_validas = ["Piedra de Bolívar", "Zaragocilla", "San Pablo", "El Carmen de Bolívar"]
    
    if data.nombre not in sedes_validas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sede no válida. Sedes permitidas: {', '.join(sedes_validas)}"
        )
    
    try:
        result = db.execute(
            text("INSERT INTO sedes (nombre) VALUES (:nombre) RETURNING id, nombre"),
            {"nombre": data.nombre}
        )
        db.commit()
        row = result.fetchone()
        return {"id": row[0], "nombre": row[1]}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sede ya existe o hubo un error al crearla"
        )

# ==================== CARRERAS ====================
@router.get("/carreras", response_model=List[CarreraResponse])
def listar_carreras(
    facultad_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener todas las carreras (opcionalmente filtradas por facultad)"""
    if facultad_id:
        result = db.execute(
            text("SELECT id, nombre, facultad_id FROM carreras WHERE facultad_id = :fid ORDER BY nombre"),
            {"fid": facultad_id}
        )
    else:
        result = db.execute(text("SELECT id, nombre, facultad_id FROM carreras ORDER BY nombre"))
    
    return [{"id": row[0], "nombre": row[1], "facultad_id": row[2]} for row in result.fetchall()]

@router.post("/carreras", response_model=CarreraResponse, status_code=status.HTTP_201_CREATED)
def crear_carrera(data: CarreraCreate, db: Session = Depends(get_db)):
    """Crear una nueva carrera"""
    try:
        result = db.execute(
            text("INSERT INTO carreras (nombre, facultad_id) VALUES (:nombre, :fid) RETURNING id, nombre, facultad_id"),
            {"nombre": data.nombre, "fid": data.facultad_id}
        )
        db.commit()
        row = result.fetchone()
        return {"id": row[0], "nombre": row[1], "facultad_id": row[2]}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La carrera ya existe o hubo un error al crearla"
        )
