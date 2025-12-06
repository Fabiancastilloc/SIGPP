# backend/app/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models.project import Project, ProjectStatus
from ..models.project_member import ProjectMember  # ✅ FALTABA ESTE IMPORT
from ..models.audit import ProjectHistory
from ..models.user import User, RoleEnum
from ..utils.permissions import get_current_user, require_role
from ..services.audit import log_action

router = APIRouter(prefix="/projects", tags=["Projects"])

# ==================== OBTENER PROYECTOS ====================
@router.get("")
def get_projects(
    estado: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener proyectos según el rol del usuario"""
    print(f"🔍 get_projects - Usuario: {current_user.nombre_completo} (rol: {current_user.rol.value})")
    
    query = db.query(Project)
    
    if current_user.rol.value == 'estudiante':
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol.value == 'profesor':
        query = query.filter(Project.profesor_id == current_user.id)
    
    if estado:
        query = query.filter(Project.estado == estado)
    
    projects = query.all()
    print(f"📊 Proyectos encontrados: {len(projects)}")
    
    return [{
        "id": p.id,
        "codigo_proyecto": p.codigo_proyecto,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "objetivos": p.objetivos,
        "estado": p.estado.value,
        "presupuesto_estimado": float(p.presupuesto_estimado),
        "presupuesto_asignado": float(p.presupuesto_asignado) if p.presupuesto_asignado else None,
        "presupuesto_ejecutado": float(p.presupuesto_ejecutado),
        "estudiante": {
            "id": p.estudiante.id,
            "nombre": p.estudiante.nombre_completo,
            "email": p.estudiante.email
        },
        "profesor": {
            "id": p.profesor.id,
            "nombre": p.profesor.nombre_completo,
            "email": p.profesor.email
        },
        "comentarios_profesor": p.comentarios_profesor,
        "comentarios_financiera": p.comentarios_financiera,
        "created_at": p.created_at.isoformat(),
        "updated_at": p.updated_at.isoformat()
    } for p in projects]


# ==================== PROYECTOS COMO COLABORADOR ====================
# ✅ CORREGIDO: Cambiado de "/projects/as-collaborator" a "/as-collaborator"
@router.get("/as-collaborator")
def get_projects_as_collaborator(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener proyectos donde el estudiante actual es COLABORADOR
    (No incluye los proyectos que creó)
    """
    print(f"🔍 get_projects_as_collaborator - Usuario ID: {current_user.id}")
    
    if current_user.rol.value != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden acceder")
    
    # Buscar membresías donde el estudiante es colaborador
    memberships = db.query(ProjectMember).filter(
        ProjectMember.student_id == current_user.id
    ).all()
    
    print(f"📊 Membresías encontradas: {len(memberships)}")
    
    # Obtener los proyectos de esas membresías
    project_ids = [m.project_id for m in memberships]
    
    if not project_ids:
        print("⚠️ No hay proyectos como colaborador")
        return []
    
    projects = db.query(Project).filter(
        Project.id.in_(project_ids)
    ).order_by(Project.created_at.desc()).all()
    
    print(f"✅ Proyectos como colaborador: {len(projects)}")
    
    result = []
    for p in projects:
        # Calcular miembros del equipo
        members_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == p.id
        ).count()
        
        result.append({
            "id": p.id,
            "codigo_proyecto": p.codigo_proyecto,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "objetivos": p.objetivos,
            "estado": p.estado.value,
            "presupuesto_estimado": float(p.presupuesto_estimado),
            "presupuesto_asignado": float(p.presupuesto_asignado) if p.presupuesto_asignado else None,
            "presupuesto_ejecutado": float(p.presupuesto_ejecutado) if p.presupuesto_ejecutado else 0,
            "comentarios_profesor": p.comentarios_profesor,
            "comentarios_financiera": p.comentarios_financiera,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
            "estudiante": {
                "id": p.estudiante.id,
                "nombre": p.estudiante.nombre_completo,
                "email": p.estudiante.email
            },
            "profesor": {
                "id": p.profesor.id,
                "nombre": p.profesor.nombre_completo,
                "email": p.profesor.email
            } if p.profesor else None,
            "is_collaborator": True,
            "team_size": members_count + 1
        })
    
    return result


# ==================== TODOS LOS PROYECTOS INVOLUCRADOS ====================
# ✅ CORREGIDO: Cambiado de "/projects/all-involved" a "/all-involved"
@router.get("/all-involved")
def get_all_projects_involved(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener TODOS los proyectos donde el estudiante está involucrado:
    - Proyectos que creó (como estudiante principal)
    - Proyectos donde es colaborador
    """
    print(f"🔍 get_all_projects_involved - Usuario ID: {current_user.id}")
    
    if current_user.rol.value != "estudiante":
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden acceder")
    
    # Proyectos creados por el estudiante
    own_projects = db.query(Project).filter(
        Project.estudiante_id == current_user.id
    ).all()
    
    print(f"📊 Proyectos propios: {len(own_projects)}")
    
    # Proyectos donde es colaborador
    memberships = db.query(ProjectMember).filter(
        ProjectMember.student_id == current_user.id
    ).all()
    
    collab_project_ids = [m.project_id for m in memberships]
    collab_projects = db.query(Project).filter(
        Project.id.in_(collab_project_ids)
    ).all() if collab_project_ids else []
    
    print(f"📊 Proyectos como colaborador: {len(collab_projects)}")
    
    # Combinar y serializar
    result = []
    
    # Proyectos propios
    for p in own_projects:
        members_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == p.id
        ).count()
        
        result.append({
            "id": p.id,
            "codigo_proyecto": p.codigo_proyecto,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "objetivos": p.objetivos,
            "estado": p.estado.value,
            "presupuesto_estimado": float(p.presupuesto_estimado),
            "presupuesto_asignado": float(p.presupuesto_asignado) if p.presupuesto_asignado else None,
            "presupuesto_ejecutado": float(p.presupuesto_ejecutado) if p.presupuesto_ejecutado else 0,
            "comentarios_profesor": p.comentarios_profesor,
            "comentarios_financiera": p.comentarios_financiera,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
            "estudiante": {
                "id": p.estudiante.id,
                "nombre": p.estudiante.nombre_completo,
                "email": p.estudiante.email
            },
            "profesor": {
                "id": p.profesor.id,
                "nombre": p.profesor.nombre_completo,
                "email": p.profesor.email
            } if p.profesor else None,
            "is_owner": True,
            "is_collaborator": False,
            "team_size": members_count + 1
        })
    
    # Proyectos como colaborador
    for p in collab_projects:
        members_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == p.id
        ).count()
        
        result.append({
            "id": p.id,
            "codigo_proyecto": p.codigo_proyecto,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "objetivos": p.objetivos,
            "estado": p.estado.value,
            "presupuesto_estimado": float(p.presupuesto_estimado),
            "presupuesto_asignado": float(p.presupuesto_asignado) if p.presupuesto_asignado else None,
            "presupuesto_ejecutado": float(p.presupuesto_ejecutado) if p.presupuesto_ejecutado else 0,
            "comentarios_profesor": p.comentarios_profesor,
            "comentarios_financiera": p.comentarios_financiera,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
            "estudiante": {
                "id": p.estudiante.id,
                "nombre": p.estudiante.nombre_completo,
                "email": p.estudiante.email
            },
            "profesor": {
                "id": p.profesor.id,
                "nombre": p.profesor.nombre_completo,
                "email": p.profesor.email
            } if p.profesor else None,
            "is_owner": False,
            "is_collaborator": True,
            "team_size": members_count + 1
        })
    
    # Ordenar por fecha de creación
    result.sort(key=lambda x: x["created_at"], reverse=True)
    
    print(f"✅ Total proyectos involucrados: {len(result)}")
    
    return result


# ==================== CREAR PROYECTO ====================
@router.post("")
def create_project(
    project_data: dict,
    current_user: User = Depends(require_role(['estudiante'])),
    db: Session = Depends(get_db)
):
    """Crear nuevo proyecto con validaciones completas"""
    # VALIDACIÓN 1: Verificar que el profesor existe
    profesor = db.query(User).filter(User.id == project_data['profesor_id']).first()
    
    if not profesor:
        raise HTTPException(status_code=400, detail="Profesor no encontrado")
    
    # VALIDACIÓN 2: Verificar que es realmente un profesor
    if profesor.rol != RoleEnum.PROFESOR:
        raise HTTPException(
            status_code=400, 
            detail=f"El usuario seleccionado ({profesor.nombre_completo}) no es un profesor. Rol actual: {profesor.rol.value}"
        )
    
    # VALIDACIÓN 3: Verificar que no sea el mismo estudiante
    if profesor.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes asignarte como tu propio profesor")
    
    # VALIDACIÓN 4: Verificar longitud de descripción
    if len(project_data['descripcion']) < 100:
        raise HTTPException(status_code=400, detail="La descripción debe tener al menos 100 caracteres")
    
    # VALIDACIÓN 5: Verificar presupuesto
    if project_data['presupuesto_estimado'] <= 0:
        raise HTTPException(status_code=400, detail="El presupuesto debe ser mayor a cero")
    
    # Generar código único
    year = 2025
    count = db.query(Project).count() + 1
    codigo = f"PROJ-{year}-{count:03d}"
    
    new_project = Project(
        codigo_proyecto=codigo,
        nombre=project_data['nombre'],
        descripcion=project_data['descripcion'],
        objetivos=project_data['objetivos'],
        estudiante_id=current_user.id,
        profesor_id=project_data['profesor_id'],
        presupuesto_estimado=project_data['presupuesto_estimado'],
        estado=ProjectStatus.DRAFT
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    log_action(db, current_user.id, "CREAR_PROYECTO", "projects", new_project.id)
    
    print(f"✅ Proyecto creado: {new_project.nombre}")
    print(f"   Estudiante: {current_user.nombre_completo}")
    print(f"   Profesor: {profesor.nombre_completo}")
    
    return {"message": "Proyecto creado exitosamente", "id": new_project.id}


# ==================== ACTUALIZAR PROYECTO ====================
@router.put("/{project_id}")
def update_project(
    project_id: int,
    project_data: dict,
    current_user: User = Depends(require_role(['estudiante'])),
    db: Session = Depends(get_db)
):
    """Actualizar proyecto (solo en estado borrador)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar permisos
    if project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # Solo se puede editar en borrador
    if project.estado != ProjectStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Solo puedes editar proyectos en borrador")
    
    # Validaciones
    if 'descripcion' in project_data and len(project_data['descripcion']) < 100:
        raise HTTPException(status_code=400, detail="La descripción debe tener al menos 100 caracteres")
    
    if 'presupuesto_estimado' in project_data and project_data['presupuesto_estimado'] <= 0:
        raise HTTPException(status_code=400, detail="El presupuesto debe ser mayor a cero")
    
    # Actualizar campos
    if 'nombre' in project_data:
        project.nombre = project_data['nombre']
    if 'descripcion' in project_data:
        project.descripcion = project_data['descripcion']
    if 'objetivos' in project_data:
        project.objetivos = project_data['objetivos']
    if 'presupuesto_estimado' in project_data:
        project.presupuesto_estimado = project_data['presupuesto_estimado']
    if 'profesor_id' in project_data:
        # Validar que el profesor existe
        profesor = db.query(User).filter(User.id == project_data['profesor_id']).first()
        if not profesor or profesor.rol != RoleEnum.PROFESOR:
            raise HTTPException(status_code=400, detail="Profesor inválido")
        project.profesor_id = project_data['profesor_id']
    
    db.commit()
    db.refresh(project)
    
    log_action(db, current_user.id, "ACTUALIZAR_PROYECTO", "projects", project.id)
    
    print(f"✅ Proyecto actualizado: {project.nombre}")
    
    return {"message": "Proyecto actualizado exitosamente"}


# ==================== ENVIAR PROYECTO ====================
@router.post("/{project_id}/submit")
def submit_project(
    project_id: int,
    current_user: User = Depends(require_role(['estudiante'])),
    db: Session = Depends(get_db)
):
    """Enviar proyecto para validación"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    if project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    if project.estado != ProjectStatus.DRAFT:
        raise HTTPException(status_code=400, detail="El proyecto ya fue enviado")
    
    project.estado = ProjectStatus.PENDING_PROFESSOR
    
    history = ProjectHistory(
        project_id=project.id,
        estado_anterior='borrador',
        estado_nuevo='pendiente_profesor',
        usuario_id=current_user.id,
        comentario='Propuesta enviada para validación'
    )
    db.add(history)
    db.commit()
    
    log_action(db, current_user.id, "ENVIAR_PROYECTO", "projects", project.id)
    
    return {"message": "Proyecto enviado para validación"}


# ==================== VALIDAR PROYECTO (PROFESOR) ====================
@router.post("/{project_id}/validate")
def validate_project(
    project_id: int,
    validation_data: dict,
    current_user: User = Depends(require_role(['profesor'])),
    db: Session = Depends(get_db)
):
    """Validar proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    if project.profesor_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    if project.estado != ProjectStatus.PENDING_PROFESSOR:
        raise HTTPException(status_code=400, detail="El proyecto no está pendiente de validación")
    
    aprobado = validation_data.get('aprobado', False)
    comentarios = validation_data.get('comentarios', '')
    
    project.comentarios_profesor = comentarios
    
    if aprobado:
        project.estado = ProjectStatus.PENDING_FINANCE
        nuevo_estado = 'pendiente_financiera'
    else:
        project.estado = ProjectStatus.DRAFT
        nuevo_estado = 'borrador'
    
    history = ProjectHistory(
        project_id=project.id,
        estado_anterior='pendiente_profesor',
        estado_nuevo=nuevo_estado,
        usuario_id=current_user.id,
        comentario=comentarios
    )
    db.add(history)
    db.commit()
    
    log_action(db, current_user.id, "VALIDAR_PROYECTO", "projects", project.id)
    
    return {"message": "Proyecto validado exitosamente"}


# ==================== ACTIVAR PROYECTO (FINANCIERA) ====================
@router.post("/{project_id}/activate")
def activate_project(
    project_id: int,
    activation_data: dict,
    current_user: User = Depends(require_role(['financiera'])),
    db: Session = Depends(get_db)
):
    """Activar proyecto y asignar presupuesto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    if project.estado != ProjectStatus.PENDING_FINANCE:
        raise HTTPException(status_code=400, detail="El proyecto no está pendiente de aprobación financiera")
    
    aprobado = activation_data.get('aprobado', False)
    presupuesto_asignado = activation_data.get('presupuesto_asignado')
    comentarios = activation_data.get('comentarios', '')
    
    project.comentarios_financiera = comentarios
    
    if aprobado and presupuesto_asignado:
        project.estado = ProjectStatus.ACTIVE
        project.presupuesto_asignado = presupuesto_asignado
        nuevo_estado = 'activo'
    else:
        project.estado = ProjectStatus.DRAFT
        nuevo_estado = 'borrador'
    
    history = ProjectHistory(
        project_id=project.id,
        estado_anterior='pendiente_financiera',
        estado_nuevo=nuevo_estado,
        usuario_id=current_user.id,
        comentario=comentarios
    )
    db.add(history)
    db.commit()
    
    log_action(db, current_user.id, "ACTIVAR_PROYECTO", "projects", project.id)
    
    return {"message": "Proyecto procesado exitosamente"}


# ==================== OBTENER DETALLES ====================
@router.get("/{project_id}")
def get_project_details(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalles completos de un proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar permisos
    can_view = False
    
    # Superusuario, auditor, financiera pueden ver todo
    if current_user.rol.value in ['superusuario', 'auditor', 'financiera']:
        can_view = True
    # Estudiante creador
    elif current_user.rol.value == 'estudiante' and project.estudiante_id == current_user.id:
        can_view = True
    # Estudiante colaborador
    elif current_user.rol.value == 'estudiante':
        is_member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.student_id == current_user.id
        ).first()
        if is_member:
            can_view = True
    # Profesor asignado
    elif current_user.rol.value == 'profesor' and project.profesor_id == current_user.id:
        can_view = True
    
    if not can_view:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    return {
        "id": project.id,
        "codigo_proyecto": project.codigo_proyecto,
        "nombre": project.nombre,
        "descripcion": project.descripcion,
        "objetivos": project.objetivos,
        "estado": project.estado.value,
        "presupuesto_estimado": float(project.presupuesto_estimado),
        "presupuesto_asignado": float(project.presupuesto_asignado) if project.presupuesto_asignado else None,
        "presupuesto_ejecutado": float(project.presupuesto_ejecutado),
        "estudiante": {
            "id": project.estudiante.id,
            "nombre": project.estudiante.nombre_completo,
            "email": project.estudiante.email
        },
        "profesor": {
            "id": project.profesor.id,
            "nombre": project.profesor.nombre_completo,
            "email": project.profesor.email
        },
        "comentarios_profesor": project.comentarios_profesor,
        "comentarios_financiera": project.comentarios_financiera,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat()
    }


# ==================== HISTORIAL ====================
@router.get("/{project_id}/history")
def get_project_history(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener historial de cambios del proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar permisos
    can_view = False
    if current_user.rol.value in ["superusuario", "auditor", "financiera"]:
        can_view = True
    elif current_user.rol.value == "estudiante" and project.estudiante_id == current_user.id:
        can_view = True
    elif current_user.rol.value == "profesor" and project.profesor_id == current_user.id:
        can_view = True
    
    if not can_view:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    history = db.query(ProjectHistory).filter(
        ProjectHistory.project_id == project_id
    ).order_by(ProjectHistory.timestamp.desc()).all()
    
    return [
        {
            "id": h.id,
            "estado_anterior": h.estado_anterior,
            "estado_nuevo": h.estado_nuevo,
            "comentario": h.comentario,
            "usuario": {
                "id": h.usuario.id,
                "nombre": h.usuario.nombre_completo,
                "rol": h.usuario.rol.value
            },
            "timestamp": h.timestamp.isoformat()
        }
        for h in history
    ]
