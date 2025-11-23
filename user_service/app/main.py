# en app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Importaciones de Adaptadores (Tecnología) ---
from .adapters.http import routes as user_routes
from .database import engine

# Crea las tablas (usando los modelos de SQLAlchemy en adapters/db/models.py)
from .adapters.db import models as db_models
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service (Hexagonal)")

# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas del adaptador HTTP
app.include_router(user_routes.router)