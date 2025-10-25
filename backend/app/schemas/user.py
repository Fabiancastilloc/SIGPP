from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    codigo_institucional: str
    email: EmailStr
    nombre_completo: str
    password: str
    rol: str
    sede_id: Optional[int] = None
    facultad_id: Optional[int] = None
    carrera_id: Optional[int] = None
    semestre: Optional[int] = None

class UserLogin(BaseModel):
    codigo_institucional: str
    password: str

class UserResponse(BaseModel):
    id: int
    codigo_institucional: str
    email: str
    nombre_completo: str
    rol: str
    sede_id: Optional[int]
    facultad_id: Optional[int]
    carrera_id: Optional[int]
    semestre: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict