from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from sqlalchemy.orm import relationship
import enum

class ProjectStatus(enum.Enum):
    DRAFT = "borrador"
    PENDING_PROFESSOR = "pendiente_profesor"
    PENDING_FINANCE = "pendiente_financiera"
    ACTIVE = "activo"
    REJECTED = "rechazado"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_proyecto = Column(String, unique=True, nullable=False, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    objetivos = Column(Text, nullable=False)
    
    estudiante_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profesor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    presupuesto_estimado = Column(Numeric(12, 2), nullable=False)
    presupuesto_asignado = Column(Numeric(12, 2), nullable=True)
    presupuesto_ejecutado = Column(Numeric(12, 2), default=0)
    
    estado = Column(Enum(ProjectStatus, values_callable=lambda obj: [e.value for e in obj]), default=ProjectStatus.DRAFT)
    comentarios_profesor = Column(Text, nullable=True)
    comentarios_financiera = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    estudiante = relationship("User", foreign_keys=[estudiante_id], back_populates="projects_created")
    profesor = relationship("User", foreign_keys=[profesor_id], back_populates="projects_advised")
    expenses = relationship("Expense", back_populates="project")
    history = relationship("ProjectHistory", back_populates="project")

    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")