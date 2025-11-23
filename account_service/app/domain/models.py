# en app/domain/models.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Account(BaseModel):
    """
    Este es el modelo de Dominio puro.
    No sabe nada de SQLAlchemy.
    """
    id: int
    user_id: int
    platform: str
    handle: str
    token: str
    created_at: datetime

    # Configuración de Pydantic V2 para "traducir"
    # desde modelos SQLAlchemy (antiguo orm_mode)
    model_config = ConfigDict(from_attributes=True)