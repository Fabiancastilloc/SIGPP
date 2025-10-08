from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class BudgetItemCreate(BaseModel):
    concepto: str = Field(..., min_length=5, max_length=120)
    justificacion: str = Field(..., min_length=10)
    costo: Decimal = Field(..., gt=0)

class BudgetItemResponse(BaseModel):
    id: int
    concepto: str
    justificacion: str
    costo: Decimal
    
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    nombre: str = Field(..., min_length=10, max_length=200)
    descripcion: str = Field(..., min_length=20)
    objetivos: str = Field(..., min_length=20)
    profesor_id: int
    items_presupuesto: List[BudgetItemCreate]

class ProjectUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=10, max_length=200)
    descripcion: Optional[str] = Field(None, min_length=20)
    objetivos: Optional[str] = Field(None, min_length=20)
    profesor_id: Optional[int] = None

class ProjectResponse(BaseModel):
    id: int
    codigo_proyecto: str
    nombre: str
    estado: str
    presupuesto_estimado: Decimal
    presupuesto_asignado: Optional[Decimal]
    presupuesto_ejecutado: Decimal
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class ProjectDetail(ProjectResponse):
    descripcion: str
    objetivos: str
    estudiante_id: int
    profesor_id: Optional[int]
    items_presupuesto: List[BudgetItemResponse]
    fecha_ultima_modificacion: datetime
    
    class Config:
        from_attributes = True
