# en app/adapters/http/routes.py

from fastapi import APIRouter, Depends
from typing import List

# Importa el Caso de Uso (lógica) y el Modelo de Dominio (puro)
from ...domain.use_cases import UserUseCases
from ...domain.models import User as DomainUser

# Importa los Schemas (DTOs)
from ... import schemas

# Importa las dependencias
from .dependencies import get_current_admin
from ...dependencies import get_user_use_cases # Importa el "proveedor"

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[DomainUser])
def get_all_users(
    admin = Depends(get_current_admin),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    return use_cases.get_all()

@router.post("/", response_model=DomainUser)
def create_new_user(
    user: schemas.UserCreate,
    admin = Depends(get_current_admin),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    return use_cases.create_new(user_data=user)

@router.put("/{user_id}", response_model=DomainUser)
def update_existing_user(
    user_id: int,
    user: schemas.UserUpdate,
    admin = Depends(get_current_admin),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    return use_cases.update_existing(user_id=user_id, user_data=user)

@router.delete("/{user_id}")
def delete_a_user(
    user_id: int,
    admin = Depends(get_current_admin),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    return use_cases.delete_existing(user_id=user_id)