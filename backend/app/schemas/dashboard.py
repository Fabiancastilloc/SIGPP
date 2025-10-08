from pydantic import BaseModel
from typing import List
from decimal import Decimal

class ProjectStats(BaseModel):
    total_proyectos: int
    proyectos_activos: int
    proyectos_pendientes: int
    proyectos_finalizados: int

class BudgetStats(BaseModel):
    presupuesto_total_asignado: Decimal
    presupuesto_total_ejecutado: Decimal
    presupuesto_disponible: Decimal
    porcentaje_ejecucion: float

class ExpenseStats(BaseModel):
    total_gastos: int
    gastos_pendientes: int
    gastos_aprobados: int
    gastos_rechazados: int
    monto_total_aprobado: Decimal

class DashboardResponse(BaseModel):
    proyectos: ProjectStats
    presupuesto: BudgetStats
    gastos: ExpenseStats

class ProyectoResumen(BaseModel):
    id: int
    codigo_proyecto: str
    nombre: str
    estado: str
    presupuesto_asignado: Decimal
    presupuesto_ejecutado: Decimal
    porcentaje_ejecutado: float

class TopProyectosResponse(BaseModel):
    proyectos_mayor_ejecucion: List[ProyectoResumen]
    proyectos_menor_ejecucion: List[ProyectoResumen]
