from sqlalchemy.orm import Session
from app.models.project import Project, BudgetItem, EstadoProyecto
from app.models.user import User, RolEnum
from app.schemas.project import ProjectCreate, ProjectUpdate
from decimal import Decimal
from datetime import datetime
from fastapi import HTTPException, status

def generar_codigo_proyecto(db: Session, estudiante: User) -> str:
    """Genera código único del proyecto: FI-IS-2025-001"""
    año_actual = datetime.now().year
    
    # Contar proyectos existentes del año actual
    count = db.query(Project).filter(
        Project.codigo_proyecto.like(f"FI-IS-{año_actual}-%")
    ).count()
    
    numero = count + 1
    codigo = f"FI-IS-{año_actual}-{numero:03d}"
    return codigo

def crear_proyecto(db: Session, proyecto_data: ProjectCreate, estudiante_id: int) -> Project:
    """Crea un nuevo proyecto con items de presupuesto"""
    
    # Verificar que el estudiante existe
    estudiante = db.query(User).filter(User.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que el profesor existe
    profesor = db.query(User).filter(User.id == proyecto_data.profesor_id).first()
    if not profesor or profesor.rol != RolEnum.PROFESOR:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado o no tiene rol de profesor"
        )
    
    # Calcular presupuesto estimado total
    presupuesto_total = sum(item.costo for item in proyecto_data.items_presupuesto)
    
    # Generar código del proyecto
    codigo = generar_codigo_proyecto(db, estudiante)
    
    # Crear proyecto
    nuevo_proyecto = Project(
        codigo_proyecto=codigo,
        nombre=proyecto_data.nombre,
        descripcion=proyecto_data.descripcion,
        objetivos=proyecto_data.objetivos,
        presupuesto_estimado=presupuesto_total,
        estudiante_id=estudiante_id,
        profesor_id=proyecto_data.profesor_id,
        estado=EstadoProyecto.BORRADOR
    )
    
    db.add(nuevo_proyecto)
    db.flush()  # Para obtener el ID del proyecto
    
    # Crear items de presupuesto
    for item_data in proyecto_data.items_presupuesto:
        item = BudgetItem(
            proyecto_id=nuevo_proyecto.id,
            concepto=item_data.concepto,
            justificacion=item_data.justificacion,
            costo=item_data.costo
        )
        db.add(item)
    
    db.commit()
    db.refresh(nuevo_proyecto)
    
    return nuevo_proyecto

def cambiar_estado_proyecto(
    db: Session, 
    proyecto_id: int, 
    nuevo_estado: EstadoProyecto, 
    usuario_actual: User
) -> Project:
    """Cambia el estado de un proyecto según el rol del usuario"""
    
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Validar transiciones de estado según rol
    if usuario_actual.rol == RolEnum.ESTUDIANTE:
        if proyecto.estudiante_id != usuario_actual.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este proyecto"
            )
        if nuevo_estado != EstadoProyecto.PENDIENTE_VALIDACION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes enviar el proyecto a validación"
            )
    
    elif usuario_actual.rol == RolEnum.PROFESOR:
        if proyecto.profesor_id != usuario_actual.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No eres el asesor de este proyecto"
            )
        if nuevo_estado not in [EstadoProyecto.VALIDADO_ASESOR, EstadoProyecto.RECHAZADO]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes validar o rechazar el proyecto"
            )
    
    elif usuario_actual.rol == RolEnum.FINANCIERA:
        if nuevo_estado not in [EstadoProyecto.ACTIVO, EstadoProyecto.RECHAZADO]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes activar o rechazar el proyecto"
            )
    
    proyecto.estado = nuevo_estado
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto
