# en app/adapters/http/routes.py

from fastapi import APIRouter, Depends
from typing import List

from ...domain.use_cases import AccountUseCases
from ...domain.models import Account as DomainAccount
from ... import schemas

from .dependencies import get_current_user_id, ensure_account_owner

# ▼▼▼ IMPORTACIÓN CORREGIDA ▼▼▼
from ...dependencies import get_account_use_cases # Ya no importa de 'main'

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[DomainAccount])
def read_user_accounts(
    user_id: int = Depends(get_current_user_id),
    use_cases: AccountUseCases = Depends(get_account_use_cases)
):
    return use_cases.get_accounts_by_user(user_id=user_id)

@router.post("/", response_model=DomainAccount)
def create_new_account(
    account: schemas.AccountCreate,
    user_id: int = Depends(get_current_user_id),
    use_cases: AccountUseCases = Depends(get_account_use_cases)
):
    return use_cases.create_new_account(account_data=account, user_id=user_id)

@router.get("/{account_id}", response_model=DomainAccount)
def get_single_account(
    account_id: int,
    use_cases: AccountUseCases = Depends(get_account_use_cases),
    # Usamos la dependencia para asegurar que el usuario sea el dueño
    _ = Depends(ensure_account_owner) 
):
    # El caso de uso ya maneja el 404
    return use_cases.get_account_by_id(account_id)

@router.put("/{account_id}", response_model=DomainAccount)
def update_existing_account(
    account_id: int,
    account_data: schemas.AccountUpdate,
    use_cases: AccountUseCases = Depends(get_account_use_cases),
    _ = Depends(ensure_account_owner)
):
    return use_cases.update_existing_account(account_id, account_data)

@router.delete("/{account_id}", response_model=DomainAccount)
def delete_user_account(
    account: DomainAccount = Depends(ensure_account_owner),
    use_cases: AccountUseCases = Depends(get_account_use_cases)
):
    return use_cases.delete_user_account(account=account)