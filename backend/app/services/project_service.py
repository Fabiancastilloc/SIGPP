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
        estado="borrador"
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

def editar_proyecto(
    db: Session,
    proyecto_id: int,
    proyecto_data: ProjectUpdate,
    usuario_actual: User
) -> Project:
    """Edita un proyecto existente y cambia estado automáticamente"""
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar permisos
    if usuario_actual.rol == RolEnum.ESTUDIANTE and proyecto.estudiante_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este proyecto"
        )
    elif usuario_actual.rol == RolEnum.PROFESOR and proyecto.profesor_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor de este proyecto"
        )
    
    # Verificar que el proyecto esté en estado editable
    if proyecto.estado not in ["borrador", "rechazado"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden editar proyectos en estado borrador o rechazado"
        )
    
    # Actualizar campos
    if proyecto_data.nombre:
        proyecto.nombre = proyecto_data.nombre
    if proyecto_data.descripcion:
        proyecto.descripcion = proyecto_data.descripcion
    if proyecto_data.objetivos:
        proyecto.objetivos = proyecto_data.objetivos
    if proyecto_data.profesor_id:
        # Verificar que el nuevo profesor existe
        profesor = db.query(User).filter(User.id == proyecto_data.profesor_id).first()
        if not profesor or profesor.rol != RolEnum.PROFESOR:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )
        proyecto.profesor_id = proyecto_data.profesor_id
    
    # Actualizar items de presupuesto si se proporcionan
    if proyecto_data.items_presupuesto is not None:
        # Eliminar items existentes
        db.query(BudgetItem).filter(BudgetItem.proyecto_id == proyecto_id).delete()
        
        # Crear nuevos items
        presupuesto_total = Decimal(0)
        for item_data in proyecto_data.items_presupuesto:
            item = BudgetItem(
                proyecto_id=proyecto.id,
                concepto=item_data.concepto,
                justificacion=item_data.justificacion,
                costo=item_data.costo
            )
            db.add(item)
            presupuesto_total += item_data.costo
        
        proyecto.presupuesto_estimado = presupuesto_total
    
    # CAMBIO AUTOMÁTICO DE ESTADO
    # Si estaba rechazado y se edita, vuelve a borrador
    if proyecto.estado == "rechazado":
        proyecto.estado = "borrador"
    
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto

def cambiar_estado_proyecto(
    db: Session,
    proyecto_id: int,
    nuevo_estado: str,
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
        if nuevo_estado != "pendiente_validacion":
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
        if nuevo_estado not in ["validado_asesor", "rechazado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes validar o rechazar el proyecto"
            )
    
    elif usuario_actual.rol == RolEnum.FINANCIERA:
        if nuevo_estado not in ["activo", "rechazado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes activar o rechazar el proyecto"
            )
    
    proyecto.estado = nuevo_estado
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto

def editar_proyecto(
    db: Session,
    proyecto_id: int,
    proyecto_data: ProjectUpdate,
    usuario_actual: User
) -> Project:
    """Edita un proyecto existente y cambia estado automáticamente"""
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar permisos
    if usuario_actual.rol == RolEnum.ESTUDIANTE and proyecto.estudiante_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este proyecto"
        )
    elif usuario_actual.rol == RolEnum.PROFESOR and proyecto.profesor_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor de este proyecto"
        )
    
    # Verificar que el proyecto esté en estado editable
    if proyecto.estado not in ["borrador", "rechazado"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden editar proyectos en estado borrador o rechazado"
        )
    
    # Actualizar campos
    if proyecto_data.nombre:
        proyecto.nombre = proyecto_data.nombre
    if proyecto_data.descripcion:
        proyecto.descripcion = proyecto_data.descripcion
    if proyecto_data.objetivos:
        proyecto.objetivos = proyecto_data.objetivos
    if proyecto_data.profesor_id:
        profesor = db.query(User).filter(User.id == proyecto_data.profesor_id).first()
        if not profesor or profesor.rol != RolEnum.PROFESOR:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )
        proyecto.profesor_id = proyecto_data.profesor_id
    
    # Actualizar items de presupuesto si se proporcionan
    if proyecto_data.items_presupuesto is not None:
        db.query(BudgetItem).filter(BudgetItem.proyecto_id == proyecto_id).delete()
        
        presupuesto_total = Decimal(0)
        for item_data in proyecto_data.items_presupuesto:
            item = BudgetItem(
                proyecto_id=proyecto.id,
                concepto=item_data.concepto,
                justificacion=item_data.justificacion,
                costo=item_data.costo
            )
            db.add(item)
            presupuesto_total += item_data.costo
        
        proyecto.presupuesto_estimado = presupuesto_total
    
    # CAMBIO AUTOMÁTICO DE ESTADO
    if proyecto.estado == "rechazado":
        proyecto.estado = "borrador"
    
    proyecto.fecha_ultima_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto
