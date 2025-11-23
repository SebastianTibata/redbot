# executor_service/app/models.py

from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from .database import Base

# Copiado desde account_service/app/models.py
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    platform = Column(String, nullable=False)
    handle = Column(String, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Copiado desde task_service/app/models.py
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    config_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending", nullable=False)