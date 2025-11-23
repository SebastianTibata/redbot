# en app/schemas.py (dentro de task_service)

from pydantic import BaseModel
from typing import Optional, Dict, Any

# --- Esquema para Crear ---

class TaskCreate(BaseModel):
    """
    Schema para crear una tarea.
    """
    account_id: int
    type: str
    config_json: Dict[str, Any]

# --- Esquema para Actualizar (Update) ---

class TaskUpdate(BaseModel):
    """
    Schema para actualizar una tarea.
    Todos los campos son opcionales.
    """
    type: Optional[str] = None
    config_json: Optional[Dict[str, Any]] = None

    class Config:
        # Pydantic v2 usa esto en lugar de orm_mode
        from_attributes = True