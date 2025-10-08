from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseDetail, ExpenseApproval
from app.models.expense import Expense, EstadoGasto
from app.models.project import Project
from app.models.user import User, RolEnum
from app.api.dependencies import get_db, get_current_user
from app.services.expense_service import (
    registrar_gasto,
    aprobar_rechazar_gasto,
    calcular_saldo_proyecto
)

router = APIRouter()

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    gasto_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo gasto (solo estudiantes)
    
    Requiere:
    - proyecto_id: ID del proyecto
    - monto: Monto del gasto
    - concepto: Descripción del gasto
    - soporte_url: URL del comprobante/factura
    """
    if current_user.rol != RolEnum.ESTUDIANTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden registrar gastos"
        )
    
    gasto = registrar_gasto(db, gasto_data, current_user.id)
    return gasto

@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    proyecto_id: Optional[int] = Query(None),
    estado: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Listar gastos según el rol del usuario
    
    Filtros opcionales:
    - proyecto_id: Filtrar por proyecto
    - estado: pendiente, aprobado, rechazado
    """
    query = db.query(Expense)
    
    # Filtrar según rol
    if current_user.rol == RolEnum.ESTUDIANTE:
        # Solo gastos de sus proyectos
        proyectos_ids = db.query(Project.id).filter(
            Project.estudiante_id == current_user.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    
    elif current_user.rol == RolEnum.PROFESOR:
        # Solo gastos de proyectos donde es asesor
        proyectos_ids = db.query(Project.id).filter(
            Project.profesor_id == current_user.id
        ).all()
        query = query.filter(Expense.proyecto_id.in_([p[0] for p in proyectos_ids]))
    
    # Filtrar por proyecto si se proporciona
    if proyecto_id:
        query = query.filter(Expense.proyecto_id == proyecto_id)
    
    # Filtrar por estado si se proporciona
    if estado:
        try:
            estado_enum = EstadoGasto(estado)
            query = query.filter(Expense.estado == estado_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido: {estado}"
            )
    
    gastos = query.order_by(Expense.creado_en.desc()).offset(skip).limit(limit).all()
    return gastos

@router.get("/{gasto_id}", response_model=ExpenseDetail)
def get_expense(
    gasto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de un gasto específico
    """
    gasto = db.query(Expense).filter(Expense.id == gasto_id).first()
    
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    
    # Verificar permisos
    proyecto = db.query(Project).filter(Project.id == gasto.proyecto_id).first()
    
    if current_user.rol == RolEnum.ESTUDIANTE and proyecto.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este gasto"
        )
    elif current_user.rol == RolEnum.PROFESOR and proyecto.profesor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor del proyecto de este gasto"
        )
    
    return gasto

@router.patch("/{gasto_id}/aprobar", response_model=ExpenseDetail)
def approve_expense(
    gasto_id: int,
    aprobacion: ExpenseApproval,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Aprobar o rechazar un gasto (profesor o área financiera)
    
    Estados: "aprobado" o "rechazado"
    """
    # Verificar que el usuario tiene permiso de aprobar
    if current_user.rol not in [RolEnum.PROFESOR, RolEnum.FINANCIERA]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para aprobar gastos"
        )
    
    # Verificar que el gasto corresponde a un proyecto del profesor (si es profesor)
    if current_user.rol == RolEnum.PROFESOR:
        gasto = db.query(Expense).filter(Expense.id == gasto_id).first()
        if not gasto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gasto no encontrado"
            )
        
        proyecto = db.query(Project).filter(Project.id == gasto.proyecto_id).first()
        if proyecto.profesor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No eres el asesor de este proyecto"
            )
    
    try:
        nuevo_estado = EstadoGasto(aprobacion.estado)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estado inválido"
        )
    
    gasto = aprobar_rechazar_gasto(
        db,
        gasto_id,
        nuevo_estado,
        current_user.id,
        aprobacion.comentarios
    )
    
    return gasto

@router.get("/proyecto/{proyecto_id}/saldo")
def get_project_balance(
    proyecto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener el saldo disponible de un proyecto
    
    Retorna:
    - presupuesto_asignado
    - presupuesto_ejecutado
    - gastos_pendientes
    - saldo_disponible
    - porcentaje_ejecutado
    """
    # Verificar que el proyecto existe
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
            detail="No tienes permiso para ver el saldo de este proyecto"
        )
    elif current_user.rol == RolEnum.PROFESOR and proyecto.profesor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres el asesor de este proyecto"
        )
    
    saldo = calcular_saldo_proyecto(db, proyecto_id)
    return saldo

@router.delete("/{gasto_id}")
def delete_expense(
    gasto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un gasto (solo si está pendiente y es del estudiante)
    """
    gasto = db.query(Expense).filter(Expense.id == gasto_id).first()
    
    if not gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gasto no encontrado"
        )
    
    # Solo el estudiante propietario puede eliminar
    if current_user.rol != RolEnum.ESTUDIANTE or gasto.estudiante_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este gasto"
        )
    
    # Solo se puede eliminar si está pendiente
    if gasto.estado != EstadoGasto.PENDIENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar gastos pendientes"
        )
    
    db.delete(gasto)
    db.commit()
    
    return {"message": "Gasto eliminado correctamente"}
