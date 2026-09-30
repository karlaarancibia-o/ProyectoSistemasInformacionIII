from app.application.interfaces.password_hasher import PasswordHasher
from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.domain.roles import ADMINISTRADOR


class AsegurarAdministradorInicial:
    """Al arrancar: si no hay ningún administrador activo y se configuraron
    ADMIN_USERNAME / ADMIN_PASSWORD, crea ese usuario como administrador (o,
    si ya existe, lo promueve y lo activa)."""

    def __init__(self, repo: UsuarioRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    def ejecutar(self, username: str | None, password: str | None) -> Usuario | None:
        if not username or not password:
            return None
        if self.repo.contar_administradores_activos() > 0:
            return None

        existente = self.repo.obtener_por_username(username)
        if existente:
            existente.rol = ADMINISTRADOR
            existente.activo = True
            return self.repo.actualizar(existente)
        return self.repo.crear(
            Usuario(
                username=username,
                password_hash=self.hasher.hashear(password),
                rol=ADMINISTRADOR,
            )
        )
