# backend/app/models/expense.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    concepto = Column(String(200), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    categoria = Column(String(50), nullable=False)  # Material, Equipo, Servicio, Transporte, Otro
    descripcion = Column(Text, nullable=True)
    fecha = Column(Date, nullable=False)
    factura_numero = Column(String(100), nullable=True)
    soporte_url = Column(String(255), nullable=False)
    registrado_por = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="expenses")
    registrado_por_user = relationship("User", foreign_keys=[registrado_por])
