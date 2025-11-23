from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        # Pydantic buscará automáticamente variables de entorno.
        # env_file es un respaldo útil para pruebas locales.
        env_file = ".env"

settings = Settings()

print(f"✅ ACCOUNT_SERVICE usa la SECRET_KEY: '{settings.SECRET_KEY}'")