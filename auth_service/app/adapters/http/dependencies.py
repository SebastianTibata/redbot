# auth_service/app/auth/dependencies.py

from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from ...config import SECRET_KEY, JWT_ALGORITHM
from ...database import SessionLocal
from ..db.models import User

security = HTTPBearer()  # extrae automáticamente Authorization: Bearer <token>

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependencia que devuelve el objeto User asociado al token.
    Lanza 401 si el token es inválido o no existe el usuario.
    """
    token = credentials.credentials
    payload = decode_token(token)

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependencia que asegura que el usuario actual tenga rol 'admin'.
    Lanza 403 si no es admin.
    """
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: requiere rol admin")
    return current_user
