from app.domain.entities.usuario import Usuario
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.domain.roles import ADMINISTRADOR, validar_rol


class CambiarRolUsuario:
    """Un administrador cambia el rol de un usuario. El sistema no puede
    quedarse sin administradores activos."""

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: int, nuevo_rol: str) -> Usuario:
        usuario = self.repo.obtener_por_id(usuario_id)
        if not usuario:
            raise NoEncontradoError("Usuario no encontrado")

        nuevo_rol = validar_rol(nuevo_rol)
        if (
            usuario.rol == ADMINISTRADOR
            and usuario.activo
            and nuevo_rol != ADMINISTRADOR
            and self.repo.contar_administradores_activos() <= 1
        ):
            raise OperacionNoPermitidaError(
                "No se puede quitar el rol al único administrador activo"
            )
        usuario.rol = nuevo_rol
        return self.repo.actualizar(usuario)
