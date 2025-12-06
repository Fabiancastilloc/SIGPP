# backend/app/models/project_member.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class MemberRole(str, enum.Enum):
    """Roles de miembros en proyecto"""
    OWNER = "owner"           # Creador del proyecto
    COLLABORATOR = "collaborator"  # Colaborador activo


class RequestStatus(str, enum.Enum):
    """Estados de solicitud de membresía"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProjectMember(Base):
    """Miembros activos de un proyecto"""
    __tablename__ = "project_members"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(MemberRole), default=MemberRole.COLLABORATOR)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="members")
    student = relationship("User")


class MembershipRequest(Base):
    """Solicitudes para unirse a un proyecto"""
    __tablename__ = "membership_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    message = Column(String, nullable=True)  # Mensaje del solicitante
    response_message = Column(String, nullable=True)  # Respuesta del dueño
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    student = relationship("User")
