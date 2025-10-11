from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    codigo_institucional: str = Field(..., min_length=5, max_length=30)
    email_institucional: EmailStr
    nombre_completo: str = Field(..., min_length=3, max_length=150)
    rol: str = Field(..., pattern="^(estudiante|profesor|financiera|auditor)$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    facultad_id: Optional[int] = None
    sede_id: Optional[int] = None
    carrera_id: Optional[int] = None
    facultad_custom: Optional[str] = Field(None, max_length=120)
    sede_custom: Optional[str] = Field(None, max_length=120)
    carrera_custom: Optional[str] = Field(None, max_length=120)

class UserLogin(BaseModel):
    codigo_institucional: str
    password: str

class UserResponse(UserBase):
    id: int
    creado_en: datetime
    facultad_id: Optional[int] = None
    sede_id: Optional[int] = None
    carrera_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    facultad_nombre: Optional[str] = None
    sede_nombre: Optional[str] = None
    carrera_nombre: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UserDetailResponse
