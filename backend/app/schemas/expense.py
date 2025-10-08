from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ExpenseCreate(BaseModel):
    proyecto_id: int
    monto: Decimal = Field(..., gt=0, description="Monto del gasto")
    concepto: str = Field(..., min_length=5, max_length=200)
    soporte_url: str = Field(..., description="URL del comprobante/factura")

class ExpenseUpdate(BaseModel):
    concepto: Optional[str] = Field(None, min_length=5, max_length=200)
    monto: Optional[Decimal] = Field(None, gt=0)
    soporte_url: Optional[str] = None

class ExpenseApproval(BaseModel):
    estado: str = Field(..., pattern="^(aprobado|rechazado)$")
    comentarios: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    proyecto_id: int
    monto: Decimal
    concepto: str
    estado: str
    creado_en: datetime
    
    class Config:
        from_attributes = True

class ExpenseDetail(ExpenseResponse):
    soporte_url: str
    comentarios: Optional[str]
    aprobado_en: Optional[datetime]
    estudiante_id: int
    aprobado_por_id: Optional[int]
    
    class Config:
        from_attributes = True
