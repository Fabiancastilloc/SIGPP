from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectDetail, ProjectUpdate, BudgetItemResponse
from app.models.project import Project, EstadoProyecto, BudgetItem
from app.models.user import User, RolEnum
from app.api.dependencies import get_db, get_current_user
from app.services.project_service import crear_proyecto, cambiar_estado_proyecto, editar_proyecto

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    proyecto_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo proyecto de grado (solo estudiantes)"""
    if current_user.rol != RolEnum.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden crear proyectos"
        )
    
    proyecto = crear_proyecto(db, proyecto_data, current_user.id)
    return proyecto


@router.get("/")
def list_projects(
    estado: Optional[str] = Query(None, description="Filtrar por estado del proyecto"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros a retornar"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar proyectos según el rol del usuario
    - **Estudiante**: solo sus proyectos
    - **Profesor**: proyectos donde es asesor
    - **Financiera/Auditor**: todos los proyectos
    """
    query = db.query(Project)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == current_user.id)
    
    # Filtrar por estado si se proporciona
    if estado:
        estados_validos = ["borrador", "pendiente_validacion", "validado_asesor", "activo", "rechazado", "finalizado"]
        if estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        query = query.filter(Project.estado == estado)
    
    # Obtener proyectos
    proyectos = query.order_by(Project.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    # Serializar manualmente para incluir items_presupuesto como diccionarios
    resultado = []
    for proyecto in proyectos:
        proyecto_dict = {
            "id": proyecto.id,
            "codigo_proyecto": proyecto.codigo_proyecto,
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "objetivos": proyecto.objetivos,
            "estado": proyecto.estado,
            "presupuesto_estimado": proyecto.presupuesto_estimado,
            "presupuesto_asignado": proyecto.presupuesto_asignado,
            "presupuesto_ejecutado": proyecto.presupuesto_ejecutado,
            "estudiante_id": proyecto.estudiante_id,
            "profesor_id": proyecto.profesor_id,
            "fecha_creacion": proyecto.fecha_creacion,
            "fecha_ultima_modificacion": proyecto.fecha_ultima_modificacion,
            "items_presupuesto": [
                {
                    "id": item.id,
                    "concepto": item.concepto,
                    "justificacion": item.justificacion,
                    "costo": float(item.costo)
                }
                for item in proyecto.items_presupuesto
            ] if proyecto.items_presupuesto else []
        }
        resultado.append(proyecto_dict)
    
    return resultado


@router.get("/{proyecto_id}")
def get_project(
    proyecto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalles de un proyecto específico"""
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
    
    # Serializar manualmente
    proyecto_dict = {
        "id": proyecto.id,
        "codigo_proyecto": proyecto.codigo_proyecto,
        "nombre": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "objetivos": proyecto.objetivos,
        "estado": proyecto.estado,
        "presupuesto_estimado": proyecto.presupuesto_estimado,
        "presupuesto_asignado": proyecto.presupuesto_asignado,
        "presupuesto_ejecutado": proyecto.presupuesto_ejecutado,
        "estudiante_id": proyecto.estudiante_id,
        "profesor_id": proyecto.profesor_id,
        "fecha_creacion": proyecto.fecha_creacion,
        "fecha_ultima_modificacion": proyecto.fecha_ultima_modificacion,
        "items_presupuesto": [
            {
                "id": item.id,
                "concepto": item.concepto,
                "justificacion": item.justificacion,
                "costo": float(item.costo)
            }
            for item in proyecto.items_presupuesto
        ] if proyecto.items_presupuesto else []
    }
    
    return proyecto_dict


@router.put("/{proyecto_id}", response_model=ProjectDetail)
def update_project(
    proyecto_id: int,
    proyecto_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Editar un proyecto existente (estudiantes y profesores)"""
    proyecto = editar_proyecto(db, proyecto_id, proyecto_data, current_user)
    return proyecto


@router.patch("/{proyecto_id}/estado")
def update_project_status(
    proyecto_id: int,
    nuevo_estado: str = Query(..., description="Nuevo estado del proyecto"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cambiar el estado de un proyecto"""
    proyecto = cambiar_estado_proyecto(db, proyecto_id, nuevo_estado, current_user)
    
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
    """Eliminar un proyecto (solo en estado borrador y por el estudiante propietario)"""
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
    if proyecto.estado != "borrador":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar proyectos en estado borrador"
        )
    
    db.delete(proyecto)
    db.commit()
    
    return {"message": "Proyecto eliminado correctamente"}

@router.patch("/{proyecto_id}/asignar-presupuesto")
def asignar_presupuesto(
    proyecto_id: int,
    presupuesto_asignado: Decimal = Query(..., gt=0),
    comentarios: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Asignar presupuesto final a un proyecto (solo Finanzas)
    """
    if current_user.rol != RolEnum.FINANCIERA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el área financiera puede asignar presupuestos"
        )
    
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOTFOUND,
            detail="Proyecto no encontrado"
        )
    
    # Solo se puede asignar presupuesto a proyectos validados por asesor
    if proyecto.estado != "validado_asesor":
        raise HTTPException(
            status_code=status.HTTP_400_BADREQUEST,
            detail="El proyecto debe estar validado por el asesor"
        )
    
    # Asignar presupuesto
    proyecto.presupuesto_asignado = presupuesto_asignado
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    # Registrar en historial
    from app.models.project import HistorialAprobacion
    historial = HistorialAprobacion(
        proyecto_id=proyecto.id,
        usuario_id=current_user.id,
        estado_anterior=proyecto.estado,
        estado_nuevo=proyecto.estado,
        comentarios=comentarios or f"Presupuesto asignado: ${presupuesto_asignado}"
    )
    db.add(historial)
    
    db.commit()
    db.refresh(proyecto)
    
    return {
        "message": "Presupuesto asignado correctamente",
        "proyecto_id": proyecto.id,
        "presupuesto_asignado": float(proyecto.presupuesto_asignado)
    }

@router.get("/pendientes-finanzas")
def list_proyectos_pendientes_finanzas(
    facultad_id: Optional[int] = Query(None),
    sede_id: Optional[int] = Query(None),
    carrera_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar proyectos pendientes de aprobación financiera (estado: validado_asesor)
    """
    if current_user.rol != RolEnum.FINANCIERA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el área financiera puede ver esta vista"
        )
    
    # Proyectos validados por asesor que esperan aprobación financiera
    query = db.query(Project).filter(Project.estado == "validado_asesor")
    
    # Filtros opcionales
    if facultad_id:
        query = query.join(User, Project.estudiante_id == User.id).filter(User.facultad_id == facultad_id)
    if sede_id:
        query = query.join(User, Project.estudiante_id == User.id).filter(User.sede_id == sede_id)
    if carrera_id:
        query = query.join(User, Project.estudiante_id == User.id).filter(User.carrera_id == carrera_id)
    
    proyectos = query.order_by(Project.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    # Serializar con información completa
    resultado = []
    for proyecto in proyectos:
        estudiante = db.query(User).filter(User.id == proyecto.estudiante_id).first()
        profesor = db.query(User).filter(User.id == proyecto.profesor_id).first() if proyecto.profesor_id else None
        
        proyecto_dict = {
            "id": proyecto.id,
            "codigo_proyecto": proyecto.codigo_proyecto,
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "objetivos": proyecto.objetivos,
            "estado": proyecto.estado,
            "presupuesto_estimado": float(proyecto.presupuesto_estimado),
            "presupuesto_asignado": float(proyecto.presupuesto_asignado) if proyecto.presupuesto_asignado else None,
            "estudiante_id": proyecto.estudiante_id,
            "estudiante_nombre": estudiante.nombre_completo if estudiante else None,
            "profesor_id": proyecto.profesor_id,
            "profesor_nombre": profesor.nombre_completo if profesor else None,
            "fecha_creacion": proyecto.fecha_creacion,
            "items_presupuesto": [
                {
                    "id": item.id,
                    "concepto": item.concepto,
                    "justificacion": item.justificacion,
                    "costo": float(item.costo)
                }
                for item in proyecto.items_presupuesto
            ] if proyecto.items_presupuesto else []
        }
        resultado.append(proyecto_dict)
    
    return resultado

@router.patch("/{proyecto_id}/asignar-presupuesto")
def asignar_presupuesto_proyecto(
    proyecto_id: int,
    presupuesto_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Asigna presupuesto final a un proyecto (solo Finanzas)
    """
    # Verificar que el usuario sea de finanzas
    if current_user.rol != RolEnum.FINANCIERA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el área financiera puede asignar presupuesto"
        )
    
    # Buscar proyecto
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar que el proyecto esté en estado correcto
    if proyecto.estado != "validado_asesor":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El proyecto debe estar validado por el asesor"
        )
    
    # Asignar presupuesto
    proyecto.presupuesto_asignado = presupuesto_data.get("presupuesto_asignado", 0)
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    # Registrar en historial si tienes tabla de historial
    # historial = HistorialProyecto(...)
    # db.add(historial)
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto

@router.get("/")
def listar_proyectos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    estado: Optional[str] = None
):
    """
    Lista proyectos según el rol del usuario
    """
    query = db.query(Project)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == current_user.id)
    # Si es FINANCIERA, mostrar todos los proyectos
    # (no aplicar filtro adicional)
    
    # Filtrar por estado si se proporciona
    if estado:
        query = query.filter(Project.estado == estado)
    
    proyectos = query.order_by(Project.fecha_creacion.desc()).all()
    
    return proyectos