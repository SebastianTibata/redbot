from sqlalchemy import Column, Integer, String, JSON, DateTime, func, ForeignKey
from ...database import Base

# --- Modelo copiado desde account_service ---
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    platform = Column(String, nullable=False)
    handle = Column(String, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- Modelo original de task_service ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    # Establecemos la relación con la tabla de cuentas
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type = Column(String, nullable=False)
    config_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending", nullable=False)