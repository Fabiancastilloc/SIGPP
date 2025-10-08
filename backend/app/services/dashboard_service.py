from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project, EstadoProyecto
from app.models.expense import Expense, EstadoGasto
from app.models.user import User, RolEnum
from decimal import Decimal
from typing import List

def obtener_estadisticas_proyectos(db: Session, usuario: User) -> dict:
    """Obtiene estadísticas de proyectos según el rol del usuario"""
    
    query = db.query(Project)
    
    # Filtrar según rol
    if usuario.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == usuario.id)
    elif usuario.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == usuario.id)
    
    total = query.count()
    activos = query.filter(Project.estado == EstadoProyecto.ACTIVO).count()
    pendientes = query.filter(
        Project.estado.in_([EstadoProyecto.PENDIENTE_VALIDACION, EstadoProyecto.VALIDADO_ASESOR])
    ).count()
    finalizados = query.filter(Project.estado == EstadoProyecto.FINALIZADO).count()
    
    return {
        "total_proyectos": total,
        "proyectos_activos": activos,
        "proyectos_pendientes": pendientes,
        "proyectos_finalizados": finalizados
    }

def obtener_estadisticas_presupuesto(db: Session, usuario: User) -> dict:
    """Obtiene estadísticas de presupuesto"""
    
    query = db.query(Project).filter(
        Project.estado == EstadoProyecto.ACTIVO
    )
    
    # Filtrar según rol
    if usuario.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == usuario.id)
    elif usuario.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == usuario.id)
    
    proyectos = query.all()
    
    total_asignado = sum(p.presupuesto_asignado or 0 for p in proyectos)
    total_ejecutado = sum(p.presupuesto_ejecutado for p in proyectos)
    disponible = total_asignado - total_ejecutado
    porcentaje = round((total_ejecutado / total_asignado * 100) if total_asignado > 0 else 0, 2)
    
    return {
        "presupuesto_total_asignado": total_asignado,
        "presupuesto_total_ejecutado": total_ejecutado,
        "presupuesto_disponible": disponible,
        "porcentaje_ejecucion": porcentaje
    }

def obtener_estadisticas_gastos(db: Session, usuario: User) -> dict:
    """Obtiene estadísticas de gastos"""
    
    query = db.query(Expense)
    
    # Filtrar según rol
    if usuario.rol == RolEnum.ESTUDIANTE:
        proyectos_ids = db.query(Project.id).filter(
            Project.estudiante_id == usuario.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    elif usuario.rol == RolEnum.PROFESOR:
        proyectos_ids = db.query(Project.id).filter(
            Project.profesor_id == usuario.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    
    total = query.count()
    pendientes = query.filter(Expense.estado == EstadoGasto.PENDIENTE).count()
    aprobados = query.filter(Expense.estado == EstadoGasto.APROBADO).count()
    rechazados = query.filter(Expense.estado == EstadoGasto.RECHAZADO).count()
    
    # Monto total aprobado
    gastos_aprobados = query.filter(Expense.estado == EstadoGasto.APROBADO).all()
    monto_total = sum(g.monto for g in gastos_aprobados)
    
    return {
        "total_gastos": total,
        "gastos_pendientes": pendientes,
        "gastos_aprobados": aprobados,
        "gastos_rechazados": rechazados,
        "monto_total_aprobado": monto_total
    }

def obtener_top_proyectos(db: Session, usuario: User, limit: int = 5) -> dict:
    """Obtiene los proyectos con mayor y menor ejecución presupuestal"""
    
    query = db.query(Project).filter(
        Project.estado == EstadoProyecto.ACTIVO,
        Project.presupuesto_asignado != None
    )
    
    # Filtrar según rol
    if usuario.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == usuario.id)
    elif usuario.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == usuario.id)
    
    proyectos = query.all()
    
    # Calcular porcentajes
    proyectos_con_porcentaje = []
    for p in proyectos:
        porcentaje = (p.presupuesto_ejecutado / p.presupuesto_asignado * 100) if p.presupuesto_asignado > 0 else 0
        proyectos_con_porcentaje.append({
            "id": p.id,
            "codigo_proyecto": p.codigo_proyecto,
            "nombre": p.nombre,
            "estado": p.estado.value,
            "presupuesto_asignado": p.presupuesto_asignado,
            "presupuesto_ejecutado": p.presupuesto_ejecutado,
            "porcentaje_ejecutado": round(porcentaje, 2)
        })
    
    # Ordenar por porcentaje
    mayor_ejecucion = sorted(proyectos_con_porcentaje, key=lambda x: x["porcentaje_ejecutado"], reverse=True)[:limit]
    menor_ejecucion = sorted(proyectos_con_porcentaje, key=lambda x: x["porcentaje_ejecutado"])[:limit]
    
    return {
        "proyectos_mayor_ejecucion": mayor_ejecucion,
        "proyectos_menor_ejecucion": menor_ejecucion
    }
