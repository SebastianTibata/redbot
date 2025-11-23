# en app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

# Importar implementaciones (Adaptadores)
from .adapters.db.sqlalchemy_repository import SQLAlchemyUserRepository
from .database import get_db

# Importar interfaces (Puertos) y Casos de Uso
from .domain.ports import UserRepositoryPort
from .domain.use_cases import UserUseCases

# --- Proveedores de Dependencias ---

def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryPort:
    """
    Proveedor del Repositorio.
    Aquí "enchufamos" el adaptador de SQLAlchemy al puerto.
    """
    return SQLAlchemyUserRepository(db)

def get_user_use_cases(
    repo: UserRepositoryPort = Depends(get_user_repository)
) -> UserUseCases:
    """
    Proveedor de Casos de Uso.
    Construye la clase de lógica de negocio inyectándole
    la implementación concreta (el repositorio).
    """
    return UserUseCases(user_repo=repo)