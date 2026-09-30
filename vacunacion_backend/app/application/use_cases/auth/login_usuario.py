from app.application.interfaces.password_hasher import PasswordHasher
from app.application.interfaces.token_service import TokenService
from app.domain.exceptions import CredencialesInvalidasError, PermisoDenegadoError
from app.domain.repositories.usuario_repository import UsuarioRepository


class LoginUsuario:
    def __init__(
        self,
        repo: UsuarioRepository,
        hasher: PasswordHasher,
        tokens: TokenService,
    ):
        self.repo = repo
        self.hasher = hasher
        self.tokens = tokens

    def ejecutar(self, username: str, password: str) -> str:
        """Devuelve el access token. El router lo envuelve en el schema Token."""
        usuario = self.repo.obtener_por_username(username)
        if not usuario or not self.hasher.verificar(password, usuario.password_hash):
            raise CredencialesInvalidasError()
        if not usuario.activo:
            raise PermisoDenegadoError("La cuenta está desactivada")

        return self.tokens.crear({"sub": usuario.username, "rol": usuario.rol})
