from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from .security import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    print(f"🔐 Token recibido: {token[:30]}...")
    
    payload = decode_token(token)
    if not payload:
        print("❌ Token inválido o expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id_str = payload.get("sub")
    print(f"👤 Usuario ID del token (string): {user_id_str}")
    
    # ✅ Convertir string a int
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        print(f"❌ Error convirtiendo user_id: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print(f"❌ Usuario {user_id} no encontrado en BD")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    print(f"✅ Usuario autenticado: {user.nombre_completo} ({user.rol.value})")
    return user

def require_role(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.rol.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        return current_user
    return role_checker
