from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from decimal import Decimal
from ..database import get_db
from ..models.user import User
from ..models.project import Project, ProjectStatus
from ..models.expense import Expense, ExpenseStatus
from ..schemas.expense import ExpenseApprove
from ..utils.permissions import get_current_user, require_role
from ..services.audit import log_action
import os
import uuid

router = APIRouter(prefix="/projects/{project_id}/expenses", tags=["Expenses"])

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
async def create_expense(
    project_id: int,
    concepto: str = Form(...),
    monto: Decimal = Form(...),
    soporte: UploadFile = File(...),
    current_user: User = Depends(require_role(["estudiante"])),
    db: Session = Depends(get_db)
):
    # Validar proyecto activo
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.estudiante_id == current_user.id,
        Project.estado == ProjectStatus.ACTIVE
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o no activo")
    
    # Validar saldo
    saldo_disponible = project.presupuesto_asignado - project.presupuesto_ejecutado
    if monto > saldo_disponible:
        raise HTTPException(status_code=400, detail="Monto excede saldo disponible")
    
    # Guardar archivo
    file_extension = soporte.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        content = await soporte.read()
        f.write(content)
    
    # Crear gasto
    new_expense = Expense(
        project_id=project.id,
        concepto=concepto,
        monto=monto,
        soporte_url=file_name,
        registrado_por=current_user.id
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    log_action(db, current_user.id, "REGISTRAR_GASTO", "expenses", new_expense.id)
    
    return {"message": "Gasto registrado exitosamente", "id": new_expense.id}

@router.get("")
def get_expenses(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar acceso al proyecto
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    if current_user.rol.value not in ["financiera", "auditor", "superusuario"]:
        if project.estudiante_id != current_user.id and project.profesor_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acceso denegado")
    
    expenses = db.query(Expense).filter(Expense.project_id == project_id).all()
    
    return [{
        "id": e.id,
        "concepto": e.concepto,
        "monto": float(e.monto),
        "estado": e.estado.value,
        "soporte_url": e.soporte_url,
        "created_at": e.created_at.isoformat()
    } for e in expenses]

@router.post("/{expense_id}/approve")
def approve_expense(
    project_id: int,
    expense_id: int,
    approval: ExpenseApprove,
    current_user: User = Depends(require_role(["profesor"])),
    db: Session = Depends(get_db)
):
    # Validar gasto y proyecto
    expense = db.query(Expense).join(Project).filter(
        Expense.id == expense_id,
        Expense.project_id == project_id,
        Project.profesor_id == current_user.id,
        Expense.estado == ExpenseStatus.PENDING
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    if approval.accion == "aprobar":
        expense.estado = ExpenseStatus.APPROVED
        expense.aprobado_por = current_user.id
        
        # Actualizar presupuesto ejecutado
        project = expense.project
        project.presupuesto_ejecutado += expense.monto
        
        message = "Gasto aprobado exitosamente"
    else:
        expense.estado = ExpenseStatus.REJECTED
        expense.comentario = approval.comentario
        message = "Gasto rechazado"
    
    db.commit()
    log_action(db, current_user.id, "APROBAR_GASTO", "expenses", expense.id)
    
    return {"message": message}