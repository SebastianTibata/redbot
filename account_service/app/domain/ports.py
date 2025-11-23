# en app/domain/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional

# ▼▼▼ LÍNEA CORREGIDA ▼▼▼
# Ahora importamos AccountUpdate junto con AccountCreate
from ..schemas import AccountCreate, AccountUpdate
from .models import Account # Importamos el modelo puro

class AccountRepositoryPort(ABC):
    """
    Define el contrato para CUALQUIER base de datos de cuentas.
    """
    
    @abstractmethod
    def save_account(self, account_data: AccountCreate, user_id: int) -> Account:
        """Guarda una nueva cuenta."""
        pass
        
    @abstractmethod
    def get_accounts_by_user_id(self, user_id: int) -> List[Account]:
        """Obtiene las cuentas de un usuario."""
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Obtiene una cuenta por su ID."""
        pass

    @abstractmethod
    def update_account(self, account_id: int, account_data: AccountUpdate) -> Optional[Account]:
        """Actualiza una cuenta existente."""
        pass

    @abstractmethod
    def delete_account(self, account: Account) -> Account:
        """Elimina una cuenta."""
        pass