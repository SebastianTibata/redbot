# en app/config.py (dentro de auth_service)
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Variables de entorno que este servicio necesita
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int = 30 # Valor por defecto

    class Config:
        # Le dice a Pydantic que lea las variables del archivo .env
        env_file = ".env" 

# Crea la instancia 'settings' que los otros archivos importarán
settings = Settings()