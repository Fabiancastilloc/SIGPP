# backend/app/routers/expenses.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from typing import Optional
import os
import uuid

from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.expense import Expense
from ..utils.permissions import get_current_user
from ..services.audit import log_action

router = APIRouter(prefix="/projects/{project_id}/expenses", tags=["Expenses"])

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
async def create_expense(
    project_id: int,
    concepto: str = Form(...),
    monto: Decimal = Form(...),
    categoria: str = Form(..., description="Material, Equipo, Servicio, Transporte, Otro"),
    descripcion: str = Form(""),
    fecha: str = Form(...),
    factura_numero: Optional[str] = Form(None),
    soporte: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear gasto - Solo estudiantes dueños de proyectos activos"""
    
    # 1. Verificar que el usuario es estudiante
    if current_user.rol.value != 'estudiante':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden registrar gastos"
        )
    
    # 2. Obtener y validar proyecto
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.estudiante_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado o no tienes permisos"
        )
    
    # 3. Verificar que el proyecto está activo
    if project.estado.value != 'activo':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo proyectos activos pueden registrar gastos. Estado actual: {project.estado.value}"
        )
    
    # 4. Verificar presupuesto asignado
    if not project.presupuesto_asignado or project.presupuesto_asignado == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El proyecto no tiene presupuesto asignado"
        )
    
    # 5. Validar monto
    if monto <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El monto debe ser mayor a cero"
        )
    
    # 6. Calcular saldo disponible
    saldo_disponible = float(project.presupuesto_asignado or 0) - float(project.presupuesto_ejecutado or 0)
    
    if float(monto) > saldo_disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Monto excede saldo disponible. Disponible: ${saldo_disponible:,.2f}"
        )
    
    # 7. Validar archivo de soporte
    allowed_ext = {'pdf', 'jpg', 'jpeg', 'png'}
    ext = soporte.filename.rsplit('.', 1)[-1].lower() if '.' in soporte.filename else ''
    
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de soporte no permitido. Use: PDF, JPG, JPEG, PNG"
        )
    
    content = await soporte.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El soporte supera el tamaño máximo de 10MB"
        )
    
    # 8. Guardar archivo
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    # 9. Crear gasto
    try:
        new_expense = Expense(
            project_id=project.id,
            concepto=concepto,
            monto=monto,
            categoria=categoria,
            descripcion=descripcion,
            fecha=datetime.fromisoformat(fecha),
            factura_numero=factura_numero,
            soporte_url=filename,
            registrado_por=current_user.id
        )
        
        db.add(new_expense)
        
        # 10. Actualizar presupuesto ejecutado
        project.presupuesto_ejecutado = Decimal(str(float(project.presupuesto_ejecutado or 0) + float(monto)))
        
        db.commit()
        db.refresh(new_expense)
        
        log_action(db, current_user.id, "REGISTRAR_GASTO", "expenses", new_expense.id)
        
        return {
            "message": "Gasto registrado exitosamente",
            "id": new_expense.id,
            "presupuesto_ejecutado": float(project.presupuesto_ejecutado),
            "saldo_disponible": float(project.presupuesto_asignado) - float(project.presupuesto_ejecutado)
        }
        
    except Exception as e:
        db.rollback()
        # Eliminar archivo si hubo error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear gasto: {str(e)}"
        )


@router.get("")
def get_expenses(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener gastos del proyecto - Acceso según rol"""
    
    # Validar acceso al proyecto
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Validar permisos
    can_view = False
    if current_user.rol.value in ('financiera', 'auditor', 'superusuario'):
        can_view = True
    elif current_user.rol.value == 'estudiante' and project.estudiante_id == current_user.id:
        can_view = True
    elif current_user.rol.value == 'profesor' and project.profesor_id == current_user.id:
        can_view = True
    
    if not can_view:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Obtener gastos
    expenses = db.query(Expense).filter(
        Expense.project_id == project_id
    ).order_by(Expense.created_at.desc()).all()
    
    return [{
        "id": e.id,
        "concepto": e.concepto,
        "monto": float(e.monto),
        "categoria": e.categoria,
        "descripcion": e.descripcion,
        "fecha": e.fecha.isoformat(),
        "factura_numero": e.factura_numero,
        "soporte_url": e.soporte_url,
        "created_at": e.created_at.isoformat()
    } for e in expenses]


@router.get("/{expense_id}")
def get_expense_by_id(
    project_id: int,
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalle de un gasto específico"""
    
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.project_id == project_id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    # Validar acceso
    project = expense.project
    can_view = False
    if current_user.rol.value in ('financiera', 'auditor', 'superusuario'):
        can_view = True
    elif current_user.rol.value == 'estudiante' and project.estudiante_id == current_user.id:
        can_view = True
    elif current_user.rol.value == 'profesor' and project.profesor_id == current_user.id:
        can_view = True
    
    if not can_view:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return {
        "id": expense.id,
        "project_id": expense.project_id,
        "concepto": expense.concepto,
        "monto": float(expense.monto),
        "categoria": expense.categoria,
        "descripcion": expense.descripcion,
        "fecha": expense.fecha.isoformat(),
        "factura_numero": expense.factura_numero,
        "soporte_url": expense.soporte_url,
        "created_at": expense.created_at.isoformat()
    }


@router.delete("/{expense_id}")
def delete_expense(
    project_id: int,
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar gasto - Solo estudiantes dueños"""
    
    if current_user.rol.value != 'estudiante':
        raise HTTPException(status_code=403, detail="Solo estudiantes pueden eliminar gastos")
    
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.project_id == project_id,
        Expense.registrado_por == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado o no tienes permisos")
    
    # Actualizar presupuesto
    project = expense.project
    project.presupuesto_ejecutado = Decimal(str(max(0.0, float(project.presupuesto_ejecutado or 0) - float(expense.monto))))
    
    # Eliminar archivo físico
    if expense.soporte_url:
        filepath = os.path.join(UPLOAD_DIR, expense.soporte_url)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.delete(expense)
    db.commit()
    
    log_action(db, current_user.id, "ELIMINAR_GASTO", "expenses", expense_id)
    
    return {"message": "Gasto eliminado exitosamente"}
