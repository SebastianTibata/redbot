# en app/domain/use_cases.py

from fastapi import HTTPException, status
from typing import Dict

# Importa los "Puertos" (contratos)
from .ports import AuthRepositoryPort, TokenServicePort, PasswordServicePort

# Importa los DTOs (schemas)
from ..schemas import UserCreate, UserLogin

class AuthUseCases:
    """
    Esta clase contiene la lógica de negocio pura (Casos de Uso).
    No sabe nada de bases de datos o tokens. Solo habla con "Puertos".
    """
    def __init__(
        self, 
        auth_repo: AuthRepositoryPort, 
        token_service: TokenServicePort,
        password_service: PasswordServicePort
    ):
        self.auth_repo = auth_repo
        self.token_service = token_service
        self.password_service = password_service

    def register_new_user(self, user_data: UserCreate):
        # Lógica de negocio: verificar si el usuario ya existe
        db_user = self.auth_repo.get_user_by_username(user_data.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El nombre de usuario ya está en uso."
            )

        # Llama al puerto del repositorio para guardar
        return self.auth_repo.save_user(user_data)

    def login_user(self, user_data: UserLogin) -> Dict[str, str]:
        # Lógica de negocio: autenticar al usuario

        # 1. Obtener la contraseña hash
        hashed_password = self.auth_repo.get_hashed_password(user_data.username)

        # 2. Verificar la contraseña
        if not hashed_password or not self.password_service.verify_password(
            user_data.password, 
            hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Usuario o contraseña incorrectos."
            )

        # 3. Obtener el usuario completo (para el token)
        user = self.auth_repo.get_user_by_username(user_data.username)

        # 4. Crear el token
        token = self.token_service.create_access_token(user)

        return {"access_token": token, "token_type": "bearer"}