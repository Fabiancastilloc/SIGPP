from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class EstadoProyecto(str, enum.Enum):
    BORRADOR = "borrador"
    PENDIENTE_VALIDACION = "pendiente_validacion"
    VALIDADO_ASESOR = "validado_asesor"
    ACTIVO = "activo"
    RECHAZADO = "rechazado"
    FINALIZADO = "finalizado"

class Project(Base):
    __tablename__ = "proyectos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_proyecto = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    objetivos = Column(Text, nullable=False)
    estado = Column(SQLEnum(EstadoProyecto), default=EstadoProyecto.BORRADOR, index=True)
    presupuesto_estimado = Column(Numeric(14, 2), default=0.00)
    presupuesto_asignado = Column(Numeric(14, 2))
    presupuesto_ejecutado = Column(Numeric(14, 2), default=0.00)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    profesor_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_ultima_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    estudiante = relationship("User", foreign_keys=[estudiante_id])
    profesor = relationship("User", foreign_keys=[profesor_id])
    items_presupuesto = relationship("BudgetItem", back_populates="proyecto", cascade="all, delete-orphan")
    gastos = relationship("Expense", back_populates="proyecto", cascade="all, delete-orphan")

class BudgetItem(Base):
    __tablename__ = "presupuesto_items"
    
    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    concepto = Column(String(120), nullable=False)
    justificacion = Column(Text, nullable=False)
    costo = Column(Numeric(14, 2), nullable=False)
    
    # Relación
    proyecto = relationship("Project", back_populates="items_presupuesto")
