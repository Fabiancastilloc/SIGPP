from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models.user import User, RoleEnum
from ..schemas.user import UserRegister, UserLogin, Token
from ..utils.security import verify_password, get_password_hash, create_access_token
from ..config import settings
from ..services.audit import log_action

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    if db.query(User).filter(User.codigo_institucional == user_data.codigo_institucional).first():
        raise HTTPException(status_code=400, detail="Código institucional ya registrado")
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    role_mapping = {
        'superusuario': RoleEnum.SUPERUSUARIO,
        'estudiante': RoleEnum.ESTUDIANTE,
        'profesor': RoleEnum.PROFESOR,
        'financiera': RoleEnum.FINANCIERA,
        'auditor': RoleEnum.AUDITOR
    }
    
    rol_enum = role_mapping.get(user_data.rol.lower())
    if not rol_enum:
        raise HTTPException(status_code=400, detail="Rol inválido")
    
    new_user = User(
        codigo_institucional=user_data.codigo_institucional,
        email=user_data.email,
        nombre_completo=user_data.nombre_completo,
        password_hash=get_password_hash(user_data.password),
        rol=rol_enum,
        sede_id=user_data.sede_id,
        facultad_id=user_data.facultad_id,
        carrera_id=user_data.carrera_id,
        semestre=user_data.semestre
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_action(db, new_user.id, "REGISTRO", "users", new_user.id)
    
    return {"message": "Usuario registrado exitosamente"}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Iniciar sesión - FIX: convertir user.id a string para JWT"""
    user = db.query(User).filter(User.codigo_institucional == credentials.codigo_institucional).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # ✅ FIX CRÍTICO: Convertir user.id a string para JWT
    access_token = create_access_token(
        data={"sub": str(user.id), "rol": user.rol.value},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    log_action(db, user.id, "LOGIN", "users", user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre_completo": user.nombre_completo,
            "rol": user.rol.value,
            "email": user.email,
            "codigo_institucional": user.codigo_institucional
        }
    }
