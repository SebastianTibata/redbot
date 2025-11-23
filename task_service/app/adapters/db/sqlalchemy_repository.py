# en app/adapters/db/sqlalchemy_repository.py

from sqlalchemy.orm import Session
from app.domain.ports import TaskRepositoryPort
from app.domain.models import Task, Account
from .models import Task as SQLTask, Account as SQLAccount
from ...schemas import TaskCreate, TaskUpdate
from typing import List, Optional  # <-- LÍNEA CORREGIDA (se añadió Optional)

class SQLAlchemyTaskRepository(TaskRepositoryPort):
    """
    Esta es la implementación CONCRETA del puerto de Repositorio
    usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_account_by_id_and_user(self, account_id: int, user_id: int) -> Optional[Account]:
        """ Valida la pertenencia de una cuenta. """
        db_account = self.db.query(SQLAccount).filter(
            SQLAccount.id == account_id,
            SQLAccount.user_id == user_id
        ).first()
        if db_account:
            return Account.model_validate(db_account) # Corregido de from_orm a model_validate
        return None

    def save_task(self, task_data: TaskCreate, user_id: int) -> Task:
        """Guarda una nueva tarea."""
        db_task = SQLTask(
            account_id=task_data.account_id,
            type=task_data.type,
            config_json=task_data.config_json
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return Task.model_validate(db_task) # Corregido de from_orm a model_validate

    def get_tasks_by_user_id(self, user_id: int) -> List[Task]:
        """Obtiene las tareas de un usuario."""
        db_tasks = self.db.query(SQLTask).join(SQLAccount).filter(
            SQLAccount.user_id == user_id
        ).all()
        # Convierte la lista de modelos de BD a modelos de Dominio
        return [Task.model_validate(task) for task in db_tasks] # Corregido

    # --- Métodos para Eliminar ---
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        db_task = self.db.query(SQLTask).filter(SQLTask.id == task_id).first()
        if db_task:
            return Task.model_validate(db_task) # Corregido
        return None
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        db_task = self.db.query(SQLTask).filter(SQLTask.id == task_id).first()
        
        if not db_task:
            return None
        
        # Actualiza los campos que se hayan enviado
        if task_data.type:
            db_task.type = task_data.type
        if task_data.config_json:
            db_task.config_json = task_data.config_json
        
        self.db.commit()
        self.db.refresh(db_task)
        
        return Task.model_validate(db_task)

    def delete_task(self, task: Task) -> Task:
        db_task = self.db.query(SQLTask).filter(SQLTask.id == task.id).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
        return task # Devuelve el modelo de dominio