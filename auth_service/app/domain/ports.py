# en app/domain/ports.py
from abc import ABC, abstractmethod
from typing import Optional
from ..schemas import UserCreate
from .models import User # Importamos el modelo puro

class AuthRepositoryPort(ABC):
    """
    Define el contrato para la base de datos de autenticación.
    """

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de usuario."""
        pass

    @abstractmethod
    def get_hashed_password(self, username: str) -> Optional[str]:
        """Obtiene solo la contraseña hash de un usuario."""
        pass

    @abstractmethod
    def save_user(self, user_data: UserCreate) -> User:
        """Guarda un nuevo usuario."""
        pass

class TokenServicePort(ABC):
    """
    Define el contrato para un servicio que crea tokens.
    """
    @abstractmethod
    def create_access_token(self, user: User) -> str:
        """Crea un token de acceso para un usuario."""
        pass

class PasswordServicePort(ABC):
    """
    Define el contrato para un servicio que maneja contraseñas.
    """
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña es correcta."""
        pass