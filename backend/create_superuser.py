import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User, RoleEnum, Sede, Facultad, Carrera
from app.utils.security import get_password_hash

def create_initial_data():
    db: Session = SessionLocal()
    
    # Crear catÃ¡logos iniciales
    sede = Sede(nombre="Sede Central")
    db.add(sede)
    db.commit()
    db.refresh(sede)
    
    facultad = Facultad(nombre="Facultad de IngenierÃ­a", sede_id=sede.id)
    db.add(facultad)
    db.commit()
    db.refresh(facultad)
    
    carrera = Carrera(nombre="IngenierÃ­a de Software", facultad_id=facultad.id)
    db.add(carrera)
    db.commit()
    
    # Crear superusuario
    superuser = User(
        codigo_institucional="SUPER001",
        email="admin@unicartagena.edu.co",
        nombre_completo="Administrador del Sistema",
        password_hash=get_password_hash("admin123"),
        rol=RoleEnum.SUPERUSER,
        sede_id=sede.id
    )
    db.add(superuser)
    db.commit()
    
    print("âœ… Datos iniciales creados")
    print("ðŸ“§ Superusuario: SUPER001 / admin123")
    db.close()

if __name__ == "__main__":
    init_db()
    create_initial_data()