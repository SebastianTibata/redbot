# en app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

# Importar implementaciones (Adaptadores)
from .adapters.db.sqlalchemy_repository import SQLAlchemyTaskRepository
from .adapters.ai.gemini_service import GeminiAIGenerator
from .database import get_db # Importar el provider de DB original

# Importar interfaces (Puertos) y Casos de Uso
from .domain.ports import TaskRepositoryPort, AIGeneratorPort
from .domain.use_cases import TaskUseCases

# --- Proveedores de Dependencias ---

def get_task_repository(db: Session = Depends(get_db)) -> TaskRepositoryPort:
    """
    Proveedor del Repositorio.
    Aquí "enchufamos" el adaptador de SQLAlchemy al puerto.
    """
    return SQLAlchemyTaskRepository(db)

def get_ai_generator() -> AIGeneratorPort:
    """
    Proveedor del Generador de IA.
    Aquí "enchufamos" el adaptador de Gemini al puerto.
    """
    return GeminiAIGenerator()

def get_task_use_cases(
    repo: TaskRepositoryPort = Depends(get_task_repository),
    ai: AIGeneratorPort = Depends(get_ai_generator)
) -> TaskUseCases:
    """
    Proveedor de Casos de Uso.
    Construye la clase de lógica de negocio inyectándole
    las implementaciones concretas que acaba de recibir.
    """
    return TaskUseCases(task_repo=repo, ai_generator=ai)