# en app/adapters/db/sqlalchemy_repository.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.ports import AccountRepositoryPort
from app.domain.models import Account
from ...schemas import AccountCreate, AccountUpdate
from .models import Account as SQLAccount

class SQLAlchemyAccountRepository(AccountRepositoryPort):
    """
    Esta es la implementación CONCRETA del puerto de repositorio
    usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def save_account(self, account_data: AccountCreate, user_id: int) -> Account:
        db_account = SQLAccount(
            platform=account_data.platform,
            handle=account_data.handle,
            token=account_data.token,
            user_id=user_id
        )
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return Account.model_validate(db_account)

    def get_accounts_by_user_id(self, user_id: int) -> List[Account]:
        db_accounts = self.db.query(SQLAccount).filter(SQLAccount.user_id == user_id).all()
        return [Account.model_validate(acc) for acc in db_accounts]

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        db_account = self.db.query(SQLAccount).filter(SQLAccount.id == account_id).first()
        if db_account:
            return Account.model_validate(db_account)
        return None

    def delete_account(self, account: Account) -> Account:
        db_account = self.db.query(SQLAccount).filter(SQLAccount.id == account.id).first()
        if db_account:
            self.db.delete(db_account)
            self.db.commit()
        return account

    # ▼▼▼ ESTE ES EL MÉTODO QUE FALTA ▼▼▼
    def update_account(self, account_id: int, account_data: AccountUpdate) -> Optional[Account]:
        db_account = self.db.query(SQLAccount).filter(SQLAccount.id == account_id).first()
        
        if not db_account:
            return None
        
        # Actualiza los campos
        if account_data.handle:
            db_account.handle = account_data.handle
        if account_data.token:
            db_account.token = account_data.token
        
        self.db.commit()
        self.db.refresh(db_account)
        
        return Account.model_validate(db_account)