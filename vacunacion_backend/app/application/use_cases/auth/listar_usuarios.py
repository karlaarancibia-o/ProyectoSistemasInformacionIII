from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository


class ListarUsuarios:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self) -> list[Usuario]:
        return self.repo.listar()
