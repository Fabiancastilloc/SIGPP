from sqlalchemy.orm import Session
from app.models.expense import Expense, EstadoGasto
from app.models.project import Project, EstadoProyecto
from app.models.user import User, RolEnum
from app.schemas.expense import ExpenseCreate
from datetime import datetime
from fastapi import HTTPException, status
from decimal import Decimal
from typing import Optional

def registrar_gasto(
    db: Session,
    gasto_data: ExpenseCreate,
    estudiante_id: int
) -> Expense:
    """Registra un nuevo gasto para un proyecto"""
    
    # Verificar que el proyecto existe y está activo
    proyecto = db.query(Project).filter(Project.id == gasto_data.proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar que el proyecto está activo
    if proyecto.estado != EstadoProyecto.ACTIVO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden registrar gastos en proyectos activos"
        )
    
    # Verificar que el estudiante es el dueño del proyecto
    if proyecto.estudiante_id != estudiante_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para registrar gastos en este proyecto"
        )
    
    # Verificar que hay presupuesto disponible
    presupuesto_disponible = (proyecto.presupuesto_asignado or 0) - proyecto.presupuesto_ejecutado
    
    if gasto_data.monto > presupuesto_disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Presupuesto insuficiente. Disponible: ${presupuesto_disponible}"
        )
    
    # Crear el gasto
    nuevo_gasto = Expense(
        proyecto_id=gasto_data.proyecto_id,
        estudiante_id=estudiante_id,
        monto=gasto_data.monto,
        concepto=gasto_data.concepto,
        soporte_url=gasto_data.soporte_url,
        estado=EstadoGasto.PENDIENTE
    )
    
    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)
    
    return nuevo_gasto

def aprobar_rechazar_gasto(
    db: Session,
    gasto_id: int,
    nuevo_estado: EstadoGasto,
    usuario_id: int,
    comentarios: Optional[str] = None
) -> Expense:
    """Aprueba o rechaza un gasto (profesor o área financiera)"""
    
    gasto = db.query(Expense).filter(Expense.id == gasto_id).first()
    
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    
    if gasto.estado != EstadoGasto.PENDIENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El gasto ya fue {gasto.estado}"
        )
    
    # Si se aprueba, actualizar presupuesto ejecutado
    if nuevo_estado == EstadoGasto.APROBADO:
        proyecto = db.query(Project).filter(Project.id == gasto.proyecto_id).first()
        proyecto.presupuesto_ejecutado += gasto.monto
    
    # Actualizar estado del gasto
    gasto.estado = nuevo_estado
    gasto.aprobado_por_id = usuario_id
    gasto.aprobado_en = datetime.utcnow()
    gasto.comentarios = comentarios
    
    db.commit()
    db.refresh(gasto)
    
    return gasto

def calcular_saldo_proyecto(db: Session, proyecto_id: int) -> dict:
    """Calcula el saldo disponible de un proyecto"""
    
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Calcular gastos pendientes
    gastos_pendientes = db.query(Expense).filter(
        Expense.proyecto_id == proyecto_id,
        Expense.estado == EstadoGasto.PENDIENTE
    ).all()
    
    total_pendiente = sum(gasto.monto for gasto in gastos_pendientes)
    
    presupuesto_asignado = proyecto.presupuesto_asignado or Decimal(0)
    presupuesto_ejecutado = proyecto.presupuesto_ejecutado
    saldo_disponible = presupuesto_asignado - presupuesto_ejecutado - total_pendiente
    
    return {
        "proyecto_id": proyecto_id,
        "presupuesto_asignado": presupuesto_asignado,
        "presupuesto_ejecutado": presupuesto_ejecutado,
        "gastos_pendientes": total_pendiente,
        "saldo_disponible": saldo_disponible,
        "porcentaje_ejecutado": round((presupuesto_ejecutado / presupuesto_asignado * 100) if presupuesto_asignado > 0 else 0, 2)
    }
