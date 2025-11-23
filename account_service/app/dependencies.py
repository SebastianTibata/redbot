# en app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

# Importar implementaciones (Adaptadores)
from .adapters.db.sqlalchemy_repository import SQLAlchemyAccountRepository
from .database import get_db

# Importar interfaces (Puertos) y Casos de Uso
from .domain.ports import AccountRepositoryPort
from .domain.use_cases import AccountUseCases

# --- Proveedores de Dependencias ---

def get_account_repository(db: Session = Depends(get_db)) -> AccountRepositoryPort:
    """
    Proveedor del Repositorio.
    Aquí "enchufamos" el adaptador de SQLAlchemy al puerto.
    """
    return SQLAlchemyAccountRepository(db)

def get_account_use_cases(
    repo: AccountRepositoryPort = Depends(get_account_repository)
) -> AccountUseCases:
    """
    Proveedor de Casos de Uso.
    Construye la clase de lógica de negocio inyectándole
    la implementación concreta (el repositorio).
    """
    return AccountUseCases(account_repo=repo)