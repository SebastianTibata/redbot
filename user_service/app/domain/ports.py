# en app/domain/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..schemas import UserCreate, UserUpdate
from .models import User # Importamos el modelo puro

class UserRepositoryPort(ABC):
    """
    Define el contrato para CUALQUIER base de datos de usuarios.
    """

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios."""
        pass

    @abstractmethod
    def save_user(self, user_data: UserCreate) -> User:
        """Guarda un nuevo usuario."""
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Actualiza un usuario existente."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> Optional[User]:
        """Elimina un usuario por su ID."""
        pass