# en app/adapters/db/sqlalchemy_repository.py

from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext

# Importa los "Puertos" (contratos) que este adaptador debe cumplir
from app.domain.ports import AuthRepositoryPort, PasswordServicePort

# Importa los modelos Puros (del Dominio) y los Schemas (DTOs)
from app.domain.models import User
from ...schemas import UserCreate

# Importa los modelos de SQLAlchemy (la tecnología de BD)
from .models import User as SQLUser

# El contexto de Passlib es un "detalle de implementación" de este adaptador
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SQLAlchemyAuthRepository(AuthRepositoryPort, PasswordServicePort):
    """
    Esta es la implementación CONCRETA de los puertos de repositorio
    y contraseña, usando SQLAlchemy y Passlib.
    """
    def __init__(self, db: Session):
        self.db = db

    # --- Implementación de PasswordServicePort ---

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    # --- Implementación de AuthRepositoryPort ---

    def get_user_by_username(self, username: str) -> Optional[User]:
        db_user = self.db.query(SQLUser).filter(SQLUser.username == username).first()
        if db_user:
            # Convierte y devuelve el modelo de Dominio (Puro)
            return User.model_validate(db_user)
        return None

    def get_hashed_password(self, username: str) -> Optional[str]:
        db_user = self.db.query(SQLUser).filter(SQLUser.username == username).first()
        if db_user:
            return db_user.password_hash
        return None

    def save_user(self, user_data: UserCreate) -> User:
        hashed_password = self._hash_password(user_data.password)
        db_user = SQLUser(
            username=user_data.username,
            password_hash=hashed_password,
            role="user" # Rol por defecto
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # Convierte y devuelve el modelo de Dominio
        return User.model_validate(db_user)