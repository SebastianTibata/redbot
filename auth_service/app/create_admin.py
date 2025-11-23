# en app/create_admin.py

from .database import SessionLocal
from .adapters.db.models import User as SQLUser
from .adapters.db.sqlalchemy_repository import SQLAlchemyAuthRepository

db = SessionLocal()

# Instanciamos el adaptador directamente
repo = SQLAlchemyAuthRepository(db)

admin_username = "admin"
admin_password = "admin123"

try:
    # Usamos el método del adaptador
    existing_user = repo.get_user_by_username(admin_username)

    if not existing_user:
        # Creamos un DTO (schema) para pasar al método
        from .schemas import UserCreate
        admin_data = UserCreate(username=admin_username, password=admin_password)

        # Usamos el método 'save_user' del repositorio
        # Nota: El repositorio por defecto lo crea como 'user', 
        # así que lo actualizamos a 'admin'
        new_admin = repo.save_user(admin_data)

        # Actualizar el rol a 'admin'
        db_admin = db.query(SQLUser).filter(SQLUser.id == new_admin.id).first()
        if db_admin:
            db_admin.role = "admin"
            db.commit()
            print(f"Administrador '{admin_username}' creado con éxito.")
        else:
            print("Error al actualizar el rol del admin.")
    else:
        print(f"El usuario '{admin_username}' ya existe.")
finally:
    db.close()