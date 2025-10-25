from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ExpenseCreate(BaseModel):
    concepto: str
    monto: Decimal

class ExpenseApprove(BaseModel):
    accion: str  # "aprobar" o "rechazar"
    comentario: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    concepto: str
    monto: Decimal
    estado: str
    soporte_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True