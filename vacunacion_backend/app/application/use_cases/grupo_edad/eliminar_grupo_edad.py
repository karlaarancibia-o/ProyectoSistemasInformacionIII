from app.application.use_cases.grupo_edad.obtener_grupo_edad import ObtenerGrupoEdad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


class EliminarGrupoEdad:
    def __init__(self, repo: GrupoEdadRepository):
        self.repo = repo

    def ejecutar(self, grupo_id: int) -> None:
        ObtenerGrupoEdad(self.repo).ejecutar(grupo_id)
        self.repo.eliminar(grupo_id)
