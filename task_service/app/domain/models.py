# en app/domain/models.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
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

    # ▼▼▼ LÍNEA CORREGIDA ▼▼▼
    # Reemplaza 'class Config' con 'model_config' para Pydantic V2
    model_config = ConfigDict(from_attributes=True)

class Task(BaseModel):
    """
    Este es el modelo de Dominio puro para una Tarea.
    """
    id: int
    account_id: int
    type: str
    config_json: Dict[str, Any]
    created_at: datetime
    status: str

    # ▼▼▼ LÍNEA CORREGIDA ▼▼▼
    # Reemplaza 'class Config' con 'model_config' para Pydantic V2
    model_config = ConfigDict(from_attributes=True)