import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Variables de entorno existentes
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    
    # Nueva variable para Google
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    class Config:
        # Le dice a Pydantic que lea las variables del archivo .env
        env_file = ".env" 

# Crea la instancia 'settings' que los otros archivos (como services.py) importarán
settings = Settings()