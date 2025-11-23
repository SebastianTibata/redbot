# en app/adapters/http/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# --- ▼▼▼ IMPORTACIONES CORREGIDAS ▼▼▼ ---
from ...config import settings 
from ...domain.ports import TaskRepositoryPort  # <-- Importación que faltaba
from ...domain.models import Task             # <-- Importación que faltaba
from ...dependencies import get_task_repository # Importa el provider del repo
# --- ^^^ IMPORTACIONES CORREGIDAS ^^^ ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """
    Decodifica el token JWT para obtener el ID del usuario.
    """
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

def ensure_task_owner(
    task_id: int, 
    repo: TaskRepositoryPort = Depends(get_task_repository),
    current_user_id: int = Depends(get_current_user_id)
) -> Task:
    """
    Dependencia que asegura que el usuario actual es el dueño de la tarea.
    """
    task = repo.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    
    # Verificamos la pertenencia a través de la cuenta asociada
    account = repo.get_account_by_id_and_user(
        account_id=task.account_id,
        user_id=current_user_id
    )
    if not account:
        raise HTTPException(status_code=403, detail="No tienes permiso sobre esta tarea.")
    
    return task