from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.schemas.user import UserCreate, UserLogin, UserDetailResponse, TokenResponse, UserResponse
from app.models.user import User, RolEnum
from app.core.security import hash_password, verify_password, create_access_token
from app.api.dependencies import get_db, get_current_user

router = APIRouter()


def obtener_datos_usuario_completo(db: Session, user: User) -> dict:
    """Obtiene información completa del usuario incluyendo facultad, sede y carrera"""
    user_data = {
        "id": user.id,
        "codigo_institucional": user.codigo_institucional,
        "email_institucional": user.email_institucional,
        "nombre_completo": user.nombre_completo,
        "rol": user.rol,
        "facultad_id": user.facultad_id,
        "sede_id": user.sede_id,
        "carrera_id": user.carrera_id,
        "creado_en": user.creado_en,
        "facultad_nombre": None,
        "sede_nombre": None,
        "carrera_nombre": None
    }

    # Obtener nombre de facultad
    if user.facultad_id:
        result = db.execute(
            text("SELECT nombre FROM facultades WHERE id = :id"),
            {"id": user.facultad_id}
        )
        row = result.fetchone()
        if row:
            user_data["facultad_nombre"] = row[0]

    # Obtener nombre de sede
    if user.sede_id:
        result = db.execute(
            text("SELECT nombre FROM sedes WHERE id = :id"),
            {"id": user.sede_id}
        )
        row = result.fetchone()
        if row:
            user_data["sede_nombre"] = row[0]

    # Obtener nombre de carrera
    if user.carrera_id:
        result = db.execute(
            text("SELECT nombre FROM carreras WHERE id = :id"),
            {"id": user.carrera_id}
        )
        row = result.fetchone()
        if row:
            user_data["carrera_nombre"] = row[0]

    return user_data


def validar_sede(sede_id: int, sede_custom: str, db: Session) -> int:
    """
    Valida que la sede sea válida para la Universidad de Cartagena.
    Solo permite: Piedra de Bolívar, Zaragocilla, San Pablo, El Carmen de Bolívar
    """
    sedes_validas = ["Piedra de Bolívar", "Zaragocilla", "San Pablo", "El Carmen de Bolívar"]
    
    if sede_custom and not sede_id:
        if sede_custom not in sedes_validas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sede no válida. Sedes permitidas: {', '.join(sedes_validas)}"
            )
        
        # Buscar si ya existe
        result = db.execute(
            text("SELECT id FROM sedes WHERE nombre = :nombre"),
            {"nombre": sede_custom}
        )
        row = result.fetchone()
        if row:
            return row[0]
        else:
            # Crear nueva sede válida
            result = db.execute(
                text("INSERT INTO sedes (nombre) VALUES (:nombre) RETURNING id"),
                {"nombre": sede_custom}
            )
            return result.fetchone()[0]
    
    return sede_id


@router.post("/register", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario en el sistema
    Solo permite sedes válidas de la Universidad de Cartagena
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(
        (User.codigo_institucional == user_data.codigo_institucional) |
        (User.email_institucional == user_data.email_institucional)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código institucional o email ya está registrado"
        )

    # Procesar facultad personalizada
    facultad_id = user_data.facultad_id
    if user_data.facultad_custom and not facultad_id:
        result = db.execute(
            text("SELECT id FROM facultades WHERE LOWER(nombre) = LOWER(:nombre)"),
            {"nombre": user_data.facultad_custom}
        )
        row = result.fetchone()
        if row:
            facultad_id = row[0]
        else:
            result = db.execute(
                text("INSERT INTO facultades (nombre) VALUES (:nombre) RETURNING id"),
                {"nombre": user_data.facultad_custom}
            )
            facultad_id = result.fetchone()[0]

    # Validar y procesar sede (solo sedes válidas)
    sede_id = validar_sede(user_data.sede_id, user_data.sede_custom, db)

    # Procesar carrera personalizada
    carrera_id = user_data.carrera_id
    if user_data.carrera_custom and not carrera_id and facultad_id:
        result = db.execute(
            text("SELECT id FROM carreras WHERE LOWER(nombre) = LOWER(:nombre) AND facultad_id = :fid"),
            {"nombre": user_data.carrera_custom, "fid": facultad_id}
        )
        row = result.fetchone()
        if row:
            carrera_id = row[0]
        else:
            result = db.execute(
                text("INSERT INTO carreras (nombre, facultad_id) VALUES (:nombre, :fid) RETURNING id"),
                {"nombre": user_data.carrera_custom, "fid": facultad_id}
            )
            carrera_id = result.fetchone()[0]

    # Crear nuevo usuario
    new_user = User(
        codigo_institucional=user_data.codigo_institucional,
        email_institucional=user_data.email_institucional,
        nombre_completo=user_data.nombre_completo,
        password_hash=hash_password(user_data.password),
        rol=user_data.rol,
        facultad_id=facultad_id,
        sede_id=sede_id,
        carrera_id=carrera_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return obtener_datos_usuario_completo(db, new_user)


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión en el sistema
    """
    user = db.query(User).filter(
        User.codigo_institucional == credentials.codigo_institucional
    ).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código institucional o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(data={
        "sub": str(user.id),
        "rol": user.rol,
        "codigo": user.codigo_institucional
    })

    user_detail = obtener_datos_usuario_completo(db, user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": user_detail
    }


@router.get("/me", response_model=UserDetailResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información del usuario autenticado actual
    """
    return obtener_datos_usuario_completo(db, current_user)


@router.get("/usuarios")
def listar_usuarios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos los usuarios del sistema
    Devuelve información básica para uso en selectores
    """
    usuarios = db.query(User).all()
    
    return [
        {
            "id": user.id,
            "codigo_institucional": user.codigo_institucional,
            "email_institucional": user.email_institucional,
            "nombre_completo": user.nombre_completo,
            "rol": user.rol,
            "creado_en": user.creado_en
        }
        for user in usuarios
    ]


@router.get("/profesores")
def listar_profesores(db: Session = Depends(get_db)):
    """
    Listar solo profesores para selección en proyectos
    Endpoint público para facilitar creación de proyectos
    """
    profesores = db.query(User).filter(User.rol == RolEnum.PROFESOR).all()
    
    return [
        {
            "id": profesor.id,
            "codigo_institucional": profesor.codigo_institucional,
            "nombre_completo": profesor.nombre_completo,
            "email_institucional": profesor.email_institucional
        }
        for profesor in profesores
    ]
