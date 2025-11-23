# en app/main.py

from fastapi import FastAPI
from .adapters.http import routes as task_routes
from .database import engine
from .adapters.db import models as db_models

# Crea las tablas (usando los modelos de SQLAlchemy en adapters/db/models.py)
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Service (Hexagonal)")

# Incluimos las rutas del adaptador HTTP
app.include_router(task_routes.router)

# (Aquí puedes añadir tu middleware de CORS si es necesario)