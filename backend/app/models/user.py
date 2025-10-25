from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import enum

class RoleEnum(enum.Enum):
    SUPERUSUARIO = "superusuario"
    ESTUDIANTE = "estudiante"
    PROFESOR = "profesor"
    FINANCIERA = "financiera"
    AUDITOR = "auditor"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_institucional = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre_completo = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(Enum(RoleEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    
    # Catálogos
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=True)
    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=True)
    semestre = Column(Integer, nullable=True)
    
    # Auditoría
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sede = relationship("Sede", back_populates="users")
    facultad = relationship("Facultad", back_populates="users")
    carrera = relationship("Carrera", back_populates="users")
    projects_created = relationship("Project", foreign_keys="Project.estudiante_id", back_populates="estudiante")
    projects_advised = relationship("Project", foreign_keys="Project.profesor_id", back_populates="profesor")

class Sede(Base):
    __tablename__ = "sedes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    codigo = Column(String, unique=True, nullable=False)
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="sede")
    facultades = relationship("Facultad", back_populates="sede")

class Facultad(Base):
    __tablename__ = "facultades"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sede = relationship("Sede", back_populates="facultades")
    users = relationship("User", back_populates="facultad")
    carreras = relationship("Carrera", back_populates="facultad")

class Carrera(Base):
    __tablename__ = "carreras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=False)
    duracion_semestres = Column(Integer, default=10)
    modalidad = Column(String, default='presencial')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    facultad = relationship("Facultad", back_populates="carreras")
    users = relationship("User", back_populates="carrera")