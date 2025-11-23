# en app/adapters/db/sqlalchemy_repository.py

from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext

# Importa el "Puerto" (contrato) que este adaptador debe cumplir
from app.domain.ports import UserRepositoryPort

# Importa los modelos Puros (del Dominio) y los Schemas (DTOs)
from app.domain.models import User
from ...schemas import UserCreate, UserUpdate

# Importa los modelos de SQLAlchemy (la tecnología de BD)
from .models import User as SQLUser

# El contexto de Passlib es un "detalle de implementación" de este adaptador
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SQLAlchemyUserRepository(UserRepositoryPort):
    """
    Esta es la implementación CONCRETA del puerto de repositorio
    usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _get_db_user_by_id(self, user_id: int) -> Optional[SQLUser]:
        """Función helper interna para obtener el objeto SQLAlchemy."""
        return self.db.query(SQLUser).filter(SQLUser.id == user_id).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        db_user = self._get_db_user_by_id(user_id)
        if db_user:
            # Convierte y devuelve el modelo de Dominio (Puro)
            return User.model_validate(db_user)
        return None

    def get_all_users(self) -> List[User]:
        db_users = self.db.query(SQLUser).all()
        # Convierte la lista de SQLAlchemy a una lista de modelos de Dominio
        return [User.model_validate(user) for user in db_users]

    def save_user(self, user_data: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_data.password)
        db_user = SQLUser(
            username=user_data.username,
            password_hash=hashed_password,
            role=user_data.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # Convierte y devuelve el modelo de Dominio
        return User.model_validate(db_user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        db_user = self._get_db_user_by_id(user_id)
        if not db_user:
            return None

        if user_data.username:
            db_user.username = user_data.username
        if user_data.role:
            db_user.role = user_data.role

        self.db.commit()
        self.db.refresh(db_user)
        return User.model_validate(db_user)

    def delete_user(self, user_id: int) -> Optional[User]:
        db_user = self._get_db_user_by_id(user_id)
        if not db_user:
            return None

        # Guardamos una copia del modelo de dominio antes de borrar
        domain_user = User.model_validate(db_user)

        self.db.delete(db_user)
        self.db.commit()
        return domain_user