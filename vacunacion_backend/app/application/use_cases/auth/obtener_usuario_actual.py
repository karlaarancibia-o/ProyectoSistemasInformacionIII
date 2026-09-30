from app.application.interfaces.token_service import TokenService
from app.domain.entities.usuario import Usuario
from app.domain.exceptions import NoAutenticadoError
from app.domain.repositories.usuario_repository import UsuarioRepository


class ObtenerUsuarioActual:
    def __init__(self, repo: UsuarioRepository, tokens: TokenService):
        self.repo = repo
        self.tokens = tokens

    def ejecutar(self, token: str) -> Usuario:
        payload = self.tokens.decodificar(token)
        if payload is None:
            raise NoAutenticadoError("Token inválido o expirado")

        usuario = self.repo.obtener_por_username(payload.get("sub"))
        if usuario is None:
            raise NoAutenticadoError("Usuario no encontrado")
        if not usuario.activo:
            raise NoAutenticadoError("La cuenta está desactivada")

        # el rol vigente es el de la base de datos, no el que traía el token
        return usuario
