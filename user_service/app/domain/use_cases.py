# en app/domain/use_cases.py

from typing import List, Optional
from fastapi import HTTPException

# Importa el "Puerto" (contrato)
from .ports import UserRepositoryPort

# Importa los modelos Puros y los DTOs
from .models import User
from ..schemas import UserCreate, UserUpdate

class UserUseCases:
    """
    Esta clase contiene la lógica de negocio pura (Casos de Uso).
    No sabe nada de SQLAlchemy. Solo habla con "Puertos".

    Es el reemplazo de tu antiguo 'UserService'.
    """
    def __init__(self, user_repo: UserRepositoryPort):
        # Recibe la implementación del repositorio a través de inyección de dependencias
        self.user_repo = user_repo

    def get_all(self) -> List[User]:
        return self.user_repo.get_all_users()

    def create_new(self, user_data: UserCreate) -> User:
        # Aquí podríamos añadir lógica de negocio, como verificar si el email ya existe
        return self.user_repo.save_user(user_data)

    def update_existing(self, user_id: int, user_data: UserUpdate) -> User:
        updated_user = self.user_repo.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return updated_user

    def delete_existing(self, user_id: int) -> dict:
        deleted_user = self.user_repo.delete_user(user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado"}