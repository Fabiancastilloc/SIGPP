from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.dashboard import DashboardResponse, TopProyectosResponse
from app.models.user import User
from app.api.dependencies import get_db, get_current_user
from app.services.dashboard_service import (
    obtener_estadisticas_proyectos,
    obtener_estadisticas_presupuesto,
    obtener_estadisticas_gastos,
    obtener_top_proyectos
)

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas generales del dashboard
    
    Retorna:
    - Estadísticas de proyectos (total, activos, pendientes, finalizados)
    - Estadísticas de presupuesto (asignado, ejecutado, disponible)
    - Estadísticas de gastos (total, pendientes, aprobados, rechazados)
    """
    proyectos_stats = obtener_estadisticas_proyectos(db, current_user)
    presupuesto_stats = obtener_estadisticas_presupuesto(db, current_user)
    gastos_stats = obtener_estadisticas_gastos(db, current_user)
    
    return {
        "proyectos": proyectos_stats,
        "presupuesto": presupuesto_stats,
        "gastos": gastos_stats
    }

@router.get("/top-proyectos", response_model=TopProyectosResponse)
def get_top_projects(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener los proyectos con mayor y menor ejecución presupuestal
    
    Parámetros:
    - limit: Número de proyectos a retornar (default: 5)
    """
    return obtener_top_proyectos(db, current_user, limit)
