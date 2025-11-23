from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_bearer_token(credentials=Depends(security)) -> str:
    return credentials.credentials

def get_current_user(token: str = Depends(get_bearer_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id and isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        payload["sub"] = user_id
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
