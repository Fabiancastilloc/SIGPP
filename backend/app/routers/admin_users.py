# backend/app/routers/admin_users.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from ..database import get_db
from ..models.user import User, RoleEnum
from ..schemas.user import UserRegister, UserResponse
from ..utils.permissions import get_current_user
from ..utils.security import get_password_hash
from ..services.audit import log_action

router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])

def require_admin(current_user: User = Depends(get_current_user)):
    """Solo superusuarios pueden acceder"""
    if current_user.rol != RoleEnum.SUPERUSUARIO:
        raise HTTPException(status_code=403, detail="Solo administradores pueden acceder")
    return current_user

# ============================================
# 📋 LISTAR USUARIOS (con paginación y filtros)
# ============================================
@router.get("")
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    rol: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(User)
    
    # Filtro por búsqueda
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                User.nombre_completo.ilike(search_filter),
                User.email.ilike(search_filter),
                User.codigo_institucional.ilike(search_filter)
            )
        )
    
    # Filtro por rol
    if rol:
        query = query.filter(User.rol == rol)
    
    # Filtro por estado
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Total
    total = query.count()
    
    # Paginación
    offset = (page - 1) * per_page
    users = query.order_by(User.created_at.desc()).offset(offset).limit(per_page).all()
    
    return {
        "users": [
            {
                "id": u.id,
                "codigo_institucional": u.codigo_institucional,
                "email": u.email,
                "nombre_completo": u.nombre_completo,
                "rol": u.rol.value,
                "sede_id": u.sede_id,
                "facultad_id": u.facultad_id,
                "carrera_id": u.carrera_id,
                "semestre": u.semestre,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat()
            }
            for u in users
        ],
        "total": total,
        "page": page,
        "per_page": per_page
    }

# ============================================
# 👤 OBTENER USUARIO POR ID
# ============================================
@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": user.id,
        "codigo_institucional": user.codigo_institucional,
        "email": user.email,
        "nombre_completo": user.nombre_completo,
        "rol": user.rol.value,
        "sede_id": user.sede_id,
        "facultad_id": user.facultad_id,
        "carrera_id": user.carrera_id,
        "semestre": user.semestre,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat()
    }

# ============================================
# ➕ CREAR USUARIO (usa tu schema UserRegister existente)
# ============================================
@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    # Verificar código institucional único
    if db.query(User).filter(User.codigo_institucional == user_data.codigo_institucional).first():
        raise HTTPException(status_code=400, detail="Código institucional ya registrado")
    
    # Verificar email único
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Mapear rol
    role_mapping = {
        "superusuario": RoleEnum.SUPERUSUARIO,
        "estudiante": RoleEnum.ESTUDIANTE,
        "profesor": RoleEnum.PROFESOR,
        "financiera": RoleEnum.FINANCIERA,
        "auditor": RoleEnum.AUDITOR
    }
    
    role_enum = role_mapping.get(user_data.rol.lower())
    if not role_enum:
        raise HTTPException(status_code=400, detail="Rol inválido")
    
    # Crear usuario
    new_user = User(
        codigo_institucional=user_data.codigo_institucional,
        email=user_data.email,
        nombre_completo=user_data.nombre_completo,
        password_hash=get_password_hash(user_data.password),
        rol=role_enum,
        sede_id=user_data.sede_id,
        facultad_id=user_data.facultad_id,
        carrera_id=user_data.carrera_id,
        semestre=user_data.semestre
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_action(db, admin.id, "CREAR_USUARIO", "users", new_user.id)
    
    return {"message": "Usuario creado exitosamente", "id": new_user.id}

# ============================================
# ✏️ ACTUALIZAR USUARIO
# ============================================
@router.put("/{user_id}")
def update_user(
    user_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir que el admin se quite su propio rol
    if user.id == admin.id and update_data.get("rol") and update_data.get("rol") != "superusuario":
        raise HTTPException(status_code=400, detail="No puedes quitarte el rol de administrador")
    
    # Verificar email único si se cambia
    if update_data.get("email") and update_data["email"] != user.email:
        if db.query(User).filter(User.email == update_data["email"]).first():
            raise HTTPException(status_code=400, detail="El email ya está en uso")
    
    # Verificar código único si se cambia
    if update_data.get("codigo_institucional") and update_data["codigo_institucional"] != user.codigo_institucional:
        if db.query(User).filter(User.codigo_institucional == update_data["codigo_institucional"]).first():
            raise HTTPException(status_code=400, detail="El código institucional ya está en uso")
    
    # Campos actualizables
    allowed_fields = ["email", "nombre_completo", "codigo_institucional", "sede_id", "facultad_id", "carrera_id", "semestre", "is_active"]
    
    for field in allowed_fields:
        if field in update_data:
            setattr(user, field, update_data[field])
    
    # Actualizar rol si viene
    if "rol" in update_data:
        role_mapping = {
            "superusuario": RoleEnum.SUPERUSUARIO,
            "estudiante": RoleEnum.ESTUDIANTE,
            "profesor": RoleEnum.PROFESOR,
            "financiera": RoleEnum.FINANCIERA,
            "auditor": RoleEnum.AUDITOR
        }
        role_enum = role_mapping.get(update_data["rol"].lower())
        if role_enum:
            user.rol = role_enum
    
    db.commit()
    db.refresh(user)
    
    log_action(db, admin.id, "ACTUALIZAR_USUARIO", "users", user.id)
    
    return {"message": "Usuario actualizado exitosamente"}

# ============================================
# 🔑 RESETEAR CONTRASEÑA
# ============================================
@router.post("/{user_id}/reset-password")
def reset_password(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    new_password = payload.get("new_password")
    if not new_password or len(new_password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    log_action(db, admin.id, "RESETEAR_PASSWORD", "users", user.id)
    
    return {"message": "Contraseña actualizada correctamente"}

# ============================================
# 🗑️ ELIMINAR USUARIO
# ============================================
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir eliminarse a sí mismo
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")
    
    # Verificar proyectos activos
    from ..models.project import Project, ProjectStatus
    active_projects = db.query(Project).filter(
        Project.estudiante_id == user.id,
        Project.estado.in_([ProjectStatus.ACTIVE, ProjectStatus.PENDING_PROFESSOR, ProjectStatus.PENDING_FINANCE])
    ).count()
    
    if active_projects > 0:
        raise HTTPException(status_code=400, detail=f"El usuario tiene {active_projects} proyecto(s) activo(s)")
    
    log_action(db, admin.id, "ELIMINAR_USUARIO", "users", user.id)
    
    db.delete(user)
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}

# ============================================
# 🔄 TOGGLE ESTADO ACTIVO
# ============================================
@router.post("/{user_id}/toggle-active")
def toggle_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes desactivarte a ti mismo")
    
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "activado" if user.is_active else "desactivado"
    log_action(db, admin.id, f"USUARIO_{status_text.upper()}", "users", user.id)
    
    return {"message": f"Usuario {status_text}", "is_active": user.is_active}

# ============================================
# 📊 ESTADÍSTICAS
# ============================================
@router.get("/stats/summary")
def get_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    total = db.query(User).count()
    activos = db.query(User).filter(User.is_active == True).count()
    inactivos = total - activos
    
    por_rol = {}
    for rol in RoleEnum:
        count = db.query(User).filter(User.rol == rol).count()
        por_rol[rol.value] = count
    
    return {
        "total": total,
        "activos": activos,
        "inactivos": inactivos,
        "por_rol": por_rol
    }
