from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


class ListarGruposEdad:
    def __init__(self, repo: GrupoEdadRepository):
        self.repo = repo

    def ejecutar(self) -> list[GrupoEdad]:
        return self.repo.listar()
