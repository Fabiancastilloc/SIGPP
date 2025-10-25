from sqlalchemy.orm import Session
from ..models.audit import AuditoriaLog

def log_action(db: Session, usuario_id: int, accion: str, tabla: str, registro_id: int, detalle: str = None, ip: str = None, user_agent: str = None):
    """Registrar acción en log de auditoría"""
    log = AuditoriaLog(
        usuario_id=usuario_id,
        accion=accion,
        tabla=tabla,
        registro_id=registro_id,
        detalle=detalle,
        ip_address=ip,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()