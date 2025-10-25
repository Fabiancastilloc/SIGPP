from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class AuditoriaLog(Base):
    __tablename__ = "auditoria_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    accion = Column(String, nullable=False)
    tabla = Column(String, nullable=False)
    registro_id = Column(Integer, nullable=False)
    detalle = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    usuario = relationship("User")

class ProjectHistory(Base):
    __tablename__ = "project_history"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    estado_anterior = Column(String, nullable=True)
    estado_nuevo = Column(String, nullable=False)
    comentario = Column(Text, nullable=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="history")
    usuario = relationship("User")