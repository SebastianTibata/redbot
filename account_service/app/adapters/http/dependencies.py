# en app/adapters/http/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ...config import settings 
from ...domain.ports import AccountRepositoryPort
from ...domain.models import Account

# ▼▼▼ IMPORTACIÓN CORREGIDA ▼▼▼
# Ya no importa de 'main.py', sino del nuevo archivo de dependencias
from ...dependencies import get_account_repository 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return int(user_id)

def ensure_account_owner(
    account_id: int, 
    repo: AccountRepositoryPort = Depends(get_account_repository),
    current_user_id: int = Depends(get_current_user_id)
) -> Account:
    """
    Dependencia que asegura que el usuario actual es el dueño de la cuenta.
    """
    account = repo.get_account_by_id(account_id)
    if not account or account.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso sobre esta cuenta.")
    return account