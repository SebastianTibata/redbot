# en app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

# Importar implementaciones (Adaptadores)
from .adapters.db.sqlalchemy_repository import SQLAlchemyAuthRepository
from .adapters.security.token_service import JWTTokenService
from .database import get_db

# Importar interfaces (Puertos) y Casos de Uso
from .domain.ports import AuthRepositoryPort, TokenServicePort, PasswordServicePort
from .domain.use_cases import AuthUseCases

# --- Proveedores de Dependencias ---

def get_auth_repository(db: Session = Depends(get_db)) -> AuthRepositoryPort:
    """
    Proveedor del Repositorio.
    Aquí "enchufamos" el adaptador de SQLAlchemy al puerto.
    Devolvemos la clase porque implementa MÚLTIPLES puertos.
    """
    return SQLAlchemyAuthRepository(db)

def get_password_service(
    repo: SQLAlchemyAuthRepository = Depends(get_auth_repository)
) -> PasswordServicePort:
    """Proveedor del Servicio de Contraseña."""
    return repo # La misma clase implementa este puerto

def get_token_service() -> TokenServicePort:
    """Proveedor del Servicio de Token."""
    return JWTTokenService()

def get_auth_use_cases(
    auth_repo: AuthRepositoryPort = Depends(get_auth_repository),
    token_service: TokenServicePort = Depends(get_token_service),
    password_service: PasswordServicePort = Depends(get_password_service)
) -> AuthUseCases:
    """
    Proveedor de Casos de Uso.
    Construye la clase de lógica de negocio inyectándole
    las implementaciones concretas.
    """
    return AuthUseCases(
        auth_repo=auth_repo, 
        token_service=token_service,
        password_service=password_service
    )