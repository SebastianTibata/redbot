# en app/domain/models.py
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    """
    Este es el modelo de Dominio puro.
    No sabe nada de SQLAlchemy.
    """
    id: int
    username: str
    role: str
    # La contraseña hash NO se incluye aquí
    # por seguridad.

    # Configuración de Pydantic V2 para "traducir"
    # desde modelos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)