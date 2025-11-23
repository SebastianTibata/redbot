# en app/adapters/http/routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List # <-- IMPORTACIÓN AÑADIDA
from ... import schemas
from ...domain.use_cases import TaskUseCases
from ...domain.models import Task as DomainTask # <-- IMPORTA EL MODELO DE DOMINIO
from .dependencies import get_current_user_id, ensure_task_owner
from pydantic import BaseModel
import json

# Importa el provider desde el archivo de dependencias
from ...dependencies import get_task_use_cases 

router = APIRouter(prefix="/tasks", tags=["tasks"])

class AIPrompt(BaseModel):
    prompt: str

@router.post("/generate-from-prompt", response_model=dict)
def generate_task_from_ai(
    prompt_data: AIPrompt,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        json_string = task_use_cases.generate_task_from_prompt(prompt=prompt_data.prompt)
        return json.loads(json_string)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ▼▼▼ RUTA CORREGIDA ▼▼▼
@router.post("/", response_model=DomainTask) # <-- Corregido de schemas.Task a DomainTask
def create_user_task(
    task: schemas.TaskCreate,
    user_id: int = Depends(get_current_user_id),
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    return task_use_cases.create_new_task(task_data=task, user_id=user_id)

# ▼▼▼ RUTA CORREGIDA ▼▼▼
@router.get("/", response_model=List[DomainTask]) # <-- Corregido de list[schemas.Task]
def list_user_tasks(
    user_id: int = Depends(get_current_user_id),
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    return task_use_cases.get_tasks_for_user(user_id=user_id)

@router.get("/{task_id}", response_model=DomainTask)
def get_single_task(
    task_id: int,
    use_cases: TaskUseCases = Depends(get_task_use_cases),
    task: DomainTask = Depends(ensure_task_owner) 
):
    return task

@router.put("/{task_id}", response_model=DomainTask)
def update_existing_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    use_cases: TaskUseCases = Depends(get_task_use_cases),
    _ = Depends(ensure_task_owner) 
):
    return use_cases.update_existing_task(task_id, task_data)

@router.delete("/{task_id}")
def delete_user_task(
    task: DomainTask = Depends(ensure_task_owner),
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    return task_use_cases.delete_task_for_user(task=task)