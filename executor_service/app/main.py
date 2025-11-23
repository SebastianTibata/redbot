

from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer
from .executor import routes as executor_routes
from .database import Base, engine
from .models import ExecutionLog

Base.metadata.create_all(bind=engine)

security_scheme = HTTPBearer()

app = FastAPI(title="Executor Service")
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(executor_routes.router, prefix="/executor", tags=["Executor"])

# Agrega el esquema de seguridad global para Swagger UI
app.openapi_schema = None
from fastapi.openapi.utils import get_openapi
def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title=app.title,
		version=app.version,
		description=app.description,
		routes=app.routes,
	)
	openapi_schema["components"]["securitySchemes"] = {
		"HTTPBearer": {
			"type": "http",
			"scheme": "bearer"
		}
	}
	for path in openapi_schema["paths"].values():
		for method in path.values():
			method.setdefault("security", [{"HTTPBearer": []}])
	app.openapi_schema = openapi_schema
	return app.openapi_schema
app.openapi = custom_openapi
