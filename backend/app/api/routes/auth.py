from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.api.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario en el sistema
    
    - **codigo_institucional**: Código único del estudiante/profesor
    - **email_institucional**: Email institucional (@unicartagena.edu.co)
    - **nombre_completo**: Nombre completo del usuario
    - **rol**: estudiante, profesor, financiera, auditor
    - **password**: Contraseña (mínimo 8 caracteres)
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
    
    # Crear nuevo usuario
    new_user = User(
        codigo_institucional=user_data.codigo_institucional,
        email_institucional=user_data.email_institucional,
        nombre_completo=user_data.nombre_completo,
        password_hash=hash_password(user_data.password),
        rol=user_data.rol
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión en el sistema
    
    - **codigo_institucional**: Código del usuario
    - **password**: Contraseña
    
    Retorna un token JWT para autenticación en otros endpoints
    """
    # Buscar usuario
    user = db.query(User).filter(
        User.codigo_institucional == credentials.codigo_institucional
    ).first()
    
    # Verificar credenciales
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código institucional o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Crear token JWT
    token = create_access_token(data={
        "sub": str(user.id),
        "rol": user.rol,
        "codigo": user.codigo_institucional
    })
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtener información del usuario autenticado actual
    
    Requiere token JWT en el header: Authorization: Bearer {token}
    """
    return current_user
