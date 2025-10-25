from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from ..config import settings

def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verificar contraseña en texto plano (solo desarrollo)"""
    return plain_password == stored_password

def get_password_hash(password: str) -> str:
    """Retornar contraseña sin cifrar (solo desarrollo)"""
    return password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    print(f"🔑 Creando token para usuario: {data.get('sub')}")
    print(f"⏰ Token expira en: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutos")
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """Decodificar y verificar token JWT"""
    try:
        print(f"🔍 Decodificando token: {token[:30]}...")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"✅ Token válido. Usuario ID: {payload.get('sub')}")
        return payload
    except jwt.ExpiredSignatureError:
        print(f"❌ Token expirado")
        return None
    except JWTError as e:
        print(f"❌ Error JWT: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado decodificando token: {str(e)}")
        return None
