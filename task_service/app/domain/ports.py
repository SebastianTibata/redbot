# en app/domain/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional # <-- LÍNEA CORREGIDA (se añadió Optional)
from ..schemas import TaskCreate, TaskUpdate
from .models import Task, Account

class TaskRepositoryPort(ABC):
    """
    Define el contrato para CUALQUIER base de datos de tareas.
    """
    
    @abstractmethod
    def save_task(self, task_data: TaskCreate, user_id: int) -> Task:
        """Guarda una nueva tarea."""
        pass
        
    @abstractmethod
    def get_tasks_by_user_id(self, user_id: int) -> List[Task]:
        """Obtiene las tareas de un usuario."""
        pass

    @abstractmethod
    def get_account_by_id_and_user(self, account_id: int, user_id: int) -> Account:
        """Valida la pertenencia de una cuenta."""
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por su ID."""
        pass
    
    @abstractmethod
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Actualiza una tarea existente."""
        pass
        
    @abstractmethod
    def delete_task(self, task: Task) -> Task:
        """Elimina una tarea."""
        pass
    
    # --- Métodos para Eliminar ---
    
    @abstractmethod
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por su ID."""
        pass
    
    @abstractmethod
    def delete_task(self, task: Task) -> Task:
        """Elimina una tarea."""
        pass

class AIGeneratorPort(ABC):
    """
    Define el contrato para CUALQUIER servicio de IA.
    """
    
    @abstractmethod
    def generate_json_from_prompt(self, prompt: str) -> str:
        """Toma un prompt y devuelve un JSON (como string)."""
        pass