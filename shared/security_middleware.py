"""
Middleware de seguridad para proteger el acceso a la aplicación RedBot.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import sys
import os

# Agregar el directorio padre al path para importar security_config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.security_config import security_config


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware que verifica la autenticación de acceso a la aplicación.
    Soporta autenticación simétrica (X-Master-Key) o asimétrica (X-Access-Token + X-Access-Signature).
    """

    def __init__(self, app, exclude_paths: list = None):
        super().__init__(app)
        # Rutas que no requieren autenticación adicional
        self.exclude_paths = exclude_paths or [
            '/docs',
            '/redoc',
            '/openapi.json',
            '/health',
            '/api/auth/login',
            '/api/auth/register',
        ]

    async def dispatch(self, request: Request, call_next: Callable):
        # Verificar si la ruta está excluida
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Si la protección está deshabilitada, permitir el acceso
        if not security_config.is_enabled():
            return await call_next(request)

        # Verificar autenticación según el tipo
        if security_config.auth_type == 'symmetric':
            master_key = request.headers.get('X-Master-Key')
            if not master_key or not security_config.verify_symmetric_key(master_key):
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Acceso denegado: llave maestra inválida o faltante",
                        "auth_type": "symmetric",
                        "hint": "Proporcione la llave maestra en el header 'X-Master-Key'"
                    }
                )

        elif security_config.auth_type == 'asymmetric':
            access_token = request.headers.get('X-Access-Token')
            access_signature = request.headers.get('X-Access-Signature')

            if not access_token or not access_signature:
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Acceso denegado: token o firma faltante",
                        "auth_type": "asymmetric",
                        "hint": "Proporcione 'X-Access-Token' y 'X-Access-Signature' en los headers"
                    }
                )

            if not security_config.verify_signed_token(access_token, access_signature):
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Acceso denegado: token o firma inválida",
                        "auth_type": "asymmetric"
                    }
                )

        # Si la autenticación es exitosa, continuar con el request
        return await call_next(request)


def setup_security_middleware(app, exclude_paths: list = None):
    """
    Configura el middleware de seguridad en una aplicación FastAPI.

    Args:
        app: Instancia de FastAPI
        exclude_paths: Lista de rutas que no requieren autenticación adicional
    """
    app.add_middleware(SecurityMiddleware, exclude_paths=exclude_paths)
    print(f"Middleware de seguridad configurado (Tipo: {security_config.auth_type})")
