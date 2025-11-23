# en app/adapters/security/token_service.py

from datetime import datetime, timedelta, timezone
from jose import jwt

from app.domain.ports import TokenServicePort
from app.domain.models import User
from ...config import settings # Importa la configuración (tecnología)

class JWTTokenService(TokenServicePort):
    """
    Implementación concreta del TokenServicePort usando JWT.
    """
    def create_access_token(self, user: User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
        to_encode = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
            "exp": int(expire.timestamp())
        }
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt