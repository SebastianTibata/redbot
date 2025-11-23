# en app/adapters/http/routes.py

from fastapi import APIRouter, Depends

# Importa el Caso de Uso (lógica)
from ...domain.use_cases import AuthUseCases

# Importa los DTOs (schemas)
from ... import schemas

# Importa el "proveedor" de Casos de Uso
from ...dependencies import get_auth_use_cases

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate, 
    use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    return use_cases.register_new_user(user_data=user)

@router.post("/login")
def login_for_access_token(
    user: schemas.UserLogin, 
    use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    return use_cases.login_user(user_data=user)