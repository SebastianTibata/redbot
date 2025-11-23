# en app/domain/use_cases.py

from typing import List, Optional

# Importa los "Puertos" (contratos)
from .ports import AccountRepositoryPort

# Importa los modelos Puros y los DTOs
from .models import Account
from ..schemas import AccountCreate, AccountUpdate
from fastapi import HTTPException # <-- Importa HTTPException

class AccountUseCases:
    """
    Esta clase contiene la lógica de negocio pura (Casos de Uso).
    No sabe qué es SQLAlchemy. Solo habla con "Puertos".

    Es el reemplazo de tu antiguo 'AccountService'.
    """
    def __init__(self, account_repo: AccountRepositoryPort):
        # Recibe la implementación del repositorio a través de inyección de dependencias
        self.account_repo = account_repo

    def create_new_account(self, account_data: AccountCreate, user_id: int) -> Account:
        # La lógica de negocio es simplemente llamar al puerto del repositorio
        return self.account_repo.save_account(account_data=account_data, user_id=user_id)

    def get_accounts_by_user(self, user_id: int) -> List[Account]:
        return self.account_repo.get_accounts_by_user_id(user_id=user_id)

    def delete_user_account(self, account: Account) -> Account:
        # (Aquí podríamos añadir lógica de negocio, como verificar si la cuenta
        # tiene tareas activas antes de permitir borrarla).

        return self.account_repo.delete_account(account=account)
    def get_account_by_id(self, account_id: int) -> Account:
        """Obtiene una sola cuenta por ID."""
        account = self.account_repo.get_account_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return account

    def update_existing_account(self, account_id: int, account_data: AccountUpdate) -> Account:
        """Actualiza una cuenta."""
        updated_account = self.account_repo.update_account(account_id, account_data)
        if not updated_account:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return updated_account