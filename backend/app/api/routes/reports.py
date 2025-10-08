from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.models.user import User, RolEnum
from app.models.project import Project
from app.models.expense import Expense
from app.api.dependencies import get_db, get_current_user
from typing import Optional
import csv
import io
from datetime import datetime

router = APIRouter()

@router.get("/proyectos/csv")
def export_projects_csv(
    estado: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar lista de proyectos en formato CSV
    """
    query = db.query(Project)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == current_user.id)
    
    # Filtrar por estado si se proporciona
    if estado:
        query = query.filter(Project.estado == estado)
    
    proyectos = query.all()
    
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados
    writer.writerow([
        'Código', 'Nombre', 'Estado', 'Presupuesto Estimado',
        'Presupuesto Asignado', 'Presupuesto Ejecutado',
        'Fecha Creación'
    ])
    
    # Datos
    for p in proyectos:
        writer.writerow([
            p.codigo_proyecto,
            p.nombre,
            p.estado.value,
            float(p.presupuesto_estimado),
            float(p.presupuesto_asignado) if p.presupuesto_asignado else 0,
            float(p.presupuesto_ejecutado),
            p.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=proyectos_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )

@router.get("/gastos/csv")
def export_expenses_csv(
    proyecto_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar lista de gastos en formato CSV
    """
    query = db.query(Expense)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        proyectos_ids = db.query(Project.id).filter(
            Project.estudiante_id == current_user.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    elif current_user.rol == RolEnum.PROFESOR:
        proyectos_ids = db.query(Project.id).filter(
            Project.profesor_id == current_user.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    
    # Filtrar por proyecto si se proporciona
    if proyecto_id:
        query = query.filter(Expense.proyecto_id == proyecto_id)
    
    gastos = query.all()
    
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados
    writer.writerow([
        'ID Gasto', 'ID Proyecto', 'Monto', 'Concepto',
        'Estado', 'Fecha Registro', 'Fecha Aprobación'
    ])
    
    # Datos
    for g in gastos:
        writer.writerow([
            g.id,
            g.proyecto_id,
            float(g.monto),
            g.concepto,
            g.estado.value,
            g.creado_en.strftime('%Y-%m-%d %H:%M:%S'),
            g.aprobado_en.strftime('%Y-%m-%d %H:%M:%S') if g.aprobado_en else ''
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=gastos_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )

@router.get("/resumen/{proyecto_id}")
def get_project_summary(
    proyecto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen completo de un proyecto con todos sus gastos
    """
    proyecto = db.query(Project).filter(Project.id == proyecto_id).first()
    
    if not proyecto:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Obtener gastos del proyecto
    gastos = db.query(Expense).filter(Expense.proyecto_id == proyecto_id).all()
    
    # Calcular estadísticas
    gastos_aprobados = [g for g in gastos if g.estado.value == "aprobado"]
    gastos_pendientes = [g for g in gastos if g.estado.value == "pendiente"]
    gastos_rechazados = [g for g in gastos if g.estado.value == "rechazado"]
    
    return {
        "proyecto": {
            "id": proyecto.id,
            "codigo": proyecto.codigo_proyecto,
            "nombre": proyecto.nombre,
            "estado": proyecto.estado.value,
            "presupuesto_estimado": float(proyecto.presupuesto_estimado),
            "presupuesto_asignado": float(proyecto.presupuesto_asignado) if proyecto.presupuesto_asignado else 0,
            "presupuesto_ejecutado": float(proyecto.presupuesto_ejecutado)
        },
        "gastos": {
            "total": len(gastos),
            "aprobados": len(gastos_aprobados),
            "pendientes": len(gastos_pendientes),
            "rechazados": len(gastos_rechazados),
            "monto_total_aprobado": sum(float(g.monto) for g in gastos_aprobados),
            "detalle": [
                {
                    "id": g.id,
                    "monto": float(g.monto),
                    "concepto": g.concepto,
                    "estado": g.estado.value,
                    "fecha": g.creado_en.strftime('%Y-%m-%d')
                } for g in gastos
            ]
        }
    }
