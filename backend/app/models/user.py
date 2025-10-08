from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class RolEnum(str, enum.Enum):
    ESTUDIANTE = "estudiante"
    PROFESOR = "profesor"
    FINANCIERA = "financiera"
    AUDITOR = "auditor"

class User(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_institucional = Column(String(30), unique=True, nullable=False, index=True)
    email_institucional = Column(String(120), unique=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(SQLEnum(RolEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False)  # ← CAMBIO AQUÍ
    facultad_id = Column(Integer, nullable=True)
    sede_id = Column(Integer, nullable=True)
    carrera_id = Column(Integer, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
