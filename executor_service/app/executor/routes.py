# executor_service/app/executor/routes.py
from typing import List, Optional
import os
import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_bearer_token
from ..database import get_db
from ..models import ExecutionLog
from ..schemas import ExecutionLog as ExecutionLogSchema

router = APIRouter()

TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://task_service:8000")


@router.post("/execute/{account_id}")
def execute_tasks(
    account_id: int,
    user=Depends(get_current_user),           # payload JWT (sub/user_id)
    token: str = Depends(get_bearer_token),   # string del JWT para reenviar
    db: Session = Depends(get_db),
):
    user_id = user.get("sub") or user.get("user_id")
    # Si user_id es un string de dígitos, lo convertimos a int
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)

    # 1) Traer todas las tareas del usuario desde task_service
    try:
        resp = requests.get(
            f"{TASK_SERVICE_URL}/tasks/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        resp.raise_for_status()
        tasks = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"No se pudo obtener tareas: {e}")

    # 2) Filtrar por account_id
    tasks_for_account = [t for t in tasks if t.get("account_id") == account_id]

    results = []
    for t in tasks_for_account:
        task_type = t.get("type") or t.get("task_type") or "unknown"
        cfg = t.get("config_json", {})

        # Simulación de ejecución:
        result_detail = {"action": task_type, "config": cfg}
        results.append(result_detail)

        # Guardar log
        log = ExecutionLog(
            user_id=user_id,
            account_id=account_id,
            task_id=t.get("id"),
            task_type=task_type,
            status="success",
            detail=result_detail,
        )
        db.add(log)

    db.commit()
    return {"count": len(tasks_for_account), "results": results}


@router.get("/logs", response_model=List[ExecutionLogSchema])
def get_logs(
    account_id: Optional[int] = Query(default=None, ge=1, description="Filtra por account_id"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Devuelve los logs del usuario autenticado. Puedes filtrar por `account_id`.
    """
    user_id = user.get("sub") or user.get("user_id")
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)

    q = db.query(ExecutionLog).filter(ExecutionLog.user_id == user_id)
    if account_id is not None:
        q = q.filter(ExecutionLog.account_id == account_id)

    # Devolvemos modelos SQLAlchemy (Pydantic los serializa por orm_mode)
    return q.order_by(ExecutionLog.created_at.desc()).all()
