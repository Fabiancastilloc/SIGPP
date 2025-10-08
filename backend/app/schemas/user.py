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

class UserLogin(BaseModel):
    codigo_institucional: str
    password: str

class UserResponse(UserBase):
    id: int
    creado_en: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UserResponse
