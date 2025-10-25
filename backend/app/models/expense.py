from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import enum

class ExpenseStatus(enum.Enum):
    PENDING = "pendiente"
    APPROVED = "aprobado"
    REJECTED = "rechazado"

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    concepto = Column(String, nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    soporte_url = Column(String, nullable=False)
    estado = Column(Enum(ExpenseStatus, values_callable=lambda obj: [e.value for e in obj]), default=ExpenseStatus.PENDING)
    comentario = Column(Text, nullable=True)
    
    registrado_por = Column(Integer, ForeignKey("users.id"), nullable=False)
    aprobado_por = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="expenses")
    registrado_por_user = relationship("User", foreign_keys=[registrado_por])
    aprobado_por_user = relationship("User", foreign_keys=[aprobado_por])