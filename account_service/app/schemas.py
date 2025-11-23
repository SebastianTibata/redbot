# en app/schemas.py (dentro de account_service)

from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    """
    Schema para crear una cuenta.
    """
    platform: str
    handle: str
    token: str

# ▼▼▼ ESTA ES LA CLASE QUE FALTABA ▼▼▼
class AccountUpdate(BaseModel):
    """
    Schema para actualizar una cuenta.
    Todos los campos son opcionales.
    """
    handle: Optional[str] = None
    token: Optional[str] = None

# (Nota: El schema de respuesta 'Account' ahora 
# vive en app/domain/models.py, así que no es necesario aquí)