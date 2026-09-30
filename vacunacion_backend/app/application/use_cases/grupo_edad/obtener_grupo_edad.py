from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


class ObtenerGrupoEdad:
    def __init__(self, repo: GrupoEdadRepository):
        self.repo = repo

    def ejecutar(self, grupo_id: int) -> GrupoEdad:
        grupo = self.repo.obtener_por_id(grupo_id)
        if not grupo:
            raise NoEncontradoError("Grupo de edad no encontrado")
        return grupo
