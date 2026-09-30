from app.domain.entities.usuario import Usuario
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.usuario_repository import UsuarioRepository


class CambiarEstadoUsuario:
    """Un administrador activa o desactiva una cuenta (un usuario desactivado
    no puede iniciar sesión ni usar su token)."""

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: int, activo: bool, actor: Usuario) -> Usuario:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise NoEncontradoError("Usuario no encontrado")

        if not activo:
            if usuario.id == actor.id:
                raise OperacionNoPermitidaError("No puede desactivar su propia cuenta")
            if (
                usuario.es_administrador
                and usuario.activo
                and self.repo.contar_administradores_activos() <= 1
            ):
                raise OperacionNoPermitidaError(
                    "No se puede desactivar al único administrador activo"
                )
        usuario.activo = activo
        return self.repo.actualizar(usuario)
