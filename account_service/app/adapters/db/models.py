from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ...database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)   # FK hacia tabla users (otro servicio)
    platform = Column(String, nullable=False)   # "instagram", "reddit", "mastodon"
    handle = Column(String, nullable=False)     # username o nombre de la cuenta
    token = Column(String, nullable=False)      # access token (por ahora texto plano)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
