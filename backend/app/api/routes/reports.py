from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.models.user import User, RolEnum
from app.models.project import Project
from app.models.expense import Expense
from app.api.dependencies import get_db, get_current_user
from app.utils.export_utils import (
    crear_pdf_proyectos, 
    crear_excel_proyectos,
    crear_pdf_gastos,
    crear_excel_gastos
)
from typing import Optional, Literal
from datetime import datetime

router = APIRouter()

def serializar_proyecto(proyecto: Project) -> dict:
    """Convierte un proyecto a diccionario para exportación"""
    return {
        'id': proyecto.id,
        'codigo_proyecto': proyecto.codigo_proyecto,
        'nombre': proyecto.nombre,
        'descripcion': proyecto.descripcion,
        'objetivos': proyecto.objetivos,
        'estado': proyecto.estado,
        'presupuesto_estimado': float(proyecto.presupuesto_estimado),
        'presupuesto_asignado': float(proyecto.presupuesto_asignado) if proyecto.presupuesto_asignado else 0,
        'presupuesto_ejecutado': float(proyecto.presupuesto_ejecutado),
        'fecha_creacion': proyecto.fecha_creacion,
        'fecha_ultima_modificacion': proyecto.fecha_ultima_modificacion
    }

def serializar_gasto(gasto: Expense) -> dict:
    """Convierte un gasto a diccionario para exportación"""
    return {
        'id': gasto.id,
        'proyecto_id': gasto.proyecto_id,
        'estudiante_id': gasto.estudiante_id,
        'concepto': gasto.concepto,
        'monto': float(gasto.monto),
        'estado': gasto.estado,
        'soporte_url': gasto.soporte_url,
        'comentarios': gasto.comentarios,
        'creado_en': gasto.creado_en,
        'aprobado_en': gasto.aprobado_en
    }

# ========== EXPORTAR PROYECTOS ==========

@router.get("/proyectos/export")
def export_projects(
    formato: Literal["pdf", "excel"] = Query(..., description="Formato de exportación: pdf o excel"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar lista de proyectos en PDF o Excel
    
    - **formato**: pdf o excel
    - **estado**: (opcional) Filtrar por estado del proyecto
    """
    # Construir query según rol
    query = db.query(Project)
    
    if current_user.rol == RolEnum.ESTUDIANTE:
        query = query.filter(Project.estudiante_id == current_user.id)
    elif current_user.rol == RolEnum.PROFESOR:
        query = query.filter(Project.profesor_id == current_user.id)
    
    # Filtrar por estado si se proporciona
    if estado:
        query = query.filter(Project.estado == estado)
    
    proyectos = query.all()
    proyectos_data = [serializar_proyecto(p) for p in proyectos]
    
    if formato == "pdf":
        buffer = crear_pdf_proyectos(proyectos_data)
        filename = f"proyectos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        media_type = "application/pdf"
    else:  # excel
        buffer = crear_excel_proyectos(proyectos_data)
        filename = f"proyectos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ========== EXPORTAR GASTOS ==========

@router.get("/gastos/export")
def export_expenses(
    formato: Literal["pdf", "excel"] = Query(..., description="Formato de exportación: pdf o excel"),
    proyecto_id: Optional[int] = Query(None, description="Filtrar por proyecto"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Exportar lista de gastos en PDF o Excel
    
    - **formato**: pdf o excel
    - **proyecto_id**: (opcional) Filtrar por proyecto
    - **estado**: (opcional) Filtrar por estado del gasto
    """
    query = db.query(Expense)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        proyectos_ids = db.query(Project.id).filter(Project.estudiante_id == current_user.id).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    elif current_user.rol == RolEnum.PROFESOR:
        proyectos_ids = db.query(Project.id).filter(Project.profesor_id == current_user.id).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    
    # Filtros adicionales
    if proyecto_id:
        query = query.filter(Expense.proyecto_id == proyecto_id)
    if estado:
        query = query.filter(Expense.estado == estado)
    
    gastos = query.all()
    gastos_data = [serializar_gasto(g) for g in gastos]
    
    if formato == "pdf":
        buffer = crear_pdf_gastos(gastos_data)
        filename = f"gastos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        media_type = "application/pdf"
    else:  # excel
        buffer = crear_excel_gastos(gastos_data)
        filename = f"gastos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ========== RESUMEN DE PROYECTO ==========

@router.get("/proyecto/{proyecto_id}/resumen")
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Verificar permisos
    if current_user.rol == RolEnum.ESTUDIANTE and proyecto.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este proyecto"
        )
    elif current_user.rol == RolEnum.PROFESOR and proyecto.profesor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor de este proyecto"
        )
    
    # Obtener gastos del proyecto
    gastos = db.query(Expense).filter(Expense.proyecto_id == proyecto_id).all()
    
    # Calcular estadísticas
    gastos_aprobados = [g for g in gastos if g.estado == "aprobado"]
    gastos_pendientes = [g for g in gastos if g.estado == "pendiente"]
    gastos_rechazados = [g for g in gastos if g.estado == "rechazado"]
    
    return {
        'proyecto': {
            'id': proyecto.id,
            'codigo': proyecto.codigo_proyecto,
            'nombre': proyecto.nombre,
            'estado': proyecto.estado,
            'presupuesto_estimado': float(proyecto.presupuesto_estimado),
            'presupuesto_asignado': float(proyecto.presupuesto_asignado) if proyecto.presupuesto_asignado else 0,
            'presupuesto_ejecutado': float(proyecto.presupuesto_ejecutado)
        },
        'gastos': {
            'total': len(gastos),
            'aprobados': len(gastos_aprobados),
            'pendientes': len(gastos_pendientes),
            'rechazados': len(gastos_rechazados),
            'monto_total_aprobado': sum(float(g.monto) for g in gastos_aprobados),
            'detalle': [
                {
                    'id': g.id,
                    'monto': float(g.monto),
                    'concepto': g.concepto,
                    'estado': g.estado,
                    'fecha': g.creado_en.strftime('%Y-%m-%d')
                }
                for g in gastos
            ]
        }
    }
