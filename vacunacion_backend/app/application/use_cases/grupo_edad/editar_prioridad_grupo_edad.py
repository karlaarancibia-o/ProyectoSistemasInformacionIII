from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


class EditarPrioridadGrupoEdad:
    """Complementa el evento 2 (diagrama nivel 2: '2. Editar prioridad')."""

    def __init__(self, repo: GrupoEdadRepository):
        self.repo = repo

    def ejecutar(self, grupo_id: int, nueva_prioridad: int) -> GrupoEdad:
        grupo = self.repo.obtener_por_id(grupo_id)
        if not grupo:
            raise NoEncontradoError("Grupo de edad no encontrado")
        grupo.prioridad = nueva_prioridad
        GrupoEdad(**vars(grupo))  # revalida invariantes del dominio
        return self.repo.actualizar(grupo)
