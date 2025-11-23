# en app/domain/use_cases.py

from fastapi import HTTPException
from typing import List, Optional
from .ports import TaskRepositoryPort, AIGeneratorPort # <-- Depende de PUERTOS
from .models import Task                               # <-- Usa Modelos de DOMINIO
from ..schemas import TaskCreate, TaskUpdate

class TaskUseCases:
    """
    Esta clase contiene la lógica de negocio pura (Casos de Uso).
    No sabe qué es SQLAlchemy o Gemini. Solo habla con "Puertos".
    """
    def __init__(self, task_repo: TaskRepositoryPort, ai_generator: AIGeneratorPort):
        self.task_repo = task_repo
        self.ai_generator = ai_generator

    def create_new_task(self, task_data: TaskCreate, user_id: int) -> Task:
        # Lógica de negocio: verificar que la cuenta pertenece al usuario
        account = self.task_repo.get_account_by_id_and_user(
            account_id=task_data.account_id,
            user_id=user_id
        )
        if not account:
            raise HTTPException(status_code=403, detail="La cuenta especificada no te pertenece.")

        # Llama al puerto del repositorio para guardar
        return self.task_repo.save_task(task_data=task_data, user_id=user_id)

    def get_tasks_for_user(self, user_id: int) -> List[Task]:
        # Llama al puerto del repositorio para obtener datos
        return self.task_repo.get_tasks_by_user_id(user_id=user_id)

    def generate_task_from_prompt(self, prompt: str) -> str:
        try:
            # Llama al puerto de IA para generar el JSON
            return self.ai_generator.generate_json_from_prompt(prompt)
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_task_by_id(self, task_id: int) -> Task:
        """Obtiene una sola tarea por ID."""
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task

    def update_existing_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        """Actualiza una tarea."""
        updated_task = self.task_repo.update_task(task_id, task_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return updated_task
        
    def delete_task_for_user(self, task: Task) -> dict:
        # La lógica de negocio (verificar pertenencia)
        # ya la hicimos en el 'ensure_task_owner' (Paso 3).
        # Así que aquí, simplemente llamamos al repositorio.
        deleted_task = self.task_repo.delete_task(task)
        return {"detail": f"Tarea {deleted_task.id} eliminada."}