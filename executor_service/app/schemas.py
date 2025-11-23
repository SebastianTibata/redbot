from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime

class ExecutionLogCreate(BaseModel):
    user_id: int
    account_id: str
    task_id: Optional[int]
    task_type: str
    status: str
    detail: Optional[Dict[str, Any]] = None

class ExecutionLog(BaseModel):
    id: int
    user_id: int
    account_id: str
    task_id: Optional[int]
    task_type: str
    status: str
    detail: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        orm_mode = True
