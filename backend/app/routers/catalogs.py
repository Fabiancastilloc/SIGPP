from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import Sede, Facultad, Carrera, User, RoleEnum

router = APIRouter(prefix="/catalogs", tags=["Catalogos"])

@router.get("/sedes")
def get_sedes(db: Session = Depends(get_db)):
    """Obtener todas las sedes"""
    sedes = db.query(Sede).all()
    return [{"id": s.id, "nombre": s.nombre, "codigo": s.codigo} for s in sedes]

@router.get("/facultades")
def get_facultades(sede_id: int = None, db: Session = Depends(get_db)):
    """Obtener facultades, opcionalmente filtradas por sede"""
    query = db.query(Facultad)
    if sede_id:
        query = query.filter(Facultad.sede_id == sede_id)
    facultades = query.all()
    return [{"id": f.id, "nombre": f.nombre, "codigo": f.codigo, "sede_id": f.sede_id} for f in facultades]

@router.get("/carreras")
def get_carreras(facultad_id: int = None, db: Session = Depends(get_db)):
    """Obtener carreras, opcionalmente filtradas por facultad"""
    query = db.query(Carrera)
    if facultad_id:
        query = query.filter(Carrera.facultad_id == facultad_id)
    carreras = query.all()
    return [{
        "id": c.id,
        "nombre": c.nombre,
        "codigo": c.codigo,
        "facultad_id": c.facultad_id,
        "duracion_semestres": c.duracion_semestres,
        "modalidad": c.modalidad
    } for c in carreras]

@router.get("/profesores")
def get_profesores(db: Session = Depends(get_db)):
    """Obtener SOLO profesores (no estudiantes ni otros roles)"""
    profesores = db.query(User).filter(User.rol == RoleEnum.PROFESOR).all()
    
    print(f"📚 Profesores encontrados: {len(profesores)}")
    for p in profesores:
        print(f"  - {p.nombre_completo} (ID: {p.id}, Rol: {p.rol.value})")
    
    return [{
        "id": p.id,
        "nombre_completo": p.nombre_completo,
        "email": p.email,
        "facultad_id": p.facultad_id
    } for p in profesores]
