# backend/app/routers/catalogs.py
"""
Router de Catálogos - SIGPP
Proporciona endpoints para datos maestros del sistema:
- Sedes, Facultades, Carreras
- Profesores
- Estudiantes (filtrados por carrera)
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models.user import Sede, Facultad, Carrera, User, RoleEnum
from ..utils.permissions import get_current_user

router = APIRouter(prefix="/catalogs", tags=["Catálogos"])


# ==================== SEDES ====================

@router.get("/sedes")
def get_sedes(db: Session = Depends(get_db)):
    """
    Obtener todas las sedes disponibles
    
    Returns:
        Lista de sedes con id, nombre y código
    """
    sedes = db.query(Sede).order_by(Sede.nombre).all()
    
    return [{
        "id": s.id,
        "nombre": s.nombre,
        "codigo": s.codigo
    } for s in sedes]


# ==================== FACULTADES ====================

@router.get("/facultades")
def get_facultades(
    sede_id: Optional[int] = Query(None, description="Filtrar por ID de sede"),
    db: Session = Depends(get_db)
):
    """
    Obtener facultades, opcionalmente filtradas por sede
    
    Args:
        sede_id: ID de la sede para filtrar (opcional)
    
    Returns:
        Lista de facultades con id, nombre, código y sede_id
    """
    query = db.query(Facultad)
    
    # Filtrar por sede si se proporciona
    if sede_id:
        query = query.filter(Facultad.sede_id == sede_id)
    
    facultades = query.order_by(Facultad.nombre).all()
    
    return [{
        "id": f.id,
        "nombre": f.nombre,
        "codigo": f.codigo,
        "sede_id": f.sede_id,
        "sede": {
            "id": f.sede.id,
            "nombre": f.sede.nombre
        } if f.sede else None
    } for f in facultades]


# ==================== CARRERAS ====================

@router.get("/carreras")
def get_carreras(
    facultad_id: Optional[int] = Query(None, description="Filtrar por ID de facultad"),
    db: Session = Depends(get_db)
):
    """
    Obtener carreras, opcionalmente filtradas por facultad
    
    Args:
        facultad_id: ID de la facultad para filtrar (opcional)
    
    Returns:
        Lista de carreras con id, nombre, código, duración y modalidad
    """
    query = db.query(Carrera)
    
    # Filtrar por facultad si se proporciona
    if facultad_id:
        query = query.filter(Carrera.facultad_id == facultad_id)
    
    carreras = query.order_by(Carrera.nombre).all()
    
    return [{
        "id": c.id,
        "nombre": c.nombre,
        "codigo": c.codigo,
        "facultad_id": c.facultad_id,
        "duracion_semestres": c.duracion_semestres,
        "modalidad": c.modalidad,
        "facultad": {
            "id": c.facultad.id,
            "nombre": c.facultad.nombre
        } if c.facultad else None
    } for c in carreras]


# ==================== PROFESORES ====================

@router.get("/profesores")
def get_profesores(
    facultad_id: Optional[int] = Query(None, description="Filtrar por facultad"),
    db: Session = Depends(get_db)
):
    """
    Obtener SOLO profesores activos
    
    Args:
        facultad_id: ID de facultad para filtrar (opcional)
    
    Returns:
        Lista de profesores con id, nombre, email y facultad
    """
    query = db.query(User).filter(
        User.rol == RoleEnum.PROFESOR,
        User.is_active == True
    )
    
    # Filtrar por facultad si se proporciona
    if facultad_id:
        query = query.filter(User.facultad_id == facultad_id)
    
    profesores = query.order_by(User.nombre_completo).all()
    
    print(f"📚 Profesores encontrados: {len(profesores)}")
    
    return [{
        "id": p.id,
        "nombre_completo": p.nombre_completo,
        "email": p.email,
        "codigo_institucional": p.codigo_institucional,
        "facultad_id": p.facultad_id,
        "facultad": {
            "id": p.facultad.id,
            "nombre": p.facultad.nombre
        } if p.facultad else None
    } for p in profesores]


# ==================== ESTUDIANTES - MISMA CARRERA ====================

@router.get("/students/same-career")
def get_students_same_career(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener estudiantes de la MISMA CARRERA que el usuario actual
    
    Solo devuelve estudiantes activos de la misma carrera,
    excluyendo al usuario que realiza la petición.
    
    Returns:
        Lista de estudiantes disponibles para colaboración
    """
    # Verificar que el usuario actual es estudiante
    if current_user.rol.value != "estudiante":
        return []
    
    # Verificar que el usuario tiene carrera asignada
    if not current_user.carrera_id:
        return []
    
    # Obtener estudiantes de la misma carrera
    students = db.query(User).filter(
        User.rol == RoleEnum.ESTUDIANTE,
        User.carrera_id == current_user.carrera_id,
        User.id != current_user.id,  # Excluir al usuario actual
        User.is_active == True
    ).order_by(User.nombre_completo).all()
    
    print(f"🎓 Estudiantes de la carrera {current_user.carrera_id}: {len(students)}")
    
    return [{
        "id": s.id,
        "nombre_completo": s.nombre_completo,
        "email": s.email,
        "codigo_institucional": s.codigo_institucional,
        "semestre": s.semestre,
        "carrera_id": s.carrera_id,
        "carrera": {
            "id": s.carrera.id,
            "nombre": s.carrera.nombre
        } if s.carrera else None
    } for s in students]


# ==================== BÚSQUEDA DE ESTUDIANTES ====================

@router.get("/students/search")
def search_students(
    q: str = Query("", min_length=0, max_length=100, description="Término de búsqueda"),
    carrera_id: Optional[int] = Query(None, description="Filtrar por carrera"),
    semestre: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por semestre"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar estudiantes por nombre o código institucional
    
    Args:
        q: Término de búsqueda (nombre o código)
        carrera_id: Filtrar por carrera específica
        semestre: Filtrar por semestre específico
        limit: Número máximo de resultados
    
    Returns:
        Lista de estudiantes que coinciden con la búsqueda
    """
    # Base query: solo estudiantes activos, excluyendo al usuario actual
    query = db.query(User).filter(
        User.rol == RoleEnum.ESTUDIANTE,
        User.id != current_user.id,
        User.is_active == True
    )
    
    # Filtrar por carrera si se proporciona
    if carrera_id:
        query = query.filter(User.carrera_id == carrera_id)
    
    # Filtrar por semestre si se proporciona
    if semestre:
        query = query.filter(User.semestre == semestre)
    
    # Buscar por nombre o código si hay término de búsqueda
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            (User.nombre_completo.ilike(search_term)) |
            (User.codigo_institucional.ilike(search_term)) |
            (User.email.ilike(search_term))
        )
    
    # Ordenar y limitar resultados
    students = query.order_by(User.nombre_completo).limit(limit).all()
    
    print(f"🔍 Búsqueda '{q}': {len(students)} resultados")
    
    return [{
        "id": s.id,
        "nombre_completo": s.nombre_completo,
        "email": s.email,
        "codigo_institucional": s.codigo_institucional,
        "semestre": s.semestre,
        "carrera_id": s.carrera_id,
        "carrera": {
            "id": s.carrera.id,
            "nombre": s.carrera.nombre
        } if s.carrera else None
    } for s in students]


# ==================== ESTUDIANTES POR CARRERA ====================

@router.get("/students/by-career/{carrera_id}")
def get_students_by_career(
    carrera_id: int,
    semestre: Optional[int] = Query(None, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los estudiantes de una carrera específica
    
    Args:
        carrera_id: ID de la carrera
        semestre: Filtrar por semestre (opcional)
    
    Returns:
        Lista de estudiantes de la carrera especificada
    """
    query = db.query(User).filter(
        User.rol == RoleEnum.ESTUDIANTE,
        User.carrera_id == carrera_id,
        User.id != current_user.id,
        User.is_active == True
    )
    
    if semestre:
        query = query.filter(User.semestre == semestre)
    
    students = query.order_by(User.semestre, User.nombre_completo).all()
    
    return [{
        "id": s.id,
        "nombre_completo": s.nombre_completo,
        "email": s.email,
        "codigo_institucional": s.codigo_institucional,
        "semestre": s.semestre,
        "carrera_id": s.carrera_id
    } for s in students]


# ==================== ESTADÍSTICAS ====================

@router.get("/stats")
def get_catalog_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener estadísticas generales de catálogos
    
    Returns:
        Contadores de sedes, facultades, carreras, profesores y estudiantes
    """
    stats = {
        "sedes": db.query(Sede).count(),
        "facultades": db.query(Facultad).count(),
        "carreras": db.query(Carrera).count(),
        "profesores": db.query(User).filter(
            User.rol == RoleEnum.PROFESOR,
            User.is_active == True
        ).count(),
        "estudiantes": db.query(User).filter(
            User.rol == RoleEnum.ESTUDIANTE,
            User.is_active == True
        ).count()
    }
    
    # Si el usuario es estudiante, agregar stats de su carrera
    if current_user.rol.value == "estudiante" and current_user.carrera_id:
        stats["estudiantes_misma_carrera"] = db.query(User).filter(
            User.rol == RoleEnum.ESTUDIANTE,
            User.carrera_id == current_user.carrera_id,
            User.id != current_user.id,
            User.is_active == True
        ).count()
    
    return stats


# ==================== INFORMACIÓN DE CARRERA ====================

@router.get("/carrera/{carrera_id}/info")
def get_carrera_info(
    carrera_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener información completa de una carrera
    
    Args:
        carrera_id: ID de la carrera
    
    Returns:
        Información detallada de la carrera con facultad y sede
    """
    carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    
    if not carrera:
        return None
    
    # Contar estudiantes activos en esta carrera
    total_estudiantes = db.query(User).filter(
        User.rol == RoleEnum.ESTUDIANTE,
        User.carrera_id == carrera_id,
        User.is_active == True
    ).count()
    
    return {
        "id": carrera.id,
        "nombre": carrera.nombre,
        "codigo": carrera.codigo,
        "duracion_semestres": carrera.duracion_semestres,
        "modalidad": carrera.modalidad,
        "facultad": {
            "id": carrera.facultad.id,
            "nombre": carrera.facultad.nombre,
            "codigo": carrera.facultad.codigo,
            "sede": {
                "id": carrera.facultad.sede.id,
                "nombre": carrera.facultad.sede.nombre,
                "codigo": carrera.facultad.sede.codigo
            } if carrera.facultad.sede else None
        } if carrera.facultad else None,
        "total_estudiantes": total_estudiantes
    }
