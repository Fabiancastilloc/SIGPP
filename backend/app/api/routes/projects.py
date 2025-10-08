from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectDetail, ProjectUpdate
from app.models.project import Project, EstadoProyecto
from app.models.user import User, RolEnum
from app.api.dependencies import get_db, get_current_user
from app.services.project_service import crear_proyecto, cambiar_estado_proyecto

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    proyecto_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo proyecto de grado (solo estudiantes)
    """
    if current_user.rol != RolEnum.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden crear proyectos"
        )
    
    proyecto = crear_proyecto(db, proyecto_data, current_user.id)
    return proyecto

@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    estado: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Listar proyectos según el rol del usuario
    
    - Estudiante: solo sus proyectos
    - Profesor: proyectos donde es asesor
    - Financiera/Auditor: todos los proyectos
    """
    query = db.query(Project)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == current_user.id)
    
    # Filtrar por estado si se proporciona
    if estado:
        try:
            estado_enum = EstadoProyecto(estado)
            query = query.filter(Project.estado == estado_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido: {estado}"
            )
    
    proyectos = query.offset(skip).limit(limit).all()
    return proyectos

@router.get("/{proyecto_id}", response_model=ProjectDetail)
def get_project(
    proyecto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de un proyecto específico
    """
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == RolEnum.ESTUDIANTE and proyecto.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este proyecto"
        )
    elif current_user.rol == RolEnum.PROFESOR and proyecto.profesor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor de este proyecto"
        )
    
    return proyecto

@router.patch("/{proyecto_id}/estado")
def update_project_status(
    proyecto_id: int,
    nuevo_estado: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambiar el estado de un proyecto
    
    Estados disponibles:
    - borrador
    - pendiente_validacion
    - validado_asesor
    - activo
    - rechazado
    - finalizado
    """
    try:
        estado_enum = EstadoProyecto(nuevo_estado)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido: {nuevo_estado}"
        )
    
    proyecto = cambiar_estado_proyecto(db, proyecto_id, estado_enum, current_user)
    return {
        "message": "Estado actualizado correctamente",
        "proyecto_id": proyecto.id,
        "estado_nuevo": proyecto.estado
    }

@router.delete("/{proyecto_id}")
def delete_project(
    proyecto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un proyecto (solo en estado borrador y por el estudiante propietario)
    """
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Solo el estudiante propietario puede eliminar
    if current_user.rol != RolEnum.ESTUDIANTE or proyecto.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este proyecto"
        )
    
    # Solo se puede eliminar si está en borrador
    if proyecto.estado != EstadoProyecto.BORRADOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar proyectos en estado borrador"
        )
    
    db.delete(proyecto)
    db.commit()
    
    return {"message": "Proyecto eliminado correctamente"}
