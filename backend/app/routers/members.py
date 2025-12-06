# backend/app/routers/members.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.project_member import ProjectMember, MembershipRequest, MemberRole, RequestStatus
from ..utils.permissions import get_current_user, require_role
from ..services.audit import log_action

router = APIRouter(prefix="/projects/{project_id}/members", tags=["Project Members"])


# ========== GESTIÓN DE COLABORADORES ==========

@router.get("")
def get_project_members(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de colaboradores de un proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar permisos
    can_view = False
    if current_user.rol.value in ["profesor", "financiera", "auditor", "superusuario"]:
        can_view = True
    elif current_user.rol.value == "estudiante":
        # Estudiante puede ver si es dueño o colaborador
        is_owner = project.estudiante_id == current_user.id
        is_member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.student_id == current_user.id
        ).first() is not None
        can_view = is_owner or is_member
    
    if not can_view:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    
    return [{
        "id": m.id,
        "student": {
            "id": m.student.id,
            "nombre_completo": m.student.nombre_completo,
            "email": m.student.email,
            "codigo_institucional": m.student.codigo_institucional
        },
        "role": m.role.value,
        "joined_at": m.joined_at.isoformat()
    } for m in members]


@router.post("")
def add_member(
    project_id: int,
    member_data: dict,
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    """Agregar colaborador (solo dueño del proyecto)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Verificar que es el dueño
    if project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo el creador puede agregar colaboradores")
    
    student_id = member_data.get("student_id")
    
    # Validar que el estudiante existe
    student = db.query(User).filter(User.id == student_id).first()
    if not student or student.rol.value != "estudiante":
        raise HTTPException(status_code=400, detail="Estudiante no encontrado")
    
    # Validar que no sea el mismo dueño
    if student_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes agregarte como colaborador")
    
    # Verificar que no esté ya agregado
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.student_id == student_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="El estudiante ya es colaborador")
    
    # Crear miembro
    new_member = ProjectMember(
        project_id=project_id,
        student_id=student_id,
        role=MemberRole.COLLABORATOR
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    log_action(db, current_user.id, "AGREGAR_COLABORADOR", "project_members", new_member.id)
    
    return {
        "message": "Colaborador agregado exitosamente",
        "member": {
            "id": new_member.id,
            "student": {
                "id": student.id,
                "nombre_completo": student.nombre_completo
            }
        }
    }


@router.delete("/{member_id}")
def remove_member(
    project_id: int,
    member_id: int,
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    """Eliminar colaborador (solo dueño)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    member = db.query(ProjectMember).filter(
        ProjectMember.id == member_id,
        ProjectMember.project_id == project_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    
    db.delete(member)
    db.commit()
    
    log_action(db, current_user.id, "ELIMINAR_COLABORADOR", "project_members", member_id)
    
    return {"message": "Colaborador eliminado"}


# ========== SOLICITUDES DE MEMBRESÍA ==========

@router.get("/requests")
def get_membership_requests(
    project_id: int,
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    """Obtener solicitudes pendientes (solo dueño)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    requests = db.query(MembershipRequest).filter(
        MembershipRequest.project_id == project_id,
        MembershipRequest.status == RequestStatus.PENDING
    ).all()
    
    return [{
        "id": r.id,
        "student": {
            "id": r.student.id,
            "nombre_completo": r.student.nombre_completo,
            "email": r.student.email,
            "codigo_institucional": r.student.codigo_institucional
        },
        "message": r.message,
        "created_at": r.created_at.isoformat()
    } for r in requests]


@router.post("/request")
def request_membership(
    project_id: int,
    request_data: dict,
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    """Solicitar unirse a un proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # No puede solicitar si es el dueño
    if project.estudiante_id == current_user.id:
        raise HTTPException(status_code=400, detail="Eres el creador del proyecto")
    
    # Verificar que no sea ya miembro
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.student_id == current_user.id
    ).first()
    
    if is_member:
        raise HTTPException(status_code=400, detail="Ya eres colaborador")
    
    # Verificar que no tenga solicitud pendiente
    pending = db.query(MembershipRequest).filter(
        MembershipRequest.project_id == project_id,
        MembershipRequest.student_id == current_user.id,
        MembershipRequest.status == RequestStatus.PENDING
    ).first()
    
    if pending:
        raise HTTPException(status_code=400, detail="Ya tienes una solicitud pendiente")
    
    # Crear solicitud
    new_request = MembershipRequest(
        project_id=project_id,
        student_id=current_user.id,
        message=request_data.get("message", "")
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return {"message": "Solicitud enviada exitosamente", "request_id": new_request.id}


@router.post("/requests/{request_id}/respond")
def respond_request(
    project_id: int,
    request_id: int,
    response_data: dict,
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    """Aprobar o rechazar solicitud (solo dueño)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or project.estudiante_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    request = db.query(MembershipRequest).filter(
        MembershipRequest.id == request_id,
        MembershipRequest.project_id == project_id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    approve = response_data.get("approve", False)
    response_message = response_data.get("message", "")
    
    if approve:
        # Aprobar: agregar como colaborador
        new_member = ProjectMember(
            project_id=project_id,
            student_id=request.student_id,
            role=MemberRole.COLLABORATOR
        )
        db.add(new_member)
        request.status = RequestStatus.APPROVED
    else:
        request.status = RequestStatus.REJECTED
    
    request.response_message = response_message
    db.commit()
    
    return {"message": "Solicitud procesada exitosamente"}
