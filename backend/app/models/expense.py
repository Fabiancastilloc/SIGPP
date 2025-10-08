from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class EstadoGasto(str, enum.Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class Expense(Base):
    __tablename__ = "gastos"
    
    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto = Column(Numeric(14, 2), nullable=False)
    concepto = Column(String(200), nullable=False)
    soporte_url = Column(String(255), nullable=False)
    estado = Column(SQLEnum(EstadoGasto), default=EstadoGasto.PENDIENTE, index=True)
    comentarios = Column(Text)
    creado_en = Column(DateTime, default=datetime.utcnow)
    aprobado_en = Column(DateTime)
    aprobado_por_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones
    proyecto = relationship("Project", back_populates="gastos")
    estudiante = relationship("User", foreign_keys=[estudiante_id])
    aprobado_por = relationship("User", foreign_keys=[aprobado_por_id])
