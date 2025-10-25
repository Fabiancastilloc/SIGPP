from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProjectCreate(BaseModel):
    nombre: str
    descripcion: str
    objetivos: str
    profesor_id: int
    presupuesto_estimado: Decimal
    
    @validator('presupuesto_estimado')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError('El presupuesto debe ser mayor a cero')
        return v

class ProjectSubmit(BaseModel):
    pass

class ProjectValidate(BaseModel):
    accion: str  # "validar" o "devolver"
    comentarios: Optional[str] = None

class ProjectActivate(BaseModel):
    accion: str  # "activar" o "rechazar"
    presupuesto_asignado: Optional[Decimal] = None
    comentarios: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    codigo_proyecto: str
    nombre: str
    descripcion: str
    estado: str
    presupuesto_estimado: Decimal
    presupuesto_asignado: Optional[Decimal]
    presupuesto_ejecutado: Decimal
    estudiante: dict
    profesor: dict
    created_at: datetime
    
    class Config:
        from_attributes = True