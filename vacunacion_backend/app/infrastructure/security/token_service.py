import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt

from app.application.interfaces.token_service import TokenService

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60


class JwtTokenService(TokenService):
    def crear(self, data: dict) -> str:
        datos = data.copy()
        datos["exp"] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
        return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

    def decodificar(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None
